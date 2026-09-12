#!/usr/bin/env python3
"""Per-art anchor coverage for the six product arts, plus the evidence kind of each rule's quote.

coverage(art) = anchored_rules / total_rules

另报 evidence 列（第 19 批加）：每条规则的 quote 是**逐字引文**还是**编者重述**——
`verbatim`（带 anchor，quote 与源行逐字相同）、`restatement`（显式声明为重述，anchor 可为 null）、
`empty`（没有 quote）。三列相加等于 total。加这一列的原因：实测 156 条规则的 quote 与 statement
逐字相同且无 anchor，其中只有 2 条能在 fulltext 逐字找到；不分开报，读者会把重述当引文。

fengshui / physiognomy / selection / taiyi are not product arts and are omitted.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")
REFERENCE_ARTS = ("meihua", "yili")

DIVINATION_SLUG_TO_ART = {
    "huangjin-ce": "liuyao",
    "huozhu-lin": "liuyao",
    "zengshan-buyi": "liuyao",
    "bushi-zhengzong": "liuyao",
    "meihua-yishu": "meihua",
    "zhouyi-zhezhong": "yili",
    "huangji-jingshi": "yili",
}


def art_of(system: str, slug: str) -> str | None:
    if system == "san-shi":
        if slug.startswith("qimen-"):
            return "qimen"
        if slug.startswith("liuren-") or slug.startswith("daliuren-"):
            return "liuren"
        return None
    if system == "divination":
        return DIVINATION_SLUG_TO_ART.get(slug)
    return {
        "bazi": "bazi",
        "luming-nayin": "bazi",
        "ziwei": "ziwei",
        "xingming": "qizheng",
    }.get(system)


def main() -> int:
    parser = argparse.ArgumentParser(description="Anchor coverage by product art")
    parser.add_argument("--fail-under", type=float, default=None, help="fail if any art coverage < this percent")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    tracked = ARTS + REFERENCE_ARTS
    stats: dict[str, dict[str, int]] = {
        art: {"total": 0, "anchored": 0, "verbatim": 0, "restatement": 0, "no_quote": 0}
        for art in tracked
    }
    per_book: list[dict] = []

    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        system, slug = book.get("system"), book.get("slug")
        art = art_of(system, slug)
        rules = [r for r in (data.get("rules") or []) if isinstance(r, dict)]
        total = len(rules)
        anchored = sum(1 for r in rules if isinstance(r.get("anchor"), dict))
        # 证据种类：空 quote / 显式重述 / 其余按逐字引文计（V15 保证「quote==statement 且无 anchor」
        # 只能是 restatement，故其余情形不会把重述混进 verbatim）。
        verbatim = sum(
            1 for r in rules if (r.get("quote") or "").strip() and r.get("quote_kind") != "restatement"
        )
        restatement = sum(1 for r in rules if r.get("quote_kind") == "restatement")
        no_quote = sum(1 for r in rules if not (r.get("quote") or "").strip())
        rec = {
            "book": f"{system}/{slug}",
            "art": art,
            "total": total,
            "anchored": anchored,
            "coverage": (anchored / total * 100.0) if total else 0.0,
        }
        rec["verbatim"] = verbatim
        rec["restatement"] = restatement
        rec["no_quote"] = no_quote
        per_book.append(rec)
        if art in stats:
            stats[art]["total"] += total
            stats[art]["anchored"] += anchored
            stats[art]["verbatim"] += verbatim
            stats[art]["restatement"] += restatement
            stats[art]["no_quote"] += no_quote

    def pack(art: str) -> dict:
        t, a = stats[art]["total"], stats[art]["anchored"]
        cov = (a / t * 100.0) if t else 0.0
        return {
            "total": t,
            "anchored": a,
            "coverage": round(cov, 2),
            "quote_verbatim": stats[art]["verbatim"],
            "quote_restatement": stats[art]["restatement"],
            "quote_empty": stats[art]["no_quote"],
        }

    arts_out = {art: pack(art) for art in ARTS}
    ref_out = {art: pack(art) for art in REFERENCE_ARTS}
    worst = None
    for art in ARTS:
        cov = arts_out[art]["coverage"]
        if worst is None or cov < worst[0]:
            worst = (cov, art)

    payload = {
        "arts": arts_out,
        "reference_arts": ref_out,
        "books": per_book,
        "fail_under": args.fail_under,
    }
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"{'art':8} {'total':>6} {'anchored':>8} {'coverage':>9} {'引文':>6} {'重述':>6} {'无quote':>7}")
        for art in ARTS:
            d = arts_out[art]
            print(
                f"{art:8} {d['total']:6d} {d['anchored']:8d} {d['coverage']:8.1f}%"
                f" {d['quote_verbatim']:6d} {d['quote_restatement']:6d} {d['quote_empty']:7d}"
            )
        print("reference (not gated)")
        for art in REFERENCE_ARTS:
            d = ref_out[art]
            print(
                f"{art:8} {d['total']:6d} {d['anchored']:8d} {d['coverage']:8.1f}%"
                f" {d['quote_verbatim']:6d} {d['quote_restatement']:6d} {d['quote_empty']:7d}"
            )
        if args.fail_under is not None:
            print(f"threshold {args.fail_under:.1f}%")

    if args.fail_under is not None:
        failed = [art for art, d in arts_out.items() if d["coverage"] < args.fail_under]
        if failed:
            print("FAIL under threshold: " + ", ".join(f"{a}={arts_out[a]['coverage']:.1f}%" for a in failed), file=sys.stderr)
            return 1
        print("PASS all six arts ≥ threshold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
