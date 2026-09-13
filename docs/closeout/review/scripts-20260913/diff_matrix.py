import json, sys

old = json.load(open('/tmp/rev/product-mirror/docs/implementation/art-verdict-judgment-gap-matrix.json'))
# the mirror copy was overwritten by the run; old snapshot is gone -> use git show of HEAD version
import subprocess
raw = subprocess.run(['git', '-C', '/Users/yuhanglin/fateradar-goal-20260912/product',
                      'show', 'HEAD:docs/implementation/art-verdict-judgment-gap-matrix.json'],
                     capture_output=True, text=True, check=True).stdout
old = json.loads(raw)
new = json.load(open('/tmp/rev/product-mirror/docs/implementation/art-verdict-judgment-gap-matrix.json'))

print('old product_head/classics_head/generated_at:', old.get('product_head'), old.get('classics_head'), old.get('generated_at'))
print('new product_head/classics_head/generated_at:', new.get('product_head'), new.get('classics_head'), new.get('generated_at'))
print()
so, sn = old['summary'], new['summary']
keys = [k for k in so if k in sn]
diff = [k for k in keys if json.dumps(so[k], sort_keys=True) != json.dumps(sn[k], sort_keys=True)]
print('summary keys differing:', len(diff))
for k in diff:
    a, b = json.dumps(so[k], ensure_ascii=False), json.dumps(sn[k], ensure_ascii=False)
    print(' -', k)
    print('    old:', a[:400])
    print('    new:', b[:400])
print()
print('summary keys only in old:', [k for k in so if k not in sn])
print('summary keys only in new:', [k for k in sn if k not in so])
print()
ro, rn = old['rows'], new['rows']
print('rows old/new:', len(ro), len(rn))
doi = {r.get('id'): r for r in ro}
dni = {r.get('id'): r for r in rn}
print('id sets equal:', set(doi) == set(dni))
changed = []
for k in sorted(set(doi) & set(dni)):
    if json.dumps(doi[k], sort_keys=True) != json.dumps(dni[k], sort_keys=True):
        changed.append(k)
print('rows changed:', len(changed), changed[:40])
