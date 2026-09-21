# 消费方数据版本 · t215 梅花体用五行（meihua 0% → 3.0%）＋ 补齐消费方标签表（21 键）

日期：2026-09-21。基线提交：`30af3e4`（t214 后）。
**数据修订提交（请钉这个）：`c5bba9be08c4080107a5a001a6e0b886ae34a558`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

三件事：把**第二个参考术（梅花）也推离 0%**（0% → 3.0%）；
把 V15 的 `scope.palace` 例外扩到梅花；以及——**本轮最该记的一条**——
查出**我自 t184 起新增的 26 个键里，21 个没登记消费方标签**，
于是它们在追问取证里一直显示成「盘面：值」**瞒了十轮**。

## 1. 梅花：体用五行入事实层

引擎一直在算体／用五行（`ti.element`／`yong.element`），事实层没产出。
新增 `meihua_ti_element`／`meihua_yong_element`（`scope.palace` 为**卦角色**：本卦／互卦／变卦），
据此落地 **`MEIHUAYISHU-013`**「体用同五行（如皆木皆金）为比和」——
条件＝**本卦**那一对的五行相同（木木/火火/土土/金金/水水 五支枚举）。

**实测两盘恰好一正一反**：

| 盘 | 本卦体 | 本卦用 | `013` |
|---|---|---|---|
| caseA | 水 | 水 | **满足**（比和） |
| caseB | 水 | 木 | 不满足 |

合成盘「体金用金，但只在**互卦**」→ **不满足**（证明 `scope.palace` 限定本卦确实在起作用）。

**如实说明天花板**：梅花其余规则多为**体用断法表**（五种关系各给断语 ⇒ 适用范围恒真，
写成谓词就是凑数）——与 t198 的判断一致。本门可写的就是「比和」这一条；
`MEIHUAYISHU-016`（变卦克体／生体）因「**变卦**指哪一卦」有歧义，**不猜**。

## 2. V15 的 `scope.palace` 例外扩到梅花（与六壬同理）

引擎一直按**角色**给梅花事实加 `scope.palace`，而 V15 只允许 ziwei／xingming／六壬写它
→ 谓词就写不出「只看本卦那一对」（会串到互/变）。已扩为第四类例外，
取值限定三角色，并把报错文案改全。
这与 2026-09 给六壬加「课传位置」例外是**同一情形**：引擎产得出，谓词就该引得着。

## 3. **补齐消费方标签表：21 个键此前会退化成「盘面：」**

产品侧 `tests/chat/chat.test.ts` 报红：

> 「meihua/xiaoliuren 的追问取证里出现了 `盘面：`」

查下去是 `context.server.ts` 的 `LABELS` 表——**我自 t184 起新增的 26 个键里，21 个没登记标签**：

```
nayin, canggan, gan, zhi, yao_zhi, bian_yao_zhi, liuyao_seq, yao_yinyang,
liuyao_yongshen(+_zhi/_state), liuyao_month_strength, liuyao_activity, liuyao_kong,
liuyao_progression, liuyao_tomb, liuyao_reversal,
liuren_ke, liuren_ke_relation, liuren_ke_completeness, liuren_yaoke, liuren_shehai,
qizheng_ascendant, meihua_ti_element, meihua_yong_element
```

它们全部退化成 `盘面：值`。而那条测试只覆盖 `meihua`／`xiaoliuren`，所以**瞒了十轮**——
直到本轮新增梅花两键才撞上。

**已全部登记**，并把这件事写成交付清单的一项：
**经典侧新增 FactKey 时，必须同步登记消费方标签**（否则消费方的取证显示会退化）。

另一处产品测试 `tests/engine/meihua.test.ts`「卦上只带体用，不带六亲世应等**纳甲**结构」
原断言写成「facts 只允许 `meihua_gua`」，**比标题更严**——
而体用五行正是标题说的「体用」。已按标题本意收紧：
允许 卦 与 体／用，但**不得**出现纳甲类结构（六亲／世应／爻支／六神／伏神／动爻）。

