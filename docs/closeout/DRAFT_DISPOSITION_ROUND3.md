# Draft 注解去向 · Round 3（玉匣记图像占位）

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线：round2 后 draft 3013 / source-reviewed 59826

本轮只处理 `selection/yuqia-ji--shidian-NA09036.json` 中 notes 首条为「图像占位，不转写。」的 70 条。未动奇门 nlc-layouts，未清空 3013。

## 规则

- 电子本原文一律是 `〔此处为图像，未转文字；请对照本段原网页。〕`，`figureCount=1`，`source_status=reference-text`。
- 升 `source-reviewed` 核实的是「电子本此段无转写文字」，不是对照原图内容，不是择日算法，`verified` 保持 false。
- 残字、符咒、待核实、栏题残格仍为 draft。

## 数量

| 项 | 数量 |
|---|---|
| 本轮升 source-reviewed | **70** |
| 玉匣记该文件 draft | 267 → **197** |
| 全局 draft | 3013 → **2943** |
| 全局 source-reviewed | 59826 → **59896** |

抽核：

1. `yuqia-ji:shidian-NA09036:P7655682809017270318` — L869 图像占位
2. `yuqia-ji:shidian-NA09036:P7655682809017450542`
3. `yuqia-ji:shidian-NA09036:P7655682809084674099`
4. `yuqia-ji:shidian-NA09036:P7655682857407528986`（本批末条）

邻行可见有字正文（如「行年值太陰」），空图与有字段交错。

`python3 tools/validate-annotations.py` → 53 books, 62839 entries, 0 errors。
