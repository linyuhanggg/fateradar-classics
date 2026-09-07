#!/usr/bin/env python3
"""Validate semantic annotations against real paragraph IDs; no human-verification promotion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from source_paragraphs import load_source_paragraphs

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"理论", "规则候选", "案例", "操作步骤", "术语", "序跋目录", "重复", "待核实", "评注或元数据", "待分类"}


def validate_pack(data: dict, paragraphs: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    slug = data.get("bookSlug")
    if not isinstance(slug, str) or not slug:
        return ["bookSlug must identify an existing source book"]
    if not any(key.startswith(slug + ":") for key in paragraphs):
        errors.append(f"Unknown book: {slug}")
    entries = data.get("entries")
    if not isinstance(entries, list):
        return errors + [f"{slug}: entries must be an array"]
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append(f"{slug}: annotation must be an object")
            continue
        key = entry.get("paragraphId")
        if not isinstance(key, str) or key not in paragraphs or not key.startswith(slug + ":"):
            errors.append(f"{slug}: unknown paragraphId {key}")
        elif key in seen:
            errors.append(f"{slug}: duplicate paragraphId {key}")
        else:
            seen.add(key)
        if entry.get("kind") not in KINDS:
            errors.append(f"{key}: unsupported kind")
        if entry.get("review") not in {"draft", "source-reviewed"}:
            errors.append(f"{key}: review must be draft or source-reviewed")
        if not isinstance(entry.get("vernacular"), str) or not entry["vernacular"].strip():
            errors.append(f"{key}: nonempty explanation or disposition required")
        for field in ("terms", "notes"):
            value = entry.get(field)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{key}: {field} must be an array of nonempty strings")
        source = paragraphs.get(key, {}) if isinstance(key, str) else {}
        if source.get("source_status") == "ocr-draft" and entry.get("review") == "source-reviewed":
            errors.append(f"{key}: OCR draft requires transcription review before source-reviewed annotation")
        if entry.get("verified") is True:
            errors.append(f"{key}: source review is not human verified")
        related = entry.get("relatedParagraphIds", [])
        if not isinstance(related, list) or any(not isinstance(item, str) or item not in paragraphs for item in related):
            errors.append(f"{key}: related paragraph does not exist")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--annotations", type=Path, default=ROOT / "references/annotations")
    args = parser.parse_args()
    paragraphs = load_source_paragraphs(ROOT)
    errors: list[str] = []
    entries = reviewed = 0
    book_slugs = set()
    seen_ids = set()
    if args.annotations.is_file():
        files = [args.annotations]
    elif args.annotations.is_dir():
        files = sorted(args.annotations.rglob("*.json"))
    else:
        files = []
    if not files:
        errors.append(f"No annotation JSON files found: {args.annotations}")
    for path in files:
        data = json.loads(path.read_text())
        errors.extend(validate_pack(data, paragraphs))
        if isinstance(data.get("bookSlug"), str):
            book_slugs.add(data["bookSlug"])
        for entry in data.get("entries", []):
            key = entry.get("paragraphId") if isinstance(entry, dict) else None
            if isinstance(key, str):
                if key in seen_ids:
                    errors.append(f"Duplicate annotation across files: {key}")
                seen_ids.add(key)
        entries += len(data.get("entries", []))
        reviewed += sum(e.get("review") == "source-reviewed" for e in data.get("entries", []) if isinstance(e, dict))
    books = len(book_slugs)
    result = {"ok": not errors, "books": books, "files": len(files), "entries": entries, "source_reviewed": reviewed,
              "note": "Structural and source-ID checks only; not a semantic or human review certificate.", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"{books} books, {entries} entries, {len(errors)} errors\n" + "\n".join(errors))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
