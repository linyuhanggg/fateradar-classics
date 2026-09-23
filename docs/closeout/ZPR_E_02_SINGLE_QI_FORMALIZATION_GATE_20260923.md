# ZPR-E-02 单气正官入口正式交接门槛

**结论**：先前的[单气月支候选](./ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.md)已由 43 个真实日期盘验证为满足 4、不满足 7、信息不足 32。原始 `canggan` 多值事实不能直接承接该三态；现已由 Product 生产来源无关的[结构事实合同](./ZPR_E_02_SINGLE_QI_FORMALIZATION_GATE_20260923.json)，并在 Classics 来源提交 `b5fdef36dff2b9c3d82d97ac38a6fb26f0f83df5` 登记 `ZPR-P1-04`、词表和冲突门禁。规则作为 `provisional`、`verified=false` 进入 [V5 机器 handoff](./P1_BAZI_TOPIC_MANIFEST_20260923_V5.json)，产品导入仍待独立验收；`ZPR-E-02` 本体未升级。运行 `python3 tools/verify-zpr-e-02-formalization-gate.py` 可复算以下边界。

月支、月令、月藏的来源入口见《子平真诠》[L328](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L328)、[L419–421](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L419)和甲酉／丙子的例证[L468–470](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L468)。[L340–347](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L340)将先辨所用与逐柱作用分开。候选只判“原始月令正官入口”，不判正官主格、顺用成效、财印护官或救应。

| 真盘或投影 | 正确窄入口状态 | 直接把原始 `canggan` 写成普通 `any_of` 的问题 |
| --- | --- | --- |
| `caseP1_010_luck_gui_only`：甲日酉月，酉只藏辛 | 满足 | 可偶然得出满足，不能证明谓词充分。 |
| `cov2_bazi_3`：丁日子月，子只藏癸 | 不满足 | 只否定本窄入口，不能否定其它格局。 |
| 同一正例删月藏、删月令或月支 | 信息不足 | 必须按密集月柱缺键处理。 |
| 同一正例加月藏庚，或加第二个日干 | 信息不足 | `canggan` 为多值键，普通“见辛”仍会误报满足。 |
| `caseB`：己日寅月，寅藏甲丙戊且丙透 | 信息不足 | 三组支持分支的普通 `any_of` 会误报不满足。 |

结构键 `natal_month_single_qi_hidden_stem@{layer:本命,pillar:month}` 已由 Product 生产：只有月支与月令均唯一且相等、属当前共享盘定义的子／卯／酉，且完整月藏集合分别恰为癸／乙／辛时才发出对应**唯一藏干值**；其它情况不发键，表示本窄入口信息不足。该键不含日干或官格语义；逻辑输入是本命月支、月令和完整月藏，Product 的 `derivedFrom` 元数据为 `ganzhi.month`、`rows.藏干`。同作用域若出现不同值，Product 与 Classics 谓词均返回信息不足。午在当前 fixture 是丁己双藏，暂不纳入。

来源规则按[L146–149](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L146)的正官干配对建十个 `any_of` 分支：本命日干与这个结构键对应的唯一藏干相配为满足，已知单气月支但配对不符为不满足，键缺失或冲突为信息不足。必须包含十个日干分支；仅写三组能命中的甲酉、丙子、戊卯时，其他已知日干在多藏月上会被错判为不满足。正式验证逐盘比对 43 盘，并检验删键、日干冲突、月藏冲突、月令冲突、多藏月和异层同键污染；分布保持 4／7／32。

V5 以 V4 整文件 SHA 和 13 条旧规则对象为历史基线，只向 `overview` 增加这条中性入口。共享 fixture 两仓字节一致，SHA-256 为 `3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc`。产品导入后需再检查 `Fact → RuleEvaluation → TopicEvaluation` 及初始／选择／取消／移动端行为。全过程保持 `ZPR-E-02` 的 `rescue=unimplemented`、`verified=false`。完整正官格和作用仍依[单格门槛](./ZPR_E_02_ZHENGGUAN_CELL_GATE_20260923.md)另行裁决。
