# 独立审查（A6 合 main 门 · reviewer-2）：只看实际 diff 与我自己重跑的结果

- 任务：`t11`（fateradar-closeout，`reviewer-2`）。范围＝captain 收窄后的四件事，不发散。
- 审查对象：**A6 候选提交 `f030441c092b5d16122fa0d3f5058e3f496e90d7`**（`fix(A6): liuyao per-line focus keeps all chart-level points + anchored sources; ziwei free-reading takes explicit luck-layer scope; export token gains 4th segment (candidate for review)`，2026-09-13 10:36:22，父提交 `00e98fc`）；10 文件 / +567 −136。
- 审查时点的 Git 事实（本机原始输出）：
  - `git rev-parse origin/main` = **f030441**，`git diff --stat f030441 origin/main` = **0 行**（我 10:38 侦察时 origin/main 还是 `230effd`；`git reflog show origin/main` 首条＝`f030441 … update by push`）→ **该候选在本次审查进行中已被推上 main**。
  - 本地 HEAD = `20ac19b`（`dsh/full-library-product`），`git log origin/main..HEAD` = `cf0c1f7`(A5)、`c300610`(A8)、`20ac19b`(A5b) —— 这 3 个提交未合 main，**不在本次审查范围**。
  - `git log f030441..HEAD -- <A6 六个源文件 + 4 个测试文件>` = **空**：A6 内容自提交后未被再改，我审的对象就是现在 main 上的字节。
- 逐文件 md5（`git show f030441:<file> | md5`，用于绑定审查对象）：
  `liuyao-free-reading.ts dc87bef4…` / `ziwei-free-reading.ts 043a2ca5…` / `reading-input-export.ts eb823deb…` / `chart.ziwei.tsx fd0c4151…` / `evidence-panel.tsx 738c54c4…` / `a6-liuyao-ziwei-free-reading-consumers.test.ts 52cf13b6…` / `c-export-readback-seven-arts.test.ts a1254495…` / `reading-input-export-link.test.ts f1caadfb…` / `ziwei-viewdate-free-reading.test.ts fff29750…` / `A6-LIUYAO-ZIWEI-FREE-READING.md 8997abcd…`
- 方法（不采信任何自报数字）：① 只读实际文件与 `git show f030441` 的实际 diff；② 把 `f030441` 用 `git archive` 导出到 `/tmp/a6clean` 做**干净快照**重跑；③ 把 `HEAD~1` 的两个引擎模块还原到 `/tmp/a6old`（其余保持当前）做**改前/改后同料对比**；④ 自写探针（`/tmp/a6probe`）做全盘扫描与变异检验。
- 边界：未 commit / push / merge；未改产品源码；未触碰 `benchmarks/mingli-contest-2024/**`、`scripts/contest-evidence.ts`、`scripts/lib/contest-evidence.ts`、`tests/contest-evidence.test.ts`；未触碰 `/Users/sync/code/**`。全部探针与日志落在 `/tmp`（产品仓只在 classics 侧新增本报告）。

> 与 t8（`reviewer`）的关系：captain 指定的产出路径 `classics:docs/closeout/review/INDEPENDENT-REVIEW-A6-BATCH-20260913.md` 在我开工期间已被 t8 写为最终版（11:08）。我**不覆盖**，本报告写到独立路径；结论与 t8 的 §1/§2/§3 一致，本文的**新增项**见 §5（主题区导出 token 不同源，t8 未覆盖）与 §7（main 现状与合并边界）。

---

## 0. 结论摘要

| # | 必须判定的事 | 我的判定 | 一句话证据 |
| --- | --- | --- | --- |
| 1 | 3 个既有测试的修改是否语义保留 | **通过（无放宽、无删除有效覆盖，净新增 4 条断言）** | 3 文件 diff 只删 15 行内容行，其中含 `expect(` 的 3 行**原样以新 token 回来**；无 `.skip/.only/.todo`，无注释掉的断言 |
| 2 | 六爻缺陷是否真修 | **通过** | 逐爻焦点 1 点→8 点；2,240 盘 / 13,440 逐爻样本：总览盘级点**一个不缺**、83,316 个盘级点样本**全部带** `anchored_text` + `sourceRevision`；点 ID 不再冒充规则/段落 ID |
| 3 | 紫微运限层 | **通过（未留新隐性默认）** | 旧代码实测「恒取第一层＝大限」且在所选层不可用时**静默换成流年**；新代码 5 层 × 25 盘 123 例 0 串层、9 个超范围日期全部如实记信息不足 |
| 4 | 导出 token 向后兼容 | **结构兼容＝通过；语义变化＝需具名说明（有条件通过）** | 3 段 / 2 段 / 第 4 段空 token 均不报错、字段不变；但 3 段 token 的解释内容由「大限」变为「本命层」，旧文件重算不再同事实 |
| — | 门禁重跑 | **通过** | 干净快照 `f030441`：4 个测试文件 **47/47**、`tsc --noEmit` 退出码 0；全仓 vitest（PATH 带 `~/.bun/bin`）**228 文件 / 3,734 条全过，0 失败** |

