# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP6（1500–1799）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-449` / 分支 `codex/multica-ming-449`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1–CP5 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）、CP3（600–899，MING-434）、CP4（900–1199，MING-438）、CP5（1200–1499，MING-444）不能代替本 NLC layouts CP6 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 1500–1799。

结论：**通过。** 结构校验 ok、errors=[]；本包 147 SR + 153 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–1499 与 1800–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-449`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1–CP5 审查稿无 diff |

无越权文件。注解未改。不抢 447/448 文件。

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

本包索引 1500–1799（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 147/300 |
| `review=draft` | 153/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空 vernacular / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（1500–1799 全包）：评注或元数据 153、案例 124、理论 19、操作步骤 4。  
kind（仅 SR）：案例 124、理论 19、操作步骤 4。

SR notes：147/147 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 1499（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P205:L034-L035`（draft） |
| 注解索引 1500（CP6 起） | `qimen-dunjia-tongzhi:nlc-layouts:P205:L037-L040`（SR） |
| 注解索引 1799（CP6 止） | `qimen-dunjia-tongzhi:nlc-layouts:P230:L025-L028`（SR） |
| 注解索引 1800（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P230:L030-L031`（draft） |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **1800–2470（671，其中 SR 331）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1–CP5 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1–CP5；如 P206@8120、P210@8165、P214@8878、P215@8324、P226@2179、P227@9567），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仅 379 段，对本包前 50 条 SR 抽核 **agree 0 / disagree 0 / nomatch 50**；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 24 段 SR，含全部 4 条操作步骤、阴一/阴二圆图理论抽样，以及阳九末段至阴二跨页案例（含休诈/真诈/重诈、鬼遁/云遁、五不遇与日格分层、内外圈不合保留）。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 1500 | `P205:L037-L040` | 案例 | 甲午丁乾墓加六合「休詐」并写；不据诈名解除墓限；丙日才日勃 | 通过 |
| 1504 | `P205:L054-L056` | 案例 | 丙申题下空白；不把相邻乙未长列归本条 | 通过 |
| 1514 | `P206:L030-L033` | 案例 | 「天丙辰乙」「惊坎巽」原连字待核；不擅改天丙地乙 | 通过 |
| 1530 | `P207:L046-L049` | 案例 | 乙九地「眞詐」与庚己刑格、门反吟地网分层 | 通过 |
| 1551 | `P209:L006-L008` | 案例 | 甲寅禽死五五与总表四四异文并存，不互订 | 通过 |
| 1564 | `P209:L056-L059` | 案例 | 丁太阴重诈与刑格门迫天网分层；癸日才五不遇 | 通过 |
| 1574 | `P210:L037-L037` | 理论 | 「卷六終」卷界；无新排盘条件 | 通过 |
| 1576 | `P213:L006-L007` | 操作步骤 | 阴一局+十干行头；白话禁从字段补公历 | 通过 |
| 1590 | `P214:L005-L006` | 理论 | 阴一圆图题与中心阴字；无时柱不补盘 | 通过 |
| 1592 | `P214:L011-L019` | 理论 | 離九英甲戌己/景/心甲辰壬/六合分层 | 通过 |
| 1608 | `P215:L005-L010` | 操作步骤 | 「中元一局」+大暑中元/处暑上元等；元别分读；入阴遁不继承阳遁 | 通过 |
| 1620 | `P216:L013-L016` | 案例 | 丁奇入墓得使明确；星反吟≠门反吟；丙单列 | 通过 |
| 1640 | `P217:L048-L050` | 案例 | 己卯英景九四片段；正文跨页不混 | 通过 |
| 1660 | `P219:L018-L021` | 案例 | 生坤丁九地鬼遁条件明确；开巽/惊巽同宫原印不改 | 通过 |
| 1680 | `P221:L005-L008` | 案例 | 辛日五不遇与日格分开；丙墓门制照录 | 通过 |
| 1700 | `P222:L034-L037` | 案例 | 飞干格未指日干；照录不补；门反吟门迫地网分层 | 通过 |
| 1720 | `P224:L013-L017` | 案例 | 乙奇开门下临坤名云遁；星伏吟与门迫保留 | 通过 |
| 1738 | `P226:L006-L007` | 操作步骤 | 阴二局+十干行头；不补公历 | 通过 |
| 1752 | `P227:L005-L006` | 理论 | 阴二圆图题；notes 记内外圈不合按原字保存 | 通过 |
| 1754 | `P227:L011-L019` | 理论 | 離九英甲申庚/景/心甲寅癸/六合；不合处不倒填 | 通过 |
| 1770 | `P228:L005-L009` | 操作步骤 | 「中元二局」+小暑中元/立秋上元等；局题不覆盖全部元别 | 通过 |
| 1780 | `P228:L049-L052` | 案例 | 星伏吟与门制战格分层；不补门伏吟 | 通过 |
| 1790 | `P229:L038-L041` | 案例 | 原数六一照录；丙得使与鸟跌穴、门伏吟分存；甲日才日勃 | 通过 |
| 1799 | `P230:L025-L028` | 案例 | 戌刑未与门位照录；乙单列不补得使；本包止末 SR | 通过 |

锚源行（抽核，页内映射）：P205–210 阳九末段至卷六终（含休诈/真诈/重诈、甲寅宫数异文）；P213–214 阴一总表/圆图；P215–225 阴一三元旁栏与逐时（含鬼遁、云遁、五不遇与日格）；P226–227 阴二总表/圆图（内外圈不合照录）；P228–230 阴二三元旁栏与逐时至丁丑。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 147 条 source-reviewed 写成已人工 verified。draft 153 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1–CP5 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | inventory 仅 379 段；CP6 前 50 SR：agree 0 / disagree 0 / nomatch 50 | 读注解以页内 L 为准。不改 inventory |
| 索引 1500 | 「休詐」与墓限并写 | 不据诈名解除墓限。不回改 |
| 索引 1514 | 「天丙辰乙」原连字 | 含义待核，不擅改。不回改 |
| 索引 1551 | 甲寅逐时五五 vs 总表四四 | 异文并存，不互订。不回改 |
| 索引 1608 / 1770 | 局题中元与旁栏上/下元并列 | 条件分读。不回改 |
| 索引 1660 | 鬼遁与开巽/惊巽同宫 | 条件明确处保留门迫。不回改 |
| 索引 1720 | 云遁名与星伏吟门迫 | 不由遁名免限制。不回改 |
| 索引 1752–1768 | 阴二圆图内外圈不合 | 按可见原字保存，不倒填。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1–CP5）。
2. **局题与三元并列（1608、1770）**：「中元一/二局」与上元/下元节气条件不得合并成单一元别。
3. **原字疑点保留**（1500 休詐、1514 天丙辰乙、1530 眞詐、1551 甲寅宫数异文）：未校前不得常识改写。
4. **遁名与限制并存**（鬼遁/云遁等）：遁名条件明确处不得用遁名取消门迫、入墓、五不遇等限制。
5. **阴二圆图内外圈不合（1752–1768）**：按原字保存，不得用理论地盘倒填。
6. **主本已审与 CP1–CP5 不能代替本 edition CP6**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 147 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 / 300–599 / 600–899 / 900–1199 / 1200–1499 已由 MING-421 / 430 / 434 / 438 / 444 审查，本岗不重做。
- 索引 1800–2470（起 `P230:L030-L031`，671）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 447/448 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-449`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
