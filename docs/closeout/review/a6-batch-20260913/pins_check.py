import json, glob, os, re, subprocess

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
C = '/Users/yuhanglin/fateradar-goal-20260912/classics'

pins = {}
for p in glob.glob(P + '/src/**/generated/*.json', recursive=True):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if isinstance(d, dict) and isinstance(d.get('sourceRevision'), str) and len(d['sourceRevision']) >= 8:
        pins[os.path.relpath(p, P)] = d['sourceRevision']

src = open(P + '/src/lib/rules/source-link.ts').read()
m = re.search(r'CLASSICS_REV\s*=\s*"([0-9a-f]{40})"', src)
if m:
    pins['src/lib/rules/source-link.ts:CLASSICS_REV'] = m.group(1)
wf = open(P + '/.github/workflows/ci.yml').read()
m2 = re.search(r'ref:\s*([0-9a-f]{40})', wf)
if m2:
    pins['.github/workflows/ci.yml:checkout ref'] = m2.group(1)

remote = subprocess.run(['git', '-C', C, 'ls-remote', 'origin', 'main'], capture_output=True, text=True).stdout.split()[0]
print('classics remote main =', remote)
print('pins found:', len(pins))
ok = bad = 0
for k, v in sorted(pins.items()):
    t = subprocess.run(['git', '-C', C, 'cat-file', '-t', v], capture_output=True, text=True).stdout.strip()
    isanc = subprocess.run(['git', '-C', C, 'merge-base', '--is-ancestor', v, remote], capture_output=True).returncode == 0
    behind = subprocess.run(['git', '-C', C, 'rev-list', '--count', f'{v}..{remote}'], capture_output=True, text=True).stdout.strip()
    print(f'  {v[:8]} type={t} ancestorOfRemoteMain={isanc} behind={behind}  <- {k}')
    if t == 'commit' and isanc:
        ok += 1
    else:
        bad += 1
print('ok pins:', ok, '| bad pins:', bad)

# 旧钉 3dc9d01 落后多少（核对账本写的 1,769）
old = '3dc9d01b69bbefdd85e3fefb548d4d0831d36626'
print('3dc9d01 -> remote main behind =', subprocess.run(['git', '-C', C, 'rev-list', '--count', f'{old}..{remote}'], capture_output=True, text=True).stdout.strip())
print('3dc9d01 -> eb4cabe behind     =', subprocess.run(['git', '-C', C, 'rev-list', '--count', f'{old}..eb4cabe'], capture_output=True, text=True).stdout.strip())
