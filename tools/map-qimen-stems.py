#!/usr/bin/env python3
"""把奇门「天地盘干相配」类规则映成谓词（16 条）。

判据（逐条都能对着 statement 复核）：

- 「天盘干 X 加/临/遇 地盘干 Y」→ `{all_of: [{tianpan_gan X}, {dipan_gan Y}], same: gong}`
  （同一宫内天盘 X、地盘 Y）。`same: gong` 是 t168 加的绑定语义。
- 「X 奇 到/入 某宫」→ 直接写 `scope.gong`（宫号按后天八卦 1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离）。
- 「门／神 与 奇 合」→ 若原文点名宫位则三句都写 `scope.gong`；未点名宫位（如「合九天」）
  才用 `same: gong` 绑定。
- 伏吟／反吟两条取引擎**已产出**的格局名 `geju_qimen`（实测样本值为「伏吟局」「反吟局」，
  带「局」字，不是「伏吟」）。

**不改判据以迁就数据**：`甲` 不出现在天地盘（甲寄六仪），所以「甲值符加地盘丙奇」
一类**不映射**——要表达它得先有「值符所落之宫」，那不在本批范围内。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOK = "san-shi/qimen-dunjia-tongzhi"
YAML_PATH = ROOT / "references/books" / BOOK / "rules.yaml"

# rule_id → (谓词 YAML, 用于复核的 statement 片段)
MAP: dict[str, tuple[str, str]] = {
    "QM-P03": ("{all_of: [{key: tianpan_gan, value: 乙}, {key: dipan_gan, value: 辛}], same: gong}", "乙奇遇辛"),
    "QM-P04": ("{all_of: [{key: tianpan_gan, value: 辛}, {key: dipan_gan, value: 乙}], same: gong}", "辛遇乙奇"),
    "QM-P05": ("{all_of: [{key: tianpan_gan, value: 癸}, {key: dipan_gan, value: 丁}], same: gong}", "癸见丁奇"),
    "QM-P06": ("{all_of: [{key: tianpan_gan, value: 丁}, {key: dipan_gan, value: 癸}], same: gong}", "丁奇见癸"),
    "QM-P07": ("{all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 癸}], same: gong}", "庚临六癸"),
    "QM-P08": ("{all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 己}], same: gong}", "庚临六己"),
    "QM-P09": ("{all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 壬}], same: gong}", "庚临壬"),
    "QM-P14": ("[{key: geju_qimen, value: 伏吟局}]", "伏吟"),
    "QM-P15": ("[{key: geju_qimen, value: 反吟局}]", "反吟"),
    "QM-P16": (
        "[{key: tianpan_gan, value: 乙, scope: {gong: 2}}, "
        "{key: tianpan_gan, value: 丙, scope: {gong: 6}}, "
        "{key: tianpan_gan, value: 丁, scope: {gong: 8}}]",
        "乙奇坤宫",
    ),
    "QM-P21": (
        "{all_of: [{key: bamen, value: 休门, scope: {gong: 1}}, "
        "{key: tianpan_gan, value: 乙, scope: {gong: 1}}]}",
        "休门与乙奇合坎",
    ),
    "QM-P22": (
        "{all_of: [{key: bamen, value: 休门, scope: {gong: 8}}, "
        "{key: tianpan_gan, value: 乙, scope: {gong: 8}}, "
        "{key: dipan_gan, value: 辛, scope: {gong: 8}}]}",
        "休门与乙奇合艮辛",
    ),
    "QM-P23": (
        "{all_of: [{key: bamen, value: 休门}, {key: tianpan_gan, value: 乙}, "
        "{key: bashen, value: 九天}], same: gong}",
        "休门与乙奇合九天",
    ),
    "QM-P24": (
        "{all_of: [{key: tianpan_gan, value: 乙}, {key: bashen, value: 九地}, "
        "{key: bamen, value: 杜门}], same: gong}",
        "乙奇合九地杜门",
    ),
    # ── 值符类：条件问的是**值符所在之宫**，不是值符星名 ─────────────────────
    # `zhifu` 事实带 `scope.gong`（t173 起），故可用 `same: gong` 把「值符宫」
    # 与「该宫的天／地盘干」绑在一起。这里 `value: "*"` 的语义是**存在性**
    # （该键须有事实，取值不限），不是凑数——星名随盘而变，静态写不出。
    # t173 曾因 15% 通配闸门把这 3 条记为 gate-blocked；t175/t176 加了谓词、
    # 分母变大后，4/27 = 14.8% ≤ 15%，闸门已不再挡（t177 实测复核）。
    "QM-P01": ("{all_of: [{key: zhifu, value: \"*\"}, {key: dipan_gan, value: 丙}], same: gong}", "甲值符加地盘丙奇"),
    "QM-P02": ("{all_of: [{key: tianpan_gan, value: 丙}, {key: zhifu, value: \"*\"}], same: gong}", "丙奇加地盘甲值符"),
    "QM-P31": ("{all_of: [{key: tianpan_gan, value: 庚}, {key: zhifu, value: \"*\"}], same: gong}", "庚临值符"),
    # ── 格名类：引擎已把格名当事实产出（`geju_qimen`，源自 patterns/ruleChecks）──────
    # 沿用既有约定（QM-P14 伏吟局／QM-P15 反吟局 就是 [{key: geju_qimen, value: …}]）。
    # QM-P25「三奇得使 乙奇加甲午甲戌 丙奇加甲子甲申 丁奇加甲寅甲辰」——
    # 引擎 `qimen-analysis.ts` 的 ENVOY 表恰为 {乙:[己,辛], 丙:[戊,庚], 丁:[壬,癸]}，
    # 即 甲午/甲戌 旬首＝辛/己、甲子/甲申＝戊/庚、甲寅/甲辰＝壬/癸，与原文逐项吻合，
    # 故「本盘 patterns 含三奇得使」就是原文所说的条件。
    "QM-P25": ("[{key: geju_qimen, value: 三奇得使}]", "乙奇加甲午甲戌"),
    "QM-P34": ("{all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 丙}], same: gong}", "六庚加丙奇"),
    "QM-P35": ("{all_of: [{key: tianpan_gan, value: 丙}, {key: dipan_gan, value: 庚}], same: gong}", "丙奇加六庚金"),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="奇门天地盘干谓词映射")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    text = YAML_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    rules = {r["rule_id"]: r for r in data["rules"]}

    problems: list[str] = []
    done: set[str] = set()
    for rid, (pred, needle) in MAP.items():
        r = rules.get(rid)
        if r is None:
            problems.append(f"{rid} 不存在")
            continue
        if needle not in (r.get("statement") or ""):
            problems.append(f"{rid} statement 不含复核片段「{needle}」")
        cur = r.get("applicable_to")
        if cur:
            # 幂等：已是本批要写的谓词就跳过（便于增量加条目）；已有**别的**谓词才报错。
            if cur == yaml.safe_load(pred):
                done.add(rid)
            else:
                problems.append(f"{rid} 已有不同谓词，本批不应改写：{cur!r}")
    if problems:
        for p in problems:
            print("FAIL:", p, file=sys.stderr)
        return 1
    todo = [r for r in MAP if r not in done]
    print(f"复核通过：{len(MAP)} 条（已落实 {len(done)}，本次待写 {len(todo)}）")

    if args.dry_run:
        return 0

    for rid, (pred, _) in MAP.items():
        if rid in done:
            continue
        pattern = re.compile(rf"(?m)^(- rule_id: {re.escape(rid)}\n(?:.*\n)*?  applicable_to: )\[\]$")
        text, n = pattern.subn(lambda mo: mo.group(1) + pred, text, count=1)
        if n != 1:
            raise SystemExit(f"改写失败: {rid}")
    YAML_PATH.write_text(text, encoding="utf-8")
    print(f"已写入 {YAML_PATH.relative_to(ROOT)}")

    ledger = [
        {"book": BOOK, "rule_id": rid, "applicable_to_yaml": pred, "evidence_from_statement": needle}
        for rid, (pred, needle) in MAP.items()
    ]
    out = ROOT / "tools/reports/qimen-stem-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())