# MING-351 叠 339 合入独立审查（CP6/8/9 审查稿 + SDZJ0170 CP1+CP2）

审查对象：`origin/codex/multica-ming-351` @ `306aaecb4ad54aa923d89999b97a5a4b0cdb0e94`。基线 `origin/codex/multica-ming-339` @ `642dbc4683b5e352de45f97265b2794a881be3cb`（MING-341 `22f7f08` 已审）。本岗工作树 `fateradar-multica-ming-355` / `codex/multica-ming-355`，写出仅本文件。未改注解 JSON、未改 `wuxing-jingji.json`、未改 339 已合入审查稿 / `ming-339-*` 账本、未改 `ming-351-integration-ledger.*`、未抢 MING-345/354 CP3。审查岗未参与 MING-351 生产。不是人工 `verified`，不是全库完成，不是产品交付，不合 main。

结论：**通过。** 相对 339 仅 8 个 `A` 路径（CP6/8/9 审查稿、SDZJ0170 注解+progress+cp2-review、`ming-351-integration-ledger.*`）；`wuxing-jingji.json` blob 不变；SDZJ0170 注解与 MING-333 `60495cc6` 全等（entries=600），未混入 MING-345 CP3（900 段 / blob `5ecc472f`）。全库校验器 `ok=true`，`verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11）：

```
git fetch origin codex/multica-ming-351 codex/multica-ming-339 \
  codex/multica-ming-333 codex/multica-ming-334 \
  codex/multica-ming-337 codex/multica-ming-338 \
  codex/multica-ming-340 codex/multica-ming-345
git ls-remote origin refs/heads/codex/multica-ming-351 refs/heads/codex/multica-ming-339
git merge-base --is-ancestor 642dbc4683b5e352de45f97265b2794a881be3cb 306aaecb4ad54aa923d89999b97a5a4b0cdb0e94
git diff --name-status 642dbc4683b5e352de45f97265b2794a881be3cb 306aaecb4ad54aa923d89999b97a5a4b0cdb0e94
git log --oneline 642dbc46..306aaecb
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-351` | `306aaecb4ad54aa923d89999b97a5a4b0cdb0e94`（`ls-remote` 一致） |
| 已审 339 tip | `642dbc4683b5e352de45f97265b2794a881be3cb`（是 351 祖先） |
| 相对 339 文件数 | **8**（全部 `A`，无 `M`/`D`） |
| `references/annotations/luming-nayin/wuxing-jingji.json` | blob `9665e5752e6535a33705f21f3415855f753928a1`（339 = 351） |
| 339 已合入审查稿 / `ming-339-*` | blob 全等（抽核 CP1/CP3/CP7/神相 CP1 + 339 账本） |
| MING-345 CP3 注解 | tip `68aa9c19` blob `5ecc472f` entries=900；**未**出现在本 tip |
| 产品路径 / `chart.*` / WebUI | 无 |
| 本岗写出 | 仅本文件 |

相对 339 新增 8 文件：

1. `docs/book-reviews/wuxing-jingji-cp6-review.md`
2. `docs/book-reviews/wuxing-jingji-cp8-review.md`
3. `docs/book-reviews/wuxing-jingji-cp9-review.md`
4. `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp2-review.md`
5. `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md`
6. `docs/integration/ming-351-integration-ledger.json`
7. `docs/integration/ming-351-integration-ledger.md`
8. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

`874f37a` 之后六笔只改 351 账本：钉 tip / 远端核验 / 再钉 / finalize。未再碰审查稿或注解。

339 已合入 blob 未变（抽核）：

| 路径 | blob（339 = 351） |
|---|---|
| `docs/book-reviews/wuxing-jingji-cp1-review.md` | `0e6ba50947eb900cf21e243103d6886e01e60c12` |
| `docs/book-reviews/wuxing-jingji-cp3-review.md` | `545a6efb520c44cbe39c79286fd1b3462eeae88c` |
| `docs/book-reviews/wuxing-jingji-cp7-review.md` | `455f6823771aff0ff4b4f4a7517bb8e89540c703` |
| `docs/book-reviews/shenxiang-quanbian-cp1-review.md` | `c808ca675b356f0fabb22db69e0999dc83bb15e9` |
| `docs/integration/ming-339-integration-ledger.json` | `609d875ff8040dfd1fbc249c3d29af41ed7ba8e3` |
| `docs/integration/ming-339-integration-ledger.md` | `2289092f7063b750641db300e17c567254f06832` |

未整树迁入 333 祖先他书：相对 339 无其它注解/书籍路径；仅 SDZJ0170 最小三路径 + 五行三份审查稿 + 本批账本。

## 2. 合入源 tip 对账

| Pack | 源 tip | cherry-pick | 路径 | blob（源 = 合入） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| 五行 CP6 MING-334 | `9d15790d5e602b228ec8d0cabead26415758d012` | `64b242f` | `docs/book-reviews/wuxing-jingji-cp6-review.md` | `88743720827e5fd0fa5a02bcc0975415012ea866` | 181 / 13277 | 否 |
| 五行 CP8 MING-337 | `fc67a6c19fc7923e88d5aa8e7a5978b7fd0010d0` | `850f59d` | `docs/book-reviews/wuxing-jingji-cp8-review.md` | `c53ae4f26114856bbec0d96569f91e687a1d5fd7` | 211 / 16576 | 否 |
| 五行 CP9 MING-338 | `402f63fb483c785652619bb1f38280aea13e2e5e` | `b477e7b` | `docs/book-reviews/wuxing-jingji-cp9-review.md` | `c0c2bf5267706704d8e30f639fa9751519353c0c` | 211 / 16334 | 否 |
| SDZJ0170 注解+progress MING-333 | `60495cc6b29bb9bc6478c3073b824cbcbbb4b4a0` | `b209e18` | `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `ab94ca8e124b3d8934ca723a76d8c2f276583f82` | entries=600 | 否 |
| （同上） | 同上 | 同上 | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md` | `98a2335b8bf5e75a05f9166300c878a4ab4bfdc7` | 101 / 6916 | 否 |
| SDZJ0170 CP2 审 MING-340 | `5182ae0a483eafe3ff9a3c26a01c39cee20f4855` | `874f37a` | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp2-review.md` | `4c0ca06a1efdc6dee2f35e1c7bfc1bcd0e05d50c` | 199 / 13174 | 否 |

