# 消费方数据版本 · t194 六爻「财官」三条落地（liuyao 34.8% → 39.1%）

日期：2026-09-21。基线提交：`c0b1571`（t193 后）。
**数据修订提交（请钉这个）：`9999f38143eead9e78765759f31aea73a46d0777`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

火珠林三条以「**财官**」作主语的规则落地 —— 关键在于把它们**共同的主语**与
**各自的分支**分开：「财官旺相／休囚」「出现／伏藏」「持世与否」是**断法**，
三条共同的**适用范围**是「本卦所取用神为财或官」。
这正是 t193 才产出的 `liuyao_yongshen` 能表达的。

**liuyao 34.8% → 39.1%**（24 → 27），未映射 **475 → 472**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 15 | 28.3% | 6.7% | 5 |
| **liuyao** | 21 (30.4%) | 21 (30.4%) | **27** | **39.1%** | **11.1%** | 8 → **9** |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **475 → 472**。4 大门禁全绿；**33** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
`coverage-report --fail-under 54` PASS；产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 判读：主语 vs 分支

| rule | 原文 | 主语（＝适用范围） | 分支（＝断法，未表达） |
|---|---|---|---|
| `HZL-R002` | 财官**旺相**、有辅体发动或生世为可用；**休囚**、克破、无辅则力薄 | 用神为财或官 | 旺相／休囚的两支判词 |
| `HZL-R005` | 财官**出现**旺相宜久远；**伏藏**有气虽可取，多利短时 | 用神为财或官 | 出现／伏藏的两支判词 |
| `HZL-R004` | 财官**持世**虽可许，但应爻或动爻克所用辅爻则事难成 | 财／官持世 | 「事难成」的条件与判词 |

「财官」＝妻财／官鬼 —— 求财、求官两路的用神。

## 3. 两条写法

### 3.1 平铺或（R002／R005）

```yaml
applicable_to: [{key: liuyao_yongshen, value: 妻财}, {key: liuyao_yongshen, value: 官鬼}]
```

用神值域 7 取 2 → **不恒真**：只在问财／问官类的盘上成立。

### 3.2 枚举配对（R004「财官持世」）

```yaml
any_of:
  - all_of: [{key: liuqin, value: 妻财, scope: {yao: 1}}, {key: shiyao, value: 初爻, scope: {yao: 1}}]
  - … 6 爻 × {妻财,官鬼} 共 12 支 …
```

**每支两句都带取值**：`shiyao` 的取值由爻位唯一确定（第 N 爻即「初爻…六爻」），
所以**不需要无取值子句** —— 有意避开那条**口径尚未裁定**的写法（t179 待授权项 ①）。

## 4. 实测

| 盘 | 用神 | 世爻六亲 | `R002` | `R005` | `R004` |
|---|---|---|---|---|---|
| caseA | 未定 | 父母@6 | **信息不足** | 信息不足 | 不满足 |
| caseB | 未定 | 兄弟@3 | **信息不足** | 信息不足 | 不满足 |
| caseC | **妻财** | 父母@6 | **满足** | **满足** | 不满足 |

- 用神未定 → **信息不足**（不是「不满足」）：本仓不把未定当已定 ✓
- 合成盘「**妻财持世**」→ `R004` **满足**；「**父母持世**」→ **不满足** ✓ 配对真的在起作用

## 5. 台账／测试同步

- 决策台账 3 条改 `mapped` 并记 `mapped_by`；
- **残留台账 30 → 28**：`HZL-R002`／`HZL-R004` 已映射，按台账设计**移出**
  （测试强制「被映射即移除」）；`ZENGSHANBUYI-007` 仍留（**需计数**：用神两现…一爻发动／两爻俱动俱静）。

## 6. 未决清单（承接 t179／t192／t193）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---|--|
| ★1 | 六爻**用神×旺衰/关系**类（`HJC-R004/005`、`ZENGSHANBUYI-013`、`ZR-05`） | 4–6 | 需**关系判定**（生克冲合、墓、克破）或「用神所在之爻的月建强度」再配上关系 |
| 2 | 六爻其余（回头生克、旬空、反吟伏吟、用神两现计数） | 若干 | 引擎已算未产出的分类（旬空／反吟伏吟）或需计数语义 |
| 3 | `QM-P30` 时格「庚临时干三奇」／`QM-P26` 直使加地丁 | 各 1 | 原文两读不猜／需无取值子句（口径待裁定） |
| 4 | 八字透干类（`SANMINGTONGH-R-02`／`YUANHAIZIPIN-008`） | 2 | 需引擎产出**藏干**（本气/中气/余气），之后可用配对技术 |
| 5 | 六壬课体余项 / 紫微命名格局 / 3 条无据 statement | 2–4 / 4 / 3 | 沿用 t187／t183／t185 |
| 6 | 其余 | — | 需授权（引擎投入）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-liuyao-caiguan.py --dry-run     # 幂等
python3 tools/map-liuyao-caiguan.py
python3 tools/test-expressible-residue.py         # 28 条（两条财官已移出）

# 语义（含「配对真的在起作用」的合成盘）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("divination/huozhu-lin",None)}
d=json.load(open("tools/reports/facts-sample.json"))["liuyao"]
for case,c in d.items():
    print(case, {rid: ev.evaluate(rules[rid], c["facts"])["verdict"] for rid in ("HZL-R002","HZL-R004","HZL-R005")})
def f(k,v,**sc): return {"key":k,"value":v,"scope":sc,"derivedFrom":["test"]}
print("合成 妻财持世 →", ev.evaluate(rules["HZL-R004"], [f("liuqin","妻财",layer="本命",yao=2), f("shiyao","二爻",layer="本命",yao=2)])["verdict"])
print("合成 父母持世 →", ev.evaluate(rules["HZL-R004"], [f("liuqin","父母",layer="本命",yao=2), f("shiyao","二爻",layer="本命",yao=2)])["verdict"])
PY

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

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`9999f38143eead9e78765759f31aea73a46d0777`**。
产品仓 `generated/liuyao.json` 已同步覆盖（27 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3545 passed / 0 failed**。

**给消费方的一条说明**：`HZL-R002`／`R005` 只有在**用神能确定**时才可判
（`liuyao_yongshen` 存在）；用神未定的盘上返回「**信息不足**」——
那是如实回答（本仓不把未定当已定），不是缺事实。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。