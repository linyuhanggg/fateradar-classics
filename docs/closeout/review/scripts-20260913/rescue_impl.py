import json, re

P = '/Users/yuhanglin/fateradar-goal-20260912/product'
C = '/Users/yuhanglin/fateradar-goal-20260912/classics'

src = open(P + '/src/lib/engine/bazi/tiaohou-rescue.ts').read()
ids = re.findall(r'id:\s*"(QTB-[A-Z0-9\-]+)"', src)
print('rule ids in tiaohou-rescue.ts:', len(ids), 'distinct:', len(set(ids)))

d = json.load(open(C + '/references/executable/qiongtong-baojian.json'))
self_rules = [r['id'] for r in d['rules'] if r.get('rescue') == 'self']
unimpl = [r['id'] for r in d['rules'] if r.get('rescue') == 'unimplemented']
none_rules = [r['id'] for r in d['rules'] if r.get('rescue') == 'none']
print('QTB rescue=self:', len(self_rules), '| unimplemented:', len(unimpl), '| none:', len(none_rules))
print('self rules not in tiaohou-rescue.ts:', sorted(set(self_rules) - set(ids)))
print('tiaohou-rescue.ts ids not self-labeled:', sorted(set(ids) - set(self_rules)))
print()
print('unimplemented QTB ids:', sorted(unimpl))
# do the unimplemented ones have named reasons in the rescue file header?
head = src.split('*/')[0]
missing_reason = [i for i in unimpl if i not in head]
print('unimplemented QTB ids without a named reason in tiaohou-rescue.ts header:', missing_reason)
