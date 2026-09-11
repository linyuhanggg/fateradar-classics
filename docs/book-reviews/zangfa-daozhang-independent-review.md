# 葬法倒杖 · 主本：独立审查 source-reviewed 全量（0–12 / 13）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-456` / 分支 `codex/multica-ming-456`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/zangfa-daozhang.md`、未抢 MING-447/452/453、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–12（13 条，全量）。

结论：**通过。** 结构校验 `ok=true entries=13 source_reviewed=13 errors=[]`；`verified` 键全缺（无一为 true）；0 draft；起 `zangfa-daozhang:L0001-L0005` 止 `zangfa-daozhang:L0230-L0278`；注解与段落库存 13/13 顺序全等。全书 13 段均对照电子原文抽核成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。风水进入知识检索，不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-456`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/zangfa-daozhang.json
git rev-parse HEAD:references/annotations/fengshui/zangfa-daozhang.json
shasum -a 256 sources/fulltext/fengshui/zangfa-daozhang/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `b01f4029d033f97921a5510a068b51be0cd5ea736d73598541dc56d412375dcd`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `ebe46194ea47a39969be5bb402f93dab3da51e1c` |
| 源 `fulltext.md` SHA256 | `c2026ed5af7b39d14ab878dd045cda378390b35102e336706ca17ac390b917b0` |
| 源行数 | 278 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `zangfa-daozhang.md` 无 diff |

对照路径：Issue 写 `sources/fulltext/fengshui/zangfa-daozhang/fulltext.md`，与 inventory `fulltext` 字段一致。catalog 另记 `references/fulltext/...` 与不同 SHA，属蒸馏包路径；本岗按 inventory / Issue 钉死的 `sources/fulltext` 抽核，不另造副本。

catalog：`source_anchor_url` 维基文库《撼龍經/葬法倒杖》；`source_provenance_status=consolidated_catalog`；`source_risk` 已提示阴宅/穴法不可外推阳宅择日，并点名浮□、□□等缺字风险。

无越权文件。注解未改。源文未改。未写产品仓。未碰 447/452/453 工作树或分支。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/zangfa-daozhang.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 13, "source_reviewed": 13,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`source_reviewed=13` 与 Issue 口径一致。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–12，13 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 13/13 |
| `review=draft` | 0 |
| `verified` 键 | **全缺**（13/13 无该字段；无一 `verified=true`） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 缺失 / 空 | 0 |
| 空 `terms` | 7（均为 Source URL / YAML 元数据段，结构合法） |
| `relatedParagraphIds` | 全无 |
| 额外键 | 无（仅 `paragraphId/kind/vernacular/terms/notes/review`） |

kind 分布：评注或元数据 7、理论 3、操作步骤 3。

Issue 钉死「verified 全 false」：本文件用缺省未升 verified（键缺失）表达，与「不得升人工 verified」一致。

Issue 钉死起 `zangfa-daozhang:L0001-L0005`、止 `zangfa-daozhang:L0230-L0278`：与文件索引 0、12 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/zangfa-daozhang.json` 13 段；注解 13 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。

非空源行 254；入段覆盖 248。未入段非空行 6 处，全部是 Markdown 章题（`# 認太極` / `# 分兩儀` / `# 求四象` / `# 倍八卦` / `# 倒杖十二法` / `# 二十四砂葬法`），不在 paragraphId 集合内——与生产侧「13 稳定段」口径一致，不构成本包失败。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起） | `zangfa-daozhang:L0001-L0005` | YAML 头，非术文 |
| 索引 2 | `zangfa-daozhang:L0012-L0012` | 认太极正文 |
| 索引 4 | `zangfa-daozhang:L0019-L0019` | 分两仪正文（简体转录） |
| 索引 6 | `zangfa-daozhang:L0026-L0026` | 求四象正文 |
| 索引 8 | `zangfa-daozhang:L0033-L0195` | 倍八卦：十六法总纲+分释 |
| 索引 10 | `zangfa-daozhang:L0202-L0223` | 倒杖十二法（实列十一杖） |
| 索引 12（止） | `zangfa-daozhang:L0230-L0278` | 二十四砂葬法 |

本包后该书 SR 审查 remaining **0**。这只表示 13 主段都已有 source-reviewed 注解并经本岗全核，不是 278 行逐句影印校勘，也不是 verified。既有 `docs/book-reviews/zangfa-daozhang.md`（生产侧账本）不覆盖、不回改。

## 5. 全量语义核（13/13，对照原文）

