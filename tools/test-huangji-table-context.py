#!/usr/bin/env python3
"""Check source fidelity and prevent malformed tables acquiring review status."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HuangjiTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        out = Path(cls.temp.name) / 'table.json'
        ann = Path(cls.temp.name) / 'annotations.json'
        subprocess.run([sys.executable, str(ROOT / 'tools/build-huangji-table-context.py'),
                        '--output', str(out), '--annotations-output', str(ann),
                        '--reviewed-literal'], check=True, capture_output=True)
        cls.data = json.loads(out.read_text())
        cls.entries = {e['paragraphId']: e for e in json.loads(ann.read_text())['entries']}
        cls.dispositions = {p['paragraphId']: p for p in cls.data['paragraphDispositions']}
        cls.source = (ROOT / cls.data['sourceFile']).read_text()
        cls.inventory = json.loads((ROOT / 'references/inventory/paragraphs/divination/huangji-jingshi.json').read_text())['paragraphs']

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_every_coordinate_has_exact_source_and_paragraph(self):
        self.assertEqual(hashlib.sha256(self.source.encode()).hexdigest(), self.data['sourceSha256'])
        for row in self.data['rows']:
            for node in row['coordinates'].values():
                if node is None:
                    continue
                self.assertEqual(self.source[node['sourceStartOffset']:node['sourceEndOffset']], node['sourceExcerpt'])
                self.assertGreaterEqual(node['labelLine'], row['chapter']['line'])
                self.assertTrue(node['sourceExcerpt'].startswith(node['labelRaw']))
                self.assertIn('〔' + node['countRaw'] + '〕', node['sourceExcerpt'])
            leaf = row['coordinates']['辰']
            expected = {p['id'] for p in self.inventory if p['start_line'] <= leaf['countEndLine'] and p['end_line'] >= leaf['countStartLine']}
            self.assertEqual(expected, set(row['sourceParagraphIds']))

    def test_corrupt_parent_is_not_inherited(self):
        broken = [r for r in self.data['rows'] if 'invalid-parent-unparsed' in r['flags']]
        self.assertEqual(len(broken), 7)
        for row in broken:
            self.assertIsNone(row['coordinates']['星'])
            self.assertIn('星己辰', str(row['invalidParentEvidence']))
            for pid in row['sourceParagraphIds']:
                self.assertEqual(self.entries[pid]['review'], 'draft')
        recovered = next(r for r in self.data['rows'] if r['coordinates']['星'] and r['coordinates']['星']['labelLine'] == 12596)
        self.assertEqual(recovered['coordinates']['星']['labelRaw'], '星庚')
        self.assertEqual(recovered['coordinates']['星']['countRaw'], '三百五十七')

    def test_numeral_anomalies_and_mixed_paragraphs_remain_draft(self):
        for pid in ['huangji-jingshi:L1368-L1368', 'huangji-jingshi:L3244-L3244',
                    'huangji-jingshi:L6615-L6615', 'huangji-jingshi:L9037-L9037',
                    'huangji-jingshi:L1124-L1125']:
            self.assertFalse(self.dispositions[pid]['eligibleForLiteralReview'])
            self.assertEqual(self.entries[pid]['review'], 'draft')
        first = self.entries['huangji-jingshi:L0047-L0047']
        self.assertEqual(first['review'], 'source-reviewed')
        self.assertIn('日甲〔一〕 → 月子〔一〕 → 星甲〔一〕 → 辰子〔一〕', first['vernacular'])
        for pid, e in self.entries.items():
            self.assertFalse(e['verified'])
            if e['review'] == 'source-reviewed':
                p = self.dispositions[pid]
                self.assertTrue(p['rowIds'])
                self.assertEqual(p['flags'], [])
                self.assertEqual(p['unparsedRaw'], '')

    def test_default_candidate_never_self_approves(self):
        with tempfile.TemporaryDirectory() as td:
            out, ann = Path(td)/'data.json', Path(td)/'annotations.json'
            subprocess.run([sys.executable, str(ROOT/'tools/build-huangji-table-context.py'),
                            '--output', str(out), '--annotations-output', str(ann)],
                           check=True, capture_output=True)
            self.assertTrue(all(e['review'] == 'draft' for e in json.loads(ann.read_text())['entries']))


if __name__ == '__main__':
    unittest.main()
