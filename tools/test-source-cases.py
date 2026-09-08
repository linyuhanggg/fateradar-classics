#!/usr/bin/env python3
import importlib.util
import unittest
import json
import tempfile
from pathlib import Path
spec = importlib.util.spec_from_file_location("source_cases", Path(__file__).with_name("export-source-cases.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PillarSourceChecks(unittest.TestCase):
    def test_recorded_complete_example(self):
        self.assertTrue(m.valid_pillars(["戊申", "甲子", "庚午", "丁丑"]))
    def test_source_typo_is_not_silently_repaired(self):
        self.assertFalse(m.valid_pillars(["甲申", "壬申", "乙己", "戊寅"]))
    def test_illegal_sexagenary_pair_is_not_recomputable(self):
        self.assertFalse(m.valid_pillars(["甲丑", "壬申", "乙巳", "戊寅"]))
    def test_missing_hour_is_not_filled(self):
        self.assertFalse(m.valid_pillars(["戊申", "甲子", "庚午"]))

    def test_meihua_numbers_do_not_invent_birth_date_or_pillars(self):
        fields, signature, repeated = m.case_input({"inputBasis": "meihua-numbers", "numbers": {"yearBranch": "辰", "lunarMonth": 12, "lunarDay": 17, "hourBranch": "申"}, "expected": {"main": "泽火革", "moving": 1}, "canRecompute": True})
        self.assertTrue(fields["canRecompute"])
        self.assertNotIn("pillars", fields)
        self.assertNotIn("solarDate", fields)
        self.assertEqual(fields["expected"], {"main": "泽火革", "moving": 1})
        self.assertNotIn("mutual", fields["expected"])
        self.assertEqual(repeated, "sameNumbersAs")
        self.assertIsNotNone(signature)

    def test_missing_meihua_hour_cannot_be_marked_recomputable(self):
        with self.assertRaisesRegex(ValueError, "marked recomputable"):
            m.case_input({"inputBasis": "meihua-numbers", "numbers": {"yearBranch": "辰", "lunarMonth": 12, "lunarDay": 17}, "canRecompute": True})

    def test_direct_hexagram_does_not_invent_numbers_or_mutual_method(self):
        case = {"inputBasis": "meihua-hexagram", "input": {"upper": "乾", "lower": "坤", "moving": 2}, "expected": {"mutualUpper": "巽", "mutualLower": "离"}, "canRecompute": True}
        fields, _, repeated = m.case_input(case)
        self.assertNotIn("numbers", fields)
        self.assertNotIn("pillars", fields)
        self.assertNotIn("互卦", fields["scope"])
        self.assertIn("未明说的取互对象", fields["unavailable"])
        self.assertEqual(fields["expected"], case["expected"])
        self.assertEqual(repeated, "sameHexagramInputAs")

    def test_multiple_cases_and_repeated_pillars_keep_separate_source_occurrences(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            para = root / "references/inventory/paragraphs/bazi/book.json"
            para.parent.mkdir(parents=True)
            para.write_text(json.dumps({"fulltext": "sources/book.md", "paragraphs": [{"id": "book:L0001-L0002", "start_line": 1, "end_line": 2}]}))
            annotation = root / "references/annotations/bazi/book.json"
            annotation.parent.mkdir(parents=True)
            case = {"name": "原例", "pillars": ["戊申", "甲子", "庚午", "丁丑"], "canRecompute": True}
            annotation.write_text(json.dumps({"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0002", "review": "source-reviewed", "vernacular": "同段重引", "notes": [], "cases": [case, {**case, "name": "转引例"}]}]}))
            rows = m.collect_cases(root)["cases"]
            self.assertEqual(len(rows), 2)
            self.assertNotEqual(rows[0]["id"], rows[1]["id"])
            self.assertEqual(rows[1]["samePillarsAs"], rows[0]["id"])
            self.assertEqual(rows[0]["source"]["paragraphId"], "book:L0001-L0002")
            self.assertFalse(rows[0]["verified"])
            self.assertIn("公历生日", rows[0]["unavailable"])

if __name__ == "__main__":
    unittest.main()
