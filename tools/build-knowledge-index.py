#!/usr/bin/env python3
"""Export a searchable index for knowledge-only packs.

These packs have no eight-arts page. The index is for retrieval, not fake charts.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "references/inventory/library-inventory.json"
PARA_DIR = ROOT / "references/inventory/paragraphs"
OUT = ROOT / "references/inventory/knowledge-index.json"


def source_revision() -> str:
    """导出所用的古籍仓 commit。

    与 `export-knowledge.py` 等导出脚本同一约定（`git rev-parse HEAD`）：产物必须能对回
    具体版本，否则「内容导出与代码版本可对应」这一条不成立。此前本脚本不写该字段，
    重新生成会**静默丢掉**已提交产物里的 `sourceRevision`，属于回退，故补上。
    """
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return ""


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
            paragraphs = sorted(payload.get("paragraphs") or [], key=lambda p: (
                p.get("annotation_review") != "source-reviewed",
                not p.get("has_vernacular", False),
            ))
            for para in paragraphs:
                if para.get("kind") in {"序跋目录", "评注或元数据", "重复"}:
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
                        "kind": para["kind"],
                        "classification_method": para.get("classification_method", "unclassified"),
                        "annotation_review": para.get("annotation_review"),
                        "has_vernacular": bool(para.get("has_vernacular")),
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
        "sourceRevision": source_revision(),
        "note": "风水/相法/择日/姓名等暂无对应页面。本索引供检索，不冒充已接入八术。原文样本可以尚未分类或注解；电子审读和白话状态按字段明示，不把检索样本当作审读完成。",
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
