# 消费方数据版本 · t206 验证深度 90% → 100%，并查证最后一条为「结构性不可满足」

日期：2026-09-21。基线提交：`6c353b3`（t205 后）。
**数据修订提交（请钉这个）：`275ac4c7bd84528431d41db930d4bd09cc3b9b22`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两件事：**补完目录式正面样盘**（12 张盘覆盖 37 条规则）→ **验证深度 90% → 100%**；
以及**查证最后剩下那一条**（`TAIWEIFU-010`）——它**不是样本不够，是结构上不可满足**。

## 1. 验证深度

| | t201 | **t206** |
|---|---:|---:|
| 口径内已映射 | 379 | 381 |
| **被样盘正面演示** | 341（90%） | **380（100%）** |
| 未被任何样本满足 | 38 | **1** |

| art | 已映射 | 有满足样本 |
|---|---:|---:|
| bazi | 224 | **224（100%）** |
| ziwei | 63 | 62 |
| qimen | 36 | **36（100%）** |
| liuren | 19 | **19（100%）** |
| liuyao | 28 | **28（100%）** |
| qizheng | 11 | **11（100%）** |

**为什么 12 张盘就够**：剩下的 37 条全是**目录式**（禄命纳音一系，按「某柱干支为 X」
逐条编排）。每张盘有四个柱 → 一张盘可演示**至多四条**，故不必为每条各加一张；
贪心覆盖得 **12 张 → 全部 37 条**（t201 时我判断「37 条要 37 张盘」是错的）。

## 2. 最后一条：查证结果是「结构性不可满足」

`TAIWEIFU-010`：

- statement：**魁钺同行，位居台辅**；君臣庆会，材善经邦。
- quote：「魁鉞同行，位居臺輔。」（引文忠实）
- 谓词：`{all_of: [{ziwei_star: 天魁}, {ziwei_star: 天钺}], same: palace}` —— 要求**同宫**。

**实测 92 张盘**（1969–2015，覆盖六十甲子）：魁钺**同宫 0 次**；
观察到的 (魁宫|钺宫) 组合**恒为不同宫**（父母|疾厄、迁移|福德、命宫|财帛…）。
魁钺按年干取、相隔固定宫位，**结构上不可能同宫**。

**书里另有读法**（同书同卷）：「若**魁臨命，鉞守身**，更迭相守」；
本库其它书：「魁鉞**夾**身」「魁鉞**相夾**」（飞行紫微斗数源旨 L2525／L2758）；
引擎既有组合判据用的也是「**魁命钺身**」（`ziwei-combinations.ts`）。

**本轮不改谓词** —— 改它等于替原文在三个读法里选一个，属**人判**。
已登记 `tools/reports/dead-predicates.json`（含证据与三种可选写法），
验证深度报告据此把它单列为 `structurally-unsatisfiable`：
**残留只有 1 条，且有归因、不是黑洞**。

## 3. 测试改成更强的性质

`test-verification-depth.py` 原先钉「目录式是最大一类」——补完样盘后它归零，该断言失效 ✗。
改钉**更强的性质**：

- 残留 **≤ 2 条**；
- **每条残留都必须有明确归因**（不留「查不出为什么」的黑洞）；
- 「结构性不可满足」若已登记，**必须出现在归因里**。

（不钉具体数字——那是会随施工变化的事实；t187／t199 的同一教训。）

## 4. 未决清单（承接 t205）

| # | 事项 | 状态 |
|---|---|---|
| 1 | **`TAIWEIFU-010`「魁钺同行」的所指** | **新增**：三种读法（并见／魁命钺身／魁钺夹命），需人裁定后改谓词 |
| 2 | `liuyao.structure` 17 条（可执行层） | 两仓无定义，需人给定义；不猜所指 |
| 3 | `yongshen.zhi` 2 条（可执行层） | 跨键配对，映射表表达不了 |
| 4 | `ZENGSHANBUYI-025` 反吟／伏吟 | 约 1.6 万盘遍历未见该结构 |
| 5 | 六爻用神×关系、八字化气/有根 7–9 条 | 需五行**关系**判定（谓词会爆炸） |
| 6 | 八字神煞 30 条 | t201 改判：横跨三套神煞体系，不是可做的块 |
| 7 | `QM-P30`「三奇」两读／`QM-P26` 无取值子句 | 原文两读／口径待裁 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/verification-depth-report.py            # 期望 380/381（100%）
python3 tools/test-verification-depth.py              # 更强的性质 + 反例
python3 -c "import json; d=json.load(open('tools/reports/dead-predicates.json'))
print(d['entries'][0]['rule_id'], d['entries'][0]['kind']); print(d['entries'][0]['why_unsatisfiable'])"

# 样盘是否都还在（键名不再相撞）
python3 -c "
import json; d=json.load(open('tools/reports/facts-sample.json'))
for k,v in d.items(): print(k, len(v))"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/domain-check.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

`CLASSICS_REV` = **`275ac4c7bd84528431d41db930d4bd09cc3b9b22`**。
产品仓 `generated/*.json` 已同步覆盖；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变
（bazi 49.9%／ziwei 67.7%／qimen 90.0%／liuren 35.9%／liuyao 40.6%／qizheng 24.4%）。

**给消费方的一条实用读数**：`tools/reports/verification-depth.json` 随仓提交。
现在 **381 条已映射规则里有 380 条**都能被某张真实样盘满足——
也就是说，**只有 1 条永远不会命中**（`TAIWEIFU-010`，原因已查清并登记）。
把它与 t182 的恒真登记册（**64** 条永远命中）合起来看，规则命中的筛选力范围已经很清楚。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。