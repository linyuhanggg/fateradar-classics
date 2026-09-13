# 独立复核：A6 批次（六爻/紫微消费者缺陷修复）合 main 前审查

- 任务：t8（fateradar-closeout，审阅者 `reviewer`）
- 复核时间：2026-09-13 10:20–11:00 (+0800)
- 审查对象：**A6 候选提交 `f030441`**（`fix(A6): liuyao per-line focus keeps all chart-level points + anchored sources; ziwei free-reading takes explicit luck-layer scope; export token gains 4th segment (candidate for review)`，2026-09-13 10:36:22）。我开工时它还在工作树里未提交，快照取自当时的工作树；提交后逐文件比对，**六个受审文件与我所审内容逐字节相同**（`liuyao-free-reading.ts`、`ziwei-free-reading.ts`、`chart.ziwei.tsx`、`evidence-panel.tsx`、`reading-input-export.ts`、`ziwei-viewdate-free-reading.test.ts` 的 md5 与 `git show f030441:<file>` 全等，A6 测试文件亦同）。其后 HEAD 前进到 `cf0c1f7`（A5 批次），不属本次审查范围。
- 方法：不用成员自报数字。**同一份探针在两棵树上各跑一次**做 A/B：
  - `/tmp/rev/a6-head` = `git archive 00e98fc`（改动前的 HEAD 内容）
  - `/tmp/rev/a6-wt` = 当时的 A6 工作树内容；另用 `git archive f030441` 建 `/tmp/rev/a6-cand` 跑候选提交自身的类型检查与全量引擎测试
  - 三棵树都把 `node_modules` 软链回真实仓，只读；探针、产物、日志全部落在 `/tmp` 与
    `classics:docs/closeout/review/a6-batch-20260913/`
- 未 commit / push / merge；未触碰 `benchmarks/mingli-contest-2024/**`、`scripts/contest-evidence.ts`、`src/lib/rules/source-link.ts`、`.github/workflows/ci.yml` 等他人现场

## 0. 结论

| 审查项 | 结论 |
| --- | --- |
| 缺陷 1（六爻逐爻焦点） | **成立且已修复**。改前该分支恒为 1 个点、0 个带古籍锚点；改后 2–15 个点、锚点齐全，盘级点不再丢 |
| 缺陷 2（紫微运限层） | **成立且已修复**。改前 210 个用例里 120 个「所选层 ≠ 正文层」；改后 0 个，且正文/事实用的是**该层自己的**干支/流曜/四化 |
| 3 个既有测试的修改 | **语义保留，未放宽**。断言数只增不减（2→4、96→97、115→116）；旧测试对新代码恰好 3 条失败，形态都是「expected X not to equal X」——即旧断言本身编码了错误行为 |
| 新测试是否只是自证 | **否**。新测试对改前代码 **13 条失败 / 47**，改后 **47/47 通过**（fail-before / pass-after 已实测） |
| 类型与回归 | 候选提交 `f030441` 自身：`tsc --noEmit` exit 0；`vitest run tests/engine` **126 文件 / 3188 条全过**；A6 测试文件 10/10。另在含在途 A8/A5 改动的当时工作树上跑过一遍：129 文件 / 3230 条全过（后者含别的批次，不作 A6 证据） |
| 合 main 建议 | **可合**（两项修复与测试经独立复核成立），但须同时登记第 4 节 (a)–(e) 四项具名缺口，其中 (a) 是「同一缺陷类在其余五术仍在」 |

## 1. 缺陷 1：六爻逐爻焦点（`liuyao-free-reading.ts`）

### 1.1 全量 A/B（探针 `probe.ts`；1,600 张盘 × 6 爻 = 9,600 个逐爻用例）

| 指标 | 改前（HEAD） | 改后（工作树） |
| --- | --- | --- |
| 逐爻焦点点数 | **恒为 1** | **2–15**（随盘与爻位变化） |
| 逐爻焦点带 `source`+`sourceRevision` 的点数＝0 的用例 | **9,600 / 9,600** | **0 / 9,600** |
| 逐爻焦点缺总览盘级点的用例 | **9,600 / 9,600** | **0 / 9,600** |
| 逐爻焦点里「解读点 ID 写进 ruleIds/paragraphIds」的用例 | **9,600 / 9,600** | **0 / 9,600** |
| 总览焦点同项（解读点 ID 冒充）用例 | **1,600 / 1,600** | **0 / 1,600** |
| 逐爻焦点内部 instanceId 重复 | 0 | 0（`uniquePoints` 去重有效） |
| 总览焦点点数分布 | 2–15 | 2–15（**未变**，无重复膨胀） |

