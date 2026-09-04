#!/usr/bin/env python3
"""Per-art structured-predicate coverage for the six product arts.

coverage(art) = rules_with_nonempty_applicable_to / anchored_rules
Wildcard share = rules_containing_* / rules_with_nonempty_applicable_to
fengshui / physiognomy / selection / taiyi are omitted (same as coverage-report.py).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")
OPEN_KEYS = ("geju", "shensha", "ziwei_star", "daxian", "geju_qimen", "keti")


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


def preds_of(rule: dict) -> list[dict]:
    preds = rule.get("applicable_to") or []
    if not isinstance(preds, list):
        return []
    return [p for p in preds if isinstance(p, dict) and p.get("key") and p.get("value") is not None]


def load_open_dump() -> dict[str, set[str]]:
    path = ROOT / "tools/reports/facts-sample.json"
    if not path.is_file():
        raise FileNotFoundError(f"missing {path}")
    dump = json.loads(path.read_text(encoding="utf-8"))
    values: dict[str, set[str]] = {k: set() for k in OPEN_KEYS}
    for pair in dump.values():
        for side in ("caseA", "caseB"):
            for fact in pair[side]["facts"]:
                key = fact.get("key")
                if key in values:
                    values[key].add(fact["value"])
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="Predicate coverage by product art")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-wildcard", type=float, default=None, help="fail if any art wildcard share > this percent")
    parser.add_argument("--check-open-values", action="store_true", help="fail if open-key values are absent from facts-sample.json")
    args = parser.parse_args()

    stats: dict[str, dict] = {
        art: {
            "anchored": 0,
            "with_predicates": 0,
            "wildcard": 0,
            "keys": set(),
        }
        for art in ARTS
    }
    open_uses: list[tuple[str, str, str, str]] = []

    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        system, slug = book.get("system"), book.get("slug")
        art = art_of(system, slug)
        if art not in stats:
            continue
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or not isinstance(rule.get("anchor"), dict):
                continue
            stats[art]["anchored"] += 1
            preds = preds_of(rule)
            if not preds:
                continue
            stats[art]["with_predicates"] += 1
            if any(p.get("value") == "*" for p in preds):
                stats[art]["wildcard"] += 1
            for p in preds:
                key = p.get("key")
                val = p.get("value")
                if isinstance(key, str):
                    stats[art]["keys"].add(key)
                if key in OPEN_KEYS and val != "*":
                    open_uses.append((art, rule.get("rule_id", ""), key, str(val)))

    arts_out = {}
    for art in ARTS:
        d = stats[art]
        anchored = d["anchored"]
        with_p = d["with_predicates"]
        wild = d["wildcard"]
        cov = (with_p / anchored * 100.0) if anchored else 0.0
        wpct = (wild / with_p * 100.0) if with_p else 0.0
        arts_out[art] = {
            "anchored": anchored,
            "with_predicates": with_p,
            "coverage": round(cov, 2),
            "wildcard": wild,
            "wildcard_pct": round(wpct, 2),
            "fact_keys": len(d["keys"]),
            "fact_key_names": sorted(d["keys"]),
        }

    payload = {"arts": arts_out, "max_wildcard": args.max_wildcard}

    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(
            f"{'art':8} {'anchored':>8} {'with_pred':>9} {'coverage':>9} "
            f"{'wild':>5} {'wild%':>7} {'keys':>5}"
        )
        for art in ARTS:
            d = arts_out[art]
            print(
                f"{art:8} {d['anchored']:8d} {d['with_predicates']:9d} {d['coverage']:8.1f}% "
                f"{d['wildcard']:5d} {d['wildcard_pct']:6.1f}% {d['fact_keys']:5d}"
            )
            if d["fact_key_names"]:
                print(f"         keys: {', '.join(d['fact_key_names'])}")

    exit_code = 0
    if args.max_wildcard is not None:
        failed = [
            art
            for art, d in arts_out.items()
            if d["with_predicates"] and d["wildcard_pct"] > args.max_wildcard
        ]
        if failed:
            print(
                "FAIL wildcard: "
                + ", ".join(f"{a}={arts_out[a]['wildcard_pct']:.1f}%" for a in failed),
                file=sys.stderr,
            )
            exit_code = 1
        else:
            print(f"PASS wildcard ≤ {args.max_wildcard:g}%")

    if args.check_open_values:
        try:
            allowed = load_open_dump()
        except FileNotFoundError as exc:
            print(f"FAIL open-values: {exc}", file=sys.stderr)
            return 1
        bad = [
            (art, rid, key, val)
            for art, rid, key, val in open_uses
            if val not in allowed[key]
        ]
        if bad:
            for art, rid, key, val in bad[:20]:
                print(f"FAIL open-values {art} {rid} {key}={val!r} not in facts-sample.json", file=sys.stderr)
            if len(bad) > 20:
                print(f"... {len(bad) - 20} more", file=sys.stderr)
            exit_code = 1
        else:
            print("PASS open-values")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
