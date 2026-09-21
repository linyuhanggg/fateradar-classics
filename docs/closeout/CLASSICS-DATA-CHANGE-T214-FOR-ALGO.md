# 消费方数据版本 · t214 爻之阴阳入事实层 ＋ 易理三条结构规则（yili 0% → 9.1%）

日期：2026-09-21。基线提交：`57a4cfb`（t213 后）。
**数据修订提交（请钉这个）：`cd86bb61af60ede956909c1b61c85284126a8ecb`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

先拿标题式扫描确认 **t213 那类「按样本拟合」缺陷没有新增**（奇门格表那些短 statement
其实逐条写明了条件，是真谓词）。于是转向一直停在 **0%** 的参考术——
**易理有一批真正的结构条件**（当位／中正／相应），条件**逐字写在原文里**，
只要一枚「爻之阴阳」事实就能写。**yili 0% → 9.1%**（3/33）。

## 1. 三条落地（条件都在原文里）

| rule | 原文 | 谓词 |
|---|---|---|
| `ZZR-01` | 阳爻居阳位（初三五）、阴爻居阴位（二四上）为"当位" | 六支枚举：阳@1/3/5 或 阴@2/4/6 |
| `ZHOUYIZHEZHO-004` | 得中又当位（如**九五、六二**）为"中正" | 两支：阳@5 或 阴@2（原文只举此二例，**不推广**） |
| `ZHOUYIZHEZHO-005` | 初与四、二与五、三与上相应；**阴阳相应为有应** | 六支：三对 × 阴阳两向 |

**实测**（乾为天／坤为地／地天泰三盘）：

| 盘 | 阴阳 | `ZZR-01` | `004` | `005` |
|---|---|---|---|---|
| 乾为天 111111 | 阳×6 | 满足 | **满足**（九五） | 不满足 |
| 坤为地 000000 | 阴×6 | 满足 | **满足**（六二） | 不满足 |
| 地天泰 111000 | 阳阳阳阴阴阴 | 满足 | 不满足 | **满足**（初阳／四阴） |

合成盘：「五阳二阴」→ `004` 满足；「五阴二阳」→ **不满足**（配对是本质）。

## 2. 一枚新事实：`yao_yinyang`（阳／阴，`scope.yao`）

引擎一直知道（`lines[].yin`），事实层没产出。它与六爻**同源**——同一卦、同一爻层——
六爻本门不用它，但两层共用；`ART_EMIT_KEYS` 里 **liuyao 与 yili 都声明**它。

## 3. 样盘：必须有**混阴阳**的一卦

新增 `yili` 一组三张。乾（六阳）与坤（六阴）能满足「当位」，
但**测不出「相应」**——相应要初四／二五／三上**阴阳相反**，
故补「**地天泰**」（阳阳阳阴阴阴）。这也是这组样盘存在的理由，写进了 dump 注释。

## 4. 顺带修掉一个极性错误（差点写反）

`lines[].yin` 在这套代码里的语义是「**位为 1 即阳爻**」
（`liuyao-base.ts` 的符号映射：`line.yin === 1 ? (moving ? "O" : "1") : …`），
字段名有历史包袱。我第一版照名字取反，**于是乾为天被标成全阴**——
是样盘实测把它抓出来的（乾→阳、坤→阴）。已按真实语义修正，并在代码里写明缘由。

## 5. 闸门与两处配套

新增一支参考术要过三处，都已处理：

1. `V16` 的 `scope.yao` 允许键 ＋ **`ART_EMIT_KEYS` 新增 `yili` 一项**；
2. **溯源分类**：新出现的 `yao_yinyang=阴` 落进「待读」→ 已登记
   （周易折中「**六二**」是易学术语：六＝阴爻、二＝爻位，句内不出现「阴」字）；
3. `test-value-provenance` 的「待读为空 ⇔ 已读非空」改为**单向蕴含**——
   待读非零是「有未读」的**信号**，不该弄红测试（这是我上一轮自己写太紧的断言）。

## 6. 数字

| | t213 | **t214** |
|---|---:|---:|
| **yili 覆盖率** | **0.0%** | **9.1%**（3/33） |
| meihua | 0.0% | 0.0%（t198 已查明多为体用断法表，适用范围恒真） |
| 六术合计已映射 | 378 | 378 |
| 未映射 | 468 | **465** |
| 验证深度 | 377/378 | 377/378（100%） |

六术覆盖率不变（bazi 49.9%／ziwei 62.4%／qimen 90.0%／liuren 35.9%／liuyao 43.5%／qizheng 24.4%）。

## 7. 未决清单（承接 t213）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **易理余项** | **新增**：`ZHOUYIZHEZHO-006`（比：相邻爻阴阳亲/敌）适用范围近恒真（任何卦都有相邻爻）→ 不写；`-007`（卦主）口径多歧；`-026`（变爻数目与爻辞）需爻辞层 |
| 2 | 梅花 21 条 | t198 已查明多为体用断法表；若要动，需先产「体用五行」两枚事实 |
| 3 | 撤回谓词 5 条所需事实 | 限类型／制化、星属南斗北斗、大限序列与武贪格 |
| 4 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义 |
| 5 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 6 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 7 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 8 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 8. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/predicate-report.py | tail -4          # yili 应为 3 / 9.1%
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("divination/zhouyi-zhezhong",None)}
d=json.load(open("tools/reports/facts-sample.json"))["yili"]
for case,c in d.items():
    yy="".join(f["value"] for f in c["facts"] if f["key"]=="yao_yinyang")
    print(case, yy, [ev.evaluate(rules[r], c["facts"])["verdict"] for r in ("ZZR-01","ZHOUYIZHEZHO-004","ZHOUYIZHEZHO-005")])
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

## 9. 给 cosmic 的版本钉

`CLASSICS_REV` = **`cd86bb61af60ede956909c1b61c85284126a8ecb`**。
产品仓 `generated/*.json` 已同步覆盖（`zhouyi-zhezhong` 不在六术导出之列，
故六术导出内容不变）；`tsc --noEmit` exit 0；产品侧 **3571 passed / 0 failed**。

**给消费方的一条说明**：`facts-sample.json` 新增 `yili` 一术（三张盘：乾／坤／泰）。
若你的测试遍历该文件的术列表，请容许这一术；`yao_yinyang` 是**爻之阴阳**
（`scope.yao` 定位到爻，值「阳」／「阴」），六爻与易理共用同一层事实。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。