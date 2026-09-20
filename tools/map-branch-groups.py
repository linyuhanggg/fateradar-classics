#!/usr/bin/env python3
"""把「地支成组」类规则映成谓词（本轮 9 条，全部用 v3 已有语法，零新事实）。

这类规则的适用条件是「某几个地支同时出现在四柱里」——

    三合局（亥卯未木局…）成局者气势全；方局（寅卯辰东方…）齐全者气势纯
    申子辰、巳酉丑、寅午戌、亥卯未为三合组合；原文强调**三字缺一不能**直接按三合化局论
    子午、丑未、寅申、卯酉、辰戌、巳亥相冲

而 t168 的 v3 语法**本来就写得出来**：

    {any_of: [{all_of: [{key: zhi, value: 申}, {key: zhi, value: 子}, {key: zhi, value: 辰}]}, …]}

`all_of` 三句各自要求一个 `zhi` 事实匹配 → 「三支齐」；组间 `any_of` → 「任一局成」。
**不加 `same`（不绑柱位）**：三合／方局要的正是三支**分布在不同柱**上，绑柱位反而错。
这也正是「三字缺一不能论」那句原文的机器表达。地支事实由 t170 的逐柱 `zhi` 提供。

本批**不新增 FactKey、不动闸门、不用通配**。判据必须命中 statement 才落盘。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# 成组定义（取自原文列举，不另行发明）
SANHE = [("申", "子", "辰"), ("巳", "酉", "丑"), ("寅", "午", "戌"), ("亥", "卯", "未")]
FANGJU = [("寅", "卯", "辰"), ("巳", "午", "未"), ("申", "酉", "戌"), ("亥", "子", "丑")]
LIUCHONG = [("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")]
TUJU = [("辰", "戌", "丑", "未")]
# 六爻：地支六合／六冲／三刑（原文列举）
LIUHE = [("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")]
LIUCHONG_YAO = [("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")]
SANXING = [("寅", "巳", "申"), ("丑", "戌", "未"), ("子", "卯")]


def group(*branches: str, key: str = "zhi") -> str:
    """一组地支的 all_of。`key` 默认四柱地支 `zhi`；六爻用爻支 `yao_zhi`。"""
    inner = ", ".join(f"{{key: {key}, value: {b}}}" for b in branches)
    return f"{{all_of: [{inner}]}}"


def any_of(groups: list[tuple[str, ...]], *, key: str = "zhi") -> str:
    """组间为或。"""
    return "{any_of: [" + ", ".join(group(*g, key=key) for g in groups) + "]}"


# rule_id → (谓词, statement 复核片段, 已知的部分覆盖说明)
MAP: dict[str, tuple[str, str, str]] = {
    "SANMINGTONGH-015": (
        any_of(SANHE),
        "申子辰、巳酉丑、寅午戌、亥卯未为三合组合",
        "原文「三字缺一不能直接按三合化局论」正是本式（每局三句 all_of）要表达的。",
    ),
    "LIXUZHONGMIN-070": (
        any_of(SANHE),
        "寅午戌火体、亥卯未木体、申子辰水体、巳酉丑金体",
        "末句「土则从四事成之」未表达（土不另成三合局）。",
    ),
    "YUZHAOSHENYI-040": (
        any_of(SANHE),
        "五行三合局齐者(木亥卯未/火寅午戌/金巳酉丑/水申子辰)",
        "",
    ),
    "DITIANSUICHA-DR-02": (
        any_of(SANHE + FANGJU),
        "三合局（亥卯未木局等）成局者气势全；方局（寅卯辰东方等）齐全者气势纯",
        "「局成宜顺、局破宜疏」的处置语未表达。",
    ),
    "SANMINGTONGH-095": (
        any_of(SANHE + FANGJU),
        "各神兽对应五行须在命局成形（三合或方局）",
        "「格局清纯不破」未表达（需格局与破格判定）。",
    ),
    "SANMINGTONGH-R-06": (
        any_of(SANHE + FANGJU + TUJU),
        "木局曲直（亥卯未或寅卯辰全）",
        "土局稼穑为四支全（辰戌丑未），已按四句 all_of 表达；「专局成时以化神为用」未表达。",
    ),
    "SANMINGTONGH-018": (
        any_of(LIUCHONG),
        "子午、丑未、寅申、卯酉、辰戌、巳亥相冲",
        "六对相冲逐对成组；「冲动、移动、变化之象」是断语不是条件。",
    ),
    "DITIANSUICHA-031": (
        group("卯", "酉"),
        "卯酉冲为震兑战",
        "",
    ),
    "DITIANSUICHA-032": (
        group("子", "午"),
        "子午冲为坎离战",
        "",
    ),
    # ── 六爻：爻支成组（事实来自 t178 新增的 `yao_zhi`）──────────────────────
    # 同为「几个地支同时出现」，只是键换成爻支 `yao_zhi`；仍然**不加 same**——
    # 六合／六冲／三刑要的正是这几个支落在**不同爻**上（同支两见是自刑，另一回事）。
    "ZR-07": (
        any_of(LIUHE, key="yao_zhi"),
        "子丑、寅亥、卯戌、辰酉、巳申、午未六合",
        "「合则成事、合则停、合住忌神则解凶」是断语不是条件，未表达；"
        "本条只用爻支，未含月建／日辰之支（更窄，不是更宽）。",
    ),
    "ZENGSHANBUYI-ZR-07": (
        any_of(LIUCHONG_YAO, key="yao_zhi"),
        "子午、丑未、寅申、卯酉、辰戌、巳亥六冲",
        "同上：只用爻支。",
    ),
    "ZENGSHANBUYI-024": (
        any_of(SANXING, key="yao_zhi"),
        "寅巳申、丑戌未、子卯三刑",
        "原文列三组；「刑则有损伤纠葛」是断语不是条件。只用爻支，未含日月之支。",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="地支成组类规则 → v3 谓词")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    problems: list[str] = []
    targets: dict[Path, str] = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        targets[p] = p.read_text(encoding="utf-8")

    found: dict[str, tuple[Path, dict]] = {}
    for p, text in targets.items():
        d = yaml.safe_load(text)
        for r in d.get("rules") or []:
            if isinstance(r, dict) and r.get("rule_id") in MAP:
                found[r["rule_id"]] = (p, r)

    done: set[str] = set()
    for rid, (pred, needle, _note) in MAP.items():
        if rid not in found:
            problems.append(f"{rid} 不存在")
            continue
        _p, r = found[rid]
        if needle not in (r.get("statement") or ""):
            problems.append(f"{rid} statement 不含复核片段「{needle}」")
        cur = r.get("applicable_to")
        if cur:
            # 幂等：已是本批要写的谓词就跳过；已有**别的**谓词才报错。
            if cur == yaml.safe_load(pred):
                done.add(rid)
            else:
                problems.append(f"{rid} 已有不同谓词，本批不应改写")
    if problems:
        for x in problems:
            print("FAIL:", x, file=sys.stderr)
        return 1
    print(f"复核通过：{len(MAP)} 条（已落实 {len(done)}，本次待写 {len(MAP) - len(done)}）")

    if args.dry_run:
        for rid, (pred, _n, _note) in MAP.items():
            print(f"  {rid:22} {pred[:96]}{'…' if len(pred) > 96 else ''}")
        return 0

    for rid, (pred, _needle, _note) in MAP.items():
        if rid in done:
            continue
        path, _r = found[rid]
        text = targets[path]
        pattern = re.compile(rf"(?m)^(- rule_id: {re.escape(rid)}\n(?:.*\n)*?  applicable_to: )\[\]$")
        text, n = pattern.subn(lambda mo: mo.group(1) + pred, text, count=1)
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
            "applicable_to_yaml": pred,
            "evidence_from_statement": needle,
            "partial": note,
        }
        for rid, (pred, needle, note) in MAP.items()
    ]
    out = ROOT / "tools/reports/branch-group-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())