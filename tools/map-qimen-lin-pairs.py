#!/usr/bin/env python3
"""奇门「庚临岁干」类：把**跨键取值相等**用 v3 已有的枚举写成**精确**谓词（t188）。

## 问题

原文格表（qimen-dunjia-tongzhi L285–306）体例统一为「**X临Y**」＝天盘X压地盘Y：

    大格 庚临六癸      刑格 庚临六己      小格 庚临壬      ← 固定干，t171 已映射
    岁格 庚临岁干      月格 庚临月干      日格 庚临日干    ← 柱干，随盘而变
    时格 庚临时干三奇  伏干 庚临日干      飞干格 日干临庚
    地罗遮蔽 六壬临时干  天网四张 六癸临时干

柱干那几条要的是「**地盘干的取值 ＝ 某柱之干**」——即跨键取值相等。语言里没有这个原语，
而写法上若用存在性通配（`value: "*"` 或省略 value）会撞 15% 通配闸门。

## 办法：枚举有限域 + 分支内配对（**不用通配、不加新原语**）

地盘干只取 9 个值（三奇六仪，无甲；中五不立）。于是把等式**逐值配对**：

    {any_of: [
      {all_of: [
         {all_of: [{key: gan, value: 庚, scope: {pillar: year}}]},          # ① 该柱之干＝庚
         {all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 庚}], same: gong}  # ② 天盘庚压地盘庚
      ]},
      … 丙丁戊己辛壬癸 共 9 支 …
    ]}

- **精确**：每个分支把「柱干＝X」与「天盘A压地盘X」配成一对，等价于跨键相等。
- **不恒真**：要求天盘 A 恰好压在那个地盘干等于该柱之干的宫上（`same: gong` 绑定），
  不是「只要出现某值即可」。这与 t168 撤回 `DITIANSUICHA-DR-07`（10 个 rizhu 穷尽值域 ⇒ 每盘成立）
  是**不同**的东西：那里是独立的或位枚举，这里是**成对**的分支。
- **不占通配**：全式没有 `value: "*"`。

## 如实披露的两点

1. **甲 不表达**：地盘无甲（甲寄六仪），故柱干为甲时本式不成立。原文对「岁干＝甲」怎么算，
   须另判（`庚临值符`＝QM-P31 是另一条），故此处按**子集**处理并披露。
2. 这些分支里对 `dipan_gan` 的取值在整式上覆盖了全部 9 个值 —— 但它们是**成对**出现的，
   不是独立的或位凑数；`eval-predicates.py --discrimination` 的 `domain_covering` 判据
   需要相应细化（t188 同轮改），否则会误报为「恒真」。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
# 地盘干的九个取值（三奇六仪，无甲）
EARTH_STEMS = ["乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# rule_id → (天盘干, 柱位, statement 复核片段, 备注)
PILLAR_CASES: dict[str, tuple[str, str, str, str]] = {
    "QM-P27": ("庚", "year", "庚临岁干", ""),
    "QM-P28": ("庚", "month", "庚临月干", ""),
    "QM-P29": ("庚", "day", "庚临日干", ""),
    "QM-P32": ("庚", "day", "庚临日干", "与 QM-P29 同文（日格／伏干两名同条件），式亦相同。"),
    "QM-P38": ("壬", "time", "六壬临时干", "原文「六壬」＝壬仪。"),
    "QM-P39": ("癸", "time", "六癸临时干", "原文「六癸」＝癸仪。"),
}

# 反向式（天盘的值＝柱干，地盘固定）：rule_id → (地盘干, 柱位, statement 复核片段, 备注)
REVERSE_CASES: dict[str, tuple[str, str, str, str]] = {
    "QM-P33": ("庚", "day", "日干临庚", "「日干临庚」是反向式：天盘是日干、地盘是庚。"),
}


def encode_reverse(dipan: str, pillar: str) -> str:
    """反向式「日干临庚」：**天盘**的值等于该柱之干，地盘固定为一个干。

    与正向同构，只是等式两侧互换：
      {any_of: [{all_of: [{all_of: [{gan: X, scope: {pillar: day}}]},
                          {all_of: [{tianpan_gan: X}, {dipan_gan: 庚}], same: gong}]}, … 9 支]}
    """
    branches = []
    for x in EARTH_STEMS:
        branches.append(
            "{all_of: ["
            f"{{all_of: [{{key: gan, value: {x}, scope: {{pillar: {pillar}}}}}]}}, "
            f"{{all_of: [{{key: tianpan_gan, value: {x}}}, {{key: dipan_gan, value: {dipan}}}], same: gong}}"
            "]}"
        )
    return "{any_of: [" + ", ".join(branches) + "]}"


def encode(tianpan: str, pillar: str) -> str:
    branches = []
    for x in EARTH_STEMS:
        branches.append(
            "{all_of: ["
            f"{{all_of: [{{key: gan, value: {x}, scope: {{pillar: {pillar}}}}}]}}, "
            f"{{all_of: [{{key: tianpan_gan, value: {tianpan}}}, {{key: dipan_gan, value: {x}}}], same: gong}}"
            "]}"
        )
    return "{any_of: [" + ", ".join(branches) + "]}"


def main() -> int:
    ap = argparse.ArgumentParser(description="奇门「X临Y」柱干类 → v3 枚举式")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cases = {**{k: (v[0], v[1], v[2], v[3]) for k, v in PILLAR_CASES.items()},
             **REVERSE_CASES}

    targets: dict[Path, str] = {}
    found: dict[str, tuple[Path, dict]] = {}
    for p in sorted((ROOT / "references/books/san-shi").glob("*/rules.yaml")):
        text = p.read_text(encoding="utf-8")
        targets[p] = text
        for r in yaml.safe_load(text).get("rules") or []:
            if isinstance(r, dict) and r.get("rule_id") in cases:
                found[r["rule_id"]] = (p, r)

    problems: list[str] = []
    done: set[str] = set()
    for rid, (tp, pillar, needle, _n) in cases.items():
        if rid not in found:
            problems.append(f"{rid} 不存在")
            continue
        _p, r = found[rid]
        if needle not in (r.get("statement") or ""):
            problems.append(f"{rid} statement 不含复核片段「{needle}」")
        cur = r.get("applicable_to")
        want = yaml.safe_load(encode_reverse(tp, pillar) if rid in REVERSE_CASES else encode(tp, pillar))
        if cur:
            if cur == want:
                done.add(rid)
            else:
                problems.append(f"{rid} 已有不同谓词，本批不应改写")
    if problems:
        for x in problems:
            print("FAIL:", x, file=sys.stderr)
        return 1
    print(f"复核通过：{len(cases)} 条（已落实 {len(done)}，本次待写 {len(cases) - len(done)}）")

    if args.dry_run:
        for rid, (tp, pillar, _needle, _n) in cases.items():
            fn = encode_reverse if rid in REVERSE_CASES else encode
            print(f"  {rid}: {fn(tp, pillar)[:110]}…")
        return 0

    for rid, (tp, pillar, _needle, _note) in cases.items():
        if rid in done:
            continue
        path, _r = found[rid]
        text = targets[path]
        pattern = re.compile(rf"(?m)^(- rule_id: {re.escape(rid)}\n(?:.*\n)*?  applicable_to: )\[\]$")
        enc = encode_reverse(tp, pillar) if rid in REVERSE_CASES else encode(tp, pillar)
        text, n = pattern.subn(lambda mo: mo.group(1) + enc, text, count=1)
        if n != 1:
            raise SystemExit(f"改写失败: {rid}")
        targets[path] = text
    for path, text in targets.items():
        path.write_text(text, encoding="utf-8")
    print(f"已写入 {len({p for p, _ in found.values()})} 个 rules.yaml")

    ledger = [
        {
            "book": found[rid][0].relative_to(ROOT / "references/books").as_posix().replace("/rules.yaml", ""),
            "rule_id": rid,
            "encoding": "enumerated-value-pairing-reverse" if rid in REVERSE_CASES else "enumerated-value-pairing",
            "applicable_to_yaml": encode_reverse(tp, pillar) if rid in REVERSE_CASES else encode(tp, pillar),
            "tianpan_gan": tp,
            "pillar": pillar,
            "earth_stems_enumerated": EARTH_STEMS,
            "evidence_from_statement": needle,
            "disclosed": "柱干为甲时不表达（地盘无甲）；原文明细须另判。",
            "note": note,
        }
        for rid, (tp, pillar, needle, note) in cases.items()
    ]
    out = ROOT / "tools/reports/qimen-lin-pair-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())