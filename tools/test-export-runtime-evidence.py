#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("runtime_evidence_export", Path(__file__).with_name("export-runtime-evidence.py"))
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)


class RuntimeEvidenceExportTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.file = "sources/fulltext/bazi/ziping/fulltext.md"
        self.write(self.file, "# 論救應\n\n官逢傷，而透印以解之。\n\n但須論其位置與力量。\n")
        self.write("references/inventory/paragraphs/bazi/ziping.json", {"fulltext": self.file, "paragraphs": [
            {"id": "ziping:L0003-L0003", "start_line": 3, "end_line": 3},
            {"id": "ziping:L0005-L0005", "start_line": 5, "end_line": 5},
        ]})
        self.rule = {"id": "ZPR-E-05", "art": "bazi", "theme": "透印救应", "school": "子平真诠", "paragraph_ids": ["ziping:L0003-L0003", "ziping:L0005-L0005"], "sources": [
            {"paragraph_id": "ziping:L0003-L0003", "start_line": 3, "end_line": 3, "quote": "官逢傷，而透印以解之。"},
            {"paragraph_id": "ziping:L0005-L0005", "start_line": 5, "end_line": 5, "quote": "但須論其位置與力量。"},
        ], "quote": "官逢傷，而透印以解之。\n[…]\n但須論其位置與力量。", "page": "geju", "required_facts": ["geju.name"], "when": {"geju.name": ["正官格"]}, "satisfy_when": "伤官透干且印透干", "fail_when": "无印", "unknown_when": "仅藏干", "rescue": "self", "vernacular": "透印只是救应候选。", "implementation_assumption": "未计算力量。", "verified": False}
        self.package = {"schema_version": "fateradar-executable-v2", "verified": False, "book": {"slug": "ziping", "system": "bazi", "title": "子平真诠", "fulltext": self.file}, "rules": [self.rule]}
        self.write_package()
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Evidence fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True, stderr=subprocess.DEVNULL)

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def write_package(self):
        self.write("references/executable/ziping.json", self.package)

    def test_separate_spans_keep_exact_quotes_and_pinned_plain_links(self):
        result = exporter.build_export(self.root)
        self.assertEqual(result["sourceRevision"], self.revision)
        rule = result["rules"][0]
        self.assertEqual(rule["id"], "ZPR-E-05")
        self.assertEqual(rule["chapter"], "論救應")
        self.assertEqual(len(rule["fragments"]), 2)
        self.assertEqual(rule["fragments"][0]["quote"], self.rule["sources"][0]["quote"])
        self.assertEqual(rule["fragments"][1]["quote"], self.rule["sources"][1]["quote"])
        self.assertEqual(rule["fragments"][1]["url"], f"https://github.com/linyuhanggg/fateradar-classics/blob/{self.revision}/{self.file}?plain=1#L5-L5")

    def test_uncommitted_source_cannot_be_attached_to_an_old_commit(self):
        self.write(self.file, "# 論救應\n\n未提交的新句。\n\n但須論其位置與力量。\n")
        self.rule["sources"][0]["quote"] = "未提交的新句。"
        self.rule["quote"] = "未提交的新句。\n[…]\n但須論其位置與力量。"
        self.write_package()
        with self.assertRaisesRegex(ValueError, "固定版本|commit|revision"):
            exporter.build_export(self.root, self.revision)

    def test_invalid_source_quote_blocks_export(self):
        self.rule["sources"][0]["quote"] = "没有在原文里的句子"
        self.write_package()
        with self.assertRaisesRegex(ValueError, "QUOTE|原文|校验"):
            exporter.build_export(self.root)

    def test_definitions_do_not_claim_execution_or_human_verification(self):
        result = exporter.build_export(self.root)
        self.assertEqual(result["kind"], "source-linked-rule-definitions")
        self.assertEqual(len(result["rules"]), 1)
        self.assertFalse(result["rules"][0]["verified"])
        self.assertNotIn("checkStatus", result["rules"][0])
        self.assertNotIn("matched", result["rules"][0])
        self.assertEqual(result["rules"][0]["when"], self.rule["when"])


if __name__ == "__main__":
    unittest.main()
