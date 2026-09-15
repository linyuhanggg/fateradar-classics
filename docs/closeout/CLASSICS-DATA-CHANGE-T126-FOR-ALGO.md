# 消费方数据版本 · t126 XYXZSBY 缺章分批合入

当前古籍 main 随本提交更新。父提交 t125 `b54edb1ad15a15c8c430a9c7e37276abbca5f49c`。

## 本批

XYXZSBY《增刪卜易》识典缺章**分批合入**：本轮合入 24 章 / **319** 新源段
（本版 616→935 段）。新注释 319（163 source-reviewed / 156 draft），
每条均绑定独立审核者（judge B）的 ACCEPT 与候选文件 sha256。

**未合入**：已抓取的 125 章中仍有 **101 章 / 788 段**未合入，因为其注释与独立审核未完成。
故本版 `catalogComplete` 仍为 **false**。

分批合入规则：某章仅当其**全部**新段都已有 hash 绑定的 ACCEPT 注释时才合入；
正式源段不得先于注释与审核进入仓库。

## 本批后全库（validate-annotations / 同 HEAD 重算）

- 源段/注释 83,670
- 未注释、重复、悬空 ID 0
- source-reviewed 72,108；draft 11,562
- catalogComplete=false **11**

## 其他同批更新

- `DRAFT_DISPOSITION_LEDGER.json`：11,562 条 draft 逐条处置账（源 ID、证据路径、分类依据）。
- `EDITION_COVERAGE.md/.json`：11 个不完整版本的"应有章节—已采章节—缺失章节—来源证据"对照。
- `evidence/t127-huangji-0803-jisi-variant.json`：0803.djvu「經月之□六」定为**版本异文**
  （本版四庫 0803 册作「己」，DZ1040 作「巳」），照录本版原字、异文并存。

## 不升、不杜撰

不凭口诀、排列规律、算法补原字。不把 draft 批量改 source-reviewed。
未完成注释与审核的缺章不得合入。`verified` 仍为 false。
`source-reviewed` 不等于影印精校。
