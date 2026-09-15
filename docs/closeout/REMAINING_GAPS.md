# 真实未决清单（当前 HEAD，不是 2026-09-12 快照）

日期：2026-09-15  
旧稿 draft 2905、SHA `3191806`/`e083dcf` **不是当前进度**。`CLASSICS-SPECIAL-ACCEPTANCE-20260913.md` 仍列 62,907 注释，只是历史快照。

精确 SHA 随本提交。当前重算：源段与注释 82,566；未注释、重复、悬空 ID 均 0；source-reviewed 71,588；draft 10,978。

## 必须保留为未完成

| 项 | 数量/状态 | 为何不能标完成 |
|---|---|---|
| catalogComplete=false | **12** 个识典补充版本 | 网页缺章尚未全部重导入并注释审核。已网页取齐的 SK1588、SK1603、SK1615 仍不是古本全帙。 |
| draft | **10,978** | 分类账已建，**分类不是结案**。 |
| 0803.djvu 己/巳 | 未决 | 原生 read_image 仍 AMBIGUOUS_GLYPH_RETAIN_DRAFT。 |
| source-reviewed | 71,588 | 不等于影印精校。 |
| 产品 pin | 未改 | 古籍 main 合入不代表产品版本已更新。 |

## 已网页取齐、仍非全帙

- SK1588《葬书》识典 dest 320
- SK1603《星命溯源》识典 dest 429
- SK1615《太乙金镜式经》识典 dest 782

## 已抓缺章、尚未合入正式库

SK1573、SK1618、HY2301、XYXZSBY、SDZJ0170、DZ1040、SK1609 等缺章 JSON 在 `.local/dsh-handoff-20260914/work/`。SK1610 有 13 章空壳 SSR；SK1599 已抓齐未注释。不得提前改 catalogComplete。

## 不升、不杜撰

- 不凭口诀、排列规律、算法补原字。
- 不把 draft 批量改 source-reviewed。
- 不删源、不缩分母。
