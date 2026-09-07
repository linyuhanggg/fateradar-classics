#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path
from source_paragraphs import split_edition

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

    def test_ocr_annotation_cannot_be_promoted_by_semantic_review(self):
        row = split_edition(self.edition, ["未校正文"])[0]
        data = {"bookSlug": "book", "entries": [{"paragraphId": row["id"], "kind": "理论", "vernacular": "OCR解释", "terms": [], "notes": [], "review": "source-reviewed"}]}
        self.assertTrue(any("OCR" in error for error in validation.validate_pack(data, {row["id"]: row})))
        data["entries"][0]["review"] = "draft"
        self.assertEqual(validation.validate_pack(data, {row["id"]: row}), [])

if __name__ == "__main__":
    unittest.main()
