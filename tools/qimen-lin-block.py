#!/usr/bin/env python3
"""奇门「X临Y」格块（8 条）的可复算分析：语义、所需事实、三种编码各自撞什么闸门。

**为什么单独做这一块**：它是当前**单个可识别块里最大的一块**——
奇门 8 条（QM-P27/28/29/30/32/33/38/39），若解开，奇门谓词覆盖可从 67.5% 升到接近 87%。
同时它是唯一一块**语义已明确、只卡在表达方式**上的：原文体例统一为「X临Y」＝天盘X压地盘Y。

原文（qimen-faqiao 选段的格表，逐条即 rule 的 quote）：

    岁格   庚临岁干        月格   庚临月干        日格   庚临日干
    时格   庚临时干三奇    伏干   庚临日干        飞干格 日干临庚
    地罗遮蔽 六壬临时干    天网四张 六癸临时干

「临」＝天盘压地盘（「日干临庚」是反向，可见体例一致）。
故八条的公共条件都是：**某宫的天盘干为 A，且该宫的地盘干等于某柱之干**。

它要三样东西：
  1. `tianpan_gan` / `dipan_gan` —— 已有（t171）；
  2. **奇门侧的柱干事实** —— 引擎已算（`facts.ganZhi`），事实层未产出，属一笔 passthrough；
  3. **把「地盘干的取值」与「某柱干」绑起来** —— 这才是真正的卡点，见下。

本脚本只做分析，**不改规则、不改闸门**；三种编码的取舍需要授权（见 §3）。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# 八条的原文与语义拆解（A=天盘干，柱=与地盘干相比的柱）
BLOCK: dict[str, dict] = {
    "QM-P27": {"name": "岁格", "tianpan": "庚", "pillar": "year", "quote": "岁格 庚临岁干"},
    "QM-P28": {"name": "月格", "tianpan": "庚", "pillar": "month", "quote": "月格 庚临月干"},
    "QM-P29": {"name": "日格", "tianpan": "庚", "pillar": "day", "quote": "日格 庚临日干"},
    "QM-P30": {"name": "时格", "tianpan": "庚", "pillar": "time", "quote": "时格 庚临时干三奇"},
    "QM-P32": {"name": "伏干", "tianpan": "庚", "pillar": "day", "quote": "伏干 庚临日干"},
    "QM-P33": {"name": "飞干格", "tianpan": "pillar", "pillar": "day", "dipan": "庚", "quote": "飞干格 日干临庚"},
    "QM-P38": {"name": "地罗遮蔽", "tianpan": "壬", "pillar": "time", "quote": "地罗遮蔽 六壬临时干"},
    "QM-P39": {"name": "天网四张", "tianpan": "癸", "pillar": "time", "quote": "天网四张 六癸临时干"},
}


def rule_by_id() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted((ROOT / "references/books/san-shi").glob("*/rules.yaml")):
        for r in yaml.safe_load(p.read_text(encoding="utf-8")).get("rules") or []:
            if isinstance(r, dict):
                out[r["rule_id"]] = r
    return out


def qimen_gate() -> tuple[int, int]:
    """奇门当前的 (通配规则数, 有谓词规则数) —— 直接问权威报告，不自己重算。"""
    out = subprocess.run(
        [sys.executable, str(ROOT / "tools/predicate-report.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout
    d = json.loads(out)
    row = (d.get("arts") or {}).get("qimen")
    if not isinstance(row, dict):
        raise SystemExit("predicate-report --json 里找不到 qimen 行")
    return int(row.get("wildcard") or 0), int(row.get("with_predicates") or 0)


def main() -> int:
    ap = argparse.ArgumentParser(description="奇门 X临Y 格块分析")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rules = rule_by_id()
    missing = [rid for rid in BLOCK if rid not in rules]
    if missing:
        raise SystemExit(f"规则不存在：{missing}")
    unmapped = [rid for rid in BLOCK if not rules[rid].get("applicable_to")]
    quote_mismatch = [
        rid for rid, spec in BLOCK.items()
        if spec["quote"] not in (rules[rid].get("quote") or "")
    ]

    wild, total = qimen_gate()
    n = len(BLOCK)
    options = {
        "explicit-wildcard": {
            "how": "写成 {zhifu 式} 存在性通配：{all_of:[{tianpan_gan,庚},{dipan_gan,\"*\"}], same:gong}",
            "gate": f"({wild}+{n})/({total}+{n}) = {(wild + n) / (total + n) * 100:.1f}%",
            "verdict": "FAIL（>15%）" if (wild + n) / (total + n) > 0.15 else "PASS",
            "needs": "授权：闸门判据是否区分「存在性」与「凑数」",
        },
        "scope-only-clause": {
            "how": ("引擎为每柱产出『柱干临宫』事实（value=柱干，scope={layer,gong}），"
                    "谓词写成 {all_of:[{tianpan_gan,庚},{key:zhu_gan_lin,scope:{pillar:year}}],same:gong}"
                    "——子句**限定柱位、不限定取值**（取值本就该随盘而变）"),
            "gate": f"字面不含 `*`，但「不限定取值」在语义上等价存在性 → 是否计入需口径裁定",
            "verdict": "取决于口径：计入则同 FAIL，不计入则 PASS 但需说明为何不算凑数",
            "needs": "授权：口径裁定 + 引擎加一笔 passthrough",
        },
        "value-join-language": {
            "how": ("语言升级：允许无取值子句 + 让 `same` 接受 `value`（即「两句所命中事实的 value 需相等」），"
                    "写成 {all_of:[{tianpan_gan,庚},{dipan_gan},{gan,scope:{pillar:year}}],same:[gong,value]}"),
            "gate": "不产生通配子句（`dipan_gan` 的取值由 join 约束）",
            "verdict": "PASS（但需语言 v4 + 消费方同步实现）",
            "needs": "语言变更（本仓可做）+ **消费方评估器同步**（跨仓协调）",
        },
    }

    report = {
        "report": "奇门「X临Y」格块（8 条）分析",
        "generated_by": "t184",
        "semantics": "天盘干 A 所在之宫，其地盘干等于某柱之干（原文体例：「X临Y」＝天盘X压地盘Y）",
        "block": {rid: {**spec, "mapped": bool(rules[rid].get("applicable_to"))} for rid, spec in BLOCK.items()},
        "still_unmapped": unmapped,
        "quote_check": "全部逐字命中" if not quote_mismatch else f"不命中：{quote_mismatch}",
        "facts": {
            "have": ["tianpan_gan", "dipan_gan"],
            "missing": ["奇门侧四柱干事实（引擎已算 facts.ganZhi，事实层未产出）"],
            "hard_part": "把「地盘干取值」与「某柱干」绑定",
        },
        "qimen_gate_now": {"wildcard_rules": wild, "rules_with_predicate": total},
        "options": options,
        "recommendation": ("blocked-needs-decision：三选一都**不是**我能单方面定的 —— "
                           "前两条要授权（闸门判据/口径裁定），第三条要消费方同步实现语言 v4。"
                           "在得到授权前不动规则、不动闸门。"),
    }
    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    print(f"奇门「X临Y」格块：{n} 条（仍未映射 {len(unmapped)} 条）；原文引文：{report['quote_check']}")
    print(f"奇门现状：通配 {wild}／有谓词 {total} = {wild / total * 100:.1f}%")
    print(f"语义：{report['semantics']}")
    print("\n缺什么：")
    print(f"  已有   : {', '.join(report['facts']['have'])}")
    print(f"  缺     : {report['facts']['missing'][0]}")
    print(f"  真卡点 : {report['facts']['hard_part']}")
    print("\n三种编码各撞什么：")
    for k, v in options.items():
        print(f"  [{k}]")
        print(f"      做法：{v['how'][:96]}")
        print(f"      闸门：{v['gate']}  → {v['verdict']}")
        print(f"      需要：{v['needs']}")
    print(f"\n结论：{report['recommendation']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())