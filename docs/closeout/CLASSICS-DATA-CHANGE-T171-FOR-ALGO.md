# 消费方数据版本 · t171 奇门天地盘干入事实层（干宫相配 16 条落地）

日期：2026-09-21。基线提交：`d3264e1`（t170 后）。
**数据修订提交（请钉这个）：`eb77f1cdec901d045f3e3ae03e764edd4548f000`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

继续 t170 的路子：**事实本来就在引擎里，只是没被当作事实产出。**
奇门一样——`QimenCell` 早就有 `sky`（天盘干）与 `earth`（地盘干），
`emitQimenFacts` 的入参类型却没带它们。本轮接上并映射。

产出：**16 条规则落地**（干宫相配／三奇入墓／龙虎神鬼遁／伏吟反吟），
qimen 谓词覆盖 **20.0% → 60.0%**，未映射 **521 → 505**。

## 1. 覆盖率前后（口径未改，可复跑）

`python3 tools/predicate-report.py`

| art | 基线 | t170 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 211 | 47.0% | 7.6% | 9 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| **qimen** | 7 (17.5%) | 8 (20.0%) | **24** | **60.0%** | 12.5% → **4.2%** | 4 → **6** |
| liuren | 11 (20.8%) | 11 (20.8%) | 11 | 20.8% | 9.1% | 3 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 | 30.4% | 14.3% | 5 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |
| meihua / yili（参考） | 0 | 0 | 0 | 0.0% | 0.0% | 0 |

- 未映射：**521 → 505**（−16）。口径一字未改，**未新增任何 `value: "*"`**。
- qimen 通配占比从 12.5% 降到 **4.2%**（分母变大，且本批没有用 `*`）。
- 4 大门禁全绿；全部 **23** 个 `tools/test-*.py` 全绿；`--check-open-values` / `--check-art-keys` PASS。

## 2. 两个新 FactKey

| key | 含义 | 取值域 | 来源 |
|---|---|---|---|
| `tianpan_gan` | 天盘干，`scope.gong ∈ 1–9`（**中五不立**） | 九干：戊己庚辛壬癸丁丙乙 | `QimenCell.sky`（已在 grid 里） |
| `dipan_gan` | 地盘干，同上 | 同上 | `QimenCell.earth` |

**无「甲」**：奇门六十甲子以六仪代甲（甲子戊、甲戌己、甲申庚、甲午辛、甲辰壬、甲寅癸），
天地盘只有九干。值域是封闭九干，写错字会被 V7 拦下。

**中五不立天地盘干事实**：与本引擎既有口径一致——中五「寄坤」，
其中五地盘干由 `hostedSky` 随天禽转到寄宫体现（中心格 `sky`/`door`/`star`/`god` 皆为 `——`）。
`emitQimenFacts` 里为此加了显式守卫，守住既有不变量「**无任何 fact 带 `gong=5`**」——
产品 `tests/engine/qimen-methods.test.ts`（34 项）依赖它，本轮该文件仍全绿。

> 这条不是随手加的：实测**未加守卫**时 `dipan_gan` 会带出 `gong=5` 共 9 条/盘，
> 直接撞红那条既有断言。选择「按引擎口径排除中五」而不是「改测试迁就数据」。

## 3. 16 条怎么映射

工具：`tools/map-qimen-stems.py`（`--dry-run` 可先看），每条都**带 statement 复核片段**，
判据必须命中原文才落盘（不命中直接 FAIL，不是自报）。

| 形态 | 规则 | 谓词 |
|---|---|---|
| 天盘干加地盘干（同宫） | QM-P03 龙逃走 乙奇遇辛、P04 虎猖狂、P05 蛇妖矫、P06 雀投江、P07 大格 庚临六癸、P08 刑格 庚临六己、P09 小格 庚临壬、P34 六庚加丙奇、P35 丙奇加六庚金 | `{all_of: [{tianpan_gan X}, {dipan_gan Y}], same: gong}` |
| 奇入某宫 | QM-P16 三奇入墓（乙奇坤宫、丙奇乾宫、丁奇艮宫） | 三条 `{tianpan_gan …, scope: {gong: 2/6/8}}` 的 OR |
| 门／神与奇合，**点名宫位** | QM-P21 龙遁（合坎=1宫）、P22 虎遁（合艮辛=8宫） | 三句都写 `scope.gong` |
| 门／神与奇合，**未点名宫位** | QM-P23 神遁（合九天）、P24 鬼遁（合九地杜门） | `{all_of: […], same: gong}` 绑定 |
| 格局名 | QM-P14 伏吟、P15 反吟 | `{geju_qimen: 伏吟局}` / `{反吟局}` |

- 宫号按后天八卦：1坎 2坤 3震 4巽 5中 6乾 7兑 8艮 9离。
- 伏吟／反吟取引擎**已产出**的格局名；实测样本值带「局」字（「伏吟局」），
  不是「伏吟」——按实测值写，不按想当然写。

### 3.1 端到端求值验收

