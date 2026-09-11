# MING-360 叠 351 合入独立审查（SDZJ0170 CP3 900 段）

审查对象：`origin/codex/multica-ming-360` @ `afeddaf39c4ae5a17969e38667799b793febbd39`。基线 `origin/codex/multica-ming-351` @ `306aaecb4ad54aa923d89999b97a5a4b0cdb0e94`（MING-355 `cea13e6` 已审）。本岗工作树 `fateradar-multica-ming-363` / `codex/multica-ming-363`，写出仅本文件。未改注解 JSON、未改 `wuxing-jingji.json`、未改 351 已合入 CP6/8/9 审查稿 / `ming-351-*` / `ming-360-integration-ledger.*`、未改子平注解、未开 CP4。审查岗未参与 MING-360 生产。不是人工 `verified`，不是紫微斗数全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 351 仅 5 路径（注解 JSON `M`、progress `M`、cp3-review `A`、本批 ledger `A`×2）；JSON 与 MING-345 `68aa9c19` blob/SHA256 **全等**（entries=900）；索引 0–599 相对 MING-333 `60495cc6` **逐条全等**；`wuxing-jingji.json` 与 CP6/8/9 审查稿 blob 仍等于 351。全库校验器 `ok=true`，本文件与全库 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11）：

```
git fetch origin \
  refs/heads/codex/multica-ming-360 \
  refs/heads/codex/multica-ming-351 \
  refs/heads/codex/multica-ming-345 \
  refs/heads/codex/multica-ming-354 \
  refs/heads/codex/multica-ming-333
git ls-remote origin refs/heads/codex/multica-ming-360 refs/heads/codex/multica-ming-351
git merge-base --is-ancestor 306aaecb4ad54aa923d89999b97a5a4b0cdb0e94 afeddaf39c4ae5a17969e38667799b793febbd39
git diff --name-status 306aaecb4ad54aa923d89999b97a5a4b0cdb0e94 afeddaf39c4ae5a17969e38667799b793febbd39
git log --oneline 306aaecb..afeddaf
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-360` | `afeddaf39c4ae5a17969e38667799b793febbd39`（`ls-remote` 一致） |
| 已审 351 tip | `306aaecb4ad54aa923d89999b97a5a4b0cdb0e94`（是 360 祖先） |
| 相对 351 文件数 | **5**（`A`×3 + `M`×2，无 `D`） |
| `references/annotations/luming-nayin/wuxing-jingji.json` | blob `9665e5752e6535a33705f21f3415855f753928a1`（351 = 360） |
| 351 已合入 CP6/8/9 / cp2-review / `ming-351-*` | blob 全等 |
| 子平 `ziping-zhenquan.json` / `yuanhai-ziping.json` | blob 全等（未抢 MING-358） |
| 源 `SDZJ0170/text.md` SHA256 | `b4850fddeac0fc7b5fad40a7a93865f47c70622e348ca4f2c79b98f37a15a790`（351 = 360；本批未改源层） |
| 产品路径 / `chart.*` / WebUI | 无 |
| CP4 审查稿 | 不存在 |
| 本岗写出 | 仅本文件 |

相对 351 变更 5 文件：

1. `A` `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp3-review.md`
2. `M` `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md`
3. `A` `docs/integration/ming-360-integration-ledger.json`
4. `A` `docs/integration/ming-360-integration-ledger.md`
5. `M` `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

`ecfc9a9` 之后五笔只改 360 账本：首推账本 / finalize / 修复验证注 / 对齐 tip / 修复 markdown 交付段。未再碰审查稿或注解。

351 已合入 blob 未变：

| 路径 | blob（351 = 360） |
|---|---|
| `docs/book-reviews/wuxing-jingji-cp6-review.md` | `88743720827e5fd0fa5a02bcc0975415012ea866` |
| `docs/book-reviews/wuxing-jingji-cp8-review.md` | `c53ae4f26114856bbec0d96569f91e687a1d5fd7` |
| `docs/book-reviews/wuxing-jingji-cp9-review.md` | `c0c2bf5267706704d8e30f639fa9751519353c0c` |
| `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp2-review.md` | `4c0ca06a1efdc6dee2f35e1c7bfc1bcd0e05d50c` |
| `docs/integration/ming-351-integration-ledger.json` | `4eee91ca3d7053d2ba1d507e41ac00c7ceaddfbd` |
| `docs/integration/ming-351-integration-ledger.md` | `c98f9644be90cf2ad684a33e0b1d1d9cf2f75528` |
| `references/annotations/bazi/ziping-zhenquan.json` | `e6afc7e8f17ee23033a881eedab86ff254c21ebf` |
| `references/annotations/bazi/yuanhai-ziping.json` | `7d82d9f289cd3b2520dd2e70e73d3ce597edc327` |

未整树迁入 345：相对 351 无其它注解/书籍路径；仅 SDZJ0170 最小三路径 + 本批账本。

## 2. 合入源 tip 对账

| Pack | 源 tip | cherry-pick | 路径 | blob（源 = 合入） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| SDZJ0170 注解 MING-345 | `68aa9c19cfef05751dee366e263f3ea01bb4cd38` | `10f1c1f`（`-x` from `68aa9c19`） | `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `5ecc472f7ef5e4325fdb83371a8315aad628cd07` | entries=900；SHA256 `4409bcdd3cb6c9e8be76d428a9fa2584f0d9acfa1f81682b6c9c297aad8f5172` | 否 |
| （同上） | 同上 | 同上 | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md` | `6c121e322b63853b267e02017d28690dfc12ac01` | 150 / 10334 | 否 |
| SDZJ0170 CP3 审 MING-354 | `706a4c10879985e5339838aea170239973379308` | `ecfc9a9`（`-x` from `706a4c10`） | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp3-review.md` | `2b6757e7fed10c7e436cd47633455154d6c0541c` | 221 / 15820 | 否 |

