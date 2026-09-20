# 消费方数据版本 · t192 死引用扫描：8 条 ziwei 规则的根因是**样盘没覆盖运限层**

日期：2026-09-21。基线提交：`1713203`（t189 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`9f783dfdc69a06fc7e4febd2284883528b4255d2`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

新增一类此前没人查的检查（**死引用**：谓词引用的键在任何样盘里都没出现过），
首跑就命中 **8 条 ziwei 规则**引用 `daxian`／`liunian_taisui` ——
**正是 t170 起挂在未决清单里的那一条**。

但**根因与我此前的记法不同**：不是「引擎不产出」，而是**样盘没覆盖运限层**。
`emitZiweiFacts` 确实产出这两键，只是 `daxian` 要 `d.accent`、`liunian_taisui` 要 `viewYear`，
而 dump 建 ziwei 盘时没给参照日期。补一张带参照日期的样盘后**归零**。

## 1. 为什么这类问题能潜伏这么久

三道谓词门禁各管一段，**都不管这一段**：

| 门禁 | 管什么 | 不管什么 |
|---|---|---|
| `--check-art-keys` | 谓词的键 vs `ART_EMIT_KEYS`（**我声明**引擎产出什么） | 声明与**实际样盘**是否一致 |
| `--check-open-values` | 开放值域的**取值**是否在样盘出现过 | **键**本身是否出现过 |
| `--max-wildcard` | 通配占比 | — |

于是：键在词表里、在我的 emit 表里，但**样盘从不产出它** → 规则永远算「信息不足」，
读起来像「事实缺失」。t170 当时就是这么记的，并把它列成「需授权：恢复产出还是承认作废」。

## 2. 查证与修复

| 步骤 | 结果 |
|---|---|
| 新增 `tools/dead-reference-report.py` | 逐片叶子比对「该术样盘的已观测 key 集合」 |
| 首跑 | **8 条 ziwei 规则**引用 `daxian`／`liunian_taisui`（共 11 处叶子） |
| 查引擎 | `emit.ts` L217「daxian」、L230「liunian_taisui」**都在产出** |
| 查条件 | `daxian` 需 `d.accent && d.palace && d.range !== "——"`；`liunian_taisui` 需 `viewYear != null` |
| 查 dump | `buildZiwei(subjectA)` —— **没给 `viewDate`/`viewHour`** → 运限层为空 |
| 修法（同 t187：补样盘，不放宽任何东西） | 新增 `caseC: buildZiwei(subjectA, "2026-09-01", 12)` |
| 复跑 | 该盘 daxian=1、liunian_taisui=1；死引用 **0 处** |

### 2.1 修复后的实际效果

| 盘 | 8 条规则的结论 |
|---|---|
| caseA／caseB（无运限层） | 多为**信息不足** ← **正确行为**，不是缺陷 |
| **caseC（带运限层）** | `ZIWEIDOUSHUQ-054/065/ZW-06` → 满足；`ZIWEIDOUSHUQ-051` → **不满足**；其余满足 |

即：这些规则**在提供运限层的盘上可判**，在没提供的盘上如实说「信息不足」。

## 3. 测试（已入 CI）

`tools/test-dead-references.py`：

- **正例**：真实语料 `find_dead() == []`；
- **反例**（必须）：人为挖掉 ziwei 的 `daxian`、liuyao 的 `yao_zhi`，扫描**必须报出来**，
  且 art 要对；
- 钉住本轮修复：ziwei 样盘确实含 `daxian`／`liunian_taisui`；
- 空样盘时报出数量 ≥ 真实情况（不误报为「全都死引用」）。

> 反例是必须的 —— 这类扫描的价值全在「**它会红**」，恒过 0 的扫描等于没有扫描（t187 的同一教训）。

## 4. 未决清单更新

| # | 事项 | 变化 |
|---|---|---|
| ~~t170 `daxian`/`liunian_taisui`~~ | **结案** | 第三个答案：**它们 never 缺失**，是**样盘没覆盖运限层**。已补样盘并归零 |
| ★1 | `QM-P30` 时格「庚临时干三奇」 | 1 条；「三奇」两读，不猜 |
| 2 | `QM-P26` 直使加地丁 | 1 条；需无取值子句，口径待裁定 |
| 3 | 八字透干类（`SANMINGTONGH-R-02`／`YUANHAIZIPIN-008`） | 2 条；需引擎产出**藏干**（本气/中气/余气），之后可用配对技术 |
| 4 | 六爻**命名状态**（月破／暗动／旬空） | 引擎已算（`monthStrength`／`activity.label`／`kong`）、事实层未产出；可解锁 ~2 条 |
| 5 | 六壬课体余项 / 紫微命名格局 / 3 条无据 statement | 沿用 t187／t183／t185 |
| 6 | 其余 | 需授权（引擎投入）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：死引用扫描
python3 tools/dead-reference-report.py            # 期望：0 处，exit 0
python3 tools/dead-reference-report.py --json
python3 tools/test-dead-references.py             # 正例 + 反例（证明非空跑）

# 运限层确实进了样盘
python3 -c "
import json
from collections import Counter
d=json.load(open('tools/reports/facts-sample.json'))['ziwei']
for case,c in d.items():
    cnt=Counter(f['key'] for f in c['facts'])
    print(f'  {case}: daxian={cnt.get(\"daxian\",0)} liunian_taisui={cnt.get(\"liunian_taisui\",0)}')"

# 8 条规则在带运限的盘上可判
python3 tools/eval-predicates.py --art ziwei --case caseC -v | grep -E "ZIWEIDOUSHUQ-(051|054|065)|ZW-06"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

**无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `9f783dfdc69a06fc7e4febd2284883528b4255d2`；产品仓无需重新导出。
六术覆盖率不变：bazi 49.4%／ziwei 67.7%／qimen **90.0%**／liuren 28.3%／liuyao 31.9%／qizheng 24.4%。

**给消费方的一条说明**：`daxian` / `liunian_taisui` 只有在**给了参照日期**
（`buildZiwei(subject, viewDate, viewHour)`）时才产出。
产品侧若在没给参照日期的盘上求这 8 条规则，得到的会是「**信息不足**」——
那是如实回答，不是缺事实。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。