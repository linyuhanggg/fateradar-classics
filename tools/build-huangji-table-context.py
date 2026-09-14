#!/usr/bin/env python3
"""Extract literal day/month/star/chen coordinates; never infer missing values.

This writes a review candidate to --output. It does not edit sources or annotations.
"""
import argparse,json,re,random,hashlib,bisect,collections,copy
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--annotations-output',type=Path)
parser.add_argument('--reviewed-literal',action='store_true',help='Use only after independent review of this exact extraction and acceptance rule.')
args=parser.parse_args()
R=Path(__file__).resolve().parents[1];SOURCE=R/'sources/fulltext/divination/huangji-jingshi/fulltext.md';ls=SOURCE.read_text().splitlines();iv=json.loads((R/'references/inventory/paragraphs/divination/huangji-jingshi.json').read_text())['paragraphs'];LOW,HIGH=44,12742
paras=[v for v in iv if v['start_line']<=HIGH and v['end_line']>=LOW]
chap=[]
for line in range(LOW,HIGH+1):
 if re.search(r'觀物篇[一二三四五六七八九十]+',ls[line-1]):chap.append({'line':line,'raw':ls[line-1]})
AXES='日月星辰';pair=re.compile(r'([日月星辰])([甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥])\s*〔([^〕]*)〕');lex=re.compile(r'[一二三四五六七八九十百千萬万零〇兩两]+')
# Deliberately conservative: this accepts ordinary explicit counts under 10,000.
# Rejected spelling is preserved, never corrected from the expected sequence.
numeral=re.compile(r'(?:[一二三四五六七八九]千)?(?:[一二三四五六七八九]百)?(?:[一二三四五六七八九]?十)?[一二三四五六七八九]?')
lineOffsets=[0]
for lineText in ls:lineOffsets.append(lineOffsets[-1]+len(lineText)+1)
consumed=[]
rows=[];parents=[];exceptions=[]
for ci,ch in enumerate(chap):
 lo=ch['line'];hi=chap[ci+1]['line']-1 if ci+1<len(chap) else HIGH
 # erase only Markdown heading marker, preserve one char per removed char to keep offsets valid
 raw='\n'.join(ls[lo-1:hi]);text=re.sub(r'(?m)^#{1,6}(?=\s)',lambda m:' '*len(m[0]),raw);starts=[0]
 for m in re.finditer('\n',text):starts.append(m.end())
 def lineof(pos):return lo+bisect.bisect_right(starts,pos)-1
 state={a:None for a in AXES};matches=[]
 for candidate in pair.finditer(text):
  originalLine=ls[lineof(candidate.start())-1]
  if originalLine.startswith('#') and not re.fullmatch(r'### [日月星辰][甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥]',originalLine):continue
  matches.append(candidate)
 gapCursor=0;invalidParents={}
 for k,m in enumerate(matches):
  gap=raw[gapCursor:m.start()]
  gapWithoutMetadata='\n'.join(l for l in gap.splitlines() if not re.search(r'皇極經世書[卷巻]|欽定四庫全書|觀物篇',l))
  for suspectAxis in '日月星':
   if suspectAxis in gapWithoutMetadata:
    invalidParents[suspectAxis]={'axis':suspectAxis,'gapStartLine':lineof(gapCursor),'gapEndLine':lineof(max(gapCursor,m.start()-1)),'raw':gap}
    for descendant in AXES[AXES.index(suspectAxis):]:state[descendant]=None
  gapCursor=m.end()
  axis,label,count=m.groups();aidx=AXES.index(axis)
  for clearedAxis in AXES[aidx:]:invalidParents.pop(clearedAxis,None)
  node={'axis':axis,'labelRaw':axis+label,'countRaw':count,'labelLine':lineof(m.start()),'countStartLine':lineof(m.start(3)),'countEndLine':lineof(m.end(3)-1),'sourceExcerpt':raw[m.start():m.end()]}
  node['lexicallyNumeric']=bool(lex.fullmatch(re.sub(r'\s','',count)))
  compactCount=re.sub(r'\s','',count)
  node['ordinaryNumeralSpelling']=bool(compactCount and numeral.fullmatch(compactCount))
  node['sourceStartOffset']=lineOffsets[lo-1]+m.start()
  node['sourceEndOffset']=lineOffsets[lo-1]+m.end()
  consumed.append((node['sourceStartOffset'],node['sourceEndOffset']))
  state[axis]=node
  for a in AXES[aidx+1:]:state[a]=None
  if axis!='辰':parents.append({'chapterStartLine':lo,**node});continue
  end=matches[k+1].start() if k+1<len(matches) else len(text)
  trailing=raw[m.end():end].strip(' \t\n#');metadata=bool(re.search(r'皇極經世書[卷巻]|欽定四庫全書',trailing))
  ids=[v['id'] for v in paras if v['start_line']<=node['countEndLine'] and v['end_line']>=node['countStartLine']]
  flags=[]
  if invalidParents:flags.append('invalid-parent-unparsed')
  if any(state[a] is None for a in AXES):flags.append('missing-explicit-parent')
  if any(state[a] and not state[a]['lexicallyNumeric'] for a in AXES):flags.append('non-numeral-in-count-preserved')
  if any(state[a] and not state[a]['ordinaryNumeralSpelling'] for a in AXES):flags.append('nonstandard-number-spelling-preserved')
  if trailing:flags.append('trailing-text-preserved-not-parsed')
  if any(state[a] and state[a]['labelRaw'][1] not in ('甲乙丙丁戊己庚辛壬癸' if a in '日星' else '子丑寅卯辰巳午未申酉戌亥') for a in AXES):flags.append('axis-label-outside-usual-stem-branch-class-preserved')
  if metadata:flags.append('volume-heading-in-trailing-text')
  # unusual numerals stay raw: no conversion, no expected sequence validation, no correction
  rows.append({'rowId':f'hj-main-ymxc-L{node["labelLine"]:05d}-N{len(rows)+1:04d}','chapter':ch,'coordinates':state.copy(),'invalidParentEvidence':list(invalidParents.values()),'sourceParagraphIds':ids,'trailingRaw':trailing,'flags':flags,'review':'draft','semanticStatus':'literal-structure-candidate-not-semantic-reviewed'})
 if not matches:exceptions.append({'chapter':ch,'reason':'no-axis-count-matches'})
 # preserve characters not consumed by any explicit pair as evidence, including titles and chronicle additions
 cursor=0
 for m in matches:
  gap=raw[cursor:m.start()]
  if gap.strip(' \t\n#'):
   exceptions.append({'chapterStartLine':lo,'startLine':lineof(cursor),'endLine':lineof(m.start()-1),'raw':gap,'reason':'text-outside-axis-count-pairs'})
  cursor=m.end()
 if raw[cursor:].strip(' \t\n#'):exceptions.append({'chapterStartLine':lo,'startLine':lineof(cursor),'endLine':hi,'raw':raw[cursor:],'reason':'text-outside-axis-count-pairs'})
