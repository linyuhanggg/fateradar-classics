# 黄帝宅经 · 主本：独立审查 source-reviewed 全量（0–10 / 11）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-451` / 分支 `codex/multica-ming-451`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/huangdi-zhaijing.md`、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-447 / MING-448 / MING-446。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。

结论：**通过。** `validate-annotations` `ok=true entries=11 source_reviewed=11 errors=[]`；`verified` 键全缺（无一为 true）；0 draft；起 `huangdi-zhaijing:L0003-L0008` 止 `huangdi-zhaijing:L0080-L0080`；注解与段落库存 11/11 顺序全等。全书 11 段对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。风水材料不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-451`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/huangdi-zhaijing.json
shasum -a 256 sources/fulltext/fengshui/huangdi-zhaijing/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/huangdi-zhaijing.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/huangdi-zhaijing.json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `6028d432d75ed420f264e0b491f8cd813f431d3540756c5bb84b54d21968f9a2`（与 Issue 钉死一致） |
| 注解 blob | `90f6e7008899d2c3e3d62577dfb59b4348a1a0aa`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/huangdi-zhaijing/fulltext.md`（80 行） |
| 源 SHA256 | `30b07fbf1d391799b9288c1ef6825858f03ee112337e93c68cf5ebded52bc57d` |
| 库存段落 | `references/inventory/paragraphs/fengshui/huangdi-zhaijing.json` 11 条，ID 顺序与注解全等 |
| catalog `source_anchor_url` | 维基文库《宅经（四库全书本）》；`consolidated_catalog` 口径 |
| 工作树相对审查基线 | 仅新增本审查稿；注解 JSON / 源文 / 既有 `huangdi-zhaijing.md` 无 diff |

无越权文件。未碰 447/448/446 工作树或分支。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/huangdi-zhaijing.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 11, "source_reviewed": 11,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

11 条：`review=source-reviewed` 全 11；无 `draft`；无 `verified: true`（字段全部缺省，校验器与「verified 全 false」同口径）。空白话 0；白话全文重复组 0；空 terms 仅 1（`L0010-L0012` 格式残留，结构合法）；空 notes 0。`relatedParagraphIds` 3 条、共 4 个外键，全部落在本书 11 个 ID 内。kind 与库存逐条一致。

全书 kind：评注或元数据 4、操作步骤 2、规则候选 2、序跋目录 1、理论 1、重复 1。

无 `待核实` kind；疑点均以 notes 保留，不补造。关键保留项（对照原文，不回改）：

| 索引 | paragraphId | 保留原因（对照原文） |
|---|---|---|
| 3 | `huangdi-zhaijing:L0018-L0034` | 「十干十二支乾艮坤巽共为二十四路」字面 10+12+4=26，未删戊己凑 24 |
| 4 | `huangdi-zhaijing:L0038-L0047` | 「正月二月三月不得东户」句读/省略待校，未擅补操作动词 |
| 7 | `huangdi-zhaijing:L0055-L0057` | 「但细看之必有灾咎」语气不顺，未改成「必无灾咎」；缺图未复原 |
| 8 | `huangdi-zhaijing:L0059-L0067` | 「南方宜□拓吉」保留缺字；「甲巳日」「修己亥同」等夹注不自动改字；地府青龙处未补地支 |
| 9 | `huangdi-zhaijing:L0069-L0078` | 源「已朱雀龍頭」notes 保留「已朱雀」；两组喜忌不可并集 |

## 4. 索引边界

段落库存 11 段；注解覆盖 0–10，与库存 ID 列表逐项相等。`remaining=0` / 无 nextId，只相对本电子本 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `huangdi-zhaijing:L0003-L0008` |
| 注解索引 10（止） | `huangdi-zhaijing:L0080-L0080` |

非空源行 66；未入段仅 Markdown 标题 4 行（L1 `# 黄帝宅经`、L16 `### 宅經卷上`、L36 `### 凡修宅次第法`、L53 `### 宅經卷下`）。正文/提要/题记覆盖完整。`remaining=0` ≠ 人工 verified / ≠ 影印校勘 / ≠ 图式完整 / ≠ 产品交付。

电子本题卷：四库提要 → 卷上总论 → 修宅次第法 → 卷下土气表与两组二十四路条文。卷下自言「已下图」，当前电子文件无图。

