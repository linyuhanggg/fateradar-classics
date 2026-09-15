#!/usr/bin/env python3
"""Edition coverage: expected chapters vs collected chapters vs missing chapters, with evidence.

For every edition in references/source-editions.json this reports the site-declared
chapter list against what the repository actually holds, and records the provenance of
each number so the comparison is checkable. Web-catalogue completeness and true
ancient-edition completeness are reported in separate columns and never merged.

Writes docs/closeout/EDITION_COVERAGE.json and EDITION_COVERAGE.md.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".local/dsh-handoff-20260914/work"


def flatten(chapters):
    for chapter in chapters:
        yield chapter
        yield from flatten(chapter.get("subChapters") or [])


def git(root: Path, *a: str) -> str:
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True).stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    root = args.root

    editions = json.loads((root / "references/source-editions.json").read_text())["editions"]
    rows = []
    for edition in editions:
        book_id = edition.get("upstreamBookId") or edition["id"].split("-")[-1]
        book_dir = root / "sources/normalized/shidianguji" / book_id
        declared = None
        book_json = book_dir / "book.json"
        if book_json.exists():
            book = json.loads(book_json.read_text())
            chapters = list(flatten(book["catalog"]["chapters"]))
            declared = {
                "chapters": len(chapters),
                "paragraphs": sum(c.get("paragraphCount") or 0 for c in chapters),
            }
        held_paragraphs = 0
        held_chapters = 0
        orig = book_dir / "original-paragraphs.json"
        if orig.exists():
            records = json.loads(orig.read_text())
            held_paragraphs = len(records)
            held_chapters = len({r["chapterId"] for r in records})

        missing = edition.get("missingChapters") or []
        missing_expected = sum(m.get("expected") or 0 for m in missing)
        missing_actual = sum(m.get("actual") or 0 for m in missing)
        low = book_id.lower()
        fetch_dir = WORK / f"{low}-missing"
        fetched = len([p for p in fetch_dir.glob("*.json") if not p.name.startswith("_")]) if fetch_dir.exists() else 0
        reimport = WORK / f"{low}-reimport"
        staged = reimport / "staged"
        staged_paras = None
        staged_missing = None
        if (staged / "_stage-report.json").exists():
            report = json.loads((staged / "_stage-report.json").read_text())
            staged_paras = report["stagedParagraphs"]
            staged_missing = report["missingChaptersRemaining"]
        elif (staged / "provenance.json").exists():
            prov = json.loads((staged / "provenance.json").read_text())
            staged_paras = prov.get("paragraphCount")
            staged_missing = len(prov.get("missingChapters") or [])

        # Editions without upstreamBookId are parallel/mirror layers (annotation mirrors,
        # facsimile collation layers); they have no site catalogue and no catalogComplete key.
        kind = "shidian-catalog" if edition.get("upstreamBookId") else "supplemental-layer"
        web_complete = bool(edition.get("catalogComplete", True))
        rows.append({
            "id": edition["id"],
            "bookId": book_id,
            "bookSlug": edition.get("bookSlug"),
            "editionKind": kind,
            "webCatalogComplete": web_complete,
            "ancientEditionComplete": False,
            "ancientEditionNote": "网页目录取齐不等于古本全帙；本版未作逐字影印校勘。",
            "declaredChapters": declared["chapters"] if declared else None,
            "declaredParagraphs": declared["paragraphs"] if declared else None,
            "heldChapters": held_chapters,
            "heldParagraphs": held_paragraphs,
            "missingChaptersListed": len(missing),
            "missingExpectedParagraphs": missing_expected,
            "missingActualParagraphs": missing_actual,
            "fetchedChapterFiles": fetched,
            "stagedParagraphs": staged_paras,
            "stagedMissingRemaining": staged_missing,
            "evidence": {
                "registry": "references/source-editions.json",
                "declaredFrom": f"sources/normalized/shidianguji/{book_id}/book.json",
                "heldFrom": f"sources/normalized/shidianguji/{book_id}/original-paragraphs.json",
                "fetchedFrom": f".local/dsh-handoff-20260914/work/{low}-missing/",
                "fetchedTool": ".local/dsh-handoff-20260914/work/fetch-shidian-missing.py",
            },
        })

    ledger = {
        "schema": "fateradar-edition-coverage-v1",
        "head": git(root, "rev-parse", "HEAD"),
        "counts": {
            "editions": len(rows),
            "webIncomplete": sum(1 for r in rows
                                   if r["editionKind"] == "shidian-catalog" and not r["webCatalogComplete"]),
            "heldParagraphs": sum(r["heldParagraphs"] for r in rows),
            "stagedNewParagraphs": sum(
                (r["stagedParagraphs"] or 0) - r["heldParagraphs"] for r in rows if r["stagedParagraphs"]),
        },
        "editions": rows,
    }
    out = root / "docs/closeout/EDITION_COVERAGE.json"
    out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")

    md = ["# 版本完整性对照（应有章节—已采章节—缺失章节—来源证据）", "",
          f"HEAD：`{ledger['head']}`", "",
          "**网页目录取齐与古本全帙完整是两件事**：本表 `webCatalogComplete` 只表示"
          "该站在线目录的章节已全部采到；`ancientEditionComplete` 一律为 false，"
          "因为尚未对任何版本完成逐字影印校勘。", "",
          "| 版本 | 网页目录齐 | 站方声明章 | 已采章 | 已采段 | 缺章 | staged 段 | staged 余缺 |",
          "| --- | :-: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in rows:
        if r["editionKind"] != "shidian-catalog":
            md.append(f"| {r['id']} | 平行层 | - | - | {r['heldParagraphs']} | - | - | - |")
            continue
        md.append(
            f"| {r['bookId']} | {'是' if r['webCatalogComplete'] else '**否**'} | "
            f"{r['declaredChapters'] if r['declaredChapters'] is not None else '-'} | "
            f"{r['heldChapters']} | {r['heldParagraphs']} | {r['missingChaptersListed']} | "
            f"{r['stagedParagraphs'] if r['stagedParagraphs'] is not None else '-'} | "
            f"{r['stagedMissingRemaining'] if r['stagedMissingRemaining'] is not None else '-'} |")
    md += ["", "缺章抓取证据在 `.local/dsh-handoff-20260914/work/<bookid>-missing/`（含 `_fetch-summary.json`）。",
           "逐条来源与工具见 `EDITION_COVERAGE.json` 的 `evidence` 字段。", ""]
    (root / "docs/closeout/EDITION_COVERAGE.md").write_text("\n".join(md))
    print(json.dumps(ledger["counts"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
