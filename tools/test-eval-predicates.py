#!/usr/bin/env python3
"""tools/eval-predicates.py 的语义测试：三态、AND/OR/嵌套/排除、同位置绑定、置信度、出处。

不读真实规则库、不写任何文件：全部用合成盘面与合成规则，直接调模块里的求值函数。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "tools/eval-predicates.py"


def load_module():
    spec = importlib.util.spec_from_file_location("eval_predicates", MOD_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


M = load_module()
FAILED: list[str] = []


def fact(key, value, **scope):
    return {"key": key, "value": value, "scope": scope, "derivedFrom": ["test"]}


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}: {got!r}")


def rule(applicable_to, **kw):
    base = {
        "rule_id": "T-01",
        "book": "test/book",
        "title": "测试书",
        "applicable_to": applicable_to,
        "quote": "原文逐字摘录",
        "statement": "陈述",
        "verified": False,
        "anchor": {"file": "sources/fulltext/test/book/fulltext.md", "start_line": 3, "end_line": 4},
    }
    base.update(kw)
    return base


def main() -> int:
    print("1. 旧形平铺列表＝OR（语义与 v2 一致，不许变）")
    two = [{"key": "bamen", "value": "休门"}, {"key": "bashen", "value": "九天"}]
    check("  只有第二支命中 → 满足", M.evaluate(rule(two), [fact("bashen", "九天")])["verdict"], "满足")
    check("  两支都不命中 → 不满足", M.evaluate(rule(two), [fact("bamen", "开门"), fact("bashen", "太阴")])["verdict"], "不满足")
    check(
        "  引用的 key 整个缺席 → 信息不足（不许降级成「不满足」）",
        M.evaluate(rule(two), [fact("bashen", "太阴")])["verdict"],
        "信息不足",
    )

    print("2. all_of＝AND（旧语言表达不了的那个缺口）")
    both = {"all_of": [{"key": "bamen", "value": "休门"}, {"key": "bashen", "value": "九天"}]}
    # 两个 key 都在盘上，但只有一支命中：旧形 OR 会判「满足」，all_of 必须判「不满足」。
    partial = [fact("bamen", "开门"), fact("bashen", "九天")]
    check(
        "  只命中一支 → 不满足（旧形这里会误判为满足）",
        M.evaluate(rule(both), partial)["verdict"],
        "不满足",
    )
    check(
        "  同一盘面用旧形 OR → 满足（对照，证明差别来自语言而非数据）",
        M.evaluate(rule(list(both["all_of"])), partial)["verdict"],
        "满足",
    )
    check(
        "  两支都命中 → 满足",
        M.evaluate(rule(both), [fact("bamen", "休门"), fact("bashen", "九天")])["verdict"],
        "满足",
    )
    # key 整个缺席 → 无法证明不成立，只能是「信息不足」，不许降级成「不满足」。
    check(
        "  其中一支的 key 整个缺席 → 信息不足",
        M.evaluate(rule(both), [fact("bashen", "九天")])["verdict"],
        "信息不足",
    )

    print("3. 信息不足：key 在本盘完全不存在，不是「不满足」")
    missing = {"all_of": [{"key": "bamen", "value": "休门"}, {"key": "keti", "value": "元首课"}]}
    r = M.evaluate(rule(missing), [fact("bamen", "休门")])
    check("  → 信息不足", r["verdict"], "信息不足")
    check("  缺事实被点名", r["missing_fact_keys"], ["keti"])

    check(
        "  显式信息不足事实不能降级为不满足",
        M.evaluate(
            rule([{"key": "suiyun_binglin", "value": "是", "scope": {"layer": "流年"}}]),
            [fact("suiyun_binglin", "信息不足", layer="流年", year=2100)],
        )["verdict"],
        "信息不足",
    )
    check(
        "  流年关系分类的信息不足不能降级为不满足",
        M.evaluate(
            rule([{"key": "dayun_liunian_relation_class", "value": "相冲", "scope": {"layer": "流年"}}]),
            [fact("dayun_liunian_relation_class", "信息不足", layer="流年", year=2100)],
        )["verdict"],
        "信息不足",
    )
    same_zhi = rule([{"key": "suiyun_same_zhi", "value": "是", "scope": {"layer": "流年", "year": 2100}}])
    unresolved = M.evaluate(same_zhi, [fact("suiyun_same_zhi", "信息不足", layer="流年", year=2100)])
    check("  同支事实显式未知 → 信息不足", unresolved["verdict"], "信息不足")
    check("  同支未知事实点名缺键", unresolved["missing_fact_keys"], ["suiyun_same_zhi"])
    check("  同支明确为是 → 满足", M.evaluate(same_zhi, [fact("suiyun_same_zhi", "是", layer="流年", year=2100)])["verdict"], "满足")
    check("  同支明确为否 → 不满足", M.evaluate(same_zhi, [fact("suiyun_same_zhi", "否", layer="流年", year=2100)])["verdict"], "不满足")

    print("4. any_of 嵌套 all_of（OR-of-AND）")
    nested = {
        "any_of": [
            {"all_of": [{"key": "bamen", "value": "休门"}, {"key": "bashen", "value": "九天"}]},
            {"all_of": [{"key": "bamen", "value": "杜门"}, {"key": "bashen", "value": "九地"}]},
        ]
    }
    check(
        "  第二支整组成立 → 满足",
        M.evaluate(rule(nested), [fact("bamen", "杜门"), fact("bashen", "九地")])["verdict"],
        "满足",
    )
    check(
        "  两支各只中一半 → 不满足",
        M.evaluate(rule(nested), [fact("bamen", "休门"), fact("bashen", "九地")])["verdict"],
        "不满足",
    )

    print("5. none_of＝排除；缺 key 不得算「满足」")
    excl = {"any_of": [{"key": "bamen", "value": "休门"}], "none_of": [{"key": "kongwang", "value": "*"}]}
    check(
        "  排除项 key 缺失 → 信息不足（无法证明「没有」）",
        M.evaluate(rule(excl), [fact("bamen", "休门")])["verdict"],
        "信息不足",
    )
    # 指名排除：盘上有 kongwang，但取值不是被排除的那个 → 满足
    named = {"any_of": [{"key": "bamen", "value": "休门"}], "none_of": [{"key": "kongwang", "value": "子"}]}
    check(
        "  排除项 key 在盘上且不命中 → 满足",
        M.evaluate(rule(named), [fact("bamen", "休门"), fact("kongwang", "丑")])["verdict"],
        "满足",
    )
    check(
        "  排除项命中（指名）→ 不满足",
        M.evaluate(rule(named), [fact("bamen", "休门"), fact("kongwang", "子")])["verdict"],
        "不满足",
    )
    check(
        "  排除项命中（通配）→ 不满足",
        M.evaluate(rule(excl), [fact("bamen", "休门"), fact("kongwang", "子")])["verdict"],
        "不满足",
    )

    print("6. same＝同位置绑定（同宫／同柱／同爻）")
    same = {
        "all_of": [
            {"key": "ziwei_star", "value": "禄存"},
            {"key": "ziwei_star", "value": "天马"},
        ],
        "same": "palace",
    }
    check(
        "  两星不同宫 → 不满足",
        M.evaluate(rule(same), [fact("ziwei_star", "禄存", palace="命宫"), fact("ziwei_star", "天马", palace="财帛")])[
            "verdict"
        ],
        "不满足",
    )
    check(
        "  两星同宫 → 满足",
        M.evaluate(rule(same), [fact("ziwei_star", "禄存", palace="命宫"), fact("ziwei_star", "天马", palace="命宫")])[
            "verdict"
        ],
        "满足",
    )

    print("7. scope 位置限定真的生效")
    pos = {"all_of": [{"key": "bamen", "value": "休门", "scope": {"gong": 9}}]}
    check("  宫位不符 → 不满足", M.evaluate(rule(pos), [fact("bamen", "休门", gong=1)])["verdict"], "不满足")
    check("  宫位相符 → 满足", M.evaluate(rule(pos), [fact("bamen", "休门", gong=9)])["verdict"], "满足")

    print("7b. 密集四柱事实缺单柱位不等于该柱位条件为假")
    year_wu = {"all_of": [{"key": "gan", "value": "戊", "scope": {"layer": "本命", "pillar": "year"}}]}
    missing_year = [fact("gan", "丙", layer="本命", pillar="month"), fact("gan", "丙", layer="本命", pillar="time")]
    r = M.evaluate(rule(year_wu), missing_year)
    check("  只有月时干、缺年干 → 信息不足", r["verdict"], "信息不足")
    check("  缺柱位仍点名 gan", r["missing_fact_keys"], ["gan"])
    check("  年干已知非戊 → 不满足", M.evaluate(rule(year_wu), missing_year + [fact("gan", "辛", layer="本命", pillar="year")])["verdict"], "不满足")
    check("  年干戊 → 满足", M.evaluate(rule(year_wu), missing_year + [fact("gan", "戊", layer="本命", pillar="year")])["verdict"], "满足")
    sparse = {"all_of": [{"key": "shensha", "value": "羊刃", "scope": {"layer": "本命", "pillar": "year"}}]}
    check("  神煞是稀疏标签，另柱有值而年柱未见 → 不满足", M.evaluate(rule(sparse), [fact("shensha", "羊刃", layer="本命", pillar="time")])["verdict"], "不满足")

    print("7c. 六壬按 scope.ruleId 判定取传；同 key 别条在场不填本条缺项")
    selection = {"key": "liuren_selection_rule_status", "value": "adopted", "scope": {"layer": "本命", "ruleId": "DLD-E-04"}}
    inner = fact("liuren_selection_rule_status", "adopted", layer="本命", ruleId="DLD-E-06")
    check("  未指定 ruleId 禁止任意匹配", M.evaluate(rule([{"key": "liuren_selection_rule_status", "value": "adopted"}]), [inner])["verdict"], "信息不足")
    check("  返吟外层缺项、比用内层仍在 → 信息不足", M.evaluate(rule([selection]), [inner])["verdict"], "信息不足")
    negative = fact("liuren_selection_rule_status", "not_adopted", layer="本命", ruleId="DLD-E-04")
    check("  外层明确未采用 → 不满足", M.evaluate(rule([selection]), [inner, negative])["verdict"], "不满足")
    positive = fact("liuren_selection_rule_status", "adopted", layer="本命", ruleId="DLD-E-04")
    check("  外层采用 → 满足", M.evaluate(rule([selection]), [inner, positive])["verdict"], "满足")
    check("  外层两状态矛盾 → 信息不足", M.evaluate(rule([selection]), [inner, negative, positive])["verdict"], "信息不足")

    print("8. 置信度＝输入完备度（机械口径，不是预测准确率）")
    r = M.evaluate(rule({"any_of": [{"key": "bamen", "value": "休门"}]}), [fact("bamen", "休门")])
    check("  key 齐全无通配 → 1.0", r["confidence"], 1.0)
    r = M.evaluate(
        rule({"all_of": [{"key": "bamen", "value": "休门"}, {"key": "keti", "value": "元首课"}]}),
        [fact("bamen", "休门")],
    )
    check("  引用 2 key 只有 1 个到手 → 0.5", r["confidence"], 0.5)
    r = M.evaluate(rule({"any_of": [{"key": "kongwang", "value": "*"}]}), [fact("kongwang", "子")])
    check("  用通配 → 打 0.2 折 = 0.8", r["confidence"], 0.8)

    print("9. 出处可溯源，且不冒充已核验")
    r = M.evaluate(rule({"any_of": [{"key": "bamen", "value": "休门"}]}), [fact("bamen", "休门")])
    src = r["source"]
    check("  quote 原样带出", src["quote"], "原文逐字摘录")
    check("  anchor 行范围带出", (src["anchor"]["start_line"], src["anchor"]["end_line"]), (3, 4))
    check("  verification 为 provisional", src["verification"], "provisional")
    check("  verified 恒 false", r["verified"], False)

    print("9b. matched 只在「满足」时给见证集")
    r = M.evaluate(
        rule({"all_of": [{"key": "bamen", "value": "休门"}, {"key": "bashen", "value": "九天"}]}),
        [fact("bamen", "休门"), fact("bashen", "太阴")],
    )
    check("  all_of 不满足时 matched 为空（不许把子句命中当整条成立）", (r["verdict"], r["matched"]), ("不满足", []))
    r = M.evaluate(rule(both), [fact("bamen", "休门"), fact("bashen", "九天")])
    check("  满足时给出见证集", (r["verdict"], len(r["matched"])), ("满足", 2))
    r = M.evaluate(rule({"any_of": [{"key": "bamen", "value": "休门"}]}), [fact("bashen", "九天")])
    check("  信息不足时 matched 也为空", (r["verdict"], r["matched"]), ("信息不足", []))

    print("10. 空 applicable_to 不猜结论")
    r = M.evaluate(rule([]), [fact("bamen", "休门")])
    check("  → 信息不足", r["verdict"], "信息不足")
    check("  置信度 0", r["confidence"], 0.0)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL EVAL SEMANTICS OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
