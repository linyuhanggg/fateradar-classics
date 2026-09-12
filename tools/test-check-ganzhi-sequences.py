#!/usr/bin/env python3
"""check-ganzhi-sequences 的判据自检（含变异测试）。

这个筛查的价值全在「报出来的确实可疑、没报的确实合规」。
第一次跑就出现 4 例假警（四柱列举被当成序列），所以判据必须有测试钉住：

- 真序列（连续时支列、六十甲子环、旬首、大运整列）必须不被报；
- 误读串（连续列里末字读错）必须被报，**而且不能因为排除规则被吃掉**；
- 四柱列举（盘例语附近、串长恰为 4）必须被排除，且排除数可见。
"""

import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "check_ganzhi", Path(__file__).with_name("check-ganzhi-sequences.py")
)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)


class GanzhiSequenceScreen(unittest.TestCase):
    def run_text(self, text: str):
        """返回 (被判为序列的串数, 发现, 被排除的柱位列举数)。"""
        problems = []
        pillars = 0
        total = 0
        for start, items in cg.sequences(text):
            seg = text[start : start + 80]
            if cg.DAY_LABEL.search(seg) or cg.PAIR_GLUED.search(seg):
                continue
            if len(items) == 4 and cg.is_pillar_list(text, start, seg):
                pillars += 1
                continue
            idx = [cg.INDEX[i] for i in items]
            steps = {(b - a) % 60 for a, b in zip(idx, idx[1:])}
            total += 1
            if len(steps) != 1:
                problems.append(items)
        return total, problems, pillars

    def test_consecutive_hour_columns_pass(self):
        total, problems, _ = self.run_text("甲子 乙丑 丙寅 丁卯 戊辰 己巳")
        self.assertEqual(total, 1)
        self.assertEqual(problems, [])

    def test_misread_last_hour_column_is_reported(self):
        # 己巳 误读成 己卯：干位仍连续，支位断裂。
        total, problems, _ = self.run_text("甲子 乙丑 丙寅 丁卯 戊辰 己卯")
        self.assertEqual(total, 1)
        self.assertEqual(problems, [["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己卯"]])

    def test_xun_head_and_fifteen_day_strides_pass(self):
        self.assertEqual(self.run_text("甲子 甲戌 甲申 甲午")[1], [])
        self.assertEqual(self.run_text("甲子 己卯 甲午 己酉")[1], [])

    def test_pillar_enumeration_is_excluded_with_marker(self):
        # 四柱：正例 + 三种真实出现过的天干形态。
        for text in (
            "四柱庚申 庚辰 戊辰 戊午",
            "四柱壬辰 壬寅 甲寅 庚午",
            "盘例癸酉 甲子 癸亥 辛酉",
            "大运丙申 乙未 甲午 癸巳",
        ):
            total, problems, pillars = self.run_text(text)
            self.assertEqual(problems, [], text)
            self.assertEqual(pillars, 1, text)
            self.assertEqual(total, 0, text)

    def test_pillar_like_run_without_marker_is_still_reported(self):
        # 变异测试：同一样的四柱串，但**附近没有任何列举语**时不得被排除。
        # 否则「排除规则」会变成一个吞掉真实发现的洞。
        total, problems, pillars = self.run_text("此处原文作 庚申 庚辰 戊辰 戊午 而电子本作 庚申 庚辰 戊辰 戊午")
        self.assertEqual(pillars, 0)
        self.assertGreaterEqual(total, 1)

    def test_long_pillar_run_is_not_excluded(self):
        # 大运整列（8 个）不是四柱，仍须满足步长恒定。
        total, problems, pillars = self.run_text("大运丙申 乙未 甲午 癸巳 壬辰 辛卯 庚寅 己丑")
        self.assertEqual(pillars, 0)
        self.assertEqual(problems, [])
        total2, problems2, _ = self.run_text("大运丙申 乙未 甲午 癸巳 壬辰 辛卯 庚寅 己卯")
        self.assertEqual(total2, 1)
        self.assertEqual(len(problems2), 1)


if __name__ == "__main__":
    unittest.main()
