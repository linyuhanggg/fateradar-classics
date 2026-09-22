# classics → cosmic：P1 流年请求回复（2026-09-22）

产品请求见 `/Users/sync/code/cosmic-fortune-lab/docs/closeout/COSMIC_TO_CLASSICS_P1_REQUEST_20260922.md`。当前回复为 **partial**：已采纳 1 条 `verified=false` 的保守流年结构规则，其余候选仍阻塞。

cosmic 已重建共享 facts sample：现在有 `本命`、`大运`、`流年`，并带年份 scope、流年干支、流年与本命关系、大运干支/方向、本命喜忌、`suiyun_binglin`、`dayun_liunian_relation` 和稳定的 `dayun_liunian_relation_class` 事实。当前 26 个八字固定 case 的 SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`，与产品仓 fixture 字节一致；当前源 manifest SHA-256 为 `d33db94fc94d91a98d8624010de7dce48cb472771cc213e377f8aef338ff3d21`，产品 handoff SHA-256 为 `7165f5cf7be1244cefc135aa24b716a3e0002c2df87e1cd59c948847bbf1a08f`。文中较早出现的 hash 均为历史重建阶段证据，以末尾“当前交接指针”为准。

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

## 最新产品验收（2026-09-22）

manifest 重新生成并同步年份选择器后，cosmic 测试已提升到 `23/24` 通过；`YUANHAIZIPIN-YR-03` 反例已通过。最新失败日志见 `tools/reports/p1-bazi-20260922/cosmic-integration-latest.log`。

剩余唯一失败是流年切换测试仍断言所有流年 RuleEvaluation 必须为 `unknown` 且没有 evidence。该断言不符合本 manifest：`YUANHAIZIPIN-YR-03` 的 `applicableLayers` 包含 `流年`，选定年份命中时应产生结构证据。产品只需放宽该断言，保留未支持层和未交付主题语义的 `unknown`。

## 最终产品验收（2026-09-22）

cosmic 已完成年份选择器和流年视图断言对齐；相关测试最终为 `24/24` 通过，日志见 `tools/reports/p1-bazi-20260922/cosmic-integration-green.log`。产品 fixture 与古籍 fixture 字节一致（SHA `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c`），`CLASSICS_REV` 与 manifest SHA 也已对齐。交接状态可供产品继续消费；未形成合同的事实和主题语义仍按 manifest 保持 `unknown`。

## 2026-09-22 主题映射同步

产品重新导入 manifest 后，`YUANHAIZIPIN-YR-03` 已同时登记到 `overview`、`career`、`wealth` 三个主题；这只是同一条流年结构证据的主题消费映射，不增加新的规则语义。最新 manifest SHA-256 为 `229406ae2dd1cad2e80ab2a000f0da684f83c0d72cb6957a875f88d485a14ddf`，交接状态仍为 `partial`。
## 2026-09-22 事实复核：选定大运与三条阻塞规则

对产品重新提供的 `tools/reports/facts-sample.json`（本轮重建后 SHA-256 `ff641776d2a120f1ace49335c4a0f60349cc5a697ff597f4eab9a398a2969b69`）逐条复核后，三条候选仍不能安全升级：

- `SANMINGTONGH-010` 的原文锚点 `L1080-L1083` 明确要求制化救应与相合有情；已有流年干支和本命关系只够表达结构入口，不能把庚辛制甲乙、癸合戊等名称出现代理为救应成立。
- `SANMINGTONGH-011` 的 `caseFlowYearBinglin@1993` 能证明 `suiyun_binglin=是`，且重建后的样盘已有当前选定年份的 active `dayun_gan_zhi`/`shishen` scope；但仍缺羊刃/七杀与财官印绶分类、命局喜忌及救应条件。
- `DITIANSUICHA-051` 的 `L13400` 只有岁运合参原则，尚无可判定的 `yongshen_effective`、`jishen_empowered` 或关系作用于命局的合同。

因此本轮只确认事实输入已部分具备，不变更任何 `applicable_to` 或 `verified`。产品下一次交接应继续补齐上述作用语义的正式 FactKey、例外和满足/不满足/信息不足样盘；active 大运事实本身已进入本轮样盘，但在语义合同形成前三条继续保持 `blocked`。

## 2026-09-22 事实复核后续：active 大运 scope 已同步

cosmic 已将选定年份有效大运的 `dayun_gan_zhi` 与 `shishen` 下沉到统一 `emitBaziFacts`，并重建共享 fixture。当前产品与 classics fixture SHA-256 均为 `ff641776d2a120f1ace49335c4a0f60349cc5a697ff597f4eab9a398a2969b69`；流年样盘现在带 `{layer: 大运, year}` 的 active scope，同时保留无年份大运候选列表。

这关闭了 `SANMINGTONGH-011` 的 active scope 输入缺口，但没有关闭其语义阻塞：仍缺羊刃/七杀与财官印绶分类、命局喜忌、制化救应和三态可审计条件。`SANMINGTONGH-010` 仍缺制化救应，`DITIANSUICHA-051` 仍缺用神得力/忌神得权及岁运作用语义。三条候选继续保持 `blocked`，没有修改 `applicable_to` 或 `verified`。

本轮 classics 校验：`python3 tools/audit-flow-year-unknown.py` 三态通过；`python3 tools/test-expressible-residue.py` 的 29 条台账自洽；`python3 tools/test-ledger-consistency.py` 的 463 条未映射规则台账一致。
## 2026-09-22 manifest hash 复核

active 大运事实同步后，产品与 classics 当前 manifest 字节 SHA-256 为 `06fb5cab18279d80190f16862dbc5cb268b323ad8fa8cf95bef667e93486e501`；此前 `229406ae…` 仅对应 active scope 同步前的旧 manifest，最新机器回复已更新为当前值。

## 2026-09-22 `layerPolicy` 合同纠正

审计发现 manifest 的 `contract.layerPolicy` 仍写成“仅适用于本命”，但 8 条规则中已有 7 条声明 `applicableLayers=[本命]`，`YUANHAIZIPIN-YR-03` 声明 `applicableLayers=[流年]`。已在生成器和 manifest 中改为按各条 `applicableLayers` 求值：不得把本命规则复制到其他时间层；未声明或缺少 scope 条件时保留 `unknown`。

修正后的 classics manifest SHA-256 为 `93fdfa3cb220e77c06d98f49702b4caaba2732091e4d171243010a71ccd203b7`。产品仓需重新运行 `python3 scripts/import-bazi-topic-handoff.py ...`，同步 `src/lib/rules/generated/bazi-topic-handoff.json`，并重跑版本/主题回归；在此之前，旧的 `06fb5cab…` 只代表上一版产品导入证据。

## 2026-09-22 产品同步回归

产品仓已导入修正后的 manifest：`cosmicManifestSha256=93fdfa3cb220e77c06d98f49702b4caaba2732091e4d171243010a71ccd203b7`，生成 handoff 文件 SHA-256 为 `40800101bf00e9d5779502a84b5db473a0b0cd798ee5fe00f7994a8a73c33b55`。定向回归命令 `bunx vitest run tests/rules/explicit-unknown-facts.test.ts tests/engine/bazi-vertical.test.ts --reporter=dot` 结果为 2 files / 24 tests 全通过；这只验证 manifest 导入和当前八字主题链路，不替代全量测试。

## 2026-09-22 semantic-gap recheck

重新以当前 `tools/reports/facts-sample.json`（SHA-256 `ff641776d2a120f1ace49335c4a0f60349cc5a697ff597f4eab9a398a2969b69`）审计 `SANMINGTONGH-010`、`SANMINGTONGH-011`、`DITIANSUICHA-051`。三条均继续保持 `blocked`，没有任何一条可诚实升级：

- `SANMINGTONGH-010` 仍缺可计算的 `rescue_condition`；流年干支和关系只构成结构入口。
- `SANMINGTONGH-011` 仍缺刃杀/财官印绶分类、命局喜忌和救应语义；`suiyun_binglin`、active 大运 scope、十神/神煞名称不能代理完整解释。
- `DITIANSUICHA-051` 仍缺 `yongshen_effective`、`jishen_empowered` 及岁运作用语义；`dayun_direction`、流年干支和描述性喜忌不足以求值。

逐条事实、scope 和最小缺口见 [`semantic-gap-audit.json`](../../tools/reports/p1-bazi-20260922/semantic-gap-audit.json)。在 classics 提供正式 FactKey/value 枚举、例外和满足/不满足/信息不足样盘之前，产品继续保留 `unknown`，不得修改 `applicable_to` 或 `verified`。

## 2026-09-22 当前事实契约登记

Classics 已在 `references/vocab/fact-vocab.json` 登记产品输入合同的六个结构 FactKey：`gender`、`spouse_star`、`spouse_palace_zhi`、`shishen_count`、`natal_same_zhi`、`natal_relation`。登记内容包括值形状/值域、`scope`、缺失语义和零值语义；六键已加入两份 predicate 工具的 Bazi 接收键表。这里仅表示产品事实可被识别和复核，不构成规则消费合同，也不升级任何规则的 `applicable_to`、`verified` 或三态结论。

当前共享 fixture `tools/reports/facts-sample.json` 的 SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`；当前 Classics 主题 manifest `docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json` 的 SHA-256 为 `93fdfa3cb220e77c06d98f49702b4caaba2732091e4d171243010a71ccd203b7`。六个结构键仅作为输入事实登记，关系结果、身财两停、比劫夺财、制化救应和岁运现实作用仍需后续正式语义合同。

