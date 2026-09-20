#!/usr/bin/env python3
"""tools/map-branch-groups.py 的回归测试。

钉住三件事：
  1. 9 条映射的 statement 复核片段确实在原文里（判据基于原文，不是自报）；
  2. 谓词形态：只用 `zhi` 叶子、**不用通配**、**不加 `same`**——
     三合／方局要的正是三支**分布在不同柱**，绑柱位反而错；
  3. 语义对得上：子午冲在「子、午同现」的盘上成立、在只有子的盘上不成立；三合局缺一支不成立。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "tools/reports/branch-group-map.json"

spec = importlib.util.spec_from_file_location("ev2", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(spec)
sys.modules["ev2"] = ev
assert spec.loader is not None
spec.loader.exec_module(ev)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def fact(key, value, **scope):
    return {"key": key, "value": value, "scope": scope, "derivedFrom": ["test"]}


def leaves(node):
    if isinstance(node, list):
        return [x for n in node for x in leaves(n)]
    if not isinstance(node, dict):
        return []
    if "key" in node:
        return [node]
    return [x for b in ("any_of", "all_of", "none_of") for x in leaves(node.get(b) or [])]


def main() -> int:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rules = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        k = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                rules[(k, r["rule_id"])] = r

    print("1. 台账 9 条，复核片段仍在原文里")
    check("  条数", len(ledger), 9)
    miss = [
        x["rule_id"]
        for x in ledger
        if x["evidence_from_statement"] not in (rules[(x["book"], x["rule_id"])].get("statement") or "")
    ]
    check("  statement 片段全部命中", miss, [])

    print("2. 谓词形态：只用 zhi、无通配、无 same")
    bad = []
    for x in ledger:
        ap = rules[(x["book"], x["rule_id"])].get("applicable_to")
        if not ap:
            bad.append(f"{x['rule_id']}: 空")
            continue
        ls = leaves(ap if isinstance(ap, dict) else {"any_of": ap})
        if {l["key"] for l in ls} != {"zhi"}:
            bad.append(f"{x['rule_id']}: 非 zhi 键")
        if any(l.get("value") == "*" for l in ls):
            bad.append(f"{x['rule_id']}: 用了通配")
        if isinstance(ap, dict) and ap.get("same"):
            bad.append(f"{x['rule_id']}: 加了 same（三合要跨柱，不能绑柱位）")
    check("  形态全部合规", bad, [])

    print("3. 语义：子午冲与三合局的成立/不成立")
    by_id = {r["rule_id"]: r for r in ev.load_rules("bazi/sanming-tonghui", None) + ev.load_rules("bazi/ditiansui-chanwei", None)}
    chart_zi_wu = [fact("zhi", "子", layer="本命", pillar="day"), fact("zhi", "午", layer="本命", pillar="year")]
    chart_only_zi = [fact("zhi", "子", layer="本命", pillar="day"), fact("zhi", "寅", layer="本命", pillar="month")]
    check(
        "  子午同现 → 子午冲成立",
        ev.evaluate(by_id["DITIANSUICHA-032"], chart_zi_wu)["verdict"],
        "满足",
    )
    check(
        "  只有子、无午 → 不成立（且 key 在场，属「不满足」不是「信息不足」）",
        ev.evaluate(by_id["DITIANSUICHA-032"], chart_only_zi)["verdict"],
        "不满足",
    )
    full = [fact("zhi", b, layer="本命", pillar=p) for b, p in zip(("申", "子", "辰"), ("year", "month", "day"))]
    check("  申子辰三支齐 → 三合局成立", ev.evaluate(by_id["SANMINGTONGH-015"], full)["verdict"], "满足")
    check(
        "  缺一支（申子）→ 不成立（原文「三字缺一不能」正是此意）",
        ev.evaluate(by_id["SANMINGTONGH-015"], full[:2])["verdict"],
        "不满足",
    )
    none_at_all = [fact("gan", "甲", layer="本命", pillar="day")]
    check(
        "  一个 zhi 都没有 → 信息不足（不得降级成不满足）",
        ev.evaluate(by_id["SANMINGTONGH-015"], none_at_all)["verdict"],
        "信息不足",
    )

    print("4. anchor:null 的那条要如实登记（不在门禁分母内）")
    san18 = rules[("bazi/sanming-tonghui", "SANMINGTONGH-018")]["anchor"]
    check("  SANMINGTONGH-018 仍是 anchor:null", san18, None)
    check(
        "  台账里 9 条中恰好 1 条不在门禁分母内",
        sum(1 for x in ledger if rules[(x["book"], x["rule_id"])].get("anchor") is None),
        1,
    )

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL BRANCH-GROUP MAP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())