# 谓词语言 v3（复合条件 / 嵌套 / 多事实联合 / 同位置绑定）

版本：`fateradar-rules-v3`。**向后兼容** `fateradar-rules-v2`：旧的平铺列表原样仍然合法，
语义一字不改。本文件是古籍仓、校验器与消费方（product 仓 `matcher.ts`）的共同契约。

## 1. 为什么要升（问题不是覆盖率）

旧 `applicable_to` 是一个平铺列表，消费方 `matchRules` 的判据是：

```ts
const matched = rule.applicableTo.filter((pred) => facts.some((f) => factMatches(f, pred)));
if (matched.length === 0) continue;
```

`filter` + `some` ⇒ **列表是「或」（任一谓词命中即命中），且每条谓词只看单个事实**。
于是旧语言**结构上无法表达**：

| 缺的表达力 | 例子（原文） | 旧语言为何不行 |
|---|---|---|
| 多事实联合（AND） | 神遁「休门与乙奇合九天」 | 平铺列表是 OR；`休门` 与 `九天` 各命中一次就成立 |
| 嵌套（OR-of-AND） | 六仪受制「休加离／伤加坤／杜加艮…」 | 无法表达「(休门 且 离宫) 或 (伤门 且 坤宫)」 |
| 同位置绑定 | 「禄存与天马同会」 | 无法要求两个事实落在**同一**宫 |
| 排除（NOT） | 「不见空亡」「不被冲克」 | 无否定子句 |
| 位置限定 | 奇门宫位、六爻爻位、八字柱位 | `scope` 只允许 `layer`/`palace` |

`needs` 的结论：**不是缺事实，是谓词语言的表达力不够**。
本文只在原文确有该结构时启用新语法，不拿它凑覆盖率。

## 2. 语法

```
applicable_to := predicate_list | group

predicate_list := [ predicate, ... ]          # 旧形；等价于 any_of，语义不变
group          := { any_of: [clause, ...] }   # 或
                | { all_of: [clause, ...] }   # 且
                ── 二者必居其一
                + 可选 none_of: [clause, ...] # 排除，与上面整体再相「与」
                + all_of 可带 same: <scope字段>

clause    := predicate | group                # 允许嵌套
predicate := { key: <FactKey>, value: <str>, scope?: {...} }
```

`scope` 允许字段（全部可选，多个字段之间是「与」）：

| 字段 | 取值 | 适用范围 | 事实侧依据 |
|---|---|---|---|
| `layer` | `本命`/`大运`/`流年`/`流月`/`流日` | 全部 | `Fact.scope.layer` |
| `pillar` | `year`/`month`/`day`/`time` | 全部 | `Fact.scope.pillar`（八字 shishen/shensha/rizhu/yueling 已带） |
| `palace` | 紫微十二宫＋身宫；七政十二宫位名 | ziwei / qizheng | `Fact.scope.palace` |
| `gong` | 整数 1–9 | qimen | `Fact.scope.gong`（奇门九宫） |
| `yao` | 整数 1–6 | liuyao | `Fact.scope.yao`（爻位） |

`value` 仍可用通配 `"*"`（匹配该 key 任意取值），但**禁止用 `*` 凑覆盖率**（`--max-wildcard 15` 门禁仍在）。

## 3. 语义（消费方必须逐条实现）

设 `facts` 为盘面事实数组。

- `predicate.matches(facts)`：存在 `f` 使 `key`/`value` 相同、且 `scope` 各字段（若给出）与 `f.scope` 相等。
- `group.matches(facts)`：`any_of`＝任一子句成立；`all_of`＝全部子句成立。
- `group.none_of`：对每个子句求「是否存在匹配事实」，**任一存在即整组为假**。
  注意 `none_of` 判的是「事实存在与否」，不是子句布尔值。
- `same: f`（仅 `all_of`）：该 `all_of` 内**命中事实携带字段 `f` 的子句**必须能绑定到同一个 `f` 值
  （同宫／同柱／同爻）。**绑定看的是命中事实携带的字段值，不是谓词自己写没写 `scope`**——
  否则「禄存与天马同会」这种两个谓词都不写 `palace` 的情形就绑不起来，而它正是 `same` 的用途。
  命中事实不带 `f` 的子句不受约束（自由）。若这些子句在 `f` 上无公共取值，则该 `all_of` 为假。
  该字段在本盘缺失（子句全为 `unknown`）时，仍按上文「信息不足」处理。
- 顶层旧形 `predicate_list`：等价 `{any_of: [...]}`。

### 三态与「信息不足」

`applicable_to` 求值返回三态，**不得**把缺输入当不满足：

- `满足`：表达式为真。
- `不满足`：表达式为假，**且**该规则声明了不满足分支（`fail_when` 非空）——本仓 rules.yaml 不承载
  `fail_when`，故 rules.yaml 侧只用「命中／未命中」，三态由 executable 包与产品侧给出。
- `信息不足`：表达式所需的某个 FactKey 在 `facts` 中**完全不存在**（引擎未产出该事实，
  或该盘未提供）。此时不得输出「不满足」。

`none_of` 是例外且必须写清：它判「事实不存在」。若 `none_of` 涉及的 key 在盘面**完全缺失**，
结论是 `信息不足`（无法证明「没有」），不是「满足」。

## 4. 校验（V16）

`python3 tools/validate-rules.py` 的 V16 门禁：

1. 顶层是 mapping 时，`any_of`/`all_of` **恰好一个**；未知键报错。
2. `any_of`/`all_of`/`none_of` 为非空列表；元素为 predicate 或嵌套 group。
3. `same` 只能出现在 `all_of` 内，取值 ∈ `{layer, pillar, palace, gong, yao}`。
4. 每个 predicate 递归按旧判据校验（V2 结构、V7 FactKey 与取值域）。
5. `scope.gong` 仅 qimen、整数 1–9；`scope.yao` 仅 liuyao、整数 1–6；
   `scope.palace` 仅 ziwei（取值须在 `ziwei_palace`）与 qizheng（取值须在 `gongwei`）；
   `scope.pillar` ∈ `{year,month,day,time}`；`scope.layer` ∈ 五个层名。
6. 嵌套深度上限 4，防止无限递归。

## 5. 不变量

- 本语言**不改变**任何规则的 `statement` / `quote` / `anchor` / `verified`。
- 升语言**不等于**升覆盖率：能写出谓词的规则才写；写不出的保持 `[]` 并登记原因。
- `verified` 仍恒为 `false`。