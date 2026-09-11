#!/usr/bin/env python3
"""Content revision must refer to the same committed notes and source text."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("export-reading-notes.py")

class ReadingExportChecks(unittest.TestCase):
    def fixture(self, folder, quote="原文"):
        root = Path(folder)
        (root / "tools").mkdir()
        shutil.copyfile(SCRIPT, root / "tools/export-reading-notes.py")
        (root / "references/readings").mkdir(parents=True)
        (root / "source.md").write_text("原文\n")
        data = {"version": 1, "notes": [{"id": "example", "art": "meihua", "title": "读法", "body": "白话", "source": {"kind": "anchored_text", "title": "书", "anchor": {"file": "source.md", "startLine": 1, "endLine": 1}, "quote": quote}, "verified": False}]}
        (root / "references/readings/chart-notes.json").write_text(json.dumps(data, ensure_ascii=False))
        def git(*args):
            return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "source")
        return root, git("rev-parse", "HEAD")

    def test_pending_text_does_not_acquire_old_revision(self):
        with tempfile.TemporaryDirectory() as folder:
            root, revision = self.fixture(folder)
            (root / "source.md").write_text("插入一行\n原文\n")
            result = subprocess.run(["python3", "tools/export-reading-notes.py"], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "dist/readings/chart-notes.json").read_text())
            self.assertEqual(data["sourceRevision"], revision)
            self.assertEqual(data["notes"][0]["source"]["quote"], "原文")
            self.assertEqual(data["notes"][0]["source"]["anchor"]["startLine"], 1)

    def test_bad_committed_quote_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root, _ = self.fixture(folder, quote="不是原文")
            result = subprocess.run(["python3", "tools/export-reading-notes.py"], cwd=root, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Quote mismatch", result.stderr)

if __name__ == "__main__":
    unittest.main()
