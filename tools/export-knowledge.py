#!/usr/bin/env python3
"""Export source paragraphs and separately reviewed annotations for product search."""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("annotation_validation", ROOT / "tools/validate-annotations.py")
annotation_validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(annotation_validation)


def build_export(root: Path, revision: str) -> dict:
    inventory = json.loads((root / "references/inventory/library-inventory.json").read_text())
    quality_path = root / "references/source-quality.json"
    quality = {book["slug"]: book for book in json.loads(quality_path.read_text())["books"]} if quality_path.exists() else {}
    books = []
    rows = []
    paragraph_map = {}
    for pack in inventory["packs"]:
        if not pack["fulltext_exists"] or pack["destination"] in {"excluded_copyright", "blocked_or_excluded"}:
            continue
        slug, system = pack["slug"], pack["system"]
        fulltext = pack["actual_fulltext_path"]
        lines = (root / fulltext).read_text().splitlines()
        paragraph_file = root / "references/inventory/paragraphs" / system / f"{slug}.json"
        data = json.loads(paragraph_file.read_text())
        books.append({"slug": slug, "title": pack["title"], "system": system,
                      "fulltext": fulltext, "paragraphCount": len(data["paragraphs"]),
                      "textStatus": quality.get(slug, {}).get("status", "unassessed"),
                      "sourceNotes": quality.get(slug, {}).get("notes", [])})
        for paragraph in data["paragraphs"]:
            start, end = paragraph["start_line"], paragraph["end_line"]
            if not 1 <= start <= end <= len(lines):
                raise ValueError(f"Invalid source range: {paragraph['id']}")
            if paragraph["id"] in paragraph_map:
                raise ValueError(f"Duplicate source paragraph: {paragraph['id']}")
            row = {"id": paragraph["id"], "bookSlug": slug, "heading": paragraph["heading"],
                   "text": "\n".join(lines[start - 1:end]), "kind": paragraph["kind"],
                   "startLine": start, "endLine": end, "terms": [], "notes": [], "review": "unreviewed"}
            rows.append(row)
            paragraph_map[row["id"]] = row
    for path in sorted((root / "references/annotations").glob("*/*.json")):
        data = json.loads(path.read_text())
        errors = annotation_validation.validate_pack(data, paragraph_map)
        if errors:
            raise ValueError(f"{path}: " + "; ".join(errors))
        for entry in data["entries"]:
            row = paragraph_map[entry["paragraphId"]]
            for field in ("kind", "vernacular", "terms", "notes", "review", "relatedParagraphIds"):
                if field in entry:
                    row[field] = entry[field]
    simplified, traditional = OpenCC("t2s"), OpenCC("s2t")
    book_titles = {book["slug"]: book["title"] for book in books}
    for row in rows:
        searchable = "\n".join([book_titles[row["bookSlug"]], row["heading"], row["text"], row.get("vernacular", ""), " ".join(row["terms"])])
        alternatives = dict.fromkeys([simplified.convert(searchable), traditional.convert(searchable)])
        alternatives.pop(searchable, None)
        if alternatives:
            row["searchText"] = "\n".join(alternatives)
    return {"version": 1, "sourceRevision": revision, "books": books, "paragraphs": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/knowledge/library.json")
    args = parser.parse_args()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    data = build_export(ROOT, revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # One paragraph per line keeps regenerated data reviewable in Git.
    header = {key: value for key, value in data.items() if key != "paragraphs"}
    body = ",\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in data["paragraphs"])
    args.output.write_text(json.dumps(header, ensure_ascii=False, separators=(",", ":"))[:-1] + ',"paragraphs":[\n' + body + '\n]}\n')
    print(json.dumps({"books": len(data["books"]), "paragraphs": len(data["paragraphs"]),
                      "source_reviewed": sum(p["review"] == "source-reviewed" for p in data["paragraphs"]),
                      "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
