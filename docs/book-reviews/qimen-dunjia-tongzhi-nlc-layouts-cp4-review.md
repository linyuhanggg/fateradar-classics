# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP4（900–1199）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-438` / 分支 `codex/multica-ming-438`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1–CP3 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）、CP3（600–899，MING-434）不能代替本 NLC layouts CP4 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 900–1199。

结论：**通过。** 结构校验 ok、errors=[]；本包 149 SR + 151 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–899 与 1200–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-438`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1–CP3 审查稿无 diff |

无越权文件。注解未改。不抢 424/431 文件。

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

本包索引 900–1199（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 149/300 |
| `review=draft` | 151/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空白话 / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（900–1199 全包）：评注或元数据 151、案例 132、理论 14、操作步骤 3。  
kind（仅 SR）：案例 132、理论 14、操作步骤 3。

SR notes：149/149 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 899（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P158:L053-L061`（SR） |
| 注解索引 900（CP4 起） | `qimen-dunjia-tongzhi:nlc-layouts:P158:L063-L064`（draft） |
| 注解索引 901（本包首条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P158:L066-L074` |
| 注解索引 1199（CP4 止 / 本包末条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P182:L034-L037` |
| 注解索引 1200（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P182:L039-L040` |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **1200–2470（1271，其中 SR 622）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1–CP3 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1–CP3），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仍与页内映射大量不一致（本岗对 CP4 前 50 条 SR 抽核 agree 0 / disagree 1，余 no match 49）；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 20 段 SR，含全部 3 条操作步骤、阳六/阳七圆图理论抽样，以及阳六末段至阳七跨页案例（含总表/逐时冲突、云遁续文、鬼遁限定、丙奇得死疑点）。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 901 | `P158:L066-L074` | 理论 | 阳六坎一圆图扇区分层；无时柱不补盘 | 通过 |
| 907 | `P158:L108-L116` | 理论 | 巽四辅丙月奇/杜/柱甲戌己/太阴分层 | 通过 |
| 909 | `P159:L005-L009` | 操作步骤 | 「中元六局」+大寒下元等四栏；元别分读 | 通过 |
| 911 | `P159:L014-L018` | 案例 | 甲子心开六六；生艮战格/死坤乙墓不并作全吉 | 通过 |
| 933 | `P161:L005-L008` | 案例 | 乙亥地丙与天丙地丁分存；乙得使与龙逃走/门迫并存 | 通过 |
| 957 | `P162:L050-L052` | 案例 | 丙戌任生四一跨页续文；不补未核格断 | 通过 |
| 981 | `P164:L046-L049` | 案例 | 丁酉原「柱艮迫」不改杜艮；丙日才飞干 | 通过 |
| 984 | `P165:L006-L008` | 案例 | 戊戌英景六四 vs 总表五四；星宫冲突并列 | 通过 |
| 1007 | `P166:L034-L037` | 案例 | 「開和迫」含义不明照录不改开震迫 | 通过 |
| 1031 | `P168:L030-L033` | 案例 | 戊午太白入荧无干不补；癸日才日勃 | 通过 |
| 1045 | `P171:L006-L007` | 操作步骤 | 阳七局+十干行头；白话禁从字段补公历 | 通过 |
| 1063 | `P172:L024-L035` | 理论 | 坤二芮甲辰壬/禽丙月奇两组不压一干 | 通过 |
| 1069 | `P172:L066-L074` | 理论 | 坎一蓬甲午辛/休/辅丁星奇/九天分层 | 通过 |
| 1075 | `P172:L108-L116` | 理论 | 巽四辅丁星奇/杜/柱甲子戊/太阴分层 | 通过 |
| 1077 | `P173:L005-L009` | 操作步骤 | 「中元七局」+冬至中元等；不混统一中元 | 通过 |
| 1079 | `P173:L014-L018` | 案例 | 甲子柱惊七七伏吟+景离战格；短条无完整九宫 | 通过 |
| 1103 | `P175:L013-L018` | 案例 | 丙子休乾/休坎两处原位；丁合太阴人遁；庚日五不遇 | 通过 |
| 1127 | `P177:L005-L005` | 案例 | 丙戌续文开乙临辛云遁；首字「伏艮」不改休 | 通过 |
| 1175 | `P180:L042-L046` | 案例 | 丁未生丁艮九地鬼遁；「但非蓬」原句保留 | 通过 |
| 1199 | `P182:L034-L037` | 案例 | 「丙奇得死」不改得使；鸟跌穴/乙得使/门迫分存；本包止 | 通过 |

锚源行（抽核，页内映射）：P158 阳六圆图坎一/巽四；P159–169 阳六三元旁栏与逐时（含戊戌总表冲突、開和迫）；P170–172 卷五终与阳七总表/圆图；P173–182 阳七三元旁栏与逐时至丁巳（含云遁续文、鬼遁、丙奇得死）。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 149 条 source-reviewed 写成已人工 verified。draft 151 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1–CP3 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | 与 `## PDF第N页`+L 映射不一致（CP4 前 50 SR：agree 0 / disagree 1 / nomatch 49） | 读注解以页内 L 为准。不改 inventory |
| 索引 909 / 1077 | 局题中元与旁栏上下元并列 | 条件分读。不回改 |
| 索引 981 | 「柱艮迫」字位 | 不改杜艮。不回改 |
| 索引 984 | 总表戊戌五四 vs 逐时六四 | 冲突并列。不回改 |
| 索引 1007 | 「開和迫」 | 含义不明照录。不回改 |
| 索引 1127 | 首字「伏艮」；云遁条件在续文 | 不改休艮。不回改 |
| 索引 1161 | 「丑日為日勃」以支称日 | 原字保留。不回改 |
| 索引 1175 | 「但非蓬」 | 不改但非墓等免责句。不回改 |
| 索引 1191 | 癸丑续文「庚日為日勃」与戊癸日组不相容 | 疑点照录。不回改 |
| 索引 1199 | 「丙奇得死」 | 不改得使。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1–CP3）。
2. **书内冲突并列**（984 等）：总表与逐时星宫冲突不得择优或静默统一。
3. **局题与三元并列（909、1077）**：「中元六/七局」与上元/下元节气条件不得合并成单一元别。
4. **原字疑点保留**（981 柱艮迫、1007 開和迫、1127 伏艮、1161 丑日日勃、1175 但非蓬、1191 庚日日勃、1199 丙奇得死）：未校前不得常识改写。
5. **主本已审与 CP1–CP3 不能代替本 edition CP4**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 149 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 / 300–599 / 600–899 已由 MING-421 / 430 / 434 审查，本岗不重做。
- 索引 1200–2470（起 `P182:L039-L040`）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 424/431 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-438`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
