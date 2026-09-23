#!/usr/bin/env python3
"""把规则当工具调用：入参盘面状态，返回结论 + 置信度 + 出处。

实现 `docs/PREDICATE-LANGUAGE-V3.md` 的三值语义（满足／不满足／信息不足）。
这是古籍仓侧的可执行参考实现；产品仓 `src/lib/rules/matcher.ts` 是同一契约的消费方实现。

    python3 tools/eval-predicates.py --art qimen --case caseA
    python3 tools/eval-predicates.py --art bazi --facts /tmp/facts.json --json
    python3 tools/eval-predicates.py --book san-shi/qimen-dunjia-tongzhi --case caseB -v

`--facts` 接受两种 JSON：
  1. `tools/reports/facts-sample.json` 那样的 `{art: {case: {label, facts: [...]}}}`
  2. 直接的盘面事实数组 `[{key, value, scope, derivedFrom}, ...]`

**置信度的定义（机械、透明，不是预测准确率）**

    fact_coverage   = 表达式引用到的 FactKey 中，本盘所需密集柱位事实均在场的比例
    wildcard_penalty = 表达式里用到通配 `*` 时的 0.2 折扣
    confidence      = round(fact_coverage * (1 - wildcard_penalty), 3)

它衡量的是**输入完备度**，即「这个结论有多少是建立在真实到手的盘面事实上的」。
它**不**表示古籍预测的准确度；`verified` 恒为 `false`，电子文本匹配与测试都不能代替人工影印核验。

三值语义要点（缺输入不是「不满足」）：
  · 谓词的 key 完全缺失，或 gan/zhi/canggan 所需柱位缺失 → 该子句 `unknown`
  · `any_of`：有真即真；无真而有 unknown → unknown；否则假
  · `all_of`：有假即假；无假而有 unknown → unknown；否则真（再校验 `same` 同位置绑定）
  · `none_of`：判「事实存在与否」。有匹配 → 假；无匹配但有 key 缺失 → unknown（无法证明「没有」）；
    无匹配且 key 齐全 → 真
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from predicate_lang import iter_predicates as _iter_leaves  # noqa: E402

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

TRUE, FALSE, UNKNOWN = "满足", "不满足", "信息不足"
SCOPE_FIELDS = ("layer", "pillar", "palace", "gong", "yao", "ruleId")


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


class Clause:
    """一个子句的求值结果：三值 + 命中事实 + 各 scope 字段上的绑定值。"""

    __slots__ = ("state", "matched", "bindings")

    def __init__(self, state: str, matched: list[dict], bindings: dict[str, set]):
        self.state = state
        self.matched = matched
        self.bindings = bindings


def fact_matches(fact: dict, pred: dict) -> bool:
    if is_unknown_fact(fact):
        return False
    if fact.get("key") != pred.get("key"):
        return False
    val = pred.get("value")
    if val != "*" and fact.get("value") != val:
        return False
    return fact_scope_matches(fact, pred)


def fact_scope_matches(fact: dict, pred: dict) -> bool:
    return all(
        (fact.get("scope") or {}).get(field) == want
        for field, want in (pred.get("scope") or {}).items()
    )


# 完整四柱每柱必有天干、地支、至少一枚藏干；其他键（如神煞）
# 是稀疏标签，某柱未出现可以是明确不满足，不能一律当缺输入。
COMPLETE_PILLAR_FACT_KEYS = {"gan", "zhi", "canggan", "natal_month_single_qi_hidden_stem"}

# One value is expected for each exact scope. A duplicate value is harmless;
# contradictory values, including a known value beside an explicit unknown,
# cannot witness a rule. Labels such as shishen/canggan are intentionally
# absent because they can have several values at one pillar.
SINGLE_VALUE_BAZI_FACT_KEYS = {
    "rizhu", "natal_day_gan", "yueling", "gender", "spouse_palace_zhi",
    "gan", "zhi", "gan_element", "nayin", "rizhu_strength", "geju",
    "natal_month_single_qi_hidden_stem",
    "tiaohou_profile_status", "dayun_direction", "dayun_gan_zhi",
    "liunian_gan", "liunian_zhi", "liunian_gan_zhi",
    "dayun_liunian_relation_class", "suiyun_binglin", "suiyun_same_zhi",
    "rescue_condition", "liunian_activation", "yongshen_effective", "jishen_empowered",
}


def has_conflicting_single_value_facts(key: str, scoped: list[dict]) -> bool:
    if key not in SINGLE_VALUE_BAZI_FACT_KEYS:
        return False
    values_by_scope: dict[tuple, set] = {}
    for fact in scoped:
        scope = fact.get("scope") or {}
        exact_scope = tuple(scope.get(field) for field in ("layer", "year", "pillar", "palace", "gong", "yao", "ruleId"))
        values = values_by_scope.setdefault(exact_scope, set())
        values.add(fact.get("value"))
        if len(values) > 1:
            return True
    return False


def is_unknown_fact(fact: dict) -> bool:
    # Only these registered contracts use this value as missing input.
    # Do not reinterpret arbitrary open-vocabulary text as an unknown marker.
    return fact.get("key") in {
        "suiyun_binglin", "suiyun_same_zhi", "dayun_liunian_relation_class",
        "rescue_condition", "liunian_activation", "yongshen_effective", "jishen_empowered",
    } and fact.get("value") == "信息不足"


def referenced_keys(clause) -> set[str]:
    if not isinstance(clause, dict):
        return set()
    if "key" in clause:
        return {clause["key"]} if isinstance(clause.get("key"), str) else set()
    out: set[str] = set()
    for branch in ("any_of", "all_of", "none_of"):
        for child in clause.get(branch) or []:
            out |= referenced_keys(child)
    return out


def uses_wildcard(clause) -> bool:
    if not isinstance(clause, dict):
        return False
    if "key" in clause:
        return clause.get("value") == "*"
    return any(uses_wildcard(c) for b in ("any_of", "all_of", "none_of") for c in clause.get(b) or [])


def constrains(clause, field: str) -> bool:
    if not isinstance(clause, dict):
        return False
    if "key" in clause:
        return field in (clause.get("scope") or {})
    return any(constrains(c, field) for b in ("any_of", "all_of", "none_of") for c in clause.get(b) or [])


def eval_predicate(pred: dict, facts: list[dict], present: set[str]) -> Clause:
    key = pred.get("key")
    if key == "liuren_selection_rule_status" and not (pred.get("scope") or {}).get("ruleId"):
        return Clause(UNKNOWN, [], {})
    if key not in present:
        return Clause(UNKNOWN, [], {})
    scoped = [f for f in facts if f.get("key") == key and fact_scope_matches(f, pred)]
    if has_conflicting_single_value_facts(key, scoped):
        return Clause(UNKNOWN, [], {})
    if (pred.get("scope") or {}).get("pillar") and key in COMPLETE_PILLAR_FACT_KEYS and not scoped:
        # Another pillar carrying the same dense FactKey does not prove this
        # pillar was emitted. Missing input cannot prove a negative claim.
        return Clause(UNKNOWN, [], {})
    if key == "liuren_selection_rule_status" and (pred.get("scope") or {}).get("ruleId"):
        # This key is multi-valued across rules. Another rule's record never
        # proves that the requested rule was checked on this chart.
        if not scoped or len({f.get("value") for f in scoped}) != 1:
            return Clause(UNKNOWN, [], {})
    matched = [f for f in facts if fact_matches(f, pred)]
    if not matched:
        if any(is_unknown_fact(f) for f in scoped):
            return Clause(UNKNOWN, [], {})
        return Clause(FALSE, [], {})
    # 绑定值取自**命中事实**携带的 scope 字段（不只是谓词自己声明的那些）：
    # `same: palace` 要能绑「两个谓词都没写 palace」的同宫事实，否则 same 就没有用途。
    bindings: dict[str, set] = {}
    for f in matched:
        for field, val in (f.get("scope") or {}).items():
            if field in SCOPE_FIELDS and val is not None:
                bindings.setdefault(field, set()).add(val)
    return Clause(TRUE, matched, bindings)


def eval_clause(clause, facts: list[dict], present: set[str]) -> Clause:
    if not isinstance(clause, dict):
        return Clause(UNKNOWN, [], {})
    if "key" in clause:
        return eval_predicate(clause, facts, present)

    if "any_of" in clause:
        results = [eval_clause(c, facts, present) for c in clause["any_of"]]
        matched = [f for r in results if r.state == TRUE for f in r.matched]
        if any(r.state == TRUE for r in results):
            state = TRUE
        elif any(r.state == UNKNOWN for r in results):
            state = UNKNOWN
        else:
            state = FALSE
        bindings = _merge_bindings(r for r in results if r.state == TRUE)
    else:
        results = [eval_clause(c, facts, present) for c in clause.get("all_of") or []]
        if any(r.state == FALSE for r in results):
            state = FALSE
        elif any(r.state == UNKNOWN for r in results):
            state = UNKNOWN
        else:
            state = TRUE
        matched = [f for r in results for f in r.matched]
        bindings = _merge_bindings(results)
        # 同位置绑定：本 all_of 内**命中事实带该字段的子句**必须能落在同一个取值上。
        # 注意：绑定看的是「命中事实携带的字段值」，不是「谓词自己写没写 scope」——
        # 否则「禄存与天马同宫」这种两个谓词都没写 palace 的情形就绑不起来，而它正是 same 的用途。
        if state == TRUE and clause.get("same"):
            field = clause["same"]
            common: set | None = None
            for r in results:
                vals = r.bindings.get(field) or set()
                if not vals:
                    continue  # 该子句的命中事实不带此字段 → 不受约束
                common = vals if common is None else (common & vals)
            if common is not None and not common:
                state = FALSE

    # none_of：判「事实存在与否」，与上面整体再相「与」。
    none_of = clause.get("none_of")
    if none_of:
        states = [eval_clause(c, facts, present) for c in none_of]
        if any(r.state == TRUE for r in states):
            state = FALSE
        elif state != FALSE and any(r.state == UNKNOWN for r in states):
            state = UNKNOWN
    return Clause(state, matched, bindings)


def _merge_bindings(results) -> dict[str, set]:
    out: dict[str, set] = {}
    for r in results:
        for field, vals in r.bindings.items():
            out.setdefault(field, set()).update(vals)
    return out


def load_chart(path: Path, art: str, case: str | None) -> tuple[list[dict], str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data, case or "inline"
    if art not in data:
        raise SystemExit(f"{path}: 没有 art={art}（有 {sorted(data)}）")
    cases = data[art]
    if case:
        if case not in cases:
            raise SystemExit(f"{path}: art={art} 没有 case={case}（有 {sorted(cases)}）")
        return cases[case]["facts"], case
    name = sorted(cases)[0]
    return cases[name]["facts"], name


def load_rules(book: str | None, art: str | None) -> list[dict]:
    out: list[dict] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        bk = data.get("book") or {}
        system, slug = bk.get("system"), bk.get("slug")
        if book:
            if f"{system}/{slug}" != book:
                continue
        elif art_of(system, slug) != art:
            continue
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            out.append({"book": f"{system}/{slug}", "title": bk.get("title"), **rule})
    return out


def evaluate(rule: dict, facts: list[dict]) -> dict:
    ap = rule.get("applicable_to")
    present = {f.get("key") for f in facts if isinstance(f, dict) and not is_unknown_fact(f)}
    keys = referenced_keys(ap if isinstance(ap, dict) else {"any_of": ap or []})
    if not ap:
        return {
            "rule_id": rule.get("rule_id"),
            "book": rule.get("book"),
            "verdict": UNKNOWN,
            "reason": "本条未声明任何适用谓词（applicable_to 为空），无从判定",
            "confidence": 0.0,
            "fact_coverage": None,
            "matched": [],
            "verified": bool(rule.get("verified")),
        }
    clause = ap if isinstance(ap, dict) else {"any_of": ap}
    res = eval_clause(clause, facts, present)
    missing = sorted({
        pred["key"] for pred in _iter_leaves(clause)
        if eval_predicate(pred, facts, present).state == UNKNOWN
    })
    covered = keys - set(missing)
    coverage = (len(covered) / len(keys)) if keys else 1.0
    penalty = 0.2 if uses_wildcard(clause) else 0.0
    confidence = round(max(0.0, coverage * (1.0 - penalty)), 3)
    anchor = rule.get("anchor") or {}
    return {
        "rule_id": rule.get("rule_id"),
        "book": rule.get("book"),
        "book_title": rule.get("title"),
        "verdict": res.state,
        "confidence": confidence,
        "fact_coverage": round(coverage, 3),
        "missing_fact_keys": missing,
        # `matched` 是**结论为「满足」时的见证集**：不满足/信息不足时一律留空，
        # 免得消费方把「各子句单独命中过」误当成整条成立（all_of 里这很常见）。
        "matched": (
            [
                {"key": f.get("key"), "value": f.get("value"), "scope": f.get("scope")}
                for f in res.matched
            ]
            if res.state == TRUE
            else []
        ),
        # 出处：电子文本溯源（原文行范围 + 逐字摘录），不是人工影印核验结论。
        "source": {
            "rule_id": rule.get("rule_id"),
            "book": rule.get("book"),
            "anchor": {
                "file": anchor.get("file"),
                "start_line": anchor.get("start_line"),
                "end_line": anchor.get("end_line"),
            },
            "quote": rule.get("quote"),
            "statement": rule.get("statement"),
            "verification": "provisional",
        },
        "verified": bool(rule.get("verified")),
    }


# ── 「键本身域完备」：在这些键上，任何无 scope 的 {key: 某取值} 子句**必然成立** ──────
# 判据不是「样本里都出现」（2 盘不足以判定），而是**引擎按固定轮排/固定布列产出该键的全部取值**，
# 已逐个核对产出代码：
#   liuyao.liushen      六神按固定次序轮排六爻 → 6 神每盘齐（facts/emit.ts 逐爻 row.spirit）
#   qimen.bamen         八门固定布列八宫 → 8 门每盘齐（grid.door）
#   qimen.jiuxing       九星固定布列（中五寄坤，天禽随 hostedStar）→ 9 星每盘齐
#   ziwei.sihua         禄权科忌每次各落一星 → 4 化每盘齐（palaces.hua）
#   ziwei.ziwei_palace  十二宫恒在，另加「身宫」标记 → 每盘齐（palaces.name/isBody）
#   liuren.sanchuan     三传恒有 → 初/中/末每盘齐（chuan.label）
# **有意不含** bazi.shishen／qizheng.gongwei 等：它们虽在两个样本里恰好齐，
# 但取值由可变输入派生（四柱十神、七政宫位），**不足以判定结构完备**——
# 宁可漏报也不误报，这类另以 sample_complete 单列备查。
DOMAIN_COMPLETE_KEYS: dict[str, set[str]] = {
    "liuyao": {"liushen"},
    "qimen": {"bamen", "jiuxing"},
    "ziwei": {"sihua", "ziwei_palace"},
    "liuren": {"sanchuan"},
}
# 样本内恰好齐、但结构性未核：只列备查，不计入 hard
SAMPLE_COMPLETE_KEYS: dict[str, set[str]] = {
    "bazi": {"shishen"},
    "qizheng": {"gongwei", "xingyao", "miaowang"},
}


def _or_position_taut(ap, keys: set[str]):
    """在**或位**找到一条其键域完备的子句（平铺列表成员，或整支都恒真的 any_of 分支）。

    只有或位上的恒真子句才会让整条规则恒真；`all_of` 里的恒真子句不影响结论。
    """
    def taut(cl) -> bool:
        return isinstance(cl, dict) and not cl.get("scope") and cl.get("key") in keys

    if isinstance(ap, list):
        for cl in ap:
            if taut(cl):
                return cl
        return None
    if isinstance(ap, dict) and "any_of" in ap:
        for branch in ap["any_of"]:
            ls = list(_iter_leaves(branch))
            if ls and all(taut(x) for x in ls):
                return ls
    return None


def _or_position_single_key_covering(ap, leaves, values: dict[str, list[str]]) -> list[str]:
    """或位「单键穷举覆盖」检测：只有这种形状才是结构恒真。

    判据：把或位拆成备选（平铺列表的成员，或 `any_of` 的分支）；
    **每个备选都恰好只约束一个键（同名、且不写 scope）**，且各备选取值合起来
    覆盖该键的封闭值域 → 该规则对任何盘都成立（如 10 个 rizhu 穷尽天干、
    5 个 liuqin 穷尽六亲）。

    反例（**不得**判为恒真）：`{any_of:[{all_of:[{gan:甲},{canggan:甲}]}, …]}` ——
    每支同时约束两个键，取值是**成对**出现的，并不因为「合起来覆盖了值域」就恒真。
    """
    if isinstance(ap, list):
        alts = [[c] for c in ap if isinstance(c, dict)]
    elif isinstance(ap, dict) and "any_of" in ap:
        alts = [list(_iter_leaves(b)) for b in ap["any_of"]]
    else:
        alts = [[c] for c in leaves]
    keys = {c.get("key") for alt in alts for c in alt if not c.get("scope")}
    if len(keys) != 1:
        return []
    key = next(iter(keys))
    domain = values.get(key) or []
    if not domain:
        return []
    for alt in alts:
        if not alt or any(c.get("scope") or c.get("key") != key for c in alt):
            return []          # 有备选约束了别的键 → 成对/复合，不判恒真
    picked = {c.get("value") for alt in alts for c in alt}
    return [key] if picked >= set(domain) else []


def discrimination_report(art: str, cases: dict, values: dict[str, list[str]]) -> list[dict]:
    """找出在**每个样本盘面**都成立的规则 —— 零区分度的嫌疑犯。

    「枚举凑数」不只看取了多少个值，还要看它是否对任何盘都成立：
    `{key: liuqin, value: 父母}` 值域合法、只取一个值，但六爻每盘都有全部六亲，
    于是它对每一盘都为真——既没有筛选作用，又把 top-N 证据面板挤满。

    **证据分两档，不可混为一谈**：
    · `hard=True`（可据此动手）：表达式含通配 `*`，或其取值把某个**封闭值域**整段覆盖
      （如 10 个 rizhu 穷尽天干），**或**在「域完备键」上写了单个取值
      （如 ziwei_palace 的任一宫名：该键每盘都产出全部取值）——结构上恒真，与盘面无关。
    · `hard=False`（仅线索）：只是在当前 N 个样本上恰好都成立。样本只有 2 盘时
      「都成立」很常见，**不足以判定凑数**，要加样本再谈。
    """
    rules = load_rules(None, art)
    out: list[dict] = []
    for rule in rules:
        ap = rule.get("applicable_to")
        if not ap:
            continue
        results = [evaluate(rule, c["facts"]) for c in cases.values()]
        if not all(r["verdict"] == TRUE for r in results):
            continue
        leaves = list(_iter_leaves(ap if isinstance(ap, dict) else {"any_of": ap}))
        wildcard = any(p.get("value") == "*" for p in leaves)
        # 「单值 × 域完备键」这一档：此前只认通配与整段覆盖，**漏掉了这一类**
        # （t182 发现：ziwei_palace / bamen / sanchuan / liushen / sihua / jiuxing）。
        taut_clause = _or_position_taut(ap, DOMAIN_COMPLETE_KEYS.get(art, set()))
        sample_clause = None if taut_clause else _or_position_taut(ap, SAMPLE_COMPLETE_KEYS.get(art, set()))
        # 「整段覆盖某个封闭值域」只在这种形状下才等于结构恒真：
        # **或位的每个备选各自只约束同一个键**，且这些取值合起来覆盖该键的值域。
        # 旧版把覆盖判在整个表达式上，于是把「**成对**分支」也误判成恒真
        # （t188/t195 的枚举配对式：每支同时约束两个键，覆盖是成对出现的，并不恒真）。
        covering = _or_position_single_key_covering(ap, leaves, values)
        out.append(
            {
                "rule_id": rule.get("rule_id"),
                "book": rule.get("book"),
                "cases": len(results),
                "leaf_count": len(leaves),
                "wildcard": wildcard,
                "domain_covering": covering,
                "domain_complete_clause": taut_clause,
                "sample_complete_clause": sample_clause,
                "hard": bool(wildcard or covering or taut_clause),
                "statement": (rule.get("statement") or "")[:80],
            }
        )
    out.sort(key=lambda r: (not r["hard"], r["rule_id"] or ""))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="按盘面状态求规则结论（三态 + 置信度 + 出处）")
    ap.add_argument("--art", choices=ARTS + REFERENCE_ARTS)
    ap.add_argument("--book", help="system/slug；与 --art 二选一")
    ap.add_argument("--facts", default=str(ROOT / "tools/reports/facts-sample.json"))
    ap.add_argument("--case", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument(
        "--discrimination",
        action="store_true",
        help="列出在全部样本盘面都成立的规则（零区分度＝疑为枚举凑数）",
    )
    ap.add_argument(
        "--only",
        default=None,
        help="只输出这些结论：满足/不满足/信息不足（逗号分隔）",
    )
    args = ap.parse_args()

    if bool(args.art) == bool(args.book):
        ap.error("--art 与 --book 必须恰好给一个")

    art = args.art or art_of(*args.book.split("/", 1))
    if args.discrimination:
        raw = json.loads(Path(args.facts).read_text(encoding="utf-8"))
        if art not in raw:
            raise SystemExit(f"{args.facts}: 没有 art={art}")
        vocab = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
        flat = discrimination_report(art, raw[art], vocab.get("values") or {})
        hard = [r for r in flat if r["hard"]]
        if args.json:
            json.dump(
                {"art": art, "cases": len(raw[art]), "flat_rules": flat}, sys.stdout, ensure_ascii=False, indent=2
            )
            sys.stdout.write("\n")
            return 0
        print(
            f"art={art}：{len(raw[art])} 个样本盘面上都成立、零区分度的规则 {len(flat)} 条"
            f"（其中结构上恒真的 hard {len(hard)} 条）"
        )
        for r in flat:
            mark = "HARD" if r["hard"] else "soft"
            why = []
            if r["wildcard"]:
                why.append("通配 *")
            if r["domain_covering"]:
                why.append("整段覆盖 " + ",".join(r["domain_covering"]))
            print(f"  [{mark}] {r['rule_id']} ({r['book']}) {'; '.join(why) or '仅样本内都成立'} — {r['statement']}")
        return 0

    facts, case_name = load_chart(Path(args.facts), art, args.case)
    rules = load_rules(args.book, args.art)
    results = [evaluate(r, facts) for r in rules]
    if args.only:
        want = {s.strip() for s in args.only.split(",")}
        results = [r for r in results if r["verdict"] in want]

    if args.json:
        json.dump(
            {"art": art, "case": case_name, "fact_count": len(facts), "results": results},
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    from collections import Counter

    tally = Counter(r["verdict"] for r in results)
    print(f"art={art} case={case_name} 盘面事实 {len(facts)} 条，规则 {len(results)} 条")
    print("  " + "  ".join(f"{k}={tally.get(k, 0)}" for k in (TRUE, FALSE, UNKNOWN)))
    if args.verbose:
        for r in results:
            if r["verdict"] == UNKNOWN and r.get("reason"):
                print(f"\n[{r['verdict']}] {r['rule_id']} ({r['book']}) — {r['reason']}")
                continue
            m = ", ".join(f"{x['key']}={x['value']}" for x in r["matched"]) or "-"
            print(
                f"\n[{r['verdict']}] {r['rule_id']} ({r['book']}) "
                f"conf={r['confidence']} 覆盖={r['fact_coverage']} 命中: {m}"
            )
            if r["missing_fact_keys"]:
                print(f"    缺事实: {', '.join(r['missing_fact_keys'])}")
            src = r.get("source") or {}
            a = src.get("anchor") or {}
            print(f"    出处: {a.get('file')} L{a.get('start_line')}-L{a.get('end_line')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
