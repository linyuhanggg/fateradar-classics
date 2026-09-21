# 消费方数据版本 · t204 四课完整度与遥克入事实层（liuren 32.1% → 35.9%）

日期：2026-09-21。基线提交：`af70c03`（t203 后）。
**数据修订提交（请钉这个）：`87b7fa5dd72088191975d50a3926c2e195879618`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t200 时我**故意没写** `DALIURENDAQU-007/008`——它们需要三个合取项，当时只有「无直接克」一项，
**只写一半的合取会让谓词过宽**（在不该适用时也适用）。本轮把缺的两项也产成事实
（引擎同样**早就算过**），两条至此**写法精确**：
**liuren 32.1% → 35.9%**（17 → 19）。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 224 | 49.9% | 7.1% | 11 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| **liuren** | 11 (20.8%) | 11 (20.8%) | **19** | **35.9%** | **5.3%** | 8 → **10** |
| liuyao | 21 (30.4%) | 21 (30.4%) | 28 | 40.6% | 10.7% | 10 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **467 → 465**。4 大门禁全绿；**36** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用 0；取值域 0；
验证深度 **343/381 = 90%**；`coverage-report --fail-under 54` PASS；
产品侧 **3571 passed / 0 failed**，`tsc` exit 0。

## 2. 两枚新事实：仍是「引擎早就算过，只是没产出」

| 新键 | 取值 | 来自 |
|---|---|---|
| `liuren_ke_completeness` | 四课／三课 | `unique(courses).length === 3` —— **取传路径本身就按它分支**（别责／昴星） |
| `liuren_yaoke` | 有／无 | `shooting`（神遥克日曰蒿矢）／`returning`（日遥克神曰弹射）候选 |

做法：在 `LiurenSelection` 上把这两项**暴露出来**（`dedupedCourseCount`、`yaoke`），
再由 `emitLiurenFacts` 产成事实。**不是新算，是把已有判定搬进事实层**——
与 t184／t186／t193／t197／t200 同一路子。

## 3. 落地两条（三个合取项现在都表达得出）

```yaml
# DALIURENDAQU-007 四课完整、无直接克、无遥克，且不属于伏吟/返吟/八专/三课别责
all_of:  [{liuren_ke_relation: 无直接克}, {liuren_ke_completeness: 四课}, {liuren_yaoke: 无}]
none_of: [{keti: 伏吟课}, {keti: 返吟课}, {keti: 八专课}, {keti: 别责课}]

# DALIURENDAQU-008 去重后恰为三课，且无直接克、无遥克
all_of:  [{liuren_ke_completeness: 三课}, {liuren_ke_relation: 无直接克}, {liuren_yaoke: 无}]
```

四个排除项来自原文，用 `none_of` 表达；`{liuren_ke_relation: 无直接克}` 这类**正句**
同时保证键在场（缺键退化成真空成立的问题，t200 记过）。

## 4. 实测（十一盘，判别力清楚）

| 盘 | 课体 | 课数 | 遥克 | 关系 | `007` | `008` |
|---|---|---|---|---|---|---|
| caseA/D | 元首课 | 三课 | 有 | 上克下＋无直接克 | 不满足 | 不满足 |
| caseC/G | 重审／涉害 | 三／四 | 有 | 下贼上＋无直接克 | 不满足 | 不满足 |
| caseE/F | 弹射／蒿矢 | 四课 | **有** | 无直接克 | 不满足 | 不满足 |
| **caseB** | **伏吟课** | 四课 | 无 | 无直接克 | **不满足**（被 none_of 排除） | 不满足 |
| **caseI** | **八专课** | 四课 | 无 | 无直接克 | **不满足**（被 none_of 排除） | 不满足 |
| **caseK** | **昴星课** | 四课 | 无 | 无直接克 | **满足** | 不满足 |
| **caseJ** | **别责课** | 三课 | 无 | 无直接克 | **不满足**（排除） | **满足** |

`007` 只在昴星课成立、`008` 只在别责课成立 —— 两条互不串味，排除项确实在起作用。

**新增样本 `caseK`**：样本原本**没有昴星课**这一形（而 007 需要它），由遍历找出
（2026-01-04 17:00 上海），补进 dump。

## 5. 顺带记下一条自己的错

新键带来 1 条机械命中（`DALIURENDAQU-003`）。我**先按关键词**把它登记成「起例说明」，
**读原文才发现**：其 statement 是「**四课已确定且不是无效盘**」——
那是**调用前提／就绪条件**（盘可用），不是起例。
已更正为 `meta-rule`，并在登记里写明「**先读再归类**」。
（t202 刚因为「不读就下结论」栽过一次，这次在同一轮内自己抓住了。）

残留台账：两条已映射**移出**、一条就绪条件**登记** → **30 条**。

## 6. 未决清单（承接 t203）

| # | 事项 | 状态 |
|---|---|---|
| 1 | 余 38 条未被样盘演示 | 37 目录式（结构性自证）＋ 1 条 `TAIWEIFU-010`（可换网格再搜） |
| 2 | 六爻用神×关系、八字化气/有根 7–9 条 | 需五行**关系**判定（写成谓词会爆炸：12×12 支对 × 爻位组合） |
| 3 | 八字神煞 30 条 | t201 改判：横跨三套神煞体系，不是可做的块 |
| 4 | `ZENGSHANBUYI-025` 反吟／伏吟 | 约 1.6 万盘遍历未见该结构（t197） |
| 5 | `QM-P30`「三奇」两读／`QM-P26` 无取值子句 | 需人判（原文两读）／需授权（口径） |
| 6 | `v14-low-correspondence`／`p6-grey-zone` | t202 查证：不可机器推进，改交 40 条人眼读单 |
| 7 | 需人判 3 项 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付（幂等：改写脚本为一次性，成果已在 rules.yaml，用下面核验）
python3 tools/test-expressible-residue.py          # 30 条
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("san-shi/daliuren-daquan",None)}
d=json.load(open("tools/reports/facts-sample.json"))["liuren"]
for case,c in d.items():
    g=lambda k:[f["value"] for f in c["facts"] if f["key"]==k]
    print(case, g("keti"), g("liuren_ke_completeness"), g("liuren_yaoke"),
          ev.evaluate(rules["DALIURENDAQU-007"], c["facts"])["verdict"],
          ev.evaluate(rules["DALIURENDAQU-008"], c["facts"])["verdict"])
PY

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
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

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`87b7fa5dd72088191975d50a3926c2e195879618`**。
产品仓 `generated/liuren.json` 已同步覆盖（19 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。

**给消费方的一条说明**：`liuren_ke_completeness`（四课／三课）与 `liuren_yaoke`（有／无）
是**整盘单一取值**；`liuren_ke_relation` 则是**去重后的取值集合**（一盘可能同时有
「无直接克」与「下贼上」）。三者语义不同，按 key 聚合时要分开处理。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。