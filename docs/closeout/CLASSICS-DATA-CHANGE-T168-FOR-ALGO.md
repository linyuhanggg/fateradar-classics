# 消费方数据版本 · t168 谓词语言升级到 v3（复合条件／嵌套／多事实联合／同位置绑定）

日期：2026-09-21。基线提交：`cd41f5b5cd31c107384633da0a75d89626938679`（`main`）。
本轮只动 `applicable_to` 与工具链；**`statement` / `quote` / `anchor` / `verified*` 一律未改**，
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论（先读这条）

任务书写的是「消灭 `tools/reports/unmapped-predicates.md` 的 440 条，原因分类全是
『条件过于复合，现有谓词表达不了』」。**逐条复核后，该原因分类只对少数成立**（详见 §3）。
真正的问题是两件事，本轮各修一件：

1. **表达力确实不够** —— 旧 `applicable_to` 平铺列表在消费方是「或」，结构上写不出
   「且／嵌套／排除／同位置」。→ 本轮把语言升到 **v3**，补上这四样（§2）。
2. **报告本身不可复算且口径失真** —— 旧件无生成器、含 1 条已不存在的 rule_id，
   把 599 条一律写成同一个原因。→ 换成可复算报告 + 逐条台账（§3）。

**580 条里的绝大多数（约 96%）不能映射，不是因为表达力，而是因为原文根本没有盘面条件
（通论／体例／取象表／起例取法／pack 元规则），或所需事实引擎未产出。**
按贯穿契约「不编造、可溯源、原文没写就不写」，这些**必须**留空。
本轮没有为了数字好看虚构任何一条条件。

## 1. 覆盖率前后（口径未改，可复跑）

`python3 tools/predicate-report.py`

| art | 基线 with_pred | 基线覆盖 | 本轮 with_pred | 本轮覆盖 | 通配 | 通配占比 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 | 31.9% | **151** | **33.6%** | 16 | 10.6% |
| ziwei | 54 | 58.1% | **63** | **67.7%** | 0 | 0.0% |
| qimen | 7 | 17.5% | **8** | **20.0%** | 1 | 12.5% |
| liuren | 11 | 20.8% | 11 | 20.8% | 1 | 9.1% |
| liuyao | 21 | 30.4% | **23** | **33.3%** | 3 | 13.0% |
| qizheng | 11 | 24.4% | 11 | 24.4% | 1 | 9.1% |
| meihua（参考，非门禁） | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |
| yili（参考，非门禁） | 0 | 0.0% | 0 | 0.0% | 0 | 0.0% |

- 分母口径**一字未改**：仍是 `anchored - catalog_titles`；七政 31 条目录篇名的既有剔除照旧。
- 六产品 art 净增 **+20** 条有谓词规则，未新增任何 `value: "*"`；通配占比全线 ≤ 15%（PASS）。
- 未映射（带锚且 `applicable_to` 为空）：**599 → 579**。

`python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys`
→ 三道全 PASS，exit 0。

## 2. 谓词语言 v3

契约全文：`docs/PREDICATE-LANGUAGE-V3.md`。旧平铺列表语义**冻结不变**（仍是「或」）。

```yaml
# 旧形（语义不变）：或
applicable_to:
- key: shishen
  value: 七杀

# v3 组：且／嵌套／排除／同位置绑定
applicable_to: {all_of: [{key: ziwei_star, value: 禄存}, {key: ziwei_star, value: 天马}], same: palace}
applicable_to: {any_of: [{all_of: [{key: bamen, value: 休门, scope: {gong: 9}}]}, …], none_of: [{key: kongwang, value: '*'}]}
```

- 组算子：`any_of` / `all_of` 必居其一，`none_of` 排除，`same` 同位置绑定（同宫／同柱／同爻）。
- `scope` 扩到 `layer / pillar / palace / gong / yao`，**全部取自引擎已产出的 `Fact.scope`**
  （奇门 `gong`、六爻 `yao`、八字 `pillar` 在 `facts-sample.json` 里本就存在），未新增 FactKey。
- 三态：`满足` / `不满足` / `信息不足`。**引用的 key 在本盘完全不存在 ⇒ 信息不足，不得降级为不满足**。
  `none_of` 尤其：缺 key 时无法证明「没有」，同样给信息不足。

### 2.1 为什么这个升级不是镀金：一个真例子

`luming-nayin/luoluzi-sanming` **LZ-06-04**「生月带禄入仕赫奕」，注文给的是穷尽式定义：
「生月帶官祿者，如甲乙人秋生，丙丁人冬生，戊己人春生，庚辛人夏生，壬癸人生于四季月是也」。

这是 **(日干组 × 月令季) 的且，组间是或**——旧语言写不出来（平铺列表会把 5 组拆成散装 OR，
命中任意一个干或任意一个支就算成立，等于把条件放宽到失真）。v3 写成五行嵌套组：

```yaml
applicable_to: {any_of: [{all_of: [{any_of: [{rizhu 甲}, {rizhu 乙}]}, {any_of: [{yueling 申},{yueling 酉},{yueling 戌}]}]}, …共五组…]}
```

