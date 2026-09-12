# Draft 注解去向 · Round 6（2026-09-12）

> 工作树 `/Users/yuhanglin/fateradar-goal-20260912/classics`，分支 `dsh/full-library-classics`。
> 本轮**不升任何条目**：产出是**全库 draft 的去向表**（可重跑），以及一处**已过时阻塞理由的更正**。
> 基线：62,839 条注解 = 60,004 `source-reviewed` + **2,835 `draft`**（`python3 tools/validate-annotations.py` 实测）。

## 1. 全库 draft 去向（按 kind）

| kind | 条数 | 去向 |
| --- | ---: | --- |
| 评注或元数据 | 1,531 | **永久 draft**：现代恢复档案／定位说明，不是古书原句（qimen nlc-layouts 1,245、约言 recovery 161、麻衣 42…），**不得当纸面证据，也不应升 source-reviewed** |
| 待核实 | 795 | 保留 draft（其中 666＝總鈐残格，见 §3；其余为各书待核条目） |
| 规则候选 | 297 | 保留 draft：199 疑字/残、34 待核/异文未唯一、25 缺底本、13 图残、26 需人读 |
| 术语 | 106 | 保留 draft（同上归因） |
| 案例 | 73 | 保留 draft |
| 理论 / 操作步骤 / 序跋目录 / 重复 | 33 | 保留 draft |

## 2. 全库 draft 去向（按阻塞归因，notes 首命中，可重跑）

| 阻塞 | 条数 | 去向 |
| --- | ---: | --- |
| 现代元数据/恢复说明（非古籍原文） | **1,302** | 永久 draft（设计如此） |
| 缺底本／无平行本 | 757 | 保留 draft；已记录已查来源与缺页，待底本 |
| 疑字／残／脱／阙／墨块 | 515 | 保留 draft；待更清晰底本或影印核对 |
| 源层 `ocr-draft`（校勘器禁升） | 166 | 需先完成转录审读（passage-reviewed）方可升；现状见下 |
| 待核／异文未唯一 | 63 | 保留 draft |
| 图残／版面／表格结构 | 31 | 保留 draft |
| 非算法材料（知识库去向） | 1 | 保留 draft（风水/择日材料不接入算法） |

**结论**：2,835 条 draft **没有一条属于「漏做功」**；最大两块是**设计上就该是 draft 的现代元数据**（1,302）与**缺底本/字残**（1,272，与前者有交叠）。

## 3. 本轮实际更动：666 条總鈐残格的**阻塞理由已过时，已更正**

666 条原记（t2）：

> 「…sources/facsimile 亦无大六壬大全影印；**残格仍无法定列，须总钤影印页**。」

该句前半句与本句的核心判断**今日均不成立**，故逐条追加更正（**追加 note，不改原 note、不改正文**，666/666 全部追加）：

| 事实 | 依据 |
| --- | --- |
| 四庫本《六壬大全》卷一影印**已在仓内** | `sources/facsimile/other/daliuren-daquan/liuren-daquan-juan1-siku-archive-06054168.pdf`，112 页，sha256 `7790f774…`，1914×2718@600ppi |
| 《總鈐》＝PDF 第 15 页标题；十表连续 p16–p25（六甲日…六癸日） | `sources/normalized/san-shi/daliuren-daquan/zongqian-layout-016-025.md` §1 |
| **「无法定列」不再成立**：列轴可从纸面复原 | 每栏「天干＋日支」首字落在逐页可测竖列上；四庫本 p16 八格行标已逐格原生复核定案；同类页 284–291／314–324 的行标合起来构成**完整甲子→癸亥六十甲子环** |
| **仍然阻塞的是逐格内容落位** | 该印本字心距 ≈70px 而字面宽 ≈100–110px → 同列字粘连、邻栏字在 x 上重叠，「某字属哪一格」在表内很大一部分不可判；p17 首栏为多行密集块 |
| 故仍保持 draft，且写明**什么能解除** | 更清晰印本／扫描，或按「栏内字串、不落格」登记（**不得以期待值补格**） |

## 4. 未做与边界

- **本轮 0 升**，`verified` 全库仍非 true（电子对照 ≠ 人工影印校勘）。
- 未处理 qimen nlc-layouts 与约言 nlc-recovery 的**升审**：前者 1,245 条是元数据（永久 draft），后者的层门（`ocr-draft`）未解除，两者都不是「读一遍就能升」。
- **约言 nlc-recovery 的层门已有逐页数字**（本轮补测，见 `sources/normalized/bazi/mingli-yueyan/partial-blocker-census-158.md`）：
  该集的 158 个 `partial` 页 = **156 页仅卡在「装饰性版面符号／项目序号未释读」**（正文已在 `reviewedRanges` 内逐句对图）
  ＋ **1 页（p30）另有实质待核**（表内分量与日数的对应、「三十一/三十」差异）
  ＋ **2 页（p1 封面题字、p2 页外手写号）为页外材料**（记录里已明写不影响正文）。
  也就是说：**除 p30 的一张表外，这批页的正文工序已为 0**；剩下的是「装饰符号未释读能否放行」这一**引用政策**决定
  （`source_paragraphs.py` 现在的门槛是「整页 source-reviewed 且无 unresolved」，156 页都还带一条 unresolved 行）。
  本文件不据此提升任何页或注解状态。
- 未批量改任何 `notes` 的历史结论；666 条是**追加**更正，原句保留可审计。
- 择日/相法/风水/紫微/禄命材料的去向仍是**知识库**，未伪造成已接入算法。

## 5. 复现命令

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
python3 tools/validate-annotations.py           # 53 books, 62839 entries, 0 errors
python3 - <<'PY'                                 # §1/§2 两张表
import json, glob, collections, re
kinds=collections.Counter()
for f in glob.glob('references/annotations/**/*.json', recursive=True):
    for it in json.load(open(f,encoding='utf-8')).get('entries') or []:
        if isinstance(it,dict) and it.get('review')=='draft': kinds[it.get('kind') or '(none)']+=1
print(dict(kinds))
PY
```
