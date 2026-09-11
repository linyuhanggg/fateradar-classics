# Draft 注解去向 · Round 2

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线 SHA：`2c8fb6f3abef8e49587042f2d84971549530f99b`  
范围：优先星历考原空单元格、大六壬大全可核电子对照、六壬秘本空 notes、紫微/麻衣空 notes。**未重做奇门 nlc-layouts 升审。未处理全部 draft，不虚报 3226 已清空。**

规则执行摘要：

- 能对照电子原文核实的，升 `source-reviewed`；`verified` 保持非 true（电子对照 ≠ 人工影印校勘）。
- 繁简/异体只用于检索，未改写引用原文。
- 缺底本、疑字、图残、跨行残、粘连待核、kind=待核实：保留 `draft`，notes 写清原因与影响。
- 空 notes 本轮全部补上具体原因。
- 未把理论/目录/案例/重复改成规则；择日/相法/紫微去向是知识库，未伪造成已接入算法。
- 未 git commit / push；未改 product 仓；未碰 `/Users/sync/code`。

## 总量

| 项 | 数量 |
|---|---|
| Round1 结束后全局 draft | 3226 |
| Round1 结束后全局 source-reviewed | 59613 |
| 本轮升 `source-reviewed` | **213**（星历考原 184 + 大六壬 28 + 六壬秘本 1） |
| 本轮处理后全局 draft | **3013** |
| 本轮处理后全局 source-reviewed | **59826** |
| 奇门 nlc-layouts | 未打开、未升（仍 1261 draft） |

213 = 184 + 28 + 1。3013 = 3226 − 213。不把未打开的玉匣记 267、麻衣其余 222、约言 162、皇极经世 40 等算作本轮已清空。

## 分文件

### 1. `references/annotations/selection/xingli-kaoyuan--shidian-SK1618.json`

| | 前 | 后 |
|---|---|---|
| draft | 185 | **1** |
| source-reviewed | 127 | **311** |
| 本轮升 | **184** | |

184 条 draft 的 vernacular 均为「十月绝阳所领日立成表空单元格。短表残格，不展开、不补格、不连成月日全表。」notes 原为「空单元格。不补表。」`source_status=reference-text`（不是 ocr-draft）。

对照识典 `sources/normalized/shidianguji/SK1618/text.md`：这 184 条源段全文一律是

```
〔原表开始；以下行列号用于保留单元格对应〕
第1行，第1列：〔空单元格〕
〔原表结束〕
```

heading 全是「网站章节：十月絶陽所領日」。邻格可见甲申、乙未、丙午、辛卯至戊戌等有字格，空格与有字格交错，电子本确实无字。升审核实的是「电子本此格无字」，不是补表、不是复原立成全表。择日入知识库，不接入算法。`verified` 未设 true。

**抽核 15 条（≥15），全部源文为〔空单元格〕：**

1. `xingli-kaoyuan:shidian-SK1618:P7639154009312624649` — L331–333
2. `xingli-kaoyuan:shidian-SK1618:P7639154010838007858` — 抽核序号 12
3. `xingli-kaoyuan:shidian-SK1618:P7639154010839007282` — 24
4. `xingli-kaoyuan:shidian-SK1618:P7639154010839220274` — 36
5. `xingli-kaoyuan:shidian-SK1618:P7639154010839449650` — 48
6. `xingli-kaoyuan:shidian-SK1618:P7639154011345551398` — 60
7. `xingli-kaoyuan:shidian-SK1618:P7639154011346944038` — 72
8. `xingli-kaoyuan:shidian-SK1618:P7639154011421032475` — 84
9. `xingli-kaoyuan:shidian-SK1618:P7639154011421933595` — 96
10. `xingli-kaoyuan:shidian-SK1618:P7639154011422162971` — 108
11. `xingli-kaoyuan:shidian-SK1618:P7639154011422425115` — 120
12. `xingli-kaoyuan:shidian-SK1618:P7639154011513290779` — 132
13. `xingli-kaoyuan:shidian-SK1618:P7639154011514847259` — 144
14. `xingli-kaoyuan:shidian-SK1618:P7639154011602714634` — 168
15. `xingli-kaoyuan:shidian-SK1618:P7639154011602976778` — L1343–1345（表末空格；其后接曹震圭按语）

