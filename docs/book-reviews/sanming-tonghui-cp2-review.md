# 三命通会主本：独立审查 CP2（300–599）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。工作树 `fateradar-multica-ming-290`，分支 `codex/multica-ming-290`。本岗写出仅本文件。未改注解 JSON、未改源文、未改识典 HY1521 / 珞琭子 / 引擎 / `chart.*` / `sanming-tonghui-cp1-review.md`。不是三命全书完成，也不是产品交付，也不是全项目完成。审查岗未参与本包生产。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–299 属 [MING-287](mention://issue/01a090a9-0aa1-71c0-8349-de247fcc6647)，本包不抢写。索引 600–969 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-290`，2026-09-11）：

```
git rev-parse HEAD
shasum -a 256 references/annotations/bazi/sanming-tonghui.json
git rev-parse HEAD:references/annotations/bazi/sanming-tonghui.json
cmp HEAD blob vs working tree
shasum -a 256 sources/fulltext/bazi/sanming-tonghui/fulltext.md
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` | `bc798566da77c30e149abf9673c88ecc386702b2`（与 Issue 钉死权威 SHA 一致） |
| 注解 SHA256 | `e68ec2914045631685c309b13b884c0089aa4ea4b8e1a2596dd782d84e2f042b`（与 Issue 一致） |
| 注解 git blob | `453b20ac9d2c35ca926bd4902522b6175c17eeb6` |
| working tree vs `HEAD` blob | 相同 |
| 源 `fulltext.md` SHA256 | `ef01ff5ff538a2c64af7fda15b1393b4eeb9f75a311fe3dda7f39f0ecaa66298` |
| 源 git blob | `61cfa939350e4acbfd15267facddc528f19658ee` |
| 本岗改动文件 | 仅新增 `docs/book-reviews/sanming-tonghui-cp2-review.md` |
| `sanming-tonghui-cp1-review.md` | 本树不存在，未创建、未改 |

无越权文件。源层未改。注解 JSON 未改。CP1 审查文件未抢写。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/sanming-tonghui.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 970, "source_reviewed": 970,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

全书 970 条：`review=source-reviewed` 全 970；`verified` 全 `false`；无 `draft`。无升 verified。

kind：理论 958、评注或元数据 8、术语 2、序跋目录 1、操作步骤 1。

空白话 0、空 terms 970（全书约定，条件写在 vernacular / subsections，见 caveat）、空 notes 42。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。

CP2（300–599）300 条：`review=source-reviewed` 全 300；`verified` 全 `false`。kind：理论 298、评注或元数据 2。空 notes 16、空 terms 300、subsections 792、`cases` 119 条共 298 个 `source_case`，`expected` 全 `null`（252 `canRecompute=true`，46 `false`，非法干支不改正文）。

## 4. 索引 0–299 相对权威 SHA 未改

本岗 HEAD 即权威 SHA，working tree 注解字节与 `HEAD` blob 相同，故 0–299 相对钉死 SHA 未改。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起，不评） | `sanming-tonghui:L0003-L0006` |
| 注解索引 299（CP1 止，不评） | `sanming-tonghui:L3031-L3031` |
| 0–299 paragraphId 集 SHA256 | `38c12477d0865d5a17a3b03c53871dc7fb959f880233320aebe2b140ffc7cec7` |

CP1 300 条同样 `source-reviewed` / `verified=false`。本包不评其语义，不写 `sanming-tonghui-cp1-review.md`。

## 5. 索引边界（本包 300–599）

| 位置 | 实测 ID |
|---|---|
| 注解索引 300（CP2 起） | `sanming-tonghui:L3035-L3036` |
| 注解索引 599（CP2 止） | `sanming-tonghui:L6005-L6029` |
| 注解索引 600（下一包起，不在本包） | `sanming-tonghui:L6033-L6051` |
| 注解索引 969（当前主本末条） | `sanming-tonghui:L10098-L10128` |

起讫与 Issue 钉死 locator 一致。下一未纳入即 `sanming-tonghui:L6033-L6051`（六戊日壬子时）。300–599 与源行号一一对应；索引 299 与 300 之间源为空白/「金木間隔」标题，未并入本包。remaining 370（600–969）与 Issue 账本一致。

CP2 覆盖卷六题记、卷七题记、卷八题记及卷六格局至卷八六丁日辛亥时。网站/库存卷号与印本编次并存，引用仍以段落 ID 为准。

