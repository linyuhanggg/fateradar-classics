# 051 逐五行喜行裁决记录候选合同

状态：这是给人工来源裁决留存证据的**窄候选格式**，不是自动取用算法、正式事实键或 `DITIANSUICHA-051` 规则。它不改变 `rules.yaml`、P1 manifest、共享事实词表或产品消费。候选可以记录一个五行的逐盘判断；盖头／截脚的吉凶作用仍始终为信息不足。

## 源文复核后能固定的部分

| 原文与校勘范围 | 可固定的合同边界 | 不能由本文固定的算法 |
| --- | --- | --- |
| 《八格》任氏曰 [L2663](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L2663)；禄刃另取见《体用》[L2949](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L2949) | 月令、透干、司令都要列证据；禄刃须记录另取入口。 | 这些输入怎样选出单一或并行用神。 |
| 《体用》[L2941–2947](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L2941) | 普通扶抑与旺极/弱极反从是不同分支；旺极抑之反激、弱极扶之无功均可能改变路线。 | 哪些盘达到“不可抑／旺极”或“不可扶／弱极”的可计算阈值，以及分支并存时的先后。 |
| 《体用》[L2949–2967](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L2949)；《衰旺》[L3203–3221](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L3203) | 取用要说明日主与四柱根气、扶制、格局；得令不自动旺、失令不自动弱。用神受合冲、劫占或阻隔时有“随岁运取用”入口。 | `rizhu_strength` 档位、五行计数、月令单项不能代替逐盘旺衰、根气或岁运取用判断。 |
| 《喜神》任氏曰 [L7313–7319](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L7313) | “戊日寅月、甲木为用”仍须裁定甲木确为用；前提成立后又分元神厚薄而喜水或火，并另有身弱改用寅中丙火入口。 | 现有强弱标签不等于元神厚薄；戊日寅月或调候候选不能代替前置用神裁决。 |
| 《闲神》任氏曰 [L8979–8999](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L8979) 与《何知》[L7369–7375](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L7369) | 记录必须区分喜、忌、仇、闲；未列入喜行不是显式忌行。“闲”在紧要岁运也可能制化护用。 | 不可从喜集合差集推导忌神、风险、现实吉凶。 |
| 《岁运》原注 [L13402–13405](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13402)；岁运安顿见《体用》[L2967](../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L2967) | 记录可分 `{layer: 本命}` 基线与 `{layer: 流年, year: selected}` 重审；051 消费需要精确到所选年。 | 本命分类不会自动延续；也不能仅见运表就宣称该年改用或原喜不变。 |

### 校勘边界

