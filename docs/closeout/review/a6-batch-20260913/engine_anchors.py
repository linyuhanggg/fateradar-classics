import json, glob, os, re, subprocess

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
C = '/Users/yuhanglin/fateradar-goal-20260912/classics'
norm = lambda s: re.sub(r'\s+', '', s or '')

def blob(rev, path):
    r = subprocess.run(['git', '-C', C, 'show', f'{rev}:{path}'], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else None

files = sorted(glob.glob(P + '/src/lib/engine/generated/*.json')) + sorted(glob.glob(P + '/src/lib/knowledge/generated/*.json'))

def walk(node, out):
    if isinstance(node, dict):
        if isinstance(node.get('anchor'), dict) and (node.get('quote') or node.get('text')):
            out.append((node['anchor'], node.get('quote') or node.get('text')))
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)

total = 0
bad_pin = []
bad_head = []
per_file = {}
for p in files:
    try:
        d = json.load(open(p))
    except Exception:
        continue
    rev = d.get('sourceRevision') if isinstance(d, dict) else None
    anchors = []
    walk(d, anchors)
    if not anchors or not rev:
        continue
    per_file[os.path.basename(p)] = (rev[:8], len(anchors))
    cache = {}
    for a, q in anchors:
        f = a.get('file'); s = a.get('startLine'); e = a.get('endLine')
        if not f or not isinstance(s, int):
            continue
        total += 1
        for tag, rv, bucket in (('pin', rev, bad_pin), ('head', 'fe76a0b92db65e54b8551b56228016810345e12f', bad_head)):
            key = (rv, f)
            if key not in cache:
                cache[key] = blob(rv, f)
            lines = cache[key]
            seg = norm(''.join(lines[s - 1:e])) if lines and s <= len(lines) else ''
            if not q or norm(q) not in seg:
                bucket.append((os.path.basename(p), f, s, e))

print('文件（pin, 锚点数）:')
for k, v in per_file.items():
    print('   ', k, v)
print('锚点总数:', total)
print('在各自 pin revision 对不上的:', len(bad_pin), bad_pin[:5])
print('在当前 remote main 对不上的:', len(bad_head), bad_head[:5])
