# 消费方数据版本 · t133 SDZJ0170 缺章分批合入

当前古籍 main 随本提交更新。父提交 t132 `9f3b00f51609b65b17bb47ba63b303ccf23b9bc6`。

## 本批

SDZJ0170《新鋟希夷陈先生紫微斗数全书》识典缺章分批合入：本轮合入 **4 章 / 150 新源段**
（本版 1,070→1,220 段）。新注释 150（62 source-reviewed / 88 draft），
每条均绑定独立审核者（judge B）的 ACCEPT 与候选文件 sha256。

已抓 150 章中仍余 **146 章 / 914 段**未合入，`catalogComplete` 仍为 **false**。
星曜吉凶是原书说法，不作为已证实算法。网页取齐不等于古本全帙。

合入时丢弃了 4 条候选里的 `subsections`（其 startLine/endLine 相对 staged 文本，
合入后会越出父段行号，validate-annotations 报错）。

## 本批后全库（validate-annotations / 同 HEAD 重算）

- 源段/注释 84,608
- 未注释、重复、悬空 ID 0
- source-reviewed 72,423；draft 12,185
- catalogComplete=false **10**

## 不升、不杜撰

不凭口诀、排列规律、算法补原字或补星曜。不把 draft 批量改 source-reviewed。
`verified` 仍为 false。
