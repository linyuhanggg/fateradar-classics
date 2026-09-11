# 太微赋：独立审查主本 source-reviewed 全量（0–2 / 3）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-474` / 分支 `codex/multica-ming-474`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/taiwei-fu.md`、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-464–472 文件。不要与紫微斗数全书 / 飞星混淆。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–2（3 条，全量）。

结论：**通过。** `validate-annotations` `ok=true entries=3 source_reviewed=3 errors=[]`；`verified` 键全缺（无一为 true）；0 draft；起 `taiwei-fu:L0005-L0011` 止 `taiwei-fu:L0015-L0052`；注解与段落库存 3/3 顺序全等。全书 3 段均对照电子原文成立。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-474`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/ziwei/taiwei-fu.json
shasum -a 256 sources/fulltext/ziwei/taiwei-fu/fulltext.md
git rev-parse HEAD:references/annotations/ziwei/taiwei-fu.json
git rev-parse origin/codex/multica-ming-329:references/annotations/ziwei/taiwei-fu.json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `613f2a05cc6bd6de245ba4108f56f04ace59946e050e888a3e90c02096aac703`（与 Issue 钉死一致） |
| 注解 blob | `54230d91b7f33e8e5b43fe81969de7621293ffeb`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/ziwei/taiwei-fu/fulltext.md`（52 行） |
| 源 SHA256 | `2f77ec8c47122cf18308e9c3fc06274df65695861526e4d1896e4fc59ce262c9`（与 D2 catalog 钉死一致） |
| Issue 对照路径 | 先确认后采用 inventory 所记 `sources/fulltext/ziwei/taiwei-fu/fulltext.md`；仓内无 `sources/normalized/ziwei/taiwei-fu*` |
| 库存段落 | `references/inventory/paragraphs/ziwei/taiwei-fu.json` 3 条，ID 顺序与注解全等 |
| 非空源行覆盖 | 正文入段 50 行；未覆盖非空仅 L1 书题 `# 太微賦`、L3 二级标题 `### 太微賦`（结构标题，非段落） |
| catalog / inventory | 维基文库《紫微斗數全書》页；`LIBRARY_INVENTORY`「尚未确认影印」；母书赋文资料包 |

无越权文件。本岗相对 329 只新增本审查稿。未碰 464–472 工作树或分支。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/ziwei/taiwei-fu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 3, "source_reviewed": 3,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。`errors=[]`。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–2，3 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 3/3 |
| `review=draft` | 0 |
| `verified` 键 | **全缺**（3/3 无该字段；无一 `verified=true`） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 缺失 | 0 |
| 空 `terms` | 仅索引 1「例曰」（2 字标题行，结构合法） |
| `subsections` | 0 |
| `sourceAttribution` | 0 |

kind 分布：理论 1、序跋目录 1、规则候选 1。无「待核实」条。

Issue 钉死「verified 全 false」：本文件用缺省未升 verified（键缺失）表达，与「不得升人工 verified」一致；校验器仅在 `verified is True` 时报错，本包未触该条件。

Issue 钉死起 `taiwei-fu:L0005-L0011`、止 `taiwei-fu:L0015-L0052`：与文件索引 0、2 一致；中间索引 1 为 `taiwei-fu:L0013-L0013`。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/ziwei/taiwei-fu.json` 3 段；注解 3 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。

| 位置 | 实测 ID | kind | 说明 |
|---|---|---|---|
| 索引 0（起） | `taiwei-fu:L0005-L0011` | 理论 | 总论：分野不可一概；十二垣 / 三十六位；身命 + 同躔生克；紫微 / 土星 / 金星 / 空亡例 |
| 索引 1 | `taiwei-fu:L0013-L0013` | 序跋目录 | 「例曰」引出下列口诀，不是完整命例 |
| 索引 2（止） | `taiwei-fu:L0015-L0052` | 规则候选 | 冲破空亡庙旺制化 → 组合名 → 宫位会照 → 流限太岁收束 |

本包后该书 SR 审查 remaining **0**。这只表示 3 主段都已有 source-reviewed 注解并经本岗逐段抽核，不是 52 行逐句影印校勘，也不是 verified。既有 `docs/book-reviews/taiwei-fu.md`（生产侧账本）不覆盖、不回改。

## 5. 全书语义对照（3/3，对照原文，不凭进度摘要）

原文取 `sources/fulltext/ziwei/taiwei-fu/fulltext.md` 的 `start_line–end_line`。本书仅 3 段，本岗**全量**对照，不抽样代替。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0011` | 理论 / SR | 源「不可一概論議」→ 白话禁止把寿命/能力/财富一概而论；「一十二垣」「三十六位」「入廟/失度」「身命為福德之本」「同躔」「生剋」「得垣失度」均落到白话；紫微舍躔、土星居垣可移动、金星司财库怕空亡、帝星动 / 贪守空与「各司其职」一致。notes 标明母书赋文包、三十六位/土金不直映现代七政评分——正确限制，未冒充独立全书 | 通过 |
| 1 | `L0013-L0013` | 序跋目录 / SR | 源仅「例曰」。白话明确：引出下列组合口诀，**不是**具体出生资料完整命例；notes「不能因“例”字就把本行统计为可复算案例」成立 | 通过 |
| 2 | `L0015-L0052` | 规则候选 / SR | L15–19 冲破/空亡/庙旺/制化/反背/交驰/吉处藏凶/败地扶持 → 白话先提条件会改变解释；L22–31 辅弼夹帝、魁钺同行、禄文拱命、日月夹财、马头带剑、刑囚夹印、善荫朝纲等名称均出现；L32–33「太陽居午」「太陰居子」与白话「太阳在午、太阴在子」一致；L42「祿存守於田財」→「禄存位于田宅或财帛」；L45–52 身命疾厄、官禄、迁移、流杀/太岁/流禄/童子限老人限/遇杀无制 → 白话转入流限并要求原局与制约，不把单条口诀定品行疾病死亡。notes 分层 L15–19 / 20–31 / 32–40 / 41–46 / 47–52，条件候选边界清楚 | 通过 |

