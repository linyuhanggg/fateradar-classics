# 雪心赋：独立审查主本 source-reviewed 全量（文件索引 0–17）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-445` / 分支 `codex/multica-ming-445`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/xuexin-fu.md`、未抢 MING-424/431/439、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–17（18 条，全量）。

结论：**通过（有限范围）。** 结构校验 ok、`errors=[]`；18/18 `source-reviewed`、0 draft；`verified` 键全缺（无一为 true）；inventory 与注解 `paragraphId` 一一对应且同序；全书仅 18 段，本岗**全核 18/18**对照原文语义成立；采集元数据、疑字保留、应验断语边界与尾注剥离均可复核。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-445`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/xuexin-fu.json
git rev-parse HEAD:references/annotations/fengshui/xuexin-fu.json
shasum -a 256 sources/fulltext/fengshui/xuexin-fu/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `2c31b139c685d61d4733a0f2bec9e0a9e4a0cb90ee7cc786bc3c1849dfb21ec5`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `ca3a01f748066a89dd8befb4c2dacb983d03376e` |
| 源 `fulltext.md` SHA256 | `5e27d9aaf634f59e97cc1afb39382ae328425c437041eeb31447b6ba2c8cef83` |
| 源行数 | 338 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `xuexin-fu.md` 无 diff |

对照路径与 Issue 一致：`sources/fulltext/fengshui/xuexin-fu/fulltext.md`。

无越权文件。注解未改。源文未改。未写产品仓。未碰 424/431/439 独占范围。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/xuexin-fu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 18, "source_reviewed": 18,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`source_reviewed=18` 与 Issue 口径一致。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–17，18 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 18/18 |
| `review=draft` | 0 |
| `verified` 键 | **全缺**（18/18 无该字段；无一 `verified=true`） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 缺失 | 0 |
| 空 `terms` | 0 |
| `subsections` | 0 |
| `sourceAttribution` | 0 |

kind 分布：评注或元数据 1、理论 17。

Issue 钉死「verified 全 false」：本文件用缺省未升 verified（键缺失）表达，与「不得升人工 verified」一致；校验器仅在 `verified is True` 时报错，本包未触该条件。

Issue 钉死起 `xuexin-fu:L0003-L0007`、止 `xuexin-fu:L0326-L0338`：与文件索引 0、17 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/xuexin-fu.json` 18 段；注解 18 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同（inventory 字段名为 `id`，值与注解 `paragraphId` 一致）。

非空源行未入段者共 18 处：L1 书题 `# 雪心賦`，以及各 `##` 节题（L9/17/35/43/59/74/107/118/157/168/193/205/215/235/278/308/324）。其余非空行均落在某条 `paragraphId` 内。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起） | `xuexin-fu:L0003-L0007` | 采集元数据 / URL，非正文 |
| 索引 1 | `xuexin-fu:L0011-L0016` | 《论山川理气》开篇 |
| 索引 8 | `xuexin-fu:L0120-L0156` | 《论穴法》最长段 |
| 索引 14 | `xuexin-fu:L0237-L0277` | 穴形异同与凶形应验 |
| 索引 17（止） | `xuexin-fu:L0326-L0338` | 勉学劝善 + 网页尾注 |

本包后该书 SR 审查 remaining **0**。这只表示 18 主段都已有 source-reviewed 注解并经本岗全核，不是 338 行逐字影印校勘，也不是 verified。既有 `docs/book-reviews/xuexin-fu.md`（生产侧账本）不覆盖、不回改。

