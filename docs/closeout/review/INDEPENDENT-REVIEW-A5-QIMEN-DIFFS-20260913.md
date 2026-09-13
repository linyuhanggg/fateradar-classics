# 独立复核（A5 · 奇门 77 条差异分类）：只看实际文件与我自己的重跑

- 任务：`t15`（fateradar-closeout，`reviewer-2`）。审查对象＝product 候选 **`cf0c1f7`**（`feat(A5): source-case wiring batch2 + structured recompute (1934 rows; qimen 1842 match/77 diff all classified) + 28-case human-read verdict reconciliation`，父 `f030441`）。
- 被核主张来自 A5 交付与其自报：77 条差异分类为「73 条经典仓已登记来源冲突 / 72 条同输入 sibling 佐证 / 4 条原印数与一般法冲突」；落宫口径三数「1,888／1,917 对 raw、1,684 寄坤、376 原宫」。
- 我的方法（不采信自报）：① 直接读候选提交的产物 `docs/implementation/ART-VERDICT-SOURCE-CASE-RECOMPUTE.json`（1,934 行 batch2）**用自写脚本重算每一个计数**，并与文件内的汇总块逐项对照；② 4 条未解释项逐条取 `fields/altMatches/sourceConflictFields/differences` 原始值，并回到 classics 原书行核对；③ 用**引擎直算**（`buildQimenLayout`）交叉校验；④ 核对 `skippedByInputBasis`/`skipReasons` 的理由是否与引擎入口/案例输入相符；⑤ 做「案例集合 ↔ 产物行集合」的会计对账。
- 边界：未 commit/push/merge；未改产品源码；未碰 `benchmarks/mingli-contest-2024/**`、`scripts/contest-evidence.ts`、`scripts/lib/contest-evidence.ts`、`tests/contest-evidence.test.ts`；未碰 `/Users/sync/code/**`。探针/脚本/日志在 `/tmp/a6review`、`/tmp/a6probe`。

---

## 1. 分类计数的可复现性 —— **三数复现为真，但 73 与 72 不是两个独立集合**

我自算（`/tmp/a6review/a5-recompute.py`，只读候选 JSON 的 1,934 行）：

```
=== 我算 byArt ===   {"meihua":{"total":2,"matchedAll":2,"withDiff":0},"liuyao":{"total":13,"matchedAll":13,"withDiff":0},"qimen":{"total":1919,"matchedAll":1842,"withDiff":77}}
差异总行数 = 77 | 文件 differenceCount = 77
=== 我算差异分类 ===
onRegisteredSourceConflict = 73
engineMatchesSiblingPrint  = 72
两者都成立                  = 72        ← 关键：72 全部落在 73 之内
两者都不成立（未解释）       = 4
冲突∪佐证 的去重行数         = 73
=== 文件里 differenceClassification ===
{"total":77,"onRegisteredSourceConflict":73,"engineMatchesSiblingPrint":72,"unexplained":4}
```

**判定：73 / 72 / 4 三个数逐项复现，文件汇总块与我自算完全一致。** 但必须写明口径，否则会被读成「73+72=145 条有据」：

- **实际是**：77 条中 **73 条**在经典仓有 `conflictingFields` 登记（原书同一输入在不同页/表印值不同）；其中 **72 条**（＝ 72/73 的子集）还能找到「同一输入的另一处印值恰好等于引擎值」的 sibling 佐证；**并集仍是 73**；**剩下 4 条两者皆无**（＝ `unexplained`）。所以正确读法是「**73 条已定位来源冲突（内含 72 条有 sibling 佐证），4 条未定位**」，不能把 73 与 72 相加。
- 分布（我自算）：差异集中在少数页 —— `P131:30`、`P198:6`、`P144:2`、`P195:2`、`P233:2`，其余 34 页各 1 条（合计 77）。字段级不符共 104 处：`chiefStar 30`、`starPalaceRaw 29`、`doorPalaceRaw 25`、`chiefDoor 20`（一行可含多字段）。
- 抽样核对了分类逻辑本身（`scripts/art-verdict-source-case-recompute.ts:721-767`）：口径是「`sourceConflictFields` 非空 → 登记冲突；否则按 `dun|ju|timePillar` 找 sibling，若 sibling 的印值==引擎值 → 佐证」。我对 `P131` 首 3 条实测其 `conflictingFields=["chiefStar","chiefDoor"]` 且 `sibling=["chiefStar","chiefDoor"]`，与分类口径一致；`P272`（阴5局丁亥时）实测 `门 印5/算9`，而**总表 P266 同输入印 9**（与引擎一致）→ 这是典型的「同书两处印值冲突」，分类正确。

