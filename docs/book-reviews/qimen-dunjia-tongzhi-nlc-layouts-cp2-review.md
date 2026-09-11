# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP2（300–599）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-430` / 分支 `codex/multica-ming-430`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 CP1 审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查与 CP1（0–299，MING-421）不能代替本 NLC layouts CP2 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 300–599。

结论：**通过。** 结构校验 ok、errors=[]；本包 145 SR + 155 draft 边界与 Issue 一致；verified 全 false（本包条目无 `verified` 键，全书亦无 true）；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（页内 L 映射）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 0–299 与 600–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-430`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本与 CP1 审查稿无 diff |

无越权文件。注解未改。不抢 424–427 文件。

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

本包索引 300–599（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 145/300 |
| `review=draft` | 155/300（全部 `kind=评注或元数据`） |
| `verified` | 全 false（本包无 `verified` 键；全书 2471 亦无 true） |
| SR 空白话 / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（300–599 全包）：评注或元数据 155、案例 121、理论 18、操作步骤 4、待核实 1、序跋目录 1。  
kind（仅 SR）：案例 121、理论 18、操作步骤 4、待核实 1、序跋目录 1。

SR notes：145/145 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 299（上一包止，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P113:L005-L005` |
| 注解索引 300（CP2 起） | `qimen-dunjia-tongzhi:nlc-layouts:P113:L007-L008`（draft） |
| 注解索引 301（本包首条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P113:L010-L014` |
| 注解索引 598（本包末条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L006-L008` |
| 注解索引 599（CP2 止） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L010-L010`（draft） |
| 注解索引 600（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P136:L012-L013` |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **600–2470（1871，其中 SR 917）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文时分层核对；本包抽核以 NLC 页内映射为准）。

**读 ID 约定（与 CP1 一致）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。PDF 页块在文件中非严格递增（同 CP1），不得按绝对行号猜测页码。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 仍与页内映射大量不一致（本岗对 CP2 前 50 条 SR 抽核 agree 0 / disagree 9，余无匹配 inventory id）；**不构成本包注解失败**，但不得只信 inventory 绝对行。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 23 段 SR，含全部 1 条待核实、全部 4 条操作步骤、全部 1 条序跋目录，以及理论/案例跨页抽样。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 301 | `P113:L010-L014` | 案例 | 甲辰龙遁：心开六六；「星符門俱伏伏吟」+乙休合坎名龙遁+杜巽战格；白话分星/门伏层 | 通过 |
| 325 | `P115:L006-L008` | 案例 | 丁巳柱惊八一；旁注总表同格八二；白话并列冲突不择优 | 通过 |
| 348 | `P117:L006-L007` | 操作步骤 | 阳三局+甲…癸行头；白话禁从字段补公历 | 通过 |
| 352 | `P117:L025-L035` | 案例 | 辅北旬表十行支与两宫数；只核符使/宫组件 | 通过 |
| 362 | `P118:L005-L006` | 理论 | 阳三局圆图题/中心「陽」；无时柱不造例 | 通过 |
| 368 | `P118:L040-L048` | 理论 | 兑七外圈柱甲辰壬 / 门惊 / 内圈任甲寅癸 / 朱雀；干分层 | 通过 |
| 374 | `P118:L079-L087` | 理论 | 艮八任甲寅癸生 / 英丁星奇直符；直符字位不推全时值符 | 通过 |
| 380 | `P119:L005-L009` | 操作步骤 | 「下元三局」旁列大寒上元等；禁合并成一律下元 | 通过 |
| 397 | `P120:L022-L025` | 案例 | 庚午冲伤：丙得使+丁入墓；己日日劫 vs 甲日五不遇/飞干格分条 | 通过 |
| 421 | `P122:L010-L013` | 案例 | 辛巳辅杜星符反吟+大格；乙日五不遇条件可读 | 通过 |
| 443 | `P123:L044-L048` | 待核实 | 原题「丁卯」在庚寅后、丙辛日组；疑序辛卯；保留丁卯不Silent改 | 通过 |
| 447 | `P124:L013-L016` | 案例 | 癸巳门伏吟+星符反吟并存；申刑寅≠时支巳 | 通过 |
| 471 | `P126:L010-L013` | 案例 | 甲辰柱惊七七伏吟+乙奇入墓+战格；不把七宫径作乙墓 | 通过 |
| 496 | `P128:L014-L014` | 案例 | 甲寅续文伏吟/死坤战格/乙墓；戊日五不遇条件保留 | 通过 |
| 519 | `P130:L005-L005` | 序跋目录 | 「奇門遁甲統宗卷四終」；非缺盘页 | 通过 |
| 521 | `P131:L006-L007` | 操作步骤 | 阳四局+十干行头；同 348 读法 | 通过 |
| 525 | `P131:L025-L035` | 案例 | 心开旬表；与逐时数字冲突按原数并列 | 通过 |
| 535 | `P132:L005-L006` | 理论 | 阳四局圆图题/中心阳；无时柱 | 通过 |
| 541 | `P132:L040-L048` | 理论 | 兑七甲午辛/惊/任甲辰壬/朱雀分层 | 通过 |
| 547 | `P132:L079-L087` | 理论 | 艮八任甲辰壬生/英甲寅癸直符分层 | 通过 |
| 557 | `P133:L015-L019` | 操作步骤 | 「下元四局」+冬至下元等四栏；元别分读 | 通过 |
| 571 | `P134:L013-L017` | 案例 | 庚午虎遁：乙奇生门临六辛；与休乙艮辛虎遁条件不合并 | 通过 |
| 598 | `P136:L006-L008` | 案例 | 甲申心开六六 vs 总表辅柱；星辅/心冲突并列 | 通过 |

锚源行（抽核，页内映射）：P113 甲辰龙遁；P115 丁巳八一冲突；P117–119 阳三总表/圆图/下元三局旁栏；P120–128 阳三逐时至甲寅续；P130 卷四终；P131–136 阳四总表/圆图/下元四局旁栏/虎遁/甲申冲突。fulltext 仅作辅对照，不以主电子覆盖 NLC 纸本局式。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 145 条 source-reviewed 写成已人工 verified。draft 155 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md`、主本审查稿与 CP1 审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | 与 `## PDF第N页`+L 映射不一致（CP2 前 50 SR：agree 0 / disagree 9） | 读注解以页内 L 为准。不改 inventory |
| 索引 325 | 丁巳逐时八一 vs 总表八二 | 冲突并列。不回改 |
| 索引 443 | 原题丁卯 vs 六十序/日干组疑辛卯 | 待核实成立；保留丁卯。不回改 |
| 索引 525 / 598 | 总表与逐时星名/宫数冲突 | 并列保存。不回改 |
| 索引 380 / 557 | 局题「下元N局」与旁栏多含上/中元 | 条件分读。不回改 |
| 索引 301 notes | 「俱伏伏吟」重字 | 白话按星/门均伏说明。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4；同 CP1）。
2. **书内冲突并列**（325、525、598）：总表与逐时数字/星名冲突不得择优或静默统一。
3. **丁卯待核实（443）**：原题丁字已确认；按序疑辛卯只作上下文，未改写前不得当无误六十条。
4. **局题与三元并列（380、557）**：「下元N局」与上元/中元节气条件不得合并成单一元别。
5. **主本已审与 CP1 不能代替本 edition CP2**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述待核实与冲突保持 unknown，不升 verified。
- 145 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 0–299 已由 MING-421 审查，本岗不重做。
- 索引 600–2470（起 `P136:L012-L013`）留给后续包；本岗不续写。
- 不重做奇门统宗主本；不抢 424–427 及其他书审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-430`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