by=collections.defaultdict(list)
for row in rows:
 for pid in row['sourceParagraphIds']:by[pid].append(row['rowId'])
dispositions=[]
rowById={r['rowId']:r for r in rows}
for p in paras:
 ids=by.get(p['id'],[]);raw='\n'.join(ls[p['start_line']-1:p['end_line']])
 start=lineOffsets[p['start_line']-1];end=start+len(raw);covered=[False]*len(raw)
 for a,b in consumed:
  if a<end and b>start:
   for pos in range(max(a,start)-start,min(b,end)-start):covered[pos]=True
 residual=''.join(c if not covered[i] else ' ' for i,c in enumerate(raw)).strip()
 flags=sorted({f for rid in ids for f in rowById[rid]['flags']})
 if residual:flags.append('unparsed-paragraph-content')
 if re.search(r'皇極經世書[卷巻]|欽定四庫全書|觀物篇',raw):flags.append('volume-or-chapter-metadata')
 dispositions.append({'paragraphId':p['id'],'startLine':p['start_line'],'endLine':p['end_line'],'sourceRaw':raw,'rowIds':ids,'unparsedRaw':residual,'disposition':'has-literal-coordinate-rows' if ids else 'no-leaf-row-matched','flags':flags,'eligibleForLiteralReview':bool(ids) and not flags})
sample=copy.deepcopy(random.Random(20260914).sample(rows,20))
for row in sample:
 line=row['coordinates']['辰']['labelLine'];row['sampleContext']={'startLine':max(LOW,line-2),'endLine':min(HIGH,row['coordinates']['辰']['countEndLine']+2),'raw':'\n'.join(ls[max(LOW,line-2)-1:min(HIGH,row['coordinates']['辰']['countEndLine']+2)])}
