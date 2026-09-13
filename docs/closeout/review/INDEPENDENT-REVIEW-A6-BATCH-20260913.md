# 独立复核（A6 合 main 门）：逐条「断言 → 证据 → 判定」

- 任务：t8（reviewer）。交付路径按 captain 指定；内容与 `REVIEW-A6-BATCH-20260913.md` 同源，本文件为**最终版**（补充 §5–§8：逐条 diff、token 兼容实测、现场未触碰证明、A8 登记核对）
- 复核对象：**A6 候选提交 `f030441`**（2026-09-13 10:36:22）。我开工时它尚未提交，快照取自当时工作树；提交后逐文件 md5 比对，六个受审文件与我所审内容**逐字节相同**（`liuyao-free-reading.ts`、`ziwei-free-reading.ts`、`chart.ziwei.tsx`、`evidence-panel.tsx`、`reading-input-export.ts`、`ziwei-viewdate-free-reading.test.ts`）。`git show --name-only f030441` = 10 个文件（1 文档 + 5 源码 + 4 测试）
- 复现环境：`/tmp/rev/a6-head`（`git archive 00e98fc`，改动前）、`/tmp/rev/a6-wt`（A6 工作树）、`/tmp/rev/a6-cand`（`git archive f030441`），`node_modules` 软链回真实仓；所有探针/产物/日志在 `classics:docs/closeout/review/a6-batch-20260913/`
- 未 commit / push / merge；未改产品源码；未触碰 contest-evidence / benchmarks / ci.yml / source-link.ts 等他人现场

## 1. 六爻逐爻焦点：**通过**

| captain 的断言 | 我的证据（自跑） | 判定 |
| --- | --- | --- |
| 逐爻焦点真从 1 点变 8 点 | 文档那条调用（`probe8.ts`）：改前 line0–line5 各 **1** 点；改后各 **8** 点。全量扫描（`probe.ts`，1,600 盘 × 6 爻 = 9,600 用例）改前恒 1 点 → 改后 **2–15 点**，非固定 8（8 是那条调用的值） | 通过（并给出更保守的适用范围） |
| 每点都有 `anchored_text` + `sourceRevision` | 8 点中 **7 点**带 `source.kind="anchored_text"` + `sourceRevision`；唯一不带的是**白话总结点** `liuyao:free:main:N`（它本身不是古籍规则点，`ruleIds` 是真实规则 ID：ZSB-E-03/BSZZ-E-01/ZSB-E-06×2…）。全量：改前「至少 1 点无锚点」9,600/9,600；改后「唯一无锚点＝白话点」9,600/9,600，"出现其它无锚点" **0** | 通过（措辞需精确：7/8 直接锚点，第 8 点是白话点） |
| 盘级规则点真回来 | `probe9.ts`（1,600 盘）：总览里 ZSB-E-14 触发 **1,575** 盘、ZSB-E-16 **105**、ZSB-E-17 **32**；改前逐爻焦点缺盘级点 **9,600/9,600**，改后 **0/9,600**。另 `probe11.ts` 专门触发 ZSB-E-09（旬空，需伏神）：550 盘中 **90** 盘触发（如 `liuyao:ZSB-E-09:hidden:hidden:2`），改前 **540/540** 逐爻缺它，改后 **0/540** | 通过（E-09/E-14/E-16/E-17 四项逐项实测） |
| 解读点 ID 不再冒充规则/段落 ID | `probe.ts`：改前总览 1,600/1,600、逐爻 9,600/9,600 用例存在「自身 ID 出现在自己的 ruleIds/paragraphIds」；改后 **0/0**。消费者侧判据来自 `reading-point-source.tsx`：`ruleIds` 非空就渲染成「规则 ID · …」 | 通过 |
| 无回归 | 总览焦点点数分布改前改后均 2–15；逐爻 instanceId 重复 0/9,600；缺爻位分支（lineIndex=9）改前改后都正确（1 点，id `liuyao:free:missing:9`） | 通过 |

## 2. 紫微 scope：**通过**（无新隐性默认）

