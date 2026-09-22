# 产品仓 P1 流年合同请求

产品仓已提出八字 P1 流年最小交接需求：

- 产品仓原文：`/Users/sync/code/cosmic-fortune-lab/docs/closeout/COSMIC_TO_CLASSICS_P1_REQUEST_20260922.md`
- 产品当前状态：除已交接的 `YUANHAIZIPIN-YR-03` 结构证据外，其余流年主题保持 `unknown`；产品不把本命规则复制成流年规则。
- 需要 classics 返回：带 `scope.layer=流年` 的 ruleId、FactKey、关系/例外语义、原文 quote/anchor、CLASSICS_REV，以及满足/不满足/缺键三态样盘。
- 优先交付 `overview` 或 `career` 一条最小规则；财运、感情字段缺口另行登记。

本文件只是跨仓施工指针，不代表规则已采纳，不改变 `verified`、ledger 或现有版本锁。

产品仓后续已补事实准备：选定流年样盘 `caseFlowYear`，并提供 `liunian_gan`、`liunian_zhi`、`liunian_gan_zhi`、`scope.year`、`liunian_natal_relation`、`dayun_liunian_relation` 与 `suiyun_binglin`。这些只是输入事实，不是流年规则；请后续审计按救应/喜忌条件继续判断。

2026-09-22 follow-up：产品 fixture 已补三态岁运并临样盘：`caseFlowYearBinglin`（1993 年 `是`）、`caseFlowYear`（2026 年 `否`）、`caseFlowYearUnknown`（2100 年 `信息不足`），并新增 `dayun_liunian_relation` 结构事实及 `dayun_liunian_relation_class` 分类事实。两仓 fixture SHA-256 均为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`，八字样盘共 26 个。当前源 manifest SHA-256 为 `36453d273f248f33705fb8a59372c16b1de510303351b53d801f690dfb94459b`，产品 handoff SHA-256 为 `62b8e8c1e68f21874799faa76878d13aa8aba7748ffe9ce80ef17ed8ee58cead`。产品已按 `scope.year` 完成 matcher 三态回归；制化救应、合参作用和喜忌分类仍需正式语义交接。

清单一致性已复核：`YUANHAIZIPIN-YR-03` 的机器回复现已把 `dayun_liunian_relation` 与 `dayun_liunian_relation_class` 列为 `availableFacts`，并已采纳为 `verified=false` 的保守流年结构证据；制化、喜忌与命局作用仍是语义缺口。

当前回复：[`CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.md`](./CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.md)；机器可读版本：[`CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json`](./CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json)。cosmic 已补流年 facts 并消费 1 条结构规则；结论为 `partial`，没有把它扩展成现实事件规则。
