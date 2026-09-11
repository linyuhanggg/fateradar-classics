# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP5（1200–1499）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-444` / 分支 `codex/multica-ming-444`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1–CP4 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）、CP3（600–899，MING-434）、CP4（900–1199，MING-438）不能代替本 NLC layouts CP5 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 1200–1499。

结论：**通过。** 结构校验 ok、errors=[]；本包 144 SR + 156 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–1199 与 1500–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-444`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1–CP4 审查稿无 diff |

无越权文件。注解未改。不抢 424/431/439 文件。

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

本包索引 1200–1499（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 144/300 |
| `review=draft` | 156/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空 vernacular / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（1200–1499 全包）：评注或元数据 156、案例 122、理论 18、操作步骤 4。  
kind（仅 SR）：案例 122、理论 18、操作步骤 4。

SR notes：144/144 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 1199（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P182:L034-L037`（SR） |
| 注解索引 1200（CP5 起） | `qimen-dunjia-tongzhi:nlc-layouts:P182:L039-L040`（draft） |
| 注解索引 1201（本包首条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P182:L042-L045` |
| 注解索引 1498（本包末条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P205:L029-L032` |
| 注解索引 1499（CP5 止） | `qimen-dunjia-tongzhi:nlc-layouts:P205:L034-L035`（draft） |
| 注解索引 1500（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P205:L037-L040` |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **1500–2470（971，其中 SR 478）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1–CP4 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1–CP4；如 P184@1404、P185@7949、P198@1498、P204@8068），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仅 379 段，对本包前 50 条 SR 抽核 **agree 0 / disagree 0 / nomatch 50**；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 22 段 SR，含全部 4 条操作步骤、阳八/阳九圆图理论抽样，以及阳七末段至阳九跨页案例（含地遁/虎遁/云遁条件、真天遁题、休吟原词、局题与三元并列）。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 1205 | `P183:L005-L005` | 案例 | 「开穴」「天门四张」原词不改常见词；丁得使与雀投江同录 | 通过 |
| 1207 | `P183:L010-L013` | 案例 | 庚申开乙地己地遁条件明确；丙墓/丁得使/门迫地网分层 | 通过 |
| 1215 | `P184:L006-L007` | 操作步骤 | 阳八局+十干行头；白话禁从字段补公历 | 通过 |
| 1229 | `P185:L005-L006` | 理论 | 阳八圆图题与中心阳字；无时柱不补盘 | 通过 |
| 1231 | `P185:L011-L019` | 理论 | 離九英甲戌己/景/心丙月奇/六合分层 | 通过 |
| 1245 | `P185:L108-L116` | 理论 | 巽四辅甲寅癸/杜/柱乙日奇/太阴分层 | 通过 |
| 1247 | `P186:L005-L009` | 操作步骤 | 「上元八局」+小寒中元等；元别分读不混 | 通过 |
| 1249 | `P186:L014-L018` | 案例 | 甲子任生八八；休坎战格/开乾丙墓；不默认补伏吟 | 通过 |
| 1253 | `P186:L032-L035` | 案例 | 青龙回首称甲子加地丙；「生坎水克火迫」原说照录 | 通过 |
| 1261 | `P187:L013-L017` | 案例 | 庚午生乙辛虎遁与门反吟/门迫并存；甲日五不遇 | 通过 |
| 1295 | `P190:L005-L009` | 案例 | 乙酉开门天乙地己地遁；乙丁得使与惊巽迫并存 | 通过 |
| 1311 | `P191:L030-L033` | 案例 | 癸巳庚癸大格与时格分存；辛日才飞干格 | 通过 |
| 1345 | `P194:L018-L022` | 案例 | 戊申生乙辛虎遁与龙逃走并存；壬日五不遇 | 通过 |
| 1379 | `P198:L006-L007` | 操作步骤 | 阳九局+十干行头；不补公历 | 通过 |
| 1393 | `P199:L005-L006` | 理论 | 阳九圆图题与中心阳字；无时柱 | 通过 |
| 1395 | `P199:L011-L019` | 理论 | 離九英甲子戊/景/心丁星奇/六合分层 | 通过 |
| 1415 | `P200:L015-L019` | 操作步骤 | 「上元九局」+大寒/春分中元等；不改并为一元 | 通过 |
| 1417 | `P200:L024-L028` | 案例 | 甲子英景九九；开乾丁墓与死坤战格；未补伏吟 | 通过 |
| 1436 | `P201:L031-L035` | 案例 | 庚午开乙辛云遁；甲日五不遇与丙墓门迫同存 | 通过 |
| 1478 | `P204:L005-L009` | 案例 | 题「真天遁」正文无完整天遁组合，不凭题名补条件 | 通过 |
| 1494 | `P205:L015-L015` | 案例 | 辛卯续文门迫时格天网照录；辛日才日格 | 通过 |
| 1498 | `P205:L029-L032` | 案例 | 「休吟」不改伏吟；丁墓/天乙伏/刑格/大格分存；丙日才日勃；本包止前末 SR | 通过 |

锚源行（抽核，页内映射）：P182–183 阳七末段地遁/云遁；P184–185 阳八总表/圆图；P186–197 阳八三元旁栏与逐时（含虎遁、地遁、青龙回首原说）；P198–199 阳九总表/圆图；P200–205 阳九三元旁栏与逐时至癸巳（含云遁、真天遁题、休吟）。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 144 条 source-reviewed 写成已人工 verified。draft 156 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1–CP4 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | inventory 仅 379 段；CP5 前 50 SR：agree 0 / disagree 0 / nomatch 50 | 读注解以页内 L 为准。不改 inventory |
| 索引 1205 | 「开穴」「天门四张」 | 不改常见词。不回改 |
| 索引 1247 / 1415 | 局题上元与旁栏中/下元并列 | 条件分读。不回改 |
| 索引 1253 | 「生坎水克火迫」 | 原说照录。不回改 |
| 索引 1259 | 「大小格」与「时」字单列 | 不擅统一为大格/小时格。不回改 |
| 索引 1478 | 题「真天遁」无完整天遁组合 | 不凭题名补条件。不回改 |
| 索引 1498 | 「休吟」 | 不改伏吟。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1–CP4）。
2. **局题与三元并列（1247、1415）**：「上元八/九局」与中元/下元节气条件不得合并成单一元别。
3. **原字疑点保留**（1205 开穴/天门四张、1253 生坎水克火迫、1259 大小格、1478 真天遁题、1498 休吟）：未校前不得常识改写。
4. **遁名与限制并存**（地遁/虎遁/云遁等）：遁名条件明确处不得用遁名取消门迫、入墓、五不遇等限制。
5. **主本已审与 CP1–CP4 不能代替本 edition CP5**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 144 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 / 300–599 / 600–899 / 900–1199 已由 MING-421 / 430 / 434 / 438 审查，本岗不重做。
- 索引 1500–2470（起 `P205:L037-L040`，971）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 424/431/439 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-444`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
