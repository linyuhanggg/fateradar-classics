# 消费方数据版本 · t203 可调用性契约 + 跨实现三态一致性

日期：2026-09-21。基线提交：`9fd7bba`（t202 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`aba931afe78fcc7fec2b0f350eff5b35ea442d9e`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标里那条「**新规则必须可被消费方当工具调用：入参盘面状态，返回结论 + 置信度 + 出处**」
此前只是**假定**（生成文件里有这些字段）。本轮把它做成**可复跑的验收**，
并且顺手做成了**跨实现一致性检查**——因为同一套谓词有**两个求值器**。

产品侧测试从 **3545 → 3571**（新增 8 + 19 项）。

## 1. 消费方契约测试（8 项）

`tests/rules/consumer-contract.test.ts`：用**真实生成数据 + 合成盘面**走完整条路
（`evaluateApplicableTo` 与 `matchRules` 都跑），钉住四件事：

| 钉子 | 断言 |
|---|---|
| **出处齐备** | `anchor.file`／`startLine`／`endLine` ＋ `source.book` 都在 |
| **绝不声称已校勘** | `verification` 只能是 `provisional`，**不得**出现 `verified` |
| **三态不冒充** | 缺键 → 「信息不足」，**且不进 hits**（不是「不满足」，更不是命中） |
| **命中形状** | `{rule, matched, score, verdict, confidence, missingKeys}` |

被检规则取自各轮新增的写法：`LIURENZHIYIN-004`（t200）、`ZENGSHANBUYI-030`（t193）、
`QM-P27`（t188 嵌套 `same`）。

### 1.1 我写错的两处，都留在测试注释里

1. 我以为置信度嵌在 `evaluation` 里 —— 实际在**顶层**（`RuleHit.confidence`）；
2. 我以为「信息不足」的置信度是 0 —— 实际是 **0.5**。原因：**置信度是「数据覆盖度」**
   （多少子句有数据可判），**不是成立概率**。

> ⚠ **给消费方的提醒**：`confidence: 0.5` 不是「五成把握」，
> 而是「一半的子句有数据可判」。两个子句里有一个「键在场」型、另一个无键可查，就会是 0.5。

## 2. 跨实现三态一致性夹具（19 项）

**同一套谓词有两个求值器**：

| 实现 | 位置 | 谁在用 |
|---|---|---|
| Python `eval-predicates.py` | 经典仓 `tools/` | 覆盖率、验证深度、各轮合成盘验收 |
| TypeScript `evaluateApplicableTo` | 产品仓 `src/lib/engine/facts/vocab.ts` | **消费方真正跑的** |

两边各写各的，就可能**悄悄分叉**（例如一边把「缺键」算成「不满足」）。
t203 我手工比对过一次（`LIURENZHIYIN-004` 两侧一致），但**手工比对不是回归**。

做法：

1. 经典侧 `tools/eval-agreement-fixture.py --write` —— 对 **5 条规则 × 16 个探针**
   求出三态，把 `expected_verdict` **算出来**（不是手抄）写进产品仓夹具
   `tests/fixtures/eval-agreement-probes.json`；
2. 产品侧 `tests/rules/eval-agreement.test.ts` 用**同一批 facts** 复放 generated 谓词并比对。

覆盖的写法（每条都带「成立／不成立／缺键」三种情形）：

| 规则 | 写法 | 何在 |
|---|---|---|
| `LIURENZHIYIN-004` | `none_of` 全称判断 + 正句保键在场 | t200 |
| `QM-P27` | 嵌套 `all_of` + 内层 `same` 配对 | t188 |
| `ZENGSHANBUYI-ZR-08` | 5 六亲 × 6 爻 枚举配对 | t197 |
| `SANMINGTONGH-R-02` | 枚举十天干做「藏与透同值」 | t195 |
| `HZL-R004` | 6 爻 × 2 六亲 持世配对 | t194 |

并专门断言 **两侧都不得把「缺键」当「不满足」**（最容易分叉的一条）。

**实测：19/19 通过**，两侧三态完全一致 ✓。

## 3. 未决清单（承接 t202）

| # | 事项 | 状态 |
|---|---|---|
| 1 | `v14-low-correspondence`／`p6-grey-zone` | t202 查证：不可机器推进，改交 40 条人眼读单 |
| 2 | 余 38 条未被样盘演示 | 37 目录式（结构性自证）＋ 1 条 `TAIWEIFU-010`（可换网格再搜） |
| 3 | 六壬「遥克／四课去重」2 条 | 引擎有遥克候选逻辑但未产出 |
| 4 | 六爻用神×关系、八字化气/有根 7–9 条 | 需五行**关系**判定（写成谓词会爆炸） |
| 5 | 八字神煞 30 条 | t201 改判：横跨三套神煞体系，不是可做的块 |
| 6 | `ZENGSHANBUYI-025`／`QM-P30`／`QM-P26` | 各 1–2 条，卡在罕见结构／原文两读／口径待裁 |
| 7 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 4. 可复跑命令

```bash
# 经典侧：重新生成一致性夹具（改过谓词后要跑）
cd /Users/sync/code/fateradar-classics
python3 tools/eval-agreement-fixture.py --write

# 产品侧：两项验收
cd /Users/sync/code/cosmic-fortune-lab
FATERADAR_CLASSICS=/Users/sync/code/fateradar-classics npx vitest run \
  tests/rules/consumer-contract.test.ts tests/rules/eval-agreement.test.ts

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
cd /Users/sync/code/fateradar-classics
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/domain-check.py
python3 tools/verification-depth-report.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 5. 给 cosmic 的版本钉

**无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `aba931afe78fcc7fec2b0f350eff5b35ea442d9e`；产品仓无需重新导出。
产品侧测试 **3571 passed / 0 failed**（新增 27 项：契约 8 + 跨实现一致性 19）。

**给消费方的三条读数**：

1. **置信度是数据覆盖度，不是成立概率** —— `0.5` 意为「半数子句有数据可判」；
2. **`verification` 恒为 `provisional`** —— 本仓全库 `verified: true` 为 0，
   任何界面都不应显示「已校勘／已验证」；
3. **谓词现在有两处实现必须同调**：改经典侧谓词语义时，
   请重跑 `tools/eval-agreement-fixture.py --write` 并跑产品侧 `eval-agreement` 测试。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。