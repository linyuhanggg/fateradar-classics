import json,glob,collections,os
base='/Users/yuhanglin/fateradar-goal-20260912/classics'
per=collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(base+'/references/executable/*.json')):
    d=json.load(open(f)); slug=d.get('book',{}).get('slug') if isinstance(d.get('book'),dict) else None
    for r in d.get('rules',[]):
        per[slug][r.get('rescue')]+=1
tot=collections.Counter()
for slug,c in sorted(per.items(), key=lambda x:-sum(x[1].values())):
    self_=c.get('self',0); none=c.get('none',0); un=c.get('unimplemented',0)
    cross=sum(v for k,v in c.items() if k not in ('self','none','unimplemented'))
    tot['self']+=self_; tot['none']+=none; tot['unimplemented']+=un; tot['cross']+=cross
    print(f'{slug}: {sum(c.values())} -> {self_}/{un}/{none}/{cross}  raw={dict(c)}')
print('TOTALS self/unimpl/none/cross =', tot['self'], tot['unimplemented'], tot['none'], tot['cross'])
