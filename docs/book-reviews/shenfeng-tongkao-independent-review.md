# 神峰通考 · 主本：独立审查 source-reviewed 全量（0–14 / 15）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-463` / 分支 `codex/multica-ming-463`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / executable、未抢 MING-447/452、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不要与《子平真诠》《渊海子平》混淆（后者仅在序言被引书名）。本包只审注解文件索引 0–14（15 条，全量）。

结论：**通过。** 结构校验 `ok=true entries=15 source_reviewed=15 errors=[]`；`verified` 全为 `false`（15/15）；0 draft；起 `shenfeng-tongkao:L0003-L0004` 止 `shenfeng-tongkao:L4826-L5106`；注解与段落库存 15/15 ID 顺序全等。全书 15 段均对照电子原文抽核成立；七正文 vernacular / subsections 小节数 75/64/61/71/68/75/21 共 **435** 与 scopeNote 一致，小节行锚全部落在所属 paragraphId 范围内。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-463`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/bazi/shenfeng-tongkao.json
git rev-parse HEAD:references/annotations/bazi/shenfeng-tongkao.json
shasum -a 256 sources/fulltext/bazi/shenfeng-tongkao/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `ae4c0d97ae41ffa383cd18487bf4efc78a841d5565e6abb6ecad7852b8f1bee5`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `ccfc51efb3d4dd23e78db29590ec36c57986b361` |
| 实际源文 | `sources/fulltext/bazi/shenfeng-tongkao/fulltext.md`（5106 行） |
| 源 SHA256 | `3cb92ceeea29b0c6d38cbd21e67780d47ff6c758793256e1a4a2fa1f464eddd3` |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / inventory 无 diff |

对照路径：Issue 写 `sources/fulltext/bazi/shenfeng-tongkao/fulltext.md`，与 inventory `fulltext` 字段一致。catalog 另记 `references/fulltext/...` 与不同 SHA（`d1e3de0f…`），属蒸馏包路径；本岗按 inventory / Issue 钉死的 `sources/fulltext` 抽核，不另造副本。

catalog：`slug=shenfeng-tongkao`；`source_anchor_url` CTP 总页；`source_risk` 已提示张楠正文/补曰/古赋/命例未拆层、局部异文需影印、疾病寿夭女命高风险须安全改写。`source_provenance_status=consolidated_catalog`。

无越权文件。注解未改。源文未改。未写产品仓。未碰 447/452 工作树或分支。未碰 `ziping-zhenquan` / `yuanhai-ziping` 注解。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/shenfeng-tongkao.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 15, "source_reviewed": 15,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发（全部显式 `verified: false`）。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–14，15 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 15/15 |
| `review=draft` | 0 |
| `verified` | **15/15 均为 `false`**（无 true；无缺键） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 元数据段空 `terms` / 空 `notes` | 8/8 元数据段（结构合法；术文段 notes/terms 非空） |
| `relatedParagraphIds` | 全无 |
| 额外键 | 有 `subsections`（仅 7 条理论段；435 小节与 vernacular `【…】` 标题一一对应） |

kind 分布（注解）：评注或元数据 8、理论 7。inventory 模式初筛 kind（待分类/案例/操作步骤）与注解 kind 不一致——属 inventory `classification_note` 已声明的「文本模式初筛 ≠ annotation」，**不回改** inventory，也不据此判注解失败。

Issue 钉死起 `shenfeng-tongkao:L0003-L0004`、止 `shenfeng-tongkao:L4826-L5106`：与文件索引 0、14 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/bazi/shenfeng-tongkao.json` 15 段；注解 15 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory `id` 列表相同。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起） | `shenfeng-tongkao:L0003-L0004` | YAML/采集说明（CTP 七章节） |
| 索引 1 | `shenfeng-tongkao:L0008-L0009` | Part01 source_url + row_range |
| 索引 2 | `shenfeng-tongkao:L0011-L0787` | 第一正文（至正财格跨章开头） |
| 索引 3 | `shenfeng-tongkao:L0791-L0792` | Part02 URL 元数据 |
| 索引 4 | `shenfeng-tongkao:L0794-L1545` | 第二正文（承正财半句） |
| 索引 5 | `shenfeng-tongkao:L1549-L1550` | Part03 URL |
| 索引 6 | `shenfeng-tongkao:L1552-L2273` | 第三正文（至骨髓歌乙日跨页） |
| 索引 7 | `shenfeng-tongkao:L2277-L2278` | Part04 URL |
| 索引 8 | `shenfeng-tongkao:L2280-L3197` | 第四正文（至四言独步跨章） |
| 索引 9 | `shenfeng-tongkao:L3201-L3202` | Part05 URL |
| 索引 10 | `shenfeng-tongkao:L3204-L3960` | 第五正文（渭泾论中截） |
| 索引 11 | `shenfeng-tongkao:L3964-L3965` | Part06 URL |
| 索引 12 | `shenfeng-tongkao:L3967-L4819` | 第六正文（渭泾续→定真→憎爱赋开头） |
| 索引 13 | `shenfeng-tongkao:L4823-L4824` | Part07 URL |
| 索引 14（止） | `shenfeng-tongkao:L4826-L5106` | 第七正文（憎爱续→万金/相心等→病源赋末） |

