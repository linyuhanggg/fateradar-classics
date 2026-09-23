# SANMINGTONGH-011 分类作用合同核对（2026-09-23）

**结论：完整 011 仍不能交接。** 本仓已有 [011A 甲子／甲子字面入口](SANMINGTONGH_011A_12_RULE_HANDOFF_20260923.md)，但原 011 的“独羊刃七煞为凶，财官印绶亦吉”缺分类取值、并存优先级、得力与救应的可执行条件。本次把[六盘年源范围候选](../../tools/reports/p1-bazi-20260922/sanming-011-classification-scope-candidate.json)固定成机器可查的草案，运行 `python3 tools/verify-sanming-011-classification-scope.py` 检查原文锚、逐柱来源和所选年事实；草案 `status=unadopted_draft`、`factKeyStatus=not_registered_do_not_emit`，不进入 `fact-vocab.json`、正式规则、manifest 或产品输出。

## 可交接的原始输入边界

产品侧**目前只需维持**已有 `suiyun_binglin`、`suiyun_same_zhi`、`dayun_gan_zhi`、`liunian_gan_zhi`、逐柱 `shishen`／`shensha` 的原始事实与 `derivedFrom`。求值前按 `scope.layer=流年, scope.year=selectedYear` 筛选流年事实，按相同年份筛选**有效**大运；本命候选分别保留 `scope.pillar=year/month/day/time`、透干与藏干来源。无年份的大运十神列表包含非当前大运，不能当本年输入。2031 年样盘本命没有七杀原始标签，却在有效大运和流年天干均见七杀；1960 年样盘本命有七杀原始标签，而有效岁运两干均为正官。因此单值 `natal_binglin_class` 即使可填，也不能代表 011 的分类。

若后续要新增专属 FactKey，[草案](../../tools/reports/p1-bazi-20260922/sanming-011-classification-scope-candidate.json)给出 `sanming_011_classification_evidence` 的**未注册值域**：来源段落、所选年形态、本命／有效大运／流年分层多候选、逐候选原始标签三态、逐柱 `derivedFrom` 和仍未裁决的作用。这里的“原始标签未见”只说明该 fixture 中未出现这个标签，**不是**“此类在命局不成立”，也不是作用反例。不得把它塞回一个 `羊刃/七杀/财官印绶/信息不足` 的单值枚举。

## 来源允许的条件顺序与不能设定的优先级

- [《论太岁》L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)把甲子岁／甲子运称并临，接上刃杀与财官印绶的相反方向，却没有说类别取本命、岁运透干、藏干还是格局。**两类原始标签同现时没有覆写顺序。** `caseFlowYearBinglin@1993` 的本命藏干就同时有七杀、财、官、印。
- [《论阳刃》L3468–3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3468)明确区分“命元有煞刃、岁运又逢”与“命有刃有印无煞、岁运逢煞”，方向相反；月令确证合财官印绶或他格时又要求按他格断。这是**有前提的来源顺序**，并非“有印覆盖七杀”或“七杀覆盖正官”的通用优先级。当前缺各前提的正式三态算法，不能执行这些分支。
- [《论阳刃》L3459](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3459)的甲日乙卯时已由两份卷五影印确认原字，[《六甲日丁卯时断》L4959–4962](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L4959)却明写甲日丁卯时，并有“七煞合刃行财官印绶大贵”的条件。按日上起时甲日卯时只能是丁卯；不能为前者伪造真实正例或把后者自动改造成 L1084 的作用例。影印页与逐字结论见[来源修正记录](SANMINGTONGH_011_SOURCE_AND_TRISTATE_FIX_20260923.md)。
- 本书[《论羊刃》L1623–1635](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1623)的刃起法与子平“五阴干无刃”并列；本命通用 `shensha=羊刃` 不能直接代入 L1084 的“独羊刃”。[《金玉赋》L10158](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L10158)又要求并临损用神才断祸，[《消息赋》徐注 L8893](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8893)的同支异干吉会要求官印财帛有用，均缺可执行的“有用／损用”判据。

## 六盘年验收边界

[核对器](../../tools/verify-sanming-011-classification-scope.py)锁定六盘年的同干支形态三态：1993、2031、1960 年为“是”，2019、2026 年为“否”，2100 年缺有效大运为“信息不足”。2019 年丁亥运／己亥岁还单独显示同支“是”，证明同干支的“否”不能否定另一段来源。1993 年的本命七杀和财官印绶同现、2031 年本命／岁运标签分歧、1960 年相反的分歧也逐项断言。**六盘都没有来源支持的 011 作用正例、反例或未知三态标注，作用全部“未裁决”。** 结构形态的正反未知不能充作作用样盘。

### 最小反例与阻塞决策

[机器草案](../../tools/reports/p1-bazi-20260922/sanming-011-classification-scope-candidate.json)的 `scopeAmbiguityWitnesses` 将三盘的**本命原始组**与**所选岁运天干原始组**分开，并由核对器从共享 fixture 重新计算。这些都不是有效类别或吉凶判定：

| 真盘年 | 本命原始组 | 所选岁运天干原始组 | 单值政策的损失 |
| --- | --- | --- | --- |
| `caseFlowYearBinglin@1993` | 七杀、财官印绶 | 财官印绶 | 本命同层两组并存，任取其一会抹掉另一组。 |
| `caseP1_011_seven_killer@2031` | 财官印绶 | 七杀 | 只取本命与只取岁运导向相反。 |
| `caseP1_011_proper_officer@1960` | 七杀、财官印绶 | 财官印绶 | 只取岁运会漏掉本命七杀。 |

解除阻断只需先裁定三个相互依赖的问题，草案以 `minimumBlockingDecisions` 固定：① 分别给 L1084、L3459–3471、L4959–4962 的刃起法和有效分类层级，说明本命透干、藏干、格局与所选大运、流年哪些入组；② 给同层多值、跨层相反组及 L3471“月令合他格”的条件优先级，任何未知前提保留未知；③ 给得力、喜忌、制化救应、损用神的可复核输入，并为每个作用分支提供真实日期盘、选定年、有效大运及逐柱出处的作用正例、反例、未知例。当前六盘只满足**形态**的正反未知，不能填补第三项；L3459 的不可达甲日乙卯时只能作来源冲突，不能列为真盘。

每项的原文与盘例均在草案中用 `sourceAnchors`、`fixtureWitnesses` 明列，核对器逐字检查锚点并重算盘例：① 对照[L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)、[L1624／1635](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1624)、[L3459](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3459)、[L4959／4962](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L4959)及上表三盘；② 对照[L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)、[L3468／3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3468)及上表三盘；③ 对照[L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)、[L3468／3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3468)、[L8893](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8893)、[L10158](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L10158)及六盘年。第三项盘例只能证明**目前缺作用裁决**，不能把“未裁决”冒充已验证的语义 unknown 真盘。

在这些裁决和样盘交齐前，011 继续 `applicable_to=[]`、`verified=false`，产品对其作用保持 unknown；011A 的字面入口不能证明原 011 完成。
