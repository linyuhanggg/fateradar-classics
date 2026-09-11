# 青囊序：独立审查主本 source-reviewed 全量（0 / 1）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-466` / 分支 `codex/multica-ming-466`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/qingnang-xu.md`、未抢 MING-458–464 文件、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0（1 条，全量）。不要与《青囊经》《青囊奥语》混淆：本包 slug=`qingnang-xu`，该书另有独立注解文件（jing 24 条 / aoyu 3 条），本岗未打开改写。

结论：**通过（有限范围）。** 结构校验 ok、`errors=[]`；1/1 `source-reviewed`、0 draft；`verified` 键缺失（无一为 true）；inventory 与注解 `paragraphId` 一一对应；全书仅 1 段，已对照原文语义成立；疑字 notes 可复核且未静默改正文。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-466`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/qingnang-xu.json
git rev-parse HEAD:references/annotations/fengshui/qingnang-xu.json
shasum -a 256 sources/fulltext/fengshui/qingnang-xu/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `86d32d689a9db3275c17ff14a53cc0af636833cd4b5c7c8e74351c372df552cd`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `1f412f7f29391aaba8bffd1c4616b3e148dd4183` |
| 源 `fulltext.md` SHA256 | `c3865ecf1be5c5037d98699c0d4af47695c581f3591024edb4cdaa0fd873763c` |
| 源行数 | 17（L1 书题；L2 空；L3–L17 入段） |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `qingnang-xu.md` 无 diff |

路径说明：Issue 对照写 `sources/fulltext/fengshui/qingnang-xu/fulltext.md`；仓内权威路径与 inventory `fulltext` 一致。本岗按该 fulltext 全文对照，不另造 normalized 副本。catalog 另有历史路径 `references/fulltext/...`，本树未用作抽核底本。

无越权文件。注解未改。源文未改。未写产品仓。未碰 458–464 独占文件。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/qingnang-xu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 1, "source_reviewed": 1,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`source_reviewed=1` 与 Issue 口径一致。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0，1 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 1/1 |
| `review=draft` | 0 |
| `verified` 键 | **缺省**（1/1 无该字段；无一 `verified=true`） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 缺失 | 0（7 条 notes） |
| 空 `terms` | 0（17 个术语） |
| `subsections` | 0 |
| `sourceAttribution` | 0 |
| `kind` | 理论（inventory `automatic_kind` 曾标「序跋目录」；注解取理论，与口诀主体相符，见账本） |

Issue 钉死「verified 全 false」：本文件用缺省未升 verified（键缺失）表达，与「不得升人工 verified」一致；校验器仅在 `verified is True` 时报错，本包未触该条件。

Issue 钉死起止 `qingnang-xu:L0003-L0017`：与文件索引 0、inventory 唯一段一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/qingnang-xu.json` 1 段；注解 1 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；`paragraphId` / 行号 / char_count=1168 与源 L3–L17 去换行字数一致。

非空源行：L1 Markdown 书题 `# 青囊序` 未入段；L3–L17 全部落入唯一 `paragraphId`。L2 空行未入段。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起=止） | `qingnang-xu:L0003-L0017` | 全书唯一长段；段内行号在 notes 中定位论述层 |

本包后该书 SR 审查 remaining **0**。这只表示 1 主段已有 source-reviewed 注解并经本岗全文对照，不是 17 行逐字影印校勘，也不是 verified。既有 `docs/book-reviews/qingnang-xu.md`（生产侧账本）不覆盖、不回改。

## 5. 全文语义对照（全书 1 段 = 必核）

原文取 `sources/fulltext/fengshui/qingnang-xu/fulltext.md` L3–L17。下列按 notes 分层与白话主张逐项核对（非模板摘要转抄）：

