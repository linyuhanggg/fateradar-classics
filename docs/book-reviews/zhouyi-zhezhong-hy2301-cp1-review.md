# 御纂周易折中 · 识典 HY2301：独立审查 CP1（0–299）

审查对象：`origin/codex/multica-ming-176` @ `4a6b4d9cad94aa6730fe7592db08bf89eee7215f`（父 `1fd3a37fae846d9b7cdf53824434f2fe47c868ee`，权威树 `fateradar-classics-grok-full-library`）。工作树只读参考 `fateradar-multica-ming-176`，本岗写出仅本文件。未改注解 JSON、未改源文、未改主本 `zhouyi-zhezhong.json`、HY1521 / SK1609 / SDZJ0170 / 引擎 / `chart.*`。不是御纂周易折中全书完成，也不是主本折中包，也不是引擎包，也不是全项目完成。source-reviewed ≠ 人工 verified。禁止重做主本 0–899。

结论：**通过。** 交包结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–680 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-183`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-176
git rev-parse HEAD HEAD^
git diff HEAD^..HEAD --name-only
git diff --stat HEAD^..HEAD
shasum -a 256 sources/normalized/shidianguji/HY2301/paragraphs.json
shasum -a 256 sources/normalized/shidianguji/HY2301/text.md
git rev-parse HEAD^:sources/normalized/shidianguji/HY2301/paragraphs.json
git rev-parse HEAD:sources/normalized/shidianguji/HY2301/paragraphs.json
git rev-parse HEAD^:sources/normalized/shidianguji/HY2301/text.md
git rev-parse HEAD:sources/normalized/shidianguji/HY2301/text.md
git cat-file -e HEAD^:references/annotations/divination/zhouyi-zhezhong.json
git cat-file -e HEAD:references/annotations/divination/zhouyi-zhezhong.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-176` | `4a6b4d9cad94aa6730fe7592db08bf89eee7215f`（本岗 HEAD 与 `ls-remote` 一致） |
| 父提交 | `1fd3a37fae846d9b7cdf53824434f2fe47c868ee` |
| 相对父提交文件 | 仅 2 个：`references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json`、`docs/book-reviews/zhouyi-zhezhong-hy2301-progress-2026-09-11.md` |
| diffstat | `+5298`（两文件均为新增） |
| 源 `paragraphs.json` SHA256 | `511d3e2a9a022444133ab985197a51f879d6d0f50d3e0f423243c9206a63c86c`（681 段，与 Issue / 进度一致） |
| 源 `text.md` SHA256 | `3daa58177a204d86c55bbe4156fc645f408e03a6990a07a7ee45104c1d617fc1` |
| 源 blob 父 vs 本提交 | `paragraphs.json` 同为 `23d84953106b9b0e778eb37c9c6a8ac05cbf12a4`；`text.md` 同为 `a526d7549cd522f7d4c2e0380e505808e4aeee8a`（本提交未改源层） |
| 主本 `zhouyi-zhezhong.json` | 父提交与本提交均不存在该路径（权威树基线不含主本注解；主本在 MING-151/159/165 线）。相对父提交未新增、未改写 |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 107 条，未补造） |
| `paragraphCount` / `figureCount` | 681 / 38；本包 0–299 `figureCount` 合计 0 |
| 注解 ID 与 `paragraphs.json` 0–299 | 300/300 一一对应，`mismatch=0`；未泄漏 300+；无主本 `zhouyi-zhezhong:L####` 混写 |

无越权文件。源层未改。主本折中 / 他书 / 引擎 / `chart.*` 未覆盖。`scopeNote` 已写明补本不替代主本、不作独立投票、网站章节名不直接等同印本卷号。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-176 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 300, "source_reviewed": 300,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

300 条：`review=source-reviewed` 全 300；`verified` 全 `false`；无 `draft` 字段。无升 verified。

kind：规则候选 276、理论 15、序跋目录 9（与进度一致）。

空白话 0、空 notes 0、空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组仅 1：索引 17 与 35 同为网站卷端「御纂周易折中卷第九」，源文本身重复该行，不是空模板填满。

notes 含 `unknown` / 「电子源示疑」仅 3 条：索引 23 / 26 / 27。本包 `figureCount=0`。

## 4. 索引边界

`paragraphs.json` 全书 681 段；本包注解只覆盖 0–299。进度 nextId 与源索引 300 一致，无错指全书末。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（CP1 起） | `zhouyi-zhezhong:shidian-HY2301:P7675240779413241875` |
| 注解索引 299（CP1 止） | `zhouyi-zhezhong:shidian-HY2301:P7675240944312877099` |
| 源索引 300（下一包起，不在本包） | `zhouyi-zhezhong:shidian-HY2301:P7675240944312893483` |
| 源索引 680（全书末条） | `zhouyi-zhezhong:shidian-HY2301:P7510771359308382243` |

