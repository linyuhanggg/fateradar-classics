import json

for n in ('head', 'wt'):
    d = json.load(open(f'/tmp/rev/p12-{n}.json'))
    print('==', n, '==')
    for k, v in d['out'].items():
        if not v.get('ok'):
            print('  ', k, 'FAILED:', v.get('error'))
            continue
        print('  ', k, '| token=', v['focusPosition'], '| points=', v['pointCount'],
              '| 运限事实=', json.dumps(v['factsWithTransit'], ensure_ascii=False)[:150])
        print('       正文尾:', v['firstBodyTail'])

# 关键向后兼容测试：用新代码读「旧代码导出的 3 段 token 文件」
print()
print('=== 旧文件（3 段 token，旧代码导出）在新代码下的回读 ===')
old = json.load(open('/tmp/rev/old-export-3seg-head.json'))
print('  旧文件 focusPosition =', old['input']['focusPosition'], '| points =', len(old['points']))
oldfacts = [f for p in old['points'] for f in (p.get('usedFacts') or []) if f.startswith(('运限', '流曜'))]
print('  旧文件里存的运限事实 =', json.dumps(oldfacts, ensure_ascii=False)[:300])
new = json.load(open('/tmp/rev/old-export-3seg-wt.json'))
newfacts = [f for p in new['points'] for f in (p.get('usedFacts') or []) if f.startswith(('运限', '流曜'))]
print('  新代码按同一 3 段 token 重新导出的运限事实 =', json.dumps(newfacts, ensure_ascii=False)[:300])
print('  两者是否相同 =', oldfacts == newfacts)
