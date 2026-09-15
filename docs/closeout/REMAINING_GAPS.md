# 真实未决清单（当前 HEAD，不是 2026-09-12 快照）

日期：2026-09-15  
本文件取代 `docs/closeout/REMAINING_GAPS.md` 旧稿（旧稿写 draft 2905、SHA `3191806`/`e083dcf`，**不是当前进度**）。  
`CLASSICS-SPECIAL-ACCEPTANCE-20260913.md` 仍列 62,907 注释，也只是历史快照。

精确 SHA 随本提交。当前重算：源段与注释 81,707；未注释、重复、悬空 ID 均 0；source-reviewed 71,205；draft 10,502。

## 必须保留为未完成

| 项 | 数量/状态 | 为何不能标完成 |
|---|---|---|
| catalogComplete=false | **14** 个识典补充版本 | 网页缺章尚未全部重导入并注释审核。已网页取齐的 SK1588 仍不是古本全帙。 |
| draft | **10,502** | 分类账已建（可核实正文 / 目录元数据 / 图文缺失 / 版本异文 / 原件仍不可辨），**分类不是结案**。 |
| 0803.djvu 己/巳 | 未决 | 本轮 DSH 原生 read_image 仍 AMBIGUOUS_GLYPH_RETAIN_DRAFT；不得按六十甲子序改字。 |
| source-reviewed | 71,205 | 不等于影印精校。 |
| 产品 pin | 未改 | 古籍 main 合入不代表产品版本已更新。 |

## 已网页取齐、仍非全帙

- SK1588《葬书》识典：dest 320，catalogComplete=true 仅为识典网站目录段数一致。

## 已抓缺章、尚未合入正式库

SK1603、SK1573、SK1615、SK1618、HY2301、XYXZSBY、SDZJ0170、DZ1040 等缺章 JSON 在 `.local/dsh-handoff-20260914/work/`，候选与审核未全部 ACCEPT，不得提前改 catalogComplete。

## 不升、不杜撰

- 不凭口诀、排列规律、算法补原字。
- 不把 draft 批量改 source-reviewed。
- 不删源、不缩分母。
