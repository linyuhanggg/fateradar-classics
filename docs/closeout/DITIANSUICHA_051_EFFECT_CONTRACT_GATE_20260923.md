# DITIANSUICHA-051 岁运作用合同验收门槛

结论：当前**不能交付有正／反／未知真盘的作用子合同**。这是对冻结的 50 个真实日期样盘和已裁决输入的判断，不是否认《滴天髓阐微》能作个案审读。`DITIANSUICHA-051` 仍是 `applicable_to=[]`、`verified=false`；产品不得把盖头／截脚例表或取用候选消费成用神得力、忌神得权、吉凶或六主题结论。

## 为什么窄作用判式仍缺前提

| 原文锚点 | 已明确的条件分支 | 不能省略的判断 |
| --- | --- | --- |
| [L13402–13405](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13402) | 先权日主与七字轻重，辨喜忌，再论太岁战冲和好 | 原局喜行并非单一月令、强弱标签或调候候选；流年作用不能从大运方向推出。 |
| [L13423–13426](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13423) | 同是喜木的庚寅／辛卯盖头，庚辛金无根、原局或岁干丙丁制金、原局酉冲寅卯会改变解释 | “见丙丁”不等于已证“得回制之能”；“减半”不是数值权重，未定义分支冲突时的优先级。 |
| [L13428](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13428) | 同是喜木的甲申／乙酉截脚，原局或岁干庚辛与壬癸的救应方向相反 | 同柱形态可在补充事实下转义；原文未提供所有组合的封闭真值表。 |
| [L13430–13434](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13430) | 岁运冲克和日主旺相／休囚、岁君犯日须合看 | 旺衰与冲战的作用次序、强度和缺键语义还没有正式合同。 |

紧接的原书案例也不能用形态代替作用：[L13455](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13455) 的辛卯截脚仍因原局丁火回克而叙述为仕途上升；[L13475–13482](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13475) 的乙酉截脚又同时涉及冬令、水金、丁火受克而叙述为不利。这是**书中论例的不同条件**，不是可用来验证现实事件预测的两个可定位出生日期样盘；两例既不能训练或验收通用“截脚必凶”，也不能填充产品共享 fixture 的正、反真盘。

上游喜行记录本身仍未采纳。其最小准入、同为戊日寅月仍分元神厚薄／身弱用火、喜忌仇闲的反例，见[051 喜行五行裁决边界](./DITIANSUICHA_051_FAVORITE_DECISION_BOUNDARY_20260923.md)；37 条例表的合法用途见[形态合同](./DITIANSUICHA_051_LISTED_SHAPE_CONTRACT_20260923.md)。

## 给 Product 的精确消费边界

现有 [semantic-contract-request](../../tools/reports/p1-bazi-20260922/semantic-contract-request.json) 中 `yongshen_effective`、`jishen_empowered`、`transit_effect_semantics` 是**请求的输出名，不是已交付的事实**。如将来交付，三者每个都必须有 `成立／不成立／信息不足` 值域和 `{layer: 流年, year: selected}` scope；不能用「无证据」充作“不成立”。当前生产消费只能将这三项保持**信息不足／不产出**。`favorite_luck_element_decision_record` 也是请求名称，未成为正式 FactKey。`dayun_gan_zhi` 须在所选年 `{layer: 大运, year: selected}` 唯一有效；仅有大运表或其它年的运柱不够。

要解除此门槛，Classics 与 Product 需共同提供一份可重放的来源合同，至少包括：

