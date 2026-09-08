#!/usr/bin/env python3
"""Import saved Shidian original paragraphs without OCR or translation promotion."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def flatten(chapters):
    for chapter in chapters:
        yield chapter
        yield from flatten(chapter.get('subChapters', []))


def original_lines(paragraph):
    if paragraph['contentEncryptType'] != 0:
        raise ValueError(f"Encrypted paragraph: {paragraph['paragraphId']}")
    return json.loads(paragraph['content'])['lines']


def content_identity(paragraph):
    return [(line.get('content', ''), line.get('figure', {}).get('uri')) for line in original_lines(paragraph)]


def import_book(source: Path, root: Path, slug: str) -> dict:
    book = json.loads((source / 'book.json').read_text())['bookInfo']
    book_id = book['bookId']
    edition_id = f'shidian-{book_id}'
    relative = Path('sources/normalized/shidianguji') / book_id
    output = root / relative
    output.mkdir(parents=True, exist_ok=True)
    chapters = list(flatten(book['catalog']['chapters']))
    records = {}
    for path in sorted((source / 'chapters').glob('*.json')):
        for paragraph in json.loads(path.read_text())['paragraphs']:
            key = paragraph['paragraphId']
            if key in records and content_identity(records[key]) != content_identity(paragraph):
                raise ValueError(f'Conflicting source paragraph: {key}')
            records[key] = paragraph
    counts = Counter(p['chapterId'] for p in records.values())
    missing = [{'chapterId': c['chapterId'], 'expected': c['paragraphCount'], 'actual': counts[c['chapterId']]}
               for c in chapters if counts[c['chapterId']] != c['paragraphCount']]
    notes = ['识典现成原文字段，未采用网站译文；未完成逐字影印校勘。',
             '网站章节名与印本卷号可能不一致，引用卷号须以正文或影印核定。',
             '网页目录段落取齐不等于古本全帙无缺；同版子篇不计独立来源。']
    notes.append('本次仅收录部分章节，缺失范围见来源清单。' if missing else '本次段落数量与该站登记的各章目录一致。')
    lines = [f"# {book['bookName']}", '', f'> 来源：https://www.shidianguji.com/book/{book_id}', '',
             '> 识典原文字段转存；未经影印逐字校勘。网站章节名不直接等同印本卷号；图像保留占位，不伪装文字。', '']
    rows, figures, originals = [], [], []
    for chapter in chapters:
        title = ''.join(item['content'] for item in chapter['chapterName'])
        paragraphs = sorted((p for p in records.values() if p['chapterId'] == chapter['chapterId']), key=lambda p: p['inChapterOrder'])
        if not paragraphs:
            continue
        lines += [f'## 网站章节：{title}', '']
        for paragraph in paragraphs:
            body = []
            source_lines = original_lines(paragraph)
            for line in source_lines:
                if line.get('figure'):
                    body.append('〔此处为图像，未转文字；请对照本段原网页。〕')
                    figures.append({'paragraphId': paragraph['paragraphId'], 'chapterId': paragraph['chapterId'],
                                    'lineId': line['lineId'], 'uri': line['figure'].get('uri'),
                                    'upstreamUrl': f"https://www.shidianguji.com/book/{book_id}/chapter/{paragraph['chapterId']}"})
                if line.get('content', '').strip():
                    body.append(line['content'])
            if not body:
                body = ['〔源段仅含版面标记，无可转存文字。〕']
            start = len(lines) + 1
            lines.extend('\n'.join(body).splitlines())
            end = len(lines)
            rows.append({'id': f"{slug}:{edition_id}:P{paragraph['paragraphId']}",
                         'start_line': start, 'end_line': end, 'heading': f'网站章节：{title}',
                         'kind': '待分类', 'upstreamParagraphId': paragraph['paragraphId'],
                         'upstreamChapterId': paragraph['chapterId'],
                         'upstreamPageIds': list(dict.fromkeys([paragraph['startPageId'], paragraph['endPageId']])),
                         'upstreamUrl': f"https://www.shidianguji.com/book/{book_id}/chapter/{paragraph['chapterId']}",
                         'figureCount': sum(bool(line.get('figure')) for line in source_lines)})
            lines.append('')
            # Preserve actual source line types and page markers, excluding derived translations.
            originals.append({key: value for key, value in paragraph.items() if key != 'translateContent'})
    unknown = set(counts) - {c['chapterId'] for c in chapters}
    if unknown:
        raise ValueError(f'Paragraphs reference unknown chapters: {sorted(unknown)}')
    file = str(relative / 'text.md')
    index = str(relative / 'paragraphs.json')
    (root / file).write_text('\n'.join(lines) + '\n')
    (root / index).write_text(json.dumps({'sourceFile': file, 'paragraphs': rows}, ensure_ascii=False, indent=2) + '\n')
    (output / 'original-paragraphs.json').write_text(json.dumps(originals, ensure_ascii=False, indent=2) + '\n')
    (output / 'figures.json').write_text(json.dumps(figures, ensure_ascii=False, indent=2) + '\n')
    (output / 'book.json').write_text(json.dumps(book, ensure_ascii=False, indent=2) + '\n')
    edition = {'id': edition_id, 'bookSlug': slug, 'label': f"{book['bookName']} · 识典 {book_id} · 待校参考",
               'file': file, 'paragraphIndex': index, 'sourceStatus': 'reference-text', 'notes': notes,
               'upstreamBookId': book_id, 'upstreamVersion': book['version'],
               'catalogComplete': not missing, 'missingChapters': missing,
               'paragraphCount': len(rows), 'figureCount': len(figures)}
    (output / 'provenance.json').write_text(json.dumps(edition, ensure_ascii=False, indent=2) + '\n')
    return edition


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--slug', required=True)
    args = parser.parse_args()
    print(json.dumps(import_book(args.source, args.root, args.slug), ensure_ascii=False))


if __name__ == '__main__':
    main()
