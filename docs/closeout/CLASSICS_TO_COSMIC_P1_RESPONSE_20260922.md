# classics → cosmic：P1 流年请求回复（2026-09-22）

产品请求见 `/Users/sync/code/cosmic-fortune-lab/docs/closeout/COSMIC_TO_CLASSICS_P1_REQUEST_20260922.md`。当前回复为 **partial**：已采纳 1 条 `verified=false` 的保守流年结构规则，其余候选仍阻塞。

cosmic 已重建共享 facts sample：现在有 `本命`、`大运`、`流年`，并带年份 scope、流年干支、流年与本命关系、大运干支/方向、本命喜忌、`suiyun_binglin`、`dayun_liunian_relation` 和稳定的 `dayun_liunian_relation_class` 事实。当前 26 个八字固定 case 的 SHA-256 为 `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c`，与产品仓 fixture 字节一致。

本轮采纳 `YUANHAIZIPIN-YR-03`：流年层 `dayun_liunian_relation_class ∈ {相冲, 相克, 相刑}` 时，输出原文所称的“忌象候选”结构证据；先按选定 `scope.year` 过滤，再求值。固定样盘为 `caseFlowYear@2025=满足`、`caseFlowYear@2026=不满足`、`caseFlowYearUnknown@2100=信息不足`。该规则不输出现实事件，制化、喜忌和命局作用仍保留 unknown。

`SANMINGTONGH-010`、`SANMINGTONGH-011`、`DITIANSUICHA-051` 仍阻塞：缺少制化救应、刃杀财官印绶分类或完整主题语义；不把空 `applicable_to` 改成近似流年规则。

机器可读清单见 [`CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json`](./CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json)，完整八字主题 manifest 见 [`P1_BAZI_TOPIC_MANIFEST_20260921.json`](./P1_BAZI_TOPIC_MANIFEST_20260921.json)。产品可消费该 1 条结构规则；其余流年主题和缺少作用语义的候选继续保持 `unknown`。

## 2026-09-22 求值边界纠正

首次运行 `python3 tools/audit-flow-year-unknown.py` 曾失败（exit 1），失败证据保留在 `tools/reports/p1-bazi-20260922/flow-year-unknown-before.json`；当时 2100 的 Fact 值“信息不足”被参考求值器降成“不满足”。classics 已修正参考求值器的显式未知传递，并以固定三态诊断复跑通过；当前报告为 `tools/reports/p1-bazi-20260922/flow-year-unknown.json`。这只关闭参考求值器的语义门；当前 YUANHAIZIPIN-YR-03 已另以关系分类事实通过独立三态审计，不等于其制化/喜忌作用语义已经完成；`SANMINGTONGH-011` 仍因刃杀财官印绶、喜忌和救应语义缺失而阻塞。产品仓需在真实 fixture 上回归同一契约，救应/喜忌语义由 classics 提供原文和人工流派裁决，不交给产品猜测。