summary={'range':[LOW,HIGH],'chapterCount':len(chap),'inventoryParagraphCount':len(paras),'literalRowCount':len(rows),'paragraphsWithRows':len(by),'paragraphsWithoutRows':len(paras)-len(by),'completeParentRows':sum(all(v is not None for v in t['coordinates'].values()) for t in rows),'rowsWithFlags':sum(bool(t['flags']) for t in rows),'flagCounts':dict(collections.Counter(f for t in rows for f in t['flags']))}
summary['eligibleLiteralParagraphs']=sum(p['eligibleForLiteralReview'] for p in dispositions)
summary['unresolvedOrMetadataParagraphs']=len(dispositions)-summary['eligibleLiteralParagraphs']
summary['literalReviewAccepted']=args.reviewed_literal
result={'sourceFile':str(SOURCE.relative_to(R)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'summary':summary,'rules':['只匹配原字(日月星辰)+单字标签+〔原数字串〕，不转换数值、不根据顺序补数或纠字。','跨行只连接空白；每个父坐标保存其自身原字与行号。','章节切换重置四级上下文；更高层新标签清除所有下级。','leaf按数字所在行关联inventory，不用上一段heading字段猜标签。','数字中的异常字及未解析历史附文/卷题全部保留；匹配并不意味着原书数字正确。','全产物draft；source-reviewed需root读源及独立Judge。'],'rows':rows,'parentNodes':parents,'paragraphDispositions':dispositions,'unparsedText':exceptions,'random20':sample}
if args.reviewed_literal:
 result['rules'][-1]='独立复核后仅整段无异常且每字均已解析的数字坐标释读标source-reviewed；不代表影印校勘、历算解释或数值正确性。'
 for row in rows:
  if row['sourceParagraphIds'] and all(next(p for p in dispositions if p['paragraphId']==pid)['eligibleForLiteralReview'] for pid in row['sourceParagraphIds']):
   row['review']='source-reviewed';row['semanticStatus']='literal-coordinate-reading-only'
if args.annotations_output:
 reasons={'axis-label-outside-usual-stem-branch-class-preserved':'标签出现通常干支分组之外的原字','nonstandard-number-spelling-preserved':'有数字串未通过保守数词语法检查','non-numeral-in-count-preserved':'数值括号内夹有非数字原字','invalid-parent-unparsed':'上级标签之间有未解析文字，已阻止沿用旧父项','missing-explicit-parent':'至少一层父项缺少可确认原文','trailing-text-preserved-not-parsed':'相邻表项间另有未解析文字','volume-heading-in-trailing-text':'后接卷题','unparsed-paragraph-content':'本段另有未解析原字','volume-or-chapter-metadata':'本段含篇题或卷题'}
 entries=[]
 for p in dispositions:
  prows=[rowById[rid] for rid in p['rowIds']];desc=[];related=set();anchors=[]
  for row in prows:
   labels=[]
   for axis in AXES:
    node=row['coordinates'][axis]
    if node is None:labels.append(axis+'层缺明确父项');continue
    labels.append(node['labelRaw']+'〔'+re.sub(r'\s','',node['countRaw'])+'〕')
    anchors.append(f"{node['labelRaw']}：原文 L{node['labelLine']}–L{node['countEndLine']}")
    related.update(v['id'] for v in paras if v['start_line']<=node['countEndLine'] and v['end_line']>=node['countStartLine'])
   desc.append(' → '.join(labels))
  if prows:
   vernacular='本段数字表项按原文所在层级读为：'+'；'.join(desc)+'。日、月、星、辰在这里仅作该表层级名，括号内照录原数字，不据此换算公历日期或推演现实事件。'
  elif 'volume-or-chapter-metadata' in p['flags']:
   vernacular='本段为卷篇著录或分界，原文记作「'+p['sourceRaw'].strip()+'」，不构成独立数字表项。'
  else:
   vernacular='本段原文「'+p['sourceRaw'].strip()+'」未能匹配完整的辰标签及其数字，暂不能恢复完整坐标；不按相邻数列补值。'
  if p['unparsedRaw'] and prows:vernacular+='另存未解析原文「'+p['unparsedRaw']+'」，不替它补造列位。'
  notes=['这是现有电子转写层的数字表结构恢复，保留原字、父项来源和未解析余文；不等于影印校字或算术正确性验证。']
  if anchors:notes.append('坐标出处：'+'；'.join(dict.fromkeys(anchors))+'。')
  if p['flags']:notes.append('保留 draft：'+'；'.join(reasons[f] for f in p['flags'])+'。')
  kind='理论' if prows else ('序跋目录' if 'volume-or-chapter-metadata' in p['flags'] else '待核实')
  e={'paragraphId':p['paragraphId'],'kind':kind,'vernacular':vernacular,'terms':[],'notes':notes,'review':'source-reviewed' if args.reviewed_literal and p['eligibleForLiteralReview'] else 'draft','verified':False}
  related.discard(p['paragraphId'])
  if related:e['relatedParagraphIds']=sorted(related)
  entries.append(e)
 args.annotations_output.write_text(json.dumps({'bookSlug':'huangji-jingshi','entries':entries},ensure_ascii=False,indent=2)+'\n')
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