## 5. 全书语义（11/11 对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/huangdi-zhaijing/fulltext.md` 的 `start_line–end_line`。本书仅 11 段，本岗全量对照，非抽样。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0008` | 序跋目录 / sr | 提要：旧题黄帝、汉隋唐宋目录未尽归黄帝→依托；二十四路阴阳；「疑即此书」保留不确定性；末署纪昀等 | 通过 |
| 1 | `L0010-L0012` | 评注或元数据 / sr | 三行均为 U+FEFF，无宅法正文；空 terms 合法；未改行号 | 通过 |
| 2 | `L0014-L0014` | 评注或元数据 / sr | 「欽定四庫全書」丛书题记，非宅法判断 | 通过 |
| 3 | `L0018-L0034` | 理论 / sr | 二十九宅书名；批五姓八宅；阳宅头亥尾巳 / 阴宅头巳尾亥；迁入方向定阴阳；福德/刑祸与天德月德例外；五虚五实；「人宅相扶」；26≠24 数差已记 notes | 通过 |
| 4 | `L0038-L0047` | 操作步骤 / sr | 先刑祸后福德；阴巳阳亥顺转；100/200 工；来路/抵路；龟头厅；四王神帝车辂舍；十二月生气死气表完整 | 通过 |
| 5 | `L0049-L0049` | 评注或元数据 / sr | 「宅經卷上」卷尾题记 | 通过 |
| 6 | `L0051-L0051` | 重复 / sr | 再次「欽定四庫全書」；`relatedParagraphIds`→`L0014-L0014` | 通过 |
| 7 | `L0055-L0057` | 操作步骤 / sr | 十二月土气所冲（正月丁未…十二月申庚）；「必有灾咎」原样保留；与卷上月生气表分列 | 通过 |
| 8 | `L0059-L0067` | 规则候选 / sr | 天门阳首、亥朱雀龙头；命座与宅福/明堂等分项；午忌高及龟头厅；人门可置牛马厩；「南方宜□拓吉」缺字保留 | 通过 |
| 9 | `L0069-L0078` | 规则候选 / sr | 乾天门高壮为吉；巳/已朱雀为阴宅龙头组；坤人门不宜马厩（与组 8 相反）；「一周二十四路」；两组不得并集 | 通过 |
| 10 | `L0080-L0080` | 评注或元数据 / sr | 「宅經卷下」卷尾题记；上下卷齐备≠图式/缺字已核 | 通过 |

关键条件与源行（全量核，非转引进度表）：

- 依托 / 疑即此书：L3–L6
- 阳宅龙头在亥尾在巳 / 阴宅龙头在巳尾在亥：L25–L26
- 入阳：巽→乾、午→子、坤→艮、酉→卯、戌→辰：L26
- 刑祸方天德月德到仍须避：L29
- 五虚五实：L31–L32
- 人宅相扶、不可独信命：L34
- 先修刑祸后修福德；阴巳阳亥；一百工/二百工：L38
- 来路/抵路（东来修东为来路、修西为抵路）：L42–L43
- 正月生气在子癸死气在午丁 … 十二月：L46–L47
- 土气所冲正月丁未 … 「必有灾咎」：L56–L57
- 南方宜□拓吉：L66
- 人门龙肠宜置牛马廄 vs 坤人门不宜置马厩：L63–L64 / L74
- 已朱雀龙头（源字「已」）：L72
- 从乾顺行至戌一周二十四路：L75

## 6. source-reviewed ≠ 人工 verified

本电子本来源为维基文库四库整理本。11 条 `source-reviewed` 只表示对照当前电子段落落实了提要署名辨析、阴阳二宅迁入条件、修宅次第与月表、两组二十四路喜忌分列及缺字/疑句去向，不是影印逐字校勘，也不是风水效验证据。风水材料进入可检索知识库，当前页面没有对应输入与算法，不得冒称已接入八术。不得把 11 条 source-reviewed 写成已人工 verified。`remaining=0` 仅对本电子本注解覆盖而言。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 字段缺省 | 11 条均无 `verified` 键；0 条 True | 与「全 false」同口径。不回改 |
| 空 terms | 1/11（`L0010-L0012`） | 格式残留，结构合法。不回改 |
| 26≠24 路数 | L23「十干十二支乾艮坤巽」 | notes 已记。不删戊己。不回改 |
| 缺图 | L57「已下图」；文件无图 | notes 已记。不复原图式。不回改 |
| 缺字 | L66「南方宜□拓吉」 | 保留缺字符号。不回改 |
| 「必有灾咎」 | L57 | 未改「必无」。不回改 |
| 源「已朱雀」 | L72 | notes 保留「已朱雀」；白话可读为巳。不回改源字 |
| 两组喜忌相反 | 人门马厩 / 天门高壮 | 注解已分表。不并集。不回改 |
| inventory `doubtful` | 仅 `L0059-L0067` 为 true | 与缺字/夹注一致。不回改 |
| 既有 `huangdi-zhaijing.md` | 生产审读稿仍在 | 本岗不覆盖；只新增 independent-review |

## Caveat（不改注解，留给后续 pack）

1. **无同书影印**：source-reviewed 停在电子语义；缺字、已/巳、必有灾咎、26≠24 保持 unknown/待校。
2. **卷下缺图**：条文可读，图式不可宣称复原；不能从 remaining=0 推出原著完帙。
3. **阴宅阳宅 ≠ 现代墓地/住宅**：依迁入方向与二气，不能并入八宅游年或玄空飞星。
4. **两组二十四路不可并集**：同一宫名/地支在两组喜忌可相反；接入时必须分表。
5. **时位表不接排盘**：月生气死气、土气所冲、可修月日均为本书文本表，不是现行择日引擎。
6. **`remaining=0`**：只表示本电子本 11 个 paragraphId 已尽；不是人工 verified、不是全书校勘、不是产品交付。

## 未决（本岗不施工）

- 缺图、缺字、路数矛盾、已/巳与「必有灾咎」：保持 notes / 回源，不升 verified。
- 11 条 source-reviewed 不是人工 verified，也不是风水效验，也不等同风水算法已实现。
- 本岗不回改注解、不改 `huangdi-zhaijing.md`、不碰 447/448/446。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-451`。该书 SR 审查 remaining **0**。
