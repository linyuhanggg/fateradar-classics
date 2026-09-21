# classics → cosmic：P1 流年请求回复（2026-09-22）

产品请求见 `/Users/sync/code/cosmic-fortune-lab/docs/closeout/COSMIC_TO_CLASSICS_P1_REQUEST_20260922.md`。当前回复为 **partial**：已采纳 1 条 `verified=false` 的保守流年结构规则，其余候选仍阻塞。

cosmic 已重建共享 facts sample：现在有 `本命`、`大运`、`流年`，并带年份 scope、流年干支、流年与本命关系、大运干支/方向、本命喜忌、`suiyun_binglin`、`dayun_liunian_relation` 和稳定的 `dayun_liunian_relation_class` 事实。当前 26 个八字固定 case 的 SHA-256 为 `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c`，与产品仓 fixture 字节一致。

本轮采纳 `YUANHAIZIPIN-YR-03`：流年层 `dayun_liunian_relation_class ∈ {相冲, 相克, 相刑}` 时，输出原文所称的“忌象候选”结构证据；先按选定 `scope.year` 过滤，再求值。固定样盘为 `caseFlowYear@2025=满足`、`caseFlowYear@2026=不满足`、`caseFlowYearUnknown@2100=信息不足`。该规则不输出现实事件，制化、喜忌和命局作用仍保留 unknown。

`SANMINGTONGH-010`、`SANMINGTONGH-011`、`DITIANSUICHA-051` 仍阻塞：缺少制化救应、刃杀财官印绶分类或完整主题语义；不把空 `applicable_to` 改成近似流年规则。

机器可读清单见 [`CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json`](./CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.json)，完整八字主题 manifest 见 [`P1_BAZI_TOPIC_MANIFEST_20260921.json`](./P1_BAZI_TOPIC_MANIFEST_20260921.json)。产品可消费该 1 条结构规则；其余流年主题和缺少作用语义的候选继续保持 `unknown`。

## 2026-09-22 求值边界纠正

首次运行 `python3 tools/audit-flow-year-unknown.py` 曾失败（exit 1），失败证据保留在 `tools/reports/p1-bazi-20260922/flow-year-unknown-before.json`；当时 2100 的 Fact 值“信息不足”被参考求值器降成“不满足”。classics 已修正参考求值器的显式未知传递，并以固定三态诊断复跑通过；当前报告为 `tools/reports/p1-bazi-20260922/flow-year-unknown.json`。这只关闭参考求值器的语义门；当前 YUANHAIZIPIN-YR-03 已另以关系分类事实通过独立三态审计，不等于其制化/喜忌作用语义已经完成；`SANMINGTONGH-011` 仍因刃杀财官印绶、喜忌和救应语义缺失而阻塞。产品仓需在真实 fixture 上回归同一契约，救应/喜忌语义由 classics 提供原文和人工流派裁决，不交给产品猜测。

## 2026-09-22 产品侧只读验收阻塞

古籍仓在产品仓只读运行：

```bash
cd /Users/sync/code/cosmic-fortune-lab
bunx vitest run tests/rules/explicit-unknown-facts.test.ts tests/engine/bazi-vertical.test.ts --reporter=dot
```

结果为 `22/24` 通过、exit 1；完整失败日志保存在 `tools/reports/p1-bazi-20260922/cosmic-integration-before.log`。这次只读验收未修改 cosmic 文件。

- `大运与流年关系分类只归一结构关系，不推断吉凶` 仍期待 `2027=相克`，但共享 fixture SHA `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c` 和当前生成器输出是 `2027=其他`。产品测试需对齐已重建 fixture，或提交有版本号的 fixture 变更；古籍规则不把 `其他` 推断成 `相克`。
- `交接七条规则的正例、反例和缺键边界在产品求值器复算` 中 `YUANHAIZIPIN-YR-03` 的反例得到 `满足`。产品通用 harness 尚未消费 manifest 的 `caseFlowYear@2025`、`caseFlowYear@2026`、`caseFlowYearUnknown@2100` 年份选择器，而是把多年份事实混在一起求值。产品需先按 `scope.year` 过滤，再求值并保留三态；古籍仓不撤回年份作用域来迁就该 harness。

在上述两项修正前，产品侧交接状态保持 `partial`，不能宣称七条规则端到端验收通过。

## 产品侧重跑（2026-09-22）

cosmic 重跑同一命令后仍为 `22/24` 通过、exit 1，日志见 `tools/reports/p1-bazi-20260922/cosmic-integration-rerun.log`：

- `流年切换改变时间层和快照身份，但保留同一出生输入` 仍要求所有流年 RuleEvaluation 都是 `unknown`。该断言与已采纳的 `YUANHAIZIPIN-YR-03` 不一致：它明确支持流年层，选定年份命中时可以是 `satisfied`；产品应只把未支持的规则/主题保留为 `unknown`。
- `交接七条规则的正例、反例和缺键边界在产品求值器复算` 中 `YUANHAIZIPIN-YR-03` 反例仍为 `满足`，说明通用 harness 仍未应用 `verification.negative` 的年份选择器。

古籍仓没有修改 cosmic 文件；在产品修正这两处后，再进行端到端重跑。

## 给产品测试 harness 的最小消费契约

对 `manifest.rules[*].verification`，产品测试应先解析 `case` 和可选 `year`：取对应 case 的 facts，再保留 `fact.scope.year === year` 的事实，最后调用 predicate evaluator。不能把整个 `caseFlowYear` 的多年份事实直接作为一个盘面。

流年视图的断言也应按规则的 `applicableLayers` 判断：`YUANHAIZIPIN-YR-03` 在 `流年` 是可执行结构证据，因此选定年份命中时允许 `satisfied`；尚未实现的主题语义、未支持时间层和缺事实条件才保持 `unknown`。这两个断言是产品消费合同的一部分，不需要古籍仓改变规则。
