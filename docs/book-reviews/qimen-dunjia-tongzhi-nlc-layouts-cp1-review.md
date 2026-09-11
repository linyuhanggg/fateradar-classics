# 奇门遁甲统宗：独立审查 NLC layouts source-reviewed CP1（0–299）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-421` / 分支 `codex/multica-ming-421`。本岗写出仅本文件。未改注解 JSON、未改源文、未改主本/演义审查稿、未改 `qimen-dunjia-tongzhi.json`、未改他书 / 引擎 / `chart.*`。本岗未参与该 edition 生产。主本审查不能代替本 NLC layouts 审查。不是全书完成，也不是算法交付，也不是人工 verified。source-reviewed ≠ 人工 verified。本包只审注解索引 0–299。

结论：**通过。** 结构校验 ok、errors=[]；本包 148 SR + 152 draft 边界与 Issue 一致；verified 全 false；draft 未升 SR；≥15 段 SR 对照 `nlc-layouts.md`（并以 `fulltext.md` 核对纸电异文）语义成立。下列 caveat 不构成本包失败，也不回改注解。索引 300–2470 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-421`，2026-09-12）：

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
| 工作树相对基线 | 仅新增本审查文件；注解 JSON / 源文 / 主本审查稿无 diff |

无越权文件。注解未改。主本与演义审查稿未改。

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

本包索引 0–299（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 148/300 |
| `review=draft` | 152/300（全部 `kind=评注或元数据`） |
| `verified` | 全 `false`（全书 2471 亦无 true） |
| SR 空白话 / 空 notes / 空 terms | 0 / 0 / 0 |
| 「白话从略 / 见原文 / TODO / 本段论述从略」类空模板 | 0 |

kind（0–299 全包）：评注或元数据 152、案例 123、理论 16、操作步骤 6、待核实 2、规则候选 1。  
kind（仅 SR）：案例 123、理论 16、操作步骤 6、待核实 2、规则候选 1。

SR notes：148/148 含「来源层：…」；多数同时否定全书校完或升 verified。否定升 verified，不是空白话。draft 保持 draft，本岗不回改、不升 SR。

## 4. 索引边界与对照源

注解 `paragraphId` 起止与 Issue 钉死一致：

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起） | `qimen-dunjia-tongzhi:nlc-layouts:P000:L003-L008`（draft） |
| 注解索引 2（本包首条 SR） | `qimen-dunjia-tongzhi:nlc-layouts:P020:L005-L005` |
| 注解索引 299（CP1 止） | `qimen-dunjia-tongzhi:nlc-layouts:P113:L005-L005`（SR） |
| 注解索引 300（下一包起，不在本包） | `qimen-dunjia-tongzhi:nlc-layouts:P113:L007-L008` |

全书注解 2471（1210 SR + 1261 draft）。本包后 remaining **300–2470（2171，其中 SR 1062）**，与 Issue 一致。

对照源：

- 主对照：`sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`（`## PDF第N页` + 页内 `Lxxx`；`P000` 用文件绝对行）。
- 辅对照：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（纸电异文，如直符加时支 vs 主电子 L529）。

**读 ID 约定（本审查实测）**：`P0xx:Laaa-Lbbb` 对 `P≥1` 取 `abs = page_heading_line + L`（`L001` = `## PDF第N页` 下一行）。此映射与 SR 白话一致。  
`references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` 中大量 `start_line/end_line` 与上述页内映射不一致（本岗抽核 agree 31 / disagree 348）；**不构成本包注解失败**，但后续包不得只信 inventory 绝对行而不核 `## PDF第N页`。本岗不改 inventory。

## 5. 抽样语义（≥15 非模板 SR，对照原文）

下列共 21 段 SR，含全部 2 条待核实、全部 1 条规则候选、全部 6 条操作步骤中的 5 条，以及理论/案例跨页抽样。原文按上节页内映射；判定只评本段 SR，不升 verified。