**新增的两条「必须登记（不阻断）」**：§5.1 主题区导出 token 与 points 不同源（我独有，1 行可修）；§5.2 其余五术同类点 ID 冒充残留（与 t8 §7(a) 一致）。

---

## 1. 第 1 件（最重要）：3 个既有测试的修改是否语义保留 —— 通过

### 1.1 行级对账（我自跑，不靠叙述）

```
git show f030441 --unified=0 -- tests/engine/ziwei-viewdate-free-reading.test.ts \
  tests/engine/c-export-readback-seven-arts.test.ts tests/engine/reading-input-export-link.test.ts
```
- 删除行 18 行 = 3 行 `--- a/...` 头 + **15 行内容行**；新增行 40 行 = 3 行 `+++ b/...` 头 + **37 行内容行**。
- 15 行删除内容行里，**含 `expect(` 的只有 3 行**，且全部以「同一条断言 + 新 token」形式加了回来：

```
-  expect(back.input.focusPosition).toBe(`事业@${viewDate}@${viewHour}`);
+  expect(back.input.focusPosition).toBe(`事业@${viewDate}@${viewHour}@流年`);
-  expect(natal.input.focusPosition).toBe("命宫@1990-01-20@12");
+  expect(natal.input.focusPosition).toBe("命宫@1990-01-20@12@流年");
-  expect(later.input.focusPosition).toBe("命宫@2024-01-20@12");
+  expect(later.input.focusPosition).toBe("命宫@2024-01-20@12@流年");
```
- 其余 12 行删除＝token 字面量、`const [palace, date, hour] = …split("@")` 解析行、3 条 `it(` 标题、2 处旧调用参数。**没有任何一条断言被删掉或被削弱**；新增 7 条 `expect(` 中 3 条是上述回归、**4 条是净新增**：
  1. `c-export-readback`: `expect(facts).toContain("运限层=流年")`
  2. `reading-input-export-link`: `expect(later…usedFacts).toContain("运限层=流年")`
  3. `ziwei-viewdate`: `expect(later.paragraphs…).toContain("当前运限层流年")`
  4. `ziwei-viewdate`: `expect(later.paragraphs…).not.toContain("当前运限层大限")`（负向断言）
- 同 diff 内 `grep` 无 `.skip` / `.only` / `.todo` / `xit(` / `xdescribe`；无「把断言注释掉」的 `+// …expect`。

### 1.2 逐条：为什么口径变化**必须**改，以及是否等价

| 文件 | 改了什么 | 是否必须 | 我的判定 |
| --- | --- | --- | --- |
| `ziwei-viewdate-free-reading.test.ts` | 两次调用各加 `scope:"流年"`；标题加「（层名由调用方给出）」 | **必须**：旧用例「两日不同」的唯一来源就是被删掉的「不传层名→自动挑第一层」错误行为（见 §3.1 改前实测），不显式给层名则两条调用都会落到本命层而变得相同，测试反而失真 | **通过**：`paragraphs not.toBe` + `toMatch(/运限\|流曜\|四化/)` 原样保留，另加 2 条更严断言 |
| `c-export-readback-seven-arts.test.ts` | `rebuildFromFile` 解析第 4 段并透传给 `buildZiweiFreeReading`；token 加 `@流年`；读取端与 `expect` 同步 | **必须**：该 helper 是「回读重建」路径的测试侧解析器，若不同步第 4 段，重建走本命层 → 与文件里的流年 points 不等，`factsOf(rebuilt)).toEqual(facts)` 必失败 | **通过**：两条原断言（facts 回读一致、换一日 facts 必须不同）都保留，新增 1 条 |
| `reading-input-export-link.test.ts` | 两个 token 各加 `@流年`；两条 `toBe` 同步；新增 1 条 | **必须**：产品 token 格式变了，`toBe` 断言的是回读后的 `input.focusPosition` 原样值 | **通过**：无删除，两日 facts `not.toBe` 保留，新增断言直接钉住「文件里写的是所选层」 |

