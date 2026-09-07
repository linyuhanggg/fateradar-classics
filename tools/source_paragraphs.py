"""Shared source paragraph loading; retained primary IDs plus separately named editions."""
from __future__ import annotations
import json
import re
from pathlib import Path

PAGE = re.compile(r"^## PDF第(\d+)页")
HEADING = re.compile(r"^#{1,6}\s+(.+)$")


def split_edition(edition: dict, lines: list[str]) -> list[dict]:
    paragraphs = []
    buffer = []
    heading = edition["label"]
    page, page_line = 0, 0

    def flush():
        if not buffer:
            return
        start, end = buffer[0], buffer[-1]
        if edition.get("pageScoped"):
            suffix = f"P{page:03d}:L{start - page_line:03d}-L{end - page_line:03d}"
        else:
            suffix = f"L{start:04d}-L{end:04d}"
        text = "\n".join(lines[start-1:end])
        metadata = all(not line.strip() or line.lstrip().startswith((">", "<!--", "Source:", "来源：")) for line in text.splitlines())
        row = {"id": f"{edition['bookSlug']}:{edition['id']}:{suffix}",
               "start_line": start, "end_line": end, "heading": heading,
               "kind": "评注或元数据" if metadata else "待分类",
               "source_file": edition["file"], "source_label": edition["label"],
               "source_status": edition["sourceStatus"], "source_notes": edition.get("notes", [])}
        if edition.get("pageScoped"):
            row["pdf_page"] = page
        paragraphs.append(row)
        buffer.clear()

    for number, line in enumerate(lines, 1):
        match = HEADING.match(line)
        if match:
            flush()
            heading = match.group(1)
            match_page = PAGE.match(line)
            if match_page:
                page, page_line = int(match_page.group(1)), number
        elif not line.strip():
            flush()
        else:
            buffer.append(number)
    flush()
    return paragraphs


def supplemental_editions(root: Path) -> list[dict]:
    registry = root / "references/source-editions.json"
    if not registry.exists():
        return []
    data = json.loads(registry.read_text())
    return data["editions"]


def load_source_paragraphs(root: Path) -> dict[str, dict]:
    result = {}
    for path in sorted((root / "references/inventory/paragraphs").glob("*/*.json")):
        data = json.loads(path.read_text())
        for paragraph in data["paragraphs"]:
            row = {**paragraph, "source_file": data["fulltext"], "source_status": "reference-text"}
            if row["id"] in result:
                raise ValueError(f"Duplicate paragraph ID: {row['id']}")
            result[row["id"]] = row
    for edition in supplemental_editions(root):
        for row in split_edition(edition, (root / edition["file"]).read_text().splitlines()):
            if row["id"] in result:
                raise ValueError(f"Duplicate edition paragraph ID: {row['id']}")
            result[row["id"]] = row
    return result
