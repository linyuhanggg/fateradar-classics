import json, glob, os, re
base = '/Users/yuhanglin/fateradar-goal-20260912/classics'
un = []
for f in sorted(glob.glob(base + '/references/executable/*.json')):
    d = json.load(open(f))
    for r in d.get('rules', []):
        if r.get('rescue') == 'unimplemented':
            un.append((os.path.basename(f), r.get('id'), r.get('theme'), r.get('book'), len(r.get('sources', []))))
print('unimplemented count:', len(un))
for row in un:
    print('  ', row)
audit = open(base + '/docs/closeout/RESCUE-LABEL-AUDIT-20260912.md').read()
missing = []
for f, rid, theme, book, nsrc in un:
    if '`%s`' % rid not in audit:
        missing.append(rid)
print()
print('unimplemented ids absent from RESCUE-LABEL-AUDIT doc:', missing)
print('audit rows total:', len(re.findall(r'^\| `[A-Z]', audit, re.M)))
