import json, subprocess

raw = subprocess.run(['git', '-C', '/Users/yuhanglin/fateradar-goal-20260912/product',
                      'show', 'HEAD:docs/implementation/art-verdict-judgment-gap-matrix.json'],
                     capture_output=True, text=True).stdout
o = json.loads(raw)
n = json.load(open('/tmp/rev/product-mirror/docs/implementation/art-verdict-judgment-gap-matrix.json'))
oi = {r['id']: r for r in o['rows']}
ni = {r['id']: r for r in n['rows']}
res = [k for k in oi if oi[k].get('classicsRescue') != ni[k].get('classicsRescue')]
unk = [k for k in oi if oi[k].get('classicsUnknownWhen') != ni[k].get('classicsUnknownWhen')]
print('rows with classicsRescue change:', len(res))
print('rows with classicsUnknownWhen change:', len(unk), unk)
for k in unk[:3]:
    print('  ', k)
    print('    old:', json.dumps(oi[k].get('classicsUnknownWhen'), ensure_ascii=False)[:200])
    print('    new:', json.dumps(ni[k].get('classicsUnknownWhen'), ensure_ascii=False)[:200])
from collections import Counter
print('rescue transitions:', Counter((oi[k].get('classicsRescue'), ni[k].get('classicsRescue')) for k in res))