锚条件与源行（全量，非转引进度表）：

- 不可一概论议：L5
- 十二垣 / 三十六位 / 身命为本：L6
- 同躔 / 生克 / 得垣失度：L7
- 紫微 / 土星 / 金星财库 / 空亡：L8–L10
- 例曰：L13
- 禄逢冲破、马遇空亡：L15
- 辅弼夹帝、魁钺同行、禄文拱命、日月夹财：L22–L26
- 日丽中天（太阳居午）、水澄桂萼（太阴居子）：L32–L33
- 禄存守田财：L42
- 身命疾厄 / 父母迁移：L45
- 流杀破军 / 羊陀太岁 / 流禄：L49–L50
- 童子限 / 老人限 / 遇杀无制：L51–L52

抽核未发现空模板白话、把「例曰」升为可复算案例、把赋文组合写成无条件结论、或把 `verified` 置 true。未与紫微斗数全书整书条目或飞星材料串档。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1/L3 书题；L5–52 入段）。3 条升 `source-reviewed` 只表示对照电子段落实了总论限制、例曰边界、组合条件与流限分层，不是影印逐字校勘，也不是紫微断语有效证据，也不等于太微赋组合已写入产品引擎或八术页面。0 条 draft 不等于 0 条未决（简称映射、影印字形仍待校）。不得把本包写成已人工 verified。太微赋是母书赋文资料包，不另计独立全书证据权重。紫微材料不冒充已接入八术页面。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺失 | 3/3 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 空 `terms` | 仅「例曰」段 | 2 字标题行，结构合法。不回改 |
| 土星 / 金星用语 | 源 L8 有「土星」「金星」 | notes 已禁直映七政行星/现代评分。不回改 |
| 「例」字 | L13「例曰」 | 未统计为可复算案例。正确 |
| 简称映射 | 禄/马/刑/囚/印/暗曜/善/荫等 | notes 要求结合母书术语核对。不猜测扩映射 |
| 生产侧 `taiwei-fu.md` | 已存在阅读记录 | 本岗不覆盖、不回改 |
| 影印状态 | LIBRARY_INVENTORY「尚未确认影印」 | 保留。不升 verified |

## Caveat（不改注解，留给后续 pack）

1. **无同书独立影印。** source-reviewed 停在电子语义；维基文库母书页整理本不足以升人工 verified。
2. **母书赋文包。** 不得把太微赋另计为独立全书来源支持；与紫微斗数全书 / 飞星条目分册保管。
3. **组合口诀 ≠ 可执行规则。** 同宫 / 会照 / 夹拱 / 守宫 / 流限分层必须分别实现；富贵刑伤寿夭断语仅历史表述。
4. **土星 / 金星 / 三十六位** 不得静默映射为现代七政行星字段或强弱评分。
5. **流层与原局不可混。** 「遇杀无制」须检查制化，不能只查凶星名称。

## 交包

- Issue：MING-474
- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-474`
- 分支：`codex/multica-ming-474`
- 基线：`6effd8e4f951fd17e1b1e0454942946ebc765da9`
- 写出：仅 `docs/book-reviews/taiwei-fu-independent-review.md`
- 结论：通过；SR remaining **0**；`source-reviewed` ≠ `verified`；未改注解
