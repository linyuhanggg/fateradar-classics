# 《论太岁》甲子岁运字面例的独立候选（2026-09-23）

结论：[L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084) 足以支持一个**只限“甲子流年又是甲子运”**的来源形态入口。本文保留正式采纳前的[独立候选 manifest](../../tools/reports/p1-bazi-20260922/sanming-011-literal-companion-candidate.json)和[四个真盘年输入](../../tools/reports/p1-bazi-20260922/sanming-011-literal-chart-fixture.json)作为审计历史。候选 ID `SANMINGTONGH-P1-011A` 已单独进入[正式 v3 12 条 P1 交接](SANMINGTONGH_011A_12_RULE_HANDOFF_20260923.md)，主题仍仅 `overview`、作用层仍仅所选流年、`verified=false`；原 `SANMINGTONGH-011` 不变。

| 真盘输入（上海，clock） | 所选年 | 有效大运／流年 | 字面入口三态 |
| --- | ---: | --- | --- |
| 1933-07-10 13:20，女 | 1984 | 甲子／甲子 | 满足 |
| 1960-01-01 13:20，男 | 1984 | 甲戌／甲子 | 不满足 |
| 1984-06-10 13:20，男 | 1984 | 无有效大运／甲子；1993 才起运 | 信息不足 |
| 1933-07-10 13:20，女 | 1983 | 甲子／癸亥 | 不满足 |

这四组由产品本地 `buildBazi(subject, selectedYear, undefined, {buildVertical:false})` 排盘并摘取该年 `liunian_gan_zhi`、`dayun_gan_zhi`、`suiyun_binglin` 事实；逐柱、起运年和事实来源均保存在 fixture。首次生成时 Product `HEAD=93c7245d`，相关代码是本地未提交状态，故不宣称远端重建。运行 `python3 tools/verify-sanming-011-literal-companion.py --replay-product` 会以当前产品工作树重新排出四盘、比较证据，并在古籍 Python 求值器上核对三态；不传 `--replay-product` 时可只验证本仓锁定 fixture、L1084 引句与正式 11 条 manifest 的 SHA。

候选谓词要求**同一所选年份**的 `liunian_gan_zhi=甲子` 与 `suiyun_binglin=是`。后一事实已经用该年有效大运与流年完整干支相等计算；不查未选中的大运列表。消费侧必须先筛选 `scope.layer=流年` 且 `scope.year=selectedYear`，再求值。校验器还放入一个异年“并临=是”的污染事实，证明不筛选时现有静态谓词会误报满足；筛选后正确保持信息不足。缺有效大运不能按“未见甲子运”判反例。

这条入口不推广到任意两柱同干支。L1084 随后说的“甲子日见甲子太岁”是**日年相并**，不能以本命日柱替代运柱；[《消息赋》徐注 L8893](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8893)的庚午运／戊午岁则另属同支异干用法。原规则 L1084 的刃杀与财官印绶分支仍缺取值层级、并存政策、喜忌及救应，见[分类来源核对](SANMINGTONGH_011_CLASSIFICATION_PROVENANCE_20260923.md)。因此本候选即使满足，也只可显示“原文甲子岁运形态”，不可输出吉凶、现实事件或六主题作用。

Product 下一步需审查并导入 v3 交接，保留原 11 条 manifest 的锁定版本与 pending 语义状态，同时加所选年过滤与初始／选中／取消选中／移动端行为验收。完整 `SANMINGTONGH-011` 的作用合同仍另行阻塞；这个字面入口不构成其完成证明。