四份审查稿均写「结论：**通过。**」且写明 `source-reviewed` 不是人工 `verified`。合入不是空文件、不是截断、不是另写副本。源 tip `ls-remote` 与账本一致。

## 3. SDZJ0170：333 全等、未混 345

| 项 | 351 tip | 333 tip | 345 tip |
|---|---|---|---|
| tip SHA | `306aaecb` | `60495cc6` | `68aa9c19` |
| 注解 blob | `ab94ca8e124b3d8934ca723a76d8c2f276583f82` | **同** | `5ecc472f7ef5e4325fdb83371a8315aad628cd07`（**不同**） |
| entries | **600** | **600** | **900** |
| `verified=true` | 0 | 0 | 0 |
| `review=source-reviewed` / `draft` | 563 / 37 | 563 / 37 | （未取） |
| paragraphId | 600 unique | 全等 | 351 ⊂ 345；345 多 300（CP3） |

基线 339 无该注解文件 → `paragraphId` **+600 / −0 / Δ0**。本 tip 停在 CP1+CP2（600 段），未叠 CP3。

## 4. 校验器独立复跑

本岗对 `306aaecb` 树复跑（本岗 worktree，非 ming-351 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42364 | 39958 | `[]` |

相对已审 339（files=57 entries=41764 source_reviewed=39395）：+1 注解文件、+600 entries、+563 source_reviewed，与 SDZJ0170 合入一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42364 条：`verified=true` **0**。本批 SDZJ0170 600 条 `verified=false` 全覆盖。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-351-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `fd2b45930a131aafaf116023b4060de737dfc4c1`；真实远端 tip 是 `306aaecb`（其后几笔只钉账本）。与 MING-339/341 账本自指滞后同类。不回改 351 账本（非本岗独占文件）。
2. 账本 `.md`「远端验证」段同样停在 `fd2b459`；内容 cherry-pick tip `874f37a` 与本审查对账一致，不影响合入正确性。
3. 全库 `files=58` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。
4. MING-345/354 CP3 仍在并行；本 tip 未取 `5ecc472f` / 900 段。后续叠入须另开集成 Issue，不得把本审查当作 CP3 放行。

## 7. remaining / 下一步

- 本 Issue（MING-355）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-351：本批叠 339 合入成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一批可评估 SDZJ0170 CP3（MING-345/354，900 段）或其它已审增量；须保持 `wuxing-jingji.json` 不被覆盖。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 351。