未入段行主要为 CTP 章题（`## CTP Part 0N …`）与空行，与 15 稳定段口径一致。本包后该书 SR 审查 remaining **0**。这只表示 15 主段都已有 source-reviewed 注解并经本岗全核，不是 5106 行逐句影印校勘，也不是 verified。

## 5. 全量语义核（15/15，对照原文）

原文取 `sources/fulltext/bazi/shenfeng-tongkao/fulltext.md` 的行范围。元数据段全文核读；七理论段按全部 vernacular 小节标题行锚核对起止原文，并抽核跨章衔接、缺月、疑字去向与「不作预测/不升 verified」边界。小节行锚 `Lα–Lβ` 共 435 处，**0** 处越出所属 paragraphId。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0004` | 评注 / SR | YAML：`source_base` CTP 七章节；白话标明非张氏原文、七网页≠七原卷 | 通过 |
| 1 | `L0008-L0009` | 评注 / SR | Part01 `source_url` chapter=739505 与 global1–309；白话区分采集行号与 Markdown 物理行 | 通过 |
| 2 | `L0011-L0787` | 理论 / SR | 75 小节：题署张楠→序言沿革（引《渊海子平》书名层）→五星身命/宫度→子平谬说/病药动静盖头→多格与合官合杀→L786–787 正财格跨章半句。疑字/括注后世层/自述验数均保留不升实证 | 通过 |
| 3 | `L0791-L0792` | 评注 / SR | Part02 URL chapter=552406；白话点明续前正财半句、非另起原卷 | 通过 |
| 4 | `L0794-L1545` | 理论 / SR | 64 小节：L794「也。」承接前章；从财/伤官食神/希文自造分层；notes 记真假伤官与印运疑文不固化喜忌表 | 通过 |
| 5 | `L1549-L1550` | 评注 / SR | Part03 URL；开头续库官论 | 通过 |
| 6 | `L1552-L2273` | 理论 / SR | 61 小节：杂气/金神/飞天禄马/子遥巳丑遥巳等；虚格疑议与有条件采例并存；末骨髓歌乙日子–辰跨页 | 通过 |
| 7 | `L2277-L2278` | 评注 / SR | Part04 URL；接乙日巳月歌 | 通过 |
| 8 | `L2280-L3197` | 理论 / SR | 71 小节：骨髓歌续完十二月；**己日月歌 L2323–2333 仅 11 条（子丑卯…亥，缺寅）** 白话不补第十二；干支体象/十干禄/图表平铺待核；四言独步跨章开头 | 通过 |
| 9 | `L3201-L3202` | 评注 / SR | Part05 URL；承四言独步 | 通过 |
| 10 | `L3204-L3960` | 理论 / SR | 68 小节：四言续→五言→喜忌篇→三元等；女命婚丧品行旧断标历史文本；渭泾论始于 L3887，本章止 L3960 胞胎财官截点 | 通过 |
| 11 | `L3964-L3965` | 评注 / SR | Part06 URL；承渭泾 | 通过 |
| 12 | `L3967-L4819` | 理论 / SR | 75 小节：渭泾续杀枭差错（篇题在上章）→定真篇→绿珠譬喻不得计实证案例→憎爱赋 L4817 跨章开头 | 通过 |
| 13 | `L4823-L4824` | 评注 / SR | Part07 URL；承憎爱赋 | 通过 |
| 14 | `L4826-L5106` | 理论 / SR | 21 小节：憎爱续→万金/相心/仙机/金玉等→病源赋 L5069 起至 L5106 电子全文末；医学/针灸修辞不作医实；不证明原刻无缺页 | 通过 |

锚定抽核（非转引进度表）：

- 题署「神峰通考 明 张楠 著」：L11
- 序引《渊海子平》书名（非本书）：L22、L29；全书 **0** 处「子平真诠」
- 五星逢卯安命逢酉安身：L36–37
- 正财跨章：L786–787 半句 → L794「也。」续完
- 金神格 / 飞天禄马：L1590+、L1606+
- 己土子→亥月歌缺寅：L2323–2333（无「己土寅月」行）
- 渭泾论篇题：L3887（第五正文内）；第六起 L3967 续正文
- 憎爱赋：L4817；第七续 L4826
- 万金赋篇题：L4842；病源赋：L5069；电子末行：L5106

抽核未发现空模板白话、静默改正文、把书内取象升实证预测、把 CTP 网页章当成原书卷界、或把 `verified` 置 true。元数据 8 段空 terms/notes 合理；术文 7 段 notes 非空且与疑点对应。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本为 CTP Wiki 七章节抽取平铺，含张楠正文、楠曰/补曰、古赋、命例与后世辑录，**未按原刻分卷拆层**。15 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/跨章衔接/疑字去向，不是影印逐字校勘，也不是命理断语有效证据，也不等于病药/从财/飞天等已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是神峰通考产品交付，更不冒充已接入八术页面。不要与 `ziping-zhenquan` / `yuanhai-ziping` 混为一书。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified: false` | 15/15 | 保持。不升 true |
| CTP 七网页 ≠ 七原卷 | 元数据与各章 vernacular 均已声明 | 不回改源结构 |
| 跨章半句/篇题截断 | 正财、骨髓歌乙日、四言、渭泾、憎爱等多处 | 注解已标续接；不补造「完整卷」 |
| 己日月歌缺寅 | L2323–2333 仅 11 月 | 白话不补；保留 |
| inventory kind ≠ annotation kind | 模式初筛 vs 人工 kind | 不回改 inventory |
| catalog `references/fulltext` SHA ≠ `sources/fulltext` | 蒸馏包 vs 权威源路径 | 本岗只核 Issue/inventory 的 `sources/fulltext` |
| 图表平铺 / 疾病寿夭女命高风险 | catalog `source_risk` + 注解 caveats | 不升 verified；不作现实医断/品行断 |
| `references/executable/shenfeng-tongkao.json` | 存在；本岗未打开改写 | 只读边界外，不改 |

## 8. 交付边界

- 本 Issue 写出：仅 `docs/book-reviews/shenfeng-tongkao-independent-review.md`
- 远端：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-463`
- 基线：`6effd8e4f951fd17e1b1e0454942946ebc765da9`
- 注解 SHA256：`ae4c0d97ae41ffa383cd18487bf4efc78a841d5565e6abb6ecad7852b8f1bee5`
- 本包后 remaining：**0**
- 不宣称产品交付、不宣称人工 verified、不 main 合并、不部署