**两处非阻断小瑕（建议顺手改，不影响判定）**：
- `reading-input-export-link.test.ts` 用例标题仍写「命宫@**本命日** 与 命宫@**流年** 读回不同」，而两个 token 现在**都**是 `@流年`，真正的差别是浏览日期 → 标题已过时（内容正确）。
- `c-export-readback` 的 `rebuildFromFile` 是产品 `parseZiweiFocus` 的**测试侧复制**；第 4 段解析现在存在两份实现，理论上可能各自漂移。产品侧解析器另有真实路径覆盖（`reading-input-export-link.test.ts` 走 `exportReadingReport → buildReadingLinkage → collectZiweiPoints → parseZiweiFocus`），我用探针单独验证过第 4 段确实生效（§4.4），因此不构成覆盖漏洞。

### 1.3 变异检验（证明「没被放宽」不是靠读 diff 自证）

把 `HEAD~1` 的两个引擎模块还原到 `/tmp/a6old`（其余文件同当前），再跑**本批的新测试 + 被改的 ziwei-viewdate 测试**：

```
❯ tests/engine/ziwei-viewdate-free-reading.test.ts (1 test | 1 failed)
❯ tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts (10 tests | 10 failed)
   × 总览带得上的盘级规则点，逐爻焦点一个都不能少
   × 逐爻焦点至少有能回到原文的古籍读法点（改前为 0）
   × 解读点 ID 不再冒充规则 ID / 段落 ID
   × 导出跟选中爻：文件里带得出本术 revision 与古籍锚点
   × 缺爻位仍是信息不足，且不冒充规则/段落锚点
   × 所选层就是正文那层：大限与流年各自指名，互不串层
   × 没选层时按本命层解释，不擅自叠一层
   × 层名不在本盘运限列表：如实记信息不足，不换层顶替
   × 导出 token 带层名：文件里的运限正文与页面同层
   × 解读点 ID 不再冒充规则 ID；缺宫点保持信息不足
 Test Files  1 failed | 1 passed (2)   Tests  11 failed | 0 passed (11)
```
即：**11/11 全部在改前代码上失败、在 `f030441` 上全过** → 新断言对两条缺陷是敏感的，不是空断言；同时说明被改的既有测试「改前通过」所依赖的正是被删除的错误行为。

---

## 2. 第 2 件：六爻缺陷是否真修 —— 通过

### 2.1 改前 / 改后（同一份输入，`/tmp/a6old` 还原 `HEAD~1` 模块 vs 当前 `f030441`）

`buildLiuyao({lines:"○阴阴阴阴阴", dayGanZhi:"甲子", monthZhi:"卯", useRelative:"世爻"})`：

| 指标 | 改前（HEAD~1 模块） | 改后（f030441） |
| --- | --- | --- |
| `buildLiuyaoFreeReading(chart)`（总览） | 8 点 | 8 点（相同集合） |
| `buildLiuyaoFreeReading(chart, {lineIndex:0})`（逐爻） | **1 点**（`liuyao:free:main:1`） | **8 点** |
| 逐爻点里带 `source`+`sourceRevision` | **0** | **7**（第 8 点是本爻白话点，设计上不绑固定段落） |
| 逐爻点 `ruleIds` / `paragraphIds` | `["liuyao-free-line", ZSB-E-01…]` / `["liuyao-free-line"]` ← 点 ID 同时冒充规则与段落 | `ZSB-E-01,ZSB-E-03,…`（真实规则 ID）/ `[]` |
| 总览点 `ruleIds` / `paragraphIds` | `["liuyao-free-overview"]` / `["liuyao-free-overview"]` | `[]` / `[]`（组件退化为「点 ID」标注） |

