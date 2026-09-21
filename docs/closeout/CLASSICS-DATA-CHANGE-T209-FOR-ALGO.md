# 消费方数据版本 · t209 六爻化进退与墓位入事实层（liuyao 40.6% → 43.5%）

日期：2026-09-21。基线提交：`964c2ee`（t208 后）。
**数据修订提交（请钉这个）：`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

六爻的两枚**具名状态**（化进/退神、墓位）入事实层，据此落地 **2 条**规则：
**liuyao 40.6% → 43.5%**（28 → 30）。
另外**自纠了一处配对错误**（我把用神取值写死成「官鬼」），本轮该记的一条。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 224 | 49.9% | 7.1% | 11 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 19 | 35.9% | 5.3% | 10 |
| **liuyao** | 21 (30.4%) | 21 (30.4%) | **30** | **43.5%** | **10.0%** | 10 → **12** |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **465 → 463**。4 大门禁全绿；**37** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用 0；取值域 0；
验证深度 **382/383 = 100%**；`coverage-report --fail-under 54` PASS；
产品侧 **3571 passed / 0 failed**，`tsc` exit 0。

## 2. 两枚具名状态（仍是「引擎已算、事实层没产出」）

| 新键 | 取值 | 来源 | **产出条件** |
|---|---|---|---|
| `liuyao_progression` | 进神／退神 | `state.progression` | **仅 `status==="satisfied"`** |
| `liuyao_tomb` | 入日墓／入动墓／入变墓 | `state.lifecycle.tombs` | **仅 `opened === false`** |

两条限定都不是我加的，是引擎自己的判据：

- 引擎另有一条分支——「**退神支对但近事动变都旺，按原文得时暂不退**」→ 未定就不产出，
  不把未定当已定（与 t193 用神、t197 旬空同一条纪律）；
- 墓位 `opened` 表示**已被冲开**，冲开的不算困 → 只取未冲开的；
  并按 `kind`（day／moving／changed）分来处，因为原文「用神入**日辰**之墓」要看 day。

## 3. 落地两条

**`ZENGSHANBUYI-020`** 「化进神（如寅化卯）力增、化退神（如卯化寅）力减；进神逢冲不进、退神逢冲不退」
→ `{any_of: [{liuyao_progression: 进神}, {liuyao_progression: 退神}]}`（后者属断法细则，未表达）。

**`ZENGSHANBUYI-031`** 「用神动随官鬼入墓——大凶；**用神入日辰之墓**亦凶」
→ 写后一支：用神所在之爻入日辰之墓，**5 六亲 × 6 爻** 枚举配对（与 t197 用神旬空同形）。
前一支「用神随官鬼入墓」是**两爻关系**，谓词层不写（见表达力审计第 7 类）。

**实测**：

| 盘 | 事实 | `020` | `031` |
|---|---|---|---|
| cov4_liuyao_1 | 有退神 | **满足** | 不满足 |
| cov4_liuyao_2 | 用神（妻财）那一爻入日墓 | 信息不足 | **满足** |
| cov2_liuyao_1 | 入日墓落在父母爻 | 信息不足 | 不满足 |
| 无进退事实的盘 | — | **信息不足**（缺席即未定） | — |

## 4. **自纠一处配对错误**（本轮该记的一条）

031 初版我把用神取值**写死成「官鬼」** —— 那是照原文措辞
（「用神动随**官鬼**入墓」）抄下来的，**是错的**：用神随盘而定
（求财＝妻财、求官＝官鬼、问文书＝父母…），必须**枚举五种六亲并与 `liuyao_yongshen` 配对**。

**发现方式**：验证深度报告把 031 标成「从未被任何样盘满足」→ 顺着去查 → 才看到写死的问题。
修后在样盘上可满足。

> 若没那一步核验，这条会带着一个**在任何非官鬼用神的盘上都恒不满足**的谓词上线。
> 这正是「覆盖率之外还要有验证深度」的价值。

## 5. 样盘

新增两张六爻盘（`cov4_liuyao_1/2`，遍历卦与动爻找出）：一张有**化退神**、
一张有**用神所在爻入日墓** —— 否则这两条规则无从演示。

## 6. 未决清单（承接 t208）

| # | 事项 | 状态 |
|---|---|---|
| 1 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口，约 2–3 条 |
| 2 | 六爻「用神随官鬼入墓」这类**两爻关系** | 表达力审计第 7 类（可写但会爆炸）；建议由引擎产判定名 |
| 3 | `ZENGSHANBUYI-007`（用神两现） | 需「配对 + 计数」，比纯计数更难 |
| 4 | `TAIWEIFU-010`「魁钺同行」／3 条格局／`liuyao.structure` 17 条／`yongshen.zhi` 2 条 | 沿用 t206／t208 |
| 5 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 6 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/verification-depth-report.py            # 期望 382/383（100%）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
d=json.load(open("tools/reports/facts-sample.json"))["liuyao"]
rules={r["rule_id"]:r for r in ev.load_rules("divination/zengshan-buyi",None)}
for case,c in d.items():
    tom=[f["value"] for f in c["facts"] if f["key"]=="liuyao_tomb"]
    pro=[f["value"] for f in c["facts"] if f["key"]=="liuyao_progression"]
    if tom or pro:
        print(case, "进退", pro, "墓", sorted(set(tom)),
              ev.evaluate(rules["ZENGSHANBUYI-020"], c["facts"])["verdict"],
              ev.evaluate(rules["ZENGSHANBUYI-031"], c["facts"])["verdict"])
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
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`**。
产品仓 `generated/liuyao.json` 已同步覆盖（30 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。

**给消费方的两条说明**：

1. `liuyao_progression` **只在引擎判定成立时出现**（缺席 = 未定或非进退，不是「不成立」）；
   `liuyao_tomb` **只在墓位未冲开时出现**。二者都按 `scope.yao` 定位到爻。
2. 若产品侧要展示「进神/退神」，请按这两个键的存在性判，不要用「不出现即为退神」反推。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。