# 《子平真诠》甲辰透戊入口的顺用候选分类：P1 来源合同

## 可交付结论

`ZPR-P1-03` 只为 `ZPR-P1-01` 已识别的**甲日、辰月、月藏戊且本命年／月／时干透戊**这一偏财取用入口，增加一个来源分类：`candidate_output={entryId:ZPR-P1-01, entry:甲辰月透戊偏财, category:财, direction:顺用, status:候选, scope:{layer:本命}, emitOn:满足}`。它是附在 `ZPR-P1-03` **RuleEvaluation** 上的来源输出元数据，不是 FactKey；不能把它反馈为本条 `applicable_to` 的输入，也不是 `ZPR-E-02` 整条的满足结论。它比 `ZPR-P1-01` 多了“该入口属于财善顺用的候选类”一项信息；适用谓词沿用 P1-01，以保证不会从任意柱上的偏财十神或 `geju` 名称反推入口。

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

消费时以 `ruleId + candidateOutput.entryId` 为记录身份，`scope.layer=本命`；**只有**该条 RuleEvaluation 为“满足”才附候选分类。不满足保留反例状态但无方向输出，信息不足也无方向输出。未来其它取用入口应有独立入口 ID 与分类规则，多个候选并存须保留为多条记录，不能合并成单个 `geju.mode`。同一入口若出现相冲的候选方向，应进入待核而非任选一条。本合同当前只交付戊透偏财这一枚入口，不宣称癸透或会支入口的分类已经实现。

## 未采纳的上层语义与版本边界

“顺用候选”还不是财格已成、实际财喜食神相生／生官护财、护卫救应有效、扶抑或调候喜行、财富结果。月令多入口取舍、逐干逐支作用、位置力度、冲合制化、喜忌及反证覆盖均未由这四枚输入事实解决。[`ZPR-E-02` 边界审计](./ZPR_E_02_SEMANTIC_BOUNDARY_20260923.md)继续适用；`references/executable/ziping-zhenquan.json` 的 `satisfy_when`、`rescue=unimplemented`、`verified=false` 与 `applicable_to` 未改，不能因本条为满足而给 E-02 输出“满足”。

机读定义在 [`rules.yaml`](../../references/books/bazi/ziping-zhenquan/rules.yaml) 的 `ZPR-P1-03`，[`export-rules.py`](../../tools/export-rules.py) 将其保留为导出规则的 `candidateOutput` 和三枚 `candidateSources`（L328 分类、L544 入口、L548 并用）。可审查的[独立 P1 handoff 候选 JSON](./ZPR_P1_03_HANDOFF_CANDIDATE_20260923.json)由 [`generate-zpr-p1-03-handoff-candidate.py`](../../tools/generate-zpr-p1-03-handoff-candidate.py)生成，另列 L328／L544／L548 来源链；提议只入 `overview` 来源结构证据，`reviewStatus=proposed_not_importable`。当前产品 importer 固定接收原 10 条，不会自动纳入本候选。未登记新的 FactKey，未改正式八字 P1 manifest、`semanticContractStatus=pending`、ZPR-E-02 或产品仓。源文 SHA-256 `5d0e11098aa076468da4bd805159550c178c1ee31d325e30be5f042d9051a053`；规则 YAML `d898cda719edb5a29c1f40c449a9295eb2f9314786fa19882816039a867f2c66`；导出器 `47e8305fc90803c4f3657b885818f0bc7bc80108d52fdf019d892ea8af7ce9bb`；共享 fixture `6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb`；handoff 候选 JSON `69f29c68458e1c612fc1d8890ef13141242ad389a087cebdfe81770cd0b8d967`。候选 JSON 还记录求值器与谓词语言文件 SHA；求值器当前已由独立本地提交 `08a37c3` 固定，交接需核对工作树与该提交的实际字节一致。P1-03 初版来源规则提交为 `4eb4478d453f5b4b6a38af99b347f69bbf9edc36`；产品若选择导入，须另钉包含本轮导出合同的不可变提交并核对指纹，不以当前 `main` 或旧 Bazi manifest 的 `CLASSICS_REV=01eaf71` 偷代本条来源。

验收命令：`python3 tools/verify-zpr-p1-03-direction-candidate.py`、`python3 tools/generate-zpr-p1-03-handoff-candidate.py --output .local/staging/zpr-p1-03-handoff-recheck.json` 并与交接候选逐字比较、`python3 tools/validate-rules.py --book bazi/ziping-zhenquan --json`。第一项核 L328／L544／L548 证据链、导出字段、四个真实日期样盘与缺项投影，并确认 E-02 仍未验收；最后一项只校验规则格式与电子来源锚点，不证明预测有效性或人工影印全书校勘。
