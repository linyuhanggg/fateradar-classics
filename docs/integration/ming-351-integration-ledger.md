# MING-351 古籍集成账本（339 tip 上 CP6/8/9 审查稿 + SDZJ0170 CP1+CP2）

机器可读权威：`docs/integration/ming-351-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-339` @ `642dbc4683b5e352de45f97265b2794a881be3cb`（MING-341 独立审查通过）
- 独占：`fateradar-multica-ming-351` / `codex/multica-ming-351`
- **未改写** 339 已合入审查稿 / `ming-339-*` 账本 / `references/annotations/luming-nayin/wuxing-jingji.json`
- **未取** MING-345 CP3 注解 blob `5ecc472f`（900 段）

## 合入前差集（SDZJ0170 注解）
- 基线无 `ziwei-doushu-quanshu--shidian-SDZJ0170.json`
- 源 tip MING-333 `60495cc6` blob `ab94ca8e`：`paragraphId` **+600 / −0 / Δ0**
- `source-reviewed` 563 / `draft` 37 / `verified=true` **0**
- 相对 MING-345：本批停在 600 段（CP1+CP2），不叠 CP3

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | cherry-pick | 状态 |
|---|---|---|---|---|
| 五行精纪 CP6 | MING-334 `9d15790` | `wuxing-jingji-cp6-review.md` | `64b242f` | integrated_pending_acceptance |
| 五行精纪 CP8 | MING-337 `fc67a6c` | `wuxing-jingji-cp8-review.md` | `850f59d` | integrated_pending_acceptance |
| 五行精纪 CP9 | MING-338 `402f63f` | `wuxing-jingji-cp9-review.md` | `b477e7b` | integrated_pending_acceptance |
| SDZJ0170 CP1+CP2 | MING-333 `60495cc` + 审 MING-340 `5182ae0` | 注解 JSON + progress + cp2-review | `b209e18` / `874f37a` | integrated_pending_acceptance |

合入方式：`git cherry-pick -x`（60495cc 在基线无父文件时为 modify/delete，保留源版本后 continue）。

## 验证
- `git diff 642dbc4`：仅上表 6 路径 + 本账本；**无** `wuxing-jingji.json` 变更、无 345 CP3、无 333 祖先他书整树
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42364 source_reviewed=39958 errors=[]
- 本批注解文件 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是五行精纪 / 紫微斗数全书全文交付；不是人工 verified。

## 交付 tip
- 账本提交：`3e25f3dc3122f83034f43e072d615f10ac72535e`（含本账本；内容 cherry-pick tip `874f37a`）

## 远端验证
-  @  @ 
