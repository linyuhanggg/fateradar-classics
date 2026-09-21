# 消费方数据版本 · t199 补正面样盘：验证深度 58% → 85%

日期：2026-09-21。基线提交：`b2cb09c`（t198 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`1b0eb70a08e446efe5fce3bd36cd9e148e91527d`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t198 量出「378 条已映射规则里只有 220 条（58%）被样盘正面演示过」。
本轮用**贪心集合覆盖**搜索补样盘：**11 张盘补上 81 条**，
验证深度升到 **320/378 = 85%**——**一条规则都没改，只补样盘**。

## 1. 前后对比

| | t198 | t199 |
|---|---:|---:|
| 口径内已映射 | 378 | 378 |
| **被样盘正面演示** | **220（58%）** | **320（85%）** |
| 未被任何样本满足 | 158 | **58** |
| 其中目录式（六十甲子一类） | 60 | 41 |
| `全信息不足`（应恒为 0） | 0 | **0** |

按术：

| art | 已映射 | t198 有满足 | **t199 有满足** | 仍未被满足 |
|---|---:|---:|---:|---:|
| bazi | 224 | 94 | **171** | 53 |
| ziwei | 63 | 55 | **61** | 2 |
| qimen | 36 | 19 | **36（100%）** | 0 |
| liuren | 16 | 16 | 16 | 0 |
| liuyao | 28 | 25 | 25 | 3 |
| qizheng | 11 | 11 | 11 | 0 |

覆盖率与通配占比**完全不变**（bazi 49.9%／ziwei 67.7%／qimen 90.0%／liuren 30.2%／liuyao 40.6%／qizheng 24.4%）——
本轮提升的是**验证深度**，不是覆盖率。这一点值得强调：**它们本来就是两个量**。

## 2. 方法：贪心集合覆盖

**目标**：找到让这些谓词判「满足」的**真实输入**（不是把谓词改宽）。

**算法**：每轮在候选集上求值**全部当前未被演示的规则**，取「命中最多」的那张盘加入，
命中即从待覆盖集合移除；重复至无候选命中或达轮次上限。

**候选网格**：10 个年份（1988/1990/1993/1995/1998/2001/2004/2007/2010/2013）
× 12 月 × 每 3 日 × 4 时辰（1/7/13/19 时），上海；性别按日奇偶。
求值器用**产品自己的** `evaluateApplicableTo` ＋已生成 `generated/<art>.json`——
与消费方同一求值器，不是另一套实现。

**效果**：

| art | 新增盘 | 覆盖规则数 |
|---|---:|---:|
| bazi | 5 | **58 / 70** |
| ziwei | 2 | 6 / 8 |
| qimen | 4 | **17 / 17（全部）** |
| 合计 | **11** | **81** |

台账 `tools/reports/positive-sample-search.json` 记了方法、网格、每轮命中与所选输入
（含每条被哪张盘演示），可复跑、可换网格（换网格会得到**等价的**不同输入）。

## 3. 样盘落到哪里

11 张盘以数据形式写进产品侧 `scripts/dump-facts.ts` 的 `COVERAGE_SAMPLES`
（附注释说明它们是搜索得来的），由 `coverageCases(art, label)` 生成 `case…`
并进 `tests/fixtures/facts-sample.json` 与 `tools/reports/facts-sample.json`。
**样盘本身是工具输入，不影响规则数据**，故 `CLASSICS_REV` 不变。

## 4. 测试：把「会变的数字」换成「不变量」

补样盘后 `tools/test-verification-depth.py` 报红——它原来钉了
「目录式 ≥ 50 条」，而搜索顺带演示掉了一批目录式规则（60 → 41）。

修法不是改数字，而是**把那条断言换成真正的不变量**：

- 钉「目录式仍是未被演示里的**最大一类**」（不钉条数）；
- 新增「未被演示占比 < 20%」。

> 钉死一个会随施工变化的数字，就是把事实当不变量——t187 记过这条教训，这次又碰上。

## 5. 剩下的 58 条（诚实交代）

| 归因 | 条数 | 说明 |
|---|---:|---|
| `catalogue-by-value` | **41** | 六十甲子纳音一类，按取值逐条编排。要逐条正面演示需**每值一张盘**；这类另有**结构性自证**（t170：复原的干支序列须等于规范六十甲子、无重无漏） |
| `other-or-condition-specific` | 17 | 条件很窄，候选网格里没有；可继续换网格搜（方法已固定，成本是算力） |

另有既有的 3 条「取值无样盘覆盖」类（`ZENGSHANBUYI-025` 反吟／伏吟等，t197 已单独登记）。

## 6. 未决清单（承接 t198）

| # | 事项 | 变化 |
|---|---|---|
| ~~★1 补正面样盘~~ | **本轮完成主体**：81 条补上，深度 58% → 85%；余 58 条已归因（41 目录式＋17 窄条件） |
| 1 | 余 58 条 | 41 目录式走结构性自证（已具）；17 条可换候选网格继续搜（低成本） |
| 2 | `ZENGSHANBUYI-025` 反吟／伏吟 | 沿用 t197（约 1.6 万盘遍历未见该结构） |
| 3 | `QM-P30`「三奇」两读 ／ `QM-P26` 需无取值子句 | 沿用 t196（各 1 条，需人判／需授权） |
| 4 | 六爻用神×关系 4–6 条、八字化气/有根 3 条 | 需五行**关系**判定 |
| 5 | 八字神煞名 30 条 | 需在 `shensha.ts` 补约 20 项取法 |
| 6 | 六壬四课 3 条 | 引擎有 `ke4` 未产出 + 需上下克/遥克关系 |
| 7 | 需人判 3 项 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：验证深度
python3 tools/verification-depth-report.py            # 期望：320/378（85%）
python3 tools/test-verification-depth.py              # 不变量 + 交叉校验 + 反例

# 搜索台账（方法、网格、每轮命中、所选输入、剩余）
python3 -c "
import json; d=json.load(open('tools/reports/positive-sample-search.json'))
print(d['method']['algorithm']); print(d['effect'])
for art,v in d['results'].items(): print(art, v['added'], '盘，覆盖', v['covered_rules'], '条')"

# 样盘是否真的进盘（产品侧）
cd /Users/sync/code/cosmic-fortune-lab
python3 -c "
import json; d=json.load(open('tests/fixtures/facts-sample.json'))
print({k: len(v) for k,v in d.items()})"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
cd /Users/sync/code/fateradar-classics
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 8. 给 cosmic 的版本钉

**无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `1b0eb70a08e446efe5fce3bd36cd9e148e91527d`；产品仓无需重新导出。
六术覆盖率不变；**变化在验证深度**：85% 的已映射规则现在有真实输入能让它们成立。

**给消费方的两条实用读数**（合起来看）：

1. **永远出现**的规则：t182 的恒真登记册（**64** 条）——命中它们不携带信息；
2. **从不出现**的规则：本轮后只剩 **58** 条（此前 158），其中 41 条是目录式。

两者之间的部分，才是规则命中真正有筛选力的范围。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。