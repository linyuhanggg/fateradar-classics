# 大六壬秘本：独立审查主本 source-reviewed CP8（索引 2100–2399）

审查对象：权威树 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-406` / 分支 `codex/multica-ming-406`（古籍仓 `linyuhanggg/fateradar-classics`）。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1–CP7 审查稿、未改大六壬大全 / 识典 SDZJ0170 / inventory / 引擎 / `chart.*`。不要重做 CP1–CP7（0–2099，含已 done [MING-401](mention://issue/01a09171-2869-79d4-90a0-fa858264cd5e)）。不要与并行 [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) JSON 修复抢写。本包只审注解文件索引 **2100–2399**。不是秘本全书完成，也不是人工 verified。本岗未参与六壬秘本生产。

结论：**通过。** 结构校验与 ≥15 段非模板抽样语义成立；本段 **298 SR + 2 draft**，draft 保持 draft 未升 SR；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–2099 相对权威 SHA 对象级未动。索引 **2400–2642**（remaining **243**）不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-406`，2026-09-12）：

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
| 审查时 `HEAD` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与 Issue 钉死权威 tip 一致；只读基线） |
| 分支 | `codex/multica-ming-406` @ 古籍仓（相对 `origin/codex/multica-ming-329` @ `6effd8e4`；见 §7） |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死一致） |
| 注解 blob HEAD vs working | 同为 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（未改） |
| 源 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| `bookSlug` | `liuren-miben` |
| `sourceTitle` | 大六壬秘本（现有电子主文本） |
| 对照原文 | `sources/fulltext/san-shi/liuren-miben/fulltext.md` |
| inventory 段落 ID | 本包 300/300 ID 均在 `references/inventory/paragraphs/san-shi/liuren-miben.json`（2643），全书 ID 集合全等；`missing=0`（注解文件序 ≠ inventory 行序，不以 inventory 切片对齐） |
| 本包覆盖 | 仅索引 2100–2399；起 `liuren-miben:L1781-L1781` 止 `liuren-miben:L2501-L2501`；未泄漏续写 2400+；未写其他 CP 审查稿 |
| `git status` | 交包前仅新增本审查稿 |

无越权文件。注解 JSON 未改。大六壬大全 / 识典路径未碰。MING-397 JSON 修复未碰。

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

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 entries=2643（sr=2554 + draft=89）；本包只审 2100–2399。JSON SHA 交包前后未变。

## 3. verified / draft 未越权提升

本包索引 2100–2399（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 298/300 |
| `review=draft` | 2/300（保持 draft，未升 SR） |
| `verified` | 全 `false`（全书 2643 亦无 true） |
| 空白话 | 0 |
| 空 terms | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 白话完全重复组 | 0 |
| 有 subsections | 4（`L2013-L2028`、`L2052-L2064`、`L2116-L2125`、`L2155-L2166`；子段与源行块对齐） |

kind（2100–2399）：规则候选 267、术语 20、案例 6、评注或元数据 3、操作步骤 2、待核实 2。

SR 白话字数 min/median/max = 9/42/221。最短为天干神名表短行（如「丁未：名屈，字玉。」）与孤虚表（「甲子旬：孤戌亥，虚辰巳。」），对照源文归属正确，不是空模板。

2 条 draft（`verified=false`，不补字、不升 sr）：

| 索引 | paragraphId | kind | 原因（对照源，不改正文） |
|---|---|---|---|
| 2137 | `L1855-L1855` | 待核实 | 「若罡在日辰，旦名」句残疑字；前过后退可读，不补「旦名」 |
| 2375 | `L2453-L2453` | 待核实 | 「火道__灭失其明」缺字；火明水暗大意可辨，不据缺字补成完整口诀 |

符合「draft 保持 draft，不得升 SR」。

## 4. 索引边界

注解全书 2643 条。本包只审注解索引 2100–2399（按文件索引；本段内源行起点单调升序）。

| 位置 | 实测 ID | 行号 |
|---|---|---|
| 注解索引 2099（上一包止，冻结） | `liuren-miben:L1779-L1779` | L1779 |
| 注解索引 2100（CP8 起） | `liuren-miben:L1781-L1781` | L1781 |
| 注解索引 2399（CP8 止） | `liuren-miben:L2501-L2501` | L2501 |
| 注解索引 2400（下一包起，不在本包） | `liuren-miben:L2503-L2503` | L2503 |

起止与 Issue 钉死一致。本包后 remaining **243**（索引 2400–2642）。

