# 八字三条语义合同候选（未采纳）

状态：`not_adopted`。本报告只检查原文和当前事实样盘，不修改 `rules.yaml`、manifest、`applicable_to` 或 `verified`。当前 manifest 仍是 `semanticContractStatus=pending`。

验证入口：

```bash
cd /Users/sync/code/fateradar-classics
python3 tools/verify-semantic-contract-candidates.py
```

脚本会校验 fixture SHA、原文锚点、规则未被采纳，以及形态样盘和正式语义键的边界。最近一次结果：`PASS`；`candidateAdopted=false`、`rulesChanged=false`、`manifestChanged=false`。

## 结论

| ruleId | 源文能否直接形成正式合同 | 当前可保留的候选 | 代码无法决定的最小问题 |
|---|---|---|---|
| `SANMINGTONGH-010` | 只能形成一个有明确例子的窄候选，不能直接推广 | `甲日克戊岁`；原局/大运的庚申制甲、癸戊相合；输出救应三态 | 庚申是同柱还是任一金根；一项救应算“成立”还是部分；多救应是否叠加；相合是否要求合化/得令/不被冲破 |
| `SANMINGTONGH-011` | 不能 | 只能确认选定年大运与流年干支相同的并临形态 | 羊刃/七杀/财官印绶分类算法；多类优先级；命局喜忌值域；并临的作用与救应 |
| `DITIANSUICHA-051` | 不能 | 可把大运重支、流年重干、盖头/截脚列为候选输入 | 用神/忌神结构化值域；盖头/截脚权重；原局制化、冲战覆盖关系；作用三态判定 |

## 原文证据

- `SANMINGTONGH-010`：[`sources/fulltext/bazi/sanming-tonghui/fulltext.md:1080`](../../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1080)–`1083`。L1082 举出庚申制甲、癸与戊相合，并区分两项、一项、无项；当前 Facts 没有正式救应证据或作用键，26 个样盘没有满足/不满足算例。
- `SANMINGTONGH-011`：同文件 `:1084`。原文只说明甲子岁运并临和羊刃七煞/财官印绶方向；当前 `caseFlowYearBinglin/1993` 只有 `suiyun_binglin=是`、`癸酉=癸酉` 形态，分类和作用仍是信息不足。
- `DITIANSUICHA-051`：[`sources/fulltext/bazi/ditiansui-chanwei/fulltext.md:13400`](../../../sources/fulltext/bazi/ditiansui-chanwei/fulltext.md#L13400)–`13430`。原文同时要求喜忌、重干支、盖头/截脚和原局制化；当前只有 `yongshen` 名称、自由文本 `natal_favorable_context` 和干支，不能推出用神得力/忌神得权。

`natal_favorable_context` 仅是描述性文本；`shishen`、`yongshen`、动态关系文本只能作为候选输入，不能代理保留语义键。三条均继续 `blocked`，待人工裁决后再补结构化事实、三态样盘和正式交接。

## 给主会话的最小裁决表

下一轮只需回答下面的合同问题；回答前不需要改代码。每个被采纳的键都必须同时给出值域、作用层、缺失/零值语义，以及共享 fixture 中各一条 `满足`、`不满足`、`信息不足` 样盘。

1. `SANMINGTONGH-010`
   - `甲日克戊岁` 是否只限原文示例，还是允许推广到全部日干克岁干？
   - `庚申制甲` 的证据是同柱 `庚申`，还是任一可计算的庚辛/金根条件？
   - `癸戊相合` 是否要求合化、得令或不被冲破？
   - 同时有一项、两项救应时，输出 `成立`、分级结果，还是仍为 `信息不足`？
2. `SANMINGTONGH-011`
   - `natal_binglin_class` 的分类算法和多类优先级是什么？
   - `natal_favorable_context` 的稳定枚举是什么？自由文本不能直接消费。
   - 岁运并临的作用如何由本命、大运、流年三层事实判定？
3. `DITIANSUICHA-051`
   - `yongshen_effective` 与 `jishen_empowered` 的值域和判定条件是什么？
   - 盖头/截脚的权重、原局制化和冲战覆盖例外如何编码？
   - “大运重支、太岁重干”只作为输入权重，还是有可审计的三态输出？

未回答的项目继续返回 `信息不足`；不能用十神名称、神煞名称或喜用文本代答。
