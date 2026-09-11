# 皇極經世書 · 识典 SK1573：独立审查 CP2（300–669）

审查对象：`origin/codex/multica-ming-168` @ `a4c1eda8d1a0d21564c4f8bc8967eba5b46f72f5`（父 CP1 `40f17d1dbbb2f76a1bf13f206a8c893e81591046`，MING-155）。工作树只读参考 `fateradar-multica-ming-168`，本岗写出仅本文件。未改注解 JSON、未改源文、未改 DZ1040 / 主本 `huangji-jingshi.json` / HY1442 / SK1603 / HY1521 / SK1609 / 指南 / 引擎 / `chart.*` / golden / MING-163 CP1 审查稿。不是皇极经世全书完成，也不是引擎包，也不是全项目完成。禁止重做 HY1442 / SK1603。不是重做 CP1（MING-163 / MING-155 已 done）。

结论：**通过。** 相对 CP1 仅注解+进度；0–299 字节级未改；`validate-annotations` `ok=true entries=670 errors=[]`；`verified` 全 false；索引 516 待核实不补造；≥15 段非模板抽读对照原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指识典 SK1573 本 edition 段落集。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-174`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-168
git rev-parse HEAD HEAD^
git diff 40f17d1..HEAD --name-only
git diff --stat 40f17d1..HEAD
shasum -a 256 sources/normalized/shidianguji/SK1573/text.md
git rev-parse 40f17d1:sources/normalized/shidianguji/SK1573/text.md
git rev-parse HEAD:sources/normalized/shidianguji/SK1573/text.md
git rev-parse 40f17d1:references/annotations/divination/huangji-jingshi--shidian-DZ1040.json
git rev-parse HEAD:references/annotations/divination/huangji-jingshi--shidian-DZ1040.json
git rev-parse 40f17d1:sources/normalized/shidianguji/HY1442/text.md
git rev-parse HEAD:sources/normalized/shidianguji/HY1442/text.md
git rev-parse 40f17d1:sources/normalized/shidianguji/SK1603/text.md
git rev-parse HEAD:sources/normalized/shidianguji/SK1603/text.md
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-168` | `a4c1eda8d1a0d21564c4f8bc8967eba5b46f72f5`（本岗检出基线与 `ls-remote` 一致） |
| 父提交（CP1） | `40f17d1dbbb2f76a1bf13f206a8c893e81591046`（`HEAD^`） |
| 相对 CP1 文件 | 仅 2 个：`references/annotations/divination/huangji-jingshi--shidian-SK1573.json`、`docs/book-reviews/huangji-jingshi-sk1573-progress-2026-09-11.md` |
| diffstat | `+6055 / -25`（注解扩写 + 进度更新） |
| 源 `text.md` SHA256 | `c101c5a29e96da89e45fdb3b01c879308c74767d1071531e202706c50791e34a`（与 Issue / 进度一致） |
| 源 blob 父 vs 本提交 | 同为 `e35bc972df2db485ac022f835f303050d071db4a`（本提交未改源层） |
| DZ1040 注解 blob | 同为 `3df402d8bd8c` 前缀，未改 |
| HY1442 / SK1603 源 blob | 与父提交相同 |
| CP1 条目 0–299 | 与 `40f17d1` 注解 JSON **完全一致**（`mismatches=0`） |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 84 条，未补造） |
| `paragraphCount` / `figureCount` | 670 / 0 |
| 注解 ID 与 `paragraphs.json` 300–669 | 370/370 一一对应，`mismatch=0`；全书 670/670 |

无越权文件。源层未改。DZ1040 / HY1442 / SK1603 / 他书 / 引擎 / `chart.*` / CP1 审查稿未覆盖。`scopeNote` 已写明补本不替代主本、不作独立投票。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-168 活树）：

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

670 条：`review=source-reviewed` 全 670；`verified` 全 `false`；无 `draft` 字段。无升 verified。

全书 kind：理论 636、案例 17、序跋目录 10、评注或元数据 4、待核实 3。

