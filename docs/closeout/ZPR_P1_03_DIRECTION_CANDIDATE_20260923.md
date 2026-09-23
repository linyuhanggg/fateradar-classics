# 《子平真诠》甲辰透戊入口的顺用候选分类：P1 来源合同

## 可交付结论

`ZPR-P1-03` 只为 `ZPR-P1-01` 已识别的**甲日、辰月、月藏戊且本命年／月／时干透戊**这一偏财取用入口，增加一个来源分类：`candidate_output={entry:甲辰月透戊偏财, category:财, direction:顺用, status:候选}`。这是可供产品另行建正式 FactKey 的机读候选输出，**不是**当前词表中可直接消费的 Fact，也不是 `ZPR-E-02` 整条的满足结论。它比 `ZPR-P1-01` 多了“该入口属于财善顺用的候选类”一项信息；适用谓词沿用 P1-01，以保证不会从任意柱上的偏财十神或 `geju` 名称反推入口。

该分类把[原文 L544](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L544)“甲生辰月，透戊则用偏财”与[原文 L328](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L328)“财官印食……善而顺用”相接，属于**有据的跨句推断**；L544 本身没有断言“已经顺用”。[L548](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L548)还明说兼透、透与会可并用，因此同盘其它入口不能被这枚标签覆盖。P1-01 对 L544–548 的国图影印本 PDF 第 41 页／原印 32 页已有目视核对；本条新增的 L328 分类目前按电子全文逐字锚定，未把整部书或规则升为 `verified=true`。

## 三态、缺项与反证范围

| 样盘或投影 | 本条判定 | 允许输出的事实边界 |
| --- | --- | --- |
| `caseP1_ZPR_01_wu_only`：1988-04-09 03:20 上海，戊辰／丙辰／甲午／丙寅 | 满足 | 戊透偏财入口附“财善顺用”**候选分类**；不称唯一用神或成格。 |
| `caseP1_ZPR_01_wu_gui_both`：1988-04-09 17:20 上海，戊癸兼透 | 满足 | 只给戊透偏财入口分类；癸透正印入口可并存，不能单值覆盖。 |
| `caseP1_ZPR_01_no_wu`：1981-04-06 03:20 上海，辛酉／壬辰／甲寅／丙寅 | 不满足 | 完整本命年／月／时干均无戊，只否定**这条戊透入口的候选分类**，不否定其它入口或 `ZPR-E-02`。 |
| `caseP1_ZPR_02_shen_zi`：1996-04-17 15:20 上海，申子辰会支输入而无戊透 | 不满足 | 会支水印入口不能冒充戊透财入口。 |
| 从满足样盘剔除 `gan@本命/year` 或 `canggan@本命/month` | 信息不足 | 缺年干不能排除年干戊；缺月藏干不能证明戊确属月令。其它柱位有同名键也不能代填。 |
| 从不满足样盘剔除 `gan@本命/year` | 信息不足 | 不能把缺少年干当成“年干不是戊”；月、时干非戊不足以作完整反证。 |

谓词需要 `rizhu=甲@本命/day`、`yueling=辰@本命/month`、`canggan=戊@本命/month`，以及本命年／月／时干中至少一枚 `gan=戊`。求值器对天干、藏干执行**逐柱密集事实**缺位检查。日干不是甲、月令不是辰、三处本命干明确均无戊时，本条可为“不满足”；它从不把“不满足”解释成逆用成立或古籍教义错误。移除正例里的 `geju` 和 `shishen` 名称事实仍为满足，说明本合同靠柱位结构而非产品已有的格局名称。

## 未采纳的上层语义与版本边界

“顺用候选”还不是财格已成、实际财喜食神相生／生官护财、护卫救应有效、扶抑或调候喜行、财富结果。月令多入口取舍、逐干逐支作用、位置力度、冲合制化、喜忌及反证覆盖均未由这四枚输入事实解决。[`ZPR-E-02` 边界审计](./ZPR_E_02_SEMANTIC_BOUNDARY_20260923.md)继续适用；`references/executable/ziping-zhenquan.json` 的 `satisfy_when`、`rescue=unimplemented`、`verified=false` 与 `applicable_to` 未改，不能因本条为满足而给 E-02 输出“满足”。

机读定义在 [`rules.yaml`](../../references/books/bazi/ziping-zhenquan/rules.yaml) 的 `ZPR-P1-03`，`candidate_output` 仅是本条源定义的待映射输出声明；尚未登记正式 `FactKey`，未改八字 P1 manifest 或 `semanticContractStatus=pending`，未改产品仓或发布。当前源文 SHA-256 `5d0e11098aa076468da4bd805159550c178c1ee31d325e30be5f042d9051a053`，本条源文件 SHA-256 `5cdb9504ccd482a939feae4339a1c2f448fdcbbed07ff5a55780e4b070f56ec1`，共享 fixture SHA-256 `6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb`。本地基准 Classics `a611764b49f9a9f4f5872c82e1f21515fdcf3a2c`；产品若选择导入，须另钉包含本规则的**不可变提交**并核对上述文件指纹，不以当前 `main` 或旧 Bazi manifest 的 `CLASSICS_REV=01eaf71` 偷代本条来源。

验收命令：`python3 tools/verify-zpr-p1-03-direction-candidate.py`、`python3 tools/validate-rules.py --book bazi/ziping-zhenquan --json`。前者核 L328／L544／L548 证据链、四个真实日期样盘与缺项投影，并确认 E-02 仍未验收；后者只校验规则格式与电子来源锚点，不证明预测有效性或人工影印全书校勘。
