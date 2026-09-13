# 给算法任务的数据变更说明（古籍专项滚交）

- 仓：`https://github.com/linyuhanggg/fateradar-classics`
- **精确版本**：以本批合入 `main` 的 SHA 为准（父提交 `a4784e2cf1bc2a907a3e81f7adc8b5730d12799d`）
- 本批 **不改** `references/executable/**`、**不改** `references/cases/source-cases.json`
- 奇门：`nlc-layouts.md` 增 PDF 308–311 阴七局逐时条文；`nlc-layout-page-reviews.json` 增四页 `partial`。消费方不得把短列（甲寅／庚申）或 311 仅三时支当成缺页错误。
- 注解：`source-reviewed` 60,013（t23 后）→ 60,108（t24–t27）；`verified` 全 false
- t24–t27 所升均为**记录性锚点**（盘图残行、识典残格、短残句），**不得**当课体/庙旺/择日/相法判断输入
- 22 条 `implementation-gap` 与 8 条 `evidence-undecided` 仍在 `references/executable` 的 `named_gaps`；实现属算法任务
- 产品 pin 由算法/Web 任务改；本专项只提供上述兼容性边界

分批细目：`CLASSICS-DATA-CHANGE-T24-FOR-ALGO.md` … `T27`。
