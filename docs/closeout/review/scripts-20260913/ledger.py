import json, glob, os, collections

C = '/Users/yuhanglin/fateradar-goal-20260912/classics'
files = sorted(glob.glob(C + '/references/annotations/**/*.json', recursive=True))
draft_files = 0
draft_entries = 0
for f in files:
    d = json.load(open(f))
    n = sum(1 for e in d.get('entries', []) if e.get('review') != 'source-reviewed')
    if n:
        draft_files += 1
        draft_entries += n
print('annotation files:', len(files), '| files containing draft:', draft_files, '| draft entries:', draft_entries)

led = json.load(open(C + '/docs/closeout/GAP_LEDGER.json'))
print()
print('GAP_LEDGER baselines:', json.dumps(led['baselines'], ensure_ascii=False)[:400])
print('GAP_LEDGER counts:', json.dumps(led['counts'], ensure_ascii=False)[:600])
print('GAP_LEDGER page_consumers:', json.dumps(led['page_consumers'], ensure_ascii=False)[:700])
print('drafts_by_file entries:', len(led['drafts_by_file']))
print('drafts_by_file sum:', sum((x.get('draft') or 0) for x in led['drafts_by_file']))
print('page_consumers keys:', list(led['page_consumers'].keys()))
print('GAP_LEDGER rules:', len(led['rules']))
