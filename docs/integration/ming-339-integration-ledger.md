# MING-339 古籍集成账本（329 tip 上审查稿增量）

机器可读权威：`docs/integration/ming-339-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`（MING-331 `9ed9c624` 独立审查通过）
- 祖先含 324 tip `9118a787` 与权威 `bc798566`
- 独占：`fateradar-multica-ming-339` / `codex/multica-ming-339`
- **未改写** 324 十一文件、329 四包注解 JSON / `ming-324-*` / `ming-329-*`、`wuxing-jingji.json`

## Inventory
| 项 | 结论 |
|---|---|
| 329 已带 315/316/318/319 | tip blob 与源 tip **全等**，本批不重合 |
| 缺口（done + 审查-only） | 312 / 313 / 317 / 335 |
| 跳过 | 334（`in_review`）；333 SDZJ0170 |

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 状态 |
|---|---|---|---|
| 神相 CP1 | MING-312 `28a23af` | `shenxiang-quanbian-cp1-review.md` | integrated_pending_acceptance |
| 五行精纪 CP1 | MING-313 `2eacfd4` | `wuxing-jingji-cp1-review.md` | integrated_pending_acceptance |
| 五行精纪 CP3 | MING-317 `d8e9798` | `wuxing-jingji-cp3-review.md` | integrated_pending_acceptance |
| 五行精纪 CP7 | MING-335 `26e22fc` | `wuxing-jingji-cp7-review.md` | integrated_pending_acceptance |

合入方式：`git cherry-pick -x`（每 commit 仅 1 个 `docs/book-reviews/*` 文件）。

## 验证
- `git diff 6effd8e4`：仅上述 4 个审查稿 + 本账本；**无**注解 JSON、无 SDZJ0170、无 324 十一文件变更
- `validate-annotations.py --json`：`ok=true` files=57 entries=41764 source_reviewed=39395
- `verified` true 计数 = 0
- `wuxing-jingji.json` blob 与基线全等 `9665e575…`

## 明确未合
- **SDZJ0170**（MING-333 CP2 生产中）
- **MING-334** CP6（仍 `in_review`）
- 不覆盖 `wuxing-jingji.json`
- 不宣称全库/人工 verified/产品完成；不合 main

source-reviewed ≠ 人工 verified。