### 1.2 文档所举那条调用（`probe8.ts`，与 A6 文档 §2.1 同一张盘）

```
改前  overview=8 点/7 带锚点   line0..line5 各 =1 点/0 带锚点
改后  overview=8 点/7 带锚点   line0..line5 各 =8 点/7 带锚点
line0 改后实例：liuyao:free:main:1
              + ZSB-E-03(use:main:1)、BSZZ-E-01(solitary:main:1)、
                ZSB-E-06(back-relation:main:1)、ZSB-E-06(restrained-moving:main:1)、
                ZSB-E-14(three-harmony sanhe:inner:水 / sanhe:main:水:1-3 / sanhe:main:金:4-6)
缺爻位分支（lineIndex=9）：改前改后都是 1 点，id 仍为 liuyao:free:missing:9
```

A6 文档写的「1→8 点」对这条调用**属实**；本轮的补充是把它推广成量化结论：**1 → 2–15（不是固定 8）**，并证明总览侧没有回归。

## 2. 缺陷 2：紫微运限层（`ziwei-free-reading.ts` + 路由/导出/EvidencePanel）

### 2.1 A/B（探针 `probe2.ts`：11 个浏览日 × 3 宫位 × 各运限层；判据＝正文与事实是否来自**所选那一层**）

| 请求的层 | 改前 | 改后 |
| --- | --- | --- |
| 该层 available（55 例） | **11 对 / 44 错**（44 例把请求的层换成了列表第一层） | **55 / 55 对** |
| 未指定层（22 例） | 带浏览日期的盘一律自行叠第一层（正文写「当前运限层大限…」） | **22 / 22 按要求按本命层**：正文明确写「本次按本命层解读，没有叠加运限层」，事实 `运限叠宫=信息不足` |
| 层名不在列表（把未知层名传进去） | 忽略参数、照样叠第一层 | 逐例记「信息不足」且 `unknowns` 里带该层名 |

「对」的判据不是文字包含层名，而是**三重一致**：正文 `当前运限层<层名><该层干支>`、正文的 `流曜X，四化Y`、事实里的 `运限层/流曜/运限四化` 都必须等于**该层在 `transitOverlays` 里的实测值**。

### 2.2 额外发现：`available:false` 的层在改前会被**换层顶替**（探针 `probe4.ts`）

扫 14 个浏览日，命中 5 例「该层在列表里但当日不可用」（如 `1920-01-15`、`1960-07-15` 的大限）：

```
改前（请求 大限）：正文写「当前运限层流年己未叠在本宫…」  ← 静默换成流年，一层的数据被搬进另一层
改后（请求 大限）：正文写「所选运限层大限在当前浏览日期不可用，信息不足。」
                  事实 运限叠宫=信息不足；unknowns 含该层名
```

即缺陷 2 的暴露面比 algo-impl 描述的两条更宽（还包括「请求的层当日不可用」这一路），改后的 `scopeUnavailable` 分支**实测正确 5/5**。

### 2.3 隐性默认值检查

- 页面 `chart.ziwei.tsx:195` 的 `scopeIndex` 默认 **-1**，且 :233 在 `scopeIndex < 0` 时用的是**本命盘**（`buildZiwei(subject)`，实测 `transit.scopes` 为空）。所以「缺省＝本命层」与页面默认状态**同源**，不是新塞的隐性默认；改前那种「默认盘却宣称叠了大限」才是错配。
- 逐处调用点已核：`chart.ziwei.tsx` 4 处、`evidence-panel.tsx`、`reading-input-export.ts`（浏览日路径与兜底路径）都带上所选层；`reading-input-export.ts:300` 那处**故意不带**（该分支是 `viewDate === undefined` 的本命盘，无层可叠），判断正确。
- 未发现新的「找不到就随便挑一个」式兜底：三层分支（available / 在列表但不可用 / 不在列表）各自显式处理，未匹配时不回退到别的层。

