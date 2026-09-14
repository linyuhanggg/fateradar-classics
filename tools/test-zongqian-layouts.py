#!/usr/bin/env python3
"""Regression checks for source-backed table recovery and knowledge consumption."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from source_paragraphs import load_source_paragraphs

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'sources/normalized/san-shi/daliuren-daquan'

class ZongqianRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((BASE / 'siku-zongqian-cells.json').read_text())
        cls.cells = cls.data['cells']
        cls.sources = load_source_paragraphs(ROOT)
        cls.annotations = {e['paragraphId']: e for e in json.loads((ROOT / 'references/annotations/san-shi/daliuren-daquan--siku-zongqian-layouts.json').read_text())['entries']}

    def test_original_image_and_complete_grid(self):
        self.assertEqual(hashlib.sha256((ROOT / self.data['sourcePdf']).read_bytes()).hexdigest(), self.data['sourcePdfSha256'])
        self.assertEqual(len(self.cells), 120)
        self.assertEqual(len({c['cellId'] for c in self.cells}), 120)
        for page, stem in enumerate('甲乙丙丁戊己庚辛壬癸', 16):
            cells = [c for c in self.cells if c['page'] == page]
            self.assertEqual({c['headerBranch'] for c in cells}, set('子丑寅卯辰巳午未申酉戌亥'))
            self.assertTrue(all(c['headerStem'] == stem for c in cells))

    def test_every_group_reaches_exact_reviewed_paragraph(self):
        lines = (ROOT / self.data['sourcePath']).read_text().splitlines()
        for cell in self.cells:
            row = self.sources[cell['paragraphId']]
            self.assertEqual(row['source_status'], 'passage-reviewed')
            self.assertEqual(row['pdf_page'], cell['page'])
            self.assertEqual(self.annotations[cell['paragraphId']]['review'], 'source-reviewed')
            text = '\n'.join(lines[row['start_line']-1:row['end_line']])
            for group in cell['branches']:
                self.assertEqual(len(group['sequenceRaw']), 3)
                self.assertIn(f"{group['position']}小字「{group['labelRaw'] or '无'}」／三字串「{group['sequenceRaw']}」", text)

    def test_archive_does_not_turn_fragments_into_reviewed_rules(self):
        ledger = json.loads((ROOT / 'docs/closeout/evidence/t32-zongqian-recovery-20260914.json').read_text())
        legacy = {e['paragraphId']: e for e in json.loads((ROOT / 'references/annotations/san-shi/daliuren-daquan.json').read_text())['entries']}
        self.assertEqual(hashlib.sha256((ROOT / ledger['sourceFile']).read_bytes()).hexdigest(), ledger['sourceSha256'])
        self.assertEqual(len(ledger['items']), 664)
        for item in ledger['items']:
            entry = legacy[item['paragraphId']]
            self.assertEqual(entry['review'], 'draft')
            self.assertEqual(entry['kind'], '评注或元数据')
            self.assertEqual(entry['relatedParagraphIds'], [ledger['guideParagraphId']])
        self.assertEqual(set(self.annotations[ledger['guideParagraphId']]['relatedParagraphIds']), {c['paragraphId'] for c in self.cells})

if __name__ == '__main__':
    unittest.main()
