# MING-329 古籍集成账本（下一批已审缺基线）

机器可读权威：`docs/integration/ming-329-integration-ledger.json`。

## 基线与叠层
- 权威：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`
- 叠层：快进 `origin/codex/multica-ming-324` tip `9118a787…`；**未改写** 324 的 11 个已交文件
- 独占：`fateradar-multica-ming-329` / `codex/multica-ming-329`

## 本批已合入（待独立验收）
| Pack | Source | Review | entries / sr / draft | 状态 |
|---|---|---|---|---|
| 六壬大全 | MING-97 `d84e26ba` | MING-97 验收收口 | 6893 / 6048 / 845 | integrated_pending_acceptance |
| 六壬秘本 | MING-97 `d84e26ba` | 同上 | 2643 / 2554 / 89 | integrated_pending_acceptance |
| SK1602 | MING-114 `59de8bf` | MING-124 `562681f0` | 13 / 11 / 2 | integrated_pending_acceptance |
| SK1609 | MING-135 `3b578879` | MING-150 `8dec7447` | 398 / 396 / 2 | integrated_pending_acceptance |

另带入对应审查/进度稿，以及已 done 的审查-only 文档：MING-315/316/318/319（仅 `docs/book-reviews/*`，未改五行精纪/神相注解 JSON）。

## 验证
- 四包 + 全库 `validate-annotations.py --json` 均 `ok=true`（全库 files=57 entries=41764 source_reviewed=39395）
- 本批 paragraphId 交叉重复 0；`verified` 全 false
- 相对 324 tip：上述 11 文件 diff 0 字节

## 明确未合
- **SDZJ0170**（账本标明 tip blob 可能缺 CP2）
- 产品 MING-320/322/327
- 不重做 324 batch1；不抢 MING-328

source-reviewed ≠ 人工 verified。不宣称全库/产品完成。不合 main。
