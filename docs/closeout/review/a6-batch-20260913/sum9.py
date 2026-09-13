import json
for n in ('head', 'wt'):
    d = json.load(open(f'/tmp/rev/p9-{n}.json'))
    print('==', n, '== charts', d['charts'], 'lineCases', d['lineCases'])
    print('   triggered(overview):', json.dumps(d['triggered'], ensure_ascii=False))
    print('   逐爻焦点缺盘级点的用例:', d['violationCases'])
    for s in d['sample']:
        print('     ', json.dumps(s, ensure_ascii=False)[:170])
    print('   唯一无锚点＝白话点(liuyao-free-line)的用例:', d['summaryIsOnlyUnanchored'])
    print('   出现其它无锚点的用例:', d['lineCasesWithUnanchoredNotSummary'])
