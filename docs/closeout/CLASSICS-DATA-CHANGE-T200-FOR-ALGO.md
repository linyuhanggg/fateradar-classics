# 消费方数据版本 · t200 四课上下关系入事实层（liuren 30.2% → 32.1%）

日期：2026-09-21。基线提交：`30cc469`（t199 后）。
**数据修订提交（请钉这个）：`aba931afe78fcc7fec2b0f350eff5b35ea442d9e`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

六壬**四课逐课的上下关系**入事实层（引擎起三传时早就算过），
据此把 `LIURENZHIYIN-004` 写成**精确**谓词：**liuren 30.2% → 32.1%**。
另外两条同族规则**故意不映射**并登记了理由——因为只写一半会让谓词**过宽**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 224 | 49.9% | 7.1% | 11 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| **liuren** | 11 (20.8%) | 11 (20.8%) | **17** | **32.1%** | **5.9%** | 7 → **8** |
| liuyao | 21 (30.4%) | 21 (30.4%) | 28 | 40.6% | 10.7% | 10 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **468 → 467**。4 大门禁全绿；**34** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
验证深度 **321/379 = 85%**；`coverage-report --fail-under 54` PASS；
产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 新事实：四课上下关系

`liuren-transmissions.ts` L409–412 起三传时**已经**逐课算了：

```ts
relation: controls(course.bottom, course.top) ? "下贼上"
        : controls(course.top, course.bottom) ? "上克下" : "无直接克"
```

`selection.courses[].relation` 一直可用，**只是没当事实产出**——
与 t184（奇门 `geju_qimen`）／t186（qimen 干支）／t193（六爻具名状态）／t197（旬空、反吟伏吟）同一路子。

新键 `liuren_ke_relation`：整盘产出**出现过的取值**（去重）。

## 3. 落地：LIURENZHIYIN-004

原文：**四课上下全无直接克；不是八专无克分支。**

「全无直接克」是对**四课的全称判断**，写法用 `none_of`：

```yaml
all_of:
  - {key: liuren_ke_relation, value: 无直接克}      # ① 键在场
none_of:
  - {key: liuren_ke_relation, value: 下贼上}
  - {key: liuren_ke_relation, value: 上克下}
  - {key: keti, value: 八专课}                       # ② 「不是八专」
```

**① 不是赘语——它是三态正确性的前提**：若只写 `none_of`，
键缺失时会**真空成立**，而且判不出「信息不足」。这一点已实测钉住（见下表最后一行）。

### 实测（十盘 + 合成，四个方向都对）

| 盘 | 课体 | 四课关系 | 结论 |
|---|---|---|---|
| caseB | 伏吟课 | 无直接克 | **满足** |
| caseE | 弹射课 | 无直接克 | **满足** |
| caseF | 蒿矢课 | 无直接克 | **满足** |
| caseJ | 别责课 | 无直接克 | **满足** |
| caseA／D | 元首课 | 上克下＋无直接克 | 不满足 |
| caseC／G | 重审／涉害 | 下贼上＋无直接克 | 不满足 |
| caseH | 返吟课 | 三者皆有 | 不满足 |
| **caseI** | **八专课** | 无直接克 | **不满足** ← 全无直接克**但**是八专 |
| 合成 | 弹射课 | 无直接克 | **满足** |
| 合成 | 弹射课 | 无直接克＋下贼上 | **不满足** |
| 合成 | 八专课 | 无直接克 | **不满足** |
| 合成 | 弹射课 | **缺键** | **信息不足** ← 正句的意义 |

## 4. 故意不映射的两条（并登记理由）

新键一落地，机械判据立刻多命中 2 条 —— 两条我都**不映射**：

| rule | 原文条件 | 为什么不能只写一半 |
|---|---|---|
| `DALIURENDAQU-007` | 四课完整、无直接克、**无遥克**，且不属于伏吟／返吟／八专／三课别责 | 「四课完整」与「无遥克」引擎未产出 |
| `DALIURENDAQU-008` | 去重后**恰为三课**，且无直接克、**无遥克** | 「去重后恰为三课」需计数／去重结果；「无遥克」同上 |

**关键区别**（这一轮学到的一条纪律）：

- **子集披露**（t194／t195／t196 用过）：条件写窄了 → 该适用时不适用 → 偏保守；
- **只写一半的合取** → 条件写**宽**了 → **在不该适用时也判适用** → 是**假阳性**。

后者不能拿「披露」当挡箭牌，所以**不映射**。新增理由类
`needs-unemitted-judgement`，残留台账 29 → 31。

## 5. 未决清单（承接 t199）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---|--|
| ★1 | **八字神煞名** | 30 | 需在 `shensha.ts` 补约 20 项**取法**（语料里有定义，是转录工作）——**剩余最大的一块**，属引擎投入，需决定做不做 |
| 2 | 六壬「遥克／四课去重」 | 2（007／008） | 引擎已有遥克候选逻辑但未产出；产出即可写 |
| 3 | 六爻用神×关系 4–6 条、八字化气/有根 3 条 | 7–9 | 需五行**关系**判定 |
| 4 | 余 58 条未被演示（41 目录式＋17 窄条件） | — | 目录式走结构性自证；窄条件可换候选网格继续搜（算力而已） |
| 5 | `ZENGSHANBUYI-025` 反吟／伏吟 | 1 | 约 1.6 万盘遍历未见该结构（t197） |
| 6 | `QM-P30`「三奇」两读／`QM-P26` 无取值子句 | 2 | 需人判（原文两读）／需授权（口径） |
| 7 | 需人判 3 项 | — | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付（幂等；再跑会打印「已落实」）
python3 /tmp/patch_004.py 2>/dev/null || echo "（改写脚本为一次性；成果已在 rules.yaml，用下面命令核验）"
python3 tools/eval-predicates.py --book san-shi/liuren-zhiyin --case caseI -v | head -6
python3 tools/test-expressible-residue.py          # 31 条，含新增「需未产出判定」类

# 四态验证（含「缺键 → 信息不足」）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("san-shi/liuren-zhiyin",None)}
d=json.load(open("tools/reports/facts-sample.json"))["liuren"]
for case,c in d.items():
    print(case, [f["value"] for f in c["facts"] if f["key"]=="keti"], ev.evaluate(rules["LIURENZHIYIN-004"], c["facts"])["verdict"])
def f(k,v): return {"key":k,"value":v,"scope":{"layer":"本命"},"derivedFrom":["t"]}
print("缺键 →", ev.evaluate(rules["LIURENZHIYIN-004"], [f("keti","弹射课")])["verdict"])
PY

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/verification-depth-report.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

`CLASSICS_REV` = **`aba931afe78fcc7fec2b0f350eff5b35ea442d9e`**。
产品仓 `generated/liuren.json` 已同步覆盖（17 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3545 passed / 0 failed**。

**给消费方的一条说明**：`liuren_ke_relation` 是**整盘去重后的取值集合**
（一个盘可能同时有「无直接克」与「下贼上」两个事实）。
判「全无直接克」必须用 `none_of` 排除「下贼上／上克下」，
**不能**用「存在 `无直接克`」——后者几乎每盘都成立。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。