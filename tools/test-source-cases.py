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
