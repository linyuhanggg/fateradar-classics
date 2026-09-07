#!/usr/bin/env python3
"""Validate semantic annotations against real paragraph IDs; no human-verification promotion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

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
    paragraphs: dict[str, dict] = {}
    for path in sorted((ROOT / "references/inventory/paragraphs").glob("*/*.json")):
        for paragraph in json.loads(path.read_text())["paragraphs"]:
            paragraphs[paragraph["id"]] = paragraph
    errors: list[str] = []
    books = entries = reviewed = 0
    for path in sorted(args.annotations.glob("*/*.json")):
        data = json.loads(path.read_text())
        errors.extend(validate_pack(data, paragraphs))
        books += 1
        entries += len(data.get("entries", []))
        reviewed += sum(e.get("review") == "source-reviewed" for e in data.get("entries", []) if isinstance(e, dict))
    result = {"ok": not errors, "books": books, "entries": entries, "source_reviewed": reviewed,
              "note": "Structural and source-ID checks only; not a semantic or human review certificate.", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"{books} books, {entries} entries, {len(errors)} errors\n" + "\n".join(errors))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