审查稿写「结论：**通过。**」且写明 `source-reviewed` 不是人工 `verified`。合入不是空文件、不是截断、不是另写副本。源 tip `ls-remote` 与账本一致。`git diff --stat 306aaecb..afeddaf`：5 files, +4537（注解 `+4072`、progress `+49`、cp3-review `+221`、ledger json `+154`、ledger md `+41`）。

## 3. SDZJ0170：345 全等、0–599 仍等于 333

| 项 | 360 tip | 345 tip | 351 / 333 tip |
|---|---|---|---|
| tip SHA | `afeddaf` | `68aa9c19` | `306aaecb` / `60495cc6` |
| 注解 blob | `5ecc472f7ef5e4325fdb83371a8315aad628cd07` | **同** | `ab94ca8e124b3d8934ca723a76d8c2f276583f82` |
| SHA256 | `4409bcdd3cb6c9e8be76d428a9fa2584f0d9acfa1f81682b6c9c297aad8f5172` | **同** | `9ae00ff4502d25cdfcad953b2560fb798fd0d265764f4a4b2905bb854821223c` |
| entries | **900** | **900** | **600** |
| `verified=true` | 0 | 0 | 0 |
| `review=source-reviewed` / `draft` | 844 / 56 | 844 / 56 | 563 / 37 |
| 索引 0–599 | 与 333 **python 逐条全等** | 同（360 raw = 345 raw） | 600 条原件 |

相对 351：`paragraphId` **+300 / −0 / Δ0**。CP3 切片 600–899：`source-reviewed` 281 / `draft` 19 / `verified=true` 0。`paragraphs.json` 全书 1070 段；注解末条索引 899 = `P7356158895376744457`；**nextId** 索引 900 `P7356158895376760841`；remaining **170**（900–1069）。本 tip 停在 CP1+CP2+CP3，未开 CP4。

## 4. 校验器独立复跑

本岗对 `afeddaf` 树复跑（本岗 worktree，非 ming-360 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json --annotations references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42664 | 40239 | `[]` |
| 本文件 | true | 1 | 1 | 900 | 844 | `[]` |

相对已审 351（files=58 entries=42364 source_reviewed=39958）：文件数不变（该注解已在 351）、+300 entries、+281 source_reviewed，与 CP3 切片一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。CP3 语义抽样已由 MING-354 独立审查，本岗核合入 blob 全等，不重做 600–899。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42664 条：`verified=true` **0**。本批 SDZJ0170 900 条 `verified=false` 全覆盖。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-360-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `68dcbc3f90833996ed33d74d3b57886e852f0b44`；真实远端 tip 是 `afeddaf`（其后一笔只修账本 markdown 交付段，并把 JSON 自指从 `548de8c` 快进到 `68dcbc3`）。与 MING-351/355 账本自指滞后同类。不回改 360 账本（非本岗独占文件）。
2. 内容 cherry-pick tip `ecfc9a9` 与本审查对账一致；`9f9aa82` 之后五笔只动 ledger。不影响合入正确性。
3. 全库 `files=58` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。
4. remaining 170（索引 900–1069）不在本包。本审查通过不等于授权本岗开 CP4；CP4 须另开生产 Issue，且不得与本 JSON 双写。

## 7. remaining / 下一步

- 本 Issue（MING-363）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-360：本批叠 351 合入 CP3 成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一批可评估 SDZJ0170 CP4（remaining 170，nextId `P7356158895376760841`）；须保持 `wuxing-jingji.json` 不被覆盖，且同 JSON 不得双写。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 360。
- 勿重做 0–899；勿抢 MING-358 子平审查。