本候选引用的上游路线锚点使用已复核正文。若后续引用形态例表，还必须沿用影印记录 [L71–L73](../../sources/normalized/bazi/ditiansui-chanwei/collation-notes.md#L71)：L13411“戌申”校作“戊申”，L13419 喜土截脚“乙卯”校作“己卯”，L13428“壬登”校作“壬癸”、 “早点酉”校作“申酉”。形态例表的校字不裁决此记录中的喜行类别或岁运吉凶。

## 稳定记录形状与作用边界

`tools/ditiansui_051_favorite_record.py` 定义版本 `DITIANSUICHA-051-favorite-record-candidate-v1`。每条记录只裁一个目标五行；多喜行用同一 chart/scope 下多条记录表达，不假定唯一用神。核心值域固定如下：

| 字段 | 固定值域／条件 | 含义 |
| --- | --- | --- |
| `recordStatus`、`decision.status` | `candidate`／`adjudicated`／`information_insufficient` | 候选和缺项都不能供 051 作是/否输入。即使候选的 `disposition` 写着喜神，也仍返回信息不足。 |
| `scope` | 精确 `{layer: 本命}` 或 `{layer: 流年, year: 正整数}` | 不接受裸年、其它层或没有年份的岁运记录。选年记录须引用本命基线并明确重审状态。 |
| `element` | `木`／`火`／`土`／`金`／`水` | 本条所裁的五行，不对其它五行作差集推论。 |
| `decision.disposition` | `喜神`／`忌神`／`仇神`／`闲神`／`信息不足` | 前四项须显式来源裁决；只有喜神是“明确喜行”，三个非喜分类均不等于 051 作用不成立。 |
| `routeReviews` | 7 个固定路线 ID；每项 `applies`／`not_applicable`／`unresolved` | 分别审月令透干取用、体用扶抑/随运、极端从强从弱、根气旺衰、喜神厚薄分支、喜忌仇闲分类、选年重审。ID 用于审计，不构成路线顺序。 |
| `routeConflict` | `none`／`resolved`／`unresolved` | unresolved 一律阻止“adjudicated”；resolved 必须写方法和来源证据。合同没有内置“从强优先”或扶抑优先。 |
| `sourceAnchors` | 固定本书全文/校勘记录路径、精确行号、原文 cue、注释层 | validator 核实际引文行和其路线范围；不校验人的命理解释真假。 |
| `unresolvedItems` | 非空问题列表，除完整候选外 | 保留用神、厚薄、从格、岁运等未裁项，不把空字段或缺事实编码成反例。 |

来源限制的路线 ID 是本版人工审读检查项：`month_command_and_revealed_use`、`suppress_support_or_follow`、`extreme_following`、`root_and_strength`、`favorite_and_hidden_use_branches`、`favorite_avoidance_enemy_idle_roles`、`selected_year_reselection`。validator 拒绝额外的现代分数／调候代理路线 ID；现有调候候选只能保留为单独来源记录。validator 的 `valid` 和 `structurallyAdjudicated` 只表示格式、引文和必需审阅项完备，绝不表示产品已采纳或源义已被程序证明。

`favorite_element_verdict` 只接受结构完整的 `adjudicated` 年记录和完全相同的选年、目标五行；其返回也将 `effectVerdict` 固定为信息不足。它是人工候选的三态门，不被导入共享 Facts、`rules.yaml`、P1 handoff，也不算 051 主规则实现。

## 当前样盘核对与真实缺口

当前 Classic 与 Product 共享 fixture 是冻结的 50 盘，SHA-256 `206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8`。定向检查通过：50 盘中 15 盘含带年份大运柱、8 盘出现任一形态列举运柱、0 盘命中喜木甲申/乙酉截脚运；50 盘全部无正式喜行裁决或 051 作用事实。**真实作用正例 0、显式反例 0**，因此尚无作用三态算法验收。

- `cov3_bazi_1`（1970-02-07 13:20）真实四柱为庚戌／戊寅／戊午／己未，撞中 L7315 的戊日寅月字面入口，但没有裁定寅中甲木为用、元神厚薄、身弱改用丙火、从强路线或选年重取。其结果须保持信息不足。
- `caseP1_051_tiaohou_candidate@2025`（1990-01-01 13:20）确有当年有效大运癸酉和壬／戊调候候选；候选源自另一类资料，并没有成为《滴天髓阐微》的水／土喜行裁决。它是选年缺喜行决断的**未知边界盘**，不是正例或反例。
- 其余新增 ZPR 样盘扩展了另一条规则的形态覆盖，没有新增 051 喜行或作用决断；不会因共享 fixture 从 43 增到 50 而改变本结论。

运行验证：

```sh
python3 tools/verify-ditiansui-051-favorite-boundary.py
python3 tools/verify-ditiansui-051-effect-gate.py
python3 tools/test-ditiansui-051-shape-contract.py
python3 tools/test-ditiansui-051-favorite-record.py
```

## 解除完整算法阻塞所需的最小追加裁决

目前缺的不是五行名目，而是同一真盘/选年可重放的上游来源裁决。请来源裁定者针对选择的单一 051 分支提供以下成套决定，不要只答“用扶抑”或“日主极强”：

1. **定本条取用路线的注释层和适用范围**：原注／任氏曰是否都参与本条？对八格、体用扶抑、从强/从弱、格局气势等路线，逐项说明本盘适用、不适用或未知，并给逐项理由和锚点。若多个适用，明确是并存会合流还是确有优先次序；原文没有明示的排序须标为人工裁决，不能伪称原文规则。
2. **给一个真实候选盘的用神与旺衰前置裁决**：优先裁 `cov3_bazi_1` 是否取寅中甲木；若取，另给“元神厚/薄”的可复核古籍条件，并说明身弱用寅中丙火入口为何适用/不适用。`rizhu_strength=极强`、月令、藏干或根数本身均不能替代此裁决。
3. **逐元素显式定类**：至少对目标木给 `喜神/忌神/仇神/闲神/信息不足` 其一；如采用“木有余/不足”分支，给原局有余/不足的来源判断及缺证处理。不得以喜行缺席推导忌行。对目标分支中会改变结果的其它五行也要逐值裁定。
4. **选年重审**：指定真实出生时间/地点与选年，给该年有效大运和流年事实来源；说明 `随岁运取用` 对本命基线是重取、经裁决沿用，还是信息不足。重取或沿用均须列原局加该年改变条件的证据；不能仅复制本命标签。
5. **提供同一窄作用支的真盘边界**：正例、明确反例、缺键/路线冲突未知例各一盘，均需原始真盘和选年、上列决策记录、形态运柱、救应/冲战审读。若所选支为喜木甲申/乙酉截脚，现 fixture 中该运柱覆盖为零，需先将待加出生日期与 case ID 发给 Product 协调后统一加入冻结 fixture；不能以书中匿名四柱、反事实喜行或伪造历史应验代替。

在取得这些裁决和三类真盘前，保留本候选 schema 与 validator，仅用于阻止把调候候选、现代扶抑路线、强弱档位、未列喜行或形态匹配升级为 051 作用。完整 051 继续 `applicable_to=[]`、`verified=false`、`semanticContractStatus=pending`。