原始输出（片段）：
```
[OLD] lineFocus.points = 1 | ids = ["liuyao:free:main:1"]
[OLD] lineFocus anchored = 0
[OLD] lineFocus[0] id = liuyao-free-line | ruleIds = ["liuyao-free-line","ZSB-E-01",…] | paragraphIds = ["liuyao-free-line"]
[OLD] overview[0] id = liuyao-free-overview | ruleIds = ["liuyao-free-overview"] | paragraphIds = ["liuyao-free-overview"]
```
消费者侧判据（我实读源码）：`src/components/reading-point-source.tsx:11-18` —— `ruleIds` 非空即渲染成「规则 ID · …」，并明确写「不能把点 ID 写成『规则 ID』」。因此改前 UI 确实会显示「规则 ID · liuyao-free-line」「段落 ID · liuyao-free-line」，改后 `ruleIds=[]` 走「点 ID」分支。**该批的引用是准确的，不是自我加戏。**

### 2.2 全盘扫描（我自己写的探针，2,240 盘 × 6 爻 = 13,440 逐爻样本）

```
[SWEEP] 扫描盘数 = 2240 | 逐爻焦点样本 = 13440
[SWEEP] 盘级规则点样本 = 83316 | 缺锚点/字段不全 = 0
[SWEEP] 逐爻焦点里比总览「多」的点数 = 13440   ← 每例恰好多 1 个 liuyao:free:main:N
[SWEEP] 缺盘级点样例 = []
[SWEEP] 锚点异常样例 = []
[SWEEP] 总览里出现过的规则 ID 数 = 11
[SWEEP] WATCH 规则在总览的触发盘数 = {"ZSB-E-14":1904,"ZSB-E-16":381,"ZSB-E-09":240,"ZSB-E-17":140}
[SWEEP] WATCH 规则在逐爻焦点里的出现次数 = {"ZSB-E-14":40320,"ZSB-E-16":2796,"ZSB-E-09":1440,"ZSB-E-17":840}
```
结论：逐爻焦点＝「总览全部盘级点（除总览白话点）」＋「本爻白话点」这一条**在 13,440 个样本上成立**（既无缺失、也无多余规则点）；83,316 个盘级点全部带 `source.kind="anchored_text"` + 非空 `sourceRevision` + `anchor.file/startLine` + 非空 `quote`（抽样打印见下，引文来自 `sources/fulltext/divination/**`）：
```
anchor sample liuyao:ZSB-E-03:use:main:1 |rev=b8150a72… |quote="自占吉凶者以世爻爲用神，此卦世臨戌土…" |anchor={"file":"sources/fulltext/divination/zengshan-buyi/fulltext.md","startLine":6684,"endLine":6684}
```
（`ZSB-E-09/14/16/17` 四类盘级规则在这批盘里分别触发 240 / 1,904 / 381 / 140 盘，全部在逐爻焦点中出现，未出现「触发却丢失」。）

---

## 3. 第 3 件：紫微运限层 —— 通过（未留新隐性默认）

### 3.1 旧缺陷复现（改前模块，真实数据）

```
[OLD] scope names = ["大限:丁卯","流年:甲辰","流月:己巳","流日:丙申","流时:甲午"]
[OLD] 不传 scope（旧默认）正文片段 = 当前运限层大限丁卯叠在本宫：流曜运禄 运喜，四化太阴化禄、天同化权、天机化科、巨门化忌。
[OLD] 旧代码 + 4 段 token：points = 14 | 正文片段 = 当前运限层大限丁卯叠在本宫：…   ← 第 4 段被忽略
[OLDUN] 2300 年盘 scopes = ["大限:false","流年:true",…]
[OLDUN] 旧代码正文片段 = 当前运限层流年庚辰叠在本宫：…                        ← 请求大限，静默换成流年
```
即旧代码有两层错：**恒取第一层**、以及**所选层不可用时换层顶替**（后者正是「不能把一层的四化搬到另一层」的直接违反）。

### 3.2 改后（f030441）实测

