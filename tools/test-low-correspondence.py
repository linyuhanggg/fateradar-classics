#!/usr/bin/env python3
"""低对应度分诊的回归测试（t202）。

钉住**本轮的结论本身**，而不是那个不可靠的分类：

1. 读单条数稳定（对应度 < 0.05 的规则），且每条都带 anchor/quote/statement 摘要
   —— 它是给人眼读的列表，缺字段就没法读；
2. **本轮的负面结论**：这个档位**大部分不是「锚点错位」**。
   实测 40 条里 23 条「三处都无重叠」→ statement 多为现代归纳／包级声明；
   9 + 8 条的标签也已被实读证明不可当判定。测试断言「no-overlap-anywhere 占多数」，
   若哪天这个分布翻转，说明引文/陈述的性质变了，值得重新看。
3. **反例**：给一段与 statement 毫无关系的文本，二元组覆盖率必须接近 0
   ——证明这个度量不是恒真（恒真的度量等于没有度量）。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("lc", ROOT / "tools/low-correspondence-triage.py")
lc = importlib.util.module_from_spec(_spec)
sys.modules["lc"] = lc
assert _spec.loader is not None
_spec.loader.exec_module(lc)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    rows = lc.triage()

    print("1. 读单成形")
    check("  条数 > 0", len(rows) > 0, True)
    check(
        "  每条都有 anchor/quote/statement 摘要",
        [r["rule_id"] for r in rows if not r.get("anchor") or not r.get("quote_head") or not r.get("statement_head")],
        [],
    )
    check(
        "  每条都带人读建议",
        [r["rule_id"] for r in rows if "人眼" not in (r.get("proposal") or "")],
        [],
    )

    print("2. 本轮结论：该档位大多是「无重叠」，不是「锚点错位」")
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    check("  no-overlap-anywhere 占多数", kinds.get("no-overlap-anywhere", 0) * 2 > len(rows), True)
    check("  三类合计 == 条数", sum(kinds.values()), len(rows))

    print("3. 反例：不相干文本的二元组覆盖率应接近 0（度量非恒真）")
    stmt = "童限自婴幼期起按古歌分配各宫；现代仅作语义层。"
    unrelated = "入庙者乃星辰登于廊庙之中，犹人出仕立于殿陛之间，所以为贵也。"
    cov = lc.coverage(lc.content_bigrams(stmt), unrelated)
    check("  不相干文本覆盖率低（<0.15）", cov < 0.15, True)
    same = lc.coverage(lc.content_bigrams(stmt), stmt)
    check("  自比覆盖率 == 1.0", same, 1.0)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL LOW-CORRESPONDENCE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())