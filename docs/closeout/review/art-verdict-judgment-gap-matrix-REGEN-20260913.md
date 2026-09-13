# 八术规则判断缺口矩阵（art × verdict judgment gap matrix）

生成：`bun run scripts/art-verdict-judgment-gap-matrix.ts`  ·  2026-09-13T02:04:04.268Z  ·  只读生成，不改引擎 / 测试 / package.json。
product HEAD `null` · classics HEAD `eb4cabe`

## 口径

- **三态** = 满足 / 不满足 / 信息不足。
- **asserted（已断言）**：`tests/engine/art-verdict-judgment-*.test.ts` 里存在真实 `expect(probeXxx(FIXTURE).status).toBe(...)`，按下述强度归因（强 → 弱）：
  `literal`（字面量 ID）＞ `runtime-probe`（**把该断言真实执行一遍**：探针取真实模块导出、夹具实参取真实模块导出值，再读探针自己返回的 `definitionId`）＞ `probe-name`（探针函数名经 PROBES 注册表一对一反查到定义 ID）＞ `loop-const`（`for (const id of WIRED_DEFINITION_IDS_*)` 参数化）＞ `fixture-name`（夹具名推断，弱证据）。
- **not-applicable**：无该分支断言，但 `docs/implementation/art-verdict-judgment-ledger-*.json` 的 `cannot_fail` / `cannot_unknown` / `gaps` 已给出理由（或 cases 模块的 `JUDGMENT_CAPABILITY_*.gap_reason`）。
- **gap**：既无断言、也无诚实理由 —— 这才是真正的缺口。
- 本矩阵度量**判断分支覆盖**，不等于古籍算法正确性验收，也不等于产品交付；`verified:false` 保持不变。

## 总数

| 项 | 数 |
| --- | ---: |
| 分母（pack12 已接线 ID，去掉第十三包 YXJ-*） | **252** |
| 运行时实际接线 WIRED_DEFINITION_IDS_AFTER_PACK12 | 252 |
| 静态解析 ID（13 字面量包 + 2 代码生成包） | 252（与运行时一致：true） |
| 古籍 executable 全部规则 | 258（15 文件，含不属本分母的 YXJ 6 条） |
| 每个 ID 都能在古籍 executable 找到定义 | 是（0 缺失） |
| 每个 ID 都有可调用探针 | 是（0 缺失） |

| 三态分布 | 条数 |
| --- | ---: |
| 三态齐全 | **30** |
| 两侧 | 213 |
| 单侧 | 9 |
| 零侧 | 0 |

> 其中 0 条 ID 依赖 `fixture-name`（弱证据）归因；严格口径（literal / runtime-probe / probe-name / loop-const）三态齐全为 30 条。

## 断言归因质量（真实执行证据）

| 项 | 数 |
| --- | ---: |
| 解析到的 status 断言 | 418 |
| 已归因到单个定义 ID | **418** |
| 其中：真实执行探针归因（runtime-probe） | 356 |
| 其中：探针名注册表反查 + 运行时坐实（probe-name-verified） | 28 |
| 其中：探针名仅静态反查、未坐实（probe-name，弱证据，不计入严格口径） | 0 |
| 其中：夹具名对齐归因（fixture-name，弱） | 0 |
| 真实执行后「执行结果 == 断言值」 | **356** |
| 真实执行后「执行结果 != 断言值」 | 0 |
| 运行时执行不可得（实参表达式 / 未导出夹具） | 45 |
| 仍无法归因到单个 ID | 0 |

> 归因方式：真实 `await import()` 加载 24 个夹具模块与接线模块，共取得 367 个可执行夹具常量；对每条断言真实调用探针一次，以探针返回值 `definitionId` 作为归属、`status` 作为实际判断。归因因此不依赖任何命名约定。

> 夹具重名（第 29 批起单独计量）：21 个常量名被一个以上夹具模块导出。归因本身用真实模块导出的值，不受名字影响；但**同名不等于同盘**——第 29 批新增的 `BIRTH_ZPR_E_06_SAT` 就与 `cases-ming-459.ts` 的同名常量撞车（一个满足盘、一个信息不足盘），矩阵据此报出 1 处假冲突，改名后归零。读这张表时若看到「已断言 ≠ 真实执行」，先查名字是否重名，再怀疑探针。

