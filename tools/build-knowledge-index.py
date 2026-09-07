#!/usr/bin/env python3
"""Export a searchable index for knowledge-only packs.

These packs have no eight-arts page. The index is for retrieval, not fake charts.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "references/inventory/library-inventory.json"
PARA_DIR = ROOT / "references/inventory/paragraphs"
OUT = ROOT / "references/inventory/knowledge-index.json"


def main() -> None:
    inventory = json.loads(INV.read_text(encoding="utf-8"))
    packs = []
    for pack in inventory["packs"]:
        if pack.get("destination") != "knowledge":
            continue
        para_path = PARA_DIR / pack["system"] / f"{pack['slug']}.json"
        samples = []
        if para_path.is_file():
            payload = json.loads(para_path.read_text(encoding="utf-8"))
            for para in payload.get("paragraphs") or []:
                if para.get("kind") != "理论":
                    continue
                if para.get("doubtful") or para.get("missing_marker"):
                    continue
                if int(para.get("char_count") or 0) < 20:
                    continue
                samples.append(
                    {
                        "id": para["id"],
                        "heading": para.get("heading") or "",
                        "start_line": para["start_line"],
                        "end_line": para["end_line"],
                    }
                )
                if len(samples) >= 5:
                    break
        packs.append(
            {
                "slug": pack["slug"],
                "title": pack["title"],
                "system": pack["system"],
                "art": pack.get("art"),
                "art_label": pack.get("art_label"),
                "fulltext": pack.get("actual_fulltext_path"),
                "paragraph_count": pack.get("paragraph_count"),
                "purpose": pack.get("purpose") or "searchable_knowledge",
                "not_an_art_page": True,
                "sample_paragraphs": samples,
            }
        )
    payload = {
        "schema_version": "fateradar-knowledge-index-v1",
        "note": "风水/相法/择日/姓名等暂无对应页面。本索引供检索，不冒充已接入八术。",
        "pack_count": len(packs),
        "packs": packs,
        "web_contract": {
            "lookup": "slug + paragraph id",
            "fields": ["slug", "title", "system", "sample_paragraphs.id", "fulltext"],
            "do_not": ["cast as bazi/ziwei/qimen chart", "invent eight-arts verdicts"],
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"knowledge packs {len(packs)} -> {OUT}")


if __name__ == "__main__":
    main()
