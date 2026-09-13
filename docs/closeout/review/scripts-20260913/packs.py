import re, glob, os, json
base = '/Users/yuhanglin/fateradar-goal-20260912/classics'
p = base + '/docs/closeout/FULL-LIBRARY-DISPOSITION-20260912.md'
lines = open(p).read().splitlines()
# only section 1 table: rows before '## 2.'
sec1 = []
for l in lines:
    if l.startswith('## 2.'):
        break
    if re.match(r'^\| `', l):
        sec1.append(re.match(r'^\| `([^`]+)`', l).group(1))
book_rows = [s for s in sec1 if s != 'files']
print('sec1 book rows:', len(book_rows), 'plus pseudo files row:', 'files' in sec1)

ft = set()
for f in glob.glob(base + '/sources/fulltext/**/fulltext.md', recursive=True):
    ft.add(os.path.basename(os.path.dirname(f)))
print('fulltext books:', len(ft))
print('in table not in fulltext:', sorted(set(book_rows) - ft))
print('in fulltext not in table:', sorted(ft - set(book_rows)))

ann_slugs = set()
for f in glob.glob(base + '/references/annotations/**/*.json', recursive=True):
    ann_slugs.add(json.load(open(f)).get('bookSlug'))
print('annotation bookSlugs:', len(ann_slugs))
print('table books without annotations:', sorted(set(book_rows) - ann_slugs))
print('annotation books not in table:', sorted(ann_slugs - set(book_rows)))
