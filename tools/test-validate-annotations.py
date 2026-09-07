#!/usr/bin/env python3
import copy
import json
import subprocess
import sys
import tempfile
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("annotations", Path(__file__).with_name("validate-annotations.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AnnotationValidation(unittest.TestCase):
    def setUp(self):
        self.paragraphs = {"book:L0001-L0002": {}, "book:L0004-L0004": {}}
        self.data = {"bookSlug": "book", "entries": [{"paragraphId": "book:L0001-L0002", "kind": "理论", "vernacular": "季节还需结合根气判断。", "terms": ["月令"], "notes": [], "review": "source-reviewed"}]}

    def test_real_reference(self):
        self.assertEqual(module.validate_pack(self.data, self.paragraphs), [])

    def test_invented_line_range_is_not_a_paragraph(self):
        self.data["entries"][0]["paragraphId"] = "book:L0001-L0004"
        self.assertTrue(any("unknown paragraphId" in x for x in module.validate_pack(self.data, self.paragraphs)))

    def test_duplicate_dispositions_are_rejected(self):
        self.data["entries"].append(copy.deepcopy(self.data["entries"][0]))
        self.assertTrue(any("duplicate" in x for x in module.validate_pack(self.data, self.paragraphs)))

    def test_empty_explanation_is_not_completed_work(self):
        self.data["entries"][0]["vernacular"] = " "
        self.assertTrue(any("nonempty explanation" in x for x in module.validate_pack(self.data, self.paragraphs)))

    def test_review_does_not_promote_verified(self):
        self.data["entries"][0]["verified"] = True
        self.assertTrue(any("human verified" in x for x in module.validate_pack(self.data, self.paragraphs)))

    def test_cli_checks_a_single_file_instead_of_succeeding_on_zero_files(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "annotation.json"
            path.write_text(json.dumps(self.data))
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("validate-annotations.py")), "--annotations", str(path), "--json"], capture_output=True, text=True)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["books"], 1)
            self.assertEqual(receipt["entries"], 1)
            self.assertFalse(receipt["ok"])  # fixture book is absent from the real library
            self.assertEqual(result.returncode, 1)

    def test_empty_directory_is_not_an_acceptance_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("validate-annotations.py")), "--annotations", folder, "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)["ok"])

    def test_related_references_must_resolve(self):
        self.data["entries"][0]["relatedParagraphIds"] = ["other:L0001-L0001"]
        self.assertTrue(any("related paragraph" in x for x in module.validate_pack(self.data, self.paragraphs)))


if __name__ == "__main__":
    unittest.main()