---

## 2. 4 条未解释项逐条（P266／P273／P312／P319）—— **判定：方向未定，不能写成「原印数与一般法冲突」**

四条（我自算，与产物逐字段一致）：

| # | caseId | 原书出处（段落 ID / 行） | 输入 | 原印 | 引擎直算 | 其他三字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `QMTZ-NLC-P266-C04-R04` | `qimen-dunjia-tongzhi:nlc-layouts:P266:L053-L063` / `L2518`（原文行「**酉九八**」，block 标题「芮死」） | 阴遁 5 局 丁酉 时 | `starPalaceRaw=9`、`doorPalaceRaw=8` | **starPalaceRaw=8**、doorPalaceRaw=8 | chiefStar 天芮✓ chiefDoor 死门✓（4 字段比 3 对） |
| 2 | `QMTZ-NLC-P273-I5-丁酉` | `…:P273:L006-L008` / `L2717-L2719`（同印「九八」） | 同上 | 同上 | 同上 | 同上 |
| 3 | `QMTZ-NLC-P312-C04-R03` | `…:P312:L053-L063` / `L2927`（「禽死**三三**」） | 阴遁 8 局 丙申 时 | `starPalaceRaw=3`、`doorPalaceRaw=3` | **starPalaceRaw=1**、doorPalaceRaw=3 | chiefStar 天禽✓ chiefDoor 死门✓ |
| 4 | `QMTZ-NLC-P319-I8-丙申` | `…:P319:L006-L008` / `L3065-L3067`（同印「三三」） | 同上 | 同上 | 同上 | 同上 |

我的独立核查（这些都是可复现的**事实**）：
1. **不是「同书两处冲突」**：四条全部 `sourceConflictFields = null`；且每组两条（总表 + 逐时条）**印值互相同意**（九八/九八、三三/三三），所以「原书自己印了两个不同值」这条路不成立。
2. **也不是口径差异**：四条 `altMatches` 均为 `{originPalace:false, adjustedStarPalace:false}` —— 原印值既不等于引擎的**原宫**，也不等于中五**寄坤**后的落宫。
3. **引擎侧我直算复核**（`buildQimenLayout`，我的探针输出）：
   ```
   阴5局丁酉时 -> chiefStar=天芮 chiefDoor=死门 starPalaceRaw=8 starPalace(寄坤)=8 originPalace=2 doorPalaceRaw=8
   阴8局丙申时 -> chiefStar=天禽 chiefDoor=死门 starPalaceRaw=1 starPalace(寄坤)=1 originPalace=5 doorPalaceRaw=3
   ```
   即：丙申那条引擎星落宫=1、门落宫=3，而原印把**星栏也写成 3**（与门栏同数）；丁酉那条引擎星门皆 8，原印星栏写 9。
4. **同表其余行几乎全对**：阴遁 5 局总表同页其余时支（乙未 6、丙申 7、己亥 4、壬寅 1 …）与阴遁 8 局同表各行都与引擎一致；全库 `starPalaceRaw` 一致率 1,888/1,917（98.5%）。→ 说明本表口径整体成立，这 4 条是**离群**。
5. **对照组：什么叫「能定性」**——`P123-Y3-DETAIL-28`（原印「丁卯/禽死/六三」）我直算 `阳3局辛卯时 → 禽死 starPalaceRaw=6 doorPalaceRaw=3`，**与原印期望完全吻合**；而该条按六十甲子槽位应为辛卯（其自身 `inputStatus=source-uncertain` 也是这么写的）。这才是有证据的定性（原印时柱写错槽位）。相形之下，§2 的 4 条**没有**同类证据可用（既无 sibling，也非槽位错位：它们的时柱与同表逐时条一致）。