## 分支处置

| 分支 | asserted | not-applicable（有诚实理由） | gap（缺适用分支） |
| --- | ---: | ---: | ---: |
| 满足 | 252 | — | — |
| 不满足 | 224 | 28 | **0** |
| 信息不足 | 49 | 195 | **8** |

### 古籍 `rescue` 词汇分布（活计数）

本矩阵逐条的「古籍救应」直接取自古籍仓的 `rescue` 字段，实测分布：`{"self":117,"none":106,"unimplemented":30,"ZPR-E-08":2,"ZPR-E-03":2,"ZPR-E-05":1}`。读法必须分清两个值：`unimplemented` = **原文有救应条款、引擎尚未实现**（这才是待实现清单）；`none` = **原文根本没有救应条款**，本条没有可实现的救应（不是待办）。两者混写会把「无可实现」冒充成「待实现」，虚增未决清单。

> 该取值的逐条依据：classics 仓 `docs/closeout/RESCUE-LABEL-AUDIT-20260912.md`——212 条**全取**（不是抽样），逐条读该条自己的原文判定，含逐字引文与理由。普查结果：**has_rescue 105 / no_rescue 106 / unclear 1**，即原本 212 条 `unimplemented` 里**恰好一半**原文根本没有救应条款，已按逐条证据改标为 `none`。同一批普查还量出**关键词筛查两向都不可靠**（含「救/解/制/化」的与不含这些字的条目，假阳 30%、假阴约 49%），所以判据只能是读原文，`rescue` 的值也一样不能按关键词批量推断。

## 按术数分布

| 术数 | 总数 | 三态齐全 | 单/两侧 | gap:不满足 | gap:信息不足 |
| --- | ---: | ---: | ---: | ---: | ---: |
| bazi | 183 | 23 | 160 | 0 | 0 |
| liuren | 23 | 1 | 22 | 0 | 8 |
| liuyao | 21 | 6 | 15 | 0 | 0 |
| ziwei | 12 | 0 | 12 | 0 | 0 |
| qimen | 6 | 0 | 6 | 0 | 0 |
| qizheng | 6 | 0 | 6 | 0 | 0 |
| meihua | 1 | 0 | 1 | 0 | 0 |

## 缺口 ID 清单（摘录，完整清单见 JSON 的 summary）

- **缺「不满足」适用分支**（gap.fail，共 0 条），完整清单在 `art-verdict-judgment-gap-matrix.json` → `summary.gap_fail_ids`；按术数：`{}`；前 12 条：``
- **缺「信息不足」适用分支**（gap.unknown，共 8 条），完整清单见 `summary.gap_unknown_ids`；按术数：`{"liuren":8}`；前 12 条：`DLD-E-02 DLD-E-03 DLD-E-04 DLD-E-05 DLD-E-06 DLD-E-07 DLD-E-08 DLD-E-09`
  - 读法（第 27 批实测）：这 8 条的 `unknown_when` 全是**该条明确声明自己不下的结论**（如 DLD-E-03 的「神杀不动、后不为灾……旺衰与所问未论」），与 qizheng 检查项里逐条附上的 `uncomputed` 同性质——是**边界声明，不是引擎少算了一步**。反过来，`uncomputed` 非空也不能当成「该条应当信息不足」：实测 qizheng 语料里 `status=satisfied` 的 98 条检查**全部**带非空 `uncomputed`。要判某条是否少算，必须读该条自己的 `satisfy_when` / `fail_when` 有没有对应的可判定事实。
- 每个 ID 少哪一侧，看 JSON 行的 `branchDisposition`（`asserted` / `not-applicable` / `gap`）与 `notApplicableReason`。

## 与既有账本的一致性

- `art-verdict-judgment-coverage-index.json`：wired=258、missing=0（只声明「至少一侧」，不声明三态完整）；本矩阵行数=252，与 wired 同源。
- ledger 并集：cannot_fail 15 · cannot_unknown 35 · judgment_covered 20；明细：MING-459(wired=48,cf=4,cu=20,cov=2) / MING-460(wired=48,cf=10,cu=10,cov=8) / MING-476(wired=56,cf=1,cu=5,cov=2) / MING-488(wired=88,cf=0,cu=0,cov=8)