同类的还有奇门 `QM-P37`「六仪受制」：原文八组「门加宫」，映射为八组 `{all_of: [{bamen <门>, scope: {gong <宫>}}]}`
的 `any_of`（宫号按后天八卦 1坎…9离，已逐组机器核对与 statement 完全一致）。

## 3. 599 条未映射的逐条处置（可复算）

新报告：`python3 tools/predicate-gap-report.py --md tools/reports/unmapped-predicates.md`
（旧件是被覆盖重写的；旧件含 1 条已不存在的 `LIURENZHIYIN-015`，且无生成器。）

逐条判定台账：`tools/reports/predicate-decisions/*.json`（每个 art 一份，含 `book/rule_id/decision/reason_class/原文依据`）。

| 理由分类 | 条数 | 含义 |
|---|---:|---|
| `not-a-condition` | 232 | 原文无盘面适用条件：通论、体例、取象表、起例取法 |
| `fact-not-emitted` | 277 | 需要引擎未产出的事实（逐条写明缺哪一项） |
| `condition-too-vague` | 35 | 原文有条件但口径未定，或**原文自己**拒绝单一条件断 |
| `meta-rule` | 35 | pack 元规则／调用条件／工程约束，不是盘面条件 |
| **合计未映射** | **579** | |

机械分类（`predicate-gap-report.py` 的 `classify()`）与台账不同时以台账为准，台账必须给原文依据。

### 3.1 「条件过于复合」这个说法对不对

不对。机械扫描能复原出「跨 key 多事实令牌」（＝真需要 AND 的候选）的**只有 7 条**，
其中还有假命中（如 `dongyao/shiyao/yingyao` 共享爻位值域、`bamen/zhishi` 共享八门值域，
术名「六爻」本身也是爻位取值）。真正被表达力卡住的，量级是**个位数到十几条**，
不是 440 条。剩下的是**原文根本没有条件**，这一点在 bazi 的 301 条里最明显：
`理为体，气为用`、`十干各有性情`、`安命宫先从子宫起正月逆排`、`旬空由十干配十二支未到之位确定`
——这些是把「怎么做」或「取象表」写成条目，不是「何时适用」。

**据此，§2 的语言升级是必要的，但不是充分条件；覆盖率的主要瓶颈不在谓词语言，而在原文性质。**

## 4. captain 复核：撤回 3 条、披露 8 条

台账里 `mapped` 23 条，经逐条对照 `statement` / `quote` 后**撤回 3 条**，净映射 **20** 条。
记录：`tools/reports/predicate-decisions/captain-audit.json`。

| 撤回 | 原映射 | 撤回理由 |
|---|---|---|
| `DITIANSUICHA-DR-07` | 10 个 `rizhu` | 作业书点名的取象表范例；10 值穷尽值域⇒任何盘都成立，零区分度；其 `quote` 无脏腑亦无天干分组 |
| `TAIWEIFU-021` | `{紫微 OR 贪狼}` | 断辞主语是土星／金星（无对应星曜名）；「紫微」取自起景句，「贪」的判据「守空」未产出——拼出来的是失真条件 |
| `ZIWEIDOUSHUQ-ZW-04` | `紫微 in 兄弟宫` | statement 是「兄弟宫主…」的通则、不含星名；星名只出自 quote 的例文，会把通则收窄 |

保留但**必须在台账披露「只覆盖原文条件的真子集」**的 8 类：`ZIWEIDOUSHUQ-ZW-01`（兄弟宫支属推断）、
`-008`（事业宫支属推断）、`-021`/`TAIWEIFU-006`（「会照」未产出，只覆盖同宫支）、`TAIWEIFU-010`、
`ZW-01`/`-011`/`-012`/`-015`（庙旺／格局名支未表达）、`QM-P37`（天盘六仪无 key）、`DR-04`。
**子集可以，超集不行**：不得新增原文没有的条件。

## 5. 工具链修复（本轮的真实收益点）

发现并修复一个**静默丢数据**的缺陷，它同时压低覆盖率、抬高未映射数，而且不报错：

> `predicate-report.py::preds_of` 与 `predicate-gap-report.py` 只认 `isinstance(..., list)`。
> 对 v3 组（一个 mapping）做 `for pred in raw` 会迭代出**键名字符串**，`isinstance(pred, dict)` 全假，
> 于是组形谓词被读成「没有谓词」；`export-rules.py` 同病——组形规则导出成 `applicableTo: []`。

修法：新增唯一实现 `tools/predicate_lang.py`（`iter_predicates` / `has_predicates` / `leaf_count`），
覆盖率报告、未映射报告、导出层统一走它。回归测试 `tools/test-predicate-lang.py` 把该行为钉死
（含与真实规则库对账：`QM-P37` 八组必须被计入）。

同时新增 **V16 校验门禁**（`tools/validate-rules.py`）：组形结构、嵌套深度上限 4、
`same` 只能出现在 `all_of`、`scope.gong` 仅奇门且 1–9、`scope.yao` 仅六爻且 1–6、
`scope.palace` 仅 ziwei（`ziwei_palace` 词表）与 qizheng（`gongwei` 词表）、`scope.pillar` 五个柱位。
`tools/test-validate-gates.py` 增加 reverse7–13：六个反例必红 + 一个合法组形必绿（防止门禁变成「一律拒绝」）。

