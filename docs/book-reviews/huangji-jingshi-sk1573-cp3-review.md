# 皇極經世書 · 识典 SK1573：独立审查 CP3（600–669 收尾）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-416` / 分支 `codex/multica-ming-416`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1/CP2 审查稿、未改进度文档、未改 DZ1040 / 主本 `huangji-jingshi.json` / HY1442 / SK1603 / HY1521 / SK1609 / 指南 / 引擎 / `chart.*` / golden。本岗未参与该书生产。不要重做 CP1/CP2（0–599）。不要抢六壬/秘本。不是皇极经世全书完成，也不是引擎包，也不是全项目完成。禁止重做 HY1442 / SK1603。

结论：**通过。** 本包只审索引 **600–669**（70 SR + 0 draft）；`validate-annotations` `ok=true entries=670 errors=[]`；`verified` 全 false；≥15 段非模板抽读对照 `sources/normalized/shidianguji/SK1573/text.md` 成立，关键句亦见于 `sources/fulltext/divination/huangji-jingshi/fulltext.md`。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。本包后该书 SR 审查 remaining **0**（仅指识典 SK1573 本 edition 注解段落集；≠全书/主本/DZ1040 完成）。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-416`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/divination/huangji-jingshi--shidian-SK1573.json
shasum -a 256 sources/normalized/shidianguji/SK1573/text.md
shasum -a 256 sources/fulltext/divination/huangji-jingshi/fulltext.md
git rev-parse HEAD:references/annotations/divination/huangji-jingshi--shidian-SK1573.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与本岗 HEAD / Issue 钉死一致） |
| 注解文件 SHA256 | `05a054d299a123ed20d5c6edaf3a921f0eb3e9fe13a2d9854ecd6ce82effb513`（与 Issue 一致） |
| 注解 blob | `f13177dc55c0e9bf4f49923bbd594e0c23f70659` |
| 源 `SK1573/text.md` SHA256 | `c101c5a29e96da89e45fdb3b01c879308c74767d1071531e202706c50791e34a` |
| 主本 `fulltext.md` SHA256 | `aeceef2a904d915ecce2739d65f0225c5aa5ab47c7a3446264a2b505f16d4d80` |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 84 条，未补造） |
| `paragraphCount` / `figureCount` | 670 / 0 |
| 注解 ID 与 `paragraphs.json` 全书 | 670/670 一一对应，`mismatch=0` |
| 本包覆盖 | 仅索引 600–669；未改 0–599；未写/改 CP1/CP2 审查稿 |
| 本岗写出 | 仅 `docs/book-reviews/huangji-jingshi-sk1573-cp3-review.md` |

无越权文件。源层未改。他书 / 引擎 / `chart.*` / CP1/CP2 审查稿未覆盖。`scopeNote` 已写明补本不替代主本、不作独立投票。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/huangji-jingshi--shidian-SK1573.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 670, "source_reviewed": 670,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

本包 CP3（600–669）70 条：

| 字段 | 实测 |
|---|---|
| `review` | `source-reviewed` 70 / 70 |
| `verified` | 全 `false`（true=0） |
| `draft` 字段 | 0（无 draft） |
| `kind` | 理论 70 |
| 空白话 / 空 notes / 空 terms | 0 / 0 / 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」空模板 | 0 |
| 白话全文重复组（≥3） | 0（去除包级后缀后 lead 亦无 ≥2 重复） |
| `figureCount` | 0 |

全书 670 条：`review=source-reviewed` 全 670；`verified` 全 `false`。无升 verified。

## 4. 索引边界

`paragraphs.json` 全书 670 段。本包只审 600–669。0–299 / 300–599 不在本包语义重审范围（只读确认边界 ID，不回改）。

| 位置 | 实测 ID | 源行 |
|---|---|---|
| 注解索引 599（CP2 止，不在本包） | `huangji-jingshi:shidian-SK1573:P7637911014440747034` | L2999–3002 |
| 注解索引 600（CP3 起） | `huangji-jingshi:shidian-SK1573:P7637911014440763418` | L3004–3004 |
| 注解索引 669（CP3 止 / 全书末） | `huangji-jingshi:shidian-SK1573:P7637911015330775090` | L3249–3252 |

起始/止点与 Issue 钉死 ID 一致。区段均为网站章节「觀物外篇下」续文至卷十四题记。本包后该书 SR 审查 remaining **0**（相对本注解 paragraphId 集合）；`catalogComplete` 仍 false。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1573/text.md` 的 `start_line–end_line`。关键句亦在主本 `sources/fulltext/divination/huangji-jingshi/fulltext.md` 可检索到（如「神妙致一」「金須百鍊」「記問之學」「用兵之道」「陽性而隂情」「王通」「皇極經世書卷十四」）。外篇下标理论（天地人物义理 / 为学养心，不是占断）。下列为非模板抽核。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 600 | `…0763418` | 理论 / sr | 源 L3004「物，」。CP3 起句残片；白话前半「物」 | 通过 |
| 601 | `…0779802` | 理论 / sr | 「一作造萬物」。异文注记 | 通过 |
| 602 | `…0796186` | 理论 / sr | 源「神」单字残片 + 主题 gloss | 通过（见 caveat） |
| 605 | `…0845338` | 理论 / sr | 「精氣為物，形也」。神气形体 | 通过 |
| 610 | `…1451546` | 理论 / sr | 「故形在則魄存」 | 通过 |
| 615 | `…1533466` | 理论 / sr | 「陽性而隂情…以類而應也」。性情色类 | 通过 |
| 620 | `…1615386` | 理论 / sr | 「無思無為者，神妙致一之地也，所謂一以貫之」 | 通过 |
| 625 | `…1697306` | 理论 / sr | 「以強通」。残片 | 通过（见 caveat） |
| 630 | `…1779226` | 理论 / sr | 「天下之事，皆以道致之…能安分則謂之道」 | 通过 |
| 635 | `…9415218` | 理论 / sr | 「一國、一家、一身皆同…則能處一國」 | 通过 |
| 640 | `…9497138` | 理论 / sr | 「斂天下之善…禹不自滿假…無德者…易滿」 | 通过 |
| 645 | `…9579058` | 理论 / sr | 「無力者…以為弓强。何不思之甚也」 | 通过 |
| 650 | `…9660978` | 理论 / sr | 「知之者鮮…金須百鍊然後精」 | 通过 |
| 655 | `…9742898` | 理论 / sr | 「天下之良醫也。能處人所不能處之事」 | 通过 |
| 660 | `…0627634` | 理论 / sr | 「得失不動心…行險僥倖，是逆天也」 | 通过 |
| 665 | `…0709554` | 理论 / sr | 「用兵之道，必待人民富，倉廪實…」 | 通过 |
| 668 | `…0758706` | 理论 / sr | 「不可謂之學」 | 通过 |
| 669 | `…0775090` | 理论 / sr | 「記問之學…王通云沒身而已」+「皇極經世書卷十四」。全书末 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- CP3 起残片「物」：L3004
- 一作造万物：L3006
- 精气为物：L3016
- 形在则魄存：L3028
- 阳性而阴情：L3041–3042
- 无思无为 / 一以贯之：L3063
- 以道致之 / 安分：L3103–3105
- 一国一家一身：L3129–3130
- 禹不自满假：L3146–3151
- 金百炼：L3187–3189
- 得失不动心 / 行险侥幸：L3221–3222
- 用兵之道：L3237
- 记问之学 / 王通 / 卷十四末：L3247–3252

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。本包 70 条电子语义阅读为 `source-reviewed`，只表示对照电子段落实了外篇下义理 / 为学养心层次与未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本，不计独立投票，不等同皇极算法已实现。观物外篇是数理与人事义理，不是占断。不得把 670 条 source-reviewed 写成已人工 verified。本包收尾后识典 SK1573 本文件 SR 审查 remaining 0，不是皇极经世全帙，也不是产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 包级 notes 套语 | 69/70 条 notes 元组相同；末条否定「不是占断…不等同皇极算法已实现」；索引 669 另含卷题说明 | 否定升 verified，不是空白话。不回改 |
| 观物外篇下白话后缀 | 69/70 含「观物外篇下数理/象数与人事义理论述，不是占断，也不等同皇极算法已实现。」；669 用「观物外篇下义理收束…」变体 | 套语后缀，前半对照源文。不是空模板。不回改 |
| 主题 gloss 批标签 | 「观物外篇下义理续论」「神气形体次第」「为学养心与才德人事义理」等 | 批处理主题标签，前半仍对源。不回改 |
| 截断段 + gloss 粘连 | 本包短源（≤6 汉字）约 13 条：600/601/602/603/605/606/610/612/624/625/634/664/668 | 残片后接主题标签。结构仍 source-reviewed。不回改；见 caveat |
| terms 偏泛 | 70/70 含「观物外篇」；另「至诚」2、「为学」1 | 结构合法。抽核源均在外篇下。不回改 |
| 索引 516（CP2 范围） | 不在本包；本岗不重审、不回改 | 遵守不重做 0–599 |

