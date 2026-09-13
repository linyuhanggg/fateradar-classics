import re
p = '/Users/yuhanglin/fateradar-goal-20260912/classics/docs/closeout/FULL-LIBRARY-DISPOSITION-20260912.md'
lines = open(p).read().splitlines()
rows = [l for l in lines if re.match(r'^\| `', l)]
slugs = [re.match(r'^\| `([^`]+)`', l).group(1) for l in rows]
print('slug rows:', len(rows))
print('distinct slugs:', len(set(slugs)))
print('non-book slug rows:', [s for s in slugs if s == 'files'])
for l in lines:
    if l.startswith('| **'):
        print('TOTAL ROW:', l)
