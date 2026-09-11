# 大六壬秘本：独立审查主本 source-reviewed CP6（索引 1500–1799）

审查对象：权威树 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-396` / 分支 `codex/multica-ming-396`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1–CP5 审查稿、未改大六壬大全 / 识典 SDZJ0170 / inventory / 引擎 / `chart.*`。不要重做 CP1–CP5（0–1499，含已 done [MING-384](mention://issue/01a0915f-4ce0-7089-9b91-79410be72a30) CP2）。不要与并行 [MING-389](mention://issue/01a09165-503b-7b84-8763-9f6958918ce7) CP4 / [MING-393](mention://issue/01a09168-b16e-737a-8793-8cdea4a474e6) CP5 写同一审查稿。本包只审注解文件索引 **1500–1799**。不是秘本全书完成，也不是人工 verified。本岗未参与六壬秘本生产。

结论：**通过。** 结构校验与 ≥15 段非模板抽样语义成立；本段 **288 SR + 12 draft**，draft 保持 draft 未升 SR；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–1499 相对权威 SHA 对象级未动。索引 **1800–2642**（remaining **843**）不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-396`，2026-09-12）：

```
git rev-parse HEAD
git branch --show-current
shasum -a 256 references/annotations/san-shi/liuren-miben.json
git hash-object references/annotations/san-shi/liuren-miben.json
git rev-parse HEAD:references/annotations/san-shi/liuren-miben.json
shasum -a 256 sources/fulltext/san-shi/liuren-miben/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
git status --porcelain
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与 Issue 钉死权威 tip 一致） |
| 分支 | `codex/multica-ming-396` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死一致） |
| 注解 blob HEAD vs working | 同为 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（未改） |
| 源 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| `bookSlug` | `liuren-miben` |
| `sourceTitle` | 大六壬秘本（现有电子主文本） |
| 对照原文 | `sources/fulltext/san-shi/liuren-miben/fulltext.md` |
| inventory 段落 ID | 本包 300/300 ID 均在 `references/inventory/paragraphs/san-shi/liuren-miben.json`（2643），全书 ID 集合全等；`missing=0`（注解文件序 ≠ inventory 行序，不以 inventory 切片对齐） |
| 本包覆盖 | 仅索引 1500–1799；起 `liuren-miben:L0563-L0563` 止 `liuren-miben:L1173-L1173`；未泄漏续写 1800+；未写其他 CP 审查稿 |
| `git status` | 交包前仅新增本审查稿 |

无越权文件。注解 JSON 未改。大六壬大全 / 识典路径未碰。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2643, "source_reviewed": 2554,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 entries=2643（sr=2554 + draft=89）；本包只审 1500–1799。JSON SHA 交包前后未变。

## 3. verified / draft 未越权提升

本包索引 1500–1799（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 288/300 |
| `review=draft` | 12/300（保持 draft，未升 SR） |
| `verified` | 全 `false`（全书 2643 亦无 true） |
| 空白话 | 0 |
| 空 terms | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 白话完全重复组 | 0 |
| 有 subsections | 0 |

kind（1500–1799）：规则候选 218、术语 55、评注或元数据 13、待核实 11、序跋目录 3。

SR 白话字数 min/median/max = 6/52/171。最短为五行标目「金。」等术语行与卷终题记，对照源文归属正确，不是空模板。

12 条 draft（`verified=false`，不补字、不升 sr）：

| 索引 | paragraphId | kind | 原因（对照源，不改正文） |
|---|---|---|---|
| 1546 | `L0658-L0658` | 规则候选 | 「青碧赤诚」疑赤色；不改正文 |
| 1673 | `L0918-L0918` | 待核实 | 「辰，太冲，氐」与常表卯太冲并列，疑错位 |
| 1680 | `L0932-L0932` | 待核实 | 「土度三五」疑十度，度数不明 |
| 1707 | `L0989-L0989` | 待核实 | 「妻獰」疑字；太阴乘酉条件保留 |
| 1710 | `L0995-L0995` | 待核实 | 「戍加壬」疑戌；不把各类寻物皆次日 |
| 1715 | `L1005-L1005` | 待核实 | 「午加戍午寅戌」粘连，课式不明 |
| 1721 | `L1017-L1017` | 待核实 | 「欲去不◎上大下厶」缺字，不补 |
| 1734 | `L1043-L1043` | 待核实 | 「九个」vs「丁癸亥辛乙未」个数不合；常人句缺字 |
| 1737 | `L1049-L1049` | 待核实 | 「辰戍亥」疑戌亥旬空 |
| 1762 | `L1099-L1099` | 待核实 | 「不肰」疑不然 |
| 1788 | `L1151-L1151` | 待核实 | 「三渊兮在水泮」句残，不补起例 |
| 1794 | `L1163-L1163` | 待核实 | 「辰戍丑未」疑辰戌丑未 |

符合「draft 保持 draft，不得升 SR」。

## 4. 索引边界

注解全书 2643 条。本包只审注解索引 1500–1799（按文件索引，不以行号单调为准——本段内源行起点实际单调升序）。

| 位置 | 实测 ID | 行号 |
|---|---|---|
| 注解索引 1499（上一包止，冻结） | `liuren-miben:L0561-L0561` | L0561 |
| 注解索引 1500（CP6 起） | `liuren-miben:L0563-L0563` | L0563 |
| 注解索引 1799（CP6 止） | `liuren-miben:L1173-L1173` | L1173 |
| 注解索引 1800（下一包起，不在本包） | `liuren-miben:L1175-L1175` | L1175 |

起止与 Issue 钉死一致。本包后 remaining **843**（索引 1800–2642）。

约略覆盖（按源行）：八卦属十二将物类（巽天罡起）→ 卷五天官加十二辰射覆物类与卷五终 → 卷六八卦将神射覆法与卷六终 → 卷七十干旺相死休囚、五行物类、二十八宿周天度位与卷七终 → 卷八李九万六壬百章歌至「三传俱是日之鬼」条。不延伸至下一 `L1175`。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（优先 SR；draft 抽核但不升格）。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 1500 | `L0563-L0563` | 术语 / sr | 巽天罡数五杂木城市；股官司山野东南方圆 | 通过 |
| 1505 | `L0573-L0573` | 术语 / sr | 兑从魁数六酉纯金尖圆金钱 | 通过 |
| 1520 | `L0606-L0606` | 规则 / sr | 贵加子文书、丑鱼蟹泥土、寅窑冶砖瓦，分象不调 | 通过 |
| 1540 | `L0646-L0646` | 规则 / sr | 勾临日辰青黑木植勾连罗网，变异瓦砖金钱鱼蟹 | 通过 |
| 1560 | `L0686-L0686` | 规则 / sr | 虎加辰铜铁环、巳金帛孝服、午烧药破碎，分象 | 通过 |
| 1580 | `L0726-L0726` | 规则 / sr | 后加未伤凶赤、申虎鼠、酉白衣、戌黄泥黄衣 | 通过 |
| 1600 | `L0769-L0769` | 序跋 / sr | 鬼撮脚卷六终；卷终题记不是占法 | 通过 |
| 1620 | `L0812-L0812` | 规则 / sr | 土木用加日辰才陆地 | 通过 |
| 1625 | `L0822-L0822` | 规则 / sr | 天元六甲医病四时五脏 vs 课式三十日三周/旬十日一递，分用不塌 | 通过 |
| 1660 | `L0892-L0892` | 规则 / sr | 火相＝灯烛 | 通过 |
| 1700 | `L0975-L0975` | 评注 / sr | 原本空白四行；版本说明不是占法 | 通过 |
| 1720 | `L1015-L1015` | 规则 / sr | 罡加卯乘勾寻斗/争田；畎疑亩不改正文 | 通过 |
| 1750 | `L1075-L1075` | 规则 / sr | 巳上武才舟车覆行阻，不得凡武皆覆舟 | 通过 |
| 1780 | `L1135-L1135` | 规则 / sr | 四仲入传未入月不可偕；凶将+天目隐胎 | 通过 |
| 1790 | `L1155-L1155` | 规则 / sr | 课名参《玉历》；勿以断语告占者，不是取传法 | 通过 |
| 1799 | `L1173-L1173` | 规则 / sr | 三传皆鬼，庚辛炎上才功名遂宜从官；常人仍忌 | 通过 |
| 1546 | `L0658-L0658` | 规则 / draft | 青碧赤诚疑赤色；不改正文、不升 SR | 通过（draft 保留） |
| 1673 | `L0918-L0918` | 待核实 / draft | 辰太冲氐疑错位；不据别本改 | 通过（draft 保留） |
| 1710 | `L0995-L0995` | 待核实 / draft | 戍疑戌；壬日条件保留 | 通过（draft 保留） |
| 1734 | `L1043-L1043` | 待核实 / draft | 九个 vs 六日表；缺字不补 | 通过（draft 保留） |
| 1788 | `L1151-L1151` | 待核实 / draft | 三渊兮句残；不补起例 | 通过（draft 保留） |
| 1794 | `L1163-L1163` | 待核实 / draft | 辰戍丑未疑戌；不改正文 | 通过（draft 保留） |

抽核未见把 draft 升 SR、未见把 verified 置 true、未见空模板白话冒充 SR、未见邻段 vernacular 错位。失败 paragraphId：无。

## 6. Caveat（不构成本包失败）

1. 12 条 draft 的疑字、缺字、宿度错位、歌注残句等仍待核；本审查只确认处置正确，不重写、不升格。
2. 部分 SR 条（如 `L1015` 畎疑亩）白话内标疑字但仍标 SR；条件绑定与源文一致，不据此失败，也不升 verified。
3. 最短白话（五行标目、卷终行）信息量低，但与源行一一对应，不是「白话从略」模板。
4. source-reviewed ≠ 人工 verified；电子全文不是影印校勘。
5. 本包不覆盖索引 0–1499（CP1–CP5）与 1800–2642（后续包）。

## 7. 交包边界

| 项 | 值 |
|---|---|
| 权威 tip | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（未变） |
| 本岗写出 | 仅 `docs/book-reviews/liuren-miben-cp6-review.md` |
| 结论 | **通过** |
| remaining | 索引 **1800–2642**（843 条） |
| 下一未纳入 | `liuren-miben:L1175-L1175` |
