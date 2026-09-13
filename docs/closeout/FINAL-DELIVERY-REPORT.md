# FateRadar 全库收尾交付报告（骨架 · 未完成）

> **状态：未完成。本文件是交付报告的结构骨架，不是完成声明。**
> 唯一状态源是 `docs/closeout/DELIVERY_ACCEPTANCE.json`；本节所有「待填」项必须在对应验收条目达到 `pass` 后，
> 用该条目的实测证据填入。**不得**因为本文件已存在就宣告交付完成。
> 生成时间：2026-09-13（goal round 6；round 10 复核过一次 main SHA）。由 captain 维护；成员不直接编辑本文件。

## 0. 交付状态摘要（每次更新时必须如实）

| 项 | 当前值 | 依据 |
|---|---|---|
| 八项总验收 | A1–A8 全部 `working`，**0 项 pass** | `DELIVERY_ACCEPTANCE.json#criteria` |
| classics main | **`fe76a0b`**（CI success）；分支 `89d69e3` 领先（措辞统一 + A1 分账 + 账本）**待审后合** | `gh run list -R linyuhanggg/fateradar-classics --branch main` |
| product main | **`f030441`**（A6 批次已过独立审查门并合入，CI **success** 含 playwright e2e）；分支 `20ac19b` 含 A5 候选与 A8 候选 `c300610`，**均未合**（等 t15 / t18 独立复核） | `gh run list -R linyuhanggg/cosmic-fortune-lab --branch main` |
| 未合 main 的分支成果 | classics 分支领先 main 1 个账本提交；product 分支领先 main 1 个矩阵提交 + **A6 批次未提交**（等 reviewer t8 审查门） | `git rev-list --count origin/main..HEAD` |
| 生产部署 | **未部署**（合入 main ≠ 已部署；部署另等用户授权） | — |

## 1. 可用入口与使用方式（2026-09-13 实测填写；浏览器侧以仓库自带 e2e 为证）

### 1.1 本地运行入口

| 用途 | 命令 / 入口 | 说明 |
|---|---|---|
| 开发预览 | `cd product && bun run dev`（Vite） | 默认端口见 `vite.config.ts`；**注意 3210/4173/5186 历史上被占用或用户在用**，起服务前先确认 |
| 生产构建预览 | `FATERADAR_TARGET=node bun run build` → `node .output/server/index.mjs` | 另有 `bun run build:worker`（`dist/worker.mjs`） |
| **端到端验收（推荐）** | `bun tests/e2e/prepare.ts` → `FATERADAR_TARGET=node bun run build` → `bun run build:worker` → `npx playwright test` | 仓库自带 Playwright 配置会**自行起 webServer 到 4173**（`tests/e2e/start-server.sh`），无需另起 dev server；缺前置产物会 `Process from config.webServer exited early` |
| CI 侧 | product CI 的 19 步里已包含上述 prepare/build/build:worker + playwright | 当前 main `f030441` CI **success**（含 e2e） |

### 1.2 免费解释与导出（机器已验的部分）

- **无需登录即可用**：e2e spec `reading-export-eight-arts.spec.ts` 的用例即「**guest export round-trips all eight arts without login**」——CI 在 `f030441` 上通过。
- **导出与版本钉**：`reading-export.spec.ts` 验「guest export round-trips inputs, **provenance and version pins** without login」。
- **选位/时制/岁运同步**：`reading-sync-acceptance.spec.ts` 逐术验「换位置后页面解释与导出 `focusPosition`/points 同步变化」「时制口径行与 `input.timeBasis` 一致」「切大运后盘面与导出同步变化」。
- **运限层**：`transit-chart.spec.ts` 含「**Ziwei transit guides follow each scope**」。
- **导出文件名口径（A6 批次起）**：紫微导出 token 增第 4 段「运限层」，文件名随之多一段（`@`→`-`），例：`fateradar-ziwei-命宫-2024-06-01-12.json` → `…-12-流年.json`；**旧 3 段 token 仍可解析**，但按本命层重建（语义变化，见 §3 的 A6 (e) 条）。
- **生时反推**：**不参与首屏**；无独立标注集时只交付候选比较能力，**不声称排序准确率**。

