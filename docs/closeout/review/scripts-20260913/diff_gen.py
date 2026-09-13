import json, subprocess, difflib

def load(p):
    return json.load(open(p))

committed = load('/tmp/rev/bazi-anchor-COMMITTED.json')
fresh = load('/tmp/rev/product-mirror/src/lib/engine/generated/bazi-anchor-rule-index.json')
print('bazi-anchor: committed sourceRevision =', committed.get('sourceRevision'))
print('bazi-anchor: fresh     sourceRevision =', fresh.get('sourceRevision'))
c, f = dict(committed), dict(fresh)
c.pop('sourceRevision'); f.pop('sourceRevision')
print('bazi-anchor identical except revision?', json.dumps(c, sort_keys=True, ensure_ascii=False) == json.dumps(f, sort_keys=True, ensure_ascii=False))
if json.dumps(c, sort_keys=True) != json.dumps(f, sort_keys=True):
    # find diff keys
    print('top keys:', list(c.keys()), list(f.keys()))
    for k in set(c) | set(f):
        a, b = json.dumps(c.get(k), sort_keys=True, ensure_ascii=False), json.dumps(f.get(k), sort_keys=True, ensure_ascii=False)
        if a != b:
            print('  differs:', k, 'len', len(a), len(b))
            if isinstance(c.get(k), list):
                ca = {x.get('id'): x for x in c[k] if isinstance(x, dict)}
                fa = {x.get('id'): x for x in f[k] if isinstance(x, dict)}
                ch = [i for i in set(ca) | set(fa) if json.dumps(ca.get(i), sort_keys=True) != json.dumps(fa.get(i), sort_keys=True)]
                print('    rule ids differing:', len(ch), sorted(ch)[:20])
                for i in sorted(ch)[:3]:
                    print('    sample', i)
                    for kk in set(ca.get(i, {})) | set(fa.get(i, {})):
                        x, y = json.dumps(ca.get(i, {}).get(kk), ensure_ascii=False), json.dumps(fa.get(i, {}).get(kk), ensure_ascii=False)
                        if x != y:
                            print('       ', kk, 'committed=', x[:160], '| fresh=', y[:160])
print()
print('=== tiaohou ===')
t = load('/tmp/rev/tiaohou-regen.json')
prod = load('/Users/yuhanglin/fateradar-goal-20260912/product/src/lib/engine/generated/tiaohou-profiles.json')
print('committed sourceRevision', prod.get('sourceRevision'), '| regen', t.get('source_revision'))
print('keys prod', list(prod.keys()))
print('keys regen', list(t.keys()))
