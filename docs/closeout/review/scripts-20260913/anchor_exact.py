import json, glob, os, subprocess, re

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
C = '/Users/yuhanglin/fateradar-goal-20260912/classics'
REV = '3dc9d01b69bbefdd85e3fefb548d4d0831d36626'

norm = lambda s: re.sub(r'\s+', '', s)

rules = []
for f in glob.glob(P + '/src/lib/rules/generated/*.json'):
    d = json.load(open(f))
    items = d['rules'] if isinstance(d, dict) and 'rules' in d else d
    for r in items:
        if isinstance(r, dict) and r.get('anchor'):
            rules.append(r)

byfile = {}
for r in rules:
    byfile.setdefault(r['anchor']['file'], []).append(r)

def blob_lines(rev, path):
    out = subprocess.run(['git', '-C', C, 'show', f'{rev}:{path}'], capture_output=True, text=True)
    return out.stdout.splitlines() if out.returncode == 0 else None

exact_pin_ok = exact_cur_ok = 0
bad = []
for path, rs in byfile.items():
    old = blob_lines(REV, path)
    new = blob_lines('eb4cabe', path)
    for r in rs:
        a = r['anchor']; s, e = a['startLine'], a['endLine']
        q = norm(r.get('quote') or '')
        seg_old = norm(''.join(old[s - 1:e])) if old and s <= len(old) else ''
        seg_new = norm(''.join(new[s - 1:e])) if new and s <= len(new) else ''
        if q and q in seg_old:
            exact_pin_ok += 1
        else:
            bad.append(('pin', path, r.get('id'), s, e))
        if q and q in seg_new:
            exact_cur_ok += 1
        else:
            bad.append(('head', path, r.get('id'), s, e))
print('total anchored rules:', len(rules))
print('exact full-quote contained in anchor range @pin :', exact_pin_ok)
print('exact full-quote contained in anchor range @HEAD:', exact_cur_ok)
print('failures:', len(bad))
for b in bad[:15]:
    print('  ', b)