约略覆盖（按源行）：卷之十通天鬼翼赋续（辰卑幼逆、三传生克顺逆、相旺休死囚鬼、刚柔男女、天罡前后、涉害浅深隔、副将同宫、孤虚、天门地户禹步、六丁神名）→ `L2193` 卷之十一大六壬玉成歌注解（进神、盗程里数、见机、墓神、子孙太阴劫杀、水乘火将、岁神朝廷、支用传干、火星明暗、关神飞祸、成神四孟）止 `L2501`。不延伸至下一 `L2503` 天目春辰。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（优先 SR；draft 抽核但不升格）。另做邻段 vern 前向错位扫描：0 条。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 2100 | `L1781-L1781` | 规则 / sr | 辰象卑幼；辰克日上神才逆；与上条日尊对翻不得塌 | 通过 |
| 2110 | `L1801-L1801` | 案例 / sr | 初子末申子加母逆 vs 初寅末午母见子顺；案例不升 verified | 通过 |
| 2120 | `L1821-L1821` | 规则 / sr | 相/旺/休/死/囚鬼五层分占，不得凡鬼皆官 | 通过 |
| 2130 | `L1841-L1841` | 规则 / sr | 刚柔上下内外推男女忧疑；条件见次条，不得凡刚皆男 | 通过 |
| 2150 | `L1900-L1900` | 规则 / sr | 涉害浅深：火临水江河、土临寅卯山林、金临丙丁消折、水临庚辛兵贼；与穿杨表并行不覆盖 | 通过 |
| 2165 | `L1941-L1941` | 规则 / sr | 传中副将同宫贼日才灾发；条件见次条 | 通过 |
| 2180 | `L2009-L2009` | 规则 / sr | 天门地户+神符杜门+玉女禹步合看逃亡；不改取传 | 通过 |
| 2182 | `L2013-L2028` | 规则 / sr（含子段） | 九天九地四季上下+八门分占；秋地下寅 ≠ 大全秋胜光，并行 | 通过 |
| 2192 | `L2052-L2064` | 操作 / sr（含子段） | 六神锦囊、玉女六丁、禹步三/九步、咒画地；金氏改辰待核不改正文 | 通过 |
| 2200 | `L2080-L2080` | 案例 / sr | 丙子魁阴武财传阻隔；「从鬼」疑从魁待核，案例不升 verified | 通过 |
| 2220 | `L2129-L2129` | 规则 / sr | 末传进神才进发 vs 路上不见才盘桓 | 通过 |
| 2240 | `L2180-L2180` | 规则 / sr | 盗所临数相乘得里；囚死则减，不得旺相例减 | 通过 |
| 2260 | `L2223-L2223` | 规则 / sr | 见机两用艰辛、疑惑先难后易；不改九宗门 | 通过 |
| 2280 | `L2263-L2263` | 规则 / sr | 墓加日才滞；支煞临干才迍；不得凡墓即滞 | 通过 |
| 2300 | `L2303-L2303` | 规则 / sr | 子孙+太阴劫杀；甲乙火神客欺主；三传支阴+凶将阴人口舌，三路并列 | 通过 |
| 2320 | `L2343-L2343` | 规则 / sr | 水乘火将惊恐；勾雀同传争讼 | 通过 |
| 2340 | `L2383-L2383` | 规则 / sr | 太岁加干支才望朝廷 | 通过 |
| 2355 | `L2413-L2413` | 规则 / sr | 支用传干他从己 vs 干传辰上我随人 | 通过 |
| 2370 | `L2443-L2443` | 规则 / sr | 传财将被克才分财破失；壬癸火财上见水将玄后为例 | 通过 |
| 2385 | `L2473-L2473` | 规则 / sr | 关神入传日辰＝讼狱；飞祸忌临辰 | 通过 |
| 2399 | `L2501-L2501` | 规则 / sr | 成神正巳顺四孟+吉将并才事成 | 通过 |
| 2137 | `L1855-L1855` | 待核实 / draft | 「旦名」句残；前过后退可读；不升 SR | 通过（draft 保留） |
| 2375 | `L2453-L2453` | 待核实 / draft | 「火道__灭」缺字；不补口诀；不升 SR | 通过（draft 保留） |

抽核未见把 draft 升 SR、未见把 verified 置 true、未见空模板白话冒充 SR、未见邻段 vernacular 错位。失败 paragraphId：无。

## 6. Caveat（不构成本包失败）

1. 2 条 draft 的句残/缺字仍待核；本审查只确认处置正确，不重写、不升格。
2. 部分 SR 条白话内标疑字（如「从鬼」疑从魁、「醜」疑丑）或旁注待核，但仍标 SR；条件绑定与源文一致，不据此失败，也不升 verified。
3. 最短白话（天干神名、孤虚短表）信息量低，但与源行一一对应，不是「白话从略」模板。
4. source-reviewed ≠ 人工 verified；电子全文不是影印校勘。
5. 本包不覆盖索引 0–2099（CP1–CP7）与 2400–2642（后续包）。
6. [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) 若后续改 JSON，本审查钉死的 SHA `30b9b2b9…` 需另核；本包不以 397 未完阻断。

## 7. 交包边界

| 项 | 值 |
|---|---|
| 权威 tip（只读审查基线） | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本地 worktree；`origin` 上该 tip/分支当时不可拉取） |
| 古籍仓交包 tip | 分支 `codex/multica-ming-406` @ `linyuhanggg/fateradar-classics`（精确 tip 见本 Issue 交包评论；相对 `6effd8e4` 仅本审查稿） |
| 产品仓 tip | 作废作关闭依据（`bd00b00` 等）；不以产品仓关闭本 Issue |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（未变） |
| 本岗写出 | 仅 `docs/book-reviews/liuren-miben-cp8-review.md` |
| 结论 | **通过** |
| remaining | 索引 **2400–2642**（243 条） |
| 下一未纳入 | `liuren-miben:L2503-L2503` |
