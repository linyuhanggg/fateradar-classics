#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('import_shidian', Path(__file__).with_name('import-shidian.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ImportShidian(unittest.TestCase):
    def fixture(self, root):
        folder = root / 'input/HY1'
        (folder / 'chapters').mkdir(parents=True)
        info = {'bookId': 'HY1', 'bookName': '測試書', 'version': 3, 'totalPage': 2, 'catalog': {'chapters': [
            {'chapterId': 'a', 'chapterName': [{'content': '卷一'}], 'paragraphCount': 1, 'subChapters': []},
            {'chapterId': 'b', 'chapterName': [{'content': '卷二'}], 'paragraphCount': 1, 'subChapters': []}]}}
        (folder / 'book.json').write_text(json.dumps({'bookInfo': info}))
        def paragraph(id, chapter, lines):
            return {'paragraphId': id, 'chapterId': chapter, 'inChapterOrder': 1,
                    'startPageId': 'paper-1', 'endPageId': 'paper-2', 'volumeVersion': 7,
                    'contentEncryptType': 0, 'content': json.dumps({'lines': lines}),
                    'translateContent': '不能导入的自动译文'}
        a = paragraph('100', 'a', [{'lineId': '1', 'lineType': 1, 'content': '陰陽原字，不改。'}])
        b = paragraph('200', 'b', [{'lineId': '2', 'lineType': 2, 'content': '夾注原字'},
                                 {'lineId': '3', 'lineType': 5, 'content': '', 'figure': {'uri': 'source/figure.webp'}}])
        (folder / 'chapters/a.json').write_text(json.dumps({'paragraphs': [a, b]}))
        (folder / 'chapters/b.json').write_text(json.dumps({'paragraphs': [b]}))
        return folder

    def test_upstream_ids_deduplicate_parent_child_and_preserve_text_and_figures(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = self.fixture(root)
            result = module.import_book(source, root, 'book')
            rows = json.loads((root / result['paragraphIndex']).read_text())['paragraphs']
            text = (root / result['file']).read_text()
            self.assertEqual([r['id'] for r in rows], ['book:shidian-HY1:P100', 'book:shidian-HY1:P200'])
            self.assertIn('陰陽原字，不改。', text)
            self.assertNotIn('不能导入的自动译文', text)
            self.assertIn('图像，未转文字', text)
            self.assertEqual(rows[1]['upstreamParagraphId'], '200')
            self.assertEqual(rows[1]['upstreamPageIds'], ['paper-1', 'paper-2'])
            self.assertEqual(result['sourceStatus'], 'reference-text')
            self.assertTrue(result['catalogComplete'])
            lines = text.splitlines()
            self.assertEqual(lines[rows[0]['start_line']-1:rows[0]['end_line']], ['陰陽原字，不改。'])

    def test_prior_paragraph_growth_changes_line_anchor_not_next_upstream_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = self.fixture(root)
            before = module.import_book(source, root, 'book')
            first = json.loads((root / before['paragraphIndex']).read_text())['paragraphs']
            path = source / 'chapters/a.json';data = json.loads(path.read_text())
            content = json.loads(data['paragraphs'][0]['content'])
            content['lines'].append({'lineId': '4', 'lineType': 1, 'content': '前段新增原行'})
            data['paragraphs'][0]['content'] = json.dumps(content);path.write_text(json.dumps(data))
            after = module.import_book(source, root, 'book')
            second = json.loads((root / after['paragraphIndex']).read_text())['paragraphs']
            self.assertEqual(first[1]['id'], second[1]['id'])
            self.assertNotEqual(first[1]['start_line'], second[1]['start_line'])

    def test_partial_catalog_is_recorded_not_promoted_to_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = self.fixture(root)
            (source / 'chapters/b.json').unlink()
            path = source / 'chapters/a.json';data=json.loads(path.read_text());data['paragraphs']=data['paragraphs'][:1];path.write_text(json.dumps(data))
            result = module.import_book(source, root, 'book')
            self.assertFalse(result['catalogComplete'])
            self.assertEqual(result['missingChapters'][0]['chapterId'], 'b')

    def test_conflicting_text_for_same_source_id_cannot_be_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = self.fixture(root)
            path=source / 'chapters/b.json';data=json.loads(path.read_text());content=json.loads(data['paragraphs'][0]['content']);content['lines'][0]['content']='另一段文字';data['paragraphs'][0]['content']=json.dumps(content);path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'Conflicting.*200'):
                module.import_book(source, root, 'book')

if __name__ == '__main__':
    unittest.main()
