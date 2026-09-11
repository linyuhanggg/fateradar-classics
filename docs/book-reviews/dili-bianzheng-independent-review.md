# 地理辨正：独立审查主本 source-reviewed 全量（0–1 / 2）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-479` / 分支 `codex/multica-ming-479`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-464 集成线与本轮其他审查稿。不要与识典 SDZJ0504《地理辨正直解》包混淆；本包只审主本 JSON。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–1（2 条，全量）。

结论：**通过。** `validate-annotations` `ok=true entries=2 source_reviewed=2 errors=[]`；`verified` 显式均为 `false`（无一为 true）；0 draft；起 `dili-bianzheng:L0003-L0005` 止 `dili-bianzheng:L0007-L1863`；注解与段落库存 2/2 顺序全等。全书 2 段均对照电子原文成立；长段 143 具名子节与白话标题行号一一对应、连续覆盖 L7–1863（无缺口、无重叠）。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书主本 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-479`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/dili-bianzheng.json
shasum -a 256 sources/fulltext/fengshui/dili-bianzheng/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/dili-bianzheng.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/dili-bianzheng.json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `32cbcf25b5d807dfb1958c6a30fa9a1665518fa1a1cbd1c94b3d1bdc97b0f5d2`（与 Issue 钉死一致） |
| 注解 blob | `683a42fc36ef8af8e653d2d23f9eea8ec1cd9bc2`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/dili-bianzheng/fulltext.md`（1863 行；inventory `fulltext` 字段同路径） |
| 源 SHA256 | `dedb06a0da127423009654a51e4114f79f9ff6b8d0eae50ae8ac51e5ccb5bda4` |
| Issue 对照路径 | 先确认后采用 inventory / 仓内路径 `sources/fulltext/fengshui/dili-bianzheng/fulltext.md`；另有 `sources/normalized/shidianguji/SDZJ0504` 识典包，**本包未审、未混入** |
| 库存段落 | `references/inventory/paragraphs/fengshui/dili-bianzheng.json` 2 条，ID 顺序与注解全等 |
| 非空源行覆盖 | 正文入段后非空行 0 条未覆盖；L1 书题、L2/L6 空行不入段；L3–5 入索引 0；L7–1863 入索引 1 |
| catalog / inventory | CTP Wiki 页抽取（`ctext_anchor` 钉在源文头）；`LIBRARY_INVENTORY` 主本 2 段 / disposition「已存影印／候选底本」；影印 `sources/facsimile/other/dili-bianzheng/` 共 6 册 PDF 存在，**本包未做影像逐字校** |

无越权文件。本岗相对 329 只新增本审查稿。未碰 464 工作树或分支。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/dili-bianzheng.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2, "source_reviewed": 2,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。`errors=[]`。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–1，2 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 2/2 |
| `review=draft` | 0 |
| `verified` | **2/2 显式 `false`**（无一 `verified=true`） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO / 待核实」类空模板 | 0 |
| `notes` | 索引 0 空数组（来源说明段，结构合法）；索引 1 两条边界 notes |
| 空 `terms` | 0 |
| `subsections` | 仅索引 1：143 条；连续 L7–1863；与顶层白话 `【…，La–Lb】` 标题 143/143 对齐 |
| `sourceAttribution` | 0 |

kind 分布：评注或元数据 1、理论 1。无「待核实」条。

Issue 钉死「verified 全 false」：本文件用显式 `false` 表达，与「不得升人工 verified」一致；校验器仅在 `verified is True` 时报错，本包未触该条件。