### 1.3 仍待实测/补齐（不写成已验）

- 八术**逐栏目**的浏览器覆盖清单（哪些栏目未被现有 e2e 覆盖）——**待 page-acceptance 产出**（任务 t4，已把要求降到「纯读 spec 也能交」）；
- **六爻点开一爻后出处块是否仍有古籍锚点**：现有 e2e **未断言**（只断言「选位→导出入口 testid 同步」）；该条由单测覆盖（47/47），浏览器层缺口已具名登记在账本 A6。

- 产品预览入口：待填（须在**最新 main** 上实测后写入，并注明端口、实测日期、实测人）。
- 免费解释是否需要登录/付款/AI：待 page-acceptance 在最新 main 实测（t4）后填。已知设计口径：免费解释由已审读内容 + 确定性事实组装，不依赖模型服务（见 `product/docs/FREE_READING_V1.md`）。
- 导出入口与文件名：待填（导出 token 语义见 `product/src/lib/reading-input-export.ts`；A6 批次把紫微导出 token 由 `宫位@日期@时刻` 扩为 `宫位@日期@时刻@运限层`，**向后兼容性须由 reviewer t8 结论确认**）。
- 生时反推入口：不参与首屏；无标注集时**不得**声称排序准确率。

## 2. 全库材料去向与正式入库结果（待填）

引用而非重算：`docs/closeout/FULL-LIBRARY-DISPOSITION-20260912.md`（逐书去向，§0 已更正两行过期值）、`docs/closeout/GAP_LEDGER.json`（台账，**部分字段已登记为过期**，见 CAPTAIN-VERIFICATION-20260913.md）、`docs/closeout/A1-DRAFT-ACCOUNT-20260913.md` + `review/a1-draft-disposition-20260913.json`。

**draft 余量去向（t7，captain 独立复核为「与注解集合一一对应」）**：2,835 行分账表与 annotations 的 draft 集合**双向一对一**（2,835/2,835 命中、0 多余行），分类：
台账元数据 **1,531**（去向＝保持 draft、不提升、不入审读队列）／实质条目待审 **1,296**／待影印转写 **1**／归档 **7**。
**用户四分类中的第 4 类「已处理但尚未正式入库」实测 0 条** —— 即余量是「审读/转写未做」，不是「数据没搬」。

**A7 口径修正（t14 全文重审，非截断检索）**：30 条 `unimplemented` = **实现缺口 22**（必须实现，跨 QTB 10 / ZPR 6 / SMTH 1 / ZWD 3 / XXDC 2）＋ **证据未决 8**。
22 条**全部落在主要页面**（tiaohou 10、geju 5、shensha 1、yongshen 1、ziwei 3、qizheng 2），已开 t19（先做调候 10）。

**奇门案例差异（t10 归档）**：结构化 1,919 条 → 逐字段一致 **1,842**、差异 **77**（其中 **0 条引擎缺陷**：73 条同书两处印值不一致、4 条原印数与正文一般法冲突）；历史 1,543 条 `starPalaceRaw`「错位」= 比对脚本取错字段（`originPalace`），已修正并有 180/180 构造输入回归测试。


必须写明的实测基线（2026-09-13 captain 实测，并经 reviewer 独立复算）：
- 注解 62,839 = source-reviewed 60,004 + draft 2,835（53 书，其中 15 书有 draft）。
- 可执行规则 258 条 / 15 文件；救应 self 117 / none 106 / unimplemented 30 / 交叉 5。
- 按术：bazi 183 / liuren 23 / liuyao 21 / ziwei 12 / qimen 6 / qizheng 6 / xiaoliuren 6 / meihua 1。
- 待填：draft 四类分账结果（t7）、奇门 308–311 页状态（t2）、《總鈐》666 残格与 14 套未确认底本的精确未决条目。

## 3. 八术能力、规则与案例验证清单（待填）

