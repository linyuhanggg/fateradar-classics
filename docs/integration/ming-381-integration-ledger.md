# MING-381 古籍集成账本（360 tip 上合入已审 SDZJ0170 CP4）

机器可读权威：`docs/integration/ming-381-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-360` @ `afeddaf39c4ae5a17969e38667799b793febbd39`（审查 MING-363 已通过）
- 独占：`fateradar-multica-ming-381` / `codex/multica-ming-381`
- **未改写** 360 已合入 CP3 段（索引 0–899）
- **未覆盖** `wuxing-jingji.json`、大六壬 JSON、紫微主本 JSON
- **未升** 产品唯一线 `6c1dfa3b` / MING-375

## 合入前差集（SDZJ0170 注解）
- 基线 900 段（CP1+CP2+CP3）
- 源 tip MING-369 `0ff72d19` blob `1f369f99` / SHA256 `d65d93d8…a261`：条目 **1070**；相对基线 `paragraphId` **+170 / −0 / Δ0**
- 全文件 `source-reviewed` 1010 / `draft` 60 / `verified=true` **0**
- CP4 切片 900–1069：`source-reviewed` 166 / `draft` 4
- 相对 MING-360：索引 **0–899 全等**

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | cherry-pick | 状态 |
|---|---|---|---|---|
| SDZJ0170 CP4 注解+progress | MING-369 `0ff72d19` | 注解 JSON + progress | `1e836b6` | integrated_pending_acceptance |
| SDZJ0170 CP4 审查稿 | MING-373 `a842a48d` | `…-cp4-review.md` | `f10fa0f` | integrated_pending_acceptance |

合入方式：`git cherry-pick -x`（最小路径，禁止 369 整树）。

## 验证
- `git diff afeddaf39`：仅注解 JSON + progress + cp4-review + 本账本；**无** `wuxing-jingji.json`、无大六壬/紫微主本 JSON、无 CP3 段回写
- 合入后 JSON 与 369 blob/SHA256 **全等**；0–899 相对 360 **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40405 errors=[]
- 本批注解文件 `verified=true`：**0**；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是紫微斗数全书/主本全文交付；不是人工 verified。
- 识典段落 remaining 0 ≠ 主本/全书完成。

## 交付 tip
- 内容 cherry-pick tip：`f10fa0fdb49626508c9d903ad360ebeb03a4731f`
- 内容+账本首推 tip：`192f6337d87edb21b3bf915fd635f0187049d64d`
- 候选/远端 tip：`a9a520a195f0549603fd30f17777bcce972a7179`（交包时 `origin/codex/multica-ming-381`；若随后仅账本自指提交则以交包评论远端 SHA 为准）

## 远端验证
- `origin/codex/multica-ming-381` @ `a9a520a195f0549603fd30f17777bcce972a7179` recorded `2026-09-11T16:40:17Z`
