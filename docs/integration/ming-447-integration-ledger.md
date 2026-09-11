# MING-447 古籍集成账本（424 tip 上合入本轮已审审查稿，不含 439 JSON）

机器可读权威：`docs/integration/ming-447-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-424` @ `85d172a68d47508db9a1cb19a32c89eeceae977a`（独立验收 MING-431 `8a5b692` 通过）
- 独占：`fateradar-multica-ming-447` / `codex/multica-ming-447`
- 合入方式：最小路径 `cherry-pick -x`；禁止整树覆盖；`verified` 保持 false
- **未升** 产品唯一线 `6c1dfa3b` / main / 部署
- **未合入** MING-439 JSON；未碰仍在跑的 442/443/444/445 独占文件

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 424 验收稿 | MING-431 `8a5b692` | `ming-424-acceptance-review.md` | `cherry-pick -x` | `a8e9ba3` | integrated_pending_acceptance |
| 果老全量审查 | MING-425 `b10ae285` | `guotian-jing-independent-review.md` | `cherry-pick -x` | `8d9ac07` | integrated_pending_acceptance |
| 天玉全量审查 | MING-426 `f06a687` | `tianyu-jing-independent-review.md` | `cherry-pick -x` | `8ba6f00` | integrated_pending_acceptance |
| 疑龙全量审查 | MING-441 `297638d` | `yilong-jing-independent-review.md` | `cherry-pick -x` | `52cce6c` | integrated_pending_acceptance |
| 入地眼全量审查 | MING-440 `4c12db7f` | `rudi-yan-quanshu-independent-review.md` | `cherry-pick -x` | `a4d2614` | integrated_pending_acceptance |
| 星學主本 CP1 | MING-422 `d83e4b4c` | `xingxue-dacheng-cp1-review.md` | `cherry-pick -x` | `bc56ecd` | integrated_pending_acceptance |
| 星學主本 CP2 | MING-429 `d9db9829` | `xingxue-dacheng-cp2-review.md` | `cherry-pick -x` | `b192969` | integrated_pending_acceptance |
| 星學主本 CP3 | MING-433 `b3516875` | `xingxue-dacheng-cp3-review.md` | `cherry-pick -x` | `906bb18` | integrated_pending_acceptance |
| 星學主本 CP4 | MING-437 `e0d8bc0c` | `xingxue-dacheng-cp4-review.md` | `cherry-pick -x` | `83ad16f` | integrated_pending_acceptance |
| 奇门 NLC CP1 | MING-421 `839e284` | `qimen-dunjia-tongzhi-nlc-layouts-cp1-review.md` | `cherry-pick -x` | `e0c6b03` | integrated_pending_acceptance |
| 奇门 NLC CP2 | MING-430 `05dd8bf7` | `qimen-dunjia-tongzhi-nlc-layouts-cp2-review.md` | `cherry-pick -x` | `0f0b8cf` | integrated_pending_acceptance |
| 奇门 NLC CP3 | MING-434 `e5a58e81` | `qimen-dunjia-tongzhi-nlc-layouts-cp3-review.md` | `cherry-pick -x` | `6597c7a` | integrated_pending_acceptance |
| 奇门 NLC CP4 | MING-438 `884c4acc` | `qimen-dunjia-tongzhi-nlc-layouts-cp4-review.md` | `cherry-pick -x` | `ba5b1a1` | integrated_pending_acceptance |
| 命理约言 NLC CP1 | MING-423 `61fe88b` | `mingli-yueyan-nlc-recovery-cp1-review.md` | `cherry-pick -x` | `a19ae0b` | integrated_pending_acceptance |
| 命理约言 NLC CP2 | MING-428 `d6a0714e` | `mingli-yueyan-nlc-recovery-cp2-review.md` | `cherry-pick -x` | `9fa5f47` | integrated_pending_acceptance |
| 命理约言 NLC CP3 | MING-435 `9153372` | `mingli-yueyan-nlc-recovery-cp3-review.md` | `cherry-pick -x` | `0ca6fb6` | integrated_pending_acceptance |

## 验证
- `git diff 85d172a..contentImportTip`：仅上述 16 个审查/验收 md（账本另计）
- 全部 `references/annotations/**` blob 与 424 tip **全等**（58/58，含秘本 397 修复后对象）
- 识典 SDZJ0170 SHA256 仍 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261`
- 大六壬 SHA256 仍 `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a`
- 秘本 SHA256 仍 `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347`
- 各审查稿 blob 与源 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批触及注解 `verified=true`：**0**；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是本批任一术数全书人工 verified。
- source-reviewed ≠ 人工 verified。
- 不含 MING-439 命理约言五段 draft 回改 JSON；不含 442–445 在跑文件。

## 交付 tip
- 内容合入 tip（16 审查/验收稿）：`0ca6fb698b84521193c0451a5a0e1992923b6e77`
- 账本核对 tip（首次 push）：`c3a911ac03d9be483c2243d6b9e86cd8228338cf`
- 远端 tip：以交包评论中 `git rev-parse origin/codex/multica-ming-447` / `git ls-remote` 为准（施工分支，非 main）
