import subprocess, hashlib, os

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
M = '/tmp/rev/product-mirror'
paths = ['src/engine', 'tests/engine', 'docs/implementation', 'scripts/art-verdict-judgment-gap-matrix.ts']

listing = subprocess.run(['git', '-C', P, 'ls-files'] + paths, capture_output=True, text=True, check=True).stdout.split()
print('tracked files compared:', len(listing))
diff = []
missing = []
for rel in listing:
    mp = os.path.join(M, rel)
    if not os.path.exists(mp):
        missing.append(rel)
        continue
    blob = subprocess.run(['git', '-C', P, 'show', f'HEAD:{rel}'], capture_output=True).stdout
    disk = open(mp, 'rb').read()
    if hashlib.md5(blob).hexdigest() != hashlib.md5(disk).hexdigest():
        diff.append(rel)
print('files differing from HEAD in mirror:', len(diff))
for d in diff[:20]:
    print('   ', d)
print('files missing in mirror:', len(missing), missing[:10])
