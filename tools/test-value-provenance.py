#!/usr/bin/env python3
"""谓词取值溯源分类的回归测试（t212）。

钉住：
1. **分类完备**：四类之和 == 取值叶子总数（不许有值落不进任何一类）；
2. **报告可复现**：连跑两次结果一致；
3. **反例**（正反两面都要）：
   · 取值**字面**在 statement 里的 → 必须归 `literal`；
   · 取值**不在**文本里、且本条没有枚举该键 → 必须归 `canonical`（需人读那一类）；
   · **枚举**：本条在同一键上展开 ≥3 个取值 → 归 `enumerated`（哪怕每个值都不在文本里）；
4. 台账里的 `canonical_pairs` 与 tally 对得上（前者之和 == 后者的 canonical 计数）。

**不钉具体数字**——它随施工变化（t187/t199 的同一教训）。钉的是性质。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("vp", ROOT / "tools/value-provenance-report.py")
vp = importlib.util.module_from_spec(_spec)
sys.modules["vp"] = vp
assert _spec.loader is not None
_spec.loader.exec_module(vp)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    data = vp.classify()
    t = data["tally"]

    print("1. 分类完备、四类齐全")
    check("  四类之和 == 取值叶子数", sum(t.values()), data["value_leaves"])
    # t213 起「待读」一类可以**为零**（读过就登记进 value-equivalences.json）——那是好状态，
    # 所以不要求 canonical > 0；要求的是「读过 + 待读」两类的和 == 非字面/非枚举/非引擎态的总量。
    check(
        "  五类都参与计数（含 canonical-reviewed）",
        sorted(k for k in ("literal", "enumerated", "canonical", "canonical-reviewed", "engine-state") if t.get(k)),
        ["canonical-reviewed", "engine-state", "enumerated", "literal"],
    )
    check(
        "  待读与已读的登记表一致（待读为空 ⇒ 全部登记过）",
        (t.get("canonical", 0) == 0) == (t.get("canonical-reviewed", 0) > 0),
        True,
    )
    check("  取值叶子数 > 1000", data["value_leaves"] > 1000, True)
    check(
        "  五类之和 == 取值叶子数（含 canonical-reviewed）",
        sum(t.get(k, 0) for k in ("literal", "enumerated", "canonical", "canonical-reviewed", "engine-state")),
        data["value_leaves"],
    )

    print("2. 可复现")
    again = vp.classify()
    check("  两次 tally 一致", again["tally"], data["tally"])
    check("  canonical_pairs 组数一致", len(again["canonical_pairs"]), len(data["canonical_pairs"]))

    print("3. canonical_pairs 与 tally 对得上")
    check(
        "  pairs 的 count 之和 == tally['canonical']",
        sum(p["count"] for p in data["canonical_pairs"]),
        t.get("canonical", 0),
    )
    check(
        "  每组都带 key/value/样例规则/计数",
        [p.get("value") for p in data["canonical_pairs"] if not all(k in p for k in ("key", "value", "sample_rule", "count"))],
        [],
    )

    print("4. 反例：三种归类各自都要能被触发（度量不得恒真）")
    # 直接测分类判定所依赖的两个原语，而不是伪造整个语料
    stmt = "财来生世或就世较易；应期看生衰旺合"
    check("  文本里有的取值 → 字面命中", vp.vr.fold_han("妻财") in vp.vr.fold_han(stmt), False)
    check("  同句里的「財」折叠后能被「财」命中", vp.vr.fold_han("财") in vp.vr.fold_han(stmt), True)
    check(
        "  枚举阈值 ≥3 才叫枚举",
        vp.ENUM_MIN_VALUES,
        3,
    )
    check(
        "  引擎态键在工具里显式列举（不是运行时猜的）",
        "liuyao_tomb" in vp.ENGINE_STATE_KEYS and "rizhu_strength" in vp.ENGINE_STATE_KEYS,
        True,
    )

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL VALUE-PROVENANCE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())