# SANMINGTONGH-011 来源陈述与同支事实三态修正（2026-09-23）

`SANMINGTONGH-011` 继续为 `applicable_to=[]`、`verified=false`，不进入六主题 manifest。本文只记录两项可独立验收的边界修正，不把结构事实写成吉凶判定。

## 来源陈述

[《论太岁》L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)直接说甲子流年再逢甲子运称“岁运并临”，紧接“独羊刃七煞为凶，财官印绶亦吉”，并将“灾殃立至”限定为羊刃。此前本条 `statement` 在单独锚定 L1084 时又写“及命局喜忌”，混入了其它段落的合参要求；现在 `statement` 只概括本锚的可见内容。命局喜忌、救应和作用仍作为待审问题，见[《论阳刃》L3459–3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3459)、[《消息赋》徐注 L8893–8894](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8893)和[《金玉赋》L10158](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L10158)。这些段落不能反推 L1084 已给出本命／岁运柱刃杀、财官印绶的分类算法或多类优先级。

`suiyun_binglin` 是同年有效大运与流年同干支的中性结构，`suiyun_same_zhi` 是同支的中性结构；L8893 的庚午运／戊午岁属于后者、不是前者。任一结构值为“否”，只否定相应形态，不否定另一段来源所称的并临，也不否定或肯定吉凶。

## 缺运事实的可执行边界

产品与古籍共享事实值域为 `是 / 否 / 信息不足`。古籍 Python 参考求值器过去漏掉 `suiyun_same_zhi` 的显式未知注册：2100 年缺有效大运的真盘虽发出 `suiyun_same_zhi=信息不足`，以“同支=是”为目标的谓词却会误回“不满足”。现已修为“信息不足”，并点名 `missing_fact_keys=[suiyun_same_zhi]`。这只修复参考求值三态，不新增正式 011 谓词。

在两仓字节一致的共享真实盘上，分别用年份 scope 求 `suiyun_binglin=是` 与 `suiyun_same_zhi=是`，Python `evaluate` 与产品 `evaluateApplicableTo` 的判语及缺键列表逐项一致：

| 样盘与所选年 | 同干支 | 同支 | 可解释范围 |
| --- | --- | --- | --- |
| `caseFlowYearBinglin@1993` | 满足 | 满足 | 癸酉运／癸酉年，仅结构。 |
| `caseFlowYear@2019` | 不满足 | 满足 | 丁亥运／己亥年，仅同支异干。 |
| `caseFlowYear@2026` | 不满足 | 不满足 | 两种形态均不命中。 |
| `caseFlowYearUnknown@2100` | 信息不足 | 信息不足 | 缺有效大运，不得写成反例。 |

八项跨仓对照均一致。古籍单测还核对显式未知的 `missing_fact_keys`，`verify-semantic-contract-candidates.py` 仍确认 011 未采纳。尚缺按本命、大运、流年层级分开的刃杀／财官印绶有效分类、并存策略、喜忌／救应作用条件及其真实三态语义样盘；这些未交付前，产品不得由两项结构事实产生 011 的主题作用或吉凶结论。