另核 L320–329 有字格（十、十一、十二：）与 L331 起空格相邻；L904 丙午有字、两侧空格；L1336 辛卯至戊戌有字、两侧空格。184 条源文无 mismatch。

保留 draft 1：

| paragraphId | 原因分类 | 影响 |
|---|---|---|
| `xingli-kaoyuan:shidian-SK1618:P7639153109960949787` | 缺底本 / 版面标记 | 源文「〔源段仅含版面标记，无可转存文字。〕」，无可转存文字，不升 |

notes 已改为：「源段仅为版面标记占位，无可转存文字。缺底本文字，不升 source-reviewed。」

---

### 2. `references/annotations/san-shi/daliuren-daquan.json`

| | 前 | 后 |
|---|---|---|
| draft | 845 | **817** |
| source-reviewed | 6048 | **6076** |
| 本轮升 | **28** | |

`source_status` 全库 draft 均为 `reference-text`。只升 vernacular 已完整对照电子本、notes 没有「待核 / 疑字 / 残 / 粘连待文渊阁」的条目。kind=待核实 695 条一律不升。4 条空 notes 补原因后仍不升。

**升 28 条（电子对照完成、无待核/疑字/残/粘连）：**

兵占 overlay 与异文并陈只归档，不改九宗门。抽核对照 `sources/fulltext/san-shi/daliuren-daquan/fulltext.md`：

| paragraphId | 抽核要点 |
|---|---|
| `daliuren-daquan:L6121-L6121` | L6121「一本云，时上神克日上神，亦主多诈」并行异文 |
| `daliuren-daquan:L6162-L6162` | L6162 参觜在申、初传传送与末见传送分层 |
| `daliuren-daquan:L6769-L6769` | L6769 大将军三年一移 + 捷法两说，「天罡不是也」 |
| `daliuren-daquan:L7058-L7058` | 四绝 / 天祸两说，作者自云《观月经》未知何出 |
| `daliuren-daquan:L7209-L7217` | 歌巳申子卯 vs 注丑申卯子，四神异文两存 |
| `daliuren-daquan:L7596-L7596` | L7596 丑未临方；急事魁加时孟入季出 |
| `daliuren-daquan:L7802-L7802` | L7802 宿度歌，虗/翌异体照录 |
| `daliuren-daquan:L11344-L11344` | L11344「铸印，戌加巳丙，传有太冲。不见太阴、天马，即非真体」 |

其余本轮所升：`L6154` `L6174` `L6324` `L6348` `L6372` `L6460` `L6609` `L6816` `L6861` `L6956` `L6992` `L7009` `L7019` `L7052` `L7201` `L7558-L7562` `L7578` `L7600` `L7842` `L7856`。

升审时去掉 notes 里残留的「draft」字样（如「draft 并陈」→「电子对照并陈」），不改 vernacular，不改正文。

**为何留下 817：**

| 原因（互斥） | 条数 | 说明 |
|---|---|---|
| kind=待核实 | 695 | 硬规则不升 |
| 待核 | 36 | notes/白话仍写待核 |
| 疑字/疑读 | 44 | 「宙」疑寅、已/己混、太禽/太常、戊已混等不能唯一还原 |
| 残 / 缺字 | 25 | 残格、残表、缺天干、衍字未核 |
| 粘连 | 8 | 口诀与夹注粘连 |
| 粘连待文渊阁 | 1 | `L0098` 井栏中末待文渊阁页叶 |
| 待影印 | 3 | 行序疑错位等 |
| 信息不足 | 4 | 「先克」「先举」未定义，不另造时序 |
| 异文并行、本轮只补 notes 不升 | 1 | `L10614` 心镜寅时 vs 本行午时；空 notes 补原因后仍 draft |
| **合计** | **817** | |

空 notes 4 条已补，仍为 draft：

| paragraphId | 补上的原因 |
|---|---|
| `daliuren-daquan:L9691-L9691` | 「宙」疑寅，疑字未唯一还原 |
| `daliuren-daquan:L9749-L9749` | 「先举」待与订讹对读，信息不完整 |
| `daliuren-daquan:L10235-L10235` | 与邻行地盘疑互换，待影印 |
| `daliuren-daquan:L10614-L10614` | 心镜寅时 / 本行午时异文并行，不据一行改正文 |

