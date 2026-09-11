#!/usr/bin/env python3
"""Regression gates for executable source integrity, using independent tiny text."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("validate_executable", Path(__file__).with_name("validate-executable.py"))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "sources/fulltext/bazi/example/fulltext.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("官逢傷，而透印以解之。\n\n相神有傷，立敗其格。\n", encoding="utf-8")
        paragraphs = self.root / "references/inventory/paragraphs/bazi/example.json"
        paragraphs.parent.mkdir(parents=True)
        paragraphs.write_text(json.dumps({"fulltext": "sources/fulltext/bazi/example/fulltext.md", "paragraphs": [
            {"id": "example:L0001-L0001", "start_line": 1, "end_line": 1},
            {"id": "example:L0003-L0003", "start_line": 3, "end_line": 3},
        ]}), encoding="utf-8")
        self.rule = {
            "id": "EX-E-01", "art": "bazi", "theme": "官逢伤", "school": "例文", "page": "geju",
            "paragraph_ids": ["example:L0001-L0001", "example:L0003-L0003"],
            "sources": [
                {"paragraph_id": "example:L0001-L0001", "start_line": 1, "end_line": 1, "quote": "官逢傷，而透印以解之。"},
                {"paragraph_id": "example:L0003-L0003", "start_line": 3, "end_line": 3, "quote": "相神有傷，立敗其格。"},
            ],
            "quote": "官逢傷，而透印以解之。\n[…]\n相神有傷，立敗其格。",
            "required_facts": ["stems"], "when": {"exists": "stems"},
            "satisfy_when": "条件已计算并成立", "fail_when": "条件已计算且不成立", "unknown_when": "缺少位置或力量",
            "rescue": "unimplemented", "vernacular": "需看印是否能起作用。", "implementation_assumption": "只记录位置。", "verified": False,
        }
        self.data = {"schema_version": "fateradar-executable-v2", "book": {"slug": "example", "system": "bazi", "title": "例文", "fulltext": "sources/fulltext/bazi/example/fulltext.md"}, "verified": False, "rules": [self.rule]}
        self.path = self.root / "references/executable/example.json"
        self.path.parent.mkdir(parents=True)

    def result(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        return validator.validate(self.root)

    def rejects(self, code):
        result = self.result()
        self.assertFalse(result["ok"])
        self.assertIn(code, [e["code"] for e in result["errors"]])

    def test_real_cross_paragraph_sources_pass(self):
        self.assertTrue(self.result()["ok"])

    def test_arbitrary_range_is_not_a_paragraph_id(self):
        self.rule["sources"][0]["paragraph_id"] = "example:L0001-L0003"
        self.rejects("PARAGRAPH_ID")

    def test_source_cannot_cross_its_paragraph(self):
        self.rule["sources"][0].update(end_line=3, quote=self.source.read_text().rstrip("\n"))
        self.rejects("RANGE")

    def test_rewritten_or_injected_quote_fails(self):
        self.rule["sources"][0]["quote"] = "官逢傷，已成格。"
        self.rejects("QUOTE")

    def test_quote_with_correct_text_but_wrong_range_fails(self):
        self.rule["sources"][0].update(start_line=3, end_line=3)
        self.rejects("QUOTE")

    def test_out_of_file_range_fails(self):
        self.rule["sources"][0]["end_line"] = 99
        self.rejects("RANGE")

    def test_summary_cannot_remove_negation_or_omit_a_source(self):
        self.rule["quote"] = self.rule["sources"][0]["quote"]
        self.rejects("QUOTE_SUMMARY")

    def test_paragraph_list_cannot_hide_a_source(self):
        self.rule["paragraph_ids"].pop()
        self.rejects("PARAGRAPH_IDS")

    def test_unknown_rescue_dependency_fails(self):
        self.rule["rescue"] = "EX-E-NOT-IMPLEMENTED"
        self.rejects("DEPENDENCY")

    def test_duplicate_rule_id_fails(self):
        self.data["rules"].append(dict(self.rule))
        self.rejects("DUPLICATE_ID")

    def test_electronic_anchor_cannot_promote_verified(self):
        self.rule["verified"] = True
        self.rejects("VERIFIED")

    def test_inventory_must_point_to_same_fulltext(self):
        other = self.source.with_name("other.md")
        other.write_text(self.source.read_text(), encoding="utf-8")
        self.data["book"]["fulltext"] = "sources/fulltext/bazi/example/other.md"
        self.rejects("BOOK")


if __name__ == "__main__":
    unittest.main()