`dayun_liunian_relation_class` 已由 cosmic 正式 emit，且 Classics 词表已有其稳定枚举；现已同步登记到两份 predicate 工具的 `ART_EMIT_KEYS`，`python3 tools/predicate-report.py --json --check-open-values --check-art-keys` 通过。该键与前述六个结构键在机械残留扫描中仍按“事实可用不等于规则语义就绪”处理，因此现有 29 条 expressible-residue 台账、463 条未映射台账和三条 semantic blocker 均保持不变。

## 2026-09-22 当前 fixture 与 manifest 同步复核

当前共享 fixture `tools/reports/facts-sample.json` 与产品 fixture 字节一致，SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`，共 26 个八字样盘。重新运行 `python3 tools/generate-p1-bazi-manifest.py --output docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json` 后，源 manifest SHA-256 为 `36453d273f248f33705fb8a59372c16b1de510303351b53d801f690dfb94459b`，与产品侧当前 manifest/handoff 指针一致。

当前 productFactGaps 已反映六个结构 FactKey 的“部分可用”状态：性别/配偶星/日支、逐柱十神与计数、跨柱同支与本命关系可作结构证据；缺失不代表零值，也不等于关系或现实结果。制化救应、刃杀/财官印绶与命局喜忌、用神得力/忌神得权及岁运作用仍没有正式合同。

因此 `SANMINGTONGH-010`、`SANMINGTONGH-011`、`DITIANSUICHA-051` 继续保持 `blocked` 和 `verified=false`，不得把当前结构事实或自由文本喜忌代理为三态语义结论。逐条当前事实和缺口见 [`semantic-gap-audit.json`](../../tools/reports/p1-bazi-20260922/semantic-gap-audit.json)，其 fixture SHA 已同步为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`。