未升的典型（有电子对照但仍有缺口，禁止凑数）：`L9187` 缺天干+衍「加」；`L9483`「必必待」疑字；`L5931`「戍」疑戌；`L0098` 井栏粘连待文渊阁。

---

### 3. `references/annotations/san-shi/liuren-miben.json`

| | 前 | 后 |
|---|---|---|
| draft | 89 | **88** |
| source-reviewed | 2554 | **2555** |
| 本轮升 | **1** | |

升：`liuren-miben:L3632-L3632`（盗逃：用神为方、刚责中柔责末）。对照 `sources/fulltext/san-shi/liuren-miben/fulltext.md` L3632：用神为方、中传去处、末为止处；壬刚午日中传卯；金氏「卯」旁注「末」、「酉」旁注「中」。白话已完整对照；notes 无待核/残。金氏旁注不得写成正文已改传位。不升运行规则。

空 notes 14 条全部补原因，**不升**（均有疑字、粘连、缺字或信息不足）：

| paragraphId | 原因 |
|---|---|
| `L3200` | 「之利」存疑 |
| `L3204` | 「子加辰寅」粘连，是否两例待核 |
| `L3228` | Χ 标记含义待核 |
| `L3327` | 冲句缺字，残缺不补 |
| `L3453` | 「方来过去」方向含糊 |
| `L3463` | 「天惭」疑天乙 |
| `L3540` | 器用后半粘连，支神待核 |
| `L3562` | 「玄武丑」未写完 |
| `L3628` | 「亥加定」疑亥加巳 |
| `L3735` | 「叶」疑克 |
| `L3741` | 「俱同」三字信息不足 |
| `L3833` | 「巳一亥」粘连 |
| `L3839` | 「四刻一刻」叠字；过将表其余节点不足 |
| `L3914` | 用空 / 天空两句粘连 |

**留下 88：**

| 原因（互斥） | 条数 |
|---|---|
| 待核 | 41 |
| kind=待核实 | 25 |
| 粘连 | 9 |
| 疑字/存疑 | 6 |
| 信息不足/未展开 | 3 |
| 未完成全书校勘 | 2（含 `L6015-L6018` 自承不升） |
| 残/缺字 | 1 |
| 待影印 | 1 |
| **合计** | **88** |

未升例：`L3162`「蛇制鬼」与「贵德临身」如何同盘未展开；`L3055`「不腚顺」疑字改义。`liuren-miben--shidian-SDZJ0628.json` 本轮未打开。

---

### 4. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

| | 前 | 后 |
|---|---|---|
| draft | 60 | 60 |
| source-reviewed | 1010 | 1010 |
| 本轮升 | **0** | |

空 notes 9 条已补，全部是段末截断、残表或疑夺，**不为凑数升疑文**。紫微入知识库，不接入八术算法。

补 notes 的 paragraphId：

- `P7356158891736104969` — 段末未完（酉人陀刃）
- `P7356158893094862886` — 天府庙旺残表
- `P7356158893094993958` — 天相残简「𨺻夘酉」
- `P7356158893095026726` — 女命天相错简，干支格疑夺
- `P7356158893095075878` — 天梁庙旺残表
- `P7356158894496022554` — 机梁七杀段截
- `P7356158894575583241` — 日落未申段截
- `P7356158895213150246` — 昌曲投河忧段截
- `P7356158895221489702` — 武曲七杀会羊段截

留下 60：跨行残/段末未完 38；kind=待核实残表 12；疑字 6；图残/图像占位 2；缺字 1；断句紊乱不臆补 1。

---

### 5. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json`

| | 前 | 后 |
|---|---|---|
| draft | 222 | 222 |
| source-reviewed | 627 | 627 |
| 本轮升 | **0** | |

空 notes 22 条已补。全是残结、句截、跨行残。相法入知识库，不冒充已接入八术。不为凑数升疑文。

补 notes 的 paragraphId（22）：

`P7624085868030296091` `P7598367380087554088` `P7598367380087717928` `P7598367380088078376` `P7598367380088471592` `P7598367409276354575` `P7624085868030656539` `P7624086152143929353` `P7598367454154227712` `P7598367454154260480` `P7624086152143945737` `P7598367455463473186` `P7598367455463505954` `P7598367455463538722` `P7624086177419116554` `P7598367455849562127` `P7598367455849676815` `P7598367455849709583` `P7624086183316094986` `P7598367464203862016` `P7598367464204943360` `P7626030500818616346`

