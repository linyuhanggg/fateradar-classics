#!/usr/bin/env python3
"""取值域检查的回归测试（t201）。

正例：真实语料 0 处越域。**反例**：人为给某个封闭值域键一个域外取值，必须报出来
——恒过 0 的检查等于没有检查。

另钉住 t201 记下的一个易错点：`rizhu` 是**日干**（值域十天干），不是「日柱」。
若哪天有人把引擎改成产出六十甲子、或把词表改错，这个断言会先红。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("dc", ROOT / "tools/domain-check.py")
dc = importlib.util.module_from_spec(_spec)
sys.modules["dc"] = dc
assert _spec.loader is not None
_spec.loader.exec_module(dc)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    print("1. 正例：真实语料无越域取值")
    check("  find_out_of_domain() == []", dc.find_out_of_domain(), [])

    print("2. 值域来自词表声明，不是记忆")
    doms = dc.closed_domains()
    check("  rizhu 是十天干（日干）——不是六十甲子", len(doms.get("rizhu", set())), 10)
    check("  含 乙", "乙" in doms.get("rizhu", set()), True)
    # nayin 是**开放**值域（纳音名很多、词表未穷举）→ 不参与越域判定；用 zhi 钉一个封闭大值域。
    check("  nayin 是开放值域（不参与越域判定）", doms.get("nayin", set()), set())
    check("  zhi 是封闭的十二地支", len(doms.get("zhi", set())), 12)

    print("3. 反例：域外取值必须报出来")
    trimmed = {k: set(v) for k, v in doms.items()}
    trimmed["rizhu"] = {"甲"}          # 只留一个合法值 → 乙/丁/癸 等全成域外
    bad = dc.find_out_of_domain(trimmed)
    check("  报出条目 > 0", len(bad) > 0, True)
    check("  都是 rizhu 键", sorted({k for _r, k, _v, _n in bad}), ["rizhu"])
    check("  报出的取值确实不在裁剪后的值域里", all(v not in trimmed["rizhu"] for _r, _k, v, _n in bad), True)

    print("4. 开放值域不参与判定（不应把开放键的任意取值都算越域）")
    trimmed2 = {k: set(v) for k, v in doms.items()}
    for open_key in ("liuyao_activity", "keti"):
        trimmed2.pop(open_key, None)
    check("  去掉开放键后仍为 0", dc.find_out_of_domain(trimmed2), [])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL DOMAIN-CHECK OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())