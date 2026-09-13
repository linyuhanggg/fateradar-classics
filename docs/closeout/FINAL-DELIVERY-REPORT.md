# FateRadar 全库收尾交付报告（骨架 · 未完成）

> **状态：未完成。本文件是交付报告的结构骨架，不是完成声明。**
> 唯一状态源是 `docs/closeout/DELIVERY_ACCEPTANCE.json`；本节所有「待填」项必须在对应验收条目达到 `pass` 后，
> 用该条目的实测证据填入。**不得**因为本文件已存在就宣告交付完成。
> 生成时间：2026-09-13（goal round 6；round 10 复核过一次 main SHA）。由 captain 维护；成员不直接编辑本文件。

## 0. 交付状态摘要（每次更新时必须如实）

| 项 | 当前值 | 依据 |
|---|---|---|
| 八项总验收 | A1–A8 全部 `working`，**0 项 pass** | `DELIVERY_ACCEPTANCE.json#criteria` |
| classics main | `fcf9a26`（CI success：`fca8d34` 已核实 success；`d36b9cd`/`fcf9a26` 为文档类提交） | `gh run list -R linyuhanggg/fateradar-classics --branch main` |
| product main | `230effd`（CI success） | `gh run list -R linyuhanggg/cosmic-fortune-lab --branch main` |
| 未合 main 的分支成果 | classics 分支领先 main 1 个账本提交；product 分支领先 main 1 个矩阵提交 + **A6 批次未提交**（等 reviewer t8 审查门） | `git rev-list --count origin/main..HEAD` |
| 生产部署 | **未部署**（合入 main ≠ 已部署；部署另等用户授权） | — |

## 1. 可用入口与使用方式（待填）

- 产品预览入口：待填（须在**最新 main** 上实测后写入，并注明端口、实测日期、实测人）。
- 免费解释是否需要登录/付款/AI：待 page-acceptance 在最新 main 实测（t4）后填。已知设计口径：免费解释由已审读内容 + 确定性事实组装，不依赖模型服务（见 `product/docs/FREE_READING_V1.md`）。
- 导出入口与文件名：待填（导出 token 语义见 `product/src/lib/reading-input-export.ts`；A6 批次把紫微导出 token 由 `宫位@日期@时刻` 扩为 `宫位@日期@时刻@运限层`，**向后兼容性须由 reviewer t8 结论确认**）。
- 生时反推入口：不参与首屏；无标注集时**不得**声称排序准确率。

## 2. 全库材料去向与正式入库结果（待填）

引用而非重算：`docs/closeout/FULL-LIBRARY-DISPOSITION-20260912.md`（逐书去向）、`docs/closeout/GAP_LEDGER.json`（台账，**部分字段已登记为过期**，见 CAPTAIN-VERIFICATION-20260913.md）。

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
| `linyuhanggg/fateradar-classics` | `fcf9a26` | success | `dsh/full-library-classics` | 1（账本提交） |
| `linyuhanggg/cosmic-fortune-lab` | `230effd` | success | `dsh/full-library-product` | 1（矩阵）+ A6 批次待审 |

内容钉 ↔ 代码版本：10/10 个生成物 `sourceRevision` 均可解析为真实 classics 提交且为 main 祖先（captain 实测）；
**但 `bazi-anchor-rule-index.json` 的内容与其来源已不一致（54/183），是 A8 硬缺口（t9）**。

## 6. 真实限制与安全清理结果（待填）

- `verified` 全库仍为 `false`（未发生人工验证不得升级；**不要求**全库 verified=true 作为完成条件）。
- 待填：draft 余量的逐项去向、精确未决清单（缺页/不可辨字/版本或语义争议）、明确不支持的学派与能力单列。
- 过程产物清理：只清理无唯一成果且无进程占用的可恢复产物；**未删除任何有唯一成果的工作树**。
- 边界遵守情况：未触碰 `/Users/sync/code/fateradar-classics`、`/Users/sync/code/cosmic-fortune-lab` 的内容（AgentTeams 平台把团队状态目录建在前者下，属平台元数据，captain 从未提交/推送该仓任何内容）。

## 7. 三种未决的分类（交付时必须逐项列出）

1. **实现缺口**（来源与输入足够，必须继续实现）：bazi-anchor 内容漂移、DLD 信息不足分支测试、其余五术同口径核对、原书案例扩面……
2. **证据或语义未决**（不得猜字、不得偷选学派）：缺页、不可辨字、原文未界定判据（如 SMTH 系列未界定术语）。
3. **执行阻塞**（单独修复运行条件）：本会话模型面 goal 工具因 agent preset=`minimal` 不可见（见账本 `goal_state.required_enabling_action`）；成员内部 allowance 与供应商余额分开判断。

> 结项条件：八项均有 `pass` 证据、范围内可自主解决的主要缺陷关闭。**只要还有可自主推进的子项，就继续；不得靠限制清单宣布完成。**
