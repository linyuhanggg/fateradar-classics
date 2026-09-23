# SANMINGTONGH-011 中性原始标签候选（2026-09-23）

结论：可以交付一个**隔离、可执行的原始标签投影**，不能把它称作《三命通会》对“独羊刃七煞／财官印绶”的有效分类，更不能交付吉凶作用。候选见[机器合同](../../tools/reports/p1-bazi-20260922/sanming-011-neutral-raw-label-candidate.json)，运行 `python3 tools/verify-sanming-011-neutral-raw-label.py` 从共享真盘事实重算。它不注册 FactKey、不修改共享 fixture、规则、manifest 或产品；原 `SANMINGTONGH-011` 仍为 `applicable_to=[]`、`verified=false`。

投影只保留既有十神的**确切字面值**：本命逐柱 `shishen` 可多值并保留 `pillar`、`derivedFrom`，所选年只取 `scope.layer=大运／流年` 且 `scope.year=selectedYear` 的天干 `shishen`；并临另取同年 `suiyun_binglin` 三态。没有标签的本命列只说明 fixture 未观察到，不能断言命局无此类别。所选年有效大运的 `shishen` 若存在且不为“七杀”，才能否定“**所选大运天干原始十神恰为七杀**”这个字面等值探针；缺该事实返回信息不足。该探针不是 011 的作用谓词。

| 真盘年 | 所选大运干十神 | 字面七杀探针 | 并临形态 | 011 分类及作用 |
| --- | --- | --- | --- | --- |
| `caseP1_011_seven_killer@2031` | 七杀 | 满足 | 是 | 未裁决 |
| `caseP1_011_proper_officer@1960` | 正官 | 不满足 | 是 | 未裁决 |
| `caseFlowYearUnknown@2100` | 有效大运缺失 | 信息不足 | 信息不足 | 未裁决 |

`caseFlowYearBinglin@1993` 本命同时观察到七杀、正财、正官、正印等原始值；2031 年盘本命未观察到七杀，却在所选运年天干看到七杀；1960 年盘正相反。`caseFlowYear@2019/2026` 的本命原始值相同、所选流年干分别为正官／偏财，验证不能串用其他年份事实。核对器还逐项检查原始事实来源、所选年和三态边界。这些是真盘**原始等值探针**的正反未知，不是古籍作用的正反未知。

原文不给把这组原始值升级为有效类别的算法：[《论太岁》L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)只列甲子岁／甲子运例及相反作用词；[《论阳刃》L3468–3471](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3468)区分原局煞刃、刃印无煞而岁运逢煞，并要求月令合他格时按他格断；[《六甲日丁卯时断》L4962](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L4962)另有“七煞合刃行财官印绶”的时柱条件。更关键的是，[L781](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L781)区分印绶与枭神，[L3084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L3084)区分受制偏官与无制七煞。旧分类范围草案把正、偏财与正、偏印一起放进“财官印绶”**原始审计桶**，只可用于证明多标签同现，不能据此断“偏印即 L1084 印绶”或“十神七杀已满足无制七煞”。通用 `shensha=羊刃` 同样不能自动认作该段的“独羊刃”。

给 Product 的下一请求很窄：继续按所选年切片输出 `suiyun_binglin` 和有效大运／流年天干的原始 `shishen`，本命十神保留柱位、明干／藏干来源与 `derivedFrom`；缺有效大运时明确 unknown。若希望判“本命某类确实不存在”，还需完整本命十神覆盖或显式零值合同，不能把缺标签当反例。古籍侧先裁定 L1084、L3468–3471、L4962 各自的分类层级、正偏名词映射、刃起法、制化得力和同现优先级，之后才能要求 Product 提供有效类别及作用三态真盘。在此之前，中性投影可供审计展示，六主题作用保持 unknown。
