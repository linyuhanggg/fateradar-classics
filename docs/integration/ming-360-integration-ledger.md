# MING-360 古籍集成账本（351 tip 上合入已审 SDZJ0170 CP3）

机器可读权威：`docs/integration/ming-360-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-351` @ `306aaecb4ad54aa923d89999b97a5a4b0cdb0e94`（审查 MING-355 已通过）
- 独占：`fateradar-multica-ming-360` / `codex/multica-ming-360`
- **未改写** 351 已合入 CP6/8/9 审查稿 / `ming-351-*` 账本 / `wuxing-jingji.json`
- **未开** CP4（remaining 170）

## 合入前差集（SDZJ0170 注解）
- 基线 600 段（CP1+CP2）
- 源 tip MING-345 `68aa9c19` blob `5ecc472f` / SHA256 `4409bcdd…5172`：条目 **900**；相对基线 `paragraphId` **+300 / −0 / Δ0**
- 全文件 `source-reviewed` 844 / `draft` 56 / `verified=true` **0**
- CP3 切片 600–899：`source-reviewed` 281 / `draft` 19
- 相对 MING-333：索引 **0–599 全等**

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | cherry-pick | 状态 |
|---|---|---|---|---|
| SDZJ0170 CP3 注解+progress | MING-345 `68aa9c19` | 注解 JSON + progress | `10f1c1f` | integrated_pending_acceptance |
| SDZJ0170 CP3 审查稿 | MING-354 `706a4c10` | `…-cp3-review.md` | `ecfc9a9` | integrated_pending_acceptance |

合入方式：`git cherry-pick -x`（最小路径，禁止 345 整树）。

## 验证
- `git diff 306aaecb`：仅注解 JSON + progress + cp3-review + 本账本；**无** `wuxing-jingji.json`、无 CP6/8/9 审查稿变更、无 CP4
- 合入后 JSON 与 345 blob/SHA256 **全等**；0–599 相对 333 **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42664 source_reviewed=40239 errors=[]
- 本批注解文件 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是紫微斗数全书全文交付；不是人工 verified；未开 CP4。

## 交付 tip
- 内容 cherry-pick tip：`ecfc9a9c5c624937b2524f8f983faf1c789d7a3d`
- 内容+账本首推 tip：`9f9aa8218d9d4c4f6414e61764c838d89814a0d5`
- 分支 HEAD / 远端：见 JSON `candidateIntegrationSha`（与 `origin/codex/multica-ming-360` 对齐）

## 远端验证
- `origin/codex/multica-ming-360` 精确 SHA 以 JSON `candidateIntegrationSha` / `remoteVerifiedAt` 为准
