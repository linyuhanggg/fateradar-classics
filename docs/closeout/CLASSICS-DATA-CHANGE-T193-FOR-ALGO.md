# 消费方数据版本 · t193 六爻具名状态入事实层（liuyao 31.9% → 34.8%）

日期：2026-09-21。基线提交：`915ea1e`（t192 后）。
**数据修订提交（请钉这个）：`b6f2f52215d99fb3ee3c7b0f0865c02fb6cfb09d`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

延续 t184（奇门 `geju_qimen`）／t187（六壬 `keti`）的路子 ——
**引擎已经给出具名分类，事实层没把它产出**。
本轮把六爻的三样具名状态产成事实，并据此落地 **2 条**规则：
**liuyao 31.9% → 34.8%**（22 → 24），未映射 **477 → 475**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 15 | 28.3% | 6.7% | 5 |
| **liuyao** | 21 (30.4%) | 21 (30.4%) | **24** | **34.8%** | **12.5%** | 6 → **8** |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **477 → 475**。4 大门禁全绿；**33** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
`coverage-report --fail-under 54` PASS；产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 三个新事实：取名，不另算

liuyao 的 `analysis` 里**本来就**逐爻给出：

| 引擎字段 | 取值 | 新 FactKey |
|---|---|---|
| `state.monthStrength` | 临月／旺／相／余气／休囚／**月破** | `liuyao_month_strength`（逐爻，`scope.yao`） |
| `state.activity.label` | 静／明动／**暗动**／日破／冲空／伏藏／变位／日冲待辨… | `liuyao_activity`（逐爻，`scope.yao`） |
| `analysis.use.requested` | 父母／兄弟／子孙／妻财／官鬼／世爻／应爻 | `liuyao_yongshen`（整盘） |

- **用神未定则不产出**（引擎给「待明确所问对象」时跳过）——不把未定当已定。
- `liuyao_activity` 的**值域有意留空**：标签随判据而增（含「日冲待辨」这类**未定态**），
  闭域会宣称引擎只会产出某几个值。安全由 `--check-open-values`（取值须在样盘出现过）保证。

## 3. 落地 2 条

| rule | 原文 | 谓词 |
|---|---|---|
| `ZENGSHANBUYI-030` | **月建冲爻为月破**；月破之爻——静则到底破… | `[{key: liuyao_month_strength, value: 月破}]` |
| `ZENGSHANBUYI-018` | **静爻得日辰冲为暗动**；暗动如同动，能生克他爻 | `[{key: liuyao_activity, value: 暗动}]` |

条件是「本卦有月破之爻／有暗动之爻」——**正是引擎那两个具名分类**；
后文「静则到底破…」「暗动如同动…」是**断法**而非条件，未表达（台账已记）。

**实测**：

| 盘 | 月破 | 暗动 | `030` | `018` |
|---|---|---|---|---|
| caseA | **有** | 无 | **满足** | 不满足 |
| caseB | 无 | 无 | 不满足 | 不满足 |
| caseC | 无 | **有** | 不满足 | **满足** |

## 4. 补齐样盘（同 t187／t192 的原则：不放宽任何东西）

`暗动` 与 `用神` 在原两盘里**都不出现**：
- 原盘所问事项（择时决策／官讼是非）不在 `TOPIC_USE` 表内 → **用神按设计不产出**；
- `liuyao_activity` 是开放值域 → 用 `暗动` 写谓词会让 `--check-open-values` 报红。

由**遍历日期找出真实输入**：`2026-01-06`、卦 `111111`、所问「求财谋利」——
该盘第 6 爻受日冲成**暗动**、用神取**妻财**。加为 liuyao `caseC`：

```
caseA: 用神=[] 活动=[静,静,静,日破,静,静]        月建强度=[相,月破,休囚,休囚,临月,休囚]
caseB: 用神=[] 活动=[明动,静,静,静,冲空,静]      月建强度=[休囚,临月,休囚,休囚,休囚,休囚]
caseC: 用神=[妻财] 活动=[静,静,静,静,静,暗动]    月建强度=[余气,休囚,旺,休囚,相,旺]
```

## 5. 新增键牵动了两处**机器事实**（都已按实况刷新）

加键之后，机械判据立刻发生变化——这是**判据变强，不是漏账**：

1. **机械命中多 3 条**：`HZL-R002`／`HZL-R004`／`ZENGSHANBUYI-007`
   （它们的 statement 里出现「旺相／休囚」「持世」「用神／月破」等如今已是事实取值的词）。
   已逐条复核并登记：前两条新增「**需配对**」类（把「用神×爻位」配到「该爻的月建强度」上），
   第三条属「**需计数**」（用神两现…一爻发动／两爻俱动俱静）。
   残留台账 **27 → 30 条**。
2. **残留台账 11 条的 `triage_kind` 变了**（同一原因）。
   该字段是**机器事实**（按实况刷新），而**判断理由仍是人工**——两者在台账里分开记录。

> 这正是 t181 那道一致性闸门该做的事：键一变，账本就得跟上；它当场报红。

## 6. 未决清单（承接 t179／t187／t192）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---|--|
| ★1 | **六爻「用神×爻位」配对类**（`HZL-R002`／`HZL-R004`） | 2 | 事实已齐（用神／月建强度／世应），需用枚举配对写出「用神所在之爻的月建强度」 |
| 2 | 六爻余项（月建日辰关系／回头生克／旬空／反吟伏吟） | 若干 | 需关系判定或引擎已算未产出的分类（反吟伏吟、旬空） |
| 3 | `QM-P30` 时格「庚临时干三奇」／`QM-P26` 直使加地丁 | 各 1 | 原文两读，不猜／需无取值子句（口径待裁定） |
| 4 | 八字透干类（`SANMINGTONGH-R-02`／`YUANHAIZIPIN-008`） | 2 | 需引擎产出**藏干**（本气/中气/余气），之后可用配对技术 |
| 5 | 六壬课体余项 / 紫微命名格局 / 3 条无据 statement | 2–4 / 4 / 3 | 沿用 t187／t183／t185 |
| 6 | 其余 | — | 需授权（引擎投入）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-fixed-values.py --dry-run       # 幂等；现 10 条
python3 tools/test-map-fixed-values.py
python3 tools/test-expressible-residue.py         # 30 条，含新增「需配对」类

# 三态语义（caseA 月破、caseC 暗动）
python3 tools/eval-predicates.py --art liuyao --case caseA -v | grep -A2 "ZENGSHANBUYI-030"
python3 tools/eval-predicates.py --art liuyao --case caseC -v | grep -A2 "ZENGSHANBUYI-018"

# 新事实确实进盘
python3 -c "
import json
d=json.load(open('tools/reports/facts-sample.json'))['liuyao']
for case,c in d.items():
    print(case, '用神', [f['value'] for f in c['facts'] if f['key']=='liuyao_yongshen'],
          '活动', [f['value'] for f in c['facts'] if f['key']=='liuyao_activity'])"

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

`CLASSICS_REV` = **`b6f2f52215d99fb3ee3c7b0f0865c02fb6cfb09d`**。
产品仓 `generated/liuyao.json` 已同步覆盖（24 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3545 passed / 0 failed**。

**给消费方的一条说明**：六爻事实层新增三键，其中
`liuyao_yongshen`（用神）**只在所问事项能确定用神时才产出**
（`TOPIC_USE` 表内的事项或显式传入 `useRelative`）；
所问不在表内时**不产出**——此时相关规则会如实返回「信息不足」，不是缺事实。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。