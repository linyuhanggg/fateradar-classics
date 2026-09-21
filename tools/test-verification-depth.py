#!/usr/bin/env python3
"""「验证深度」报告的回归测试（t198）。

钉住三件事：

1. **不变量**：`全信息不足 == 0`。若某条谓词的键真的在任何样盘里都没出现，
   它就会落进这一类；而**死引用扫描**（`dead-reference-report.py`）也必然报出来。
   两者是独立实现，**同时干净**才算事实层没漏。测试直接交叉调用两者。
2. **分类**：`有满足 + 未被满足 == 已映射`；未被满足的归因里，
   目录式（六十甲子纳音一类按取值逐条编排）应占大头——那类要 60 张盘才能逐条演示。
3. **反例**：给 `classify` 一条引用**不存在键**的规则，必须落进「全信息不足」
   ——证明分类不是空转（恒过 0 的检查等于没有检查）。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("vd", ROOT / "tools/verification-depth-report.py")
vd = importlib.util.module_from_spec(_spec)
sys.modules["vd"] = vd
assert _spec.loader is not None
_spec.loader.exec_module(vd)

_spec2 = importlib.util.spec_from_file_location("dr2", ROOT / "tools/dead-reference-report.py")
dr = importlib.util.module_from_spec(_spec2)
sys.modules["dr2"] = dr
assert _spec2.loader is not None
_spec2.loader.exec_module(dr)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    r = vd.report()

    print("1. 不变量：全信息不足 == 0，且与死引用扫描一致")
    check("  全信息不足", r["total"].get("全信息不足", 0), 0)
    check("  死引用扫描同时为 0（独立实现）", dr.find_dead(), [])
    check("  已映射 > 300（确有施工）", r["mapped"] > 300, True)

    print("2. 分类自洽")
    check("  有满足 + 未被满足 == 已映射", r["demonstrated"] + r["undemonstrated"], r["mapped"])
    check("  entries 条数 == 未被满足数", len(r["entries"]), r["undemonstrated"])
    check(
        "  未被满足的归因合计 == 未被满足数",
        sum(r["undemonstrated_by_why"].values()),
        r["undemonstrated"],
    )
    check(
        "  目录式（六十甲子一类）占大头",
        r["undemonstrated_by_why"].get("catalogue-by-value", 0) >= 50,
        True,
    )
    check(
        "  每条未被满足的都有 kind 与 why",
        [e["rule_id"] for e in r["entries"] if not e.get("kind") or not e.get("why")],
        [],
    )

    print("3. 反例：引用不存在的键 → 必须落进「全信息不足」")
    bogus = {
        "rule_id": "TEST-BOGUS",
        "applicable_to": [{"key": "does_not_exist_key", "value": "X"}],
        "anchor": {"file": "x", "start_line": 1, "end_line": 1},
    }
    import json

    dump = json.loads(vd.DUMP.read_text(encoding="utf-8"))
    check(
        "  classify 判为「全信息不足」",
        vd.classify(bogus, dump["bazi"]),
        "全信息不足",
    )
    good = {
        "rule_id": "TEST-GOOD",
        "applicable_to": [{"key": "gan", "value": "甲"}],
        "anchor": {"file": "x", "start_line": 1, "end_line": 1},
    }
    check("  键在场的规则不会落进「全信息不足」", vd.classify(good, dump["bazi"]) != "全信息不足", True)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL VERIFICATION-DEPTH OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())