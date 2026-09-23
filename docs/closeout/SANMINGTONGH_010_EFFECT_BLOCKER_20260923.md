# 《三命通会》010 完整救应与作用：来源冲突及定值缺口

裁决：`SANMINGTONGH-010` 的完整作用目前**不能**交付为 `rescue_condition` 或 `transit_effect_semantics`。L1081 的甲日戊岁字面入口已由独立 010A 交接；[L1082 的两项条件式阶梯](SANMINGTONGH_010_CONDITIONAL_EFFECT_CONTRACT_20260923.md)可在**外部已独立定值**时执行，但十个真实排盘均未给“有效制伏”或“戊癸有情”定值。机器可读的[审计及待决接口](SANMINGTONGH_010_EFFECT_AUDIT_20260923.json)由 [`verify-sanming-010-effect-audit.py`](../../tools/verify-sanming-010-effect-audit.py)锁定。原 010 的 `applicable_to=[]`、`verified=false` 保持。

## 源文并未给出一个可直接计算的救应布尔值

| 层次 | 来源证据 | 当前不能越过的边界 |
|---|---|---|
| 入口 | [《论太岁》L1081](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1081)举“甲日尅戊年”。 | 只是一个具体例子，不能推广到所有日干克岁干，也不是凶事发生。 |
| “有救” | [L1082](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1082)连写四柱庚申、有效大运与“将甲木制伏纯粹不能克戊土”。两份数字整理本 [HY1521 L4914–4918](../../sources/normalized/shidianguji/HY1521/text.md#L4914)、[SK1610 L5177–5180](../../sources/normalized/shidianguji/SK1610/text.md#L5177)虽然加了逗点，仍未裁定庚申出现本身是否充分，或两条路径都须证成“不能克戊”的有效作用。 | 同书[《论偏官》L3087](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3087)另举甲寅见庚申，在子辰印局下走“煞生印、印生身”路径；这一反向上下文并非本条反例，却证明不能把庚申字样无条件当制甲成功。需裁定位置、根气、月令、火制、印化、原局与岁运干扰，以及所选年的有效大运柱。 |
| “有情” | [L1082](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1082)在甲戊例称四柱或大运癸与戊合为有情；同书[《论十干合》L1118](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1118)却称戊癸“无情之合”，[《有气者急有情者切》L8035](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8035)又给合气与其它有情读法。 | 三段的对象、局部语境和优先级未裁决。戊癸合**形态**不等于本例 `affinity=proven`；也不能因一般“无情之合”直接判本例 `ruled_out`。 |
| 后续条件 | [L1085–1086](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1085)在甲日戊岁例又列寅卯亥未、额外甲乙、庚辛、巳酉丑金局及丙丁火局；[L1087](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1087)另列日干天月德且太岁为用神的例外。[HY1521 L4961](../../sources/normalized/shidianguji/HY1521/text.md#L4961)的现代逗点也不足以决定“无庚辛／金局制木／火局焚木”的结合次序。 | 三支齐、发出“三合”关系、日柱有天月德标签，都不证明金局制木／火局焚木、也不证明太岁真为用神。不能把 L1082 的局部四档结果当 L1087 之后的全章终局。 |
| 其它同书解释 | [《太岁忌逢战斗》L9697–9698](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L9697)还谈“以岁为用神者无咎”、身旺弱、日与运俱犯、五行有救减分和甲日逢戊岁运。 | 这些是补充限定，不给它们与 L1082、L1086–1087 的可执行优先级，也不允许借现成格局/用神候选替代“太岁是用神”。 |

L1082 的“两字俱全／一字／二字俱无”可以表示**局部来源阶梯**，但产品请求的单一 `rescue_condition ∈ {成立, 不成立, 信息不足}` 无法同时保存“有效制伏”“有情”两路的独立状态、原局/有效大运出处和后续例外。审计提出四个**仅供裁决的 typed 输入槽**：`effectiveSuppression`、`affinity`、`laterClauseResolution`、`dayDeAndYearYongshenException`，各取 `proven / ruled_out / undetermined`，并按 `scope.layer=流年`、`scope.year=所选年` 绑定。本命柱须保留柱位；大运只取该年的有效柱，不得在全人生大运列表中任选。重复且互相矛盾的同 scope 值置 `undetermined`；缺键、只扫具名线索或只见结构均不能变成 `ruled_out`。这些槽尚非获准的 FactKey，不能向产品发 `rescue_condition=成立/不成立`。

## 真盘裁决与最小缺口

共享 [43 盘 fixture](../../tools/reports/facts-sample.json) 中十个 `caseP1_010_*`：`both / same_only / split_only / split_and_gui / natal_gui_only / luck_gui_only / neither / unknown_luck` 在 2018 年均满足**甲日戊岁入口**，但八盘的完整救应与作用均为信息不足；`wrong_day@2018` 与 `wrong_year@2017` 为本例**不适用**，不是 `rescue_condition=不成立`。`both` 同时有本命庚申、癸和日柱天月德标签，也没有独立制伏/有情/岁为用神定值。`neither` 只表示旧诊断未见同柱庚申和癸，年、时干却都有庚，不能据此称 L1086 的“无庚辛”。`unknown_luck` 缺该年有效大运，原局虽见寅午戌与火局关系文本，仍不能认作焚木或排除运上救应。**零个完整作用正例、零个完整作用反例**；删键样盘只能验证未知传播，不能冒充真盘作用反例。

**最小下一裁决**是先在 `caseP1_010_same_only@2018` 上判清 L1082 的“四柱元有庚申金”究竟本身足以给 `effectiveSuppression=proven`，还是还须独立证明甲木已被“制伏纯粹不能克戊”。该盘本命年柱确为庚申而无癸这条具名线索，能隔离两种读法；判定必须附原页、断句和所需力量/干扰标准。即使这一步解决，也仅能解开一个输入槽，不能跳过戊癸有情及 L1086–1087 的后续裁决而输出最终作用。

下一次可接受的交付须同时给出：一份对 L1082、L1086–1087、L1118、L8035、L9697 的逐句口径和优先级裁决；能对原局与所选年有效大运分别证明 `proven` 或穷尽 `ruled_out` 的事实来源与冲突政策；至少各一张真实日期排出的完整作用正例、完整排除反例、缺键/冲突未知盘，并由独立来源复核。随后才能定 `rescue_condition` 的“成立／不成立”究竟是任一局部救应、两路俱全，还是含后续例外的全章结论；`transit_effect_semantics` 还须另作命局作用与主题映射裁决。在此之前产品只能显示 010A 字面入口和中性线索，完整 010 保持 `unknown`。
