#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('chronicle', Path(__file__).with_name('build-huangji-chronicle-context.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ChronicleContextTests(unittest.TestCase):
    def run_extract(self, lines):
        paragraphs = [{'id': f'p{i}', 'start_line': i, 'end_line': i} for i in range(1, len(lines)+1)]
        return module.extract(lines, paragraphs, 1, len(lines))

    def test_parent_change_clears_descendants(self):
        rows, _ = self.run_extract(['觀物篇十三', '經日之甲一', '經月之寅三', '經星之己七十六',
                                   '經辰之子二千一百', '甲子二', '經月之卯四', '乙丑三'])
        self.assertEqual(rows[4]['parsed']['parents']['辰']['numberRaw'], '二千一百')
        self.assertIsNone(rows[-1]['parsed']['parents']['辰'])
        self.assertIn('missing-explicit-parent:星辰', rows[-1]['flags'])

    def test_unparsed_coordinate_is_barrier(self):
        rows, deferred = self.run_extract(['經日之甲一', '經月之寅三', '經星之己七十六',
                                          '經辰之子二千一百', '經星之□七十七', '甲子二'])
        self.assertIsNone(rows[-1]['parsed']['parents']['星'])
        self.assertIsNone(rows[-1]['parsed']['parents']['辰'])
        self.assertEqual(deferred[0]['sourceRaw'], '經星之□七十七')

    def test_do_not_infer_ruler_or_split_multicolumn(self):
        rows, deferred = self.run_extract(['甲辰唐堯', '乙巳二', '丙午三 四', '戊申五〔未校〕'])
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(deferred), 3)
        self.assertEqual(rows[0]['parsed']['numberRaw'], '二')
        self.assertFalse(any(rows[0]['parsed']['parents'].values()))
        self.assertEqual(rows[0]['entry']['review'], 'draft')

    def test_chapter_resets_and_unusual_label_preserved(self):
        rows, _ = self.run_extract(['經日之甲一', '經月之己三', '經星之乙二',
                                   '觀物篇十四', '經星之丙三'])
        self.assertEqual(rows[1]['parsed']['node']['labelRaw'], '己')
        self.assertIn('unusual-axis-label:月', rows[1]['flags'])
        self.assertIsNone(rows[-1]['parsed']['parents']['日'])
        self.assertEqual(rows[-1]['parsed']['chapter']['line'], 4)


if __name__ == '__main__':
    unittest.main()