**结论（第 2 块）→ 【已按 captain 提示补核后改判：成立】**：
> ⚠️ 本节初版判定为「方向未定·不能写成原印数与一般法冲突」，理由是我没找到一般法推导。**该判定已作废**：按 captain 提示补查 `tests/engine/qimen-source-layouts.test.ts::methodDifferences`（第 22-29 行）与案例元数据 `notes` 后，**这 4 条的定性有既有依据，且我独立复核通过**——详见 §7「补核与改判」。下面 (a)(b) 两条只作为「若要进一步证明旧表异常来源」的可选深化，不再是收尾前置条件。
- **(a) 回原影印读图**：`文瑞本` PDF 266 / 273 / 312 / 319 的四格（`nlc-layouts.md` L2518、L2717-2719、L2927、L3065-3067 对应格）逐格核对是 9/8 还是 8/8、3/3 还是 1/3（OCR 层面的单字差异最可能）；
- **(b) 一般法推导**：按本书正文的转宫/寄宫规则推出该局该时的值符落宫，再判是原印错还是引擎口径不适用。
在（a）或（b）完成前，这 4 条应保持产物里的「未解释」状态，**登记措辞改为「方向未定·待读图/待一般法推导」**。

---

## 3. 落宫口径三数 —— **复现为真，并做了引擎直算交叉校验**

我自算（同样从 1,934 行原始字段重算，不读汇总块）：

```
=== 我算 starPalaceSemantics ===
comparable = 1917
matchesRawLandingPalace(match) = 1888
matchesAdjustedStarPalace(寄坤) = 1684
matchesOriginPalace(原宫) = 376
=== 文件里 starPalaceSemantics ===
{"comparable":1917,"matchesRawLandingPalace":1888,"matchesAdjustedStarPalace":1684,"matchesOriginPalace":376}
```
四个数与自报**完全一致**。口径含义（我实读 `scripts/…:584-612` 与引擎返回键）：`starPalaceRaw` = 值符星**落宫**（中五保留 5）、`starPalace` = 中五**寄坤**后落宫、`originPalace` = 值符星**原宫**；主比对用 raw，另两数作为「口径差异 vs 真实分歧」的判别栏。
引擎直算交叉校验（我的探针，独立于产物）：
```
阳1局乙丑时 -> chiefStar=天蓬 chiefDoor=休门 starPalaceRaw=9 starPalace(寄坤)=9 originPalace=1 doorPalaceRaw=2
```
即 captain 给的 `starPalaceRaw=9、doorPalaceRaw=2` **我算得同值**；同时可见「原表两列数跟着**落宫**走、值符原宫恒为 1」这一口径说明与此盘相符（原宫=1，落宫=9，原表记 9）。→ 第 3 块**通过**。

---

## 4. 有没有被掩盖的差异 —— **理由大部分成立；另发现 1 条会计缺口（新）**

### 4.1 `skippedByInputBasis` / `skipReasons`（我逐类核对）

```
文件 skippedByInputBasis = {"meihua-hexagram":3,"liuyao-line-symbols":1,"ziwei-component":178}，skipReasons 182 条，逐类与我自算的「案例数 − 产物行数」一致：
  meihua-hexagram: 案例 3  | batch2(meihua) 行 2   （3 条全跳）
  liuyao-line-symbols: 案例 14 | batch2(liuyao) 行 13（1 条跳）
  ziwei-component: 案例 178 | batch2(ziwei) 行 0   （178 条全跳）
  qimen-layout: 案例 1920 | batch2(qimen) 行 1919（**1 条既无行、也无跳过理由**）
```