## 4. yili 余项扫过（无新增）

30 条未映射里 **26 条是 `not-a-condition`**（易理体例／生成论／哲学），
3 条 `fact-not-emitted`（比／卦主／变爻数目与爻辞），1 条 vague——
与 t214 判断一致，**没有新增可写项**。

## 5. 数字

| | t214 | **t215** |
|---|---:|---:|
| **meihua 覆盖率** | 0.0% | **3.0%**（1/33） |
| yili | 9.1% | 9.1%（3/33） |
| 六术合计已映射 | 378 | 378 |
| 未映射 | 465 | **464** |
| 验证深度 | 377/378 | 377/378（100%） |
| 溯源：字面／枚举／已读／引擎态／**待读** | 816/477/35/37/**0** | **820/483/36/37/0** |

六术覆盖率不变（bazi 49.9%／ziwei 62.4%／qimen 90.0%／liuren 35.9%／liuyao 43.5%／qizheng 24.4%）。

## 6. 未决清单（承接 t214）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **新增 FactKey 必须同步登记消费方标签** | **新增（流程项）**：本轮之前漏了 21 个，退化成「盘面：」 |
| 2 | 梅花余项 | 断法表（恒真）不写；`-016` 变卦所指有歧义，需人判 |
| 3 | 易理余项 | 26 条 not-a-condition；`-007` 卦主口径多歧、`-026` 需计数与爻辞层 |
| 4 | 撤回谓词 5 条所需事实 | 限类型／制化、星属南斗北斗、大限序列与武贪格 |
| 5 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义 |
| 6 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 7 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/predicate-report.py | tail -3      # meihua 1 / 3.0%、yili 3 / 9.1%
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("divination/meihua-yishu",None)}
d=json.load(open("tools/reports/facts-sample.json"))["meihua"]
for case,c in d.items():
    ti=[f["value"] for f in c["facts"] if f["key"]=="meihua_ti_element" and f["scope"]["palace"]=="本卦"]
    yo=[f["value"] for f in c["facts"] if f["key"]=="meihua_yong_element" and f["scope"]["palace"]=="本卦"]
    print(case, "体", ti, "用", yo, ev.evaluate(rules["MEIHUAYISHU-013"], c["facts"])["verdict"])
PY

# 消费方标签表（新键必须都在）
cd /Users/sync/code/cosmic-fortune-lab
python3 -c "
import re,pathlib
s=pathlib.Path('src/lib/chat/context.server.ts').read_text()
m=re.search(r'const LABELS[^=]*=\s*\{(.*?)\n\};', s, re.S)
keys=set(re.findall(r'^\s*\"?([a-z_]+)\"?\s*:', m.group(1), re.M))
import json
v=json.load(open('src/lib/engine/facts/fact-vocab.json'))
missing=[k for k in v['keys'] if k not in keys]
print('词表里没有标签的键:', missing)"
npx vitest run tests/chat tests/engine/meihua.test.ts

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
python3 tools/audit-contract.py
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`c5bba9be08c4080107a5a001a6e0b886ae34a558`**。
产品仓 `generated/*.json` 已同步（六术导出内容不变——梅花不在六术导出之列）；
`tsc --noEmit` exit 0；产品侧 **3571 passed / 0 failed**。

**给消费方的两条说明**：

1. `facts-sample.json` 新增 `meihua` 一术（两张盘）。梅花的体／用五行是
   `meihua_ti_element`／`meihua_yong_element`，**按卦角色**（`scope.palace`：本卦／互卦／变卦）
   区分——判「体用关系」时请限定 `本卦`。
2. **如果你在消费侧展示这些事实**：本次补齐了 21 个键的中文标签
   （`context.server.ts` 的 `LABELS`），此前它们会显示成「盘面：值」。
   若你另有自己的标签表，请一并对齐 `fact-vocab.json` 的键列表。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。