原文取 `sources/fulltext/fengshui/zangfa-daozhang/fulltext.md` 的行范围。下列覆盖全部索引；长段核对方法名/杖名集合与关键 caveat，不凭进度摘要。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0001-L0005` | 评注 / SR | YAML 头：题名/slug/来源说明；白话明确「不是术文」 | 通过 |
| 1 | `L0010-L0010` | 评注 / SR | Wikisource「認太極」URL；无术文，只溯源 | 通过 |
| 2 | `L0012-L0012` | 理论 / SR | 金鱼水界→圆晕太极→小明堂侧卧→天轮/三轮；条件与否定「无此者非」保留；非实测结论 | 通过 |
| 3 | `L0017-L0017` | 评注 / SR | Wikisource「分兩儀」URL | 通过 |
| 4 | `L0019-L0019` | 理论 / SR | 阴穴/阳穴两仪；阴龙宜阳穴、阳龙宜阴穴皆有饶减；二气相感中取不用饶减。notes 记简体转录与饶减无尺寸 | 通过 |
| 5 | `L0024-L0024` | 评注 / SR | Wikisource「求四象」URL | 通过 |
| 6 | `L0026-L0026` | 理论 / SR | 脉息窟突=少阴少阳太阴太阳；取中/剖开/培高/凿平四法定基顺序固定 | 通过 |
| 7 | `L0031-L0031` | 评注 / SR | Wikisource「倍八卦」URL | 通过 |
| 8 | `L0033-L0195` | 操作 / SR | 源内十六法专释齐全（盖粘倚撞斩截吊坠正求架折挨并斜插）；开篇息法只列斩截坠却称「已上四法」，`高$山` 乱码、垢复/（後厥）/下薄莫粘张力、窝不葬心反驳、架法「破土尺余+玄武高龙虎压」前提，白话与 notes 均定位不改正文、不折算工程量 | 通过 |
| 9 | `L0200-L0200` | 评注 / SR | Wikisource「倒杖十二法」URL | 通过 |
| 10 | `L0202-L0223` | 操作 / SR | 标题十二、正文〇标十一杖（顺逆缩离没穿斗截对缀犯），terms 11 与源一致；不补第十二。离杖「壘土浮□」、逆杖「四獸鹹備」、斗杖「腕藍扳鞍」疑字/用字不一，notes 可核；各杖前提/否定句（冲脑散、顽硬天罡、土蚁、泥水等）与原文对齐 | 通过 |
| 11 | `L0228-L0228` | 评注 / SR | Wikisource「二十四砂葬法」URL | 通过 |
| 12 | `L0230-L0278` | 操作 / SR | 总例+〇标 24 法，terms 24 与源全等（担伞…牵弓）。回龙「生\<鼻勾\>\<鼻合\>」、停驿「登□□」、虚埙、撞穴「避兇就兇，假也靈塋」均存疑不补；斗斧「前朝不许」不读成禁看前朝；半纪/一纪/吞棺三分之一/挑饶三分不折算现代量。富贵灾祸句均标书内取象 | 通过 |

抽核未发现空模板白话、静默改正文、把书内取象升实证、或把 `verified` 置 true。元数据 7 段空 terms 合理；术文 6 段 terms 非空。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（YAML + 六章题 + 术文/URL）。13 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/疑字去向，不是影印逐字校勘，也不是阴宅断语有效证据，也不等于葬法/倒杖/砂法已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是葬法倒杖产品交付，也不覆盖生产侧 `docs/book-reviews/zangfa-daozhang.md`。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 注解 SHA256 | 与 Issue 钉死一致 | 通过 |
| `verified` 键缺失 | 13/13 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 章题未入段 | 6 个 `# …` 非空行 | inventory 口径；不扩 ID |
| 息法「四法」实列三 | 开篇斩截坠；吊在后文专释 | notes/白话已记。不改正文 |
| `高$山陰龍` | `$` 乱码 | 只定位 |
| 「垢復」 | 疑姤復 | 不改成已校卦名 |
| 「下薄莫粘」vs 后文反问 | 张力保留 | 不补否定字消矛盾 |
| 十二法 / 十一杖 | 〇 标 11；标题写十二 | 不凭通行记忆补第十二 |
| 离杖浮□、停驿登□□、合字占位 | 源内缺字/合文标记 | 只标阙 |
| 「鹹備」「腕藍/剜藍」「虛塤」 | 疑字或异写 | 各依本段，不径改 |
| 撞穴末句 | 「避兇就兇，假也靈塋」 | 文义别扭。不编两层凶 |
| catalog `references/fulltext` SHA | 与 `sources/fulltext` 不同 | 按 Issue/inventory 的 sources 路径审 |
| 富贵/灾祸/世出何人 | 书内取象 | 不升现实应验 |

## Caveat（不改注解，留给后续 pack）

1. **疑字与缺文不是已校定。** `$`、垢复、（後厥）、浮□、登□□、鼻旁合字占位、鹹/咸、腕/剜、虚埙、撞穴末句等仍待底本。
2. **十二法标题与十一杖正文不对齐。** 不得凭他本记忆补第十二杖名写入本包。
3. **息法开篇称四法却列三。** 吊法在分释中出现；不得改开篇句去强行对齐。
4. **书内尺寸与年数**（尺余、三尺、吞棺三分之一、挑饶三分、半纪、一纪）不得折成现代工程或统计。
5. **阴宅形势与葬法条件** 依赖现场勘验；当前产品无实测地形输入，不得生成施工参数或个人结果，更不冒称已接入八术页面。
6. **既有 `zangfa-daozhang.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。

## 8. 交付

| 项 | 值 |
|---|---|
| Issue | MING-456 |
| 分支 | `codex/multica-ming-456` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/zangfa-daozhang-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过**；SR remaining 0 |

下一步：协调者快速核对证据后闭环；无需重做 0–12；无需回改注解。
