# 消费方数据版本 · t172 executable 层求值器（目标项 3／4）

日期：2026-09-21。基线提交：`b8a2b98`（t171 后）。
**本轮只加工具、无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`eb77f1cdec901d045f3e3ae03e764edd4548f000`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标项 3（守 `fateradar-executable-v2` 的三态／`rescue`／`named_gaps`／`implementation_assumption`／
`verified:false`）与目标项 4（新规则必须可被消费方当工具调用）此前**只落在谓词层**
（`applicable_to` + `eval-predicates.py`）。而 `references/executable/*.json` 的 **258 条记录
自带三态字段**，`when` 也是机器可读的——**古籍仓却没有任何东西去求值它**。

本轮补上这一段：`tools/eval-executable.py`，入参盘面状态 → 结论 + 置信度 + 出处。

## 1. 本轮覆盖率不变（口径未改）

`python3 tools/predicate-report.py` 与 t171 逐项一致：bazi 47.0%／ziwei 67.7%／qimen 60.0%／
liuren 20.8%／liuyao 30.4%／qizheng 24.4%；未映射 505 条；`git status -- references/books references/vocab` 为空。

4 大门禁全绿；全部 **24** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS。

## 2. 为什么要做：`when` 机器可读，却没人求值

executable 层与谓词层是**两套独立声明**：

| | 谓词层（rules.yaml） | executable 层 |
|---|---|---|
| 适用范围写法 | `applicable_to`，按 **FactKey** 词表 | `when`，按**字段路径** |
| 例子 | `{key: rizhu_strength, value: 中和}` | `{equals: {day.gan: 甲}}`、`{exists: three.chuan}` |
| 三态 | 由求值器给 | 记录自带 `satisfy_when`/`fail_when`/`unknown_when` |
| 此前求值器 | ✅ `eval-predicates.py`（t168） | ❌ **无** |

实测 `when` 的形态分布（258 条）：

| 形态 | 条数 | 机器可读 |
|---|---:|---|
| `{all: [{equals…}, …]}` | 120 | ✅ |
| `{exists: 路径}` | 91 | ✅ |
| `{geju.name: […]}` 等简写 | 19 | ✅ |
| `{equals: {…}}` | 8 | ✅ |
| `{in: {…}}` | 4 | ✅ |
| `{skyStemIn: […], locationBasis}` | 4 | ✅ |
| `{scope, definition}` / `{definition}` | 11 | ❌ 需定义表 |
| `{interference.id: […]}` | 1 | ❌ 需注册表 |

即 **246/258 可机器求值**，12 条需要定义表。`when` 里只用到 **37 种字段名**。

## 3. `FIELD_MAP`：字段路径 ↔ FactKey 对照表

这是本轮的实质产物（写在 `tools/eval-executable.py`），每条都写明依据。要点：

- **能接上的占多数**：`day.gan`/`month.zhi`/`year.zhi`/`time.gan`/`pillars.zhi` → **t170 新增的逐柱
  `gan`/`zhi`**；`geju.name` → `geju`；`geju.tenGod` → `shishen`；`three.chuan` → `sanchuan`；
  `ke.style` → `keti`；`star.palace`/`sun.palace` → `xingyao`；`star.dignity` → `miaowang`；
  `sun.mansion`/`moon.mansion` → `xiudu`。
- **正好接上 t171**：`sky.stem+palace`（4 条 `skyStemIn`）→ **`tianpan_gan`**。
  也就是说 t171 加的天地盘干，直接让 executable 层这 4 条可判。
- **接不上的 9 种逐条写明理由**（不凑近似名）：`zhifu.palace`／`timedry.palace`（值符／值使落宫，
  引擎未产出）、`liuyao.structure`（卦体结构）、`positions`、`four.ke`、`shehai.method`、
  `yongshen.zhi`、`day.gan.element`、`xiaoliuren.*`（本仓事实层无小六壬）、`meihua.*`。

> **交叉印证**：t171 我独立判断「QM-P01／P02／P31 需要『值符所落之宫』」，而 executable 层
> 的 `QMD-E-01`（伏吟落宫）`required_facts` 恰好就写着 `zhifu.palace`、`when.exists` 也是它。
> 两条独立路径指向同一个缺口——这比单方推断更可信。

## 4. 两条必须写清的口径（防误读）

1. **`exists` 在字段对应的 key 整个缺席时给「信息不足」，不给「不满足」。**
   事实袋里没有这个 key，无法区分「本盘不成立」与「引擎没产出」；
   而后者正是 `named_gaps` 关心的「未知分支在实现上能否忠实成立」。
   （key 在场时 `exists` 只看存在性、不看取值，故恒为满足。）