| captain 的断言 | 我的证据（自跑） | 判定 |
| --- | --- | --- |
| 消除了「恒取第一层」 | `probe2.ts`（11 浏览日 × 3 宫位）：请求的层 available 的 55 例中，改前 **44 例串层**（请求流年/流月/流日/流时一律被换成列表第一层大限/童限），改后 **55/55 正确**。判据是**三重一致**：正文 `当前运限层<层名><该层干支>叠在本宫：流曜X，四化Y`、正文流曜/四化、事实 `运限层/流曜/运限四化` 全部等于该层在 `transitOverlays` 的实测值 | 通过 |
| 没有换个形式留下新默认 | ①缺省（不传 scope）改前会**自行叠第一层**（30/30 带浏览日期的盘），改后逐例按本命层（22/22），且 `item.scopeName === selectedScope?.name` 在 `selectedScope=undefined` 时对真实 overlay（scopeName 恒为字符串）永不命中；②未知层名 → 如实「不在本盘运限列表，信息不足」，不换层；③**在列表但当日不可用**（`probe4.ts`，1920/1960 的大限等 5 例真实数据）：改前静默换成流年，改后「所选运限层X在当前浏览日期不可用，信息不足」+ 事实 运限叠宫=信息不足 + unknowns 带层名，**5/5 正确**；④页面 `scopeIndex` 默认 `-1` 且该状态显示本命盘（`chart.transit.scopes` 实测为空），故「缺省＝本命层」与页面默认**同源**，不是新塞的默认；⑤全部调用点逐个核过：`chart.ziwei.tsx` 4 处、`evidence-panel.tsx`、`reading-input-export.ts` 2 处都带层，`reading-input-export.ts:300` **故意不带**（该分支是 `viewDate===undefined` 的本命盘，无层可叠），判断正确 | 通过 |

## 3. 三个既有测试的修改：**通过（语义保留，未放宽）**

**逐条格式（断言 → 证据 → 判定）**

| 测试文件 | 修改者的断言（口径变化所致） | 我的证据（自跑/自读 diff） | 判定 |
| --- | --- | --- | --- |
| `tests/engine/ziwei-viewdate-free-reading.test.ts` | 「只是把层名显式化，原断言语义保留」 | expect 2→4；旧 2 条断言原文保留，新增 2 条更严（必含 `当前运限层流年`、不得含 `当前运限层大限`）；旧用例×新代码**失败**（`expected X not to equal X`）→ 旧用例赖以通过的唯一来源是被删掉的隐式换层 | **通过** |
| `tests/engine/reading-input-export-link.test.ts` | 「token 加第 4 段，断言未放宽」 | expect 96→97；两条 `focusPosition` 原样断言与「两日 facts 不同」均保留，新增 `toContain("运限层=流年")`；无删除项 | **通过** |
| `tests/engine/c-export-readback-seven-arts.test.ts` | 「回读解析同步第 4 段，断言保留」 | expect 115→116；`rebuildFromFile` 解析与产品 `parseZiweiFocus` 同口径（**必需**，否则重建路径不同源=假通过）；回读一致 + 换日不同两条保留，新增 `toContain("运限层=流年")` | **通过** |

合 main 前必须修的点见 §7（本节无必修项）。

**「无断言被删」的精确对账（自跑 `git diff 00e98fc..f030441 -- tests/`，原始输出 `a6-batch-20260913/tests-diff.txt`）**：4 个测试文件 **+233 / −15** 行；被删的 15 行里去重后只有 **3 行含 `expect(`**，且这 3 行都在新增行里以「同一条断言 + 新 token」形式回来：

```
DEL expect(back.input.focusPosition).toBe(`事业@${viewDate}@${viewHour}`);
ADD expect(back.input.focusPosition).toBe(`事业@${viewDate}@${viewHour}@流年`);
DEL expect(natal.input.focusPosition).toBe("命宫@1990-01-20@12");
ADD expect(natal.input.focusPosition).toBe("命宫@1990-01-20@12@流年");
DEL expect(later.input.focusPosition).toBe("命宫@2024-01-20@12");
ADD expect(later.input.focusPosition).toBe("命宫@2024-01-20@12@流年");
```

其余 12 行删除均为 token 字面量 / `const [palace,date,hour]` 解析行 / 测试标题 / 旧调用参数。另核对：本批**未引入** `.skip` / `.only` / `.todo` / `xit(` / `xdescribe`（同一 diff 里 grep 为空），也**没有**把断言注释掉（无 `+// …expect`）。

断言数只增不减（自跑 `grep -c "expect("`）：

