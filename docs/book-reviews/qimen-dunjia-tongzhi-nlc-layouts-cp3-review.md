# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP3（600–899）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-434` / 分支 `codex/multica-ming-434`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1/CP2 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）不能代替本 NLC layouts CP3 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 600–899。

结论：**通过。** 结构校验 ok、errors=[]；本包 146 SR + 154 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–599 与 900–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-434`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1/CP2 审查稿无 diff |

无越权文件。注解未改。不抢 424/427/431 文件。

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

本包索引 600–899（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 146/300 |
| `review=draft` | 154/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空白话 / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（600–899 全包）：评注或元数据 154、案例 129、理论 14、操作步骤 3。  
kind（仅 SR）：案例 129、理论 14、操作步骤 3。

SR notes：146/146 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 599（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L010-L010`（draft） |
| 注解索引 600（CP3 起） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L012-L013`（draft） |
| 注解索引 601（本包首条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L015-L018` |
| 注解索引 899（CP3 止 / 本包末条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P158:L053-L061` |
| 注解索引 900（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P158:L063-L064` |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **900–2470（1571，其中 SR 771）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1/CP2 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1/CP2），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仍与页内映射大量不一致（本岗对 CP3 前 50 条 SR 抽核 agree 0 / disagree 3，余 no match 47）；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 19 段 SR，含全部 3 条操作步骤、阳五/阳六圆图理论抽样，以及阳四末段至阳六跨页案例（含总表/逐时冲突与疑点保留）。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 601 | `P136:L015-L018` | 案例 | 庚辰门伏吟+开乾丙奇入墓仍写丙奇得使/火入金乡；庚日日勃分条件 | 通过 |
| 613 | `P137:L005-L005` | 案例 | 乙酉丁亥间无时柱/符使/数题；疑丙戌不写入原题；丙生合戊天遁保留 | 通过 |
| 633 | `P138:L035-L038` | 案例 | 乙未丁/乙得使与雀投江、龙逃走并存；门迫独立 | 通过 |
| 666 | `P141:L013-L016` | 案例 | 庚戌首句「休雀和」不改休震/休兑 | 通过 |
| 688 | `P143:L010-L013` | 案例 | 庚申休门临巽合乙奇未另写风遁名；乙得使入墓+癸日飞干分条 | 通过 |
| 696 | `P144:L006-L007` | 操作步骤 | 阳五局+甲…癸行头；白话禁从字段补公历 | 通过 |
| 702 | `P144:L039-L049` | 案例 | 柱惊旬表；白话标与逐时数字冲突按原数保存 | 通过 |
| 710 | `P145:L005-L006` | 理论 | 阳五局圆图题/中心「陽」；无时柱 | 通过 |
| 716 | `P145:L040-L048` | 理论 | 兑七柱甲申庚/惊/任甲午辛/朱雀分层 | 通过 |
| 722 | `P145:L079-L087` | 理论 | 艮八任甲午辛生/英甲辰壬直符分层 | 通过 |
| 726 | `P145:L108-L116` | 理论 | 巽四辅乙日奇/杜/柱甲申庚/太阴分层 | 通过 |
| 728 | `P146:L005-L009` | 操作步骤 | 「中元五局」+小寒下元等四栏；元别分读 | 通过 |
| 765 | `P149:L006-L008` | 案例 | 丙戌柱惊三九 vs 总表戌三八；门宫冲突并列 | 通过 |
| 800 | `P151:L013-L016` | 案例 | 癸巳庚癸大格后「時」单列不补时格 | 通过 |
| 811 | `P152:L006-L008` | 案例 | 戊戌任生五二 vs 总表戌五三；门宫冲突并列 | 通过 |
| 823 | `P152:L049-L053` | 案例 | 辛丑虎遁三条件；「景墓」原词不改宫 | 通过 |
| 855 | `P155:L005-L005` | 案例 | 甲寅续文一九还宫 vs 前页一一数栏分存 | 通过 |
| 877 | `P157:L006-L007` | 操作步骤 | 阳六局+十干行头；同 696 读法 | 通过 |
| 899 | `P158:L053-L061` | 理论 | 乾六心甲子戊开/冲丁星奇/九地；本包止 | 通过 |

锚源行（抽核，页内映射）：P136 庚辰门伏；P137 无题天遁疑丙戌；P138–143 阳四逐时至庚申；P144–146 阳五总表/圆图/中元五局旁栏；P149–156 阳五逐时总表冲突、虎遁、甲寅续文；P157–158 阳六总表行头与圆图至乾六。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 146 条 source-reviewed 写成已人工 verified。draft 154 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1/CP2 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | 与 `## PDF第N页`+L 映射不一致（CP3 前 50 SR：agree 0 / disagree 3 / nomatch 47） | 读注解以页内 L 为准。不改 inventory |
| 索引 613 | 无时柱疑丙戌 | 推断不写原题。不回改 |
| 索引 666 | 「休雀和」字位 | 不改门宫。不回改 |
| 索引 702 / 765 / 811 / 814 | 总表与逐时门宫数字冲突 | 冲突并列。不回改 |
| 索引 728 | 局题「中元五局」与旁栏多含上/下元 | 条件分读。不回改 |
| 索引 800 | 「時」单列 | 不补时格。不回改 |
| 索引 823 | 「景墓」 | 原词保留。不回改 |
| 索引 849 | 「生兌庚同一戰在固」连读未定 | 不凭常识改句。不回改 |
| 索引 855 / 875 | 数栏 vs 「一九還宮」 | 分存。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1/CP2）。
2. **书内冲突并列**（702、765、811、814 等）：总表与逐时门宫/星宫冲突不得择优或静默统一。
3. **无题疑丙戌（613）**：顺序推断不得写入原题或组件输入。
4. **局题与三元并列（728）**：「中元五局」与上元/下元节气条件不得合并成单一元别。
5. **原字疑点保留**（666 休雀和、800「時」、823 景墓、849 连读未定）：未校前不得常识改写。
6. **主本已审与 CP1/CP2 不能代替本 edition CP3**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 146 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 已由 MING-421 审查，300–599 已由 MING-430 审查，本岗不重做。
- 索引 900–2470（起 `P158:L063-L064`）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 424/427/431 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-434`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
