import json, subprocess

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
raw = subprocess.run(['git', '-C', P, 'show', '00e98fc:docs/implementation/art-verdict-judgment-gap-matrix.json'],
                     capture_output=True, text=True, check=True).stdout
cap = json.loads(raw)
mine = json.load(open('/Users/yuhanglin/fateradar-goal-20260912/classics/docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.json'))

for k in ['product_head', 'classics_head', 'generated_at', 'generated_by']:
    print(k, '| captain:', cap.get(k), '| mine:', mine.get(k))
print()
cs, ms = cap['summary'], mine['summary']
diffkeys = [k for k in set(cs) | set(ms) if json.dumps(cs.get(k), sort_keys=True) != json.dumps(ms.get(k), sort_keys=True)]
print('summary keys differing:', diffkeys)
for k in diffkeys:
    print('  ', k, '| captain:', json.dumps(cs.get(k), ensure_ascii=False)[:200])
    print('  ', ' ' * len(k), '| mine   :', json.dumps(ms.get(k), ensure_ascii=False)[:200])
ci = {r['id']: r for r in cap['rows']}
mi = {r['id']: r for r in mine['rows']}
print('ids equal:', set(ci) == set(mi), len(ci))
rowdiff = [i for i in ci if json.dumps(ci[i], sort_keys=True) != json.dumps(mi.get(i), sort_keys=True)]
print('rows differing:', len(rowdiff), rowdiff[:10])
for i in rowdiff[:2]:
    for f in sorted(set(ci[i]) | set(mi[i])):
        a, b = json.dumps(ci[i].get(f), ensure_ascii=False), json.dumps(mi[i].get(f), ensure_ascii=False)
        if a != b:
            print('   row', i, f, '| captain=', a[:160], '| mine=', b[:160])