- **`ziwei-component 178` 的理由成立（两半我都核了）**：
  - 「案例自身也登记缺完整农历/公历生日」→ 我自算：178/178 条 input 都缺 `year/month/day/hour`，样例 `{"lunarMonth":1,"hourBranch":"子"}`（`classics:references/cases/source-cases.json`）；
  - 「引擎只有整盘入口，无『按组件取命身宫/紫微星位』的入口」→ 我实读 `product:src/lib/engine/ziwei.ts`：导出仅 `buildZiwei(subject, viewDate?, viewHour?)`（L107），无组件入口。
  → 这是**已披露的引擎能力缺口**（与 A6 那批「消费者入口」同源），不是掩盖。**判定：理由成立。**
- **`meihua-hexagram 3` 的理由成立**：`buildMeihua(input: MeihuaInput)`（`src/lib/engine/meihua.ts:129`）只吃 `yearBranch/lunarMonth/lunarDay/hourBranch`，而三条案例给的是 `{upper,lower,moving}`（如 `{upper:"乾",lower:"坤",moving:1}`）→ 「无按上下卦＋动爻直接装卦的入口」属实。**判定：理由成立。**
- **`liuyao-line-symbols 1` 的理由成立**：`zengshan-buyi:ZS-LY-L0393` 的 input 只有 `{linesBottomUp:[…]}`，缺 `dayGanZhi/monthBranch`；`buildLiuyao` 需要日柱（缺失即抛 `GanZhiInputError`）。**判定：理由成立。**

### 4.2 **新发现：1 条奇门案例在产物里「两头都不在」**

`qimen-dunjia-tongzhi:QMTZ-NLC-P123-Y3-DETAIL-28`（文瑞本阳3局逐时条·原题丁卯）：
- 它不在 `batch2.rows`（qimen 1,920 → 1,919 的那 1 条），**也不在 `skipReasons`（182 条里没有它）**；其 `canRecompute=false` 的理由只写在 classics 案例文件自身的 `unavailable/inputUncertainty` 里。
- 我核了它被排除的合理性：该条排在庚寅之后，按六十甲子槽位应为**辛卯**，同页「丙辛日」组也不配丁卯；而我直算**阳3局辛卯时 = 禽死、starPalaceRaw=6、doorPalaceRaw=3**，与该条记录的期望字段（禽死/六三）**完全吻合** → 排除是对的（原印时柱疑似写错槽位），只是产物/报告的会计没把它登记进去。
- 影响：小（不改变 77/1842 的差异结论），但属于「被掩盖的差异」类——A5 的 `ART-VERDICT-SOURCE-CASE-RECOMPUTE.md` 只写了「未接入：meihua-hexagram 3、liuyao-line-symbols 1、ziwei-component 178」，**没有提这 1 条 qimen**。建议补登（一行即可，理由引用案例文件）。

---

## 5. 复现清单（我实际跑的命令/脚本）

- 计数复算：`python3 /tmp/a6review/a5-recompute.py`（byArt / 77 / 73-72-4 / starPalaceSemantics 全部自算，日志 `/tmp/a6review/a5-recompute.log`）
- 4 条明细：`python3 /tmp/a6review/a5-four.py`（字段级 印值/引擎值/match、altMatches、differences）
- 同表对齐：`python3 /tmp/a6review/a5-table.py`（阴5/阴8 局逐行印值 vs 引擎值）
- 会计对账：`python3 /tmp/a6review/a5-accounting2.py`、`a5-skip.py`（案例集合 ↔ 行集合 ↔ skipReasons）
- 案例输入核对：`python3 /tmp/a6review/a5-cases.py`、`a5-skipcases.py`、`a5-p123.py`
- 引擎直算：`npx vitest run --config /tmp/a6probe/vitest.config.ts --root /tmp/a6probe qimen-layout`（`/tmp/a6probe/qimen-layout.probe.test.ts`，日志 `/tmp/a6review/qmlayout.log`）
- 原书行核对：`classics:sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md` L2512-L2524、L2717-L2719、L2927、L3065-L3067、L4664-L4666
- 引擎入口核对：`product:src/lib/engine/ziwei.ts:107`、`src/lib/engine/meihua.ts:129`、`src/lib/engine/liuyao.ts:365`