```
[PROBE] 旧算法 find(available) 取到 = 大限 丁卯 ；页面若选流年 = 流年 甲辰
[PROBE] 新口径 scope=流年 正文片段 = 当前运限层流年甲辰叠在本宫：流曜年解，四化廉贞化禄、破军化权、武曲化科、太阳化忌。
[PROBE] 缺省 scope 正文 = 本次按本命层解读，没有叠加运限层；要看某一层请在盘面选择大限/流年等时层。
[PROBE] 不知名层 正文 = 所选运限层「不知名层」不在本盘运限列表，信息不足。不拿别的一层顶替，也不把空档写成没有运限。
[UNSCOPE] 年份 {1901,1950,2130,2200,2300,1850,1500,2400,9999} scopes = ["大限:false","流年:true",…]
[UNSCOPE] 不可用层 大限 → 正文 = 所选运限层大限在当前浏览日期不可用，信息不足。不改看别的运限层，也不把空档写成没有大限或流年。
[UNSCOPE] 不可用层 大限 → unknowns 含层名 = ["所选运限层「大限」在该浏览日期不可用：信息不足"]
[UNSCOPE] 是否串到其它可用层 = false
```
多层全扫（25 盘 × 123 个「当日可用层」样本）：
```
[ZSWEEP] 紫微盘数 = 25 | 层样本 = 123
[ZSWEEP] 串层 count = 0 | 自身层缺席 count = 0 | 缺省非本命层 count = 0
```
「有没有换个形式留下新默认」我的独立检查：
1. 缺省（不传 `scope`）→ 本命层，且正文**显式**写「本次按本命层解读」，不自行叠层；`usedFacts` 记 `运限叠宫=信息不足`（措辞可商榷，见 §6(d)，但不是「悄悄按成立处理」）。
2. 匹配用 `item.scopeName === selectedScope?.name`：`scopeName` 在 `ziwei-reading.ts:474-505` 由 `chart.transit.scopes.map(...)` **一对一**生成且恒为 string，因此 `selectedScope=undefined`（缺省）时不存在「误命中某一层」的可能；`scopes` 与 `transitOverlays` 一对一的构造我也实读过。
3. 「在列表但当日不可用」→ 如实信息不足（9 个真实日期验证），**不换层**（对照组：旧代码在这类盘上换成了流年）。
4. 页面默认 `scopeIndex = -1`（`chart.ziwei.tsx:195`），该状态下 `chart = natal` 且 `scope = chart.transit?.scopes[-1] = undefined` → 与「缺省＝本命层」同源，不是新塞的默认。
5. 调用点：`chart.ziwei.tsx` 5 处（总览 / 宫位详情 / 12 主题 / 导出 points / EvidencePanel）统一走 `ziweiFocus()`；`evidence-panel.tsx` 增 `scope` 透传；`reading-input-export.ts` 的浏览日分支与兜底分支都带层；`reading-input-export.ts:300`（`viewDate===undefined` 分支）**有意不带**层——该分支就是本命盘，判断正确。

---

## 4. 第 4 件：导出 token 第 4 段的向后兼容

### 4.4 实测（真实 `parseZiweiFocus` 路径，即 `exportReadingReport → buildReadingLinkage → collectZiweiPoints`）

```
[PROBE] 旧 3 段 token `命宫@2024-06-01@12`      : points = 14 | focusPosition = 命宫@2024-06-01@12 | 正文含当前运限层 = false | 含本命层 = true
[PROBE] 新 4 段 token `命宫@2024-06-01@12@流年` : points = 14 | 正文含 = 当前运限层流年甲辰叠在本宫：…
[PROBE] 第 4 段为空 `命宫@2024-06-01@12@`       : focusPosition 原样回写 | points = 14（按本命层）
[PROBE] 2 段 `命宫@2024-06-01`                  : points = 1（无 viewHour 的兜底分支，与改前同）
[PROBE] 旧 3 段导出文件回读                     : points = 14（`readBackReadingReport` 正常）
[PROBE] fromPoints 回读 focusPosition/正文同层   : true（页面 points → 导出文件，页面与导出同源成立）
```
判定：
- **结构兼容＝通过**：旧 token（3 段 / 2 段 / 第 4 段空）都不报错，字段语义不变，`focusPosition` 原样回写；旧 JSON 文件仍能 `readBackReadingReport`。
- **语义变化＝需具名说明**：同一 3 段 token 的解释内容由改前的「大限叠宫」变成改后的「按本命层解读，没有叠加运限层」；因此**旧文件与「按同一 token 重算」的结果不再逐字一致**（这属于口径变更，不是崩坏；改后的写法在两种情形下都不编造）。
- **影响面我已自查**：`grep` 全仓未发现任何「把持久化的 focusPosition 再喂回 `buildReadingLinkage`」的路径（`src/routes/api`、`src/lib/*.server.ts` 无 `focusPosition` 存储；`src/lib/export/reading-report.ts:203` 只是把文件里的字段当字符串读回），导出文件名/testid 会因第 4 段多一段（`sanitizeExportToken` 把 `@`→`-`）。→ 建议在 `A6-LIUYAO-ZIWEI-FREE-READING.md` 与账本写明「3 段 token 视为『无层信息』」，并告知 page-acceptance 下载文件名变化。

