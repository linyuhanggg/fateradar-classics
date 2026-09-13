import json

a = json.load(open('/tmp/rev/bazi-anchor-WORKTREE.json'))
b = json.load(open('/tmp/rev/a8-cur/src/lib/engine/generated/bazi-anchor-rule-index.json'))
print('worktree  sourceRevision =', a.get('sourceRevision'))
print('regen     sourceRevision =', b.get('sourceRevision'))
x, y = dict(a), dict(b)
x.pop('sourceRevision'); y.pop('sourceRevision')
same = json.dumps(x, sort_keys=True, ensure_ascii=False) == json.dumps(y, sort_keys=True, ensure_ascii=False)
print('除 sourceRevision 外完全相同 =', same)
ra = {r['id']: r for r in x['rules']}
rb = {r['id']: r for r in y['rules']}
print('规则数 worktree/regen =', len(ra), len(rb))
diff = [i for i in set(ra) | set(rb) if json.dumps(ra.get(i), sort_keys=True, ensure_ascii=False) != json.dumps(rb.get(i), sort_keys=True, ensure_ascii=False)]
print('内容不同的规则数 =', len(diff), diff[:10])
# t5 时我测到 54 条 (QTB) 差异；看这些 id 现在是否一致
old54 = None
import subprocess
raw = subprocess.run(['git', '-C', '/Users/yuhanglin/fateradar-goal-20260912/product', 'show', 'HEAD:src/lib/engine/generated/bazi-anchor-rule-index.json'], capture_output=True, text=True).stdout
try:
    head = json.loads(raw)
    rh = {r['id']: r for r in head['rules']}
    hx, hy = dict(head), dict(b)
    hx.pop('sourceRevision'); hy.pop('sourceRevision')
    print('HEAD(stamp %s) vs regen: 整体相同 = %s' % (head.get('sourceRevision')[:8], json.dumps(hx, sort_keys=True) == json.dumps(hy, sort_keys=True)))
    d2 = [i for i in set(rh) | set(rb) if json.dumps(rh.get(i), sort_keys=True, ensure_ascii=False) != json.dumps(rb.get(i), sort_keys=True, ensure_ascii=False)]
    print('HEAD vs regen 不同规则数 =', len(d2), d2[:8])
except Exception as e:
    print('HEAD 读取失败', e)
# 抽一条 QTB 看是否已有救应句片段
q = ra.get('QTB-M-01-03')
print('worktree QTB-M-01-03 fragments =', json.dumps(q.get('fragments'), ensure_ascii=False)[:200])
print('regen    QTB-M-01-03 fragments =', json.dumps(rb['QTB-M-01-03'].get('fragments'), ensure_ascii=False)[:200])