## 6. 抽样语义（23 段非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/bazi/sanming-tonghui/fulltext.md` 的 `start_line–end_line`。格局条件/救应/反转/未知去向多数成立；命例一律 `expected=null`；女命、小儿、时辰断的历史分类未转成对现实用户的婚姻、生育、刑案或寿命判断。下列为非模板抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L3035-L3036` | 理论 / sr | 「木若逢金间隔」；杨博己巳庚午乙卯庚辰乙坐卯两庚间隔，与庚申戊子乙酉甲申乙弱从夫化金分路。两例 `expected=null` | 通过 |
| 311 | `L3080-L3098` | 理论 / sr | 偏官七杀：有制偏官/无制七杀；制过多失用；身旺杀弱财吉 vs 身弱杀强财引鬼；用杀不用印与煞不离印并列表。`{{SKchar\|3741}}` 缺字留存 | 通过 |
| 315 | `L3120-L3122` | 理论 / sr | 弃命从杀须无比印；阴干易从、阳木不能从为本书说，不扩成唯一从格 | 通过 |
| 316 | `L3126-L3126` | 理论 / sr | 时杀归库：乙辛丑时辛杀坐库；六辛戊戌时戊对辛为正印，与标题不合，标疑待校不改字 | 通过 |
| 318 | `L3134-L3135` | 理论 / sr | 官杀混杂「不可以混杂为贱」；三例官从戊化/丁壬化木/辛禄胜杀。第一例戊藏未透、第三例无丑，不补实支 | 通过 |
| 323 | `L3173-L3190` | 理论 / sr | 正财：身财相称；先印后财 vs 先财后印；身弱喜比刃与忌比劫分层；暗生官不添实官 | 通过 |
| 332 | `L3239-L3239` | 理论 / sr | 弃命从财：丁酉月庚辛多、日干无气；运财官与南方扶根喜忌相反 | 通过 |
| 335 | `L3261-L3290` | 理论 / sr | 印绶：年虚透不够；官为印根≠通根；丙卯子运反坏印、乙亥须财土制水，作者明言不可执泥 | 通过 |
| 344 | `L3351-L3396` | 理论 / sr | 伤官伤尽两法仍须身财或印；丁未丁未丙午丙午伤尽无财仍贫。L3373 内嵌论食神，不拆 ID | 通过 |
| 345 | `L3400-L3407` | 理论 / sr | 飞天禄马：庚子壬子辛亥癸亥冬月并冲虚邀；丑绊/寅绊对象不同，不添午巳。作者划界庚子辛亥是伤官、壬子癸亥非 | 通过 |
| 348 | `L3424-L3424` | 理论 / sr | 福星贵人：甲丙寅丙子以年遁；「若以日遁则非」，不拿日干表冒充本篇 | 通过 |
| 355 | `L3457-L3486` | 理论 / sr | 阳刃：五阳有刃五阴无刃是书内格法，不删阴干羊刃落柱；身弱可借刃、身强才怕夺；壬丙子午冲与前怕冲并列表 | 通过 |
| 357 | `L3505-L3505` | 评注 / sr | 卷六「钦定四库全书」题记，不增术法 | 通过 |
| 365 | `L3565-L3566` | 理论 / sr | 飞财：戊寅巳未戊寅甲寅月干「巳」非法，`canRecompute=false`，不改己未/戊未；三寅冲申不补申 | 通过 |
| 374 | `L3624-L3629` | 理论 / sr | 拱禄拱贵须同干日時虚夹，忌填实；戊子甲寅被克不能拱；月令有用先取提纲 | 通过 |
| 500 | `L4290-L4292` | 理论 / sr | 拱揖阙门：年对宫为阙；七十二格只列部分不补齐；己/巳疑字原留 | 通过 |
| 518 | `L4373-L4373` | 评注 / sr | 卷七四库题记 | 通过 |
| 536 | `L4545-L4546` | 理论 / sr | 旺夫伤子：丙戌丙申丁巳辛亥合法；「丁坐已」与日支巳并存不改字。伤子不是生育预测 | 通过 |
| 544 | `L4753-L4781` | 理论 / sr | 论小儿：关煞岁数只存原文；作者自言百中经多不验、诸说不尽验。不转儿科诊断 | 通过 |
| 551 | `L4867-L4867` | 理论 / sr | 卷八库题，无命理条文。kind 与卷六/七评注不一致，见 caveat | 通过结构 |
| 552 | `L4871-L4895` | 理论 / sr | 六甲日甲子时：子遥巳格忌丑绊午冲。年月官衔混排不串配四柱；`{{SKchar\|2824}}` 缺字不补；灾祸身份不设 expected | 通过 |
| 560 | `L5082-L5099` | 理论 / sr | 库存标题「申时断」、正文壬申；明枭暗鬼、丙戌原字保留。不改库存 ID | 通过 |
| 599 | `L6005-L6029` | 理论 / sr | 六丁日辛亥时：财官双美印长生，通月气/不通分论。洪朝选卒于狱、何汝健子孙进士不另造盘；本包止此 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 金木间隔、杨博与从夫化金两路：L3035–L3036
- 偏官有制/无制、制过多、财为杀根：L3080–L3090
- 弃命从杀阴从阳木不能从：L3120–L3122
- 时杀归库乙辛丑 vs 六辛戊戌：L3126
- 官杀混杂三例不可概贱：L3134–L3135
- 正财身财相称、先印后财：L3173–L3178
- 弃命从财忌根气：L3239
- 印绶官运可坏、财运可救：L3286–L3288
- 伤官伤尽反例丙午叠火：L3359–L3360
- 飞天禄马作者划界：L3400–L3407
- 福星贵人年遁非日遁：L3424
- 阳刃身弱借刃、非刃制约例：L3457–L3467
- 卷六题记：L3505
- 飞财非法月柱巳未：L3565–L3566
- 拱禄填实则凶：L3624–L3629
- 拱揖阙门：L4290–L4292
- 卷七题记：L4373
- 旺夫伤子丙戌丙申丁巳辛亥：L4545–L4546
- 小儿关煞不尽验：L4753–L4760
- 卷八题记：L4867
- 甲子时子遥巳、官衔不串配：L4871–L4875
- 壬申时库存标题/正文：L5082–L5083
- 丁亥时财官印、本包止：L6005–L6029
- 下一包起六戊日壬子：L6033–L6051