---

## 5. 我独有的新增发现（t8 报告未覆盖）

### 5.1 【中·1 行可修】`chart.ziwei.tsx` 12 主题区的导出 token 仍是 `宫位` 名，而它的 points 已带所选层 → **文件内 token 与 points 不同源**

位置：`src/routes/chart.ziwei.tsx:837-846`（12 主题分区）。该处 `points={reading.points}` 来自 `buildZiweiFreeReading(chart, ziweiFocus(topic.palace))`（**带层**），但 `focusPosition={topic.palace}`（**不带日期、不带层**）。实测（我复刻该调用点）：

```
[TOPIC] 主题区导出文件: input.focusPosition = "夫妻" | points = 5
[TOPIC] 主题区导出文件 正文含当前运限层流年 = true
[TOPIC] 同 token 重算: points = 5 | 正文含当前运限层 = false
[TOPIC] → 文件内 points 与 token 重算结果是否一致 = false
[TOPIC] 总览区 token `夫妻@2024-06-01@12@流年` 重算 正文含当前运限层流年 = true
```
即：**同一个文件里，points 说「当前运限层流年」，而它的 `input.focusPosition` 只写「夫妻」，用该 token 重算得到的是本命层**。对照命格总览区的导出（`chart.ziwei.tsx:787-790`，token 带 `@日期@时刻@层`）重算完全同层。
- 性质：**不是本批引入的**（该 token 本来就不带日期/时刻，本来就无法复原同盘），但本批「页面与导出同源」的口径**同样适用于它**，而本批只改了总览区；文档 §3 表格「导出 token 由 `宫位@日期@时刻` 扩为 …」把范围写得过大。
- 严重度：**不阻断**——产品内没有任何路径会从导出的 token 反查重算（见 §4），文件自身 points 与页面一致；风险落在「回读一致性」类校验/未来功能。
- 建议修法（1 行，与总览区同表达式）：
  ```tsx
  focusPosition={
    comparisonOnly || scopeIndex < 0
      ? topic.palace
      : `${topic.palace}@${date}@${resolvedViewHour}${scope?.name ? `@${scope.name}` : ""}`
  }
  ```
  或者明确登记为 remaining 并在文档里限定「导出 token 带层」只覆盖命格总览区。

### 5.2 【中·同 t8 §7(a)】其余五术的同类「点 ID 冒充规则/段落 ID」仍在

我实读证据：`src/lib/engine/free-reading.ts:26-47` 的 `provenancePoint` 在未显式给 `ruleIds`/`paragraphIds` 时**兜底写成 `[extra.id]`**（`insufficientPoint` 同）；本批只把六爻/紫微改成显式构造，`qimen-free-reading.ts:93/108`、`liuren-free-reading.ts:51/82`、`qizheng/meihua/xiaoliuren-free-reading.ts` 仍在调用兜底版本（八字另有自己的 `insufficientPoint` 实现）。→ 与本批同源缺陷类别，**不在本批范围**，与 t8 §7(a) 一致（其列出 7 处并称已派 t17）；我未逐处复算数量，仅确认「兜底仍在、调用点仍在」。

---

## 6. 其他必须登记（不阻断）项（与 t8 §7(b)-(e) 交叉）

- (b)`lineRulePoints` 用 `endsWith(":"+targetId)` 分组可能误纳盘级点，仅影响**顺序**——我未独立复算 t8 的 16/1,280；我的等价检查证明**内容层面无增无减**（§2.2：逐爻＝总览盘级点 + 1 个白话点，13,440/13,440）。
- (c)`scopeUnavailable` 分支**本批无测试**：我用 9 个真实超范围日期验证正确（§3.2）；建议补一条断言（如 `buildZiwei(subject,"1920-01-15",12)` + `scope:"大限"`）把它钉住。
- (d) 缺省本命层时 `usedFacts` 写 `运限叠宫=信息不足`，与正文「本次按本命层解读」的语义略有张力（好在正文不误导）；该字符串已被新测试钉住，改词需同步改断言。
- (e) 见 §4 的 3 段 token 语义口径说明（写文档即可）。