| 层 | 源行 | 原文要点 | 注解主张 | 判定 |
|---|---|---|---|---|
| 开篇阴阳/来龙 | L3–L5 | 雌雄、金龙、来龙、三叉、河洛；罗经十二支+干维→二十四山顺逆、四十八局 | 白话：山水阴阳、来龙水路、二十四山顺逆与五行 | 通过 |
| 反拘泥 | L6 | 「陽山陽向水流陽，執定此說甚荒唐」「陰山陰向水流陰，笑殺拘泥都一般」 | notes：该句是被批评的说法，不能只摘执行；白话明确批评阳配阳/阴配阴口诀 | 通过 |
| 山上/水里 | L7 | 「山上龍神不下水，水裏龍神不上山」 | notes：未明确术语前不能套进同一张盘；terms 分列两词 | 通过 |
| 量山步水 | L8–L9 | 净阴净阳、来处起顶、明堂朝水、直射直流家业退 | 白话：量山步水时观察来处、明堂、朝水、高峰；直射直流等方向关系 | 通过 |
| 进退定义 | L10、L12 | L10「生出剋出…退 / 生入剋入…進」；L12「進神宜進…退神宜退亦同旺」 | notes：不能简化成「进神吉、退神凶」；白话：进退须与位置相合 | 通过 |
| 折水度量 | L13 | 「四尺八寸爲一步」；小/中/大神三折上御街 | notes：历史度量，不擅自换算现代米 | 通过 |
| 房份 | L14–L15 | 乾坤艮巽长男；寅申已亥长伶丁；甲庚丙壬中男；乙辛丁癸小男等 | notes：传统房份，不用于推断现实家庭结局；白话列二十四山与房份配对 | 通过 |
| 血脉收束 | L15–L17 | 「水是山家血脈精」；一行颠倒五行、以讹传讹 | 白话：水比作山家血脉；无直接复算罗盘程序；财富人丁官位保留为传统判断 | 通过 |

独立核对源文关键短语均存在：阳山阳向 / 荒唐、山上龙神不下水、生入克入为进、退神宜退、四尺八寸为一步、水是山家血脉精。未发现空模板白话、把疑字静默改正文、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1 书题「青囊序」；L3–17 入段）。catalog `source_anchor_url` 为维基文库整理页。1 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/疑字去向，不是影印逐字校勘，也不是风水断语有效证据，也不等于玄空/净阴净阳/进退神已写入产品引擎。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是青囊序全书产品交付，也不覆盖生产侧 `docs/book-reviews/qingnang-xu.md`。风水材料不冒充已接入八术页面。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺失 | 1/1 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 元空 vs 玄空 | 源文多用「元空」；terms 用「玄空」 | 避讳/通假常见。白话未改正文。不回改 |
| 「衰望」「四金四林」「寅申已亥」「畫夜」「要職」 | 均见于 L5/L11/L14/L15/L16 | notes 已记可能版本/字形问题。保留原文 |
| 「湹澗」「請騐」「財狼𤢎」 | L3 / L16 / L9 | 疑字/罕用字。注解未静默改；可后续校勘 |
| inventory `automatic_kind=序跋目录` vs 注解 `kind=理论` | 书名「序」但正文为理气口诀长段 | 注解取理论合理。不回改 |
| 单段长文 | 1 paragraphId 覆盖 L3–L17 | notes 已说明段内行号定位；未新造 ID。不拆段 |
| 与青囊经/奥语 | 同目录另有 `qingnang-jing.json`（24）/`qingnang-aoyu.json`（3） | 本包仅审 xu。未混淆、未改他书 |
| LIBRARY_INVENTORY「已存影印／候选底本」 | 库存标记 | 本岗未打开影印做逐字校；SR ≠ 影印 verified |
| 既有 `qingnang-xu.md` | 生产侧阅读记录 | 并存。不覆盖 |

## Caveat（不改注解，留给后续 pack）

1. **疑字未校定。** 「衰望」「四金四林」「已/巳」「畫/晝」「湹澗」「請騐」「財狼𤢎」等仍待影印或他本；不得据此升 verified。
2. **单段口诀不是可执行排局程序。** 二十四山顺逆、四十八局、进退神、房份配对进入产品前必须另建可复算规则层，禁止从白话句直接生成住宅建议。
3. **元空/玄空、净阴净阳、山上/水里龙神** 是理气传统分层；接入时禁止拼成一张无出处的万能盘。
4. **既有 `qingnang-xu.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。
5. **勿与青囊经/青囊奥语混审。** 三书 slug 与段落集不同；本包 remaining=0 仅对 `qingnang-xu`。

## 8. 交付

| 项 | 值 |
|---|---|
| Issue | MING-466 |
| 分支 | `codex/multica-ming-466` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/qingnang-xu-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后闭环；无需重做索引 0；无需回改注解。