网站章节覆盖（源 `heading`，不是印本卷号）：御製周易折中序（0–2）/ 凡例（3–15）/ 御纂周易折中卷第九（16–17）/ 彖上傳（18–35）/ 象下傳（36–299，该网站章源文续至索引 501）。索引 16–17 与 35 源行是「御纂周易折中卷第九」，白话均标「章节名不等于印本卷号核定；属目录/卷端」，未把网站章名写成印本卷次。索引 300 源是「覆公餗，信如何也。」，仍在网站章「象下傳」下。remaining 381（300–680）与进度一致。起始/止点与 Issue 钉死 ID 一致。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/HY2301/text.md` 的 `start_line–end_line`。凡例标理论、不升占断；彖/象分层保留本义·程传·集说·案；短象辞不单面取用；网站卷端不作印本卷号。下列为非模板抽核。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 / 1 | `P…241875` / `P…258259` | 序跋 / sr | 「御纂周易折中。」；「御製周易折中序」。版式/序题，不是筮法 | 通过 |
| 2 | `P…720806` | 序跋 / sr | 易学广大悉备；朱子象数天理；命李光地修折中；康熙五十四年。纂修缘起，不升占断。源末「十八曰書」白话截于「康熙五十…」 | 通过结构；见 caveat |
| 5 | `P…411305` | 理论 / sr | 「今案：易學當以朱子爲主，故列本義於先」。体例，不是爻变占法 | 通过 |
| 12 | `P…769958` | 理论 / sr | 程以易为说理之书、朱以为卜筮之教；经传先本义，不合则折中。读法分歧保留 | 通过 |
| 16–17 | `P…681883` / `P…698267` | 序跋 / sr | 「御纂周易折中」「卷第九」。网站章名 ≠ 印本卷号 | 通过 |
| 18 | `P…714651` | 序跋 / sr | 篇题「彖上傳」。网站章，不是印本卷 | 通过 |
| 22 | `P…893222` | 规则 / sr | 屯案：本义以「動乎險中」释大亨贞，程传属上句；「屯稱雲雷，解稱雷雨」。案语不升单面断 | 通过 |
| 23 | `P…909606` | 规则 / sr | 源 L211–296 蒙→需→师→比；L287「此三字疑衍文」（比吉也）。notes 保留 unknown。白话从蒙起，压缩到「師，衆也」，未写入比吉也疑衍句 | 通过结构；见 caveat |
| 26 | `P…958758` | 规则 / sr | 源 L377「同人曰。」L379「衍文」L381「此三字義文」。白话标明本义衍文 + 程传疑文，unknown，不补造 | 通过 |
| 27 | `P…975142` | 规则 / sr | 王肃本「時字在之字下」；同段后有贲「亨字疑衍」（L561）。notes 电子源示疑。白话写王肃本，未点名亨字疑衍 | 通过结构；见 caveat |
| 35–36 | `P…278675` / `P…176043` | 序跋 / sr | 再次「卷第九」；「象下傳」。卷端/传题，不是印本卷核定 | 通过 |
| 37–38 | `P…857727` / `P…023330` | 规则 / sr | 咸大象「山上有澤…虛受人」；本义「以虛而通」、程传山泽通气。短象辞不单取 | 通过 |
| 100 | `P…950571` | 规则 / sr | 明夷莅众：用明之过则伤于察，用晦乃所以为明。条件句，不单面明察 | 通过 |
| 150 | `P…398719` | 规则 / sr | 蹇四来连：当位曰实不曰正；案语「当位两字宜著九五」。案不升单面 | 通过 |
| 238 | `P…219938` | 规则 / sr | 升大象：王肃本顺作慎，古字通用。异文保留，不改字 | 通过 |
| 265 | `P…081030` | 规则 / sr | 井大象：本义津润上行 vs 程传器汲；案「须以朱子之说为长」，桔槔说并存 | 通过 |
| 292 / 299 | `P…811563` / `P…877099` | 规则 / sr | 鼎大象「正位凝命」；九三程传「失其相求之义」+案「失其义谓爻象无相应之义」。本包止此 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 书名 / 序题：L9、L11
- 御制序、李光地、康熙五十四年、十八曰书：L13–26
- 凡例朱子为主、列本义于先：L38
- 程说理 / 朱卜筮、折中异同：L76–83
- 网站卷第九：L102–104、L770
- 彖上傳篇题：L108
- 屯案云雷 / 雷雨：L208–209
- 比「此三字疑衍文」：L287
- 同人曰 / 衍文 / 此三字義文：L377–383
- 王肃本时字：L473
- 贲亨字疑衍：L561
- 象下傳篇题：L774
- 咸大象虚受：L776–788
- 明夷用晦：L1051–1054
- 蹇四当位实：L1243–1247
- 升王肃顺/慎：L1596–1602
- 井津润上行 / 桔槔并存：L1703–1709
- 鼎正位凝命：L1816–1817
- CP1 止鼎九三程传/案：L1851–1852
- 下一包起覆公餗：L1854

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。300 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/体例/本义·程传·集说·案/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本，不计独立投票，不等同易学引擎已实现。网站章节「彖上傳」「象下傳」「卷第九」是识典目录名，不是印本卷次核定。不得把 300 条 source-reviewed 写成已人工 verified。本包不是御纂周易折中全帙，也不是产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 包级 notes 套语 | 300 条 notes[0] 均为「识典 HY2301 电子语义审读…不是影印校勘或人工 verified」 | 否定升 verified，不是空白话。不回改 |
| 短象辞白话后缀 | 129 条以「象传原文：…须连同本义、程传与集说…不单句取象作断」起式；notes[-1]「短象辞不单面取用」129 | 套语后缀，前半对照源文。不是空模板。不回改 |
| 凡例白话后缀 | 12 条理论末句「说明本义优先…属读法，不直接给出爻变占法」 | 同上。不回改 |
| 索引 17 / 35 同文 | 源 L104 与 L770 均为「御纂周易折中卷第九」；白话相同且标明非印本卷号 | 电子卷端重复，不是模板填错。不回改 |
| 彖上傳大段切分 | 索引 19/23/26/27 单段跨数卦（蒙需师比、同人谦大有、随蛊临观等） | 电子切段如此。白话用省略压缩。不回改 |
| 索引 23 比吉也疑衍 | 源 L287「此三字疑衍文」；白话未引该句，只在 notes 保留 unknown | 压缩漏点。unknown 标记仍在。不回改 |
| 索引 27 亨字疑衍 | 同段源 L561「亨字疑衍」；白话写王肃本时字，未点贲亨 | 压缩漏点。notes 有电子源示疑。不回改 |
| 索引 2 「十八曰書」 | 源 L25–26；白话截于「康熙五十…」，未标 曰/日 | 电子字形，未补造为「日」。不回改 |
| 索引 26 「義文」 | 源作「此三字義文」；白话作程传疑文。孔疏「稱同人曰」仍在源 L383 | 跟源疑文提示，不改字。不回改 |
| 索引 297 集说「如诸家」 | 源集说为张子；白话「集说汇录诸家（如诸家）」 | 人名占位。本义/程传/案仍对源。不回改 |
| terms 偏泛 | 如索引 4 收「謙」（吕祖谦）、38/100 收「觀」、238 收「蒙」、200 仅「周易折中」 | 结构合法。抽核不以 terms 当规则。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **索引 23**：源段含比「此三字疑衍文」（L287）。白话压缩在师卦名，引用比彖须回源，不能只看白话。
2. **索引 27**：同段后部贲「亨字疑衍」（L561）未入白话。引用贲亨须回源。
3. **彖上傳电子大段**：19/23/26/27 一包多卦。条件/案语属于段内哪一卦，须按源行切，不能把段首卦名套到段尾。
4. **索引 2**：御制序末「十八曰書」保持电子字形，不升为康熙五十四年某日的校定纪年。
5. **网站「卷第九」**：出现在索引 16–17 与 35，只是识典卷端/篇末标记；本包起始于序、凡例，彖上之后接象下（咸起）。不得按印本卷九理解本包范围。
6. **129 条短象辞**：原文句对源，但解释在邻段本义/程传。单抽「象传原文」句不能当已分层规则。
7. **进度 nextId 正确**：CP2 从索引 **300** `zhouyi-zhezhong:shidian-HY2301:P7675240944312893483`（源「覆公餗，信如何也。」）起，remaining 381。不要从全书末 `P7510771359308382243` 起，不要重做 0–299，不要改主本折中。

## 未决（本岗不施工）

- 同人「曰」衍文 / 「義文」、比「吉也」疑衍、贲「亨字疑衍」、王肃本时字/顺作慎、十八曰书：保持 unknown，不升 verified。
- 识典待校。300 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同易学引擎已实现。
- 主本 `zhouyi-zhezhong.json` 不在本包范围；识典 0–299 审完不等于御纂周易折中全书完成。
- 索引 300–680 留给后续包，本岗不续写、不重做 0–299。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-183`。