**逐术汇总表已生成**：`docs/closeout/EIGHT-ARTS-VERIFICATION-MATRIX.md`（脚本汇总：规则数来自 `references/executable/*.json`，探针/断言来自最新 HEAD 重生成的缺口矩阵，案例数来自 `references/cases/source-cases.json`，bookSlug→术 由 executable 文件名映射）。该表**只是汇总，不是验收结论**。关键读数：八字 183 条规则/849 原书案例、奇门 1,920 案例（其中 1,919 可复算）、六壬 23 条但有 8 条信息不足分支 gap、**小六壬 6 条规则不在 252 行矩阵分母内（pack13）**、七政 6 条 3 unimplemented。

- 规则侧：`product/docs/implementation/art-verdict-judgment-gap-matrix.json`（**已在最新 HEAD 重生成**，且与 reviewer 独立镜像重生成逐行 0 差异）；coverage-index wired 258 / missing 0；不满足分支 gap 0；**信息不足分支 gap 8（DLD-E-02～E-09）**。
- 案例侧（三类必须分开，互不折算）：原书可复算 3,568（13 书）／独立已知盘 140 fixture／合成边界（`art-boundary-unknowns-cases-*`）。**当前原书案例只挂接并对账 10 条**，扩面进行中（t6）。
- 待填：八术主要栏目逐项「真实输入 → 引擎计算 → 条件/例外/救应 → 页面解释 → 来源 → 导出」证据链（t4）。

## 4. 八项验收证据（逐项索引，2026-09-13 当前状态）

**八项当前全部 `working`、零 `pass`**（唯一状态源：`DELIVERY_ACCEPTANCE.json#criteria`）。下表只做索引，不新造指标。

| 条目 | 状态 | 已验证的证据（可复现） | 精确剩余 |
|---|---|---|---|
| **A1** 资料去向 | working | 55 行资料包口径（**54 书 + 1 影印伪行**）；注解 **62,839 = source-reviewed 60,013 + draft 2,826**（captain 直扫复算）；draft 2,835→2,826 分账表与注解集合**一一对应**（2,835/2,835、0 多余）；两项具名条目**682 条**（《總鈐》残格 666 逐项 + 未确认影印底本 **16**，已澄清 14 为层级混用） | **独立复核结论**（t22：A1 可否判 pass） |
| **A2** 引文可回溯 | working | reviewer 复核 **643/643 条带 anchor 规则在 pin 与当前 main 双 revision 0 漂移**；t23b1 新增 **9 条** source-reviewed 锚点（逐字符含空格位比对）；页面出口出处接线（六术 PointsPanel） | ①**页面实际展示的引文未逐条回读**；②六爻出处块浏览器层断言缺口 |
| **A3** 判断可追事实 | working | 缺口矩阵在最新 HEAD 重生成（**wired 258 / coverage-index missing 0 / ids_without_probe 0 / 418 断言 / 0 无归因**），并与 reviewer 两次独立重生成**逐行 0 差异** | ①伏神旬空「未算条件」修复（t16 在改）；②消费者侧验收 |
| **A4** 分支测试 | working | 矩阵实测：不满足分支 gap **0**（已断言 224）；信息不足分支 gap **8（DLD-E-02～E-09）** | DLD 8 条 + DLD-E-15 + ZSB-E-15/18/19 零触发（t12） |
| **A5** 三类案例分账 | working | 结构化复算 **1,934 行**（qimen 1,842 一致 / **77 差异，0 条引擎缺陷**：73 同书两处印值不一致 + 4 原印数与正文一般法冲突）；**180/180 构造输入**证明 starPalaceRaw 语义；人读断语对账 **38 条**；三类分账不折算 | ①t15 独立复核 77 条分类；②覆盖面（1,951/3,568 可复算）；③断语级对账仅 38 条 |
| **A6** 八术免费解释 | working | **A6 批次已合 main（`f030441`）且 CI success（含 playwright e2e）**；e2e 覆盖**八术导出回读 + 逐术选位/时制/岁运同步 + 紫微运限层**；guest 无需登录 | ①其余五术 7 处「白话点 ID 冒充锚点」（t17）；②`chart.ziwei.tsx` 12 主题区 token 与 points 不同源（1 行，post-merge）；③六爻出处块浏览器断言 |
| **A7** 已知错误/不单列 | working | 救应标签实测 **self 117 / none 106 / unimplemented 30 / 交叉 5**；30 条 unimplemented **全文重审** → **实现缺口 22**（全部落主要页面：调候 10／格局 5／神煞 1／用神 1／紫微 3／七政 2）+ 证据未决 8；`named_gaps` **42**（11 source-term + 30 unimplemented-reason + 1 verdict-scope） | ①22 条实现缺口（t19 先做调候 10）；②**不支持学派/能力单列清单尚未成文** |
| **A8** 两仓检查/版本 | working | **classics main `5cc8b8b`/`e00c80f`/`12009f9` CI 三连 success**；**product main `f030441` CI success（含 e2e）**；版本钉 11/11 可解析为真实提交且为 main 祖先；578 锚点 0 漂移（captain 自核 489） | ①A5/A8 候选独立复核门（t15/t18）；②其余产物 pin 新鲜度、knowledge-index 生成器未重跑；③网页逐栏目覆盖清单 |

