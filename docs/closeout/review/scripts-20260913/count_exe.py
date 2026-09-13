import json,glob,collections,os
base='/Users/yuhanglin/fateradar-goal-20260912/classics'
files=sorted(glob.glob(base+'/references/executable/*.json'))
tot=0; arts=collections.Counter(); rescue=collections.Counter(); per=collections.Counter()
ids=collections.Counter(); dup=[]
missing_keys=collections.Counter()
for f in files:
    d=json.load(open(f))
    rules=d.get('rules',[])
    per[os.path.basename(f)]=len(rules)
    for r in rules:
        tot+=1
        arts[r.get('art')]+=1
        rescue[r.get('rescue')]+=1
        ids[r.get('id')]+=1
        for k in ('id','art','rescue','paragraph_ids','sources'):
            if k not in r: missing_keys[k]+=1
dup=[k for k,v in ids.items() if v>1]
print('json files',len(files))
print('total rules',tot)
print('rules by art',dict(arts))
print('rescue counter',dict(rescue))
print('duplicate ids',dup)
print('missing keys',dict(missing_keys))
print('--- per file ---')
for k,v in sorted(per.items(), key=lambda x:-x[1]): print(' ',k,v)
# cross-ref check: rescue referencing other rule ids