2. **「不满足」只出现在「引用字段都能在本盘判定、且条件为假」时。**
   因此 91 条 `exists` 子句不会单独产出「不满足」。
   **宁可报信息不足，也不把「引擎没产出」算成「原文条件不成立」。**

这两条与谓词层同源，且是**有意为之的保守**——放宽它们能立刻让数字好看，但那正是本任务禁止的。

## 5. 实测：全库 258 条的三态分布

```
满足 65   不满足 143   信息不足 38   未提供定义表 12
rescue=unimplemented 30 条   带 named_gaps 31 条   verified=true 0 条
```

按术分布（露出的问题很集中）：

| art | 记录 | 满足 | 不满足 | 信息不足 | 未提供定义表 | 说明 |
|---|---:|---:|---:|---:|---:|---|
| bazi | 183 | 46 | 136 | 0 | 1 | 最可判：`when` 以 `day.gan`/`month.zhi` 等值为主 |
| liuren | 23 | 10 | 7 | 6 | 0 | 课体与三传可判；四课／涉害取法不可判 |
| liuyao | 21 | 0 | 0 | **21** | 0 | **全为信息不足**：`liuyao.structure` 等未产出 |
| xiaoliuren | 6 | 0 | 0 | **6** | 0 | 本仓事实层无小六壬 |
| qizheng | 6 | 5 | 0 | 1 | 0 | 曜宫／庙旺可判 |
| qimen | 6 | 4 | 0 | 2 | 0 | 天地盘干可判（t171 之功）；值符落宫不可判 |
| ziwei | 12 | 0 | 0 | 1 | **11** | 11 条是命名格局定义（无定义表） |
| meihua | 1 | 0 | 0 | **1** | 0 | 无引擎事实 |

**结论：executable 层的可判性瓶颈不是语言，而是三件事**——
(a) 命名定义表缺失（ziwei 11 条 `辅弼夹帝`／`禄马同宫` 之类）；
(b) 卦体结构类事实未产出（liuyao 21 条）；
(c) 小六壬／梅花事实层为空（7 条）。

## 6. 未决清单

1. **命名定义表**：ziwei 11 条格局定义（`辅弼夹帝`／`日月夹财`／`君臣庆会`／`日出扶桑`／
   `月朗天门`／`月生沧海`／`金灿光辉`／`魁命钺身`／`禄马同宫`／`武曲守垣`／`贪火相逢`）
   + 1 条 `interference.id`。要有定义表才能求值；**不要**把它们塞进三态里的任意一态。
2. **`zhifu.palace`／`timedry.palace`**：t171 §6 已列为下一批候选（给 `zhifu`/`zhishi` 加 `scope.gong`），
   executable 层两条记录也在等它。
3. **六爻卦体结构**：liuyao 21 条 executable 记录全卡在 `liuyao.structure`；
   这与 t169 台账里六爻 31 条 `fact-not-emitted` 是同一块。
4. **`day.gan.element`／`tenGodFacts.<十神>.element`**：九运／十神五行派生未产出。
5. t170／t171 遗留：`daxian`/`liunian_taisui` 事实现状；`fold_han` 不处理古异体字；
   `nayin` 尚无谓词使用。
6. t169 遗留：189 条重述是否换成真引文、V11 111 vs G1 <50、25 条既有结构恒真映射。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# executable 层求值（入参盘面状态 → 三态 + 置信度 + 出处）
python3 tools/eval-executable.py --all
python3 tools/eval-executable.py --all --json | head -40
python3 tools/eval-executable.py --package references/executable/daliuren-daquan.json --case caseB -v
python3 tools/test-eval-executable.py            # 24 项：三态语义 + 对照表不得引用不存在的事实

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 谓词层求值（t168 起）
python3 tools/eval-predicates.py --art ziwei --case caseA -v
python3 tools/eval-predicates.py --art bazi --discrimination
```

## 8. 给 cosmic 的版本钉

**本轮无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 均未改），
故 `CLASSICS_REV` **不变**，仍为 `eb77f1cdec901d045f3e3ae03e764edd4548f000`；产品仓无需重新导出。

新工具已入 CI：`tools/test-eval-executable.py` 与既有
`test-predicate-lang` / `test-eval-predicates` / `test-map-nayin-ganzhi` / `test-map-qimen-stems` /
`test-needs-human-review-report` 一同成为每批必过的门禁。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0；
电子文本匹配、模型审查与测试都不能代替人工影印核验。