> 读表须知：`working` 不等于「快完成」——每条的「精确剩余」都是**验收项级的缺口**，不是进度百分比。
> 证据出处一律以账本 `evidence` 数组与仓库文件为准；本表不代替账本。


## 5. 两仓 main SHA、版本对应与 CI（每次集成后更新）

| 仓 | main SHA | CI | 工作树分支 | 分支领先 main |
|---|---|---|---|---|
| `linyuhanggg/fateradar-classics` | `fe76a0b` | success | `dsh/full-library-classics` | 1（账本提交） |
| `linyuhanggg/cosmic-fortune-lab` | `f030441` | **success**（含 playwright e2e） | `dsh/full-library-product` | 1（矩阵）+ A6 批次待审 |

内容钉 ↔ 代码版本：10/10 个生成物 `sourceRevision` 均可解析为真实 classics 提交且为 main 祖先（captain 实测）；
**但 `bazi-anchor-rule-index.json` 的内容与其来源已不一致（54/183），是 A8 硬缺口（t9）**。

> 版本块实测时间：2026-09-13 round 34（SHA 复核）／round 16 初版（`git rev-parse` + `gh run list`，非转抄）。
> 两仓**分支均领先 main**：classics 3 / product 2 —— 按方案「独立审核通过后及时合 main」，
> classics 的 A7 具名登记（`d383143`）正在被 reviewer-2 做 id 一致性复核，A6 候选（`f030441`）正在做审查门；
> 两者通过后一次性推 main 并跑各自 CI。

> **首次「过审查门 → 合 main」记录（2026-09-13 round 24）**：product `230effd → f030441`（矩阵重生成 + A6 批次，reviewer-2 结论「可合」且给出 5 条具名缺口 a–e）；classics `c45dfdb → 3b90bbd`（A7 具名登记 + 账本 + 审查产物）。
> 同期**明确排除**未审的 A5 候选 `cf0c1f7`（实测 `merge-base --is-ancestor cf0c1f7 origin/main` = NO）。

## 6. 真实限制与安全清理结果（2026-09-13 实测填写）

### 6.1 真实限制（逐项，不粉饰）

