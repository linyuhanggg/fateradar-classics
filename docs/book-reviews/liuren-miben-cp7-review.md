# 大六壬秘本：独立审查主本 source-reviewed CP7（索引 1800–2099）

审查对象：权威树 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-401` / 分支 `codex/multica-ming-401`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1–CP6 审查稿、未改大六壬大全 / 识典 SDZJ0170 / inventory / 引擎 / `chart.*`。不要重做 CP1–CP6（0–1799，含已 done [MING-393](mention://issue/01a09168-b16e-737a-8793-8cdea4a474e6)/[MING-396](mention://issue/01a0916a-b38b-7470-9956-fde684d120ff)）。不要与并行 [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) JSON 修复抢写。本包只审注解文件索引 **1800–2099**。不是秘本全书完成，也不是人工 verified。本岗未参与六壬秘本生产。

结论：**通过。** 结构校验与 ≥15 段非模板抽样语义成立；本段 **290 SR + 10 draft**，draft 保持 draft 未升 SR；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–1799 相对权威 SHA 对象级未动。索引 **2100–2642**（remaining **543**）不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-401`，2026-09-12）：

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
| 分支 | `codex/multica-ming-401` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死一致） |
| 注解 blob HEAD vs working | 同为 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（未改） |
| 源 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| `bookSlug` | `liuren-miben` |
| `sourceTitle` | 大六壬秘本（现有电子主文本） |
| 对照原文 | `sources/fulltext/san-shi/liuren-miben/fulltext.md` |
| inventory 段落 ID | 本包 300/300 ID 均在 `references/inventory/paragraphs/san-shi/liuren-miben.json`（2643），全书 ID 集合全等；`missing=0`（注解文件序 ≠ inventory 行序，不以 inventory 切片对齐） |
| 本包覆盖 | 仅索引 1800–2099；起 `liuren-miben:L1175-L1175` 止 `liuren-miben:L1779-L1779`；未泄漏续写 2100+；未写其他 CP 审查稿 |
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

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 entries=2643（sr=2554 + draft=89）；本包只审 1800–2099。JSON SHA 交包前后未变。

## 3. verified / draft 未越权提升

本包索引 1800–2099（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 290/300 |
| `review=draft` | 10/300（保持 draft，未升 SR） |
| `verified` | 全 `false`（全书 2643 亦无 true） |
| 空白话 | 0 |
| 空 terms | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 白话完全重复组 | 0 |
| 有 subsections | 0 |

kind（1800–2099）：规则候选 202、术语 63、评注或元数据 16、案例 10、待核实 9。

SR 白话字数 min/median/max = 12/60/208。最短为释句「刺龙指腿上之人。释刺腿。」与地支将神宿度短行，对照源文归属正确，不是空模板。

10 条 draft（`verified=false`，不补字、不升 sr）：

| 索引 | paragraphId | kind | 原因（对照源，不改正文） |
|---|---|---|---|
| 1843 | `L1261-L1261` | 待核实 | 「太与妇人」太字不明，疑太常或太岁；不补将 |
| 1890 | `L1355-L1355` | 待核实 | 「蟛鬼」疑井鬼；不据别本改 |
| 1893 | `L1361-L1361` | 待核实 | 「戍」疑戌，「硅娄」疑奎娄；不改正文 |
| 1907 | `L1392-L1392` | 术语 | 「虎孝家、公吏、屠 」句末缺，不补 |
| 1922 | `L1422-L1422` | 待核实 | 戊寅段既写立至又写飞神带马来迟，冲突待核 |
| 1940 | `L1458-L1458` | 待核实 | 「又在在乙前」乙疑贵；不据别本改 |
| 1957 | `L1492-L1492` | 待核实 | 「或干贵或」句残，不补字 |
| 1992 | `L1562-L1562` | 待核实 | 句末「庚辛」残缺，不补 |
| 2077 | `L1732-L1732` | 待核实 | 「若因青龙若归踪」句涩疑字，不补 |
| 2081 | `L1740-L1740` | 待核实 | 「爱克」疑受克；案例不升 verified |

符合「draft 保持 draft，不得升 SR」。

## 4. 索引边界

注解全书 2643 条。本包只审注解索引 1800–2099（按文件索引；本段内源行起点单调升序）。

| 位置 | 实测 ID | 行号 |
|---|---|---|
| 注解索引 1799（上一包止，冻结） | `liuren-miben:L1173-L1173` | L1173 |
| 注解索引 1800（CP7 起） | `liuren-miben:L1175-L1175` | L1175 |
| 注解索引 2099（CP7 止） | `liuren-miben:L1779-L1779` | L1779 |
| 注解索引 2100（下一包起，不在本包） | `liuren-miben:L1781-L1781` | L1781 |

起止与 Issue 钉死一致。本包后 remaining **543**（索引 2100–2642）。

