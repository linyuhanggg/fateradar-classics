#!/usr/bin/env python3
"""Per-art anchor coverage for the six product arts.

coverage(art) = anchored_rules / total_rules
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


def art_of(system: str, slug: str) -> str | None:
    if system == "san-shi":
        if slug.startswith("qimen-"):
            return "qimen"
        if slug.startswith("liuren-") or slug.startswith("daliuren-"):
            return "liuren"
        return None
    return {
        "bazi": "bazi",
        "luming-nayin": "bazi",
        "ziwei": "ziwei",
        "divination": "liuyao",
        "xingming": "qizheng",
    }.get(system)


def main() -> int:
    parser = argparse.ArgumentParser(description="Anchor coverage by product art")
    parser.add_argument("--fail-under", type=float, default=None, help="fail if any art coverage < this percent")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    stats: dict[str, dict[str, int]] = {art: {"total": 0, "anchored": 0} for art in ARTS}
    per_book: list[dict] = []

    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        system, slug = book.get("system"), book.get("slug")
        art = art_of(system, slug)
        rules = [r for r in (data.get("rules") or []) if isinstance(r, dict)]
        total = len(rules)
        anchored = sum(1 for r in rules if isinstance(r.get("anchor"), dict))
        rec = {
            "book": f"{system}/{slug}",
            "art": art,
            "total": total,
            "anchored": anchored,
            "coverage": (anchored / total * 100.0) if total else 0.0,
        }
        per_book.append(rec)
        if art in stats:
            stats[art]["total"] += total
            stats[art]["anchored"] += anchored

    arts_out = {}
    worst = None
    for art in ARTS:
        t, a = stats[art]["total"], stats[art]["anchored"]
        cov = (a / t * 100.0) if t else 0.0
        arts_out[art] = {"total": t, "anchored": a, "coverage": round(cov, 2)}
        if worst is None or cov < worst[0]:
            worst = (cov, art)

    payload = {"arts": arts_out, "books": per_book, "fail_under": args.fail_under}
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"{'art':8} {'total':>6} {'anchored':>8} {'coverage':>9}")
        for art in ARTS:
            d = arts_out[art]
            print(f"{art:8} {d['total']:6d} {d['anchored']:8d} {d['coverage']:8.1f}%")
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
