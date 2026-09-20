# 消费方数据版本 · t176 具名固定取值 4 条 + 六壬课传位置接线

日期：2026-09-21。基线提交：`1f2b03c`（t175 后）。
**数据修订提交（请钉这个）：`68c35c771ea8c8d5a66210461fc577d2f4ae0025`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

本轮三件事，都不新增事实、不新增语法、不用通配：

1. **四柱枚举干支对**（魁罡日／八专日）——用**显式柱位 scope** 表达「某柱＝列举之一」；
2. **具名纳音**（论海中金）——t170 产出的 `nayin` 事实**此前无任何谓词使用**，本条是第一个；
3. **六壬课传位置接线**——关掉了引擎自带的接线提示 `LR-UNKNOWN-MIBEN-021-WIRE`。

覆盖率：bazi **48.8% → 49.4%**（219→222），liuren **20.8% → 22.6%**（11→12），
未映射 **497 → 493**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | **222** | **49.4%** | 7.2% | 9 → **10** |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 24 | 60.0% | 4.2% | 6 |
| liuren | 11 (20.8%) | 11 (20.8%) | **12** | **22.6%** | 8.3% | 3 → **5** |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 | 30.4% | 14.3% | 5 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **493**。未新增任何 `value: "*"`；三道谓词门禁 PASS；4 大门禁全绿；
**26** 个 `tools/test-*.py` 全绿；`coverage-report --fail-under 54` PASS；
本轮新映射**无一命中零区分度 hard 档**（bazi 17／liuren 3 均为既有）。

## 2. 三种形态与写法理由

### 2.1 四柱枚举干支对：用显式柱位，**不能用 `same`**

原文「庚辰、庚戌、壬辰、戊戌为魁罡日」的条件是**日柱**等于列举之一：

```yaml
applicable_to: {any_of: [{all_of: [{key: gan, value: 庚, scope: {pillar: day}},
                                    {key: zhi, value: 辰, scope: {pillar: day}}]}, …]}
```

两句都钉在 `pillar: day` → 「日柱＝庚辰」；组间 `any_of` → 「日柱是列举之一」。

**为什么不能用 `same: pillar`**：`same` 把该 `all_of` 内**所有**受约束子句绑到**同一个**取值，
而这里每个候选对是**独立的一组**（魁罡的 4 对互为或关系）。写成
`all_of[庚,辰,庚,戌,壬,辰,戊,戌] + same: pillar` 会要求「四对同时成立在同一柱」——不可能。

落地：`R-06` 魁罡日（4 对）、`SANMINGTONGH-097` 八专日（8 对）。

### 2.2 具名纳音

`SANMINGTONGH-004`「论海中金须配合所见火、水、木、土等条件」→ `[{key: nayin, value: 海中金}]`。

单谓词用**平铺列表**形。初版我误写成 `{nayin: 海中金}`——那既不是谓词也不是 v3 组，
被 **V16** 以「未知组字段 / any_of 必须恰好有一个」当场拦下（这一步很值：
它证明门禁对作者笔误有效）。已修，并在工具注释里写明这个坑。

### 2.3 六壬课传位置：关掉引擎自带的接线提示

`LIURENMIBEN-021`「参看传中是否见财，以及青龙是否居日上」→

```yaml
applicable_to: [{key: tianjiang, value: 青龙, scope: {palace: 日上}},
                {key: liuqin, value: 妻财, scope: {palace: 初传}}, …中传…, …末传…]
```

平铺列表＝或（两分支二选一）。这条同时需要两处放开：

- **V15 原本只放 ziwei（十二宫）与七政（宫位）写 `scope.palace`**。六壬的「位置」不是宫，
  而是**课传位置**（日上／辰上／初传／中传／末传）。本轮加六壬分支，取值即这五个。
  `reverse14` 钉住「非法位置必红、合法必绿」。
- **`ART_EMIT_KEYS[liuren]` 补 `liuqin`**：盘面样本实测三传六亲早已产出
  （`scope.palace=初传/中传/末传`），只是没登记进表——不补就会 `--check-art-keys` 红。

引擎侧早就就绪：`liuren.ts` 的 `pushScoped` 一直在发 `tianjiang`＋位置，
并且自带一条 unknown 记录 `LR-UNKNOWN-MIBEN-021-WIRE` 写着
「引擎已能发出 palace=日上 的天将事实；规则 applicableTo 仍为空」。**本条就是那次接线。**

## 3. 端到端验收（最有说服力的一条）

| 盘 | 天将（位置级） | 三传六亲 | 本条结论 |
|---|---|---|---|
| caseA | 白虎@日上、天空@辰上 | 官鬼/父母/父母 | 不满足 |
| caseC | 腾蛇@日上、太阴@辰上 | 子孙/**妻财@中传**/官鬼 | **满足** |
| caseE | 六合@日上、白虎@辰上 | **妻财@初传**/兄弟/官鬼 | **满足** |
| **caseF** | 太常@日上、勾陈@辰上、**青龙@初传** | 官鬼/父母/兄弟 | **不满足** |
| **caseG** | **青龙@日上**、腾蛇@辰上 | **妻财@初传**/子孙/兄弟 | **满足**（两分支各命中一次） |