| 限制 | 规模/状态 | 依据 |
|---|---|---|
| `verified` 全库仍为 **false** | 规则与注解两侧均未发生人工影印逐字核验 | 账本 A2/A5；`a1-open-items` 的 `verified:false` |
| 精确未决（可定位、可披露） | **682 条** = 《總鈐》残格 **666**（影印在仓，但**逐格内容归属不可判**：字心距≈70px、相邻字粘连成 200–250px 墨条、邻栏 x 重叠；未定处留〔?〕）+ 未确认影印底本 **16 套**（`sources/facsimile/**` 双路检索 0 命中，**解锁需外部材料**） | `docs/closeout/evidence/a1-open-items-20260913.{json,md}`（captain 独立核：682 条、0 重复、0 空栏、0 条自述已定） |
| **实现缺口 22 条**（必须实现，不得记为不支持） | 全部落在主要页面：调候 10、格局 5、神煞 1、用神 1、紫微组合 3、七政庙宫 2 | 账本 A7；t14 全文重审（非截断检索） |
| 证据未决规则 8 条 | SMTH-E-06/07/08/09/10、DLD-E-09、YXJ-E-04、XXDC-E-05 | 同上 |
| 明确不支持的学派/能力**单列清单** | **尚未成清单**（现只有逐条 `unimplemented` 理由 + 22/8 分类）→ A7 剩余项 | 账本 A7 remaining |
| draft 余量 | **2,835** 条（台账元数据 1,531／实质条目待审 1,296／待转写 1／归档 7）；**「已处理未入库」= 0** | t7 分账 + captain 一一对应复核 |
| 页面展示引文 | **未逐条回读**（锚点集合 643/643 双 revision 0 漂移已验，但「页面实际展示的引用」仍需回读） | 账本 A2 remaining |
| 八字案例覆盖 | 原书案例 3,568 条中可机械复算 1,951，**断语级对账仅 38 条**；奇门 1,919 条只做 5 条断语级对账 | 账本 A5 remaining |
| 生时反推 | **无独立标注集**，只交付候选比较能力，**不声称排序准确率** | `docs/PERSONAL_READING.md`、账本 A6 |

### 6.2 安全与边界（逐条实测/声明）

- **未新增付费服务**；未购买/启用任何收费 API；视觉能力（modlens → codex）**未自行启用**，等用户明示授权（账本 `execution_blockers.B-vision`）。
- **未篡改任何日志**；未重启 Multica 或旧调度器；**未做任何生产部署**（合入 main ≠ 已部署）。
- **未触碰其他任务现场**：`/Users/sync/code/fateradar-classics`、`/Users/sync/code/cosmic-fortune-lab` 的**内容从未被本任务写入或提交**。
  ※ 如实披露：AgentTeams 平台把团队状态目录建在 `/Users/sync/code/fateradar-classics/.agent-teams/`（由会话 cwd 决定），captain **从未 commit/push 该仓任何内容**，该目录仅作平台元数据。
- **未清理任何有唯一成果的工件**：只停过一个 dev server 进程（历史记录）；工作树、分支、证据文件全部保留。
- 另一条车道的在途现场（`benchmarks/mingli-contest-2024/**`、`scripts/contest-evidence.ts`、`scripts/lib/contest-evidence.ts`、`tests/contest-evidence.test.ts`）**全程未动、未提交**。

### 6.3 结论口径

本报告证明的是**文本来源、计算实现与页面一致性**；**不证明传统术数对现实事件的预测有效性**，也不把任何「测试通过」当成预测准确率。
`verified` 未达标不构成本次完成条件的豁免：凡影响主要能力的未决项，在账本里仍为 `blocked`/`working`，不以「已披露」代替完成。

- `verified` 全库仍为 `false`（未发生人工验证不得升级；**不要求**全库 verified=true 作为完成条件）。
- 待填：draft 余量的逐项去向、精确未决清单（缺页/不可辨字/版本或语义争议）、明确不支持的学派与能力单列。
- 过程产物清理：只清理无唯一成果且无进程占用的可恢复产物；**未删除任何有唯一成果的工作树**。
- 边界遵守情况：未触碰 `/Users/sync/code/fateradar-classics`、`/Users/sync/code/cosmic-fortune-lab` 的内容（AgentTeams 平台把团队状态目录建在前者下，属平台元数据，captain 从未提交/推送该仓任何内容）。

## 7. 三种未决的分类（交付时必须逐项列出）

1. **实现缺口**（来源与输入足够，必须继续实现）：bazi-anchor 内容漂移、DLD 信息不足分支测试、其余五术同口径核对、原书案例扩面……
2. **证据或语义未决**（不得猜字、不得偷选学派）：缺页、不可辨字、原文未界定判据（如 SMTH 系列未界定术语）。
3. **执行阻塞**（单独修复运行条件）：本会话模型面 goal 工具因 agent preset=`minimal` 不可见（见账本 `goal_state.required_enabling_action`）；成员内部 allowance 与供应商余额分开判断。

> 结项条件：八项均有 `pass` 证据、范围内可自主解决的主要缺陷关闭。**只要还有可自主推进的子项，就继续；不得靠限制清单宣布完成。**