约略覆盖（按源行）：卷八李九万六壬百章歌续（三传相续、戌亥加支朱雀等）→ `L1365` 卷八九万百章歌终 → 卷之九六壬穿杨百章歌（十二将宿度、行人、占婚、官讼、回禄、鬼三合、失脱、病症等）→ `L1765` 卷之十通天鬼翼赋起至「日者尊长官人…克辰上神，顺也」。不延伸至下一 `L1781`。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（优先 SR；draft 抽核但不升格）。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 1800 | `L1175-L1175` | 规则 / sr | 三传相续才事叠至；吉凶随神将，不得凡相续皆凶 | 通过 |
| 1810 | `L1195-L1195` | 规则 / sr | 戌亥加支乘雀才斛斗；乘常/龙才典质满架，分象不调 | 通过 |
| 1825 | `L1225-L1225` | 规则 / sr | 甲子乙亥土神篱倒；乘虎男虚女血儿胀；狞字不改正文 | 通过 |
| 1840 | `L1255-L1255` | 规则 / sr | 申加巳玄胎；六合内战子孙灾；占事迟疑 vs 期约儿孙分占 | 通过 |
| 1860 | `L1295-L1295` | 评注 / sr | 金氏旁注罡/魁校记，不是占法改写 | 通过 |
| 1880 | `L1335-L1335` | 规则 / sr | 四墓覆四生才病讼仇再发；不得凡墓皆再发 | 通过 |
| 1900 | `L1378-L1378` | 规则 / sr | 太岁吉将克日辰+年值天乙才得官；不得单见太岁克日 | 通过 |
| 1910 | `L1398-L1398` | 规则 / sr | 龙受克难图 vs 龙克岁利有余；用空财除，止于求财 | 通过 |
| 1935 | `L1448-L1448` | 规则 / sr | 千里贵前、倍此贵后；前去后归第五辰，不补里数演算 | 通过 |
| 1950 | `L1478-L1478` | 规则 / sr | 无克战刑害才子天后女妍、丑天乙男俊 | 通过 |
| 1970 | `L1518-L1518` | 规则 / sr | 涉害用火临壬癸隔江津 vs 土临甲寅山林隔 | 通过 |
| 1990 | `L1558-L1558` | 规则 / sr | 午加支蛇+寅日才回禄；壬寅午加寅例；案例不升 verified | 通过 |
| 2010 | `L1598-L1598` | 规则 / sr | 鬼三合：戊己木局鬼旺、庚辛炎上不利 | 通过 |
| 2030 | `L1638-L1638` | 规则 / sr | 武乘二马逾垣；地户水窗 vs 天门绳来 | 通过 |
| 2050 | `L1678-L1678` | 术语 / sr | 阴乘卯在东方，释太阴乘方为逃处 | 通过 |
| 2070 | `L1718-L1718` | 规则 / sr | 辛日子加罡作虎难医；午蛇临酉另详 | 通过 |
| 2090 | `L1758-L1758` | 规则 / sr | 盗神两路：旬前一位 OR 春卯夏午秋酉冬子 | 通过 |
| 2099 | `L1779-L1779` | 规则 / sr | 日象尊长；日克辰上神才顺 | 通过 |
| 1843 | `L1261-L1261` | 待核实 / draft | 太字不明；病死与讼枷分占；不升 SR | 通过（draft 保留） |
| 1890 | `L1355-L1355` | 待核实 / draft | 蟛鬼疑井鬼；不据别本改 | 通过（draft 保留） |
| 1893 | `L1361-L1361` | 待核实 / draft | 戍/硅娄疑字；不改正文 | 通过（draft 保留） |
| 1922 | `L1422-L1422` | 待核实 / draft | 戊寅立至/来迟冲突；阳阴伏吟分读 | 通过（draft 保留） |
| 1940 | `L1458-L1458` | 待核实 / draft | 乙前疑贵前；不据别本改 | 通过（draft 保留） |
| 1957 | `L1492-L1492` | 待核实 / draft | 或干贵或句残；不补字 | 通过（draft 保留） |
| 1992 | `L1562-L1562` | 待核实 / draft | 庚辛句残；巳加辰孝服 vs 巳雀灶事 | 通过（draft 保留） |
| 2077 | `L1732-L1732` | 待核实 / draft | 若归踪句涩；三路可读不补 | 通过（draft 保留） |
| 2081 | `L1740-L1740` | 待核实 / draft | 爱克疑受克；案例不升 verified | 通过（draft 保留） |

抽核未见把 draft 升 SR、未见把 verified 置 true、未见空模板白话冒充 SR、未见邻段 vernacular 错位。失败 paragraphId：无。

## 6. Caveat（不构成本包失败）

1. 10 条 draft 的疑字、缺字、句残、行人立至冲突等仍待核；本审查只确认处置正确，不重写、不升格。
2. 部分 SR 条白话内标疑字或「狞原文」但仍标 SR；条件绑定与源文一致，不据此失败，也不升 verified。
3. 最短白话（释句、十二将宿度短行）信息量低，但与源行一一对应，不是「白话从略」模板。
4. source-reviewed ≠ 人工 verified；电子全文不是影印校勘。
5. 本包不覆盖索引 0–1799（CP1–CP6）与 2100–2642（后续包）。
6. [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) 若后续改 JSON，本审查钉死的 SHA `30b9b2b9…` 需另核；本包不以 397 未完阻断。

## 7. 交包边界

| 项 | 值 |
|---|---|
| 权威 tip | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（未变） |
| 本岗写出 | 仅 `docs/book-reviews/liuren-miben-cp7-review.md` |
| 结论 | **通过** |
| remaining | 索引 **2100–2642**（543 条） |
| 下一未纳入 | `liuren-miben:L1781-L1781` |
