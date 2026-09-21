#!/usr/bin/env python3
"""未映射谓词的可复算三分类报告。

背景：`tools/reports/unmapped-predicates.md` 是过程稿产物，仓内没有生成器，
且含至少 1 条陈旧 rule_id（`LIURENZHIYIN-015` 在该书 rules.yaml 已不存在）。
本脚本从 `references/books/*/*/rules.yaml` 与 `references/vocab/fact-vocab.json`
重新算出「带锚但 applicable_to 为空」的集合，并把每条按**可从 statement 复原出的
事实令牌**分类，供人工复核。

三分类（机械判据，可复算）：

- `no-chart-token`：statement 里找不到该 art 引擎任何 FactKey 的合法取值。
  盘面条件无从复原。可能是通论／体例／元规则，也可能是需要引擎未产出的事实。
- `single-pair`：只复原出 1 个 (key,value) 对。**现有谓词语言本可表达**，
  未映射属报告缺陷或漏做，不是表达力不足。
- `multi-key`：复原出 ≥2 个不同 key 的令牌。需要**同一盘面上多事实同时成立（AND）**，
  而现有 `applicable_to` 平铺列表在消费方是「任一命中即命中」（OR）——
  这才是「条件过于复合」的真实含义。
- `multi-pair-same-key`：同一 key 的 ≥2 个取值。OR 本可表达，同样属漏做。

令牌扫描只采信长度 ≥2 的取值，避免「木」「火」这类单字在散文里假命中；
单字干支另记为 `ganzhi_cue`，不参与分类，仅供复核参考。

用法：
    python3 tools/predicate-gap-report.py                 # 人类可读
    python3 tools/predicate-gap-report.py --json          # 机器可读
    python3 tools/predicate-gap-report.py --art qimen -v  # 单术逐条
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from predicate_lang import has_predicates  # noqa: E402

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


def load_vocab() -> tuple[list[str], dict[str, list[str]], str]:
    data = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
    return list(data["keys"]), dict(data["values"]), data.get("any", "*")


# 各 art 引擎实际产出的 key，与 tools/predicate-report.py 的 ART_EMIT_KEYS 一致。
ART_EMIT_KEYS: dict[str, frozenset[str]] = {
    "bazi": frozenset(
        {
            "rizhu",
            "yueling",
            # 四柱干支与纳音：引擎由已有 ganzhi 四柱／「纳音」行逐柱产出（见 emitBaziFacts）。
            "gan",
            "zhi",
            # 藏干（`PillarFact.hidden`，本气在前）：emitBaziFacts 早就在读它算十神。
            "canggan",
            "nayin",
            "rizhu_strength",
            "geju",
            "yongshen",
            "shishen",
            "shensha",
            "kongwang",
        }
    ),
    "ziwei": frozenset({"ziwei_palace", "ziwei_star", "sihua", "daxian", "liunian_taisui"}),
    "qimen": frozenset(
        {
            # 四柱干支：引擎 facts.ganZhi 直接透传（与 bazi 共用键，按 scope.pillar 区分）。
            "gan",
            "zhi",
            "jiuxing",
            "bamen",
            "bashen",
            "zhifu",
            "zhishi",
                        # 四柱干支：引擎 facts.ganZhi 直接透传（与 bazi 共用键，按 scope.pillar 区分）。
            "gan",
            "zhi",
            "geju_qimen",
            # 天盘干／地盘干：由已有 QimenCell.sky / .earth 逐宫产出。
            "tianpan_gan",
            "dipan_gan",
            "kongwang",
        }
    ),
    "liuren": frozenset(
        {
            "keti",
            "sanchuan",
            "tianjiang",
            # 四柱干支：引擎 facts.ganZhi 直接透传（与 bazi/qimen 共用键，按 scope.pillar 区分）。
            "gan",
            "zhi",
            # 三传所乘六亲：`liuren.ts` 的 pushScoped 已产出（盘面样本实测有
            # scope.palace=初传/中传/末传 的 liuqin），此前只是没登记进本表。
            "liuqin",
            "yuejiang",
            "kongwang",
        }
    ),
    "liuyao": frozenset(
        {
            "shiyao",
            "yingyao",
            "liuqin",
            "liushen",
            "fushen",
            "dongyao",
            # 世序／卦体分类（本宫…游魂／归魂）：引擎 main.sequence 直接透传。
            "liuyao_seq",
            # 纳甲地支（本爻／变爻）：引擎 row.ganzhi[1] / row.changed[1] 直接产出。
            "yao_zhi",
            "bian_yao_zhi",
            # 具名状态三键：引擎 analysis 已算（用神／月建强度／爻活动），此前只进解读文本。
            "liuyao_yongshen",
            "liuyao_month_strength",
            "liuyao_activity",
        }
    ),
    "qizheng": frozenset({"xingyao", "gongwei", "xiudu", "miaowang"}),
}

GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")

# 取值域同义的 key 组：同一个词面在组内多个 key 上都能命中，会虚增「多 key」计数。
# 只按「组」计数才是真实的条件维数。经 facts-sample.json 复核取值域确实重合。
SYNONYM_GROUPS: tuple[frozenset[str], ...] = (
    frozenset({"dongyao", "shiyao", "yingyao"}),  # 皆为爻位 初爻…六爻
    frozenset({"bamen", "zhishi"}),               # 皆为八门
    frozenset({"jiuxing", "zhifu"}),              # 皆为九星
    frozenset({"liuqin", "fushen"}),              # 皆为六亲
)
# 术名本身出现在 statement 里不是条件（如「六爻」同时是 yao 键的取值）。
ART_SELF_NAMES = frozenset({"六爻", "八字", "紫微", "奇门", "六壬", "七政"})


def group_of(key: str) -> str:
    for g in SYNONYM_GROUPS:
        if key in g:
            return "+".join(sorted(g))
    return key

# 需要引擎未产出的事实／非盘面条件的文面提示。只作复核线索，不单独定案。
META_CUES = ("调用", "规则", "pack", "本书", "任务", "adapter", "上游", "已通过", "须作为")
DOCTRINE_CUES = ("为体", "为用", "之理", "之道", "不可", "须", "当", "论命", "万物", "圣人")


def classify(art: str, statement: str, values: dict[str, list[str]]) -> dict:
    keys = ART_EMIT_KEYS.get(art, frozenset())
    tokens: list[tuple[str, str]] = []
    for key in sorted(keys):
        for val in values.get(key) or []:
            # 长度 ≥2，且不是「化禄/化权」这类会大面积误命中的短值集合的例外——
            # 词表本身即为判据，只按长度过滤。
            if len(val) < 2 or val not in statement:
                continue
            if val in ART_SELF_NAMES:  # 术名不是条件
                continue
            tokens.append((key, val))
    # 去重并保持稳定序
    seen: set[tuple[str, str]] = set()
    uniq = [t for t in tokens if not (t in seen or seen.add(t))]

    # 同义组内同一词面只算一维，避免 dongyao+shiyao+yingyao 把一维虚增成三维。
    groups: dict[str, set[str]] = {}
    for k, v in uniq:
        groups.setdefault(group_of(k), set()).add(v)
    n_keys = len(groups)
    n_pairs = sum(len(v) for v in groups.values())

    if n_pairs == 0:
        kind = "no-chart-token"
    elif n_keys >= 2:
        kind = "multi-key"
    elif n_pairs >= 2:
        kind = "multi-pair-same-key"
    else:
        kind = "single-pair"

    ganzhi = sorted((set(statement) & GAN) | (set(statement) & ZHI))
    return {
        "kind": kind,
        "tokens": [{"key": k, "value": v} for k, v in uniq],
        "keys_hit": sorted(groups),
        "ganzhi_cue": ganzhi,
        "meta_cue": [c for c in META_CUES if c in statement],
        "doctrine_cue": [c for c in DOCTRINE_CUES if c in statement],
    }


def collect() -> dict:
    keys, values, any_token = load_vocab()
    rows: list[dict] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        system, slug = book.get("system"), book.get("slug")
        art = art_of(system, slug)
        if art not in set(ARTS) | set(REFERENCE_ARTS):
            continue
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or not isinstance(rule.get("anchor"), dict):
                continue
            preds = rule.get("applicable_to") or []
            if has_predicates(preds):
                continue
            st = rule.get("statement") or ""
            info = classify(art, st, values)
            rows.append(
                {
                    "art": art,
                    "book": f"{system}/{slug}",
                    "rule_id": rule.get("rule_id"),
                    "statement": st,
                    **info,
                }
            )
    return {"rows": rows, "any": any_token}


def load_ledgers() -> dict[tuple[str, str], dict]:
    """把各 art 的判定台账读成 (book, rule_id) → decision。台账是过程记录，缺失不报错。

    `captain-audit.json` 的 `reverted` 列表是**权威覆盖**：复核撤回的条目以 captain 结论为准，
    但不改写各 art 台账原件（保留「谁在什么阶段判了什么」的可追溯性）。
    """
    out: dict[tuple[str, str], dict] = {}
    for path in sorted((ROOT / "tools/reports/predicate-decisions").glob("*.json")):
        if path.name == "captain-audit.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for row in data.get("decisions") or []:
            key = (row.get("book"), row.get("rule_id"))
            if key[0] and key[1]:
                out[key] = {**row, "_ledger": path.name}

    audit_path = ROOT / "tools/reports/predicate-decisions/captain-audit.json"
    if audit_path.is_file():
        try:
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            audit = {}
        for row in audit.get("reverted") or []:
            key = (row.get("book"), row.get("rule_id"))
            if not (key[0] and key[1]):
                continue
            prev = out.get(key, {})
            out[key] = {
                **prev,
                "decision": "unmapped",
                "reason_class": row.get("reason_class") or "not-a-condition",
                "note": f"captain 复核撤回（原映射：{row.get('was')}）",
                "_ledger": "captain-audit.json",
                "_reverted_from": row.get("was"),
            }
    return out


# 事实缺口归因：**分诊线索，不是判决**。只用来给「下一批做什么」排序。
# 归类依据是台账里那句手写的「需要的事实」文本。**分类带 art 约束**——否则会出现
# 「八字条目的『时干』被归到奇门」这类串档（初版实测过）。
FACT_GAP_RULES: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    # (标签, 关键词, 适用 art；空＝不限)
    ("六爻：月建日辰／变卦变爻／爻位", ("月建", "日辰", "变爻", "变卦", "六冲", "六合", "入墓", "卦名", "旺衰", "空亡", "世爻", "应爻", "互卦"), ("liuyao",)),
    ("奇门：天地盘干／值符值使落宫／时干", ("值符", "直使", "三奇", "天盘干", "地盘干", "六庚", "乙奇", "时干", "六壬临", "六癸"), ("qimen",)),
    ("六壬：四课／课体细节／驿马", ("四课", "驿马", "天将落宫", "遥克", "上下克", "课体"), ("liuren",)),
    ("梅花：体用生克", ("体卦", "用卦", "体用", "互卦"), ("meihua", "yili")),
    ("纳音：象辞与纳音名", ("纳音",), ()),
    ("神煞：具体名与取法", ("神煞", "关煞", "德干", "秀干", "元辰"), ()),
    ("地支关系：三合局／方局／冲合", ("三合", "方局", "相冲", "六冲", "自刑", "下克上"), ()),
    ("柱干支：时／岁／月／日柱", ("岁干", "月干", "日干", "时干", "柱干", "日支", "月支", "时支", "年支", "柱干支", "天干类", "藏干"), ()),
    ("格局／行限／亮度", ("格局", "行限", "虚星", "三方四正", "亮度"), ()),
    ("大运／流年干支", ("大运", "流年"), ()),
    ("性别（女命／男命）", ("性别", "女命", "男命"), ()),
)


def fact_gap_summary(rows: list[dict]) -> list[tuple[str, list[dict]]]:
    """把**当前仍未映射**且台账判为 fact-not-emitted 的规则按缺口归因分组。

    必须按 live `applicable_to` 过滤：台账是当时的过程记录，此后被映射掉的条目
    仍写着 fact-not-emitted，不过滤会把已完成的算成待办。
    """
    ledgers = load_ledgers()
    idx = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        k = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                idx[(k, r.get("rule_id"))] = r
    groups: dict[str, list[dict]] = {}
    for r in rows:
        d = ledgers.get((r["book"], r["rule_id"]))
        if not d or d.get("reason_class") != "fact-not-emitted":
            continue
        live = idx.get((r["book"], r["rule_id"]))
        if live is None or (live.get("applicable_to") or []):
            continue
        text = (d.get("missing_fact") or "") + " " + (d.get("note") or "")
        label = "其他／未归类"
        for name, keys, arts in FACT_GAP_RULES:
            if arts and r["art"] not in arts:
                continue
            if any(k in text for k in keys):
                label = name
                break
        groups.setdefault(label, []).append(
            {"rule_id": r["rule_id"], "book": r["book"], "art": r["art"], "missing": (d.get("missing_fact") or "")[:60]}
        )
    return sorted(groups.items(), key=lambda kv: -len(kv[1]))


REASON_LABEL = {
    "not-a-condition": "原文无盘面适用条件（通论／体例／取象表／起例取法）",
    "meta-rule": "pack 元规则／调用条件，不是盘面条件",
    "fact-not-emitted": "需要引擎未产出的事实",
    "condition-too-vague": "原文有条件但口径未定或明确拒绝单一条件",
}
KIND_LABEL = {
    "no-chart-token": "statement 中无可复原的 FactKey 取值",
    "single-pair": "可复原 1 个谓词对（现有语言本可表达）",
    "multi-pair-same-key": "同一 key 多个取值（OR 本可表达）",
    "multi-key": "跨 key 多事实（需 AND）",
}


def write_markdown(rows: list[dict], *, path: Path) -> None:
    """重新生成未映射报告：每条都带可复算的分类与台账理由。

    取代旧的 `tools/reports/unmapped-predicates.md` —— 旧件无生成器、含陈旧 rule_id，
    且把 599 条一律写成「条件过于复合」，与逐条复核结果不符。
    """
    ledgers = load_ledgers()
    by_art: dict[str, list[dict]] = {}
    for r in rows:
        by_art.setdefault(r["art"], []).append(r)

    lines: list[str] = [
        "# 未能翻译成谓词的规则（可复算版）",
        "",
        "由 `python3 tools/predicate-gap-report.py --md tools/reports/unmapped-predicates.md` 生成。",
        "口径：`references/books/*/*/rules.yaml` 中 **有 anchor 且 `applicable_to` 为空** 的规则。",
        "旧版本文件无生成器、含 1 条已不存在的 `LIURENZHIYIN-015`，且把每一条都标成",
        "「条件过于复合，现有谓词表达不了」——逐条复核后该说法只对其中少数成立，故整份重写。",
        "",
        "`分类` 是机械判据（见脚本 `classify()`），`台账理由` 是逐条复核结论（见",
        "`tools/reports/predicate-decisions/*.json`）。两者不一致时以台账为准，且台账必须给原文依据。",
        "",
        f"共 **{len(rows)}** 条。",
        "",
    ]
    totals: dict[str, Counter] = {}
    for art in sorted(by_art):
        rows_art = sorted(by_art[art], key=lambda r: (r["book"], r["rule_id"]))
        c = Counter()
        for r in rows_art:
            d = ledgers.get((r["book"], r["rule_id"]))
            c[d.get("reason_class") if d else "未复核"] += 1
        totals[art] = c

    lines.append("| art | 合计 | " + " | ".join(REASON_LABEL.values()) + " | 未复核 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for art in sorted(by_art):
        c = totals[art]
        lines.append(
            f"| `{art}` | {sum(c.values())} | "
            + " | ".join(str(c.get(k, 0)) for k in REASON_LABEL)
            + f" | {c.get('未复核', 0)} |"
        )
    lines.append("")

    for art in sorted(by_art):
        lines.append(f"## {art}")
        lines.append("")
        lines.append("| book | rule_id | 分类 | 台账理由 | 缺的事实 | 原文依据 | statement |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in sorted(by_art[art], key=lambda r: (r["book"], r["rule_id"])):
            d = ledgers.get((r["book"], r["rule_id"])) or {}
            reason = REASON_LABEL.get(d.get("reason_class"), d.get("reason_class") or "未复核")
            stmt = (r["statement"] or "").replace("|", "\\|")
            if len(stmt) > 70:
                stmt = stmt[:70] + "…"
            ev = (d.get("evidence_from_statement") or "").replace("|", "\\|")[:40]
            missing = (d.get("missing_fact") or "").replace("|", "\\|")[:40]
            lines.append(
                f"| `{r['book']}` | `{r['rule_id']}` | {KIND_LABEL.get(r['kind'], r['kind'])} "
                f"| {reason} | {missing} | {ev} | {stmt} |"
            )
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="未映射谓词的可复算三分类")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--art", default=None, help="只看某一术")
    ap.add_argument("-v", "--verbose", action="store_true", help="逐条打印 statement")
    ap.add_argument("--md", default=None, help="把报告写回该 markdown 路径（可复算）")
    ap.add_argument("--fact-gaps", action="store_true", help="按「需要的事实」给当前未映射规则排序（下批优先级）")
    args = ap.parse_args()

    data = collect()
    rows = data["rows"]
    if args.art:
        rows = [r for r in rows if r["art"] == args.art]

    by_art: dict[str, Counter] = {}
    for r in rows:
        by_art.setdefault(r["art"], Counter())[r["kind"]] += 1

    if args.fact_gaps:
        groups = fact_gap_summary(rows)
        total = sum(len(v) for _, v in groups)
        if args.json:
            # --json 时**不得**先 print：那会把抬头混进 stdout，让下游 json.load 解析失败
            # （本工具初版即如此，被自己的调用方抓到）。
            json.dump({"total": total, "groups": {k: v for k, v in groups}}, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return 0
        print(f"当前仍为 fact-not-emitted 的未映射规则 {total} 条（已按 live applicable_to 过滤）")
        for name, items in groups:
            print(f"\n{len(items):4}  {name}")
            for it in items[:3]:
                print(f"        {it['rule_id']:20} {it['missing']}")
        return 0

    if args.md:
        write_markdown(rows, path=(ROOT / args.md) if not Path(args.md).is_absolute() else Path(args.md))
        print(f"wrote {args.md}（{len(rows)} 条）")
        return 0

    if args.json:
        json.dump(
            {
                "total": len(rows),
                "by_art": {a: dict(c) for a, c in by_art.items()},
                "rows": rows,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    kinds = ("no-chart-token", "single-pair", "multi-pair-same-key", "multi-key")
    print(f"未映射（带锚且 applicable_to 为空）共 {len(rows)} 条")
    print(f"{'art':10} " + " ".join(f"{k:>20}" for k in kinds) + f"{'合计':>8}")
    for art in list(ARTS) + list(REFERENCE_ARTS):
        if art not in by_art:
            continue
        c = by_art[art]
        print(f"{art:10} " + " ".join(f"{c.get(k, 0):>20}" for k in kinds) + f"{sum(c.values()):>8}")
    total = Counter(r["kind"] for r in rows)
    print(f"{'合计':10} " + " ".join(f"{total.get(k, 0):>20}" for k in kinds) + f"{len(rows):>8}")

    if args.verbose:
        for r in rows:
            print(f"\n[{r['art']}] {r['book']} {r['rule_id']}  <{r['kind']}>")
            print(f"  {r['statement'][:200]}")
            if r["tokens"]:
                print("  tokens: " + ", ".join(f"{t['key']}={t['value']}" for t in r["tokens"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())