## 7. source-reviewed ≠ 人工 verified

主本 `sourceTitle` 为四库全书本主文本。本包 300 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了条件/救应/反转/未知去向，不是影印逐字校勘，也不是预测有效证据。命例一律 `expected=null`。不得把 970 条 source-reviewed 写成已人工 verified。本包不是三命全帙，也不是产品交付。

## 8. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 空 terms | 全书 970、CP2 300 条 `terms=[]` | 条件写在 vernacular/subsections，不是空白话。不回改 |
| notes 空 | CP2 16/300（短格/题记为主：324–328、347–350、357、374–377、418–419、422、518） | 校验器允许。不回改 |
| notes 套语 | 多条 notes 以「原文/ID/verified保持…无日期或效验 expected」起句 | 否定升 verified，不是空模板。不回改 |
| 卷端 kind 不一致 | 卷六/卷七题记 `评注或元数据`；卷八（551）及后续卷九–十二标 `理论` | 白话正确标编次、无术法。kind 不齐，不回改 |
| JSON `scopeNote` 过时 | 仍写「当前151主段至L1428、269小节，下一L1432三奇」；实测 entries=970 至 L10128 | 头部账本滞后。禁止改 JSON |
| 库存标题 ≠ 正文时干 | 如 560 标题申时、正文壬申；同类六甲/六乙/六丙日支标题 | 白话已点明，不改库存 ID |
| 长段合并 | 543 招嫁不定 L4582–L4749；544 小儿；344 伤官内嵌食神；时辰断按日时一组 | 不拆 ID。不是空模板 |
| 疑字/缺字 | `{{SKchar|…}}`、己/巳、非法干支（巳未、庾戌等）46 例 `canRecompute=false` | 不补字、不修柱。不回改 |

## 未决（本岗不施工）

- Checkpoint 3 起于源索引 600：`sanming-tonghui:L6033-L6051`；当前主本仍余 370 段（600–969）。
- CP1（0–299）由 MING-287 独立审查，本包不评、不抢文件。
- 本审查不把任何条目标成人工 verified。
- 不宣称三命全书完成，不计入最新版八术页面交付。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-290`。
