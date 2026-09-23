# DITIANSUICHA-051 原文列举形态窄合同

状态：可执行的**来源例表条件匹配**；`DITIANSUICHA-051` 完整岁运作用规则仍未采纳，`applicable_to=[]`、`verified=false`，P1 `semanticContractStatus=pending`。

## 输入与三态

`tools/ditiansui_051_shape_contract.py` 的 `evaluate_shape(facts, year, shape, favorite_decision)` 只对**所选年**的有效大运柱求值。`shape` 限 `gaitou`／`jiejiao`；大运柱须为该年唯一有效的 `dayun_gan_zhi`，不从十年运表、其它年份或流年柱补值。`favorite_decision` 须是另行裁决的喜行五行记录，含 `status=adjudicated`、`favoriteElement`、同一大运年 scope、`sourceRef`、`route` 和 `evidenceMode`。`counterfactual` 只供条件测试，不是实际裁决；生产来源须标 `source_adjudicated` 并附真实可追溯来源。

| 输出 | 仅表示 |
|---|---|
| 满足 | 给定喜行五行与有效运柱命中该形态的 [37 条经校勘例表](../../tools/reports/p1-bazi-20260922/ditiansui-051-shape-examples.json)。 |
| 不满足 | 完整输入已给定，但这一**形态的列举例表**没有该五行／运柱组合。它不否定另一形态或任何作用。 |
| 信息不足 | 目标年有效运柱缺失／冲突，或喜行裁决缺失、仍是候选、作用域不符。 |

无论形态匹配结果如何，返回的 `effectVerdict` 始终是`信息不足`。本合同不计算用神已得力、忌神得权、十年吉凶、数值强度、六主题输出；也不把“减半”当 0.5。原文 [L13421–13428](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13421) 的庚寅／甲申例显示制化、原局透干和流年可改变作用，[L13430–13434](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13430) 又要求旺衰与冲战合看，没有通用优先级。`jishen_empowered` 若要另立算法还须明示跨章引用[《何知章》L7365–7374](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L7365)。

## 样盘与验证边界

共享真实日期排盘 `caseFlowYear@2025` 有有效运柱 `丁亥`；在**反事实假设**喜行火时，截脚列举形态“满足”（L13419）；假设喜行木时，同一形态“不满足”。两项只测试条件分支，不是该人的真实喜忌。`caseP1_051_tiaohou_candidate@2025` 的有效运柱为 `癸酉`，调候候选不是已裁决喜行五行，实际输入返回“信息不足”。所选年 2100 无有效运柱亦为“信息不足”。测试另覆盖候选、错年、冲突运柱和 PDF 第 503 页 `乙卯→己卯` 的校勘项；校勘项是源表单测，不冒充真实生日。

运行 `python3 tools/verify-ditiansui-051-shape-examples.py` 核 37 条原文与影印校记，`python3 tools/test-ditiansui-051-shape-contract.py` 核独立求值。下一步的真正阻碍是上游可审计 `favorite_luck_element_decision_record`：须裁定流派、取用路线、旺衰／从格、喜忌与闲神、年 scope；再定义原局根气、制化、冲战、岁运作用的组合与三态真实样盘。条件匹配不解除这些阻碍。
