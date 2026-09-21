#!/usr/bin/env python3
"""把 **executable 层**（schema `fateradar-executable-v2`）当工具调用：
入参盘面状态，返回结论 + 置信度 + 出处。

为什么需要它：`references/executable/*.json` 的 258 条记录各自带
`satisfy_when` / `fail_when` / `unknown_when` 三态，而 `when` 是**机器可读**的
（实测 258 条里只有 11 条是纯 `{definition: …}` 命名定义）。但此前**古籍仓没有任何东西
去求值 `when`**——`validate-executable.py` 只校验字段与引文。本脚本补这一段。

产物里规则的 `applicable_to`（谓词）与本层的 `when` 是**两套独立声明**：
前者按 `FactKey` 词表写，后者按**字段路径**写（`day.gan` / `ke.style` / `skyStemIn`…）。
`FIELD_MAP` 就是这两套之间的对照表，每条都写明依据（接哪个 FactKey、带什么 scope）。

三态口径（与 `docs/PREDICATE-LANGUAGE-V3.md` 一致，缺输入≠不满足）：

- `满足`：`when` 为真。
- `不满足`：`when` 为假，**且**所引用的字段都能在本盘判定。
- `信息不足`：某字段**没有对应 FactKey**（声明了引擎不产出的事实），或对应 key
  在本盘完全不存在 —— 无从判定，不得降级成「不满足」。
- `未提供定义表`：`when` 是 `{definition: X}` / `{scope, definition}` / `{interference.id: …}`
  这类**命名定义**。没有定义表就无法求值；单列一类，不伪装成任何三态。

两条口径要写清，否则容易被误读：

1. **`exists` 在字段对应的 key 整个缺席时给「信息不足」，不给「不满足」。**
   事实袋里没有这个 key，无法区分「本盘不成立」与「引擎没产出」——
   后者正是 executable 层 `named_gaps` 关心的「未知分支必须成立」。
   （key 在场时 `exists` 只看存在性、不看取值，故恒为满足。）
2. **「不满足」只出现在「引用的字段都能在本盘判定、且条件为假」时。**
   因此 `equals`/`in`/简写要产出「不满足」，前提是 key 在场而取值不符；
   91 条 `exists` 子句不会单独产出「不满足」。这是有意的：
   **宁可报信息不足，也不把「引擎没产出」算成「原文条件不成立」。**

`置信度` 仍是**输入完备度**（引用字段中能接到 FactKey 且本盘存在的比例），
**不是预测准确率**。`verified` 一律由 JSON 原值带出（当前全库为 `false`）。

本脚本**只读**：不改 executable JSON、不改 rules.yaml、不写锚点。
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRUE, FALSE, UNKNOWN, UNDEF = "满足", "不满足", "信息不足", "未提供定义表"

# ── 字段路径 → FactKey 对照 ─────────────────────────────────────────────────
# value = (FactKey, scope 约束, 依据)。scope 为 None 表示不限。
# 只写**能从 fact-vocab 与引擎产出（ART_EMIT_KEYS）确认**的对照；
# 接不上的一律留空并如实报「信息不足」，不用近似名去凑。
FIELD_MAP: dict[str, tuple[str, dict | None, str]] = {
    # 四柱：与 t170 新增的逐柱 gan/zhi 一一对应
    "day.gan": ("gan", {"pillar": "day"}, "日柱天干；t170 起逐柱产出"),
    "day.gan.element": (None, None, "日干五行不是 FactKey（yongshen 是用神五行，非日干五行）"),
    "day.zhi": ("zhi", {"pillar": "day"}, "日柱地支；t170 起逐柱产出"),
    "month.gan": ("gan", {"pillar": "month"}, "月柱天干"),
    "month.zhi": ("zhi", {"pillar": "month"}, "月柱地支（＝月令 yueling 的新取法）"),
    "year.gan": ("gan", {"pillar": "year"}, "年柱天干"),
    "year.zhi": ("zhi", {"pillar": "year"}, "年柱地支"),
    "time.gan": ("gan", {"pillar": "time"}, "时柱天干"),
    "pillars.gan": ("gan", None, "四柱天干（任一柱）"),
    "pillars.zhi": ("zhi", None, "四柱地支（任一柱）"),
    # 格局／十神
    "geju.name": ("geju", None, "格局名；引擎产出 geju"),
    "geju.tenGod": ("shishen", None, "十神；引擎产出 shishen"),
    # 六壬
    "three.chuan": ("sanchuan", None, "三传；引擎产出 sanchuan"),
    "ke.style": ("keti", None, "课体；引擎产出 keti（样本实测有「伏吟课」等）"),
    # 奇门：t171 新增的天地盘干
    "sky.stem": ("tianpan_gan", None, "天盘干；t171 起逐宫产出"),
    "sky.stem+palace": ("tianpan_gan", None, "天盘干落宫（skyStemIn 判据所本）"),
    "earth.stem": ("dipan_gan", None, "地盘干；t171 起逐宫产出"),
    # 七政
    "star.palace": ("xingyao", None, "某曜所落宫位：xingyao 事实自带 scope.palace"),
    "sun.palace": ("xingyao", {"value": "太阳"}, "太阳所落宫位"),
    # 接不上的（如实登记，不凑近似名）
    # t173 起 zhifu / zhishi 事实带上 scope.gong（值符星落宫 / 值使门落宫，
    # 取自引擎已有的 layout.starPalace / layout.doorPalace）。
    "zhifu.palace": ("zhifu", None, "值符所落之宫：t173 起 zhifu 事实带 scope.gong"),
    "timedry.palace": ("zhishi", None, "值使所落之宫：t173 起 zhishi 事实带 scope.gong"),
    # t205 更新：旧注说「引擎产出的是逐爻分名」——那就照分名接。
    # 「positions 在场」＝**本盘产出了逐爻事实**，任何六爻盘都成立（六个爻位总在）。
    # 用 `yao_zhi`（逐爻纳甲支，逐爻必有）作在场代理；`.activity`／`.moving` 各接真身。
    "positions": ("yao_zhi", None, "六爻位置总名 → 逐爻在场（yao_zhi 逐爻必有）；见 positions.main.* 各项"),
    "positions.main.activity": ("liuyao_activity", None, "逐爻活动状态；t193 起产出"),
    "positions.main.moving": ("dongyao", None, "动爻；引擎产出 dongyao（无动爻时本键缺席，故不作在场代理）"),
    # t205 更新：这两项引擎**早就算过**（`selection.courses` 与 `selection.shehaiMethod`），
    # 此前只进解读文本。现在产成事实，记录里的子句才判得出来。
    "ascendant.sign": ("qizheng_ascendant", None, "上升点所在宫；t205 起产出（引擎按 Math.floor(asc/30)%12 取）"),
    "four.ke": ("liuren_ke", None, "四课各课上神；t205 起产出（与 sanchuan 同形）"),
    "shehai.method": ("liuren_shehai", None, "涉害取法；t205 起产出，沿用引擎原值 depth／mengzhong"),
    "yongshen.zhi": (None, None, "用神地支：引擎只产出用神五行 yongshen"),
    "yongshen.state": (None, None, "用神旺衰状态：引擎未产出"),
    "stars": (None, None, "星曜集合总名：未产出（分名是 xingyao）"),
    "star.name": ("xingyao", None, "星曜名；引擎产出 xingyao"),
    "star.dignity": ("miaowang", None, "庙旺；引擎产出 miaowang"),
    "sun.mansion": ("xiudu", None, "太阳所躔宿度；引擎产出 xiudu"),
    "moon.mansion": ("xiudu", None, "太阴所躔宿度"),
    "moon.palace": ("xingyao", {"value": "太阴"}, "太阴所落宫位"),
    "meihua.ti.element": (None, None, "梅花体卦五行：本仓无 meihua 引擎事实"),
    "meihua.yong.element": (None, None, "梅花用卦五行：同上"),
    "meihua.role": (None, None, "梅花体用角色：同上"),
    "liuyao.structure": (None, None, "六爻卦体结构：引擎未产出"),
    "interference.id": (None, None, "干扰项命名表：无注册表"),
    "xiaoliuren.palace.hour": (None, None, "小六壬时宫：本仓事实层未产出（产品词表有此键，古籍仓词表无）"),
}
# 前缀映射：`tenGodFacts.<十神>.<层/性>` 这类带变量的名字
PREFIX_MAP: list[tuple[str, str, dict | None, str]] = [
    ("tenGodFacts.", "shishen", None, "十神事实（名字里带十神与层/性；按 shishen 求值）"),
]


def lookup_field(name: str) -> tuple[str | None, dict | None, str]:
    if name in FIELD_MAP:
        return FIELD_MAP[name]
    for prefix, key, scope, basis in PREFIX_MAP:
        if name.startswith(prefix):
            return key, scope, basis
    return None, None, "无对照（未登记）"


def facts_present(facts: list[dict]) -> set[str]:
    return {f.get("key") for f in facts if isinstance(f, dict)}


def _match(facts: list[dict], key: str, want, scope: dict | None) -> bool:
    for f in facts:
        if f.get("key") != key:
            continue
        if scope:
            # 按 scope 字段逐个比：早年只支持 pillar/value，t183 因紫微格局定义需要
            # （`{ziwei_star: 紫微, scope: {palace: 命宫}}`）泛化为任意字段同名匹配。
            fscope = f.get("scope") or {}
            if any(fscope.get(k) != v for k, v in scope.items()):
                continue
        if want is None:
            return True
        if isinstance(want, (list, tuple, set)):
            if f.get("value") in want:
                return True
        elif f.get("value") == want:
            return True
    return False


def eval_field(name: str, want, facts: list[dict], present: set[str]) -> tuple[str, str, str | None, dict | None]:
    """返回 (状态, 依据说明, FactKey|None, scope|None)。"""
    key, scope, basis = lookup_field(name)
    if key is None:
        return UNKNOWN, basis, None, None
    if key not in present:
        return UNKNOWN, f"{basis}（本盘无 {key} 事实）", key, scope
    ok = _match(facts, key, want, scope)
    return (TRUE if ok else FALSE), basis, key, scope


DEFINITIONS_DIR = ROOT / "references/definitions"


def load_definitions() -> tuple[dict[str, dict], dict[str, dict]]:
    """读取有据定义表：返回 (可展开的定义, 已查明「无定义」的条目)。

    定义一律来自原文（表内每条都带锚点行与逐字引文），本函数不做任何补写。
    """
    defined: dict[str, dict] = {}
    undefined: dict[str, dict] = {}
    for f in sorted(DEFINITIONS_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for e in d.get("entries") or []:
            defined[e["name"]] = {**e, "_file": f.name}
        for e in d.get("not_defined") or []:
            undefined[e["name"]] = {**e, "_file": f.name}
    return defined, undefined


DEFINED, UNDEFINED = load_definitions()


def eval_definition(name: str, facts: list[dict], present: set[str]) -> tuple[str, list[str]]:
    """按定义表求值一个命名定义。三态语义与其它子句一致。"""
    e = DEFINED.get(name)
    if e is None:
        u = UNDEFINED.get(name)
        if u is not None:
            ev = (u.get("evidence") or [{}])[0]
            where = f"（{ev.get('file','')} L{ev.get('line','')}）" if ev else ""
            return UNDEF, [
                f"命名定义「{name}」在语料里**没有构成定义**：{u.get('status')}{where}；"
                f"{u.get('note','')[:80]}"
            ]
        return UNDEF, [f"命名定义「{name}」无定义表"]
    src = e.get("source") or {}
    where = f"{src.get('file','')} L{src.get('line','')}"
    expansion = e.get("expansion")
    if not expansion:
        return UNKNOWN, [
            f"命名定义「{name}」**已据原文登记**（{where}：{src.get('quote','')[:48]}），"
            f"但展开所需事实尚未产出：{'／'.join(e.get('needs') or ['（未列）'])}"
        ]
    # ⚠ t208 修：原实现只读 `expansion["all_of"]`，于是**或形（any_of）定义会被当成空合取
    # → 恒真**。日出扶桑（「日在卯守命是也，守官祿宮亦然」）就是或形，曾对每张盘都报「满足」。
    # 现在：合取／析取各自求值；**未知形态一律 UNKNOWN，绝不默认 TRUE**。
    def _clause_status(cls: dict) -> str:
        """单句：ok／missing（缺键）／bad（不成立）。"""
        if cls.get("key") not in present:
            return "missing"
        return "ok" if _match(facts, cls["key"], cls.get("value"), cls.get("scope")) else "bad"

    if "all_of" in expansion:
        clauses = expansion["all_of"] or []
        missing = [c for c in clauses if _clause_status(c) == "missing"]
        if missing:
            return UNKNOWN, [f"命名定义「{name}」按 {where} 展开，但本盘缺事实 {sorted({c['key'] for c in missing})}"]
        bad = [c for c in clauses if _clause_status(c) == "bad"]
        if bad:
            return FALSE, [f"命名定义「{name}」按 {where} 展开：{'、'.join(f'{c.get(chr(107)+chr(101)+chr(121))}={c.get(chr(118)+chr(97)+chr(108)+chr(117)+chr(101))}' for c in bad)} 未同时成立"]
        return TRUE, [f"命名定义「{name}」按 {where} 展开且成立"]

    if "any_of" in expansion:
        branches = expansion["any_of"] or []
        statuses = [[_clause_status(c) for c in (b.get("all_of") or [])] for b in branches]
        if any(st and all(s == "ok" for s in st) for st in statuses):
            return TRUE, [f"命名定义「{name}」按 {where} 展开：有一支成立"]
        if any("missing" in st for st in statuses):
            return UNKNOWN, [f"命名定义「{name}」按 {where} 展开为或形，但仍有分支缺事实，无法排除"]
        return FALSE, [f"命名定义「{name}」按 {where} 展开为或形，各支均不成立"]

    return UNKNOWN, [
        f"命名定义「{name}」的展开形态（{sorted(expansion)}）求值器不认识——"
        "**按未知处理，不得默认成立**"
    ]


def eval_when(when, facts: list[dict], present: set[str]) -> tuple[str, list[str]]:
    """求值 `when`，返回 (三态, 依据行)。"""
    notes: list[str] = []
    if not isinstance(when, dict):
        return UNDEF, ["when 不是 mapping"]

    # 命名定义类：没有定义表就无法求值
    if "definition" in when:
        # t183：不再一律报「无定义表」——有据定义表里能查到就按原文展开求值；
        # 语料里确实没有构成定义的，报「没有」并附检索证据；有定义但缺事实的，报缺什么。
        return eval_definition(when["definition"], facts, present)
    if "interference.id" in when:
        return UNDEF, ["干扰项命名表无注册表"]

    if "all" in when:
        states = [eval_when(c, facts, present) for c in when["all"]]
        notes = [n for _, ns in states for n in ns]
        if any(s == FALSE for s, _ in states):
            return FALSE, notes
        if any(s in (UNKNOWN, UNDEF) for s, _ in states):
            return UNKNOWN, notes
        return TRUE, notes

    if "any" in when:
        states = [eval_when(c, facts, present) for c in when["any"]]
        notes = [n for _, ns in states for n in ns]
        if any(s == TRUE for s, _ in states):
            return TRUE, notes
        if any(s in (UNKNOWN, UNDEF) for s, _ in states):
            return UNKNOWN, notes
        return FALSE, notes

    if "exists" in when:
        st, basis, _, _ = eval_field(str(when["exists"]), None, facts, present)
        return st, [f"exists {when['exists']}：{basis}"]

    if "equals" in when and isinstance(when["equals"], dict):
        states = []
        for field, want in when["equals"].items():
            st, basis, _, _ = eval_field(field, want, facts, present)
            notes.append(f"{field}={want}：{basis}")
            states.append(st)
        if any(s == FALSE for s in states):
            return FALSE, notes
        if any(s == UNKNOWN for s in states):
            return UNKNOWN, notes
        return TRUE, notes

    if "in" in when and isinstance(when["in"], dict):
        states = []
        for field, want in when["in"].items():
            st, basis, _, _ = eval_field(field, want, facts, present)
            notes.append(f"{field}∈{want}：{basis}")
            states.append(st)
        if any(s == FALSE for s in states):
            return FALSE, notes
        if any(s == UNKNOWN for s in states):
            return UNKNOWN, notes
        return TRUE, notes

    if "skyStemIn" in when:
        st, basis, _, _ = eval_field("sky.stem+palace", when["skyStemIn"], facts, present)
        return st, [f"skyStemIn {when['skyStemIn']}：{basis}"]

    # 简写：{字段名: [允许值…]}（AND）
    shorthand = {k: v for k, v in when.items() if k not in ("scope", "locationBasis")}
    if shorthand:
        states = []
        for field, want in shorthand.items():
            st, basis, _, _ = eval_field(field, want, facts, present)
            notes.append(f"{field}∈{want}：{basis}")
            states.append(st)
        if any(s == FALSE for s in states):
            return FALSE, notes
        if any(s == UNKNOWN for s in states):
            return UNKNOWN, notes
        return TRUE, notes

    return UNDEF, ["when 形态未识别"]


def referenced_fields(when) -> set[str]:
    out: set[str] = set()
    if isinstance(when, dict):
        for k, v in when.items():
            if k in ("all", "any", "none"):
                for c in v or []:
                    out |= referenced_fields(c)
            elif k == "exists":
                out.add(str(v))
            elif k in ("equals", "in") and isinstance(v, dict):
                out |= set(v)
            elif k == "skyStemIn":
                out.add("sky.stem+palace")
            elif k in ("definition", "scope", "locationBasis", "interference.id"):
                continue
            else:
                out.add(k)
    return out


def evaluate_record(rule: dict, facts: list[dict]) -> dict:
    when = rule.get("when")
    present = facts_present(facts)
    verdict, notes = eval_when(when, facts, present)
    fields = referenced_fields(when)
    mapped = {f for f in fields if lookup_field(f)[0] is not None}
    resolvable = {f for f in mapped if lookup_field(f)[0] in present}
    confidence = (len(resolvable) / len(fields)) if fields else 0.0
    return {
        "id": rule.get("id"),
        "art": rule.get("art"),
        "theme": rule.get("theme"),
        "verdict": verdict,
        "confidence": round(confidence, 3),
        "fields": sorted(fields),
        "unmapped_fields": sorted(f for f in fields if lookup_field(f)[0] is None),
        "rescue": rule.get("rescue"),
        "rescue_unimplemented": rule.get("rescue") == "unimplemented",
        "has_named_gaps": bool(rule.get("named_gaps")),
        "verified": rule.get("verified"),
        "implementation_assumption": rule.get("implementation_assumption"),
        "notes": notes[:4],
        # 出处：段落 ID + 逐字引文（电子文本溯源，不是影印核验）
        "source": {
            "paragraph_ids": rule.get("paragraph_ids"),
            "page": rule.get("page"),
            "quote": rule.get("quote"),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="executable 层求值：盘面状态 → 三态 + 置信度 + 出处")
    ap.add_argument("--package", help="references/executable/<file>.json")
    ap.add_argument("--all", action="store_true", help="全部 15 包")
    ap.add_argument("--facts", default=str(ROOT / "tools/reports/facts-sample.json"))
    ap.add_argument("--case", default=None, help="facts-sample 里的 case（默认该 art 首个）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    files = (
        sorted(glob.glob(str(ROOT / "references/executable/*.json")))
        if args.all or not args.package
        else [str(ROOT / args.package)]
    )
    sample = json.loads(Path(args.facts).read_text(encoding="utf-8"))

    results: list[dict] = []
    for fp in files:
        pkg = json.loads(Path(fp).read_text(encoding="utf-8"))
        for rule in pkg.get("rules") or []:
            art = rule.get("art")
            if art not in sample:
                results.append(
                    {
                        "id": rule.get("id"),
                        "art": art,
                        "theme": rule.get("theme"),
                        "verdict": UNKNOWN,
                        "confidence": 0.0,
                        "fields": sorted(referenced_fields(rule.get("when"))),
                        "unmapped_fields": [],
                        "rescue": rule.get("rescue"),
                        "rescue_unimplemented": rule.get("rescue") == "unimplemented",
                        "has_named_gaps": bool(rule.get("named_gaps")),
                        "verified": rule.get("verified"),
                        "implementation_assumption": rule.get("implementation_assumption"),
                        "notes": [f"本仓 facts-sample 无 art={art} 的盘面（无引擎事实）"],
                        "source": {},
                    }
                )
                continue
            cases = sample[art]
            case = args.case if args.case in cases else sorted(cases)[0]
            results.append(evaluate_record(rule, cases[case]["facts"]))

    tally = Counter(r["verdict"] for r in results)
    if args.json:
        json.dump(
            {
                "packages": len(files),
                "records": len(results),
                "tally": dict(tally),
                "results": results,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    print(f"executable 记录 {len(results)} 条（{len(files)} 包）")
    print("  " + "  ".join(f"{k}={tally.get(k, 0)}" for k in (TRUE, FALSE, UNKNOWN, UNDEF)))
    print(f"  rescue=unimplemented {sum(1 for r in results if r['rescue_unimplemented'])} 条；"
          f"带 named_gaps {sum(1 for r in results if r['has_named_gaps'])} 条；"
          f"verified=true {sum(1 for r in results if r['verified'] is True)} 条")
    unmapped = Counter(f for r in results for f in r["unmapped_fields"])
    if unmapped:
        print("\n接不上 FactKey 的字段（这些记录的对应子句只能是信息不足）：")
        for k, v in unmapped.most_common():
            print(f"  {v:4} {k}")
    if args.verbose:
        for r in results:
            print(f"\n[{r['verdict']}] {r['id']} ({r['art']}) conf={r['confidence']} rescue={r['rescue']}")
            for n in r["notes"]:
                print(f"    {n}")
            src = r.get("source") or {}
            if src.get("paragraph_ids"):
                print(f"    出处: {', '.join(src['paragraph_ids'][:3])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())