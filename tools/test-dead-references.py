#!/usr/bin/env python3
"""「死引用」扫描的回归测试（t192）。

既跑正例（真实语料必须零死引用），也跑**反例**——证明这个扫描不是空跑：
把某个术的已观测键集合人为挖掉一个，扫描必须报出来。

之所以要证明它非空跑：这类扫描的价值全在「它会红」；一个恒过 0 的扫描等于没有扫描
（t187 记过的同一教训）。

同时钉住本轮的具体修复：`daxian` / `liunian_taisui` 必须在样盘里出现过
（它们只有在给了**参照日期**时才产出；此前样盘不带参照日期，导致 8 条 ziwei 规则
恒为「信息不足」，被误记成「事实缺失」）。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("dr", ROOT / "tools/dead-reference-report.py")
dr = importlib.util.module_from_spec(_spec)
sys.modules["dr"] = dr
assert _spec.loader is not None
_spec.loader.exec_module(dr)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    print("1. 正例：真实语料零死引用")
    check("  find_dead() == []", dr.find_dead(), [])

    print("2. 运限层确实进了样盘（本轮修复）")
    seen = dr.observed_keys()
    check("  ziwei 样盘含 daxian", "daxian" in seen.get("ziwei", set()), True)
    check("  ziwei 样盘含 liunian_taisui", "liunian_taisui" in seen.get("ziwei", set()), True)

    print("3. 反例：挖掉一个键必须报出来（证明扫描非空跑）")
    trimmed = {k: set(v) for k, v in seen.items()}
    trimmed["ziwei"] = set(trimmed.get("ziwei", set())) - {"daxian"}
    dead = dr.find_dead(trimmed)
    hit = [x for x in dead if x[2] == "daxian"]
    check("  报出引用 daxian 的规则", len(hit) > 0, True)
    check("  且 art 正确", sorted({a for a, _r, _k in hit}), ["ziwei"])

    trimmed2 = {k: set(v) for k, v in seen.items()}
    trimmed2["liuyao"] = set(trimmed2.get("liuyao", set())) - {"yao_zhi"}
    hit2 = [x for x in dr.find_dead(trimmed2) if x[2] == "yao_zhi"]
    check("  挖掉 liuyao.yao_zhi 也会报", len(hit2) > 0, True)

    print("4. 空集不误报（没有样盘的术另行处理，不应把全部叶子都算死引用）")
    blank = {k: set() for k in ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")}
    n_blank = len(dr.find_dead(blank))
    n_real = len(dr.find_dead())
    check("  空样盘时报出的数量 ≥ 真实情况", n_blank >= n_real, True)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL DEAD-REFERENCE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())