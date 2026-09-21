# 消费方数据版本 · t197 六爻旬空/反吟伏吟入事实层 · 用神旬空落地（liuyao 40.6%）

日期：2026-09-21。基线提交：`10f705a`（t196 后）。
**数据修订提交（请钉这个）：`1b0eb70a08e446efe5fce3bd36cd9e148e91527d`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两枚引擎已算、事实层没产出的**具名结构**入层（旬空、反吟／伏吟），
其中旬空据此落地一条（**liuyao 39.1% → 40.6%**）；
另一条（反吟／伏吟）**我选择不映射**，并把「找不到能演示它的盘」的遍历证据一并登记。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 224 | 49.9% | 7.1% | 11 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 16 | 30.2% | 6.2% | 7 |
| **liuyao** | 21 (30.4%) | 21 (30.4%) | **28** | **40.6%** | **10.7%** | 9 → **11** |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **469 → 468**。4 大门禁全绿；**33** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
`coverage-report --fail-under 54` PASS；产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 两枚具名结构

| 新键 | 取值 | 来源 | 产出条件 |
|---|---|---|---|
| `liuyao_kong` | 空 | `node.state.kong` | **只在空时产出**（缺席即不空）——避免每盘多六条「不空」噪声 |
| `liuyao_reversal` | 反吟／伏吟／卦变反伏 | `analysis.reversals` 的 `kind` | 有该结构时产出 |

`liuyao_reversal` 有一条**重要限定**：引擎自己注明
「卦变反伏与支反吟/伏吟口径未统一，**不据此终断反复成败**」——
故这里**只产出结构之名，不掺结论**（与 t193 用神「未定则不产出」同一纪律）。

## 3. 落地：用神旬空

原文（增删卜易）：**用神旬空**——空而不空（动／旺／临日月）则不空；真空——出旬即应；旬空亦可冲实。

适用范围＝「**用神所在之爻旬空**」。要表达它得把三样配起来：
用神的**名** → 该名出现在**哪一爻** → 那一爻**是否空**：

```yaml
any_of:                                   # 5 六亲 × 6 爻 = 30 支
  - all_of: [{key: liuyao_yongshen, value: 妻财},
             {key: liuqin, value: 妻财, scope: {yao: 3}},
             {key: liuyao_kong, value: 空, scope: {yao: 3}}]
  - …
```

**每支三句都带取值与 scope**，不需要无取值子句。

**如实披露**：用神也可能是「世爻／应爻」（非六亲），那几种不在本式内——属**子集**；
后文「空而不空／真空／冲实」是**断法**，不是适用范围。

### 实测

| 盘 | 用神 | 空爻（其六亲） | 结论 |
|---|---|---|---|
| caseA | 未定 | 2（妻财） | **信息不足** |
| caseB | 未定 | 5（妻财） | **信息不足** |
| caseC | **妻财** | 5（**兄弟**） | **不满足** ← 用神在场，但空不在它那一爻 |
| 合成 | 妻财 | 3（妻财，**即用神所在爻**） | **满足** |
| 合成 | 妻财 | 5（空在别的爻） | **不满足** ← 配对是本质 |

## 4. **不映射**的那一条：反吟／伏吟，附遍历证据

`ZENGSHANBUYI-025`「反吟主反复颠倒、伏吟主呻吟忧虑；皆非吉象」本可随 `liuyao_reversal` 落地，
但：

- 十个样盘里 `liuyao_reversal` **一次都没出现**；
- 我又遍历 **12 月 × 28 日 × 6 卦 × 8 种动爻组合（约 1.6 万盘）**，**仍未找到**含反吟／伏吟的盘。

结论：该结构确实罕见。**故不映射** —— 写了也无法被样盘演示，属未验证的表达。
已按新增的「**取值无样盘覆盖**」类登记（残留台账 28 → 29），
并把上述遍历作为 note 写进台账（后人若要重试，知道已经找过哪些空间）。

`liuyao_reversal` 键**保留**（引擎确实会算它、将来样本更丰富时可直接用），
但**当前 0 客户、0 样盘覆盖** —— 这一点在交付文档与版本注释里都写明。

## 5. 未决清单（承接 t196）

| # | 事项 | 变化 |
|---|---|---|
| ★1 | `ZENGSHANBUYI-025` 反吟／伏吟 | **新增**：事实已就位，卡在**没有能演示它的样盘**（~1.6 万盘遍历未见） |
| 2 | `QM-P30`「三奇」两读 ／ `QM-P26` 需无取值子句 | 沿用 t196（各 1 条，需人判／需授权） |
| 3 | 六爻用神×**关系**类（`HJC-R004/005`、`ZENGSHANBUYI-013`、`ZR-05`） | 4–6 条，需五行生克关系判定 |
| 4 | 八字化气/有根类（3 条） | 需五行关系；`canggan` 已就位 |
| 5 | **梅花 21 条** | 本仓无梅花事实层；产品引擎有体用五行 —— 是**下一个最大的可做块** |
| 6 | 八字神煞名 30 条 | 需在 `shensha.ts` 补约 20 项取法 |
| 7 | 六壬四课 3 条 | 引擎有 `ke4` 未产出 + 需上下克/遥克关系 |
| 8 | 需人判 3 项 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-liuyao-kong.py --dry-run        # 幂等
python3 tools/map-liuyao-kong.py
python3 tools/test-expressible-residue.py         # 29 条（含新增「取值无样盘覆盖」）

# 语义（配对是本质）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("divination/zengshan-buyi",None)}
d=json.load(open("tools/reports/facts-sample.json"))["liuyao"]
for case,c in d.items(): print(case, ev.evaluate(rules["ZENGSHANBUYI-ZR-08"], c["facts"])["verdict"])
def f(k,v,**sc): return {"key":k,"value":v,"scope":sc,"derivedFrom":["test"]}
print("用神妻财@3爻且该爻空 →", ev.evaluate(rules["ZENGSHANBUYI-ZR-08"], [f("liuyao_yongshen","妻财",layer="本命"), f("liuqin","妻财",layer="本命",yao=3), f("liuyao_kong","空",layer="本命",yao=3)])["verdict"])
print("用神妻财@3爻、空在5爻 →", ev.evaluate(rules["ZENGSHANBUYI-ZR-08"], [f("liuyao_yongshen","妻财",layer="本命"), f("liuqin","妻财",layer="本命",yao=3), f("liuyao_kong","空",layer="本命",yao=5)])["verdict"])
PY

# 反吟／伏吟为何不映射（遍历证据）
python3 -c "
import json
d=json.load(open('tools/reports/expressible-residue.json'))
for e in d['entries']:
    if e['rule_id']=='ZENGSHANBUYI-025': print(e['reason_class'], '|', e['note'][:150])"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
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

## 7. 给 cosmic 的版本钉

`CLASSICS_REV` = **`1b0eb70a08e446efe5fce3bd36cd9e148e91527d`**。
产品仓 `generated/liuyao.json` 已同步覆盖（28 条带谓词）；
两仓 `fact-vocab.json` 由引擎 `toFactVocabJson()` 生成、完全一致；
`tsc --noEmit` exit 0；产品侧 **3545 passed / 0 failed**。

**给消费方的一条说明**：`liuyao_kong` **只在旬空时出现**（值「空」），
**缺席即表示不空** —— 不要把它当成「每爻都有一个布尔事实」；
需要「不空」的条件请用 `none_of` 表达。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。