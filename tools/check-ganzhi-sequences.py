#!/usr/bin/env python3
"""干支序列连续性检查（不读图，纯文本层）。

用途：转写稿里出现的干支串（尤其「行标」列、六十甲子环、逐日表）应当**在六十甲子环上连续**。
若某个字被读错或漏抄，序列就会在环上出现跳号或不连续——这是不需要读图就能发现的转写失误。

判据：
- 只检查**长度 ≥ 3** 的连续干支串（两字相邻在散文中太常见，不作为序列）（相邻两字之间只允许分隔符：空格、·、・、、、,、，、|、换行）。
- 合规 = 整串在六十甲子环上**步长恒定**（含 +1 的六十甲子、+15 的十五日/三元分节、+10 的旬首等，
  升序或降序均可）。步长不恒定才是可疑：某字读错或漏抄会打断等差。
- **排除两类「本来就不该等差」的写法**（否则会刷出假警，第一次跑就出现 4 例）：
  1. `…日` 标目与 `干支干支` 连写（原有）。
  2. **独立柱位列举**：四个干支是四个各自独立的柱（四柱、大运列，如「庚申 庚辰 戊辰 戊午」、
     「丙申 乙未 甲午 癸巳」），不是同一环上的连续序列。
     判据（**串长恰为 4 且附近有列举标记**）：四个干支都是合法干支，且串所在行/邻行出现
     「四柱／盘例／运列／例／大运」这类**盘例列举语**。此时四个干支是四个各自独立的柱，
     不是环上的连续序列。
     只对**四柱**适用：连续时支列、六十甲子环、大运**整列**（8 个以上）都不在此列，
     它们照样要满足步长恒定。
     为什么不用「干支位步长」之类的结构判据：四柱的天干形态不固定（庚庚戊戊、壬壬甲庚、
     癸甲癸辛都有），而真正该报的误读串（连续列里末字读错）其天干恰好是连续 +1——
     结构判据要么漏掉前三者，要么吃掉后者；**列举标记是更可靠、也更可复核的判据**。
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


PILLAR_CONTEXT = re.compile(r"四柱|盘例|运列|大运|另盘|例")


def is_pillar_list(text: str, start: int, seg: str) -> bool:
    """
    四柱列举：串长恰为 4，且串所在行或邻行出现盘例列举语（四柱／盘例／运列／大运／例）。
    """
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", start)
    line = text[line_start : line_end if line_end >= 0 else len(text)]
    return bool(PILLAR_CONTEXT.search(line))


def check_file(path: Path):
    text = path.read_text(encoding="utf-8")
    problems = []
    pillars = []
    total = 0
    for start, items in sequences(text):
        # 该串一旦落在「…日」标目或「干支干支」连写里，就整串跳过（不是行标序列）。
        seg = text[start : start + 80]
        if DAY_LABEL.search(seg) or PAIR_GLUED.search(seg):
            continue
        idx = [INDEX[i] for i in items]
        steps = {(b - a) % 60 for a, b in zip(idx, idx[1:])}
        line = text.count("\n", 0, start) + 1
        # 独立柱位列举（四柱／大运列）本来就不等差，单独计数，不算发现。
        if len(items) == 4 and is_pillar_list(text, start, seg):
            pillars.append((line, items))
            continue
        total += 1
        # 合规判据：步长恒定（升或降均可）。六十甲子为 +1，十五日/三元分节为 +15，旬首为 +10；
        # 步长**不恒定**才是可疑——读错或漏抄一个字就会打断等差。
        if len(steps) != 1:
            problems.append((line, items))
    return total, problems, pillars


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
    excluded = 0
    for f in files:
        total, problems, pillars = check_file(f)
        checked += total
        excluded += len(pillars)
        if problems:
            bad += len(problems)
            print(f"{f.relative_to(ROOT)}: {len(problems)} 处步长不恒定")
            for line, items in problems[:5]:
                print(f"    L{line}: {' '.join(items)}")
    print(
        f"\n文件 {len(files)} 个｜被判为序列的干支串 {checked} 条｜其中步长不恒定 {bad} 条"
        f"｜另排除独立柱位列举（四柱／大运列）{excluded} 条（不计入发现，见文件头判据）"
    )
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