| 文件 | 改动前 | 改动后 |
| --- | ---: | ---: |
| `tests/engine/ziwei-viewdate-free-reading.test.ts` | 2 | **4** |
| `tests/engine/reading-input-export-link.test.ts` | 96 | **97** |
| `tests/engine/c-export-readback-seven-arts.test.ts` | 115 | **116** |

逐条 diff 与判定：

1. **`ziwei-viewdate-free-reading.test.ts`**
   - 旧：`buildZiweiFreeReading(buildZiwei(subject,"1990-01-20",12), { palace:"命宫" })` 与 `…("2024-01-20"…)`，断言 `paragraphs.join("|") not.toBe` + `toMatch(/运限|流曜|四化/)`。
   - 新：两条调用各加 `scope:"流年"`；**保留**原两条断言，**新增** `toContain("当前运限层流年")`、`not.toContain("当前运限层大限")`；标题加「（层名由调用方给出）」。
   - 判定：**通过**。旧用例的「两日不同」唯一来源就是「不传层名 → 自动挑第一层」这一被删掉的错误行为（见下 §4 反证），新用例改为显式层名后仍在验同一件事（换浏览日 → 该层正文改写），并多钉两条更严的断言。断言数 2→4，无删除、无放宽。
2. **`reading-input-export-link.test.ts`**
   - 旧：token `命宫@1990-01-20@12` / `命宫@2024-01-20@12`，断言两条 `input.focusPosition` 原样 + 两日 facts 不同。
   - 新：token 各加 `@流年`；**保留**上述断言，**新增** `expect(later facts).toContain("运限层=流年")`。
   - 判定：**通过**。新断言直接钉住「导出的文件里写的是所选层」，是覆盖扩大；无既有断言被删。
3. **`c-export-readback-seven-arts.test.ts`**
   - 旧：`rebuildFromFile` 用 `const [palace,date,hour] = focusPosition.split("@")`，token `事业@${viewDate}@${viewHour}`，断言 facts 回读一致 + 换日 facts 不同。
   - 新：解析第 4 段（与产品 `parseZiweiFocus` 同口径），token 加 `@流年`，**保留**两条断言并**新增** `expect(facts).toContain("运限层=流年")`、窄化后的「换一日 → facts 必须不同（否则重建一致是空断言）」也保留。
   - 判定：**通过**。测试侧解析与产品侧解析同步是**必需**的（否则重建路径与产品不同源，测试会变成假通过）。
4. `art-free-reading-round1.test.ts` / `art-free-reading-testids.test.ts`（本批**未改**）仍全过：1 条 testid 扫描 + 8 条稳定性断言，说明既有出处/稳定性契约没被这批改动破坏。

**反证（不是靠读 diff 自证）**：把 HEAD 版测试文件配 A6 代码跑，**恰好 3 条失败**，形态全为 `expected X not to equal X`（两个浏览日现在都按本命层 → 正文/事实相同）；把 A6 版测试配 HEAD 代码跑，**13 条失败 / 47**。即：旧断言编码了错误行为，新断言钉住修复（fail-before / pass-after 双向成立）。

## 4. 复跑命令与原始结果（可直接照抄）

```
# A/B 两棵树
mkdir -p /tmp/rev/a6-head && git -C <product> archive 00e98fc | tar -x -C /tmp/rev/a6-head
rsync -a --exclude .git --exclude node_modules --exclude .output --exclude .env \
      --exclude .tanstack --exclude artifacts --exclude benchmarks <product>/ /tmp/rev/a6-wt/
ln -s <product>/node_modules /tmp/rev/a6-head/node_modules   # 同理 a6-wt
cp probe*.ts <tree>/ && cd <tree> && bun probeN.ts            # 探针两棵树各跑一次

# 候选提交自身的门禁（git archive f030441 → /tmp/rev/a6-cand）
./node_modules/.bin/tsc --noEmit                                  # exit=0
./node_modules/.bin/vitest run tests/engine                       # 126 files / 3188 tests passed
./node_modules/.bin/vitest run tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts  # 10/10
```