## Caveat（不改注解，留给后续 pack）

1. **截断段 gloss 粘连（本包约 13 条）**：如索引 600「物」/ 602「神」/ 603「人，一无」/ 624「不可」/ 625「以强通」等。电子行切残片后直接拼接主题标签，引用须回源行，不能只看白话末句主题词。
2. **主题 gloss 批标签**：外篇下「义理续论 / 神气形体次第 / 为学养心」是包级分类词，不是逐句新义；抽规则须回源。
3. **`remaining=0`**：只表示识典 SK1573 本注解文件 paragraphId 的 SR 审查已尽；`catalogComplete=false`、缺章 84、主本/DZ1040 不在本包。
4. **历史 CP2 审查稿曾覆盖 300–669**：本 Issue 将收尾重钉为独立 CP3（600–669）。本岗不改既有 CP1/CP2 审查稿，不把旧稿范围当作本包重做依据。

## 未决（本岗不施工）

- 截断段粘连白话：保持回源，不升 verified。
- 识典待校。670 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同皇极算法已实现。
- 主本 / DZ1040 不在本包范围；识典 SR 审查收尾不等于皇极经世全书完成。
- 本岗不回改注解、不重做 CP1/CP2（0–599）、不碰 HY1442 / SK1603 / 六壬 / 秘本。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-416`。远端仓 `linyuhanggg/fateradar-classics`。
