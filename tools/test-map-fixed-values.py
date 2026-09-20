#!/usr/bin/env python3
"""tools/map-fixed-values.py 的回归测试（本批 4 条）。

本批两种形态：
  A. **四柱枚举干支对**（魁罡日／八专日）——用**显式柱位 scope**，不用 `same`；
  B. **具名纳音**（海中金）——`nayin` 事实由 t170 产出，本条是首个使用它的谓词；
  C. **六壬课传位置**（青龙居日上／传中见财）——平铺列表＝或，各句带 `scope.palace`。

钉住：形态合规（无通配）、statement 复核片段在原文里、以及**语义边界**——
尤其「青龙在**任意一传**不等于龙居日上」这条原文警告必须真的被 scope 区分开。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("ev3", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(spec)
sys.modules["ev3"] = ev
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
    ledger = json.loads((ROOT / "tools/reports/fixed-value-map.json").read_text(encoding="utf-8"))
    idx = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        k = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                idx[(k, r["rule_id"])] = r

    print("1. 台账 4 条，复核片段仍在原文里")
    check("  条数 10（+t193 两条六爻具名状态）", len(ledger), 10)
    check(
        "  statement 片段全部命中",
        [x["rule_id"] for x in ledger if x["evidence_from_statement"] not in (idx[(x["book"], x["rule_id"])].get("statement") or "")],
        [],
    )

    print("2. 形态：无通配；枚举对用显式柱位且不写 same")
    bad = []
    for x in ledger:
        ap = idx[(x["book"], x["rule_id"])].get("applicable_to")
        if not ap:
            bad.append(f"{x['rule_id']}: 空")
            continue
        ls = leaves(ap if isinstance(ap, dict) else {"any_of": ap})
        if any(l.get("value") == "*" for l in ls):
            bad.append(f"{x['rule_id']}: 用了通配")
        if isinstance(ap, dict) and ap.get("same"):
            bad.append(f"{x['rule_id']}: 写了 same（枚举对是各组独立，不能用全局绑定）")
    check("  无通配、无 same", bad, [])

    print("3. 语义：日柱枚举对")
    rules = {r["rule_id"]: r for r in ev.load_rules("bazi/sanming-tonghui", None)}
    chart_renzi = [
        fact("gan", "庚", layer="本命", pillar="year"),
        fact("zhi", "午", layer="本命", pillar="year"),
        fact("gan", "壬", layer="本命", pillar="day"),
        fact("zhi", "子", layer="本命", pillar="day"),
    ]
    chart_jisi = [
        fact("gan", "己", layer="本命", pillar="day"),
        fact("zhi", "巳", layer="本命", pillar="day"),
    ]
    chart_jiwei = [
        fact("gan", "己", layer="本命", pillar="day"),
        fact("zhi", "未", layer="本命", pillar="day"),
    ]
    check("  日柱壬子 → 八专日成立", ev.evaluate(rules["SANMINGTONGH-097"], chart_renzi)["verdict"], "满足")
    check("  日柱己巳 → 不成立（八专列的是己未）", ev.evaluate(rules["SANMINGTONGH-097"], chart_jisi)["verdict"], "不满足")
    check("  日柱己未 → 成立", ev.evaluate(rules["SANMINGTONGH-097"], chart_jiwei)["verdict"], "满足")
    check("  日柱壬子 → 不是魁罡（庚辰/庚戌/壬辰/戊戌）", ev.evaluate(rules["R-06"], chart_renzi)["verdict"], "不满足")
    # 关键：scope 钉在 day，year=庚午 不能把「庚…辰」凑成魁罡
    check(
        "  年柱庚午 + 日柱壬子 不得被当成魁罡/八专的错配（柱位须同一柱）",
        ev.evaluate(rules["R-06"], [fact("gan", "庚", layer="本命", pillar="year"), fact("zhi", "辰", layer="本命", pillar="day")])["verdict"],
        "不满足",
    )

    print("4. 语义：具名纳音")
    check(
        "  有海中金 → 成立",
        ev.evaluate(rules["SANMINGTONGH-004"], [fact("nayin", "海中金", layer="本命", pillar="year")])["verdict"],
        "满足",
    )
    check(
        "  只有路旁土 → 不成立",
        ev.evaluate(rules["SANMINGTONGH-004"], [fact("nayin", "路旁土", layer="本命", pillar="year")])["verdict"],
        "不满足",
    )
    check(
        "  完全没有 nayin 事实 → 信息不足（不降级成不满足）",
        ev.evaluate(rules["SANMINGTONGH-004"], [fact("gan", "甲", layer="本命", pillar="day")])["verdict"],
        "信息不足",
    )

    print("5. 语义：六壬课传位置——「任意一传」不得等同「居日上」")
    lr = {r["rule_id"]: r for r in ev.load_rules("san-shi/liuren-miben", None)}
    base = [
        fact("tianjiang", "白虎", layer="本命", palace="日上"),
        fact("tianjiang", "青龙", layer="本命", palace="初传"),  # 青龙在传中，不在日上
        fact("liuqin", "官鬼", layer="本命", palace="初传"),
        fact("liuqin", "父母", layer="本命", palace="中传"),
        fact("liuqin", "父母", layer="本命", palace="末传"),
    ]
    check(
        "  青龙只在初传、传中无财 → 不成立（原文明确警告这一点）",
        ev.evaluate(lr["LIURENMIBEN-021"], base)["verdict"],
        "不满足",
    )
    check(
        "  青龙居日上 → 成立",
        ev.evaluate(
            lr["LIURENMIBEN-021"],
            [fact("tianjiang", "青龙", layer="本命", palace="日上")],
        )["verdict"],
        "满足",
    )
    # 要判「不满足」，两边的 key 都必须**在盘上可判**：只给 tianjiang 的话，
    # liuqin 整个缺席 → 无法排除「传中见财」→ 按三态口径只能是「信息不足」。
    check(
        "  青龙在辰上（非日上），且传中确无财 → 不成立",
        ev.evaluate(
            lr["LIURENMIBEN-021"],
            [
                fact("tianjiang", "青龙", layer="本命", palace="辰上"),
                fact("liuqin", "官鬼", layer="本命", palace="初传"),
                fact("liuqin", "父母", layer="本命", palace="中传"),
                fact("liuqin", "兄弟", layer="本命", palace="末传"),
            ],
        )["verdict"],
        "不满足",
    )
    check(
        "  只有 tianjiang、liuqin 整个缺席 → 信息不足（不得当成不满足）",
        ev.evaluate(
            lr["LIURENMIBEN-021"],
            [fact("tianjiang", "青龙", layer="本命", palace="辰上")],
        )["verdict"],
        "信息不足",
    )
    check(
        "  传中见财（中传）→ 成立（或分支）",
        ev.evaluate(
            lr["LIURENMIBEN-021"],
            [fact("liuqin", "妻财", layer="本命", palace="中传")],
        )["verdict"],
        "满足",
    )
    check(
        "  一个相关 key 都没有 → 信息不足",
        ev.evaluate(lr["LIURENMIBEN-021"], [fact("keti", "元首课", layer="本命")])["verdict"],
        "信息不足",
    )

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL FIXED-VALUE MAP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())