| 结果 | 证据文件 |
| --- | --- |
| A6 批次 47/47（captain 与我各自跑） | `a6-batch-20260913/…`（我这次：候选提交 10/10 + 三既有测试在 `engine-tests` 内全过） |
| 旧测试×新代码 = 3 failed / 34 passed（37） | `a6-batch-20260913/oldtests-on-newcode.txt` |
| 新测试×旧代码 = 13 failed / 34 passed（47） | `a6-batch-20260913/newtests-on-oldcode.txt` |
| 候选提交 tsc exit 0 | `a6-batch-20260913/cand-typecheck.txt` |
| 候选提交引擎全量 126 文件 / 3188 条全过 | `a6-batch-20260913/cand-engine-tests.txt` |
| 六爻全量 A/B（9,600 用例） | `out-head.json` / `out-wt.json` |
| 盘级点回归 + ZSB-E-09 专项 | `p9-head.json` / `p9-wt.json` / `p11-head.json` / `p11-wt.json` |
| 紫微分支（available/不可用/不在列表） | `p2-*.json` / `p4-*.json` / `p5-wt.json` |
| 跨八术点 ID 冒充 + 后缀碰撞 | `p7-*.json` / `p6-wt.json` |

## 5. 导出 token 加第 4 段：旧的 3 段数据**能解析**，但语义会变（**有条件通过**）

`probe12.ts` 实测（`p12-head.json` / `p12-wt.json`，并用旧代码导出 3 段文件后在新代码下回读）：

| 情形 | 改前（HEAD） | 改后（A6） |
| --- | --- | --- |
| 3 段 token `命宫@2024-06-01@12` | 解析 OK，14 点，运限事实 = `运限层=大限 丁卯 / 运禄 运喜 / …` | **解析仍 OK**，14 点，运限事实 = `运限叠宫=信息不足`（本命层） |
| 4 段 `…@流年` / `…@流月` / `…@不存在层` | 第 4 段被忽略（三者结果与 3 段完全相同，都=大限） | 分别 = 流年 甲辰 / 流月 己巳 / 「不在本盘运限列表，信息不足」 |
| 无日期 token `命宫` | 22 点，无运限事实 | **完全相同**（22 点，无运限事实） |
| 旧文件（3 段，旧代码导出）在新代码下重算 | — | 旧文件存的 `运限层=大限…` ≠ 新代码按同一 token 得到的 `运限叠宫=信息不足` → **不再「回读重建达同一批事实」** |

- **结构/解析兼容：通过**（旧 token 不报错，字段不变，无日期路径完全一致）。
- **语义兼容：不通过（需具名说明）**。影响面已定位：①已导出的旧 JSON 文件若做「回读一致性」比对会不符；②导出文件名/testid 会多一段（`sanitizeExportToken` 把 `@`→`-`，旧 `fateradar-ziwei-命宫-2024-06-01-12.json` → 新 `…-12-流年.json`）；③未发现 DB 侧或页面侧用 stored token 反查一致性（`evidence-db.server.ts` 不存 `focusPosition`；`chart-reading-export.test.ts` 用字面 3 段 token 断言文件名，仍通过）。**建议**：在 `A6-LIUYAO-ZIWEI-FREE-READING.md` 与账本写明「3 段 token 视为『无层信息』，与旧文件事实清单可能不一致」，并把文件名变化告知 page-acceptance（浏览器验收若按文件名找下载会受影响）。

## 6. 该批次是否碰了 contest-evidence 现场：**未碰（通过）**

- `git show --name-only f030441` 只有 10 个 A6 文件；**不含** `benchmarks/**`、`scripts/contest-evidence.ts`、`scripts/lib/contest-evidence.ts`、`tests/contest-evidence.test.ts`，也不含 `ci.yml` / `source-link.ts` / `VERSION_MAP.json`。
- 现场文件仍是修改前状态（mtime 全部 09:59–10:01，早于本批 10:36 的提交）：`benchmarks/mingli-contest-2024/README.md`（M）、`resolutions.template.json`、两个 `contest-evidence.ts`、`tests/contest-evidence.test.ts`（均 ??）。
- 我本轮全部动作只读 + /tmp 重跑，未对上述路径做任何写操作。

## 7. 合 main 前必须修 / 必须登记的点

**必须修（阻断级）：无。** 两条缺陷均真实且已修、被测钉住，候选提交 tsc + 引擎全量绿。