## 2026-09-22 共享 fixture 与 manifest 最终同步

前一版 Classics manifest 仍记录旧 fixture `ff641776…`，而当前 `tools/reports/facts-sample.json` 已重建为 `ee750a96…`。现已用当前生成器重建源 manifest，并同步 `productFactGaps` 的“部分可用”状态；Classics 与 Cosmic 当前源 manifest 字节 SHA-256 均为 `36453d273f248f33705fb8a59372c16b1de510303351b53d801f690dfb94459b`，产品 handoff 产物 SHA-256 为 `62b8e8c1e68f21874799faa76878d13aa8aba7748ffe9ce80ef17ed8ee58cead`，共享 fixture SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`。

Cosmic 重新导入该 manifest 后，目标回归 5 个文件、48 项通过；Classics 的 flow-year、residue、ledger、executable、open-values 和 art-keys 检查继续通过。三条语义 blocker 没有升级，`applicable_to`、`verified` 和 29/463 台账均未改变。

## 2026-09-22 三条语义合同请求已机器化

三条 blocker 的下一次交接要求已写入 [`semantic-contract-request.json`](../../tools/reports/p1-bazi-20260922/semantic-contract-request.json)。该文件只登记待交付的 FactKey、值域、scope、缺失/零值语义、原文锚点和三态样盘要求，状态为 `pending`；当前没有把这些待定义键加入可执行词表，也没有修改任何规则的 `applicable_to` 或 `verified`。满足/不满足样盘仍需 Classics 根据原文和流派裁决补齐，`caseFlowYearUnknown@2100` 仅作为现有缺键边界，不能冒充满足或不满足正例。

Cosmic 的消费门槛已同步写入该机器请求的 `consumerGate`：将来 manifest 若消费保留语义键，除了把 `semanticContractStatus` 改为 `accepted`，还必须为每个实际消费的键提供包含“信息不足”的 `valueDomain`、`scope.layer`，以及共享 fixture 中真实存在的满足/不满足/信息不足三态 case；仅改状态字段会被 Cosmic 导入器拒绝。

## 2026-09-22 当前 Cosmic 全量回归

在当前共享 fixture、manifest 和 handoff hash 下，Cosmic 全量 `bunx vitest run --reporter=dot` 已通过 **296 个测试文件、4170 项测试**，另有 2 个文件和 44 项跳过。新增的 handoff semantic import gate 也已覆盖正常 pending 导入与伪 accepted 缺合同拒绝路径。该回归证明产品交接门禁和现有三态链路稳定，不改变三条 Classics semantic blocker 的 `blocked`/`verified=false` 状态。

## 2026-09-22 语义合同候选审计（未采纳）

Classics 已生成只读候选包 `tools/reports/p1-bazi-20260922/semantic-contract-candidates.json`，配套验证脚本为 `tools/verify-semantic-contract-candidates.py`，审计报告为 `tools/reports/p1-bazi-20260922/semantic-contract-candidate-audit.json`。脚本验证通过，且确认共享 fixture SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`；三条规则均保持 `candidateAdopted=false`、`rulesChanged=false`、`manifestChanged=false`、`verified=false`。