1. 独立于 051 形态匹配的逐五行喜行／忌行裁决：原局四柱、节气和根气证据；采用的《八格》／《体用》／《喜神》等取用路线；元神厚薄、从格和冲突取舍；本命基线怎样延续或在所选年重算。某元素未列为喜，不自动成为忌或 051 的反例。
2. 针对**限定的一个**作用分支，列出原局、所选年有效大运和流年需要的事实键、值域、来源行号、救应／冲战冲突顺序与缺键传播。若只覆盖喜木庚寅／辛卯或甲申／乙酉，也必须把原文中的丙丁、庚辛、壬癸、酉冲及“制得动否”逐项裁决；不能只写“有盖头／截脚”。
3. 同一限定分支的真实出生时间排盘**正例、显式反例、信息不足例**各至少一盘，带所选年和所需全部事实的 provenance。书中匿名四柱例只作来源阐释；反事实喜行只测条件分支，均不能充作已裁决真盘。输出必须仍限于古籍语义，不把历史职业、寿夭叙述映射为现代事件预言。

最小的当前阻断不是缺少一张形态表，而是没有任何真实样盘同时具备「来源裁决的喜行」和「补充制化／冲战后作用结果」的正反证据。运行 `python3 tools/verify-ditiansui-051-effect-gate.py` 核原文 17 处条件线索、共享 fixture 哈希和 50 盘语义事实缺口；该检查是阻断证据，不是算法验收。50 盘中 15 盘已有带年份 scope 的大运柱，仍有 0 盘带喜行裁决或作用语义；现有 `rizhu_strength` 档位、调候候选和形态输出不足以填补这些输入。

## 下一支最小可检验合同：喜木遇甲申／乙酉截脚

这一支有 [L13419](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13419) 的列举和 [L13428](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13428) 的救应／冲突说明，适合作为**待裁决目标**，现在仍不是正式 FactKey 或可执行作用规则。当前 15 个有年份大运柱的真盘中，8 个运柱在 37 条表里可找到某种形态；**0 个**为甲申或乙酉。即使 8 个形态碰巧命中，也没有逐五行喜行裁决，不能填作正例。验证器按盘而非按十个年份重复计数。

| 待交付输入或判式 | 最小值域和 scope | 必须补齐的证据 |
| --- | --- | --- |
| 喜木裁决记录（目前仅是请求名 `favorite_luck_element_decision_record`） | 木为明确喜行／木为明确非喜行／信息不足；本命基线加所选年份适用说明 | 四柱、节气、根气、采用的取用路线及排除其它路线的理由；厚薄、从格、原局制化与「随岁运取用」冲突裁决。非喜须显式分类，不能由未列入喜行推出。 |
| 有效大运柱 `dayun_gan_zhi` 与流年柱 `liunian_gan_zhi` | 大运 `{layer: 大运, year: selected}`、流年 `{layer: 流年, year: selected}`；各年唯一值或信息不足 | 原始排盘、起运和选年 provenance。甲申／乙酉是目标分支的必要形态，不是作用成立的充分条件。 |
| 原局及岁干的庚辛克制、壬癸救应 | 对每一来源路径分别给存在且能作用／明确不存在或不能作用／信息不足，并注明本命或所选年 | [L13428](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13428) 的「必凶」与「和平无凶」两句可能同时触发；须裁决金水同现、合冲改变作用和缺键传播，不能仅以天干字面出现决定。电子字形“壬登”据[影印校勘](../../sources/normalized/bazi/ditiansui-chanwei/collation-notes.md#L73)作“壬癸”。 |
| 窄分支的作用结论 | 成立／不成立／信息不足；`{layer: 流年, year: selected}` | 先定义被判的单一语义（例如“木受截脚而无救应”），再给出与上列输入一致的正例、**显式反例**、缺键未知真盘各一例。不得把“十年皆否”映射为现实事件或把“减半”变成数值。 |

上表是上游最小交付清单，**不是**新增四个正式键。当前无真实盘达到最后一行的正／反验收；即使后续发现甲申／乙酉真盘，也须先完成第一行的独立喜木裁决及第三行的救应优先级，再谈 `yongshen_effective` 或 `transit_effect_semantics`。`jishen_empowered` 还需另据《何知》[L7365–7374](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L7365) 说明跨章合参，不能从这一喜木分支推出。