## 消费者（两条通道，必须分开看）

产品里到页面有两条不同的通道，只看其中一条会得出错误结论：

- **通道 A（import 图）**：注册表 `src/engine/art-verdict-definition-ids.ts` 的引用者共 70 个文件，全部落在 `tests/` 与 `src/engine/*cases*.ts`（探针夹具）内；从 app 入口做 import 图可达 **0** 个消费者。
- **通道 B（生成产物）**：同一批古籍定义另被导出为 `src/lib/engine/generated/liuren-source-rules.json`、`src/lib/engine/generated/liuyao-source-rules.json`、`src/lib/engine/generated/qimen-source-rules.json`、`src/lib/engine/generated/qizheng-source-rules.json`、`src/lib/engine/generated/ziwei-source-rules.json`（共 68 条 rule id），由各术引擎 import 后写入盘面 point 的 `ruleIds`，进入免费解释与页面。
- **通道 C（`src/lib/rules/generated/<art>.json`，另一套 ID 命名空间）**：`src/lib/rules/generated/bazi.json`、`src/lib/rules/generated/liuren.json`、`src/lib/rules/generated/liuyao.json`、`src/lib/rules/generated/qimen.json`、`src/lib/rules/generated/qizheng.json`、`src/lib/rules/generated/ziwei.json`，共 643 条规则、其中带原文行号锚点 643 条；由 `src/lib/rules/<art>.ts` import → `catalog.ts` → `matcher.ts`（结构化谓词匹配）→ `EvidencePanel`，显示在 `/chart/bazi` `/chart/liuren` `/chart/liuyao` 等页面。与本矩阵 252 条探针 ID **无交集**（命名空间不同），故不参与逐 ID 的 shipped 判定。校验状态分布：`{"provisional":643}`。

#### 判断本身上没上页面：逐条去向（第 29 批新增）

上表说的「通道 A = 0」只说明**探针注册表本身**没有运行时消费者，不等于判断没到用户面前。按定义 ID 逐条查它有没有进入任何交付给引擎/页面的产物，结果如下：`{"engine-source-rules":68,"none":64,"tiaohou-profile":120}`（按术数：`{"liuyao":{"engine-source-rules":21},"liuren":{"engine-source-rules":23},"bazi":{"none":63,"tiaohou-profile":120},"meihua":{"none":1},"qimen":{"engine-source-rules":6},"qizheng":{"engine-source-rules":6},"ziwei":{"engine-source-rules":12}}`）。

- `engine-source-rules`：定义被导出成 `src/lib/engine/generated/*-source-rules.json`，由各术引擎 import → 盘面 point 的 `ruleIds` → 页面。
- `tiaohou-profile`：定义以 QTB-* 出现在 `tiaohou-profiles.json`（调候 profile 通道），引擎按 profileId 取用。
- `none`：**64** 条在任何产物里都查不到该 ID（`GTJ-E-01、MHY-E-01、SFTK-E-01、SFTK-E-02、SMTH-E-01、SMTH-E-02、SMTH-E-03、SMTH-E-04` …）。也就是说：页面上**看不到这条规则的编号**，它只存在于验证工装里。

不过「看不到编号」不等于「判断没显示」。再查每条声明的引擎字段路径有没有出现在 app 入口可达的模块里（`consumer_scan.judgment_channel_none_field_path_also_absent_count = 0`）：这 64 条**全部**命中，即这些判断赖以成立的值本身是页面代码会读的（例：神煞类走 `chart.rows.find((row) => row.label === "神煞")`，命局类走 `analysis.geju.*` 的免费解读与格局面板）。

> 这个字段路径判定是**文本命中**级证据（弱）：路径字符串出现 ≠ 那个值真的被这条规则读到。它只用来把「连提都没提到」的一批筛出来——现在这一批是空的。另外它自己踩过两次误判，都留在这里当反面教材：①把方括号选择器整段剥掉，键成了 `rows.values`，把 24 条神煞规则误判成「路径不在可达模块里」；②选择器是多值时（`[id=month-chong|month-xing|…]`）拿整串去比，把 ZPR-E-07/E-08 误判。现在按「根路径命中 + 选择器取值任一命中」判定。

