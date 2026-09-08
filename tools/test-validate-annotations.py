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

    def test_attribution_requires_actual_work_relation_and_explanation(self):
        entry = self.data["entries"][0]
        entry["sourceAttribution"] = {"work": "", "relation": "guess", "note": ""}
        self.assertTrue(any("sourceAttribution" in e for e in module.validate_pack(self.data, self.paragraphs)))
        entry["sourceAttribution"] = {"work": "撼龙经", "relation": "mixed-in", "note": "主文件混入另一书正文，保留容器出处。"}
        self.assertEqual(module.validate_pack(self.data, self.paragraphs), [])

    def test_named_work_in_an_anthology_is_not_forced_to_be_misfiled(self):
        self.data["entries"][0]["sourceAttribution"] = {"work": "相儿经", "relation": "anthology", "note": "图书集成相术部所收篇目。"}
        self.assertEqual(module.validate_pack(self.data, self.paragraphs), [])

    def test_subsections_cannot_escape_parent_or_duplicate_identity(self):
        entry = self.data["entries"][0]
        entry["subsections"] = [{"id": "S001", "title": "子节", "startLine": 1, "endLine": 4, "vernacular": "具体解释", "terms": [], "notes": []}]
        self.paragraphs[entry["paragraphId"]] = {"start_line": 1, "end_line": 2}
        self.assertTrue(any("subsection" in e for e in module.validate_pack(self.data, self.paragraphs)))
        entry["subsections"][0]["endLine"] = 2
        self.assertEqual(module.validate_pack(self.data, self.paragraphs), [])
        entry["subsections"].append(copy.deepcopy(entry["subsections"][0]))
        self.assertTrue(any("subsection" in e for e in module.validate_pack(self.data, self.paragraphs)))

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

    def test_book_count_does_not_count_multiple_editions_as_multiple_books(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in ("primary.json", "recovery.json"):
                (Path(folder) / name).write_text(json.dumps(self.data))
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("validate-annotations.py")), "--annotations", folder, "--json"], capture_output=True, text=True)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["books"], 1)
            self.assertEqual(receipt["files"], 2)
            self.assertTrue(any("across files" in e for e in receipt["errors"]))

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