---

## 6. 结论

第 1 块（73/72/4）**复现为真**，但须写明「72 ⊂ 73，并集 73，未解释 4」，不得相加；第 2 块 4 条**经补核后判定成立**（见 §7：原印 9/3 与同书正文「值符加地盘时干」一般法冲突，我独立复算地盘丁在艮八、丙在坎一，与引擎 8/1 及元数据 notes 逐字相符；但措辞应是「原印与一般法冲突、实现按一般法并保留原印」，**不是**「原印数错」——旧表异常来源尚未证明）；第 3 块三数 **1,917/1,888/1,684/376 复现为真**，并用引擎直算（阳1局乙丑 starPalaceRaw=9、doorPalaceRaw=2）交叉验证口径；第 4 块 skip 理由**逐类成立**（178 ziwei-component 两半理由我都核过），另发现 **1 条奇门案例（P123-Y3-DETAIL-28）在产物会计里两头都不在**（排除合理但未登记）。

**最终判定：该差异项可以按已披露限制收尾**（77 条差异无需改引擎、不阻塞 A5 判 pass），**但收尾前必须先改两处登记**：① 4 条未解释项的措辞按 §7 的改判写成「原印沿用旧表/未知排法，与同书正文一般法（值符加地盘时干）冲突；实现按一般法，原印保留对照」，**不要写成「原印数错」**（旧表异常来源未证），并指明依据：元数据 `notes` + 产品侧 `qimen-source-layouts.test.ts::methodDifferences`（printed 9/byMethod 8、printed 3/byMethod 1）+ 本报告 §7 的地盘一般法复算；② 补登 `qimen-dunjia-tongzhi:QMTZ-NLC-P123-Y3-DETAIL-28`（1 行，理由可直接引用该案例自身的 `inputStatus/inputUncertainty` 与我算出的「辛卯时=禽死六三」）。

---

## 7. 补核与改判（回应 captain 的两点新增要求）

### 7.1 「P266/P273/P312/P319 的定性」—— **成立（我改判）**，三重证据

captain 让我打开「实际元数据 + 既有 `qimen-source-layouts.test.ts::methodDifferences`」。我照做后，初版的「方向未定」判定**作废**，理由如下（全部我自跑/自读）：

1. **产品侧既有裁决（可执行证据）**：`product:tests/engine/qimen-source-layouts.test.ts:22-29`
   ```ts
   // Same-edition table and prose method disagree in these two inputs (four
   // occurrences). Preserve printed expectations; assert the declared hour-stem
   // method separately. Evidence and adjudication: docs/QIMEN_SOURCE_LAYOUTS.md.
   const methodDifferences = {
     "…QMTZ-NLC-P266-C04-R04": { printed: 9, byMethod: 8 },
     "…QMTZ-NLC-P273-I5-丁酉": { printed: 9, byMethod: 8 },
     "…QMTZ-NLC-P312-C04-R03": { printed: 3, byMethod: 1 },
     "…QMTZ-NLC-P319-I8-丙申": { printed: 3, byMethod: 1 },
   };
   ```
   测试对这 4 条同时断言「原印值 == printed」与「引擎算值 == byMethod」→ 把「原印 9/3」与「一般法 8/1」**双向钉死**。我自跑该文件：`tests/engine/qimen-source-layouts.test.ts (1926 tests) ✓`（连同 qimen/qimen-methods/qimen-star-palace-semantics 共 **1,971 passed / 4 files**）。
