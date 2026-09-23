# ZPR-P1-04：单气月支正官原始入口交接

`ZPR-P1-04` 已在 Classics 作为 `provisional`、`verified=false` 的来源结构规则登记，供 Product 独立审核后导入。它只归 `overview`、只适用于本命：完整月支／月令为子、卯、酉单气支，唯一藏干与本命日干所配正官干相同时，确认**原始月令正官入口**。它不裁正官主格、兼格、顺用作用、救应或吉凶，也不改变原 `ZPR-E-02` 的 `rescue=unimplemented`、`verified=false`。

机器交接是 [V5 manifest](./P1_BAZI_TOPIC_MANIFEST_20260923_V5.json)。`python3 tools/verify-p1-bazi-14-handoff.py --compare-product-fixture` 会重新生成并逐字节比较、核对前 13 条规则对象和 V4 整文件 SHA、导出规则、来源行号与共享盘。`python3 tools/verify-zpr-e-02-formalization-gate.py` 复核所有 43 盘的三态、原始 `canggan` 多值误判和 Product 结构键；`python3 tools/verify-zpr-e-02-zhengguan-cell-gate.py` 继续证明完整正官格作用尚缺。

| 锁定对象 | SHA-256 或提交 |
| --- | --- |
| Classics 来源修订 | `b5fdef36dff2b9c3d82d97ac38a6fb26f0f83df5` |
| V4 整文件历史基线，13 条 | `4429116dfd1aef1287406594d8fc80aa41e3fa1eda71235403ed1fcb94c76fda` |
| V5 manifest，14 条 | `7ea7b0214f1150c522273133febf3575f8821bc5fddd7c4d2cca1e3b2a36d802` |
| 两仓字节相同的 43 盘 fixture | `3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc` |
| Classics 八字规则导出 | `489073b00238bbb035e649c54878e7bf15d698b590244b1bc1bce96cddbab1d8` |
| 来源 YAML | `50124bafe9a9022076e6e0abd09c60c63876e93a297297478896c40a1587240b` |
| 来源提交中的事实词表 | `76ea0a3b0a87417987caa16c548a923c72487c20af55c9801d335135f352dbea` |
| 来源提交中的谓词求值器 | `63b624ef89835759e6caf2aa0ee1120934143ac6954a43e560553ac6319d2893` |

Product 已在 `buildBazi` 的本命事实中生产来源无关结构键 `natal_month_single_qi_hidden_stem@{layer:本命,pillar:month}`，值域为十天干，当前只在月支与月令一致、月藏完整且单气为子癸／卯乙／酉辛时发出；其它情况缺键。来源规则再以本命日干和此结构键配十个正官干分支。两个求值器均须把新键视为同 scope 单值、密集柱位事实：缺本命键或仅异层同键为信息不足，冲突值亦为信息不足。旧 43 盘按新合同得到满足 4、不满足 7、信息不足 32；例盘 `caseP1_010_luck_gui_only` 为满足、`cov2_bazi_3` 为不满足、`caseB` 多藏月为信息不足。删键、冲突及异层污染投影只作边界验证，不能冒充新的真实负例。

主 `quote/anchor` 为《子平真诠》[L328](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L328)的“月令配日干”。十干官煞分类和单气界另依 [L146–149](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L146)、[L419](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L419)，甲酉／丙子例证见 [L468](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L468)、[L470](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L470)。V5 规则行的 `supportingSources` 逐字记录这些附锚；当前 `dist/rules/bazi.json` 只有主锚，Product 若只展示生成规则的 `source.quote` 会遗漏本条推导所需来源。导入后须让证据展示并列附锚，或明确显示来源限制，不能把 L328 单句称作十干和单气的全部出处。

V5 只向 `overview.ruleIds` 与 `overview.requiredFactKeys` 增加新条目，前 13 条规则对象和其它主题归属逐对象不变；`semanticContractStatus=pending`、所有 `verification.verified=false`。下一道来源门槛仍是多藏月主兼格取舍和正官财生／印护、冲伤煞混、刑冲破害的作用与救应合同，[完整正官一格审计](./ZPR_E_02_ZHENGGUAN_CELL_GATE_20260923.md)尚未解除。