## 3. 测试修改是否语义保留（本轮重点）

### 3.1 断言只增不减

| 文件 | HEAD `expect(` 数 | 工作树 `expect(` 数 |
| --- | ---: | ---: |
| `tests/engine/ziwei-viewdate-free-reading.test.ts` | 2 | **4** |
| `tests/engine/reading-input-export-link.test.ts` | 96 | **97** |
| `tests/engine/c-export-readback-seven-arts.test.ts` | 115 | **116** |

逐行读 diff：**没有任何断言被删或被弱化**；被改的只是「测试标题 + token 字符串 + 调用参数」。三处改动的性质：

1. `ziwei-viewdate-free-reading.test.ts`：旧用例**只传浏览日期、不传层名**，之所以能通过，正是靠「自动挑第一层（大限）」这个错误行为。新用例显式传 `scope: "流年"`，仍验「换浏览日 → 该层正文随之改写」，并**加了 2 条更严的断言**（必须出现 `当前运限层流年`，且不得出现 `当前运限层大限`）。
2. `reading-input-export-link.test.ts`：token 由 3 段扩为 4 段并**新增**「文件里出现 `运限层=流年`」；原有「两个浏览日事实不同」「focusPosition 原样回读」保留。
3. `c-export-readback-seven-arts.test.ts`：`rebuildFromFile` 同步解析第 4 段（与产品 `parseZiweiFocus` 同口径）；**新增** `expect(facts).toContain("运限层=流年")`；原有「回读重建事实一致」「换日事实不同」保留。

### 3.2 旧测试 × 新代码 = 恰好 3 条失败，失败形态证明「旧断言编码了错误行为」

用 HEAD 版测试文件配工作树代码跑（日志 `a6-batch-20260913/oldtests-on-newcode.txt`）：

```
Test Files  3 failed (3)      Tests  3 failed | 34 passed (37)
FAIL ziwei-viewdate-free-reading  > 本命日与另一流年叠宫正文不同
FAIL reading-input-export-link    > 紫微导出走浏览日期…读回不同
FAIL c-export-readback-seven-arts > focusPosition 自带日期时刻，回读后重建的是同一张流日盘
三条断言失败形态完全一致：expected X not to equal X（两个浏览日现在都按本命层，正文/事实相同）
```

即：旧用例唯一的「不同」来源就是那个被删掉的隐式换层行为；口径改成「层名必须显式」后它们必然失败——**修改是被新契约逼出来的，不是为了让测试好过**。

### 3.3 新测试 × 旧代码 = 13 条失败（证明新测试确实钉住修复，不是自证）

用工作树版测试配 HEAD 代码跑（日志 `newtests-on-oldcode.txt`）：

```
Test Files  4 failed (4)      Tests  13 failed | 34 passed (47)
A6 测试文件 10 条全部失败；3 个既有测试各 1 条失败
```

改后同一批 47/47 通过（我独立重跑，与 captain 结论一致）。**fail-before / pass-after 双向成立**，不存在空断言或恒真断言。

## 4. 需要登记 / 处理的缺口（都会影响「A6 完成」的口径，请勿静默放过）

### (a)【中】同一缺陷类在其余五术仍然存在——已实测定位 7 处

「解读点 ID 被写进自己的 `ruleIds`/`paragraphIds`」这一缺陷，A6 文档 §5.2 已声明「只在本次两术内修掉，其余术是否同类需各自核对」。本轮把它核完了（探针 `probe7.ts`，`ReadingPointSource` 的显示判据：有 `ruleIds` 就显示「规则 ID」）：

| 术 | 残留（点 ID 自己出现在 ruleIds+paragraphIds） |
| --- | --- |
| 奇门 | `qimen-free-palace` ×1 |
| 六壬 | `liuren-free-overview` ×1 |
| 七政 | `qizheng-free-palace`、`qizheng-free-chart-level` ×2 |
| 梅花 | `meihua-free-tiyong` ×1 |
| 小六壬 | `xiaoliuren-free-overview`、`xiaoliuren-provenance` ×2 |
| 六爻 / 紫微 | **0**（本批已修，改前各 1 类） |

