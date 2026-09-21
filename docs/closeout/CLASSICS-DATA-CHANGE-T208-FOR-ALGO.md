# 消费方数据版本 · t208 宫地支入事实层＋4 条命名格局可求值；修掉定义求值器的恒真缺陷

日期：2026-09-21。基线提交：`2ce1bb0`（t207 后）。
**数据修订提交（请钉这个）：`8f349b2d29aaf2661ef545140ba03fe126703151`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

三件事：**宫地支**（`ziwei_palace_zhi`）入事实层 → **4 条命名格局记录可求值**
（t183 挂到现在的条目结清）；按引文写出这 4 条格局的展开；
以及**修掉 `eval_definition` 一个让或形定义「恒真」的缺陷**——这是本轮最重要的发现。

## 1. 宫地支与 4 条命名格局

引擎早已算（底座 `p.earthlyBranch` → `palaces[].branch`），事实层没产出。
`references/definitions/ziwei-geju.json`（t183 建）早就把 4 条的 `needs` 写成
「宫地支（`palaces.earthlyBranch`）——引擎已算（`p.earthlyBranch`），但事实层未产出」。
**本轮结清**：产出该键，并按各自**引文**逐字写展开（未增条件）。

| 格局 | 引文 | 展开（逐字转写） |
|---|---|---|
| 武曲守垣 | 「武守命卯宮是也，餘不是。」 | 武曲在命宫 且 命宫支卯 |
| 日出扶桑 | 「日在卯守命是也，守官祿宮亦然。」 | 太阳在**命宫或事业**且该宫支卯 |
| 月朗天门 | 「月落亥宮 月在亥守命是也」 | 太阴在命宫 且 命宫支亥 |
| 月生沧海 | 「月生滄海 月在子宮守田宅是也。」 | 太阴在田宅宫 且 该宫支子 |

**宫名对译**（写进 `expansion_note`）：原文作「官祿宮」，引擎宫名用「事业」——同一宫的通行异名。

## 2. 修掉一个「恒真」缺陷（本轮最重要）

`eval_definition` 原来**只读 `expansion["all_of"]`**。于是**或形（`any_of`）展开**
取到空 `clauses` → `missing=[]`、`bad=[]` → **直接判「满足」** ✗。
`日出扶桑` 正是或形：**修之前它对每一张盘都报满足**（假阳性）。

修法：

- **合取**：缺键→信息不足；有不成立→不满足；否则满足（原逻辑保留）；
- **析取**：任一支全 ok→满足；有分支缺键→信息不足；各支皆不成立→不满足；
- **展开形态不认识 → 信息不足，绝不默认成立**。

实测：

| 盘 | 结果 |
|---|---|
| 真实盘 caseA | 武曲守垣／日出扶桑／月朗天门／月生沧海 **均不满足** |
| 合成「日在命宫·卯」 | 日出扶桑 **满足**（第一支） |
| 合成「日在事业·卯」 | 日出扶桑 **满足**（第二支） |
| 合成「日在**夫妻**·卯」 | 日出扶桑 **不满足**（旧实现恒真） |

## 3. 可执行层三态

| | t205 | **t208** |
|---|---:|---:|
| 满足 | 72 | 72 |
| 不满足 | 148 | **152** |
| **信息不足** | 34 | **30** |
| 未提供定义表 | 4 | 4 |

即：**4 条命名格局记录不再卡在「未提供定义表／信息不足」**，可判三态。
（满足 73→72 的那一下，正是把 `日出扶桑` 的假阳性改回「不满足」。）
其余不变：`rescue=unimplemented` 30、带 `named_gaps` 31、**`verified=true` 0**，
`validate-executable.py` 仍 OK（15 包 / 258 条 / 579 来源跨度 / 42 具名缺口）。

## 4. 测试

`test-definition-table.py`：

- 更新现状（`evaluable` **5** 条＝君臣庆会 + 上述四条；`needs-fact` **3** 条＝
  金灿光辉／贪火相逢／日月夹财）；
- **补回归**：或形两支各自成立、**非支不成立**、**未知形态不得默认成立**；
- 原先用「武曲守垣」演示「有定义但缺事实」的断言已失效（它现在有展开），
  改用仍缺事实的「金灿光辉」；并新增「展开已写但本盘缺键 → **信息不足**」。

## 5. 未决清单（承接 t207）

| # | 事项 | 状态 |
|---|---|---|
| 1 | 计数语义（独发／独静／用神两现） | t207 定性：**唯一有真实需求的语言缺口**，约 2–3 条 |
| 2 | `金灿光辉`／`贪火相逢`／`日月夹财` 3 条格局 | 分别缺「单守」判定／星曜亮度（t180 已婉拒）／「夹」关系层 |
| 3 | `谹弼夹帝`／`禄马同宫`／`魁命钺身` | 语料无构成定义（t183 已登记，**不编造**） |
| 4 | `TAIWEIFU-010`「魁钺同行」 | 三种读法待人裁定（t206） |
| 5 | `liuyao.structure` 17 条 | 两仓无定义 |
| 6 | `yongshen.zhi` 2 条 | 跨键配对，映射表表达不了 |
| 7 | 跨键关系 7–9 条 | 建议改由引擎产判定名 |
| 8 | 派生判定数十条 | 引擎投入 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/eval-executable.py --all                 # 信息不足应降到 30
python3 tools/test-definition-table.py                 # 含或形与未知形态回归
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ex","tools/eval-executable.py"); ex=importlib.util.module_from_spec(spec); sys.modules["ex"]=ex; spec.loader.exec_module(ex)
caseA=json.load(open("tools/reports/facts-sample.json"))["ziwei"]["caseA"]["facts"]
present={x["key"] for x in caseA}
for n in ("武曲守垣","日出扶桑","月朗天门","月生沧海"): print(n, ex.eval_definition(n, caseA, present)[0])
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
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

`CLASSICS_REV` = **`8f349b2d29aaf2661ef545140ba03fe126703151`**。
产品仓 `generated/*.json` 已同步覆盖；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变
（bazi 49.9%／ziwei 67.7%／qimen 90.0%／liuren 35.9%／liuyao 40.6%／qizheng 24.4%）。

**给消费方的一条提醒**：`ziwei_palace_zhi` 是**宫的地支**（与 `ziwei_palace` 的宫名同 scope：
`{layer: 本命, palace: 宫名}`，另有 `身宫` 别名宫）。它与 bazi/qimen/liuren 的 `zhi`
（`scope.pillar`）语义不同——按 key 聚合时请连 scope 一起看。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。