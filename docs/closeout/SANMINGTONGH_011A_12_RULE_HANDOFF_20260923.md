# P1 第 12 条：甲子岁运字面形态交接（2026-09-23）

## 结论与边界

`SANMINGTONGH-P1-011A` 已作为 **provisional、verified=false** 的独立来源结构规则进入 [v3 机器 manifest](P1_BAZI_TOPIC_MANIFEST_20260923.json)，仅归 `overview`，仅适用于选定流年。它不改变原 `SANMINGTONGH-011` 的 `applicable_to=[]`、`verified=false` 与分类作用缺口；整份 manifest 的 `semanticContractStatus` 仍为 `pending`。本条满足只表示《三命通会·论太岁》[L1084](../../sources/fulltext/bazi/sanming-tonghui/fulltext.md#L1084)明列的“甲子流年又是甲子运”字面形态，不输出羊刃七煞／财官印绶分类、吉凶、现实事件或六主题作用。

| 锁定物 | SHA-256／提交 |
| --- | --- |
| 源规则与两枚 FactKey 合同 | `a6ab65a182c1936a1938c0e1a1ea15bd2ea2e6f9` |
| v3 12 条机器 manifest | `d14138f81b9ed8ee366c8b9b95530126c1668450a5808e5934cf17a58c17e8d2` |
| 旧 v2 11 条 manifest | `dd2293b4bee38edf4aea3020769c2f4be8f09419b94135abd7d7ca12e20a5e7c` |
| 原共享 43 个八字 fixture | `6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb` |
| 011A 独立四盘年 fixture | `2f6da6abc82eefbbb73a20c4311b4e93337f916119067561bab616a8279ebce1` |
| 当前 `dist/rules/bazi.json` 导出 | `781e5c5f31dfe4747f06e5f9fce758e89eed136166987c5c233cc43f66a6a1b2` |

v3 前 11 条 `rules` 与 v2 逐项相同，共享 43 个八字样盘不变；第 12 条另指向[四盘 fixture](../../tools/reports/p1-bazi-20260922/sanming-011-literal-chart-fixture.json)。其 `quote` 为“又如甲子流年又是甲子運謂之嵗運并臨”，`anchor` 为同文件 L1084，`applicableTo.all_of` 只要求 `liunian_gan_zhi=甲子` 与 `suiyun_binglin=是`，两叶 `scope.layer=流年`。`requiredFacts` 另要求两键 `scope.year=selected`；必须先只保留 `scope.year=selectedYear` 的事实，再用静态谓词求值。

四盘年为：1933-07-10 女命在 1984 甲子运／甲子年满足；1960-01-01 男命在 1984 甲戌运／甲子年不满足；1984-06-10 男命在 1984 尚无有效大运，显式信息不足；第一盘选 1983 癸亥年不满足。校验器还加入异年“并临=是”污染事实：未筛选时静态求值会误报满足，按选定年筛选后保持信息不足。这里的“不满足”仅否定原文这一个字面例；缺有效大运不能借未出现甲子运判反例。本命日柱甲子也不能充当大运甲子。

## Product 消费与复核

Product 应导入 v3 manifest 和同一源提交导出的 `dist/rules/bazi.json`；初始未选年不得显示命中，选择 1984 可显示满足／不满足／信息不足，切换到 1983 或取消选择不得沿用上一年事实。总览证据必须显示来源、L1084 和“仅字面形态”的限制；移动端也需确认选年与证据状态一致。通用证据链和合参读取完整 `chart.facts` 时尤其要按 `scope.year` 切片，不能把 1983 的并临事实用于 1984。该消费行为须由 Product 侧自身测试和界面验收证明，Classics 四盘验证不能替代。

本地复核命令：

```bash
python3 tools/validate-rules.py --book bazi/sanming-tonghui --json
python3 tools/export-rules.py
python3 tools/generate-p1-bazi-12-manifest.py
python3 tools/verify-p1-bazi-11-handoff.py
python3 tools/verify-p1-bazi-12-handoff.py --replay-product
```

`classicsRev` 是本地源提交；v3 文件及本交接另行提交，均不能在未推送时冒充远端可获取证据。完整 `SANMINGTONGH-011` 的刃杀／财官印绶来源层级、并存优先级、喜忌及救应仍待正式事实合同，见[分类出处核对](SANMINGTONGH_011_CLASSIFICATION_PROVENANCE_20260923.md)。
