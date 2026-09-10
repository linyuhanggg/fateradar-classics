#!/usr/bin/env python3
"""Structural exporter tests use a tiny source; semantic month expectations live in engine tests."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("export_tiaohou", Path(__file__).with_name("export-tiaohou.py"))
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ExportTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        text = self.root / exporter.TEXT
        text.parent.mkdir(parents=True)
        text.write_text("独立测试原文片段。\n\n第二段明确来源。\n", encoding="utf-8")
        self.pid = "qiongtong-baojian:L0001-L0001"
        self.write("references/inventory/paragraphs/bazi/qiongtong-baojian.json", {"paragraphs": [
            {"id": self.pid, "heading": "例文", "start_line": 1, "end_line": 1},
            {"id": "qiongtong-baojian:L0003-L0003", "heading": "例文", "start_line": 3, "end_line": 3},
        ]})
        self.data = {"schema_version": "fateradar-executable-v2", "verified": False,
                     "book": {"slug": "qiongtong-baojian", "title": "穷通宝鉴", "fulltext": exporter.TEXT}, "rules": []}
        for day in exporter.STEMS:
            for month in exporter.MONTHS:
                self.data["rules"].append({"id": day + month, "sources": [{"paragraph_id": self.pid, "start_line": 1, "end_line": 1, "quote": "独立测试原文片段。"}],
                    "tiaohou": {"dayGan": day, "monthZhi": month, "scope": "month", "priority": [["丙", "癸"]], "note": "只测结构，不声称此片段包含所有月令取用。", "sourceParagraphIds": [self.pid], "checks": []}})

    def write(self, relative, data):
        path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def export(self):
        self.write(exporter.PACK, self.data)
        return exporter.build_export(self.root, "fixture-revision")

    def test_preserves_joint_group_and_exact_source(self):
        output = self.export()
        self.assertEqual(len(output["profiles"]), 120)
        self.assertEqual(output["profiles"][0]["priority"], [["丙", "癸"]])
        self.assertEqual(next(iter(output["sources"].values()))["quote"], "独立测试原文片段。")

    def test_missing_month_fails_instead_of_filling_default(self):
        self.data["rules"].pop()
        with self.assertRaisesRegex(ValueError, "120"):
            self.export()

    def test_duplicate_month_fails(self):
        self.data["rules"][-1] = copy.deepcopy(self.data["rules"][0])
        with self.assertRaisesRegex(ValueError, "重复"):
            self.export()

    def test_quote_cannot_be_rewritten(self):
        self.data["rules"][0]["sources"][0]["quote"] = "已得用。"
        with self.assertRaisesRegex(ValueError, "quote"):
            self.export()

    def test_source_cannot_cross_paragraph(self):
        self.data["rules"][0]["sources"][0].update(end_line=3, quote="独立测试原文片段。\n\n第二段明确来源。")
        with self.assertRaisesRegex(ValueError, "超出"):
            self.export()

    def test_profile_cannot_reference_undeclared_source(self):
        self.data["rules"][0]["tiaohou"]["sourceParagraphIds"] = ["qiongtong-baojian:L0003-L0003"]
        with self.assertRaisesRegex(ValueError, "未声明"):
            self.export()

    def test_replacement_effect_survives_export(self):
        self.data["rules"][0]["tiaohou"]["checks"] = [{"id": "conditional", "label": "缺壬", "role": "alternative", "effect": "replace", "priority": [["己"]], "conditions": [{"kind": "absent", "gan": "壬", "scope": "all", "label": "未见壬"}], "explanation": "测试明确替代", "sourceParagraphIds": [self.pid]}]
        check = self.export()["profiles"][0]["checks"][0]
        self.assertEqual(check["effect"], "replace")
        self.assertEqual(check["priority"], [["己"]])
        self.assertEqual(check["sourceIds"], [self.pid + "@1-1"])


if __name__ == "__main__":
    unittest.main()
