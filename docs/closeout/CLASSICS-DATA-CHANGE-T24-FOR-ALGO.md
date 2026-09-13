# 给算法任务的数据变更说明（t24 / 古籍专项）

- 仓：`linyuhanggg/fateradar-classics`
- 分支：`dsh/full-library-classics`（合 main 后以远端 SHA 为准）
- 本批不改 executable 规则 JSON，不改 `source-cases.json`。
- 注解：`source-reviewed` 60,013 → 60,021（+8 条大六壬盘图残行记录性锚点）；`verified` 全 false。
- 新增锚点 ID：`daliuren-daquan:L9463-L9463`、`L9469`、`L9479`、`L9495`、`L9503`、`L9505`、`L9521`、`L9529`（均 `:Lxxxx-Lxxxx` 全写见证据文件）。
- 兼容性：产品若只消费 `source-reviewed` 引文，这 8 条现在可引用，但**不得**当课体判断或吉凶来源；残行信息不足。
- 未决仍阻塞实现的条目（本批只补登记、未立新规则）：乙酉三奇取亥、轩盖三传序、柔日昴星亥/寅初传冲突、甲子 vs 四课丁、已亥/己亥、矿决等。详见各条 `notes` 中 `t24 未决登记`。
