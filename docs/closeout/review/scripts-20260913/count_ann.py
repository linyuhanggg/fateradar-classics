import json,glob,collections,os
base='/Users/yuhanglin/fateradar-goal-20260912/classics'
files=sorted(glob.glob(base+'/references/annotations/**/*.json',recursive=True))
tot=0; rev=collections.Counter(); per=collections.Counter(); drafts=collections.Counter()
books=set(); nopara=0; noparadraft=0; reviewkeys=collections.Counter()
for f in files:
    d=json.load(open(f))
    slug=d.get('bookSlug') or os.path.basename(f)[:-5]
    books.add(slug)
    for e in d.get('entries',[]):
        tot+=1
        r=e.get('review')
        reviewkeys[r]+=1
        rev[r]+=1
        per[slug]+=1
        if r!='source-reviewed':
            drafts[slug]+=1
        if not e.get('paragraphId'):
            nopara+=1
            if r!='source-reviewed': noparadraft+=1
print('files',len(files))
print('distinct bookSlug',len(books))
print('total entries',tot)
print('review counter',dict(rev))
print('source-reviewed',rev.get('source-reviewed',0))
print('draft(all non-source-reviewed)',tot-rev.get('source-reviewed',0))
print('entries without paragraphId',nopara,'of which draft',noparadraft)
print('books total entries >0:',len([k for k,v in per.items() if v>0]))
print('books with draft:',len(drafts))
for k,v in drafts.most_common():
    print('  DRAFT',k,v,'/ total',per[k])
