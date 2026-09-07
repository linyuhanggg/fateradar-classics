#!/usr/bin/env python3
"""Export source paragraphs and separately reviewed annotations for product search."""
from __future__ import annotations

import argparse
import importlib.util
import io
import tarfile
import tempfile
import json
import subprocess
from pathlib import Path
from opencc import OpenCC
from source_paragraphs import load_source_paragraphs

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
    sources = load_source_paragraphs(root)
    book_map = {book["slug"]: book for book in books}
    source_lines = {}
    for paragraph in sources.values():
        slug = paragraph["id"].split(":", 1)[0]
        if slug not in book_map:
            raise ValueError(f"Source edition has no included book: {slug}")
        source_file = paragraph["source_file"]
        if source_file not in source_lines:
            source_lines[source_file] = (root / source_file).read_text().splitlines()
        lines = source_lines[source_file]
        start, end = paragraph["start_line"], paragraph["end_line"]
        if not 1 <= start <= end <= len(lines):
            raise ValueError(f"Invalid source range: {paragraph['id']}")
        row = {"id": paragraph["id"], "bookSlug": slug, "heading": paragraph["heading"],
               "text": "\n".join(lines[start - 1:end]), "kind": paragraph["kind"],
               "startLine": start, "endLine": end, "terms": [], "notes": [], "review": "unreviewed"}
        if source_file != book_map[slug]["fulltext"]:
            row.update({"sourceFile": source_file, "sourceLabel": paragraph.get("source_label", "补充来源"),
                        "sourceStatus": paragraph["source_status"], "notes": paragraph.get("source_notes", [])})
            if paragraph.get("pdf_page", 0) > 0:
                row["pdfPage"] = paragraph["pdf_page"]
        rows.append(row)
        paragraph_map[row["id"]] = row
    for book in books:
        book["paragraphCount"] = sum(row["bookSlug"] == book["slug"] for row in rows)
    for path in sorted((root / "references/annotations").glob("*/*.json")):
        data = json.loads(path.read_text())
        errors = annotation_validation.validate_pack(data, sources)
        if errors:
            raise ValueError(f"{path}: " + "; ".join(errors))
        for entry in data["entries"]:
            row = paragraph_map[entry["paragraphId"]]
            for field in ("kind", "vernacular", "terms", "notes", "review", "relatedParagraphIds"):
                if field in entry:
                    row[field] = list(dict.fromkeys(row[field] + entry[field])) if field == "notes" else entry[field]
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
    # Publish only a committed source snapshot. OCR page edits can otherwise shift
    # global line anchors while the export still labels itself with the old HEAD.
    source_paths = ["references/inventory", "references/annotations", "references/source-editions.json", "references/source-quality.json", "sources/fulltext", "sources/normalized"]
    present = [path for path in source_paths if subprocess.check_output(["git", "ls-tree", "HEAD", "--", path], cwd=ROOT)]
    archive = subprocess.check_output(["git", "archive", "--format=tar", "HEAD", "--", *present], cwd=ROOT)
    with tempfile.TemporaryDirectory(prefix="fateradar-knowledge-export-") as folder:
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(folder, filter="data")
        data = build_export(Path(folder), revision)
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
