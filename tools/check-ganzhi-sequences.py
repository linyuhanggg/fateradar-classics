#!/usr/bin/env python3
"""干支序列连续性检查（不读图，纯文本层）。

用途：转写稿里出现的干支串（尤其「行标」列、六十甲子环、逐日表）应当**在六十甲子环上连续**。
若某个字被读错或漏抄，序列就会在环上出现跳号或不连续——这是不需要读图就能发现的转写失误。

判据：
- 只检查**长度 ≥ 3** 的连续干支串（两字相邻在散文中太常见，不作为序列）（相邻两字之间只允许分隔符：空格、·、・、、、,、，、|、换行）。
- 合规 = 整串在六十甲子环上**步长恒定**（含 +1 的六十甲子、+15 的十五日/三元分节、+10 的旬首等，
  升序或降序均可）。步长不恒定才是可疑：某字读错或漏抄会打断等差。
- 输出每条不合规的串及其所在文件行号，供人工按图复核。

退出码：0 = 无非连续；1 = 存在非连续（供 CI 或人工核查使用）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
CYCLE = [GAN[i % 10] + ZHI[i % 12] for i in range(60)]
INDEX = {g: i for i, g in enumerate(CYCLE)}

PAIR = rf"[{GAN}][{ZHI}]"
# 只认**长度 ≥3** 的连续干支串：两字相邻在散文里极常见（「庚子 壬子」不是序列），
# 三字以上才基本可以肯定是「行标列/六十甲子环/逐日表」这类序列语境。
RUN = re.compile(rf"(?:{PAIR}(?:[\s·・、,，|｜]*)){{3,}}")

# 日柱标目（如「甲己日」「辛日」「丁壬」「戊癸日」）与行标同为大字两字格，混在串里会让步长失真。
# 它们以「…日」结尾或以「干支＋干支」连写出现，故在判据前先剔除这两类：
DAY_LABEL = re.compile(rf"(?:{PAIR}|[{GAN}{ZHI}]{{1,2}})日")
PAIR_GLUED = re.compile(rf"{PAIR}{PAIR}")
PAIR_RE = re.compile(PAIR)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOBS = [
    "sources/normalized/san-shi/**/*.md",
    "sources/normalized/bazi/**/*.md",
]


def sequences(text: str):
    for m in RUN.finditer(text):
        items = PAIR_RE.findall(m.group(0))
        if len(items) >= 3:
            yield m.start(), items


def check_file(path: Path):
    text = path.read_text(encoding="utf-8")
    problems = []
    total = 0
    for start, items in sequences(text):
        # 该串一旦落在「…日」标目或「干支干支」连写里，就整串跳过（不是行标序列）。
        seg = text[start : start + 80]
        if DAY_LABEL.search(seg) or PAIR_GLUED.search(seg):
            continue
        idx = [INDEX[i] for i in items]
        total += 1
        # 合规判据：步长恒定（升或降均可）。六十甲子为 +1，十五日/三元分节为 +15，旬首为 +10；
        # 步长**不恒定**才是可疑——读错或漏抄一个字就会打断等差。
        steps = {(b - a) % 60 for a, b in zip(idx, idx[1:])}
        if len(steps) != 1:
            line = text.count("\n", 0, start) + 1
            problems.append((line, items))
    return total, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="要检查的文件或目录（缺省用内置 glob）")
    args = ap.parse_args()

    files: list[Path] = []
    if args.paths:
        for raw in args.paths:
            p = Path(raw)
            files.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])
    else:
        for g in DEFAULT_GLOBS:
            files.extend(sorted(ROOT.glob(g)))
    files = sorted(set(files))

    checked = 0
    bad = 0
    for f in files:
        total, problems = check_file(f)
        checked += total
        if problems:
            bad += len(problems)
            print(f"{f.relative_to(ROOT)}: {len(problems)} 处步长不恒定")
            for line, items in problems[:5]:
                print(f"    L{line}: {' '.join(items)}")
    print(f"\n文件 {len(files)} 个｜干支串 {checked} 条｜步长不恒定 {bad} 条")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
