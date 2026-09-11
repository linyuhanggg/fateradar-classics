#!/usr/bin/env python3
"""Report supplemental source progress separately from the unchanged primary index."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from source_paragraphs import load_source_paragraphs, supplemental_editions

ROOT = Path(__file__).resolve().parents[1]


def build(root: Path) -> dict:
    paragraphs = load_source_paragraphs(root)
    annotations = {}
    for path in sorted((root / "references/annotations").glob("*/*.json")):
        for entry in json.loads(path.read_text())["entries"]:
            key = entry["paragraphId"]
            if key in annotations:
                raise ValueError(f"Duplicate annotation across files: {key}")
            annotations[key] = entry
    editions = []
    for edition in supplemental_editions(root):
        prefix = f"{edition['bookSlug']}:{edition['id']}:"
        rows = [p for key, p in paragraphs.items() if key.startswith(prefix)]
        attached = [annotations[p["id"]] for p in rows if p["id"] in annotations]
        statuses = Counter(p["source_status"] for p in rows)
        editions.append({"id": edition["id"], "bookSlug": edition["bookSlug"], "label": edition["label"], "file": edition["file"],
                         "paragraphs": len(rows), "sourceStates": dict(statuses), "annotations": len(attached),
                         "reviewedBodyExplanations": sum(e["review"] == "source-reviewed" and e["kind"] not in {"评注或元数据", "序跋目录"} for e in attached)})
    return {"version": 1, "note": "补充/恢复来源单列，不改变主索引53640段口径；图文核对不等于语义解读或算法验证。", "editions": editions}


def main():
    data = build(ROOT)
    (ROOT / "references/inventory/source-editions.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    lines = ["# 补充与恢复来源进度", "", data["note"], "", "| 来源 | 片段 | 来源状态 | 注解 | 已审正文白话 |", "|---|---:|---|---:|---:|"]
    for item in data["editions"]:
        states = "、".join(f"{key}: {value}" for key, value in item["sourceStates"].items())
        lines.append(f"| {item['label']} | {item['paragraphs']} | {states} | {item['annotations']} | {item['reviewedBodyExplanations']} |")
    lines += ["", "reference-text表示收录的补充对照文字；ocr-draft表示未校识别稿；page-reviewed仅限已核整页，passage-reviewed仅限已核正文范围。未校字句不得因相邻页已校而升级。", "", "可靠知识导出使用已提交源快照，工作中的校稿变化要提交后才进入下一版本。"]
    (ROOT / "docs/SOURCE_EDITIONS_INVENTORY.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"editions": len(data["editions"]), "paragraphs": sum(x["paragraphs"] for x in data["editions"]), "body_explanations": sum(x["reviewedBodyExplanations"] for x in data["editions"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
