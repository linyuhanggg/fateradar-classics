import json, glob, os, re, subprocess

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
C = '/Users/yuhanglin/fateradar-goal-20260912/classics'
REMOTE_MAIN = 'fe76a0b92db65e54b8551b56228016810345e12f'
norm = lambda s: re.sub(r'\s+', '', s or '')

def blob(rev, path, cache):
    key = (rev, path)
    if key not in cache:
        r = subprocess.run(['git', '-C', C, 'show', f'{rev}:{path}'], capture_output=True, text=True)
        cache[key] = r.stdout.splitlines() if r.returncode == 0 else None
    return cache[key]

cache = {}
files = sorted(glob.glob(P + '/src/lib/engine/generated/*.json')) + sorted(glob.glob(P + '/src/lib/knowledge/generated/*.json')) + sorted(glob.glob(P + '/src/lib/rules/generated/*.json'))

def collect(node, out):
    """收集形如 {file,startLine,endLine,quote} 的锚点对象（含 fragments/anchor/sources 各种嵌法）。"""
    if isinstance(node, dict):
        if isinstance(node.get('file'), str) and isinstance(node.get('startLine'), int) and node.get('quote'):
            out.append((node, node['quote']))
        for v in node.values():
            collect(v, out)
    elif isinstance(node, list):
        for v in node:
            collect(v, out)

grand = 0
bad_pin = []
bad_main = []
per_file = {}
for p in files:
    try:
        d = json.load(open(p))
    except Exception:
        continue
    rev = d.get('sourceRevision') if isinstance(d, dict) else None
    hits = []
    collect(d, hits)
    if not hits or not rev:
        continue
    per_file[os.path.basename(p)] = (rev[:8], len(hits))
    for node, q in hits:
        grand += 1
        f, s, e = node['file'], node['startLine'], node.get('endLine', node['startLine'])
        for tag, rv, bucket in (('pin', rev, bad_pin), ('main', REMOTE_MAIN, bad_main)):
            lines = blob(rv, f, cache)
            seg = norm(''.join(lines[s - 1:e])) if lines and s <= len(lines) else ''
            if norm(q) not in seg:
                bucket.append((os.path.basename(p), f, s, e))

print('文件（pin, 锚点数）:')
for k, v in sorted(per_file.items()):
    print('   ', k, v)
print('锚点总数:', grand, '(账本 A8 记 7 份产物 578 锚点)')
print('在各自 pin 对不上:', len(bad_pin), bad_pin[:5])
print('在当前 remote main 对不上:', len(bad_main), bad_main[:5])
