# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed remaining（2100–2470）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-461` / 分支 `codex/multica-ming-461`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1–CP7 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）、CP3（600–899，MING-434）、CP4（900–1199，MING-438）、CP5（1200–1499，MING-444）、CP6（1500–1799，MING-449）、CP7（1800–2099，MING-455）不能代替本 NLC layouts remaining 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 2100–2470（371）。本包后 remaining **0**（该 edition 独立审查收口）。

结论：**通过。** 结构校验 ok、errors=[]；本包 182 SR + 189 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥20 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–2099 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-461`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json
git rev-parse HEAD:references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗起点 HEAD 一致） |
| 注解文件 SHA256 | `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`（与 Issue 钉死一致） |
| 注解 blob @ 基线 HEAD | `a7a4c66578d108cf44a1ab70b3fd161ca6ff54e4` |
| `nlc-layouts.md` blob @ 基线 | `0f2c83602d5d3715f31f87f42ae7b3104e2bfc80` |
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1–CP7 审查稿无 diff |

无越权文件。注解未改。不抢 447/452 文件。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2471, "source_reviewed": 1210,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

本包索引 2100–2470（371 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 182/371 |
| `review=draft` | 189/371（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空 vernacular / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（2100–2470 全包）：评注或元数据 189、案例 164、操作步骤 9、理论 9。  
kind（仅 SR）：案例 164、操作步骤 9、理论 9。

SR notes：182/182 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 2099（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P255:L002-L003`（draft） |
| 注解索引 2100（本包起） | `qimen-dunjia-tongzhi:nlc-layouts:P255:L005-L009`（SR） |
| 注解索引 2470（本包止 / 全书末） | `qimen-dunjia-tongzhi:nlc-layouts:P325:L081-L091`（SR） |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **0**，与 Issue 一致（该 edition 独立审查收口）。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1–CP7 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1–CP7；如 P261@2648、P266@2460、P267@3093、P273@2710、P279@2554、P299@2776、P312@2870、P313@3219、P325@2964、P255@10370），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仅 379 段；对本包前 50 条 SR 抽核 **agree-present 1 / disagree 0 / nomatch 49**（全包 182 SR 仅 40 条 ID 命中 inventory）。**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥20 非模板 SR，对照原文）

下列共 22 段 SR，覆盖本包起止、阴四下元至阴九符使简表、阴五行头与阴五圆图扇区、阴六–九行头，以及龙/鬼遁题文差、人遁与门迫、得使入墓、戌刑壬原字、天乙地丁、缺项不补等分层。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 2100 | `P255:L005-L009` | 操作步骤 | 「下元四局」+處暑中元/大雪上元等；元别分读不混 | 通过 |
| 2102 | `P255:L014-L018` | 案例 | 甲子辅杜四四与丙乾墓、死坤战格分层 | 通过 |
| 2128 | `P257:L022-L026` | 案例 | 「眞天遁」生丙戊与鸟跌穴；「經日」「死氣和」原词不改 | 通过 |
| 2154 | `P259:L018-L022` | 案例 | 丙丁得使与火入金乡门制并存；丙日才飞干格 | 通过 |
| 2182 | `P261:L032-L037` | 案例 | 休丁太阴人遁明确；壬日才日勃；门迫不由人遁免除 | 通过 |
| 2208 | `P263:L018-L022` | 案例 | 题「龍遁又作鬼遁」；「但非艮蓬」限制保留；龙/鬼分层 | 通过 |
| 2235 | `P265:L020-L023` | 案例 | 「生離義」重复照录不重计；丁得使与门迫天网分层 | 通过 |
| 2239 | `P266:L006-L007` | 操作步骤 | 阴五局+十干行头；白话禁从字段补公历 | 通过 |
| 2253 | `P267:L005-L008` | 操作步骤 | 阴五圆图外圈艮八丁星奇；无时柱不补盘 | 通过 |
| 2255 | `P267:L013-L014` | 理论 | 阴五圆图题与中心阴字；无时柱 | 通过 |
| 2257 | `P267:L019-L027` | 理论 | 離九英甲寅癸/景/心乙/日奇/六合；圈位分层不倒填 | 通过 |
| 2259 | `P267:L032-L043` | 理论 | 坤二芮甲午辛与禽甲子戊两组不可压成一个地干 | 通过 |
| 2273 | `P268:L005-L009` | 操作步骤 | 「下元五局」+立秋中元/霜降小雪上元；元别分读 | 通过 |
| 2285 | `P269:L005-L008` | 案例 | 乙得使入墓与丁乾墓同存；不得因得使免墓 | 通过 |
| 2311 | `P271:L013-L016` | 案例 | 「戌刑壬」照录不改常见戌刑未；乙日才五不遇 | 通过 |
| 2339 | `P273:L020-L023` | 案例 | 乙得使入墓与丁乾墓同存；丙日才五不遇 | 通过 |
| 2366 | `P275:L013-L016` | 案例 | 甲辰仅伤震战格；不补伏吟句 | 通过 |
| 2392 | `P277:L018-L021` | 案例 | 天乙地丁与天乙伏分层；丁单列不补得使；癸日才日格 | 通过 |
| 2410 | `P279:L006-L007` | 操作步骤 | 阴六局+十干行头；不补公历 | 通过 |
| 2420 | `P279:L067-L077` | 案例 | 阴六第5旬符使简表「芮死」；只核星门原宫四类组件 | 通过 |
| 2458 | `P325:L006-L007` | 操作步骤 | 阴九局+十干行头；不补公历 | 通过 |
| 2470 | `P325:L081-L091` | 案例 | 阴九第6旬「輔杜」；「卯三」缺星宫不补；本包末 SR | 通过 |

