# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP7（1800–2099）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-455` / 分支 `codex/multica-ming-455`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1–CP6 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）、CP2（300–599，MING-430）、CP3（600–899，MING-434）、CP4（900–1199，MING-438）、CP5（1200–1499，MING-444）、CP6（1500–1799，MING-449）不能代替本 NLC layouts CP7 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 1800–2099。

结论：**通过。** 结构校验 ok、errors=[]；本包 149 SR + 151 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–1799 与 2100–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-455`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1–CP6 审查稿无 diff |

无越权文件。注解未改。不抢 447/452/453 文件。

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

本包索引 1800–2099（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 149/300 |
| `review=draft` | 151/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空 vernacular / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（1800–2099 全包）：评注或元数据 151、案例 127、理论 19、操作步骤 3。  
kind（仅 SR）：案例 127、理论 19、操作步骤 3。

SR notes：149/149 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 1799（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P230:L025-L028`（SR） |
| 注解索引 1800（CP7 起） | `qimen-dunjia-tongzhi:nlc-layouts:P230:L030-L031`（draft） |
| 注解索引 2099（CP7 止） | `qimen-dunjia-tongzhi:nlc-layouts:P255:L002-L003`（draft） |
| 注解索引 2100（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P255:L005-L009`（SR） |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **2100–2470（371，其中 SR 182）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1–CP6 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1–CP6；如 P239@2273、P241@9686、P252@10363、P253@2367、P254@10880、P255@10371），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仅 379 段，对本包前 50 条 SR 抽核 **agree 0 / disagree 0 / nomatch 50**；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 22 段 SR，含全部 3 条操作步骤、阴三/阴四圆图与卷七终理论抽样，以及阴二末段至阴四前的逐时案例（含天遁/龙遁题文差、风遁门字、云遁/鬼遁、星门反吟、五不遇与日格分层）。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 1801 | `P230:L033-L037` | 案例 | 题「天遁」正文「龍遁」；「但非伏吟」≠免墓；原未改奇不補 | 通过 |
| 1809 | `P231:L010-L014` | 案例 | 「生開臨巽…名風遁」与「開艮」两开字并存不强择；丙丁得使与乙日五不遇分层 | 通过 |
| 1821 | `P232:L005-L005` | 案例 | 丙戌续文：天丙地乙、开乙辛云遁、龙逃走与乙/庚日条件分层 | 通过 |
| 1835 | `P233:L014-L017` | 案例 | 「墓」单列与「乙奇入墓」并存；辛日才飞干格；大格未给干不补 | 通过 |
| 1851 | `P234:L031-L034` | 案例 | 辛丑星伏吟≠全盘伏吟；生坎/休艮按纸保存 | 通过 |
| 1871 | `P236:L005-L005` | 案例 | 己酉续文：丁雀投江、丙鸟跌穴并存；丁日才日勃；地网不删 | 通过 |
| 1891 | `P237:L039-L042` | 案例 | 己未丙丁得使与火入金乡同存；癸日五不遇与戊日日格分条件 | 通过 |
| 1901 | `P239:L006-L007` | 操作步骤 | 阴三局+十干行头；白话禁从字段补公历 | 通过 |
| 1915 | `P240:L005-L006` | 理论 | 阴三圆图题与中心阴字；无时柱不补盘 | 通过 |
| 1917 | `P240:L011-L019` | 理论 | 離九英甲午辛/景/心丁/辛奇/六合；notes 记辛奇异文不造第四奇 | 通过 |
| 1933 | `P241:L005-L009` | 操作步骤 | 「中元三局」+夏至中元/寒露下元等；元别分读 | 通过 |
| 1951 | `P242:L030-L033` | 案例 | 壬申丁得使与太白入荧、虎猖狂分层；伤巽无关系不补 | 通过 |
| 1971 | `P244:L010-L014` | 案例 | 休丁九地鬼遁条件明确；乙日五不遇与门制并存；末丁奇单列 | 通过 |
| 1991 | `P245:L036-L040` | 案例 | 休乙巽风遁与丁乾墓、星伏吟门迫并存；丙日才日格 | 通过 |
| 2011 | `P247:L018-L021` | 案例 | 己亥休兑与开兑同宫照录；乙得使龙逃走与门迫蛇妖矫分层 | 通过 |
| 2031 | `P249:L005-L008` | 案例 | 己酉壬日才日勃；门制与地网分层 | 通过 |
| 2051 | `P250:L034-L037` | 案例 | 戊午门反吟与星反吟两层明确；天网另存 | 通过 |
| 2066 | `P252:L005-L005` | 理论 | 「卷七終」卷界；鸟图装饰不提星门宫 | 通过 |
| 2068 | `P253:L006-L007` | 操作步骤 | 阴四局+十干行头；不补公历 | 通过 |
| 2082 | `P254:L005-L006` | 理论 | 阴四圆图题；无时柱 | 通过 |
| 2084 | `P254:L011-L019` | 理论 | 離九英甲辰壬/景/心丙/月奇/六合；圈位分层不倒填 | 通过 |
| 2098 | `P254:L108-L116` | 理论 | 巽四辅甲子戊/杜/柱丁/星奇/太阴；本包末 SR | 通过 |

锚源行（抽核，页内映射）：P230–238 阴二末段逐时（含天遁/龙遁题文差、风遁门字、云遁）；P239–240 阴三总表/圆图（含離九辛奇异文）；P241–251 阴三三元旁栏与逐时（含鬼遁、风遁、星门反吟、五不遇与日格）；P252 卷七终；P253–254 阴四总表/圆图至巽四扇区。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 149 条 source-reviewed 写成已人工 verified。draft 151 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1–CP6 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | inventory 仅 379 段；CP7 前 50 SR：agree 0 / disagree 0 / nomatch 50 | 读注解以页内 L 为准。不改 inventory |
| 索引 1801 | 题「天遁」正文「龍遁」 | 题文差保留，不互订。不回改 |
| 索引 1809 | 风遁句内两「開」字 | 不强择一门。不回改 |
| 索引 1917 | 離九内圈「辛奇」与外圈干层不同 | 异文照录，不造第四奇。不回改 |
| 索引 1933 | 局题中元与旁栏上/下元并列 | 条件分读。不回改 |
| 索引 1971 / 1991 | 鬼遁/风遁名与门迫、入墓、五不遇并存 | 不由遁名免限制。不回改 |
| 索引 2011 | 休兑与开兑同宫 | 按纸保存。不回改 |
| 索引 2051 | 星反吟与门反吟分层 | 两层都保留。不回改 |
| PDF 页块乱序 | P239@2273、P253@2367、P255@10371、P254@10880 | 只信页标题+页内 L。不回改源文 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1–CP6）。
2. **局题与三元并列（1933）**：「中元三局」与上元/下元节气条件不得合并成单一元别。
3. **原字疑点保留**（1801 天遁/龙遁题文差、1809 风遁两开、1917 離九辛奇）：未校前不得常识改写。
4. **遁名与限制并存**（鬼遁/风遁/云遁等）：遁名条件明确处不得用遁名取消门迫、入墓、五不遇等限制。
5. **圆图圈位分层（1917、2084、2098）**：外圈干与内圈干不同层，不得倒填成完整时盘。
6. **主本已审与 CP1–CP6 不能代替本 edition CP7**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述疑点与冲突保持 unknown，不升 verified。
- 149 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 / 300–599 / 600–899 / 900–1199 / 1200–1499 / 1500–1799 已由 MING-421 / 430 / 434 / 438 / 444 / 449 审查，本岗不重做。
- 索引 2100–2470（起 `P255:L005-L009`，371）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 447/452/453 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-455`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
