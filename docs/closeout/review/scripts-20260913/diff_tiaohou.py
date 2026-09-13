import json

t = json.load(open('/tmp/rev/tiaohou-regen.json'))
prod = json.load(open('/Users/yuhanglin/fateradar-goal-20260912/product/src/lib/engine/generated/tiaohou-profiles.json'))
print('committed sourceRevision:', prod.get('sourceRevision'))
print('regen     sourceRevision:', t.get('sourceRevision'))
a = dict(prod); b = dict(t)
a.pop('sourceRevision'); b.pop('sourceRevision')
print('identical except revision?', json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False))
for k in set(a) | set(b):
    x = json.dumps(a.get(k), sort_keys=True, ensure_ascii=False)
    y = json.dumps(b.get(k), sort_keys=True, ensure_ascii=False)
    print('  key', k, 'same' if x == y else 'DIFFERS', len(x), len(y))
    if x != y and isinstance(a.get(k), list):
        print('     len committed/regen:', len(a[k]), len(b[k]))
        ca = {json.dumps(i, sort_keys=True) for i in a[k]}
        cb = {json.dumps(i, sort_keys=True) for i in b[k]}
        print('     only committed:', len(ca - cb), 'only regen:', len(cb - ca))