本包 CP2（300–669）kind：理论 365、序跋目录 3、评注或元数据 1、待核实 1。与交包自称一致。

空白话 0、空 notes 0、空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组（≥3）0。本包 `figureCount=0`。

待核实仅索引 **516** `huangji-jingshi:shidian-SK1573:P7637911011882680347`（源「月半盈半𧇊」罕见字形，保留 unknown，不补造）。与交包一致。

## 4. 索引边界

`paragraphs.json` 全书 670 段；本包注解覆盖 300–669，连同继承的 0–299 共 670。进度 `remaining=0` / `nextId` 无，只相对本注解 paragraphId 集合；`catalogComplete` 仍 false。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（CP1 起，本包只读） | `huangji-jingshi:shidian-SK1573:P7430493364681703433` |
| 注解索引 299（CP1 止，本包未改） | `huangji-jingshi:shidian-SK1573:P7637911008657817609` |
| 注解索引 300（CP2 起） | `huangji-jingshi:shidian-SK1573:P7637911008657833993` |
| 注解索引 516（待核实） | `huangji-jingshi:shidian-SK1573:P7637911011882680347` |
| 注解索引 669（CP2 止 / 全书末条） | `huangji-jingshi:shidian-SK1573:P7637911015330775090` |

区段：观物外篇上续（300–457）→ 卷十四卷端（458–460）→ 观物外篇下（461–669）。起始/止点与 Issue 钉死 ID 一致。`remaining=0` ≠ 人工 verified / ≠ 皇极全书校勘 / ≠ 主本或 DZ1040 完成。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1573/text.md` 的 `start_line–end_line`。外篇上续标理论（裁数/策数/真数）；卷端标序跋/元数据；外篇下标理论（天地人物义理，不是占断）。下列为非模板抽核。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `P…7833993` | 理论 / sr | 源 L1704–1705「五十六裁為四十二」。CP2 起句，圆方裁数 | 通过 |
| 301 | `P…6962826` | 理论 / sr | 「六十四裁為四十八也」。续裁数 | 通过 |
| 320 | `P…2296499` | 理论 / sr | 「用以體為基，故存一也」。体用存一 | 通过 |
| 350 | `P…0722342` | 理论 / sr | 卦数去四，阴策二十四与三十二合五十六。蓍策 | 通过 |
| 380 | `P…082790` | 理论 / sr | 「七七四十九，大衍之用數也」 | 通过 |
| 400 | `P…0661530` | 理论 / sr | 易有真数三；参天三三而九，两地倍三而六 | 通过 |
| 420 | `P…0989210` | 理论 / sr | 四分八、十六、三十二、六十四。二分递生 | 通过 |
| 450 | `P…074766` | 理论 / sr | 地以既成；阳上阴下尊卑 | 通过 |
| 457 | `P…188454` | 理论 / sr | 阴符七国时书；韵法阖辟律天；卷十三题。外篇上收束 | 通过 |
| 458–460 | `P…059699` 等 | 序跋/评注 / sr | 钦定四库；卷十四；宋邵雍撰。版式/卷端，不是断法 | 通过 |
| 461 | `P…108851` | 序跋 / sr | 篇题「觀物外篇下」。网站章 ≠ 印本卷号 | 通过 |
| 480 | `P…926683` | 理论 / sr | 阳尊而神役物藏用；生死主于阳；升降消长 | 通过 |
| 500 | `P…254363` | 理论 / sr | 天行昼夜，日行寒暑 | 通过 |
| 516 | `P…680347` | 待核实 / sr | 「月半盈半𧇊」罕见字形；白话保留原形，不改正文 | 通过 |
| 580 | `P…435738` | 理论 / sr | 坤血艮肉坎髓巽骨等十二卦配身。象数配属，不是占断 | 通过 |
| 620 | `P…615386` | 理论 / sr | 无思无为，神妙致一，一以贯之 | 通过 |
| 650 | `P…660978` | 理论 / sr | 人之情知之者鲜；金须百炼然后精 | 通过 |
| 668–669 | `P…758706` / `P…775090` | 理论 / sr | 不可谓之学；记问之学未足为事业；王通没身；卷十四题。全书末 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- CP2 起五十六裁为四十二：L1704–1705
- 六十四裁为四十八：L1707
- 用以体为基存一：L1756–1757
- 阴策五十六：L1843–1844
- 大衍七七四十九：L1923
- 真数参两：L1995
- 四分至六十四：L2061–2062
- 阳上阴下尊卑：L2139
- 阴符韵法卷十三：L2448–2455
- 钦定/卷十四/邵雍撰：L2459–2463
- 观物外篇下篇题：L2467
- 阳尊神役物：L2529–2535
- 天行昼夜日行寒暑：L2629
- 月半盈半𧇊：L2685–2686
- 坤血艮肉十二配：L2932–2934
- 无思无为：L3063
- 金百炼：L3187–3189
- 记问之学 / 卷十四末：L3247–3252

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。本包 370 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了裁数/策数/真数/卷端层次/外篇下义理/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本，不计独立投票，不等同皇极算法已实现。观物外篇是数理与人事义理，不是占断。不得把 670 条 source-reviewed 写成已人工 verified。本包完成识典 SK1573 本文件段落集，不是皇极经世全帙，也不是产品交付。`remaining=0` 仅对本 edition 注解覆盖而言。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 包级 notes 套语 | CP2 370 条 notes[0] 均为「识典 SK1573 电子语义审读…不是影印校勘或人工 verified」 | 否定升 verified，不是空白话。不回改 |
| 观物外篇上白话后缀 | 约 158 条含「观物外篇上…」；理论条末句「…不是占断，也不等同皇极算法已实现。」 | 套语后缀，前半对照源文。不是空模板。不回改 |
| 观物外篇下白话后缀 | 约 209 条含「观物外篇下…」；同类否定占断后缀 | 同上。不回改 |
| 主题 gloss 批标签 | 「观物外篇下义理续论」「象数续论」「神气形体次第」「蓍卦体用与策数」等重复出现 | 批处理主题标签，前半仍对源。不回改 |
| 截断段 + gloss 粘连 | 约 23 条：电子切段末字未收束时，主题 gloss 直接粘在残句后（如 312「十二变而成真数参两…」、315「而成三百观物外篇上象数续论」、394「二十观物外篇上象数续论」、540「因物物类分属…」、541「有之天地日月…」） | 残片压缩/粘连。结构仍 source-reviewed。不回改；见 caveat |
| 索引 516「𧇊」 | 源有罕见字形；kind=待核实；白话保留原形 | 正确保留 unknown。不回改 |
| terms 偏泛 | 大量 terms 仅「观物外篇」 | 结构合法。抽核源均在外篇。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **截断段 gloss 粘连（约 23 条）**：如索引 312 / 315 / 394 / 403 / 410 / 456 / 483 / 491 / 537 / 540 / 541 / 548 / 549 / 554 / 572 / 599 / 602 / 603 / 608 / 611 / 624 / 631 / 663。电子行切残片后直接拼接主题标签，引用须回源行，不能只看白话末句主题词。
2. **索引 540**：源止于「因物」；白话成「因物物类分属与人为万物之灵」。邻段 541 起「而然也」才续完；接入时以 L2770–2784 为准。
3. **索引 516**：字形「𧇊」未定；保持待核实 / unknown，不升 verified。
4. **主题 gloss 批标签**：外篇下「义理续论 / 神气形体次第」等是包级分类词，不是逐句新义；抽规则须回源。
5. **`remaining=0`**：只表示识典 SK1573 本注解文件 paragraphId 已尽；`catalogComplete=false`、缺章 84、主本/DZ1040 不在本包。

## 未决（本岗不施工）

- 「𧇊」字形与截断段粘连白话：保持 unknown / 回源，不升 verified。
- 识典待校。670 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同皇极算法已实现。
- 主本 / DZ1040 不在本包范围；识典 0–669 审完不等于皇极经世全书完成。
- 本岗不回改注解、不重做 CP1、不碰 HY1442 / SK1603。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-174`。
