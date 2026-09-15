#!/usr/bin/env python3
"""Regression checks for the per-item draft disposition ledger."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "draft_disposition", Path(__file__).with_name("build-draft-disposition.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ROOT = Path(__file__).resolve().parents[1]


class DraftDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT / "docs/closeout/DRAFT_DISPOSITION_LEDGER.json").read_text())

    def test_every_draft_has_a_row(self):
        rows = self.ledger["rows"]
        self.assertEqual(len(rows), self.ledger["draftTotal"])
        self.assertTrue(rows, "ledger must not be empty")

    def test_rows_carry_evidence_and_source_identity(self):
        for row in self.ledger["rows"]:
            self.assertEqual(row["reviewStatus"], "draft")
            self.assertTrue(row["sourceId"])
            self.assertTrue(row["evidence"], f"{row['sourceId']} lacks classification evidence")
            self.assertTrue(row["sourceFile"], f"{row['sourceId']} lacks source file")
            self.assertFalse(row["verified"], "draft rows must not be marked verified")

    def test_category_counts_match_rows(self):
        from collections import Counter
        actual = Counter(r["category"] for r in self.ledger["rows"])
        self.assertEqual(dict(actual.most_common()), self.ledger["categoryCounts"])
        for cat in self.ledger["categoryCounts"]:
            self.assertIn(cat, self.ledger["categoryDefinitions"])

    def test_only_defined_categories_are_used(self):
        defined = set(self.ledger["categoryDefinitions"])
        used = {r["category"] for r in self.ledger["rows"]}
        self.assertTrue(used <= defined, f"undefined categories: {used - defined}")

    def test_lacuna_paragraphs_never_land_in_catalog_metadata(self):
        for row in self.ledger["rows"]:
            if row["signals"]["hasLacunaMarker"] or row["signals"]["hasFigureOrDoubt"]:
                self.assertEqual(row["category"], "figure_or_lacuna",
                                 f"{row['sourceId']} has a lacuna/figure signal but was filed as "
                                 f"{row['category']}")

    def test_metadata_rows_are_backed_by_a_metadata_signal(self):
        for row in self.ledger["rows"]:
            if row["category"] != "catalog_metadata":
                continue
            self.assertTrue(
                row["kind"] in module.METADATA_KINDS or "章题" in row["reason"] or "现代恢复" in row["reason"],
                f"{row['sourceId']} filed as catalog_metadata without a metadata signal")

    def test_ledger_head_is_a_real_commit(self):
        import subprocess
        recorded = self.ledger["head"]
        self.assertRegex(recorded, r"^[0-9a-f]{40}$")
        # The recorded HEAD must exist in this repository (an ancestor of the current
        # tip), so a ledger can never cite a fabricated or foreign revision.
        exists = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"{recorded}^{{commit}}"],
            capture_output=True, text=True).returncode == 0
        self.assertTrue(exists, f"recorded HEAD {recorded} is not a commit in this repository")
        ancestor = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", recorded, "HEAD"],
            capture_output=True, text=True).returncode == 0
        self.assertTrue(ancestor, f"recorded HEAD {recorded} is not an ancestor of HEAD")


if __name__ == "__main__":
    unittest.main()