| 归口 | 条数 | 说明 |
| --- | ---: | --- |
| 既被探针覆盖、也已进入生成产物（有页面消费） | **68** | 定义本身已到引擎与页面 |
| 只有探针、未进入生成产物 | **184** | 按术数：`{"bazi":183,"meihua":1}` |

- 结论：**68** 条判断的定义确实已由页面/免费解释消费（经通道 B）；另有 **184** 条（主要是 bazi）只有探针与测试，尚未进入生成产物 —— 这部分才是「测试层面的能力证据，不是线上行为」。
- 注意口径差别：通道 B 证明的是**定义已随生成产物进入消费链**，不等于本盘每次都命中该规则；命中与否由引擎按本盘事实计算。本矩阵不据此声称算法正确性或预测有效性。

## 分支声明 vs 可达性：来源写了什么，引擎到不到得了

| 分支 | 已断言 | 原文给了具体条件但引擎到不了（已记理由） | 原文明文声明无该分支 | 无理由裸缺口 |
| --- | ---: | ---: | ---: | ---: |
| 不满足 | 224 | 22 | 6 | 0 |
| 信息不足 | 49 | 195 | 0 | 8 |

- **信息不足只有 49/252（19%）的定义真的能到达**：其余 195 条的 unknown_when 原文写了具体未定情形，但引擎当前产不出该态（每条已记理由，不是裸缺口）。这是「258 条定义 ≠ 完整实现」的量化口径，详见 `docs/implementation/ART-VERDICT-BRANCH-DECLARATION-AUDIT.md`。
- **不满足**：224 条已断言；22 条原文写了「不是本课体/不在本范围」类条件而项目按「本条不适用」记 -- 这些条目的理由逐条可查；6 条原文自己就写明「无独立的不满足分支」，故到不了是**符合来源**而非缺口。
- 不满足不可达清单（已记理由）：DLD-E-10 DLD-E-14 LRZY-E-01 MHY-E-01 XXDC-E-04 XXDC-E-05 XXDC-E-06 ZPR-E-02 ZPR-E-20 ZPR-E-23 ZPR-E-32 ZPR-E-33 ZPR-E-34 ZPR-E-35 ZPR-E-36 ZPR-E-37 ZPR-E-38 ZPR-E-39 ZSB-E-03 ZSB-E-04 ZSB-E-18 ZSB-E-19

## 已知语义缺陷：本矩阵证明不了什么（独立对抗性复核发现）

本矩阵度量的是**探针三分支有没有被断言**，不是**古籍规则的 satisfy_when / fail_when / unknown_when 是否被正确实现**。独立对抗性复核（`docs/implementation/D-REVIEW-GAP-MATRIX-ATTRIBUTION.md`）确认了下面三处缺陷，因此本矩阵的 `asserted` / 三态齐全**不得**当作规则正确性的证据：