| 索引 | paragraphId | kind | 对照要点 | 判定 |
|---|---|---|---|---|
| 2 | `P020:L005-L005` | 规则候选 | 「更嫌六乙來臨二。丙丁臨六亦如之。」；白话标丁墓坤/乾一支，并与丁到艮异式并存 | 通过 |
| 4 | `P045:L005-L006` | 操作步骤 | 纸本「直符加時干法」+ 时干落宫加天盘直符；白话保留「直符」用词 | 通过 |
| 6 | `P046:L005-L005` | 操作步骤 | 丁卯地盘丁七→天蓬加七，阴遁同例；白话禁无据把移星改跟值使 | 通过 |
| 8 | `P046:L010-L011` | 操作步骤 | 标题「直符加時支」、定义用天盘直使；对照 fulltext L529 标题/首句误写，白话已分层 | 通过 |
| 10 | `P091:L006-L007` | 操作步骤 | 阳一局 + 甲…癸十干行头；白话为读表步骤非另造时刻 | 通过 |
| 12 | `P091:L011-L021` | 案例 | 蓬休旬表十行支与原宫数；白话禁当十份完整九宫 | 通过 |
| 22 | `P091:L081-L091` | 案例 | 心開旬表；同读法 | 通过 |
| 24 | `P092:L005-L006` | 理论 | 阳一局圆图题/中心「陽」；白话无时柱不造甲子 | 通过 |
| 30 | `P092:L040-L048` | 理论 | 兑七柱丁星奇/惊/任丙月奇/朱雀；白话不统一替换神名 | 通过 |
| 42 | `P093:L005-L010` | 案例 | 阳局上元一局甲己日乙丑蓬休九二；白话限主星主门原宫 | 通过 |
| 80 | `P096:L010-L013` | 案例 | 庚辰门反吟+多门迫+庚癸大格；白话禁把己卯续注并入 | 通过 |
| 104 | `P098:L005-L009` | 案例 | 真地遁辛卯：乙开己称地遁仍列入墓/雀投江等；「真」≠无限制 | 通过 |
| 131 | `P099:L060-L063` | 案例 | 辛丑开艮天丙亦名天遁；景艮迫用词疑点保留 | 通过 |
| 179 | `P103:L034-L037` | 案例 | 癸亥心开六六伏吟+天网/战格；与甲寅同宫不同附加，分条保留 | 通过 |
| 197 | `P105:L011-L019` | 待核实 | 离九内圈「甲辰」旁印「寅」；与乾六「甲辰壬」差别保留，不补干 | 通过 |
| 201 | `P105:L040-L048` | 待核实 | 兑七内圈旁「辛奇」vs 艮八「星奇」；不另造三奇分类 | 通过 |
| 213 | `P106:L005-L009` | 操作步骤 | 「下元二局」旁列小寒上元等；白话禁合并成一律下元 | 通过 |
| 251 | `P109:L010-L013` | 案例 | 辛巳大格/白虎猖狂/蛇妖矫分位；乙日五不遇与飞干格分支 | 通过 |
| 291 | `P112:L021-L025` | 案例 | 丁壬日庚子：开门在乾丁得使入墓；原印「生辰」不改艮 | 通过 |
| 295 | `P112:L038-L041` | 案例 | 壬寅景震乙得使、死巽丁加庚；单写「丙」不补遁格 | 通过 |
| 299 | `P113:L005-L005` | 案例 | 癸卯续文门伏+丙得使鸟跌穴+太白入荧；五不遇限丁日 | 通过 |

锚源行（抽核，页内映射）：P020 L3503 三奇入墓句；P045–046 L3077–3092 直符加时干/丁卯例/直符加时支；P091 阳一总表；P092 圆图；P093 乙丑条；P096–099/103 阳一逐时；P105 阳二圆图待核实二则；P106 三元用局；P109–113 阳二逐时至 CP1 止。fulltext L127 同句简体、L527–529 加时干/支异文。

## 6. source-reviewed ≠ 人工 verified

NLC layouts 层为文瑞书局影印局式恢复；升 `source-reviewed` 只表示对照已恢复电子段落实了层次/条件/冲突去向，不是全 PDF 逐页校完，也不是预测有效证据，也不等于奇门算法或主本卷四至九局式产品交付。不得把本包 148 条 source-reviewed 写成已人工 verified。draft 152 条（现代定位/范围说明）保持 draft。本包不是全书交付。旧总述 `qimen-dunjia-tongzhi.md` 与主本审查稿仍保留各自缺口账本，本审查不覆盖、不改写。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| supplemental inventory 绝对行 | 与 `## PDF第N页`+L 映射大量不一致（agree 31 / disagree 348） | 读注解以页内 L 为准。不改 inventory |
| 索引 8 / fulltext L529 | 纸本「直符加時支」+直使；主电子标题/首句误作加时干/值符 | 白话已分层。不回改 |
| 索引 197 | 离九「甲辰」旁「寅」非壬 | 待核实成立。不回改 |
| 索引 201 | 「辛奇」vs「星奇」 | 待核实成立。不回改 |
| 索引 131 | 「景艮迫」用词与常见门克宫不合 | 疑点保留。不回改 |
| 索引 291 | 原印「生辰」 | 白话已点明不改艮。不回改 |
| 包级 notes 套语 | SR notes 含来源层与否定全书校完 | 否定升 verified。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **读 ID 必须用页内 L，不能只信 supplemental inventory 绝对行**（见 §4）。
2. **纸电异文（索引 8）**：移门小节以 NLC 纸本直使为准；主电子 L529 不得静默覆盖。
3. **阳二圆图待核实（197、201）**：寅字 / 辛奇字位未校前不得补干或另造三奇分类。
4. **局题与三元并列（213）**：「下元二局」与上元/中元节气条件不得合并成单一元别。
5. **主本已审 CP1–3 不能代替本 edition**；本包也不关闭主本/旧总述中的纸本局式与算法缺口。

## 未决（本岗不施工）

- 上述待核实与异文保持 unknown，不升 verified。
- 148 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同奇门产品交付。
- 索引 300–2470（起 `P113:L007-L008`）留给后续包；本岗不续写、不重做 0–299。
- 不重做奇门统宗主本；不抢六壬/秘本/皇极/飞星紫微/星學大成主本审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-421`。注解 JSON SHA256 审查前后均为 `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca`。
