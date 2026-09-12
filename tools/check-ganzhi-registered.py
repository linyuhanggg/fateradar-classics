#!/usr/bin/env python3
"""把「干支序列步长筛查」的实测条数与**已登记待核**条数对账（供 CI 用）。

为什么需要这一层：筛查会如实报出「步长不恒定」的串，但其中一部分是**已登记待核**的
（例如奇门 p281 第 6 列的「巳/卯」，需原生读图复读一次才能结案），在本仓当前能力下无法关闭。
若让筛查自己当门禁，CI 会长期红着——红着的门禁等于没有门禁。
所以这里只对账**集合是否变化**：条数必须等于登记数，且每条都能在登记清单里找到对应行。

用法：
  python tools/check-ganzhi-registered.py          # 对账；不一致则 exit 1
  python tools/check-ganzhi-registered.py -v       # 同时打印每条
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location(
    "check_ganzhi", Path(__file__).with_name("check-ganzhi-sequences.py")
)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)

# ── 已登记待核的「步长不恒定」串 ──────────────────────────────────────────────
# 每条 = (文件, 行号, 串)。行号变化也视为不一致：说明文件被改动过，须重新核对。
# 现有 3 条的来历与待办写在 sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-0280-0298.md
# 的 doubt_281；它们是同一页（p281）同一行 C6–C11 的三处重复引用。
REGISTERED: list[tuple[str, int, str]] = [
    (
        "sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-0280-0298.md",
        98,
        "甲子 乙丑 丙寅 丁卯 戊辰 己卯",
    ),
    (
        "sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-0280-0298.md",
        104,
        "甲子 乙丑 丙寅 丁卯 戊辰 己卯",
    ),
    (
        "sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-0280-0298.md",
        110,
        "甲子 乙丑 丙寅 丁卯 戊辰 己卯",
    ),
]


def scan() -> list[tuple[str, int, str]]:
    """按工具的判据重扫默认范围，返回 (相对路径, 行号, 串文本)。"""
    files: list[Path] = []
    for g in cg.DEFAULT_GLOBS:
        files.extend(sorted(ROOT.glob(g)))
    out: list[tuple[str, int, str]] = []
    for f in sorted(set(files)):
        _, problems, _ = cg.check_file(f)
        for line, items in problems:
            out.append((str(f.relative_to(ROOT)), line, " ".join(items)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    found = scan()
    for rel, line, text in found:
        if args.verbose:
            print(f"  L{line} {rel}: {text}")
    print(f"实测步长不恒定 {len(found)} 条｜已登记 {len(REGISTERED)} 条")

    got = sorted(found)
    want = sorted(REGISTERED)
    if got != want:
        print("\n不一致——以下条目未登记（新增须先逐条核对，确属真实转写问题就修文本，"
              "确属待读图复核就登记进本文件并写明理由）：")
        for item in got:
            if item not in want:
                print(f"  新增: L{item[1]} {item[0]}: {item[2]}")
        for item in want:
            if item not in got:
                print(f"  消失（已修复？请从 REGISTERED 移除）: L{item[1]} {item[0]}: {item[2]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
