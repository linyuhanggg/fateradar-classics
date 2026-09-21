# 消费方数据版本 · t210 用神之爻的支与旺衰入事实层；更正 t205 的一处判断

日期：2026-09-21。基线提交：`301ac86`（t209 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

补上两枚**用神之爻**的事实（支、月建强度），使可执行层 `ZSB-E-01`／`ZSB-E-02`
在**用神已定**的盘上可判；同时**更正 t205 的一处判断**——
我当时说这两个字段「跨键配对，映射表表达不了」，**那是错的**。

## 1. 更正：为什么这不是配对

| | 谓词层（rules.yaml） | 可执行层（executable） |
|---|---|---|
| 「用神旬空」怎么写 | 要枚举 **5 六亲 × 6 爻** 并与 `liuyao_yongshen` 配对（t197） | — |
| 「用神之爻的支」 | 同样要配对（谓词层没有「用神之爻」这个概念） | **不用**：引擎 `analysis.use.preferredIds` 已把「哪一爻是用神」定下来了 |

引擎侧有「用神之爻」这个对象，所以它能**直接给出**该爻的支与月建强度 —— 这是**透传**，不是配对。
t205 我把两者混为一谈，故判错。已改 FIELD_MAP 与注释。

## 2. 两枚新事实

| 新键 | 取值 | 来源 |
|---|---|---|
| `liuyao_yongshen_zhi` | 用神所取之爻的**支** | `analysis.use.preferredIds` → 该爻 branch |
| `liuyao_yongshen_state` | 用神之爻的**月建强度** | 同源 → 该爻 `state.monthStrength` |

FIELD_MAP：`yongshen.zhi` → `liuyao_yongshen_zhi`；`yongshen.state` → `liuyao_yongshen_state`。
**「接不上 FactKey 的字段」21 处 → 19 处**（只剩 `liuyao.structure` 17、`day.gan.element` 1、`year.gan.doushu` 1）。

## 3. 效果**依盘而定**——这一点必须说清

`eval-executable --all` 取各术**首个**样盘（六爻是 caseA），而 **caseA 的用神未定**
→ 该盘上这两条仍如实报「信息不足」→ **`--all` 的总数没有变化**（满足 72／不满足 152／信息不足 30）。

但在**用神已定**的盘上：

| 盘 | 结果 |
|---|---|
| caseC | 满足的：`['ZSB-E-01', 'ZSB-E-02']`（其余 17 条信息不足） |
| cov4_liuyao_2 | 同上 |
| cov2_liuyao_1 | 同上 |
| **caseA（用神未定）** | 19 条**全部**信息不足 ← 如实 |

即：改进是真的，只是**不在默认那一张盘上显现**。

## 4. 顺带查明：报告口径的一个局限（记入未决）

executable 的报告只取**首个样盘**，于是「只在某些盘上才可判」的改进**看不见**。
要看得见，得让报告**跨盘汇总**（例如按「在几张盘上可判」分类）。
本轮不加这个功能（避免为一处洞察加一层报告逻辑），但把它记进未决——因为它会**系统性地掩盖**这类改进。

## 5. 未决清单（承接 t209）

| # | 事项 | 状态 |
|---|---|---|
| 1 | **executable 报告跨盘汇总** | **新增**：现只取首个样盘，会掩盖「只在某些盘可判」的改进 |
| 2 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义（**现居「接不上」之首**） |
| 3 | `day.gan.element` 1 ／ `year.gan.doushu` 1 | 前者引擎有五行表但未产出该键；后者未产出 |
| 4 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口，约 2–3 条 |
| 5 | `TAIWEIFU-010`「魁钺同行」 | 三种读法待人裁定（t206） |
| 6 | 跨键关系 7–9 条 | 建议由引擎产判定名（审计第 7 类） |
| 7 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 8 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：用神之爻的事实与两条记录的可判性
python3 -c "
import json; d=json.load(open('tools/reports/facts-sample.json'))['liuyao']
for k,c in d.items():
    z=[f['value'] for f in c['facts'] if f['key']=='liuyao_yongshen_zhi']
    s=[f['value'] for f in c['facts'] if f['key']=='liuyao_yongshen_state']
    if z: print(k, '用神支', z, '旺衰', s)"
python3 tools/eval-executable.py --package references/executable/zengshan-buyi.json --case caseC
python3 tools/eval-executable.py --package references/executable/zengshan-buyi.json --case caseA   # 用神未定 → 全信息不足
python3 tools/eval-executable.py --all                                                            # 总数不变（默认取 caseA）

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
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。
产品仓 `generated/*.json` 已同步覆盖（导出无变化）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变
（bazi 49.9%／ziwei 67.7%／qimen 90.0%／liuren 35.9%／liuyao 43.5%／qizheng 24.4%）。

**给消费方的两条说明**：

1. `liuyao_yongshen_zhi` / `liuyao_yongshen_state` **只在用神已定时出现**
   （用神未定 → 缺席 → 相关记录如实报「信息不足」，不是「不成立」）。
2. 若产品侧要判「用神是否逢空／逢月破」，现在可以直接用这两个键 + `liuyao_kong`
   （**引擎已替你定好用神之爻**，不必自己配对）。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。