Issue 钉死起 `dili-bianzheng:L0003-L0005`、止 `dili-bianzheng:L0007-L1863`：与文件索引 0、1 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/dili-bianzheng.json` 2 段；注解 2 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。

| 位置 | 实测 ID | kind | 说明 |
|---|---|---|---|
| 索引 0（起） | `dili-bianzheng:L0003-L0005` | 评注或元数据 | CTP 来源头 / 混排未拆注层说明，不是经文 |
| 索引 1（止） | `dili-bianzheng:L0007-L1863` | 理论 | 青囊上中下 → 序 → 奥语 → 天玉内传 → 宝照 → 平砂玉尺辨伪；143 子节分层；尾句未完 |

本包后该书主本 SR 审查 remaining **0**。这只表示 2 主段都已有 source-reviewed 注解并经本岗对照电子原文成立，不是 1863 行逐句影印校勘，也不是 verified，更不是 SDZJ0504 识典包审查。

## 5. 全书语义对照（2/2，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/dili-bianzheng/fulltext.md` 的 `start_line–end_line`。本书仅 2 主段，本岗**全量**对照；长段另按子节锚点抽核，不抽样代替整书结论。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0005` | 评注或元数据 / SR | 源 L3 `source_base: CTP《地理辨正》Wiki 文本页抽取`、L4 `ctext_anchor`、L5「蒋注与经文混排，未拆注层」。白话称采集说明、混排未拆注层、**不是经文**——与源一致，未把元数据升为经文 | 通过 |
| 1 | `L0007-L1863` | 理论 / SR | 见下分锚；顶层白话总述「原经、蒋注、姜氏说、章氏直解及后附辨伪论分层；尾句未完」与 notes 一致；143 子节起止连续无缺口 | 通过 |

### 5.1 长段分锚抽核（对照源行，非转引进度表）

| 子域 | 行号 | 独立核实 | 与注解一致性 |
|---|---|---|---|
| 题署 / 上卷 | L7–15 | 「地理辨正」「黄石青囊经」、蒋传姜校、「上卷」；经文一六…五十、中五九宫、化始 | 题署不外推作者已考定；经文不给山向排盘参数 |
| 洛书九宫 | L76–81 | 一北…九南；坎一坤二…离九 | 保留数位表，不另猜未列法 |
| 中卷 | L108–113 | 「太极南垣」；阴阳相见/相乘 | 字差待校声明成立；不直接算星体坐标 |
| 五星序列疑缺 | L144–156 | 木东后接「中央/季夏」再金水，缺火土完整句 | 注解「不能补成已核全表」正确，未静默补句 |
| 疑字保留 | L182 / L1133 | 「亢失娄鬼」；「巽已」「若已丙」（巳/已） | 保留原录、不擅改 |
| 下卷列项 | L320–321 | 五兆八卦六甲八门五运六气 | 不把同名八门当奇门运行事实 |
| 青囊序 | L498–499 / L628–636 | 看雌雄；江南…四组后「非」 | 被驳表不得摘作认可规则 |
| 两片三叉 | L611–612 | 俗注左旋右旋/生旺墓被「非」 | 三叉=水交，非长生三合 |
| 山管山水管水 | L849–860 | 山上不下水、水里不上山 | 山水分用，不混一套参数 |
| 奥语四星组 | L933–940 | 坤壬乙巨门等；姜氏挨星=洛书九气 | 同例非固定等号；旧注表被否定者不采纳 |
| 天玉 / 零正 | L1089+ / L1134–1144 | 三卦八神；正向生入零水克入 | 反言批评与条件分层保留；百步不换现代阈值 |
| 宝照 / 九宫 | L1266+ / L1349–1353 | 山中支穴→平洋；一白贪…九紫弼 vs 八宫掌诀「无明验」 | 形局三吉 ≠ 方位永久吉星；被驳八宫不作正法 |
| 人元疑点 | L1367–1370 | 原文「寅申巳亥人元」而蒋注起句「此四季之支」；「先荣后凋」 | 注解保留疑点，不校成预设答案 |
| 章氏直解 | L1523–1528 | 来往气运阴阳，排除干支/左右/上下元固定坎离等 | 与蒋注署名区分；不擅认章=蒋 |
| 平砂玉尺辨伪 | L1644–1863 | 另起蒋氏辨伪；三合双山/左右旋长生均为「谬」；止于「无物不具」 | 被引表不作认可算法；截尾未完不称底本齐全 |
| L1842 | L1840–1842 | 坎离「不可以…言」；震巽「而可以木言也」平行不齐 | 保留疑点，不擅添「不」字 |

抽核未发现空模板白话、把被驳俗注/三合双山表升为认可算法、把口诀未传细法补成完整排盘、把 SDZJ0504 识典段混入主本 ID、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（CTP Wiki 行表；经注混排）。2 条升 `source-reviewed` 只表示对照电子段落实了来源边界、经注/姜说/章氏/辨伪分层、被驳表不得反用、尾句未完限制，不是 6 册影印逐字校勘，也不是蒋派玄空可执行证据，也不等于地理辨正已写入产品风水引擎或八术页面。0 条 draft 不等于 0 条未决（缺火土句、氏/昂/璧/亢失、巳已、L1842、截尾续文、口传细诀仍待校或未知）。不得把本包写成已人工 verified。风水材料不冒充已接入八术页面。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified=false` | 2/2 显式 false | 不升 true。不回改 |
| 索引 0 空 `notes` | 来源元数据段 | 结构合法。不回改 |
| 五星序列缺火土句 | L144–156 | notes/白话已禁补表。不回改 |
| 疑字 / 断行 | L182、L289–290「气不我，去」、L1133 已/巳、L1842 | 保留原录。不静默替换 |
| 被驳表 | 江南四组、公母子孙分龙、双山三合长生等 | 注解明确否定。不得摘作规则 |
| 口传细诀 | 奥语/天玉/宝照多处「口诀」「未显言」 | 不补猜算法。不回改 |
| 识典 SDZJ0504 | `sources/normalized/shidianguji/SDZJ0504` 另包 | **本包范围外**。不混主本 ID |
| 影印 6 册 | `sources/facsimile/other/dili-bianzheng/` | 存在≠本包已影像校。不升 verified |
| L1863 截尾 | 「无物不具」句未完 | notes 已标。不称全本齐全 |

## Caveat（不改注解，留给后续 pack）

1. **尾句未完 / 非影像校。** source-reviewed 停在电子语义；6 册影印存在不足以升人工 verified。
2. **主本 ≠ 识典 SDZJ0504。** 后者为《地理辨正直解》另路径；本审查不覆盖、不互相冲抵。
3. **被驳表 ≠ 认可算法。** 凡注末「非」「谬」的名单不得单独摘入规则引擎。
4. **同名八门 / 返伏吟 / 功曹传送 / 北斗打劫** 不得静默映射为奇门、六壬或天文北斗算法。
5. **口传未书步骤**（起星、城门细法、顺逆双起全表）不得用后世某派表冒称本文已给全。
6. **风水材料不接入八术页面交付计数。**

## 交包

- Issue：MING-479
- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-479`
- 分支：`codex/multica-ming-479`
- 基线：`6effd8e4f951fd17e1b1e0454942946ebc765da9`
- 写出：仅 `docs/book-reviews/dili-bianzheng-independent-review.md`
- 结论：通过；主本 SR remaining **0**；`source-reviewed` ≠ `verified`；未改注解