2. **案例元数据 notes 已写明推导**（`classics:references/cases/source-cases.json`，4 条各自的 `notes`）：「同版图文现已齐证：定义要求**值符加地盘时干**，且注明阴遁同例；外圈**地盘丁八**，与本条星九不一致。实现沿一般法，原印数不改；没有证明旧表的异常来源，不称两处原表互异。」（丙申那条写「**地盘丙在坎一**，通用排法得到星落宫 1」）。
3. **我独立复算一般法（不经元数据）**：用 `buildQimenLayout` 读引擎的**地盘层**：
   ```
   阴5局地盘 = {"1":"壬","2":"辛","3":"庚","4":"己","5":"戊","6":"乙","7":"丙","8":"丁","9":"癸"}  → 时干丁在艮8 → 一般法星落宫 8 = 引擎 starPalaceRaw=8 ✓（原印 9 与之冲突）
   阴8局地盘 = {"1":"丙","2":"丁","3":"癸","4":"壬","5":"辛","6":"庚","7":"己","8":"戊","9":"乙"}  → 时干丙在坎1 → 一般法星落宫 1 = 引擎 starPalaceRaw=1 ✓（原印 3 与之冲突）
   ```
   → 元数据 notes 的「地盘丁八／地盘丙在坎一」与引擎地盘层**逐字相符**，且与 §2 的引擎直算（8/1）一致。

**改判后的准确表述（建议口径）**：这 4 条＝「**同版表法（原印 9/3）与同书正文一般法（值符加地盘时干 → 8/1）冲突**；实现按正文一般法，原印值保留供对照」。**不宜写成「原印数错」**——元数据自己声明「没有证明旧表的异常来源」；也不宜写成「同书两处印值冲突」（两纸一致，`conflictingFields` 为空）。

### 7.2 完全独立的重算（**不读产物任何分类字段**）—— 三个数逐条复现

我另写探针（`/tmp/a6probe/a5-independent-recount.probe.test.ts`）：只读 `classics:references/cases/source-cases.json`，对每条 qimen 案例**自己调引擎算 4 个字段**并逐字段比较，再按「案例自身 `conflictingFields` 非空」与「同 `dun|ju|timePillar` 的另一条印值是否等于引擎值」**自己分类**：

```
[A5X] 我自算 qimen 可复算条数 = 1919 | 全一致 = 1842 | 有差异 = 77      （产物自报 1919 / 1842 / 77）
[A5X] 我自算 onRegisteredSourceConflict = 73                            （产物 73）
[A5X] 我自算 engineMatchesSiblingPrint  = 72                            （产物 72）
[A5X] 两者都成立 = 72 | 两者都不成立 = 4                                 （产物 4）
[A5X] 未解释 id = [P266-C04-R04, P273-I5-丁酉, P312-C04-R03, P319-I8-丙申]
```
→ 从**原始来源**（案例数据 + 引擎）重算出的 6 个数与产物/自报**完全一致**，结论不变：72 ⊂ 73、并集 73、未解释 4。

### 7.3 顺带发现的登记项（非阻断，且**不在 A5 候选里**，属 product 既有状态）

`qimen-source-layouts.test.ts` 注释引用的裁决文档 **`docs/QIMEN_SOURCE_LAYOUTS.md` 在 product 仓中不存在**：该文档只在未合并提交 `d13540a`（新增）与 `83bbfd1`（改写，+19 行，正是引入 `methodDifferences` 的那次）上；而把这份测试搬到 main 基线的迁移提交 `00d4abb` 只带走了 `tests/engine/qimen-source-layouts.test.ts` 与 `tests/fixtures/qimen-source-layouts.json`（其 stat 里没有该文档）。→ 建议（不作为 A5 收尾条件）：把该文档随迁移补进 main，或把注释里的路径改为实际存在的落点（案例 notes 已承载推导，指向它亦可）。

---

**末句判定（§7 补核后，取代 §6 的表述）：该差异项可以按已披露限制收尾** —— 77 条差异不需改引擎、不阻塞 A5 判 pass；收尾前须落地两项登记（① 4 条按 §7.1 的口径写成「同版表法 vs 正文一般法冲突，实现按一般法、原印保留对照」，不得写成「原印数错」；② 补登 `QMTZ-NLC-P123-Y3-DETAIL-28`），另有一项非阻断建议（§7.3 的 `docs/QIMEN_SOURCE_LAYOUTS.md` 缺失）。