**必须登记（不阻断，但不得静默）：**
1. **【中】(a) 其余五术同类缺陷 7 处仍在**（页面会显示「规则 ID · qimen-free-palace」等）：奇门 `qimen-free-palace`、六壬 `liuren-free-overview`、七政 `qizheng-free-palace`/`qizheng-free-chart-level`、梅花 `meihua-free-tiyong`、小六壬 `xiaoliuren-free-overview`/`xiaoliuren-provenance`。已在账本 A6 remaining 登记（t17 已派）。修法：照抄本次两术的显式构造（风险最小），或改 `free-reading.ts::provenancePoint` 去掉 `[extra.id]` 兜底一次修全（会动八字等既有输出，须先跑全量）。
2. **【低】(b)** `lineRulePoints` 用 `endsWith(":"+targetId)` 分组，因 targetId 自身含冒号（`back-control:main:4` 等）实测 1,280 盘里 **16 例**误纳盘级点；**仅影响顺序**（去重后内容无增减，重复 0/9,600）。建议解析 targetId 后相等比较。
3. **【低】(c)** 「请求的层当日不可用」分支（`scopeUnavailable`）**无测试**，我用 5 例真实数据验证正确；建议补断言（`buildZiwei(subject,"1920-01-15",12)` + `scope:"大限"`）。
4. **【低】(d)** 本命层默认下事实写 `运限叠宫=信息不足`，与正文「未选层」语义不符（且新测试已钉住该字符串，改词需同步改断言）。
5. **【低】(e)** 见 §5 的 token 语义口径说明（写文档即可）。

## 8. 顺带核对：captain 对 A8 硬缺口的登记是否准确（**准确，两处小注**）

- **登记主体正确**：`bazi-anchor-rule-index` 重生成后，我在当前工作树上用生成器重跑（`FATERADAR_CLASSICS_ROOT=<classics> bun scripts/export-bazi-source-rules.ts`）并与工作树文件逐字段比对：183 条规则**除 `sourceRevision` 外完全相同（0 处差异）**——即我 t5 报的「54/183 不一致」**确已修复**；`QTB-M-01-03` 的 fragments 确实已补回 `L0089+L0093+L0099`。
- **三处同步属实**：`source-link.ts::CLASSICS_REV` = `.github/workflows/ci.yml` ref = `bazi-anchor-rule-index.json::sourceRevision` = `c45dfdb4`，另 `tiaohou-profiles.json` 也已同步为 `c45dfdb4`。
- **pin 有效性自核**：我扫出产品全部 **11 个 sourceRevision/CLASSICS_REV/CI ref**，逐个 `git cat-file` + `merge-base --is-ancestor <pin> <remote main>`：**11/11 是真实提交且为当前 remote main（`fe76a0b`）的祖先，0 个不可解析**（与登记「10/10」同集，我多算了一处 tiaohou）。
- **剩余 pin 的「戳记新鲜度」登记也准确**：liuren/liuyao/qimen/qizheng/ziwei source-rules 与 reading-notes 分别落后 1,432–1,683 个提交，账本**登记为 remaining 而非已解决**，与实测一致。
- **578 锚点 0 漂移可复核且成立**：我按 `{file,startLine,endLine,quote}` 全量扫 `src/lib/engine/generated/*`（566 个）+ `reading-notes.json`（12 个）= **578**，在每个文件**自己的 pin** 与**当前 remote main** 两份 blob 上逐条做「空白归一后整句包含」判定：**两侧各 0 处不符**（`scripts/engine_anchors*.py`）。
- **两处小注**：①「原值 3dc9d01 落后 main **1,769** 提交」是**基线相关**的数字（对 `eb4cabe` 为 1,750、对 `fe76a0b` 为 1,783），建议写明所对基线，避免与我的 1,750 看起来互相矛盾；②账本 A6 的 evidence 把 `classics:docs/closeout/review/REVIEW-A6-BATCH-20260913.md` 标成「reviewer-2 独立审查」，(a) 的 7 处也标成「reviewer-2 实测定位」——该文件与那 7 处测量出自 **reviewer（我，t8）**，请更正署名（不影响结论）。

## 9. 结论（一句话）

两条缺陷真实、修复真实有效、三个既有测试**语义保留且覆盖扩大**、导出 token 结构兼容但语义需具名说明、contest-evidence 现场未被触碰；**合 main 建议＝可合**，同步登记 §7 的 (a)–(e)。
