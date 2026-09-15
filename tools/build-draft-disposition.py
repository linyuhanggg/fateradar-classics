#!/usr/bin/env python3
"""Build a per-item disposition ledger for every `draft` annotation at the current HEAD.

Re-runnable and deterministic: every count and every category decision is derived
from repository state, and each row records the evidence that drove its category.

Categories (objective-defined):
  catalog_metadata  目录/元数据   — chapter titles, 卷端题署, imprint/page matter, modern recovery notes
  verifiable_text   可核实正文   — readable body prose that still awaits a full semantic read
  figure_or_lacuna  图文缺失     — image placeholders, missing glyphs, doubtful or missing markers
  edition_variant   版本异文     — the note records a variant/parallel-edition question
  illegible         原件仍不可辨 — unresolved fragments with no positive readability signal

Writes:
  docs/closeout/DRAFT_DISPOSITION_LEDGER.json   (machine-readable, per item)
  docs/closeout/DRAFT_DISPOSITION_CURRENT.md    (human summary) unless --no-md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from source_paragraphs import load_source_paragraphs  # noqa: E402

LACUNA = ("〔此处为字形或图像", "〔此处为图像", "〔源段仅含版面标记", "〔原表", "□", "〓")
TITLELIKE = re.compile(r"^(第[一二三四五六七八九十百千]+[章卷篇節节]|[卷篇]之[一二三四五六七八九十]|"
                       r"[上下]卷|總目|总目|目錄|目录|凡例|序$|跋$)")
VARIANT_HINT = ("异文", "異文", "别本", "別本", "他本", "另一版本", "版本差异", "底本不同", "异体字")
MODERN_META = ("现代恢复", "恢复档案", "定位说明", "现代元数据", "nlc-layouts", "recovery")
METADATA_KINDS = {"序跋目录", "评注或元数据"}


def load_text_cache(root: Path, files: set[str]) -> dict[str, list[str]]:
    cache = {}
    for rel in files:
        path = root / rel
        if path.exists():
            cache[rel] = path.read_text().splitlines()
    return cache


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--no-md", action="store_true")
    args = ap.parse_args()
    root = args.root

    paragraphs = load_source_paragraphs(root)
    by_file: dict[str, list[str]] = defaultdict(list)
    for pid, row in paragraphs.items():
        by_file[row["source_file"]].append(pid)
    text_cache = load_text_cache(root, set(by_file))

    def text_of(pid: str) -> str:
        row = paragraphs[pid]
        lines = text_cache.get(row["source_file"])
        if not lines:
            return ""
        return "\n".join(lines[row["start_line"] - 1:row["end_line"]])

    ann_rows = []
    for path in sorted((root / "references/annotations").glob("**/*.json")):
        if path.name.startswith("_"):
            continue
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        for entry in data.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            pid = entry.get("paragraphId") or entry.get("sourceId")
            if pid:
                ann_rows.append((pid, entry, data.get("bookSlug"), path.relative_to(root).as_posix()))

    rows = []
    counts = Counter()
    for pid, entry, book, ann_file in ann_rows:
        if (entry.get("review") or entry.get("status")) != "draft":
            continue
        src = paragraphs.get(pid, {})
        text = text_of(pid) if pid in paragraphs else ""
        notes = " ".join(entry.get("notes") or [])
        kind = entry.get("kind") or src.get("kind") or "?"
        compact = re.sub(r"\s+", "", text)
        evidence: list[str] = []
        category = None
        lacuna_hit = next((m for m in LACUNA if m in text), None)
        signals = {
            "hasLacunaMarker": bool(lacuna_hit),
            "hasFigureOrDoubt": bool(src.get("figureCount") or src.get("doubtful") or src.get("missing_marker")),
            "hasVariantHint": any(h in notes for h in VARIANT_HINT),
            "readableChars": len(re.sub(r"[\s，。、；：！？「」『』（）()〔〕·．.,;:!?\"'—-]", "", text)),
        }

        if lacuna_hit:
            category = "figure_or_lacuna"
            evidence.append(f"源文含缺字/图像占位标记 {lacuna_hit!r}")
        elif signals["hasFigureOrDoubt"]:
            category = "figure_or_lacuna"
            evidence.append(f"源层标记 figureCount={src.get('figureCount')} "
                            f"doubtful={src.get('doubtful')} missing_marker={src.get('missing_marker')}")
        elif signals["hasVariantHint"]:
            category = "edition_variant"
            hit = next(h for h in VARIANT_HINT if h in notes)
            evidence.append(f"注解 note 记录版本/异文问题，命中 {hit!r}")

        if category is None:
            readable = len(re.sub(r"[\s，。、；：！？「」『』（）()〔〕·．.,;:!?\"'—-]", "", text)) >= 1
            if kind in METADATA_KINDS or TITLELIKE.match(compact) or any(m in notes for m in MODERN_META):
                category = "catalog_metadata"
                if kind in METADATA_KINDS:
                    evidence.append(f"kind={kind}")
                if TITLELIKE.match(compact):
                    evidence.append(f"源文形如章题/目录：{compact[:24]!r}")
                if any(m in notes for m in MODERN_META):
                    evidence.append("note 标记为现代恢复/元数据说明")
            elif readable:
                category = "verifiable_text"
                evidence.append(f"kind={kind}，源文存在可读文字共 {len(compact)} 字（无缺字/图像标记），"
                                "尚待完整语义对读")
            else:
                category = "illegible"
                evidence.append(f"kind={kind}，源文无任何可读文字（去标点后为空），须待更清晰底本")

        counts[category] += 1
        rows.append({
            "sourceId": pid,
            "bookSlug": book,
            "kind": kind,
            "category": category,
            "reviewStatus": "draft",
            "verified": bool(entry.get("verified")),
            "sourceFile": src.get("source_file"),
            "sourceLines": f"L{src.get('start_line')}-L{src.get('end_line')}" if src else None,
            "heading": src.get("heading"),
            "annotationFile": ann_file,
            "evidence": evidence,
            "signals": signals,
            "reason": "; ".join(evidence),
            "resolved": False,
        })

    ledger = {
        "schema": "fateradar-draft-disposition-v1",
        "head": _git(root, "rev-parse", "HEAD"),
        "draftTotal": len(rows),
        "categoryCounts": dict(counts.most_common()),
        "categoryDefinitions": {
            "catalog_metadata": "目录/元数据：章题、卷端题署、版记或现代恢复说明，按 schema 保留 draft 状态",
            "verifiable_text": "可核实正文：电子原文完整可读，尚待完整语义对读",
            "figure_or_lacuna": "图文缺失：含缺字、图像占位或残表标记",
            "edition_variant": "版本异文：note 记录异文或版本差异问题",
            "illegible": "原件仍不可辨：残句无正向可读证据",
        },
        "rows": rows,
    }
    out = root / "docs/closeout/DRAFT_DISPOSITION_LEDGER.json"
    # Compact: the ledger is a machine-readable per-item record (11k+ rows); the
    # human-readable summary lives in DRAFT_DISPOSITION_CURRENT.md.
    out.write_text(json.dumps(ledger, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in ledger.items() if k != "rows"}, ensure_ascii=False, indent=2))

    if not args.no_md:
        _write_md(root / "docs/closeout/DRAFT_DISPOSITION_CURRENT.md", ledger)
    return 0


def _git(root: Path, *a: str) -> str:
    import subprocess
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True).stdout.strip()


def _write_md(path: Path, ledger: dict) -> None:
    by_book = Counter()
    for row in ledger["rows"]:
        by_book[row["bookSlug"] or "?"] += 1
    lines = [
        "# Draft 逐条处置账（当前 HEAD 自动重算）",
        "",
        f"HEAD：`{ledger['head']}`",
        f"draft 总数：**{ledger['draftTotal']}**",
        "",
        "本文件由 `tools/build-draft-disposition.py` 生成，可随时重跑；"
        "每一条 draft 都有独立行记录源 ID、证据路径与分类依据。",
        "**分类不等于结案**：`catalog_metadata` 依 schema 保留 draft 属正常去向，"
        "`verifiable_text`、`figure_or_lacuna`、`edition_variant`、`illegible` 仍是真实待办。",
        "",
        "## 分类计数",
        "",
        "| 分类 | 条数 | 含义 |",
        "| --- | ---: | --- |",
    ]
    defs = ledger["categoryDefinitions"]
    for cat, n in ledger["categoryCounts"].items():
        lines.append(f"| `{cat}` | {n} | {defs.get(cat, '')} |")
    lines += ["", "## 按书分布（draft 条数）", "", "| 书 | draft |", "| --- | ---: |"]
    for book, n in by_book.most_common():
        lines.append(f"| {book} | {n} |")
    lines += ["", "逐条明细见 `DRAFT_DISPOSITION_LEDGER.json`。", ""]
    path.write_text("\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
