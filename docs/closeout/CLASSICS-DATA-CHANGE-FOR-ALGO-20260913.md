# 给算法任务的数据变更说明（古籍专项滚交）

- 仓：`https://github.com/linyuhanggg/fateradar-classics`
- **精确版本**：本滚交合入 `main` 后的 SHA（父提交 `d01ea097e332d691ea3f48967fbf30e997ca9c07`；以本提交为准）
- 本专项 **不改** `references/executable/**`、**不改** `references/cases/source-cases.json`
- 注解：`source-reviewed` 60,013（t23 后）→ 60,108（t24–t27）；`verified` 全 false
- t24–t27 所升均为**记录性锚点**（盘图残行、识典残格、短残句），**不得**当课体/庙旺/择日/相法判断输入
- 22 条 `implementation-gap` 与 8 条 `evidence-undecided` 仍在 `references/executable` 的 `named_gaps`；实现属算法任务
- 产品 pin 由算法/Web 任务改；本专项只提供上述兼容性边界

分批细目：`CLASSICS-DATA-CHANGE-T24-FOR-ALGO.md` … `T27`。
