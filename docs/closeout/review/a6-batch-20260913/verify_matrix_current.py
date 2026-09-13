import json, subprocess

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
cap = json.loads(subprocess.run(['git', '-C', P, 'show', '00e98fc:docs/implementation/art-verdict-judgment-gap-matrix.json'],
                                capture_output=True, text=True, check=True).stdout)
fresh = json.load(open('/tmp/rev/a6-wt/docs/implementation/art-verdict-judgment-gap-matrix.json'))
print('committed head fields: product', cap.get('product_head'), 'classics', cap.get('classics_head'))
print('fresh     head fields: product', fresh.get('product_head'), 'classics', fresh.get('classics_head'))
cs, fs = cap['summary'], fresh['summary']
d = [k for k in set(cs) | set(fs) if json.dumps(cs.get(k), sort_keys=True) != json.dumps(fs.get(k), sort_keys=True)]
print('summary keys differing:', d)
for k in d:
    print('   ', k, '| committed:', json.dumps(cs.get(k), ensure_ascii=False)[:180])
    print('   ', ' ' * len(k), '| fresh    :', json.dumps(fs.get(k), ensure_ascii=False)[:180])
ci = {r['id']: r for r in cap['rows']}
fi = {r['id']: r for r in fresh['rows']}
print('ids equal:', set(ci) == set(fi), len(ci), len(fi))
rowdiff = [i for i in ci if json.dumps(ci[i], sort_keys=True) != json.dumps(fi.get(i), sort_keys=True)]
print('rows differing:', len(rowdiff), rowdiff[:10])