---

## 7. 门禁重跑原始输出（全部我自己跑的）

### 7.1 干净快照（`git archive f030441` → `/tmp/a6clean`，不含工作树里他人未提交内容）

```
$ npx vitest run tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts \
    tests/engine/ziwei-viewdate-free-reading.test.ts \
    tests/engine/c-export-readback-seven-arts.test.ts \
    tests/engine/reading-input-export-link.test.ts
 ✓ tests/engine/c-export-readback-seven-arts.test.ts (20 tests) 444ms
 ✓ tests/engine/reading-input-export-link.test.ts (16 tests) 210ms
 ✓ tests/engine/ziwei-viewdate-free-reading.test.ts (1 test) 62ms
 ✓ tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts (10 tests) 4ms
 Test Files  4 passed (4)      Tests  47 passed (47)

$ npx tsc --noEmit ; echo TSC_EXIT=$?
TSC_EXIT=0            # 输出为空
```
同一组 4 个文件在**产品工作树**上跑也是 `4 passed / 47 passed`；在产品仓 HEAD = `20ac19b`（含其后 3 个未审提交）时再跑一次仍是 `4 passed / 47 passed`（11:35），且 `git log f030441..HEAD -- <A6 文件>` 为空 → A6 内容在后续提交中未被改动。

### 7.2 全仓（产品真实布局）

```
$ PATH="$HOME/.bun/bin:$PATH" npx vitest run        # 产品工作树，HEAD 当时为 20ac19b（A6 内容未变）
 Test Files  228 passed (228)      Tests  3734 passed (3734)      Duration 187.53s
```
（含其他成员在本工作树里未提交的新测试文件，因此条数高于 A6 文档自报的 3,675；A6 文档「222 files / 3675 tests passed」与我这次「222 passed files（不带 bun 时）」同一量级，可对得上。）

**环境坑（写清楚，免得别人误判为回归）**：本 harness 的默认 PATH **不含 `~/.bun/bin`**，此时 `tests/load-script.test.ts`、`tests/release-script.test.ts`、`tests/integration/load-seed.test.ts` 会因 spawn `bun` 失败（`status=null`）而报 3 条失败。把 `~/.bun/bin` 加进 PATH 后：
```
$ PATH="$HOME/.bun/bin:$PATH" npx vitest run tests/load-script.test.ts tests/release-script.test.ts tests/integration/load-seed.test.ts
 Test Files  3 passed (3)      Tests  15 passed (15)
```
另：在 `/tmp` 镜像里跑全仓还会额外失败 5 条（`c-export-provenance-version-seven-arts`、`tiaohou-rescue`，因找不到同级 classics 仓 / pin）——在产品真实布局下这 2 个文件：
```
$ PATH="$HOME/.bun/bin:$PATH" npx vitest run tests/engine/c-export-provenance-version-seven-arts.test.ts tests/engine/tiaohou-rescue.test.ts
 Test Files  2 passed (2)      Tests  27 passed (27)
```

### 7.3 静态门禁（并证明「不是我引入的」）

```
$ npx prettier --check <6 个改动文件>
[warn] src/lib/engine/ziwei-free-reading.ts
[warn] src/lib/reading-input-export.ts
→ 这两份文件的 HEAD~1 版本（/tmp/a6fmt 内）同样 warn：**改前既存漂移**，本批未新增（也未顺手修，符合文档说明）

$ npx eslint <6 个改动文件>            # 5 条 prettier/prettier
  ziwei-free-reading.ts:155  ← HEAD~1 同行（换行后 117 行）已存在
  reading-input-export.ts:144/145/146/151 ← HEAD~1 同行（144/151）已存在
→ 5 条全部为改前既存，非本批引入
```

### 7.4 禁区检查