后果与本次修掉的完全同类：页面出处块会显示「规则 ID · qimen-free-palace」「段落 ID · meihua-free-tiyong」，把白话点冒充古籍规则/原文锚点（A2「引文能回到准确原文范围」、A6「网页显示与核心事实一致」）。
两种修法（择一，建议按术照抄本次做法，风险最小）：①逐术显式构造点（如本次）；②在 `free-reading.ts` 的 `provenancePoint` 去掉 `ruleIds/paragraphIds` 的 `[extra.id]` 兜底——**一次修掉全部术**，但会动到八字等既有输出，须先跑全量单测并接受若干快照变化。
**建议**：在账本 A6 的 `remaining` 里写成具名缺口（列上表 7 处），或在合 main 前顺手修（工作量很小）。

### (b)【低】`lineRulePoints` 的后缀匹配会误纳盘级点（只影响顺序，不影响内容）

实现用 `instanceId.endsWith(":" + targetId)` 分组。`instanceId = liuyao:<规则ID>:<topic>:<targetId>`，而 `targetId` 自身可能含冒号（如 `back-control:main:4`、`clash-protection:main:N`、`<组id>→<节点id>`）。实测（`probe6.ts`，1,280 张盘）：**16 例**把 `liuyao:ZSB-E-17:day-back-control:back-control:main:4` 之类的盘级点归进了「本爻命中的规则点」组。

影响**仅限排序**：这些点本来也在 `chartLevelPoints` 里，`uniquePoints` 按 instanceId 去重后仍只出现一次（全量 9,600 用例重复数为 0，内容无丢失、无重复）。与代码注释「单独取一次只为顺序」的意图不完全相符。
**建议**：把判据改成解析 `targetId`（`instanceId.split(":").slice(3).join(":")`）后与 `node.main.id` **相等**比较，并加一条断言钉住「本爻组只含 targetId 恰好等于本爻的点」。

### (c)【低】「请求的层当日不可用」分支没有测试钉住

该分支（`scopeUnavailable`）本轮用 5 个真实用例验证正确（见 §2.2），但新测试只覆盖了 available 与「不在列表」，**没有覆盖「在列表但不可用」**。建议补一条（可直接用 `buildZiwei(subject, "1920-01-15", 12)` + `{ palace: "命宫", scope: "大限" }`）：

```
expect(text).toContain("所选运限层大限在当前浏览日期不可用")
expect(facts).toContain("运限叠宫=信息不足")
expect(text).not.toContain("当前运限层")   // 不得换层顶替
```

（该日期实测 `scopes` = 大限:UNAVAILABLE、流年/流月/流日/流时:available，见 `p5-wt.json`。）

### (d)【低】本命层默认下的事实用词

未选层时正文写「本次按本命层解读，没有叠加运限层」，但事实清单写的是 `运限叠宫=信息不足`——「信息不足」与「未选层」不是同一件事（此处并不缺资料）。新测试当前把 `运限叠宫=信息不足` 钉住了，所以改词要同步改断言。建议改为 `运限叠宫=未选层（本命层）` 之类；若决定保留，请在文档里写清口径，避免 A6 复核时被当成「拿信息不足凑数」。

### (e)【低】旧 3 段 token 的导出文件语义变化（向后兼容）

`parseZiweiFocus` 现在把第 4 段当层名；旧文件里的 `命宫@2024-06-01@12`（3 段）读回时 `scope` 为空 → 按本命层重建，而该文件当初是按「第一层（大限）」导出的。也就是说**旧导出文件不再「回读重建达同一批事实」**（现有回读一致性断言只覆盖新 4 段 token，没有旧 token 用例）。新导出不受影响。
**建议**：在 A6 文档或账本里写明「3 段 token 视为无层信息，与旧文件的事实清单可能不一致」，避免后续把旧文件回读不符当成新缺陷；不必为此改代码。

## 5. 顺带复核 captain 的 A3 矩阵重生成（他要求我不要再自己跑；我按「三重比对」核了，未重复全量劳动）

