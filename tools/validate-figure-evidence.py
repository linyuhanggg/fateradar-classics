#!/usr/bin/env python3
"""Check recovered figure provenance and actual source/annotation connections."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from source_paragraphs import load_source_paragraphs

ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path) -> dict:
    paragraphs = load_source_paragraphs(root)
    annotations = {}
    for path in (root / "references/annotations").rglob("*.json"):
        for entry in json.loads(path.read_text()).get("entries", []):
            annotations[entry["paragraphId"]] = entry
    errors, seen, owners = [], set(), {}
    for path in sorted((root / "sources/normalized").rglob("figure-transcriptions.json")):
        pack = json.loads(path.read_text())
        manifests = json.loads((path.parent / "figure-recovery-manifest.json").read_text())
        manifest = {item["file"]: item for item in manifests}
        used = set()
        for entry in pack["entries"]:
            key, pid = entry["id"], entry["paragraphId"]
            if key in seen or not key.startswith(pid + ":figure-"):
                errors.append(f"{key}: invalid or duplicate figure ID")
            seen.add(key)
            owners[key] = pid
            if pid not in paragraphs or key not in annotations.get(pid, {}).get("figureEvidenceIds", []):
                errors.append(f"{key}: missing source/annotation connection")
            source = paragraphs.get(pid, {})
            source_lines = (root / source["source_file"]).read_text().splitlines() if source else []
            source_text = "\n".join(source_lines[source.get("start_line", 1)-1:source.get("end_line", 0)])
            if key not in source_text:
                errors.append(f"{key}: source paragraph does not link evidence")
            file = entry["imageFile"]
            local = (root / file).resolve()
            if not local.is_relative_to(root.resolve()) or not local.is_file():
                errors.append(f"{key}: missing or out-of-repository image")
                continue
            digest = hashlib.sha256(local.read_bytes()).hexdigest()
            original = manifest.get(file, {})
            if digest != entry["sha256"] or digest != original.get("sha256"):
                errors.append(f"{key}: image hash mismatch")
            if local.stat().st_size != original.get("bytes"):
                errors.append(f"{key}: image size mismatch")
            if not pid.endswith(":P" + original.get("paragraphId", "")):
                errors.append(f"{key}: recovered image belongs to another paragraph")
            used.add(file)
            if entry.get("review") != "image-read" or not entry.get("description"):
                errors.append(f"{key}: image reading not recorded")
            status = entry.get("textStatus")
            if status not in {"partial", "transcribed", "no-legible-caption"}:
                errors.append(f"{key}: unknown text status")
            if status == "transcribed" and not entry["captionTranscription"].strip():
                errors.append(f"{key}: transcribed caption must not be empty")
            if status == "no-legible-caption" and entry["captionTranscription"].strip():
                errors.append(f"{key}: caption contradicts no-legible-caption status")
            if "□" in entry["captionTranscription"] and (status != "partial" or not entry.get("unresolved")):
                errors.append(f"{key}: undecided glyph hidden by completion status")
        if used != set(manifest):
            errors.append(f"{path}: recovery manifest and evidence disagree")
    for pid, entry in annotations.items():
        for key in entry.get("figureEvidenceIds", []):
            if key not in seen:
                errors.append(f"{pid}: dangling figure evidence {key}")
            elif owners[key] != pid:
                errors.append(f"{pid}: figure evidence belongs to {owners[key]}")
    return {"ok": not errors, "figures": len(seen), "errors": errors,
            "note": "Provenance and linkage checks only; transcription needs image review."}


if __name__ == "__main__":
    result = validate(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(not result["ok"])
