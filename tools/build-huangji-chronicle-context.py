#!/usr/bin/env python3
"""Recover explicit coordinates and single-cell readings in chapters 13–24.

Candidate only. Do not infer rulers, eras, missing cells, or calendar dates.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

AXES = '日月星辰'
STEMS = '甲乙丙丁戊己庚辛壬癸'
BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
NUMBER = '[一二三四五六七八九十百千萬万零〇兩两]+'
COORD = re.compile(r'經([日月星辰])之([' + STEMS + BRANCHES + '])(' + NUMBER + r')$')
CELL = re.compile(r'([' + STEMS + '][' + BRANCHES + '])(' + NUMBER + r')?$')


def extract(lines, paragraphs, low=12743, high=20178):
    """Reset missing axes rather than carrying ambiguous parents forward."""
    state = {axis: None for axis in AXES}
    chapter = None
    parsed = {}
    for line_no in range(low, min(high, len(lines)) + 1):
        raw = lines[line_no - 1]
        body = re.sub(r'^\s*#{1,6}\s+', '', raw).strip()
        if '觀物篇' in body:
            chapter = {'line': line_no, 'raw': body}
            state = {axis: None for axis in AXES}
        match = COORD.fullmatch(body)
        if match:
            axis, label, number = match.groups()
            index = AXES.index(axis)
            state[axis] = {'line': line_no, 'raw': body, 'axis': axis,
                           'labelRaw': label, 'numberRaw': number}
            for child in AXES[index + 1:]:
                state[child] = None
            parsed[line_no] = {'type': 'coordinate', 'chapter': chapter,
                               'node': state[axis], 'parents': state.copy()}
        else:
            # An unparsed coordinate-like line is a barrier, not permission
            # to associate the following entries with the preceding ruler/table.
            for axis in AXES:
                if '經' + axis + '之' in body:
                    for child in AXES[AXES.index(axis):]:
                        state[child] = None
            cell = CELL.fullmatch(body)
            if cell:
                parsed[line_no] = {'type': 'single-cell', 'chapter': chapter,
                                   'ganzhiRaw': cell[1], 'numberRaw': cell[2],
                                   'parents': state.copy()}
    candidates, deferred = [], []
    for paragraph in paragraphs:
        start, end = paragraph['start_line'], paragraph['end_line']
        if start < low or end > high:
            continue
        raw = '\n'.join(lines[start - 1:end])
        item = parsed.get(start)
        if start != end or item is None:
            deferred.append({'paragraphId': paragraph['id'], 'startLine': start,
                             'endLine': end, 'sourceRaw': raw,
                             'reason': 'not-one-explicit-coordinate-or-single-cell'})
            continue
        axes = AXES[:AXES.index(item['node']['axis']) + 1] if item['type'] == 'coordinate' else AXES
        missing = [a for a in axes if item['parents'][a] is None]
        unusual = [a for a in axes if item['parents'][a] and
                   item['parents'][a]['labelRaw'] not in (STEMS if a in '日星' else BRANCHES)]
        parent_text = '；'.join(item['parents'][a]['raw'] + '（L' + str(item['parents'][a]['line']) + '）'
                               for a in axes if item['parents'][a])
        if item['type'] == 'coordinate':
            description = '本项原列“' + item['node']['raw'] + '”，是本表的' + item['node']['axis'] + '层标签与数词。'
        else:
            description = '本格原列干支“' + item['ganzhiRaw'] + '”'
            description += ('，后接数词“' + item['numberRaw'] + '”。') if item['numberRaw'] else '，没有附数词。'
        description += '其明确所在层级为：' + (parent_text or '本段以前未取得完整明确标签') + '。'
        description += '仅释读原表标签、干支及数词，不据邻格推算帝王在位年、公历年份或补齐表列。'
        flags = (['missing-explicit-parent:' + ''.join(missing)] if missing else [])
        flags += ['unusual-axis-label:' + ''.join(unusual)] if unusual else []
        candidates.append({'paragraphId': paragraph['id'], 'startLine': start,
                           'sourceRaw': raw, 'parsed': item, 'flags': flags,
                           'proposedReview': 'draft' if flags else 'source-reviewed',
                           'entry': {'paragraphId': paragraph['id'], 'kind': '理论',
                                     'vernacular': description, 'terms': [],
                                     'notes': ['仅恢复现有电子文本明确可见的表项与层级；尚未作影印逐字校勘，也未把原表年代与历史事实等同。'] +
                                              (['不完整或异常层级保留待核：' + '；'.join(flags)] if flags else []),
                                     'review': 'draft', 'verified': False}})
    return candidates, deferred


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = root / 'sources/fulltext/divination/huangji-jingshi/fulltext.md'
    paragraphs = json.loads((root / 'references/inventory/paragraphs/divination/huangji-jingshi.json').read_text())['paragraphs']
    existing = json.loads((root / 'references/annotations/divination/huangji-jingshi.json').read_text())['entries']
    known = {e['paragraphId'] for e in existing}
    candidates, deferred = extract(source.read_text().splitlines(), [p for p in paragraphs if p['id'] not in known])
    result = {'sourceFile': str(source.relative_to(root)), 'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'scope': 'Only unannotated explicit single cells/coordinates of chapters 13–24; all output draft pending independent review',
              'candidates': candidates, 'deferred': deferred}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'candidates': len(candidates), 'deferred': len(deferred),
                      'eligibleForReview': sum(not c['flags'] for c in candidates)}))


if __name__ == '__main__':
    main()