**caseF 是本轮最有价值的一条**：它盘上**有青龙，但在初传、不在日上** → 本条**不满足**。
这正是原文那句「**青龙在任意一传不等于龙居日本**」被 `scope.palace` 区分开——
若当初只写 `{tianjiang: 青龙}`（无 scope），caseF 会被误判为满足。

八专日同样逐支可辨：日柱`己巳`**不成立**、`己未`**成立**（列的是己未，差一支）。

三条边界断言（已入测试）：缺柱位事实 → 信息不足；只有 `tianjiang` 而 `liuqin` 整个缺席 →
**信息不足**（不能排除「传中见财」，不得当成不满足）；应有尽有而条件为假 → 不满足。

## 4. 一个口径说明（免得被当成算错）

`predicate-report.py` 的 liuren 有谓词 **12** 条，而产品仓 `generated/liuren.json` 只有 **11** 条带谓词。
差的是 `DALIURENDAQU-006`——它是 `kind: procedure`，导出到 `dist/procedures/`
（按导出器约定「procedure → tests only」），产品检索池不含。**不是漏导出。**

## 5. 本轮顺手查过、但没有采纳的

- **十恶大败日／探病忌日**（`JR-08`／`JR-12`）等：形态与魁罡日同构，但属**择日**书目，不在六个产品术内。
- **旬中六甲全见**（`YUZHAOSHENYI-042`）：四柱只有四柱，装不下六甲；且「全见」的结构未明 —— 不映射。
- **四位纯全／一气生成**（`SANMINGTONGH-100`）：「四柱地支**顺连**如寅卯辰巳」含**次序**语义，
  而 `all_of` 是无序的「三支齐」→ 写成 all_of 会**放宽**（任何排列都算），属**超集**，禁止。
- **R-09 十干喜忌支位**：把 10 个天干全枚举 → 穷尽 `rizhu` 值域＝恒真零区分度，
  与 t168 撤回 `DITIANSUICHA-DR-07` 同一理由 —— 不映射。
- **自刑**（`YUZHAOSHENYI-026`）：需**同一支出现两次**，而 `all_of` 两句相同 `{zhi: 辰}`
  会被**同一个事实**同时满足 → 假阳。v3 的表达力边界，登记待议（t175 已记）。

## 6. 未决清单（承接 t169–t175）

1. **v3 边界：同值异位**（§5 自刑）——需「两子句须由不同事实满足」或「同字段不同取值」语义。
2. **15% 通配闸门挡住 4 条奇门规则**：事实已齐，但只能写 `{all_of:[{zhifu,"*"},…]}`
   → qimen 会到 17.9%。**未放宽、未挑 2 条凑数**；需二选一授权。
3. **六爻爻支事实**：一加即可复用 t175 的成组写法（六合／六冲）与本节的自刑问题。
4. **神煞 30 条**需扩取法表；**梅花 21 条**本仓无事实层（产品已有 `meihua_gua`，两处词表仍漂移）；
   **柱干支 30 条**余下多为跨键取值相等（如「庚临岁干」）——v3 的 `same` 只绑 scope 字段、
   不绑取值，属语言或事实的设计问题。
5. **`liuyao.structure`（executable 17 条）**是打包名、无单一 FactKey 对应，需古籍侧拆声明。
6. t169–t174 其余：`daxian`/`liunian_taisui`、ziwei 11 条命名格局缺定义表、
   `fold_han` 不处理古异体字、189 条重述是否换真引文、V11 111 vs G1 <50、
   25 条既有结构恒真映射、3 条无据 statement。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本批映射（幂等：已落实的会跳过，已有**不同**谓词才报错）
python3 tools/map-fixed-values.py --dry-run
python3 tools/map-fixed-values.py
python3 tools/test-map-fixed-values.py       # 形态 + 语义（含「任意一传≠居日上」）

# 六壬 scope.palace 门禁反例
python3 tools/test-validate-gates.py         # reverse14：非法位置红／合法绿

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 三态求值
python3 tools/eval-predicates.py --art liuren --case caseF -v | grep -A2 "LIURENMIBEN-021"
python3 tools/eval-predicates.py --art liuren --case caseG -v | grep -A2 "LIURENMIBEN-021"
python3 tools/eval-predicates.py --art bazi --case caseA -v | grep -A2 "SANMINGTONGH-097"
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`68c35c771ea8c8d5a66210461fc577d2f4ae0025`**。
产品仓 `generated/*.json` 已同步覆盖（bazi 222 条带谓词、liuren 11 条 doctrine）；
`tsc --noEmit` exit 0；相关 6 个测试文件 **49 项全绿**（含 `liuren-boundary-unknowns`）。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。