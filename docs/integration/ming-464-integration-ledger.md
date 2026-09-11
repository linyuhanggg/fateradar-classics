# MING-464 古籍集成账本（叠已验收 447 tip，合入 439 JSON 与本轮已审审查稿）

机器可读权威：`docs/integration/ming-464-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-447` @ `77291945bc3d1290099fb6ef617cf07934bfd42d`（独立验收 MING-454 `2b56087ae8f445516ef899c9f45c8f10b37580a6` 通过）
- 独占：`fateradar-multica-ming-464` / `codex/multica-ming-464`
- 合入方式：最小路径 `cherry-pick -x`；禁止整树覆盖；`verified` 保持 false
- **未升** 产品唯一线 `6c1dfa3b` / main / 部署
- **未合入** 452 产品定义 ID；未碰仍在跑的 458–463 独占文件

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 447 验收稿 | MING-454 `2b56087a` | `ming-447-acceptance-review.md` | `cherry-pick -x` | `9d0fae1` | integrated_pending_acceptance |
| 命理约言 NLC JSON+修复说明 | MING-439 `e4870ee` | `mingli-yueyan--nlc-recovery.json` + five-draft-repair.md | `cherry-pick -x` | `0827d1f` | integrated_pending_acceptance |
| 命理约言五段修复审查 | MING-442 `cadfad3d` | `mingli-yueyan-nlc-recovery-five-draft-repair-review.md` | `cherry-pick -x` | `095aaa8` | integrated_pending_acceptance |
| 星學主本 CP5 | MING-443 `057619eb` | `xingxue-dacheng-cp5-review.md` | `cherry-pick -x` | `c0b761c` | integrated_pending_acceptance |
| 奇门 NLC CP5 | MING-444 `1ba8a44e` | `qimen-dunjia-tongzhi-nlc-layouts-cp5-review.md` | `cherry-pick -x` | `2850fb9` | integrated_pending_acceptance |
| 雪心赋全量审查 | MING-445 `4a3b5fe8` | `xuexin-fu-independent-review.md` | `cherry-pick -x` | `478d7f0` | integrated_pending_acceptance |
| 葬书全量审查 | MING-448 `8965ddd9` | `zangshu-independent-review.md` | `cherry-pick -x` | `b27175b` | integrated_pending_acceptance |
| 奇门 NLC CP6 | MING-449 `99421c59` | `qimen-dunjia-tongzhi-nlc-layouts-cp6-review.md` | `cherry-pick -x` | `84cb0f7` | integrated_pending_acceptance |
| 青囊经全量审查 | MING-450 `091c2de6` | `qingnang-jing-independent-review.md` | `cherry-pick -x` | `e5b57f5` | integrated_pending_acceptance |
| 黄帝宅经全量审查 | MING-451 `63917f80` | `huangdi-zhaijing-independent-review.md` | `cherry-pick -x` | `773e976` | integrated_pending_acceptance |
| 撼龙经全量审查 | MING-453 `90ae6a6c` | `hanlong-jing-independent-review.md` | `cherry-pick -x` | `0b9c6ad` | integrated_pending_acceptance |
| 奇门 NLC CP7 | MING-455 `cf154dde` | `qimen-dunjia-tongzhi-nlc-layouts-cp7-review.md` | `cherry-pick -x` | `99414f9` | integrated_pending_acceptance |
| 葬法倒杖全量审查 | MING-456 `4c2b0f99` | `zangfa-daozhang-independent-review.md` | `cherry-pick -x` | `4e4fa27` | integrated_pending_acceptance |
| 青囊奥语全量审查 | MING-457 `4a79f218` | `qingnang-aoyu-independent-review.md` | `cherry-pick -x` | `893cff1` | integrated_pending_acceptance |

## 验证
- `git diff 77291945..contentImportTip`：仅 1 个注解 JSON + 14 个审查/验收/修复 md（账本另计）
- 命理约言 NLC JSON SHA256 = `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`（与目标一致）
- 447 已有约言 CP1–CP3 审查稿 **未覆盖**（blob 与 447 tip 全等）
- 识典 SDZJ0170 / 大六壬 / 秘本 / 星學主本 / 奇门 NLC layouts 注解 blob 与 447 tip **全等**
- 各合入路径 blob 与源 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40410 errors=[]
- 本批触及注解 `verified=true`：**0**；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是本批任一术数全书人工 verified。
- source-reviewed ≠ 人工 verified。
- 不含 452 产品定义 ID；不含 458–463 未完成包；未改 chart.* / 账号 / 支付 / 后端 / 产品唯一线。

## 交付 tip
- 内容合入 tip（14 审查/验收/修复路径 + 1 JSON）：`893cff12f7bfd12323fe05542568c679472e8e2b`
- 账本核对 tip：以本文件提交后 `HEAD` / 交包评论中 `git rev-parse origin/codex/multica-ming-464` / `git ls-remote` 为准（施工分支，非 main）
