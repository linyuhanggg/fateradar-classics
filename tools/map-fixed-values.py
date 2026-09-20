#!/usr/bin/env python3
"""把「适用条件是**具名固定取值**」的规则映成谓词（本批 3 条）。

两种形态，都用 v3 已有语法、都不新增事实：

1. **四柱枚举干支对**——形如「庚辰、庚戌、壬辰、戊戌为魁罡日」：
   条件是该**柱**等于列举的某一对。写法用**显式柱位 scope**，不需要 `same`：

       {any_of: [{all_of: [{key: gan, value: 庚, scope: {pillar: day}},
                           {key: zhi, value: 辰, scope: {pillar: day}}]}, …]}

   两句都钉在 `pillar: day` →「日柱＝庚辰」；组间 `any_of` →「日柱是列举之一」。
   （**不能**用 `same: pillar`：`same` 把所有受约束子句绑到**同一个**取值，
   而这里每个候选对是独立的一组。）

3. **位置级课传事实**（六壬）——形如「青龙是否居日上」：
   平铺列表里各写 `scope.palace`（日上／辰上／初传／中传／末传），列表＝或。
   这些位置事实由 `liuren.ts` 的 `pushScoped` 产出；V15 本轮才允许六壬写 `scope.palace`。

2. **具名纳音**——形如「论海中金须配合所见火、水、木、土等条件」：
   `{nayin: 海中金}`。`nayin` 事实由 t170 产出，**此前无任何谓词使用**，本条是首个。

判据必须命中 statement 才落盘。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def pair_on_pillar(gan: str, zhi: str, pillar: str) -> str:
    return (
        f"{{all_of: [{{key: gan, value: {gan}, scope: {{pillar: {pillar}}}}}, "
        f"{{key: zhi, value: {zhi}, scope: {{pillar: {pillar}}}}}]}}"
    )


def any_pairs(pairs: list[tuple[str, str]], pillar: str) -> str:
    return "{any_of: [" + ", ".join(pair_on_pillar(g, z, pillar) for g, z in pairs) + "]}"


# rule_id → (谓词, statement 复核片段, 说明)
MAP: dict[str, tuple[str, str, str]] = {
    "R-06": (
        any_pairs([("庚", "辰"), ("庚", "戌"), ("壬", "辰"), ("戊", "戌")], "day"),
        "庚辰、庚戌、壬辰、戊戌为魁罡日",
        "四对皆日柱；「忌见财官」是断语不是条件，未表达。",
    ),
    "SANMINGTONGH-097": (
        any_pairs(
            [("甲", "寅"), ("乙", "卯"), ("丁", "未"), ("己", "未"), ("庚", "申"), ("辛", "酉"), ("壬", "子"), ("癸", "丑")],
            "day",
        ),
        "八专日（甲寅、乙卯、丁未、己未、庚申、辛酉、壬子、癸丑）",
        "八对皆日柱；「日坐禄旺之地，身强为论；以月令它格为用」是断语，未表达。",
    ),
    # 六壬：位置级天将／六亲（引擎已产出 scope.palace=日上/辰上/初传/中传/末传）。
    # 原文特意点明「青龙在任意一传不等于龙居日本」——`scope.palace=日上` 正是这个区分。
    "LIURENMIBEN-021": (
        "[{key: tianjiang, value: 青龙, scope: {palace: 日上}},"
        " {key: liuqin, value: 妻财, scope: {palace: 初传}},"
        " {key: liuqin, value: 妻财, scope: {palace: 中传}},"
        " {key: liuqin, value: 妻财, scope: {palace: 末传}}]",
        "参看传中是否见财，以及青龙是否居日上",
        "平铺列表＝或：二选一（传中见财 / 青龙居日上）。"
        "引擎自带 unknown `LR-UNKNOWN-MIBEN-021-WIRE` 说「规则 applicableTo 仍为空」，本条即那次接线。",
    ),
    # ── 六爻具名状态（引擎 analysis 已算，t193 才产成事实）────────────────────────
    # 「月建冲爻为月破」「静爻得日辰冲为暗动」的条件，正是引擎给出的**具名分类**
    # （`state.monthStrength` / `state.activity.label`）。取名而不另算。
    "ZENGSHANBUYI-030": (
        "[{key: liuyao_month_strength, value: 月破}]",
        "月建冲爻为月破",
        "条件是「本卦有月破之爻」；后文「静则到底破、动则能伤本变…出月或合日不破」是断法细则，未表达。",
    ),
    "ZENGSHANBUYI-018": (
        "[{key: liuyao_activity, value: 暗动}]",
        "静爻得日辰冲为暗动",
        "条件是「本卦有暗动之爻」；「暗动如同动，能生克他爻」是断法，未表达。",
    ),
    # ── 六壬课体（`keti`）：引擎按取传结果定课体名，事实层早已产出 ──────────────
    # 「伏吟／返吟／八专」在原文里既是课体名、也是条件（adapter 的 is_fuyin/is_fanyin/is_bazhuan
    # 就是判这些），故 {keti: 伏吟课} 正是「本盘为伏吟」的忠实写法。
    # 沿用既有约定（DALIURENDAQU-006 蒿矢/弹射、LIURENZHIYIN-017 元首/重审 都是这么写的）。
    "DALIURENDAQU-010": ("[{key: keti, value: 伏吟课}]", "十二神各居本宫",
        "原文「伏吟有克还为用，无克刚干柔取辰」即伏吟课取传；「月将支与占时支相同」是伏吟的成因。"),
    "DALIURENDAQU-011": ("[{key: keti, value: 返吟课}]", "十二神各居冲位",
        "原文「返吟有克亦为用，无克别有井栏名」即返吟课取传。"),
    "LIURENZHIYIN-009": ("[{key: keti, value: 八专课}]", "干支同位",
        "八专课的定义就是干支同位（引擎 liuren-transmissions.ts 在干支同位时定八专课）；"
        "「四课去重后为两课」是同一结构的另一面，未单独表达。"),
    # 奇门「时干入墓 戊戌、壬辰、丙戌、癸未、丁丑、己丑也」——条件就是**时柱**等于其一。
    # 用显式柱位 scope（t176 的技术），不需要 same：每个候选对是独立一组。
    # 前提是奇门侧产出四柱干支（t186 加，引擎 facts.ganZhi 透传）。
    "QM-P36": (
        any_pairs([("戊", "戌"), ("壬", "辰"), ("丙", "戌"), ("癸", "未"), ("丁", "丑"), ("己", "丑")], "time"),
        "时干入墓，戊戌、壬辰、丙戌、癸未、丁丑、己丑也",
        "六对皆时柱；「入墓」之名取自原文该表，未自行推墓位。",
    ),
    "SANMINGTONGH-004": (
        # 单谓词用**平铺列表**形（[{key,value}]）；不能写成 {nayin: 海中金}——
        # 那不是谓词也不是 v3 组，V16 会当作「未知组字段」拒掉（本批初版即被它拦下）。
        "[{key: nayin, value: 海中金}]",
        "论海中金须配合所见火、水、木、土等条件",
        "本条即「具名纳音」条件；**t170 产出的 `nayin` 事实此前无谓词使用，本条是第一个**。",
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser(description="具名固定取值类规则 → 谓词")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets: dict[Path, str] = {}
    found: dict[str, tuple[Path, dict]] = {}
    problems: list[str] = []
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        text = p.read_text(encoding="utf-8")
        targets[p] = text
        for r in yaml.safe_load(text).get("rules") or []:
            if isinstance(r, dict) and r.get("rule_id") in MAP:
                found[r["rule_id"]] = (p, r)

    done: set[str] = set()
    for rid, (pred, needle, _n) in MAP.items():
        if rid not in found:
            problems.append(f"{rid} 不存在")
            continue
        _p, r = found[rid]
        if needle not in (r.get("statement") or ""):
            problems.append(f"{rid} statement 不含复核片段「{needle}」")
        cur = r.get("applicable_to")
        if cur:
            # 幂等：已经是本批要写的谓词就跳过（可安全重跑，便于增量加条目）；
            # 已有**别的**谓词才报错——那说明有人先动过，本批不该覆盖。
            if cur == yaml.safe_load(pred):
                done.add(rid)
            else:
                problems.append(f"{rid} 已有不同谓词，本批不应改写：{cur!r}")
    if problems:
        for x in problems:
            print("FAIL:", x, file=sys.stderr)
        return 1
    todo = [r for r in MAP if r not in done]
    print(f"复核通过：{len(MAP)} 条（已落实 {len(done)} 条，本次待写 {len(todo)} 条）")

    if args.dry_run:
        for rid, (pred, _n, _d) in MAP.items():
            print(f"  {rid:22} {pred[:100]}{'…' if len(pred) > 100 else ''}")
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
            "note": note,
        }
        for rid, (pred, needle, note) in MAP.items()
    ]
    out = ROOT / "tools/reports/fixed-value-map.json"
    json.dump(ledger, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"台账 {out.relative_to(ROOT)}：{len(ledger)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())