```
$ git show --name-only --format="" f030441
docs/implementation/A6-LIUYAO-ZIWEI-FREE-READING.md
src/components/evidence-panel.tsx
src/lib/engine/liuyao-free-reading.ts
src/lib/engine/ziwei-free-reading.ts
src/lib/reading-input-export.ts
src/routes/chart.ziwei.tsx
tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts
tests/engine/c-export-readback-seven-arts.test.ts
tests/engine/reading-input-export-link.test.ts
tests/engine/ziwei-viewdate-free-reading.test.ts
→ 不含 benchmarks/mingli-contest-2024/**、scripts/contest-evidence.ts、scripts/lib/contest-evidence.ts、tests/contest-evidence.test.ts（无人现场被动）
```

---

## 8. 合并操作边界（重要：现在 main 已经是 f030441）

- 我审查时点：`origin/main == f030441`（reflog 显示本轮 push）；`dsh/full-library-product` 本地 HEAD 已到 `20ac19b`，比 main **多 3 个未审提交**（`cf0c1f7` A5、`c300610` A8、`20ac19b` A5b）。**这 3 个不在我的审查范围**，需要各自的审查门。
- 若 captain 后续再推 main：**只推/只取你确认过的提交**，不要 `git add -A`。当前工作树里仍有**不属于 A6、也不属于我审查范围**的改动，例如
  `M benchmarks/mingli-contest-2024/README.md`、`M docs/implementation/ART-VERDICT-SOURCE-CASE-RECOMPUTE.{json,md}`、`M scripts/art-verdict-source-case-recompute.ts`、`M tests/fixtures/liuyao-source-components.json`、`?? benchmarks/mingli-contest-2024/resolutions.template.json`、`?? scripts/contest-evidence.ts`、`?? scripts/lib/contest-evidence.ts`、`?? tests/contest-evidence.test.ts`、`?? tests/engine/{bazi-source-case-seat-batch2,liuyao-source-case-use-reconciliation,meihua-source-components}.test.ts`、`?? tests/fixtures/{bazi-source-case-seat-batch2,meihua-source-components}.json`。
- 我本轮未写产品仓任何文件；本报告是 classics 侧新增文件。

---

## 9. 复现清单（我实际用过的路径与命令）

- 干净快照：`git -C <product> archive f030441 -o /tmp/a6clean.tar && tar -xf /tmp/a6clean.tar -C /tmp/a6clean && ln -s <product>/node_modules /tmp/a6clean/node_modules`
- 改前同料：`cp -R <product>/src /tmp/a6old/src`；`git show f030441^:src/lib/engine/{liuyao,ziwei}-free-reading.ts > /tmp/a6old/src/lib/engine/…`；其余顶层条目软链回产品仓（**注意先删掉误软链进来的 `vitest.config.ts`**，否则 vitest 会读产品配置）
- 探针（写在 `/tmp/a6probe`，用 `--config /tmp/a6probe/vitest.config.ts --root /tmp/a6probe` 运行，alias `@ → <product>/src`）：
  `independent.probe.test.ts`（点数/锚点/冒充/层/ token）、`sweep.probe.test.ts`（2,240 盘）、`ziwei-sweep.probe.test.ts`（25 盘 × 全层）、`unavailable-scope.probe.test.ts`（9 个超范围日期）、`topic-export.probe.test.ts`（主题区 token 同源）
- 变异：`/tmp/a6old/mutation.vitest.config.ts` + 本批新测试文件（旧模块 + 新测试 → 11 failed）
- 日志：`/tmp/a6review/{probe,sweep2,zsweep,unavail,old,oldun,topic,mutation,clean-4files,clean-tsc,product-full-suite-bun,prettier,eslint}.log`

---

## 10. 结论

四条必须判定的事：**三条通过、一条「结构兼容通过 / 语义变化需具名说明」**；无必修项（A6 两项缺陷真修且有变异敏感的测试钉住，三个既有测试语义保留且覆盖扩大，门禁在干净快照上 47/47 与 `tsc` 0 退出，全仓 228 文件 / 3,734 条全过）；须登记两条非阻断项（§5.1 主题区导出 token 与 points 不同源——1 行可修或写明口径；§5.2 其余五术同类残留）与 §6 的 (b)–(e)；另需注意 `origin/main` 已经是 `f030441`，而本地分支仍多出 3 个未审提交。

**最终判定：可以合 main。**（本批 `f030441` 内没有必须修的点；它事实上已在 main 上，我这一门不要求回滚。若 captain 要「零残留」，唯一需要作为后续提交处理的就是 §5.1 那一行。）
