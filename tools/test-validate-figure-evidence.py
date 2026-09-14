#!/usr/bin/env python3
"""Regression checks for cross-paragraph evidence leakage and false completion."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("figure_check", Path(__file__).with_name("validate-figure-evidence.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
READ = Path.read_text


class FigureEvidenceTests(unittest.TestCase):
    def evaluate(self, mutation):
        def altered(path, *args, **kwargs):
            value = READ(path, *args, **kwargs)
            if path.name in {"figure-transcriptions.json", "mayi-shenxiang--shidian-NGJ89241199903149974518.json"}:
                data = json.loads(value)
                mutation(path.name, data)
                return json.dumps(data, ensure_ascii=False)
            return value
        with patch.object(Path, "read_text", altered):
            return module.validate(module.ROOT)

    def test_actual_evidence_is_connected(self):
        self.assertTrue(module.validate(module.ROOT)["ok"])

    def test_existing_figure_cannot_attach_to_another_paragraph(self):
        def mutation(name, data):
            if name.startswith("mayi-shenxiang"):
                owner = next(e for e in data["entries"] if e.get("figureEvidenceIds"))
                other = next(e for e in data["entries"] if e["paragraphId"] != owner["paragraphId"])
                other["figureEvidenceIds"] = owner["figureEvidenceIds"]
        errors = self.evaluate(mutation)["errors"]
        self.assertTrue(any("belongs to" in e for e in errors), errors)

    def test_empty_caption_cannot_be_transcribed(self):
        def mutation(name, data):
            if name == "figure-transcriptions.json":
                data["entries"][0].update(captionTranscription="", textStatus="transcribed")
        errors = self.evaluate(mutation)["errors"]
        self.assertTrue(any("must not be empty" in e for e in errors), errors)

    def test_changed_source_image_cannot_retain_review_hash(self):
        def mutation(name, data):
            if name == "figure-transcriptions.json":
                data["entries"][0]["sha256"] = "0" * 64
        errors = self.evaluate(mutation)["errors"]
        self.assertTrue(any("hash mismatch" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
