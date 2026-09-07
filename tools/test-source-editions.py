#!/usr/bin/env python3
import importlib.util
import unittest
import json
import tempfile
from pathlib import Path
from source_paragraphs import split_edition, load_source_paragraphs

spec = importlib.util.spec_from_file_location("annotations", Path(__file__).with_name("validate-annotations.py"))
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)

class SourceEditions(unittest.TestCase):
    def setUp(self):
        self.edition = {"id": "nlc-recovery", "bookSlug": "book", "label": "初识稿", "file": "sources/ocr.md", "sourceStatus": "ocr-draft", "pageScoped": True}

    def test_correction_on_prior_pdf_page_does_not_move_next_page_id(self):
        before = split_edition(self.edition, ["## PDF第001页", "", "前页", "", "## PDF第002页", "", "后页"])
        after = split_edition(self.edition, ["## PDF第001页", "", "前页", "拆回第二列", "", "## PDF第002页", "", "后页"])
        self.assertEqual(before[-1]["id"], after[-1]["id"])
        self.assertNotEqual(before[-1]["start_line"], after[-1]["start_line"])
        self.assertEqual(before[-1]["pdf_page"], 2)

    def test_editions_have_distinct_ids_even_at_same_line_numbers(self):
        a = split_edition(self.edition, ["内容"])
        b = split_edition({**self.edition, "id": "other"}, ["内容"])
        self.assertNotEqual(a[0]["id"], b[0]["id"])

    def test_only_fully_reviewed_page_is_upgraded(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "sources").mkdir()
            (root / "references").mkdir()
            (root / "sources/ocr.md").write_text("## PDF第021页\n\n第一页\n\n## PDF第022页\n\n第二页\n")
            (root / "sources/reviews.json").write_text(json.dumps({"sourcePath": "sources/ocr.md", "pages": [{"pdfPage": 21, "status": "partial", "unresolved": ["疑字"]}, {"pdfPage": 22, "status": "source-reviewed", "unresolved": [], "scope": "全页转写"}]}))
            (root / "references/source-editions.json").write_text(json.dumps({"editions": [{**self.edition, "pageReviews": "sources/reviews.json"}]}))
            rows = list(load_source_paragraphs(root).values())
            self.assertEqual([row["source_status"] for row in rows], ["ocr-draft", "page-reviewed"])
            self.assertIn("全页转写", rows[1]["source_notes"])

    def test_ocr_annotation_cannot_be_promoted_by_semantic_review(self):
        row = split_edition(self.edition, ["未校正文"])[0]
        data = {"bookSlug": "book", "entries": [{"paragraphId": row["id"], "kind": "理论", "vernacular": "OCR解释", "terms": [], "notes": [], "review": "source-reviewed"}]}
        self.assertTrue(any("OCR" in error for error in validation.validate_pack(data, {row["id"]: row})))
        data["entries"][0]["review"] = "draft"
        self.assertEqual(validation.validate_pack(data, {row["id"]: row}), [])

if __name__ == "__main__":
    unittest.main()