### 5.1 可被消费方当工具调用

新增 `tools/eval-predicates.py`：**入参盘面状态，返回结论 + 置信度 + 出处**。

```bash
python3 tools/eval-predicates.py --art ziwei --case caseA -v
#  [满足] ZIWEIDOUSHUQ-ZW-01 conf=1.0 覆盖=1.0 命中: ziwei_star=天机@命宫
#      出处: sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md L...
```

- `置信度` 定义为**输入完备度**（引用的 key 中本盘实际存在的比例；用通配打 0.8 折），
  **明确不是古籍预测准确率**；`verification` 仍 `provisional`，`verified` 恒 `false`。
- 出处＝书目 + 原文行号锚点 + 逐字摘录，是电子文本溯源，**不是人工影印核验**。
- 六术实测（caseA）：bazi 满足75/不满足78/信息不足369；ziwei 54/9/41；qimen 8/0/32；
  liuren 10/1/50；liuyao 21/0/61；qizheng 11/0/78。

产品仓同步实现同一契约（`src/lib/engine/facts/vocab.ts` 的 `evaluateApplicableTo`、
`matcher.ts` 改为按三态取「满足」入池、`types.ts` 的 `ApplicableTo`，
以及 `admin.rules.ts` 的叶子遍历）；`tsc --noEmit` exit 0，`vitest run tests/rules` 28 passed。

## 6. 未决清单

1. **缺事实是最大的一块（277 条）**，且高度集中：奇门天盘干（乙丙丁庚甲）约 31 条、
   七政格局名与行限 12 条、六爻月建日辰／变爻变卦／空亡入墓／六冲六合 31 条、
   八字日支与大运流年干支／纳音／神煞取法输入 39 条、六壬四课上下克与天将落宫 18 条。
   **这些要动引擎事实层，不是谓词层的事。**
2. **七政无新映射（24.4% 原样）**：65 条里 53 条是通论／目录篇名，12 条缺神煞与虚星 key。
3. **meihua 与 yili 仍 0%**，且**没有引擎为这两术产出任何事实**；本轮不造映射。
4. **六壬 42 条一条未映射**：21 条是 pack 元规则／调用条件，18 条缺事实（四课、驿马、天将落宫）。
   其中伏吟／返吟 3 条若上游确认 adapter 对这两类盘稳定产出 `keti`，可补映射（约 +3 条）。
5. **`needs-human-review.md` 的 81 条本轮未推进**（急件是谓词层；那 81 条要人判锚点，
   本轮不含）。`anchor: null` 的规则（如 meihua 19 条、liuren 8 条）不在覆盖率口径内，未造谓词。
6. **两份 `fact-vocab.json` 已漂移**：产品仓多 `meihua_gua` / `xiaoliuren_palace` 两个 key。
   `CLASSICS_STATUS.md` §G6 记的 `cmp` 一致**已不成立**。本轮未动词表（越权），仅登记。
7. 既有未映射规则里存在 `value: "*"` 的通用谓词（如 `ZENGSHANBUYI-006 fushen:"*"`、
   `HJC-R002 shiyao:"*"`），本轮**未清理**（不在未映射集合内），留作单独一笔。

## 7. 不变量与可复跑命令

不变量：外层契约不变（不新增 FactKey、不改 `statement/quote/anchor`、不生成让 `verified` 变 true 的自我认定、
不把未实现的救应写成没有救应、宁留 `anchor: null` 也不硬锚）；`verified: true` 全库计数 **0**。

```bash
cd /Users/sync/code/fateradar-classics

# 闸门（本轮全绿）
python3 tools/validate-rules.py                    # OK 55 file(s)
python3 tools/validate-executable.py               # OK 15 packages, 258 records, 579 spans, 42 gaps
python3 tools/validate-annotations.py              # 55 books, 88492 entries, 0 errors
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done

# 覆盖率（口径未改）
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/predicate-report.py                  # 对比 §1 表

# 未映射：可复算报告 + 逐条台账
python3 tools/predicate-gap-report.py
python3 tools/predicate-gap-report.py --md tools/reports/unmapped-predicates.md
python3 tools/predicate-gap-report.py --art qimen -v

# 当工具调用：入参盘面状态 → 结论 + 置信度 + 出处
python3 tools/eval-predicates.py --art ziwei --case caseA -v
python3 tools/test-eval-predicates.py              # 三态语义 28 项
python3 tools/test-predicate-lang.py               # 组形不得被读成空

# 导出（产品仓消费）
python3 tools/export-rules.py                      # exported == anchored_exportable
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` 必须钉在**本轮提交的 40 位 SHA** 上（见本文件所在提交），不能写 `main`：
锚点行号按该 commit 的 fulltext 分行算出，用 `main` 会让出处随更新漂移。
`dist/rules/*.json` 已按本轮重新导出，产品仓 `src/lib/rules/generated/*.json` 同步覆盖。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。