# 消费方数据版本 · t175 地支成组规则 9 条（全部用 t168 的 v3 语言，零新事实）

日期：2026-09-21。基线提交：`89b758a`（t174 后）。
**数据修订提交（请钉这个）：`3b4aa5368730d5df47f6bb631ba4aa83736fb148`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

本轮验证了 **t168 那次语言升级确实在付息**。

「三合局／方局／六冲」这类规则的适用条件是「**某几个地支同时出现在四柱里**」，
而 **v3 本来就写得出来**，不需要任何新语法、新 FactKey 或新关系算子：

```yaml
applicable_to: {any_of: [{all_of: [{key: zhi, value: 申}, {key: zhi, value: 子}, {key: zhi, value: 辰}]}, …]}
```

`all_of` 三句各要一个 `zhi` 事实匹配 → 「三支齐」；组间 `any_of` → 「任一局成」。
**不加 `same`**：三合／方局要的正是三支**分布在不同柱**上，绑柱位反而错。
地支事实由 t170 的逐柱 `zhi` 提供。**不新增 FactKey、不动闸门、不用通配。**

落地 **9 条**，bazi 谓词覆盖 **47.0% → 48.8%**，未映射 **505 → 497**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 |
|---|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | **219** | **48.8%** | 7.3% |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% |
| qimen | 7 (17.5%) | 24 (60.0%) | 24 | 60.0% | 4.2% |
| liuren | 11 (20.8%) | 11 (20.8%) | 11 | 20.8% | 9.1% |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 | 30.4% | 14.3% |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% |

- 未映射：**505 → 497**（−8）。**9 条映射里 8 条在门禁分母内**——
  `SANMINGTONGH-018` 是 `anchor: null`，从来不在「有锚且谓词为空」的口径里（§3）。
- **未新增任何 `value: "*"`**；通配占比 7.6%→7.3%（分母变大）。三道谓词门禁 PASS。
- 4 大门禁全绿；24 个 `tools/test-*.py` 全绿；`coverage-report --fail-under 54` PASS。
- 本轮新映射**无一命中零区分度 hard 档**（hard 总数仍是既有 17 条）。

## 2. 9 条落地明细（逐条带 statement 复核片段）

工具 `tools/map-branch-groups.py`：判据必须命中 statement 才落盘（不命中直接 FAIL）。

| rule_id | 原文条件 | 谓词 |
|---|---|---|
| `SANMINGTONGH-015` | 申子辰、巳酉丑、寅午戌、亥卯未为三合组合；**三字缺一不能**直接按三合化局论 | 4 个 `all_of` 三支组的 `any_of` |
| `LIXUZHONGMIN-070` | 寅午戌火体、亥卯未木体、申子辰水体、巳酉丑金体 | 同上（4 组） |
| `YUZHAOSHENYI-040` | 五行三合局齐者（木亥卯未／火寅午戌／金巳酉丑／水申子辰） | 同上（4 组） |
| `DITIANSUICHA-DR-02` | 三合局成局者气势全；**方局**齐全者气势纯 | 三合 4 组 + 方局 4 组 |
| `SANMINGTONGH-095` | 各神兽对应五行须在命局成形（**三合或方局**） | 三合 4 组 + 方局 4 组 |
| `SANMINGTONGH-R-06` | 木局曲直（亥卯未或寅卯辰全）…土局稼穑（**辰戌丑未全**） | 三合 4 + 方局 4 + 土局 1（四支 `all_of`） |
| `SANMINGTONGH-018` | 子午、丑未、寅申、卯酉、辰戌、巳亥相冲 | 6 个二支组的 `any_of` |
| `DITIANSUICHA-031` | 卯酉冲为震兑战 | `all_of`（卯、酉） |
| `DITIANSUICHA-032` | 子午冲为坎离战 | `all_of`（子、午） |

**部分覆盖已在台账 `tools/reports/branch-group-map.json` 逐条写明**，例如
`DR-02` 的「局成宜顺、局破宜疏」是处置语、`SANMINGTONGH-095` 的「格局清纯不破」需格局判定，
均未表达。

## 3. 端到端验收（三态语义在真实盘上对得上）

样本四柱地支：caseA `午/申/子/未`，caseB `子/寅/巳/子`。

| rule | caseA | caseB | 说明 |
|---|---|---|---|
| `DITIANSUICHA-032` 子午冲 | **满足** | 不满足 | caseA 年支午与日支子同现 → 子午冲 ✓ |
| `SANMINGTONGH-018` 六冲 | **满足** | 不满足 | caseA 命中「子午」一对 ✓ |
| `SANMINGTONGH-015` 三合 | 不满足 | 不满足 | 两盘都没有完整三合局 ✓ |
| `DITIANSUICHA-031` 卯酉冲 | 不满足 | 不满足 | 无卯无酉 ✓ |
| `SANMINGTONGH-R-06` 五局 | 不满足 | 不满足 | 同上 ✓ |

