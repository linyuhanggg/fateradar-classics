# 《皇极经世书》电子本逐段审读（cursor 工作包）

状态：全文件 8789 个真实段落 ID 均已对照现有主文本处理。基线 `d47f77d` 的 corpus-3 初稿不是语义验收；本包从独立分支重审。`verified` 一律 false。结构校验通过，不等于人校或预测有效。

## 范围与独占文件

- 原文只读：`sources/fulltext/divination/huangji-jingshi/fulltext.md`（SHA256 `aeceef2a904d915e…`）
- 注解：`references/annotations/divination/huangji-jingshi.json`
- 账本：`docs/book-reviews/cursor-expand-huangji-jingshi-remaining.json`（remainingCount=0）
- 未改原文、其他书注解、inventory、公共导出、算法、依赖、main
- 仓内无独立 AGENTS/CLAUDE；口径依 `docs/FATERADAR_FULL_LIBRARY_PLAN.md`

## 完成统计

| 章 | 段数 | 去向 |
|---|---:|---|
| 提要与空页 | 2 | 解题；空页 draft/unknown |
| 卷一至四 以元经会 / 以会经运 | 5992 | 坐标格按章次+栏名+字面标去向 |
| 卷五至六 以运经世 | 1465 | 编年史事入知识库，不造命理规则 |
| 卷七至十 声音与年表混排 | 1271 | 声音律吕表与残留编年分开 |
| 卷十一至十二 观物 51–62 | 13 | 义理手写白话 |
| 卷十三至十四 外篇 | 43 | 义理手写白话 |
| 附录张行成索隐 | 3 | 别书分层，截断不补 |

种类（重审后）：术语 8191，案例 503，理论 65，序跋目录 25，评注或元数据 4，待核实 1。review：source-reviewed 8788，draft 1。verified true = 0。

## 必须保留的限定

- 易外别传、朱子“推步之书”是体例定位，不是占验已验。
- 天下之数出于理，违乎理则入于术；以数入术则失理。
- 先天学主诚，不诚不可以得道。
- 观物非以目、非以心，而是以理；不以我观物，以物观物；以我观物则情偏而暗。
- 有数而不见，不得补成零或另造。
- 水火土石是本书地体，不改写成金木水火土再接入八字。
- 声音唱和不是元会运世序号格，也不进入纳音。
- 名存实亡犹愈于俱亡；五伯语其王则未；无学则未尽善。

## 验证

`python3 tools/validate-annotations.py --annotations references/annotations/divination/huangji-jingshi.json --json`：ok，8789 条，0 errors。该校验只做结构与 ID，不是语义证书。

## 未决（不阻塞本文件账本清零）

- 无四库 0803 影印在工作树，疑符□■○不补字，个别疑文位置保留。
- 长编年按干支分年转写，未把每一条晋唐长记改成完全现代叙事。
- 电子标题常承上一格，解释以正文为准。
- 不提升人工 verified / golden。源码质量通过后仍由 integration 复核。