该包只把缺口写成候选外形，尚不能进入 manifest：010 还缺救应推广范围、阈值、优先级和满足/不满足样盘；011 还缺刃杀/财官印绶分类、喜忌和岁运并临作用；051 还缺结构化用神/忌神作用、盖头截脚权重和例外样盘。Cosmic 因此继续保持 `semanticContractStatus=pending`，不消费这些候选键。

## 2026-09-22 交接生成器可重复性修正

生成器新增导出文件路径与 SHA-256 后，已重新生成 manifest 并让 cosmic 重新导入：

- Classics/Cosmic 源 manifest SHA-256：`d33db94fc94d91a98d8624010de7dce48cb472771cc213e377f8aef338ff3d21`
- Cosmic handoff 产物 SHA-256：`7165f5cf7be1244cefc135aa24b716a3e0002c2df87e1cd59c948847bbf1a08f`
- 共享 fixture SHA-256：`ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`
- 导入命令：`python3 scripts/import-bazi-topic-handoff.py /Users/sync/code/fateradar-classics/docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json`
- 结果：8 条规则导入成功；三条 semantic blocker 仍为 `pending/blocked`，没有升级 `applicable_to` 或 `verified`。

## 2026-09-22 当前字节锁复核

当前 Classics 与 Cosmic 源 manifest 字节一致，SHA-256 为 `d33db94fc94d91a98d8624010de7dce48cb472771cc213e377f8aef338ff3d21`；Cosmic handoff 产物 SHA-256 为 `7165f5cf7be1244cefc135aa24b716a3e0002c2df87e1cd59c948847bbf1a08f`，共享 fixture SHA-256 为 `ee750a96ae11dece15bdcef26b5e0fcc6b928a1e6947f1aa7ffd47fdb4c53aa7`。此前 hash 只代表旧工作区同步阶段。

本次只复核字节锁和候选审计，不改变 `semanticContractStatus=pending`，也不升级三条 blocker。

## 2026-09-22 当前发布候选复核

Classics 当前本地 `main` 为 `97e9ebec3f02c8c98cbcef8af1fa095da0299da4`，该提交已包含候选合同和发布证据，且其父链包含 `CLASSICS_REV=6321186f6aeebd0737537c45286153eedf49adb4`。远端仍只有 `origin/main=cd41f5b5cd31c107384633da0a75d89626938679`，`git ls-remote` 未返回 `6321186f…` 或 `97e9ebe…`；因此当前只能证明本地树可复核，不能把 CI 或远端发布写成完成。

本地复核结果：Cosmic 三个 source-link 文件 13 项通过；Classics `validate-executable` 为 15 个文件、258 条规则、579 个 source span、0 errors；ledger consistency 为 463 条未映射全部有理由。
