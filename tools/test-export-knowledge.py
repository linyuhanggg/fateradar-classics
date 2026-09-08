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
        self.write_json("references/inventory/paragraphs/bazi/book.json", {"fulltext": "sources/fulltext/bazi/book/fulltext.md", "paragraphs": [{"id": "book:L0001-L0002", "start_line": 1, "end_line": 2, "heading": "章节", "kind": "理论"}]})

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
        self.write_json("references/inventory/paragraphs/bazi/book.json", {"fulltext": "sources/fulltext/bazi/book/fulltext.md", "paragraphs": [{"id": "book:L0001-L0002", "start_line": 1, "end_line": 2, "heading": "得時不旺", "kind": "理论"}]})
        row = module.build_export(self.root, "commit")["paragraphs"][0]
        self.assertIn("得时不旺", row["searchText"])
        self.assertEqual(row["heading"], "得時不旺")

    def test_navigation_only_source_is_not_presented_as_full_text(self):
        self.write_json("references/source-quality.json", {"version": 1, "books": [{"slug": "book", "status": "navigation-only", "notes": ["仅导航，正文恢复中"]}]})
        book = module.build_export(self.root, "commit")["books"][0]
        self.assertEqual(book["textStatus"], "navigation-only")
        self.assertEqual(book["sourceNotes"], ["仅导航，正文恢复中"])

    def test_supplement_retains_own_file_and_ocr_draft_status(self):
        self.write("sources/recovered.md", "## PDF第021页\n\n待校OCR正文\n")
        self.write_json("references/source-editions.json", {"version": 1, "editions": [{"id": "recovery", "bookSlug": "book", "system": "bazi", "label": "影印初稿", "file": "sources/recovered.md", "sourceStatus": "ocr-draft", "pageScoped": True, "notes": ["尚待校核"]}]})
        data = module.build_export(self.root, "commit")
        original, draft = data["paragraphs"]
        self.assertEqual(original["id"], "book:L0001-L0002")
        self.assertEqual(draft["sourceFile"], "sources/recovered.md")
        self.assertEqual(draft["sourceStatus"], "ocr-draft")
        self.assertEqual(draft["review"], "unreviewed")
        self.assertEqual(draft["pdfPage"], 21)
        self.assertEqual(data["books"][0]["paragraphCount"], 2)

    def test_research_book_and_upstream_reference_are_searchable_without_promotion(self):
        self.write("sources/candidate.md", "待校新原文\n")
        self.write_json("sources/candidate-index.json", {"sourceFile": "sources/candidate.md", "paragraphs": [{"id": "candidate:shidian-HY2:P200", "start_line": 1, "end_line": 1, "heading": "网站卷名待核", "kind": "待分类", "upstreamUrl": "https://www.shidianguji.com/book/HY2/chapter/c", "figureCount": 1}]})
        self.write_json("references/source-editions.json", {"books": [{"slug": "candidate", "title": "候选新书", "system": "san-shi", "fulltext": "sources/candidate.md", "textStatus": "unassessed", "sourceNotes": ["仅供研究，不作为算法依据"]}], "editions": [{"id": "shidian-HY2", "bookSlug": "candidate", "label": "新版本待校", "file": "sources/candidate.md", "paragraphIndex": "sources/candidate-index.json", "sourceStatus": "reference-text", "notes": ["未逐字校勘"]}]})
        result = module.build_export(self.root, "fixed")
        self.assertEqual(len(result["books"]), 2)
        row = next(p for p in result["paragraphs"] if p["bookSlug"] == "candidate")
        self.assertEqual(row["review"], "unreviewed")
        self.assertEqual(row["sourceStatus"], "reference-text")
        self.assertEqual(row["upstreamUrl"], "https://www.shidianguji.com/book/HY2/chapter/c")
        self.assertEqual(row["figureCount"], 1)
        self.assertNotIn("vernacular", row)
        self.assertEqual(result["books"][1]["textStatus"], "unassessed")

    def test_mixed_work_attribution_survives_without_rewriting_container_or_quote(self):
        attribution = {"work": "另一部书", "relation": "mixed-in", "note": "当前收录文件混入此书正文。"}
        self.write_json("references/annotations/bazi/book.json", {"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0002", "kind": "重复", "vernacular": "这一段来自另一部书。", "terms": [], "notes": [], "review": "source-reviewed", "sourceAttribution": attribution}]})
        result = module.build_export(self.root, "fixed")
        row = result["paragraphs"][0]
        self.assertEqual(row["sourceAttribution"], attribution)
        self.assertEqual(row["bookSlug"], "book")
        self.assertEqual(row["text"], "原文第一行\n原文第二行")
        self.assertIn("另一部書", row.get("searchText", ""))

    def test_reviewed_subsections_export_exact_lines_without_inflating_source_count(self):
        self.write_json("references/annotations/bazi/book.json", {"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0002", "kind": "理论", "vernacular": "整段解释", "terms": [], "notes": [], "review": "source-reviewed", "subsections": [{"id": "S001", "title": "傷官", "startLine": 2, "endLine": 2, "vernacular": "子节说明", "terms": [], "notes": ["保留条件"]}]}]})
        data = module.build_export(self.root, "fixed")
        self.assertEqual(data["books"][0]["paragraphCount"], 1)
        self.assertEqual(len(data["paragraphs"]), 1)
        part = data["paragraphs"][0]["subsections"][0]
        self.assertEqual(part["id"], "S001")
        self.assertEqual(part["text"], "原文第二行")
        self.assertIn("伤官", part["searchText"])

    def test_bad_annotation_fails_export(self):
        self.write_json("references/annotations/bazi/book.json", {"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0009"}]})
        with self.assertRaisesRegex(ValueError, "unknown paragraphId"):
            module.build_export(self.root, "commit")


if __name__ == "__main__":
    unittest.main()