| 产物 | product_head | classics_head | 与本次比对结果 |
| --- | --- | --- | --- |
| captain 提交 `00e98fc`（`git show 00e98fc:…json`） | 230effd | 92f8d62 | 基准 |
| 我 t5 的镜像重生成（`review/art-verdict-judgment-gap-matrix-REGEN-20260913.json`） | null（镜像无 .git） | eb4cabe | **summary 0 差异、252 行 0 差异** |
| 我 t8 在**当前 classics HEAD `8e3c9a2`**、当前工作树内容重跑 | null | 8e3c9a2 | **summary 0 差异、252 行 0 差异** |

即：**三次独立运行（captain 一次、我两次，跨不同路径与不同 classics 提交）在全部 252 行与全部 summary 指标上完全一致**，只有 `product_head/classics_head/generated_at` 三个记录字段不同（镜像无 `.git` 故为 null）。A3 的重生成**核实通过**，无需再跑。

两点时效说明（供归档时写清，不是缺陷）：
1. `92f8d62` 是**本地提交**，不是远端 `origin/main`（`eb4cabe`）的祖先；但其 `references/executable/**` 与 `eb4cabe` **逐字节相同**（`git diff --stat 92f8d62..eb4cabe -- references/executable references/annotations` 为空），故矩阵读到的规则输入与远端 main 等价。归档时建议注明这层等价关系，或改用远端存在的 SHA。
2. 之后 classics 本地又前进了若干提交，其中 `references/executable/{sanming-tonghui,ziping-zhenquan}.json` 只**新增 `named_gaps` 字段**（6 条：`SMTH-E-04/06/07/09/10`、`ZPR-E-06`；规则数 20/39 不变、`rescue` 与 `unknown_when` 均未变），而矩阵脚本**不读** `named_gaps`（`grep -c named_gaps` = 0）——所以矩阵**仍然有效，不需要重跑**；本轮第 3 次重跑也实测确认了这一点。

## 6. 复现入口

- 探针脚本：`classics:docs/closeout/review/a6-batch-20260913/probe{,2,4,5,6,7,8}.ts`（同一份文件拷进两棵 /tmp 树各自跑）
- 原始输出：同目录 `out-{head,wt}.json`（六爻+紫微全量）、`p2-*`（紫微分分支）、`p4-*`（不可用层）、`p5-*`/`p6-*`（scope 表 / 后缀碰撞）、`p7-*`（跨八术点 ID 冒充）、`p8-*`（文档那条调用）
- 日志：`oldtests-on-newcode.txt`（旧测试×新代码 3 失败）、`newtests-on-oldcode.txt`（新测试×旧代码 13 失败）、`cand-typecheck.txt`（候选提交 tsc exit 0）、`cand-engine-tests.txt`（126 文件/3188 全过）、`cand-a6-tests.txt`（10/10）、`engine-tests.txt`（含在途改动的当时工作树 129/3230）、`typecheck.txt`
- 矩阵比对脚本：`verify_captain_matrix.py`、`verify_matrix_current.py`

**仍未审他人在途改动**：复核期间工作树另出现 `src/lib/rules/source-link.ts`、`.github/workflows/ci.yml`、`scripts/export-bazi-source-rules.ts`、`src/lib/engine/generated/{bazi-anchor-rule-index,tiaohou-profiles}.json`、`docs/closeout/VERSION_MAP.json` 的改动（看方向是 A8 版本钉/重导出，与我 t5 的报告同向），以及 classics 侧 `references/executable/*.json` 的 `named_gaps` 在途改动。这些**不在 t8 范围**，本轮未审、也未计入任何结论。

## 7. 复审结论

- algo-impl 报的两条缺陷**真实存在**，修复**真实有效**，两条都不是「改标签」：六爻侧是补点与去伪锚点，紫微侧是按所选层取数并显式处理不可用/不存在两种情形。
- 3 个既有测试的修改**语义保留**：断言数只增不减，无删除与弱化；旧断言之所以要改，是因为它们依赖的隐式换层行为被（正确地）去掉了。
- 新测试**不是自证**：对旧代码 13 条失败、对新代码 47/47 通过；`tsc` 干净、引擎全量 129 文件/3230 条通过。
- **合 main 建议：可合**，但请把第 4 节 (a)–(e) 作为具名缺口登记（(a) 建议顺手修或明确写进 A6 remaining），并把 (b)(c)(d)(e) 一并写进 A6 文档的「仍留给 A6 的部分」。
