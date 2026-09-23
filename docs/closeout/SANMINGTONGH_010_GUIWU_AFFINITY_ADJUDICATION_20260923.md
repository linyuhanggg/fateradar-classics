# 《三命通会》010：戊癸“有情”只在甲日戊岁例中作局部称谓

## 裁决

《论太岁》[L1081–1082](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1081)在**甲日遇所选戊流年**这个例子里，直说“四柱／大运中有一癸字与戊相合为有情”。国图[卷二影印 PDF 第 121 页（原印四三）](../../sources/facsimile/other/sanming-tonghui/NLC416-13jh000156-94145.pdf#page=121)可见“一癸字與戊相合爲有情”，[HY1521 L4919–4923](../../sources/normalized/shidianguji/HY1521/text.md#L4919)与 [SK1610 L5181–5184](../../sources/normalized/shidianguji/SK1610/text.md#L5181)同指这条具名支路。因此，至少可以对这段来源的**字面条件**作三态核对：原局四天干及所选年的有效大运天干中恰有一个可见的癸，所选流年干为戊，则 `namedGuiWuClause=present`；四柱与有效大运均完整、无癸则 `absent`；缺键、冲突或多癸需另审则 `undetermined`。这只是来源限定的局部称谓，不是全书通用的“戊癸合有情”事实。

《论十干合》[L1118](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1118)把戊癸称为“无情之合”，国图[同卷影印 PDF 第 125 页（原印四七）](../../sources/facsimile/other/sanming-tonghui/NLC416-13jh000156-94145.pdf#page=125)接着以少长、形貌、婚配解释这个**十干配对的取象名目**。同书[《消息赋》注 L9699–9700](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L9699)明确说明“此言人之性情心术”，也把少长无情接到婚配。它不直接否定《论太岁》甲日戊岁局部“以癸配戊”的救应称谓；反过来，L1082 也不能改写 L1118 的一般取象名目。[《有气者急有情者切》L8035](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8035)把“有情”解释为合气，又记另一说可含吉神生克，进一步说明不同段落的用语对象不能机械合并。同书[《当忧不忧》L3926](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3926)在另一壬日见戊煞语境中举 `丙寅／戊戌／壬戌／癸卯`，以“癸合去戊”解释当忧不忧，亦显示戊癸组合在不同语境有不同作用；这**不是** 010 的甲日戊岁作用正例。

[《论十干合》L1122–1124](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1122)另谈一对一、偏枯、和气贵神、冲破受伤与“合处相伤反为无补”。这些是**同书一般合论的效果限制**，没有直接写成 L1082 字面称谓的必用前提，也没有给出从原局／岁运完整计算“和气”“受伤”“争合”及其优先级的方法。因此不能因为 L1118 的“无情”就把具名支路判 `absent`；也不能因为 L1082 有癸就把待审的 `effectiveAffinity=proven`、`rescue_condition=成立`、局部阶梯“凶半／反吉”或全年吉凶写入产品。即使 `namedGuiWuClause=absent`，也只否定这一具名戊癸支路，不穷尽其它“有情”或救应路径。

## 十个实际排盘的边界

使用两仓共享 [`tools/reports/facts-sample.json`](../../tools/reports/facts-sample.json) 的十个 `caseP1_010_*` 实际日期排盘，逐盘只读取所选 2018 年（`wrong_year` 为 2017 年）的流年干、原局四天干和**该年有效**大运柱。不读取无年份的整段大运列表，不把 2013 等其它流年的癸或戊借给所选年。[验证器](../../tools/verify-sanming-010-guiwu-affinity.py)锁定源文、整理本、影印的哈希，以及十盘本条所读取输入的规范化投影哈希（`c77a7012…58773ad`），并核对这张矩阵；共享样盘中其它主题的中性事实更新不会使本项审计失效：

| 盘 | L1082 入口 | 具名一癸支路 | 来源事实 | 有效有情／完整作用 |
|---|---|---|---|---|
| `both` | 满足 | `present` | 月癸、2018 丙戌运 | 未裁定 |
| `same_only` | 满足 | `absent` | 四柱及 2018 丁亥运无癸 | 未裁定 |
| `split_only` | 满足 | `absent` | 四柱及 2018 丁亥运无癸 | 未裁定 |
| `split_and_gui` | 满足 | `present` | 时癸、2018 丁亥运 | 未裁定 |
| `natal_gui_only` | 满足 | `present` | 月癸、2018 丁亥运 | 未裁定 |
| `luck_gui_only` | 满足 | `present` | 四柱无癸、2018 癸巳运 | 未裁定 |
| `neither` | 满足 | `absent` | 四柱及 2018 己丑运无癸 | 未裁定 |
| `unknown_luck` | 满足 | `undetermined` | 四柱无癸、缺 2018 有效大运 | 未裁定 |
| `wrong_day` | 不适用 | 不适用 | 乙日戊岁 | 不适用 |
| `wrong_year` | 不适用 | 不适用 | 甲日但所选 2017 丁岁 | 不适用 |

这里的 `present/absent/undetermined` 是**字面条件的正／反／未知真盘**，不是有效有情或人生作用的真盘正反例。L1082 所说“有一癸字”是否容许两癸争合，L1122–1124 的一般限制如何应用到本例，以及 L1086–1087 的后续排除和例外如何排序，仍缺同一甲日戊岁语境中带原局、有效大运、明确判词的正反实例或同等精度的同书释例；不能用这十盘的结构覆盖替代作用裁决。

## 给 Product 的最低结构事实

Product 可以提供选定年的 `liunian_gan`、本命日干与四柱**逐柱天干**、所选年唯一有效的 `dayun_gan_zhi`，并保留各自 `scope.layer/year/pillar`、缺失与同 scope 冲突。可独立派生只读、来源限定的 `namedGuiWuClause` 三态诊断及癸的出处（本命柱位或当年大运）；它不能作为 `affinity` 或 `transit_effect_semantics` 的已证值。若未来要合成有效有情，还须额外明确多癸／多戊争合、天干与支中的冲破受伤、和气与合化是否相关、原局与所选年大运的优先级，以及与 L1086–1087 后续分支的合参次序。正式 010 的 `applicable_to=[]`、`verified=false`、manifest／规则／共享 fixture 均不因本裁决改变。