| 样本 | 格局 | 天盘干 | QM-P03 龙逃走 | QM-P14 伏吟 | QM-P15 反吟 |
|---|---|---|---|---|---|
| caseA | 门迫／三奇得使／奇门相合 | 乙@8、辛@1… | **满足**（乙@8 与地盘辛@8 同宫） | 不满足 | 不满足 |
| caseB | 伏吟局 | 乙@4… | 不满足（乙@4，地盘辛@8，不同宫） | **满足** | 不满足 |

`QM-P22 虎遁` 在 caseA 为**不满足**——乙@8、地盘辛@8 都在 8 宫，但休门不在 8 宫；
三句同宫的要求正确生效（这正是 t168 的 `same: gong`／显式 scope 在起作用）。

## 4. 顺带修正：`matched` 的契约

求值结果里的 `matched` 此前在任何三态下都会带上「各子句各自命中过」的叶子。
`all_of` 里这很容易被消费方误读成「整条成立」。本轮改为：

> **`matched` 只在三态为「满足」时给出见证集；不满足／信息不足一律为空。**

古籍仓 `tools/eval-predicates.py` 与产品仓 `vocab.ts` 的 `evaluateApplicableTo` 两处同步，
并各加断言（`test-eval-predicates.py` 新增 9b 组三项）。

## 5. 未映射（本批明确不做，且已钉住）

「**甲值符加地盘丙奇**」（QM-P01 龙回首、P02 鸟跌穴、P31 伏宫）一类**不映射**：
`甲` 不出现在天地盘（甲寄六仪），要表达它得先有「**值符所落之宫**」这一事实——
那需要 `zhifu`/`zhishi` 带 `scope.gong`，属下一批的设计决定，不在本次范围。
测试 `test-map-qimen-stems.py` 第 5 组显式断言这三条**仍为空**，防止后续被顺手映射。

其余未映射qimen规则（P13 时干克日干需「克」关系；P25 三奇得使需旬首；P27–P30 岁／月／日／时格、
P32／P33、P36、P38／P39 需时干或岁干等）原因不变，台账 `tools/reports/predicate-decisions/qimen.json` 有逐条记录。

## 6. 未决清单

1. **`zhifu`/`zhishi` 是否带 `scope.gong`**：加上即可解锁 QM-P01／P02／P26／P31（约 4 条）。
   加 scope 是对既有事实的**增量**（既有谓词未声明 scope 故行为不变），但需先评估对其他消费处的影响。
2. **`daxian`/`liunian_taisui` 的事实现状**（t170 §5 遗留）：11 个 ziwei 谓词叶子恒为「信息不足」。
3. **fact-not-emitted 剩余 201 条**（505 条未映射中）：纳音取象其余书、神煞具体名 23、
   六爻月建日辰／变卦 36、六壬四课细节 4、七政格局行限 6。
4. **`nayin` 仍无谓词使用**：需按各条 statement 逐个判，不批量。
5. **`fold_han` 不处理古异体字**（t170 §3.4）：影响 V11/V14 判据，建议单独一笔评估。
6. t169 未决项仍在：189 条重述是否换成真引文、V11 111 vs G1 <50、25 条既有结构恒真映射。

## 7. 不变量与可复跑命令

不变量：不改 `statement`/`quote`/`anchor`/`verified*`；不新增 `value: "*"`；不硬锚；
不把未实现的救应写成没有救应；不生成让 `verified` 变 true 的自我认定。`verified: true` 全库 **0**。

本轮改动均经**字段级审计**：`applicable_to` 之外无任何字段变动（含 book block 与 rule set）。

```bash
cd /Users/sync/code/fateradar-classics

# 奇门天地盘干映射（含原文复核 + 中五不变量）
python3 tools/map-qimen-stems.py --dry-run     # 复核 16 条 statement 片段
python3 tools/test-map-qimen-stems.py          # 台账/形态/中五/无甲/未迁移

# 闸门（本轮全绿）
python3 tools/validate-rules.py                # OK 55 file(s), 285 warning(s)
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 覆盖率与未映射
python3 tools/predicate-report.py               # qimen 60.0%
python3 tools/predicate-gap-report.py           # 505 条

# 三态求值（入参盘面状态 → 结论 + 置信度 + 出处）
python3 tools/eval-predicates.py --art qimen --case caseA -v | grep -A2 "QM-P03"
python3 tools/eval-predicates.py --art qimen --case caseB -v | grep -A2 "QM-P14"

# 导出与产品仓同步
python3 tools/export-rules.py                   # exported == anchored_exportable
```

产品仓（本机无 `bun`，用 `jiti` 跑 TS 重新生成夹具）：
`tsc --noEmit` exit 0；与本轮相关 9 个测试文件 **103 项全绿**（含 `qimen-methods` 34 项）。

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`eb77f1cdec901d045f3e3ae03e764edd4548f000`**。
不可写 `main`：锚点行号按该 commit 的 fulltext 分行算出。
产品仓 `generated/*.json` 已同步覆盖；两处 `fact-vocab.json` 共有键值域逐项一致（38 键）。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。