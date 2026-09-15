# 古籍专项当前验收账 · 2026-09-15

结论：**尚未全部完成。** 本文件是当前进度。`CLASSICS-SPECIAL-ACCEPTANCE-20260913.md` 仍写 62,907 注释，只可作历史。

精确 SHA 随本提交。基线 `5449b299` 为 81,417 段；t125 后 83,351；本批 t134 后 **84,807**。

## 独立重算

源段 84,807，注释 84,807；未注释、悬空 ID、重复 ID 均 0。source-reviewed 72,565，draft 12,242。source-reviewed 不等于影印复核。

catalogComplete=false 仍 **10** 个：SK1610、DZ1040、SK1573、HY2301、7533808921945833506、SDZJ0174、SK1599、SK1619、SK1609、SDZJ0170。XYXZSBY 与 SK1588、SK1603、SK1615、SK1618 一样，只是识典网页目录取齐，**不是**古本全帙。

## 已合入

- t126 XYXZSBY《增刪卜易》缺章分批合入：24 章 / 319 新段已带 hash 绑定独立审核合入（163 source-reviewed / 156 draft）；staged 共 1,107 新段，其**余 788 段待注释审核，未合入**，`catalogComplete` 仍为 false。
- t127 XYXZSBY《增刪卜易》缺章继续分批合入：再合 32 章 / 212 新段（59 source-reviewed / 153 draft），累计 56 章 / 531 新段（本版 616→1,147 段）。已抓 125 章中仍余 69 章 / 576 段未合入；`catalogComplete` 仍 false。
- t128 XYXZSBY《增刪卜易》缺章继续分批合入：再合 10 章 / 164 新段（35 source-reviewed / 129 draft），累计 66 章 / 695 新段（本版 616→1,311 段）。已抓 125 章中仍余 59 章 / 412 段未合入；`catalogComplete` 仍 false。
- t129 XYXZSBY《增刪卜易》缺章继续分批合入：再合 17 章 / 84 新段（43 source-reviewed / 41 draft），累计 83 章 / 779 新段（本版 616→1,395 段）。已抓 125 章中仍余 42 章 / 328 段未合入；`catalogComplete` 仍 false。
- t130 XYXZSBY《增刪卜易》缺章继续分批合入：再合 19 章 / 160 新段（52 source-reviewed / 108 draft），累计 102 章 / 939 新段（本版 616→1,555 段）。已抓 125 章中仍余 23 章 / 168 段未合入；`catalogComplete` 仍 false。
- t131 XYXZSBY《增刪卜易》缺章继续分批合入：再合 16 章 / 114 新段（52 source-reviewed / 62 draft），累计 118 章 / 1,053 新段（本版 616→1,669 段）。已抓 125 章中仍余 7 章 / 54 段未合入（卡在 pack 380、680 两份未过独立审核）；`catalogComplete` 仍 false。
- t132 XYXZSBY《增刪卜易》缺章收束：再合 7 章 / 54 新段（12 source-reviewed / 42 draft），累计 125 章 / 1,107 新段（本版 616→1,723 段）。识典网页目录 `catalogComplete=true`，**不是**古本全帙；卜筮断语不入算法。
- t133 SDZJ0170《紫微斗数全书》缺章分批合入：4 章 / 150 新段（62 source-reviewed / 88 draft）。本版 1,070→1,220 段；识典网页仍余 146 章未合入，`catalogComplete` 仍 false。星曜吉凶是原书说法，不把本批写成算法已证实。
- t134 SDZJ0170《紫微斗数全书》缺章继续分批合入：3 章 / 199 新段（142 source-reviewed / 57 draft）。本版 1,220→1,419 段；仍余 143 章 / 715 段未合入，`catalogComplete` 仍 false。

- t122 SK1588：30→320，290 新注释（274 source-reviewed / 16 draft）。
- t123 SK1603：247→429，182 新注释（113 source-reviewed / 69 draft）。
- t124 SK1615：105→782，677 新注释（270 source-reviewed / 407 draft）。太乙不入算法。
- t125 SK1618：312→1097，785 新注释（357 source-reviewed / 428 draft）。择日不入算法。见 `evidence/t125-xingli-sk1618-785-review-20260915.json`。

## 未通过全库完成门槛

1. 10 个补充版本网页缺章未全部补采合入（已抓取并 staged；注释与独立审核未完成）。XYXZSBY 网页目录已取齐，仍非古本全帙。
2. 12,097 draft 逐条处置账已建，正文疑义与图文缺口未全部真实解决。
3. 0803.djvu 己/巳 已定为**版本异文**（本版作己、DZ1040 作巳，原字保留），见 `evidence/t127-huangji-0803-jisi-variant.json`；字形本身仍不能独立裁定。
4. 不以 CI 代替语义及影印验收。

不得为通过验收降低标准、批量改状态、删源或缩范围。
