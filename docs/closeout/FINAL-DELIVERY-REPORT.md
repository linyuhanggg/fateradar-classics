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

## 1. 可用入口与使用方式（待填）

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

## 4. 八项验收证据（逐项索引，待逐项填证）

| 条目 | 状态 | 证据入口 | 精确剩余 |
|---|---|---|---|
| A1 资料去向 | working | `FULL-LIBRARY-DISPOSITION-20260912.md`、reviewer 独立复算 | 见账本 A1.remaining |
| A2 引文可回溯 | working | reviewer 643/643 锚点**双 revision 0 漂移** | 页面实际展示引文尚未逐条回读 |
| A3 判断可追到事实/规则/理由 | working | 缺口矩阵（最新 HEAD，双次独立重生成一致） | 消费者侧验收 |
| A4 分支测试覆盖 | working | 418 断言 / 28 文件 | DLD-E-02～E-09 信息不足分支、ZSB-E-15/18/19 零触发 |
| A5 三类案例分账 | working | `ART-VERDICT-CASE-KINDS.*` | 原书案例 10/3,568 已对账 |
| A6 八术免费解释 | working | ArtFreeReading 已进 8 个术数路由（captain 实测） | 浏览器逐栏目回读 + 切换不残留 |
| A7 已知错误修复/撤下 | working | `RESCUE-LABEL-AUDIT-20260912.md` | SMTH-E-04/06/07/08/09/10、ZPR-E-06 具名登记 |
| A8 两仓检查+版本对应+集成验收 | working | 两仓 main CI success；**bazi-anchor-rule-index 内容漂移 54/183（硬缺口）** | 见账本 A8.remaining |

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
