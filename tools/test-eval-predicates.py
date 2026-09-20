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