锚源行（抽核，页内映射）：P255–265 阴四下元至阴四末段（含天遁/人遁/龙鬼遁）；P266–268 阴五行头与阴五圆图/下元题；P269–277 阴五逐时（含得使入墓、戌刑壬、天乙地丁）；P279/299/312/325 阴六–九行头与符使简表至全书末。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。另独立抽读阴五圓图兌七/乾六/坎一/艮八/震三/巽四扇区（索引 2261–2271）与阴七/阴八行头及阴八外圈（2424/2438/2452），语义与上表同法通过，不另占表行。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 182 条 source-reviewed 写成已人工 verified。draft 189 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1–CP7 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。该 edition 独立审查收口（remaining 0）≠ 人工 verified 全书，≠ 产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | inventory 仅 379 段；本包前 50 SR：agree-present 1 / disagree 0 / nomatch 49 | 读注解以页内 L 为准。不改 inventory |
| 索引 2100 / 2273 | 局题下元与旁栏上/中元并列 | 条件分读。不回改 |
| 索引 2128 | 「經日」「死氣和」原词 | 不改常见日或宫词。不回改 |
| 索引 2182 | 人遁与门迫/刑格并存 | 不由遁名免限制。不回改 |
| 索引 2208 | 「龍遁又作鬼遁」+「但非艮蓬」 | 题文与限制分层。不回改 |
| 索引 2235 | 「生離義」重复 | 照录不重计。不回改 |
| 索引 2259 | 坤二芮/禽两组干 | 不可压成一个地干。不回改 |
| 索引 2285 / 2339 | 乙得使入墓与丁乾墓 | 不得因得使免墓。不回改 |
| 索引 2311 | 「戌刑壬」 | 原字保留，不改戌刑未。不回改 |
| 索引 2470 | 「卯三」缺星宫 | 只抄可见字段，缺项不补。不回改 |
| PDF 页块乱序 | P261@2648、P266@2460、P267@3093、P273@2710、P279@2554 等 | 只信页标题+页内 L。不回改源文 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1–CP7）。
2. **局题与三元并列（2100、2273）**：下元局题与上/中元节气条件不得合并成单一元别。
3. **原字疑点保留**（2208 龙鬼遁题文、2311 戌刑壬、2470 卯三缺位）：未校前不得常识改写或补缺。
4. **遁名与限制并存**（人遁/龙遁/鬼遁/天遁等）：遁名条件明确处不得用遁名取消门迫、入墓、五不遇等限制。
5. **得使入墓（2285、2339）**：得使与入墓同存时不得因得使免墓。
6. **圆图圈位分层（2257–2271）**：外圈干与内圈干不同层，不得倒填成完整时盘。
7. **主本已审与 CP1–CP7 不能代替本 edition remaining**；本包收口也不关闭主本/旧总述中的纸本局式与算法缺口，也不等于人工 verified。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 182 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 / 300–599 / 600–899 / 900–1199 / 1200–1499 / 1500–1799 / 1800–2099 已由 MING-421 / 430 / 434 / 438 / 444 / 449 / 455 审查，本岗不重做。
- 本包后 remaining **0**；该 edition 独立审查收口完成。不宣称全书人工 verified。
- 不重做奇门统宗主本；不抢 447/452 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-461`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
