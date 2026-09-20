#!/usr/bin/env python3
"""有据定义表与其求值的回归测试（t183）。

钉住四件事：

1. **引文逐字落在所引行上**——定义表里每一条 source/evidence 的 quote 必须是那一行原文的
   逐字片段。初版我把 register 的**截断**引文（带 `…`）粘了进来，还有一条文件路径写错；
   这条断言就是为它们立的。
2. **查得到就按原文展开求值**：`君臣庆会` 在本样本盘上应判**不满足**
   （原文 L1595「紫微左右同守命是也」→ 三星须同在命宫）。
3. **有定义但缺事实 → 信息不足**（不是「未提供定义表」），且理由里要带**锚点行**。
4. **语料里确实没有构成定义 → 仍报「未提供定义表」**，并给出检索证据
   （`辅弼夹帝` 只在赋文里作断语、`魁命钺身` 全文 0 次、`禄马同宫` 只在别门散文里）。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFS = ROOT / "references/definitions"

spec = importlib.util.spec_from_file_location("ee_t", ROOT / "tools/eval-executable.py")
ee = importlib.util.module_from_spec(spec)
sys.modules["ee_t"] = ee
assert spec.loader is not None
spec.loader.exec_module(ee)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def fact(key, value, **scope):
    return {"key": key, "value": value, "scope": scope, "derivedFrom": ["test"]}


def main() -> int:
    print("1. 定义表：引文逐字落在所引行上")
    n_quotes = 0
    bad = []
    tables = []
    for f in sorted(DEFS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        tables.append((f, d))
        for e in (d.get("entries") or []) + (d.get("not_defined") or []):
            refs = ([e["source"]] if e.get("source") else []) + (e.get("evidence") or [])
            for s in refs:
                n_quotes += 1
                p = ROOT / s["file"]
                if not p.is_file():
                    bad.append(f"{e['name']}: 文件不存在 {s['file']}")
                    continue
                lines = p.read_text(encoding="utf-8").split("\n")
                if s["line"] > len(lines) or s["quote"] not in lines[s["line"] - 1]:
                    bad.append(f"{e['name']}: {s['file']} L{s['line']} 引文不是逐字片段")
    check(f"  {n_quotes} 处引文全部逐字（含路径存在）", bad, [])

    print("2. 定义表：三态齐全且不编造")
    entries = [e for _f, d in tables for e in d.get("entries") or []]
    not_def = [e for _f, d in tables for e in d.get("not_defined") or []]
    check("  有据定义 8 条", len(entries), 8)
    check("  evaluable 恰 1 条", [e["name"] for e in entries if e["status"] == "evaluable"], ["君臣庆会"])
    check("  needs-fact 7 条", sum(1 for e in entries if e["status"] == "needs-fact"), 7)
    # 用集合比较：中文按码位排序与书写顺序不同，别把排序差异当成内容差异
    check("  无构成定义的 3 条", {e["name"] for e in not_def}, {"辅弼夹帝", "禄马同宫", "魁命钺身"})
    check("  absent 只有魁命钺身", [e["name"] for e in not_def if e["status"] == "absent"], ["魁命钺身"])
    check(
        "  每条有据定义都带锚点行",
        [e["name"] for e in entries if not (e.get("source") or {}).get("line")],
        [],
    )

    print("3. 求值：查得到就按原文展开")
    cheng = [e for e in entries if e["name"] == "君臣庆会"][0]
    chart_bad = [fact("ziwei_star", "紫微", layer="本命", palace="命宫")]
    check("  只有紫微在命宫 → 不满足", ee.eval_definition("君臣庆会", chart_bad, {"ziwei_star"})[0], ee.FALSE)
    chart_ok = [
        fact("ziwei_star", "紫微", layer="本命", palace="命宫"),
        fact("ziwei_star", "左辅", layer="本命", palace="命宫"),
        fact("ziwei_star", "右弼", layer="本命", palace="命宫"),
    ]
    check("  三星同在命宫 → 满足", ee.eval_definition("君臣庆会", chart_ok, {"ziwei_star"})[0], ee.TRUE)
    chart_wrong_palace = [
        fact("ziwei_star", "紫微", layer="本命", palace="命宫"),
        fact("ziwei_star", "左辅", layer="本命", palace="兄弟"),
        fact("ziwei_star", "右弼", layer="本命", palace="命宫"),
    ]
    check(
        "  左辅不在命宫 → 不满足（scope.palace 真的在起作用）",
        ee.eval_definition("君臣庆会", chart_wrong_palace, {"ziwei_star"})[0],
        ee.FALSE,
    )
    check(
        "  展开式与原文一致（三句 all_of 各自 scope.palace=命宫）",
        sorted({c["scope"]["palace"] for c in cheng["expansion"]["all_of"]}),
        ["命宫"],
    )

    print("4. 有定义但缺事实 → 信息不足，且理由带锚点")
    verdict, notes = ee.eval_definition("武曲守垣", [], {"ziwei_star"})
    check("  信息不足（不是「未提供定义表」）", verdict, ee.UNKNOWN)
    check("  理由带锚点行", "L1619" in notes[0], True)
    check("  理由说明缺什么", "宫地支" in notes[0], True)

    print("5. 语料无构成定义 → 仍报「未提供定义表」，并给检索证据")
    verdict, notes = ee.eval_definition("魁命钺身", [], set())
    check("  魁命钺身 → 未提供定义表", verdict, ee.UNDEF)
    check("  理由含「0 次」证据", "0 次" in notes[0], True)
    verdict, _ = ee.eval_definition("辅弼夹帝", [], set())
    check("  辅弼夹帝 → 未提供定义表", verdict, ee.UNDEF)
    verdict, _ = ee.eval_definition("禄马同宫", [], set())
    check("  禄马同宫 → 未提供定义表", verdict, ee.UNDEF)
    verdict, notes = ee.eval_definition("查无此名", [], set())
    check("  表外名字 → 未提供定义表", verdict, ee.UNDEF)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL DEFINITION-TABLE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())