`mayi-shenxiang.json`（非识典层，19 draft）本轮未改。

---

### 6. 本轮明确不做

- `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json`：1261 draft，ocr-draft 校验拦截。Round1 已说明。本轮不重做升审。
- 玉匣记 267、命理约言 nlc-recovery 162、皇极经世 40、六壬秘本识典层 61 等未打开。

## 本轮保留 draft 的原因分类（仅已处理文件的剩余 draft）

| 原因 | 条数 | 文件 |
|---|---|---|
| kind=待核实 | 732 | 大六壬 695 + 秘本 25 + 紫微残表 12 |
| 待核 | 77 | 大六壬 36 + 秘本 41 |
| 疑字/疑读 | 50 | 大六壬 44 + 秘本 6 |
| 残 / 缺字 / 段末未完 | 65 | 大六壬 25 + 秘本 1 + 紫微 38+1 缺字 + 星历考原 0 |
| 粘连（含待文渊阁） | 18 | 大六壬 8+1 + 秘本 9 |
| 待影印 | 4 | 大六壬 3 + 秘本 1 |
| 信息不足 / 未展开 | 7 | 大六壬 4 + 秘本 3 |
| 缺底本 / 版面标记 | 1 | 星历考原 1 |
| 图残 / 图像占位 | 2 | 紫微 2 |
| 未完成全书校勘 | 2 | 秘本 2 |
| 异文并行只补 notes 不升 | 1 | 大六壬 `L10614` |
| 断句紊乱不臆补 | 1 | 紫微 |
| 麻衣残结/句截（本轮只补空 notes） | 222 | 麻衣识典层全部仍 draft |
| **已处理文件剩余 draft** | **1188** | 星历 1 + 大六壬 817 + 秘本 88 + 紫微 60 + 麻衣 222 |

已处理文件剩余 1+817+88+60+222 = 1188。本轮升 213。全局仍余 3013，差额 1825 是未打开文件（奇门 1261、玉匣 267、约言 162、秘本识典 61、皇极 40、麻衣主文本 19、Round1 小文件保留 15 等）。

## 实际修改的 JSON

1. `references/annotations/selection/xingli-kaoyuan--shidian-SK1618.json` — 184 条 review→source-reviewed，1 条补缺底本原因
2. `references/annotations/san-shi/daliuren-daquan.json` — 28 条升审，4 条空 notes 补原因
3. `references/annotations/san-shi/liuren-miben.json` — 1 条升审，14 条空 notes 补原因
4. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` — 9 条空 notes 补原因，review 未升
5. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json` — 22 条空 notes 补原因，review 未升

`paragraphId` 无改动。`verified: true` 出现次数仍为 0。

## 下一轮建议（不在本轮做）

1. 大六壬剩下 817 以 kind=待核实 695 为主，须先能对照电子本还原残格/疑字，禁止批量标不支持。
2. 麻衣识典层 222、玉匣记 267 仍全是 draft，按残图/句截/可核正文拆开，不要整文件升。
3. 奇门 nlc-layouts 1261 仍被 ocr-draft 拦截；若要升，须先改源层或校验器元数据例外，不是注解层能单独完成。
4. 择日/相法/紫微已核条目只进知识库，不要在产品仓接线。

## 验证命令与结果

工作目录：`/Users/yuhanglin/fateradar-goal-20260912/classics`

```bash
python3 tools/validate-annotations.py
python3 tools/validate-annotations.py --json
```

纯文本结果：

```
53 books, 62839 entries, 0 errors
```

JSON 摘要：

```json
{
  "ok": true,
  "books": 53,
  "files": 79,
  "entries": 62839,
  "source_reviewed": 59826,
  "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
  "errors": []
}
```

对照 Round1 结束 `source_reviewed` 59613 / `draft` 3226：本轮 +213 source-reviewed、−213 draft，与星历考原 184 + 大六壬 28 + 六壬秘本 1 一致。校验器声明这只是结构与段落 ID 检查，不是语义证书，更不是人工 verified。

未执行 `git commit` / `git push`。`git status` 仅古籍工作树上述 5 个注解 JSON 与本文件。
