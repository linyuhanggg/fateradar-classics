# 消费方数据版本 · t218 收尾可执行层的「接不上字段」（满足 92→96、信息不足 10→6）

日期：2026-09-21。基线提交：`0a79b35`（t217 后）。
**本轮无规则/谓词数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`c5bba9be08c4080107a5a001a6e0b886ae34a558`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

可执行层「引用接不上 FactKey 的字段」由 **5 → 1**（只剩 `year.gan.doushu`），
「任何盘都判不了」由 **12 → 8**，「满足」由 **92 → 96**、「信息不足」由 **10 → 6**。
途中查出小六壬**两处并行 facts 构建**互相覆盖的真缺陷。

## 1. 小六壬：起课输入与吉类计数入事实层

执行层有 3 条记录引用 `xiaoliuren.hour.branch`／`.lunar.month`／`.count.good`，
这些值一直只存在于 `meta` **文本**里（「取数 月 X · 日 Y · 时 Z」「三宫标签计数 吉类 N」），
事实层没有对应键 → 永远接不上。

新增四键：`xiaoliuren_hour_zhi`、`xiaoliuren_lunar_month`、`xiaoliuren_lunar_day`、
`xiaoliuren_count_good`（0–3 闭值域）。

**顺带查出一个真缺陷**：小六壬有**两处并行的 facts 构建**——
`xiaoliuren-base.ts` 的 `buildXiaoliurenBase` 与 `xiaoliuren.ts` 的 `buildXiaoliuren`
（dump 与实际使用的是后者）。后者只建「宫神」三条，**把前者的产出盖掉了**。
两处已补齐，并在代码注释里注明重复、建议产品侧收敛为一处。

## 2. 日干五行入事实层（逐柱）

`gan_element`（`scope.pillar`，值域五行）——执行层 `day.gan.element` 要日柱那一枚。
与既有的 `gan`／`zhi`／`nayin` 同层，故一次性给四柱（不多不少）。

## 3. 补上 t215 漏接的一条字段（同类自查）

`meihua.ti.element`：t215 已经把 `meihua_ti_element` **产出来了**，却**漏了把字段接上**——
于是 `MHY-E-01` 仍判不了。本轮接上。
⇒ 记入流程项：**新产事实要同时在 `FIELD_MAP` 里接上对应字段**（与 t215 的
「新键要登记消费方标签」并列）。

## 4. 效果（跨盘口径）

| | t217 | **t218** |
|---|---:|---:|
| **满足** | 92 | **96** |
| 不满足 | 152 | 152 |
| **信息不足** | 10 | **6** |
| 未提供定义表 | 4 | 4 |
| **至少一张盘可判** | 246 | **250** |
| **任何盘都判不了** | 12 | **8** |
| **接不上 FactKey 的字段引用** | 5 | **1**（仅 `year.gan.doushu`） |

剩下 8 条判不了的构成：
4 条**语料无构成定义**（未定义的格局等）、3 条**事实键在任何样盘都不在场**
（其中 `ZPR-E-08` 需**关系层**：六合／三合／三会，属审计第 7 类）、1 条字段（`year.gan.doushu`）。

其余不变：`rescue=unimplemented` 30、带 `named_gaps` 31、**`verified=true` 0**、
`validate-executable.py` OK（15 包 / 258 条 / 579 来源跨度 / 42 具名缺口）。

## 5. 两处旧断言按标题收紧（不是放宽）

1. `tests/engine/xiaoliuren.test.ts`「产出**三条落宫事实**」原写「facts **总长** 3」，
   比标题更严（新事实不是落宫事实）→ 改为按标题核对：宫神事实恰好三条、
   四枚输入/计数事实在场、**且非宫神事实不得带 `palace` scope**（比原断言多钉一条）；
2. 词表的 `Record<FactKey, …>` 与 `ART_EMIT_KEYS` 老断言各拦下一次漏登记（本轮照旧）。

## 6. 未决清单（承接 t217）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **可执行层剩余 8 条** | **新增**：4 无构成定义、3 键不在场（含需关系层的 `ZPR-E-08`）、1 字段（`year.gan.doushu`） |
| 2 | **新产事实要同时接上 FIELD_MAP 字段** | **新增（流程项）**：t215 产了 `meihua_ti_element` 却漏接字段，本轮才发现 |
| 3 | 小六壬 facts 构建重复 | **新增（产品侧清理项）**：`xiaoliuren-base.ts` 与 `xiaoliuren.ts` 两处并行 |
| 4 | `liuyao.structure` 的正式定义 | t217 已落地代理键并归因；正式定义仍待人工裁定 |
| 5 | 梅花／易理余项 | 断法表（恒真）不写；`-016` 变卦所指有歧义；`-007` 卦主口径多歧；`-026` 需计数与爻辞层 |
| 6 | 撤回谓词 5 条所需事实 | 限类型／制化、星属南斗北斗、大限序列与武贪格 |
| 7 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 8 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 9 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 10 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/eval-executable.py --all                     # 期望 满足 96 / 信息不足 6
python3 tools/eval-executable.py --all --across | sed -n '5,12p'   # 可判 250 / 判不了 8
python3 -c "
import json;d=json.load(open('tools/reports/facts-sample.json'))
for c,v in d['xiaoliuren'].items():
    print(c, [(f['key'],f['value']) for f in v['facts'] if f['key']!='xiaoliuren_palace'])
print('日干五行:', [(f['scope']['pillar'],f['value']) for f in d['bazi']['caseA']['facts'] if f['key']=='gan_element'])"

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

## 8. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`c5bba9be08c4080107a5a001a6e0b886ae34a558`；`tsc --noEmit` exit 0；
产品侧 **3574 passed / 0 failed**。

**给消费方的三条说明**：

1. 事实层新增 5 键：`gan_element`（逐柱，`scope.pillar`）、
   `xiaoliuren_hour_zhi`／`_lunar_month`／`_lunar_day`／`_count_good`——均已在 `LABELS` 登记。
2. **小六壬的事实层现在带起课输入与吉类计数**（此前只有三条宫神）；
   宫神事实仍是三条，且只有它们带 `palace` scope。
3. **产品侧待清理**：小六壬存在两处并行的 facts 构建
   （`xiaoliuren-base.ts` 与 `xiaoliuren.ts`），本仓已让两边一致，建议收敛为一处。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。