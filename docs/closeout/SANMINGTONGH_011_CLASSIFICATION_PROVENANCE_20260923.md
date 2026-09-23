# SANMINGTONGH-011 分类证据的层级合同（2026-09-23）

结论：`SANMINGTONGH-011` 仍为 `applicable_to=[]`、`verified=false`。现有真实盘能够逐层证明并临形态及十神**名称来源**，尚不能证明“独羊刃七煞为凶、财官印绶亦吉”的任何自动作用判语。可执行的 [来源核对器](../../tools/verify-sanming-011-provenance.py) 只读 43 盘共享 fixture，检查六个指定盘年、原文锚点和规则未采纳状态；运行 `python3 tools/verify-sanming-011-provenance.py` 可重现下表，并保留逐柱 `derivedFrom`。

| 真盘、选定年 | 有效大运／流年 | 本命十神原始证据 | 运／年干十神 | L1084 同干支／徐注同支形态 |
| --- | --- | --- | --- | --- |
| `caseFlowYearBinglin@1993` | 癸酉／癸酉 | 七杀、正财、正官、正印等并存，含藏干来源 | 正财／正财 | 是／是 |
| `caseP1_011_seven_killer@2031` | 辛亥／辛亥 | 有印、财，无本命七杀标签 | 七杀／七杀 | 是／是 |
| `caseP1_011_proper_officer@1960` | 庚子／庚子 | 年月天干七杀，另有印、财 | 正官／正官 | 是／是 |
| `caseFlowYear@2019` | 丁亥／己亥 | 七杀、财、官、印及通用羊刃标签 | 正财／正官 | 否／是 |
| `caseFlowYear@2026` | 丁亥／丙午 | 与上行同一原局 | 正财／偏财 | 否／否 |
| `caseFlowYearUnknown@2100` | 有效大运缺失／庚申 | 与上行同一原局 | 未知／偏印 | 信息不足／信息不足 |

这六行的作用值均为**未裁决**。`caseFlowYearBinglin@1993` 若只取本命单一 `natal_binglin_class`，七杀和财官印绶会互相覆盖；`caseP1_011_seven_killer@2031` 若只取本命，又会漏掉岁运干的七杀；`caseP1_011_proper_officer@1960` 若只取岁运干，又会漏掉本命七杀。这不是三个不同的作用正例，而是三种互不等价的取值政策。藏干十神、透干十神、原局格局以及岁运十神也不能未经原文裁决混成同一层级。`caseFlowYear@2019` 的运年同亥异干只命中[《消息赋》徐注 L8893](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L8893)式的同支结构；不把它放进[《论太岁》L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)同干支入口。缺有效大运时两种结构都返回信息不足，绝不能当作“不并临”。

若将来定义分类事实，最小记录应保留 `sourcePassage`、`scope.layer`、`scope.year`、`scope.pillar`、十神或刃位的 `derivedFrom`、原局/大运/流年**多值候选**及每个候选的 `是/否/信息不足`；只在输入覆盖完整时才可写“否”。分类的**取值来源与同现冲突政策**是尚未裁决的规则参数，不应由字段名 `natal_binglin_class` 偷偷固定为本命单值。进一步的作用判语还须有选定年与有效大运、类别是否真的得力、喜忌、救应以及[《论阳刃》L3468–3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3468)的相反分支和他格优先条件；[《金玉赋》L10158](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L10158)又把并临之祸系于“损用神”。这些均没有当前可验证的三态样盘。

《论阳刃》[L3459](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3459) 的甲日“时上见乙卯”与[六甲日丁卯时断 L4959](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L4959)冲突：甲日按日上起时卯时只能是丁卯，不能用真实出生日期造乙卯时正例。前者已经对见两份卷五影印，详见[影印核对与三态修正](SANMINGTONGH_011_SOURCE_AND_TRISTATE_FIX_20260923.md)；因此保留异文而不静默改字。羊刃起法也有[《论羊刃》L1623–1635](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1623)的不同口径；共享 fixture 的通用 `shensha=羊刃` 仅列作原始标签，不能充作本条“独羊刃”的已裁决输入。

下一次升级 011 的验收顺序是：先为各来源段落分配独立形态与分类 scope，给出同层多候选及跨层冲突政策；再对刃杀/财官印绶的“有效”与喜忌救应建立正例、反例、未知三态真盘；最后才可确定作用与六主题映射。任何一步仍未知时，本条继续留在不可执行域。此合同既不新增 `FactKey`，也不修改六主题 manifest。