三条边界断言（已入测试）：

- **三支缺一 → 不满足**：正是原文「三字缺一不能直接按三合化局论」的机器表达。
- **只有子、无午 → 不满足**（不是「信息不足」）：`zhi` 事实在场，条件可判而假。
- **一个 `zhi` 事实都没有 → 信息不足**：不得把「引擎没产出」算成「条件不成立」。

## 4. 一条要如实说明的账

9 条里 `SANMINGTONGH-018` 是 **`anchor: null`**（属 t169 台账的 189 条不可锚之一），
因此它**从来不在**「有锚且 `applicable_to` 为空」的未映射口径内 —— 给了谓词也不动那两个数字。
所以「落地 9 条」与「未映射 −8」并不矛盾。测试里显式钉住「恰好 1 条不在分母内」，
免得以后被当成算错。

## 5. 本轮顺手查过、但没有采纳的

- **六爻的六合／六冲**（`ZR-07` 子丑寅亥…、`ZENGSHANBUYI-ZR-07` 子午丑未…）：
  形态与 bazi 完全同构，但六爻**没有任何地支事实**（`emitLiuyaoFacts` 只产六亲／六神／爻位／
  动爻／伏神／世序），而 `zhi` 是 bazi 的键 —— 用 `--check-art-keys` 就会被拦。
  **要做得先给六爻加爻支事实**，属另一笔。
- **自刑**（`YUZHAOSHENYI-026` 辰午酉亥自刑）：自刑要**同一支出现两次**，
  而 `all_of` 两句相同的 `{zhi: 辰}` 会被**同一个事实**同时满足 → 会假阳。**不映射**。
  这暴露了 v3 的一个真实表达力边界：**「两个不同位置上的同一取值」currently 写不出来**
  （`same` 只绑同一取值，不能要求不同柱）。登记为下一批的语言候选。
- **`KR-06`／`XIEJIBIANFAN-004`**：不在六个产品术内（风水／择日），或属起例（建除十二神依月支起例）。

## 6. 未决清单（承接 t169–t174）

1. **v3 的表达力边界：同值异位**（§5 自刑）。要支持得引入「子句须由**不同事实**满足」
   或「两子句绑同一字段的不同取值」——这是语言变更，需先定语义再实现。
2. **15% 通配闸门挡住 4 条奇门规则**（t173 §5）：事实已齐，但只能写成 `{all_of:[{zhifu,"*"},…]}`
   → qimen 会到 17.9%。**未放宽闸门、未挑 2 条凑数**；需二选一授权。
3. **六爻爻支事实**（§5）：一加即可复用本轮的成组写法（六合／六冲／自刑）。
4. **liuren 位置级天将已就绪但只差一条**：引擎 `liuren.ts` 已产出 `tianjiang`＋`palace=日上/辰上/初传…`，
   且自带 `LR-UNKNOWN-MIBEN-021-WIRE` 明说「规则 applicableTo 仍为空」。
   唯一卡点是 **V15 目前不许 liuren 写 `scope.palace`**（只放 ziwei／七政）。
   放开即可映射 `LIURENMIBEN-021`（青龙居日上；原文还特意说「青龙在任意一传不等于龙居日本」，
   正好靠 `scope.palace=日上` 区分）。
5. **神煞 30 条**需扩 `shensha` 取法表；**梅花 21 条**本仓无事实层（产品已有 `meihua_gua`，
   但两处词表仍漂移）；**柱干支 30 条**含性别与跨键取值相等。
6. t169–t174 其余：`daxian`/`liunian_taisui`、`liuyao.structure` 打包名、
   ziwei 11 条命名格局缺定义表、`fold_han` 不处理古异体字、`nayin` 尚无谓词使用、
   189 条重述是否换真引文、V11 111 vs G1 <50、25 条既有结构恒真映射、3 条无据 statement。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮新增：地支成组映射（含 statement 复核）
python3 tools/map-branch-groups.py --dry-run      # 已映射后应报 0 条可映射
python3 tools/test-map-branch-groups.py           # 形态 + 语义 + anchor 账

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 三态求值（入参盘面状态 → 结论 + 置信度 + 出处）
python3 tools/eval-predicates.py --art bazi --case caseA -v | grep -A2 "DITIANSUICHA-032"
python3 tools/eval-predicates.py --art bazi --discrimination | grep -c HARD

# 导出与产品仓同步
python3 tools/export-rules.py                     # exported == anchored_exportable
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`3b4aa5368730d5df47f6bb631ba4aa83736fb148`**。
产品仓 `generated/*.json` 已同步覆盖（bazi 219 条带谓词）；`tsc --noEmit` exit 0；
相关 6 个测试文件 **60 项全绿**。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。