1. **`probeQmdE03` 严重失真**（`src/engine/art-verdict-definition-ids.ts:3674-3688`）：该探针从不读 `checks[].status`，只要有 point 和任意 ruleCheck 就返回「满足」。规则 `QMD-E-03` 声明 `fail_when = 本奇在本宫未遇列明六仪`。实测 14,256 张盘中有 **14,047** 张返回「满足」，而引擎自身的 QMD-E-03 ruleCheck 判为 `not_satisfied` —— 即 98.5% 的假阳性。这类探针正属于「字段存在测试」，不是判断。
2. **10/12 条「三态齐全」的第三态不是规则的 unknown_when（注：ZPR 族的这一条已过时——D2 之后 ZPR 探针已改用 engineVerdictStatus 镜像引擎三态；现存同类折叠在 ZSB 族，见第 4 条与 docs/implementation/D5-ZSB-UNKNOWN-FOLD-FIX.md）**：`probeZprE04/05/06/09…16` 写成 `ready ? 满足 : interference ? 不满足 : 信息不足`（如 `:3794-3808`、`:3962-3976`、`:4485-4626`），而引擎自身在「七杀仅藏干」等规则声明的 unknown 情形下由 `interferenceVerdict`（`src/lib/engine/bazi/geju.ts:327-331`）返回「信息不足」，探针却把它折成「不满足」。被断言的「信息不足」其实是**前置条件不成立**（格局不对）那一态，规则真正的 unknown 分支不可达。
3. **capability 解析此前有损**：旧版用文本正则读 `JUDGMENT_CAPABILITY_*`，实测只找到 67/83 条，漏掉单行条目与 `Object.fromEntries` 生成的映射，导致 `ZPR-E-32…39` 这 8 条虽有 `can_unknown:false` + `gap_reason` 却被记成裸缺口。**已修复**为真实 import 读取（现 83 条，gap.unknown 163 → 155）。
4. **ZSB 族折叠：D5 已修**。`probeZsbRule`（ZSB-E-06…E-19 共用）与 `probeZsbE01…E05` 原口径为 `satisfied → 满足；否则 checks.length → 不满足；否则 信息不足`，把引擎的 `unknown` 折成**不满足**（引擎该态的理由串是「当前没有明确日月支持，尚需动爻、伏飞及其他实际支持判断根气」，属事实不足而非已判否）。D5 改为统一的 `engineCheckVerdict`。暴露面（19 个 ZSB 探针 × 120 组日/月输入）：折叠 147 例，集中于 ZSB-E-03/E-09/E-11/E-13/E-14/E-15，其中 ZSB-E-14 的 `不满足` 20/20 全是折叠。D6 已按「先量后改」在同一类写法上做了全族测量（1,248 盘）：`probeDldE15` 又查出 12 例真折叠并已修；`probeQmdE04/E05/E06`（逐条状态齐全）与 `probeDldE11/E12/E13` 实测 0 折叠；`probeDldE14` 的判语是**接线判断**、字段无逐条状态，列为另一待裁定项；D8 补齐余下两类：`probeDldCombination`（DLD-E-16…E-22）实测干净（1,248 盘，`shapeStatus` 只出现 `not_satisfied`/`satisfied`，无一例 `unknown`）；`probeQtbProfile`/`probeQtbM0101` 形状同族但**规则原文把「日干或月令不在本条范围」明文写成 fail_when**（`qiongtong-baojian.json` QTB-M-01-01），故现状正确、不得按形状改成信息不足。**判据在规则原文的 fail_when，不在代码形状**——详见 `docs/implementation/D6-FOLD-SHAPE-AUDIT.md` 与 `D8-COMBINATION-AND-QTB-AUDIT.md`。
5. **归因缺陷已修（D4 §5）**：旧版把 `const r = probeX(夹具)` 记成「变量名 → 文件内全部同名绑定」，于是每个 `it` 块里复用的 `const r` 会互相串台，`expect(r.status)` 被展开成对文件内**每一个** `r` 调用点的断言 —— 虚增断言数并制造出假的「断言与引擎不符」。现改为**同 `it` 块 + 就近**绑定（模块作用域绑定回退为「断言之前最后一次」）。更正前后：断言 401 → 393、归因 383 → 377、真实执行不符 4（全为误报）→ **0**、无法归因 18 → 16。

- 结论：断言数与三态齐全数是**可靠的记账**（第 5 条的归因缺陷修复后）；规则语义正确性必须另行审查。复核已确认的探针缺陷（第 1、2 条）与未决语义（第 4 条）是真实待修项，已登记，不得因本矩阵显示「已断言」而当作已实现。

## 诚实的界限

- 共解析 418 条 status 断言：418 条已归因到单个定义 ID，其中 356 条经真实执行确认「实际判断 == 断言值」；仍无法归因 0 条（实参为表达式或夹具未导出，JSON 的 `status_assertions_unattributed_detail` 逐条列出）。
- 旧版矩阵按「夹具名推断」归因，`BIRTH_ZPR_E_04_SAT` 这类真实命名一律解析失败，导致 418 条断言中 226 条被记为无法归因、并因此得出「三态齐全 = 0」。该归因 bug 已修复（夹具名解析 + 真实执行探针双重归因），本文件的数字为修复后重算结果。
- 探针自身的缺省夹具输出另记 `default-fixture`（`count: 0`、无测试文件），**不计入任何 asserted**：它是运行时事实，不是测试证据。只有测试里真正写出 `.toBe(...)` 的断言才计入。

> 产物：`docs/implementation/art-verdict-judgment-gap-matrix.json`（每 ID 一行）与本文件。只读生成；不 commit / push / merge。
