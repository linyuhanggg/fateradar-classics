# 盘面白话读法

这组内容供现有八术页面的解读栏使用，回答“盘上是什么、术语怎样理解、还要一起看什么”。它不是新增占断规则，也不靠扩张自动匹配数量体现覆盖率。

`chart-notes.json` 当前9条，覆盖八术。7条保留古籍或注本的引文行号；七政计算说明、小六壬通行取法说明另标 implementation_note。所有人工verified保持false。

导出：`python3 tools/export-reading-notes.py --output <产品工作树>/src/lib/engine/generated/reading-notes.json`。不传output时写入本仓dist/readings。导出前检查ID、术数和非空正文，古籍引文必须逐字对应所列行；CI同步执行。

古籍内容不得只剩引文：body写白话说明，source保存原文证据。不得用书中一个标签直接确定现实成败，不把注本或现代整理冒称古本原文。source核对仅证明电子文本对应，不替代影印校勘。

本轮与产品算法的配套说明见产品仓docs/READABLE_CORE_2026-09-07.md。产品主版本已扩展至八术，后续审读按实际页面字段补充，而不是批量填充泛泛断语。
