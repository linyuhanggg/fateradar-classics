#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("export_knowledge", Path(__file__).with_name("export-knowledge.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class KnowledgeExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("sources/fulltext/bazi/book/fulltext.md", "原文第一行\n原文第二行\n")
        self.write_json("references/inventory/library-inventory.json", {"packs": [{"fulltext_exists": True, "destination": "engine", "slug": "book", "system": "bazi", "title": "测试底本", "actual_fulltext_path": "sources/fulltext/bazi/book/fulltext.md"}]})
        self.write_json("references/inventory/paragraphs/bazi/book.json", {"paragraphs": [{"id": "book:L0001-L0002", "start_line": 1, "end_line": 2, "heading": "章节", "kind": "理论"}]})

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def write_json(self, name, data):
        self.write(name, json.dumps(data, ensure_ascii=False))

    def test_unreviewed_source_is_not_promoted(self):
        result = module.build_export(self.root, "source-commit")
        row = result["paragraphs"][0]
        self.assertEqual(row["text"], "原文第一行\n原文第二行")
        self.assertEqual(row["review"], "unreviewed")
        self.assertNotIn("vernacular", row)
        self.assertEqual(result["sourceRevision"], "source-commit")
        self.assertEqual(result["books"][0]["textStatus"], "unassessed")

    def test_annotation_is_joined_by_real_id(self):
        entry = {"paragraphId": "book:L0001-L0002", "kind": "规则候选", "vernacular": "这是已核对的具体白话。", "terms": ["术语"], "notes": ["例外待核"], "review": "source-reviewed"}
        self.write_json("references/annotations/bazi/book.json", {"bookSlug": "book", "entries": [entry]})
        row = module.build_export(self.root, "commit")["paragraphs"][0]
        self.assertEqual(row["vernacular"], entry["vernacular"])
        self.assertEqual(row["notes"], ["例外待核"])
        self.assertEqual(row["text"], "原文第一行\n原文第二行")

    def test_traditional_and_simplified_search_preserves_source(self):
        self.write("sources/fulltext/bazi/book/fulltext.md", "傷官與財印\n伤官与财印\n")
        row = module.build_export(self.root, "commit")["paragraphs"][0]
        self.assertEqual(row["text"], "傷官與財印\n伤官与财印")
        self.assertIn("伤官与财印", row["searchText"])
        self.assertIn("傷官與財印", row["searchText"])

    def test_heading_is_included_in_character_conversion(self):
        self.write_json("references/inventory/paragraphs/bazi/book.json", {"paragraphs": [{"id": "book:L0001-L0002", "start_line": 1, "end_line": 2, "heading": "得時不旺", "kind": "理论"}]})
        row = module.build_export(self.root, "commit")["paragraphs"][0]
        self.assertIn("得时不旺", row["searchText"])
        self.assertEqual(row["heading"], "得時不旺")

    def test_navigation_only_source_is_not_presented_as_full_text(self):
        self.write_json("references/source-quality.json", {"version": 1, "books": [{"slug": "book", "status": "navigation-only", "notes": ["仅导航，正文恢复中"]}]})
        book = module.build_export(self.root, "commit")["books"][0]
        self.assertEqual(book["textStatus"], "navigation-only")
        self.assertEqual(book["sourceNotes"], ["仅导航，正文恢复中"])

    def test_bad_annotation_fails_export(self):
        self.write_json("references/annotations/bazi/book.json", {"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0009"}]})
        with self.assertRaisesRegex(ValueError, "unknown paragraphId"):
            module.build_export(self.root, "commit")


if __name__ == "__main__":
    unittest.main()
