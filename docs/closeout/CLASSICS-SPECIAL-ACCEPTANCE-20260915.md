# 古籍专项当前验收账 · 2026-09-15

结论：**尚未全部完成。** 本文件是当前进度。`CLASSICS-SPECIAL-ACCEPTANCE-20260913.md` 仍写 62,907 注释，只可作历史。

精确 SHA 随本提交。基线 `5449b299` 为 81,417 段；t125 后 83,351；本批 t126 后 **83,670**。

## 独立重算

源段 83,670，注释 83,670；未注释、悬空 ID、重复 ID 均 0。source-reviewed 72,108，draft 11,562。source-reviewed 不等于影印复核。

catalogComplete=false 仍 11 个：SK1610、DZ1040、SK1573、XYXZSBY、HY2301、7533808921945833506、SDZJ0174、SK1599、SK1619、SK1609、SDZJ0170。SK1588、SK1603、SK1615、SK1618 网页目录已取齐，不是古本全帙。

## 已合入

- t126 XYXZSBY《增刪卜易》缺章分批合入：24 章 / 319 新段已带 hash 绑定独立审核合入（163 source-reviewed / 156 draft）；staged 共 1,107 新段，其**余 788 段待注释审核，未合入**，`catalogComplete` 仍为 false。

- t122 SK1588：30→320，290 新注释（274 source-reviewed / 16 draft）。
- t123 SK1603：247→429，182 新注释（113 source-reviewed / 69 draft）。
- t124 SK1615：105→782，677 新注释（270 source-reviewed / 407 draft）。太乙不入算法。
- t125 SK1618：312→1097，785 新注释（357 source-reviewed / 428 draft）。择日不入算法。见 `evidence/t125-xingli-sk1618-785-review-20260915.json`。

## 未通过全库完成门槛

1. 11 个补充版本网页缺章未全部补采合入（已全部抓取并 staged 共 36,347 段，注释与独立审核未完成）。
2. 11,562 draft 逐条处置账已建，正文疑义与图文缺口未全部真实解决。
3. 0803.djvu 己/巳 已定为**版本异文**（本版作己、DZ1040 作巳，原字保留），见 `evidence/t127-huangji-0803-jisi-variant.json`；字形本身仍不能独立裁定。
4. 不以 CI 代替语义及影印验收。

不得为通过验收降低标准、批量改状态、删源或缩范围。