## 5. 全量语义（18/18，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/xuexin-fu/fulltext.md` 的行范围。全书仅 18 段，本岗全部抽核（满足 ≥15，且覆盖元数据、理气、水法、龙虎、穴法、克择、应验、阳宅、收束）：

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0007` | 评注或元数据 / SR | 源为 source_base/URL/normalized_note；白话标明网页白文+影印锚点、非逐字校；notes 确认非正文 | 通过 |
| 1 | `L0011-L0016` | 理论 / SR | 形气阴阳、生旺休囚、人体/地形类比；未给可测步骤；「地灵人杰」notes 不升实证 | 通过 |
| 2 | `L0019-L0034` | 理论 / SR | 入山水口、登穴明堂、祖宗子孙/宾主；贵显说与观察顺序分层；「淚淚」保留不改正文 | 通过 |
| 3 | `L0037-L0042` | 理论 / SR | 分合向背；反对小醇大疵/众凶寻一吉；倒杖与卦例批评；不把「合则从」单独升合格 | 通过 |
| 4 | `L0045-L0058` | 理论 / SR | 山形五星剥换与形似易混；非天文七政；活龙活蛇为形势辞 | 通过 |
| 5 | `L0061-L0073` | 理论 / SR | 交锁织结 vs 穿割箭射；元辰直出+外拦反吉；水口葫芦喉与抱身牛角分层 | 通过 |
| 6 | `L0076-L0106` | 理论 / SR | 近朝优于远朝；生旺休废互审；水底/石间穴不指导开挖；当生不生/见死不死连支持关系读 | 通过 |
| 7 | `L0109-L0117` | 理论 / SR | 龙虎回不去逼、缺侧以水补、莫把水为定格；长房/小子 notes 不推现实家庭 | 通过 |
| 8 | `L0120-L0156` | 理论 / SR | 移步换形、动静有情、高低缓急、单山须关拦；「何用九星八卦」保留顾内回头语境；不扩施工尺寸 | 通过 |
| 9 | `L0159-L0167` | 理论 / SR | 穴吉仍忌葬凶；择年月日；批评偶中自神；无择日表；子午针不解决磁偏 | 通过 |
| 10 | `L0170-L0192` | 理论 / SR | 看格胜看书、信眼；内外隐拙；三合四冲只列名目不生成应期测试；看格≠八字格局 | 通过 |
| 11 | `L0195-L0204` | 理论 / SR | 罗城水口、华表捍门；近护优于远高；八门缺在地理语境非奇门排法；深穴无工程深度 | 通过 |
| 12 | `L0207-L0214` | 理论 / SR | 砂水吉凶；形势优先于星辰卦例；九曲九迁为取象非数量晋升公式 | 通过 |
| 13 | `L0217-L0234` | 理论 / SR | 文笔旗鼓仓库等官品取象辞汇；颜回彭祖石崇裴度缺输入不升复算案例；天乙太乙不接产品神煞 | 通过 |
| 14 | `L0237-L0277` | 理论 / SR | 形似易误、主宾改义、小土堆不径断眼患；保留旧时代品行断语边界；不升医疗/品行鉴定 | 通过 |
| 15 | `L0280-L0307` | 理论 / SR | 关藏空缺、声响、急缓；宗庙水法误人 vs 山运有准分立场；不折流派为一套 | 通过 |
| 16 | `L0310-L0323` | 理论 / SR | 阳宅宽平、山谷凹风、平洋得水；孔林/龙虎山为例不升算法正例；不推荐买房改建 | 通过 |
| 17 | `L0326-L0338` | 理论 / SR | 尽信书不如无书、积德与著赋之意；尾注 2011/HKDNR 标为网页附属非古籍理论 | 通过 |

抽核未发现空模板白话、把应验断语升实证、把网页尾注当正文理论、或把 `verified` 置 true。失败 paragraphId：**无**。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1 书题「雪心賦」；L3–7 采集元数据；L11–338 正文入段，中间节题不入 inventory）。18 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/边界去向，不是影印逐字校勘，也不是风水断语有效证据，也不等于寻龙/穴法/阳宅已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是雪心赋全书产品交付，也不覆盖生产侧 `docs/book-reviews/xuexin-fu.md`。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺失 | 18/18 无字段；无 true | 等价未升 verified。不回填 false 键 |
| L0003–L0007 元数据 | 源为 URL/采集说明 | notes 已标非正文。不改正文混入 |
| 「淚淚」 | L0024 转录字形 | notes 保留。不猜改 |
| 山形五星 vs 天文五星 | 论五星段 | notes 已分层。不接七政历算 |
| 「八门缺、八风吹」 | 罗城水口段 | 地理围护语境。不接奇门八门 |
| 「看格」 | 古格宜看段 | 形局观察。不接八字格局模块 |
| 应验取象（九迁、官品、疾病婚配） | 多段 | 传统辞汇。不升实证/医疗/品行规则 |
| 网页尾注 L0335–L0338 | 全文完 + 2011 版权 + HKDNR | notes 已剥离。不入理论 |
| 既有 `xuexin-fu.md` | 生产侧审读账本 | 本独立审查文件并存。不互相覆盖 |

## Caveat（不改注解，留给后续 pack）

1. **电子底本≠影印校定。** 白文来自网页转录；书格/Wikimedia/NCL 仅作版本锚点，本包未做逐字对校。
2. **应验断语与房份/疾病/品行说** 是原文传统取象，不是可复算案例或用户鉴定规则。
3. **流派取法立场**（重形势、批评机械卦例/宗庙水法）不得折成产品统一排盘表。
4. **既有 `xuexin-fu.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。
5. **风水材料** 不冒充已接入八术页面或引擎。

## 8. 交付

| 项 | 值 |
|---|---|
| Issue | MING-445 |
| 分支 | `codex/multica-ming-445` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/xuexin-fu-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后闭环；无需重做 0–17；无需回改注解。
