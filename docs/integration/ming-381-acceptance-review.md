# MING-381 叠 360 合入独立验收（SDZJ0170 CP4 1070 段）

审查对象：`origin/codex/multica-ming-381` @ `b21ae71538d46d64169508589ffb1a209e6466ff`。基线 `origin/codex/multica-ming-360` @ `afeddaf39c4ae5a17969e38667799b793febbd39`（MING-363 `0662260` 已审）。源注解 MING-369 `0ff72d19dd48c400ce75d9a303f02c5a2f8df961`；审查稿 MING-373 `a842a48d3a9b4c41a1cf5091a53b5460f98a61c4`。本岗工作树 `fateradar-multica-ming-385` / `codex/multica-ming-385`，写出仅本文件。未改注解 JSON、未改 381 账本、未改 `wuxing-jingji.json`、未改大六壬 JSON、未改紫微主本 JSON、未改源层、未升产品唯一线 `6c1dfa3b`。审查岗未参与 MING-381 生产。不要重跑已通过的 360/363/369/373 生产包。不是人工 `verified`，不是紫微斗数全书/主本完成，不是产品交付，不合 main。

结论：**通过。** 相对 360 仅 5 路径（注解 JSON `M`、progress `M`、cp4-review `A`、本批 ledger `A`×2）；JSON 与 MING-369 `0ff72d19` blob/SHA256 **全等**（entries=1070）；索引 0–899 相对 360 **逐条全等**；CP4 900–1069 = 166 SR + 4 draft；全文件 1010 SR + 60 draft；`verified=true` **0**。全库校验器 `ok=true`，`errors=[]`。`source-reviewed` 不是人工 `verified`。识典段落 remaining 0 ≠ 主本/全书完成。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-12）：

```
git fetch origin \
  refs/heads/codex/multica-ming-360 \
  refs/heads/codex/multica-ming-381 \
  refs/heads/codex/multica-ming-369 \
  refs/heads/codex/multica-ming-373
git ls-remote origin \
  refs/heads/codex/multica-ming-360 \
  refs/heads/codex/multica-ming-381 \
  refs/heads/codex/multica-ming-369 \
  refs/heads/codex/multica-ming-373
git merge-base --is-ancestor afeddaf39c4ae5a17969e38667799b793febbd39 b21ae71538d46d64169508589ffb1a209e6466ff
git diff --name-status afeddaf39c4ae5a17969e38667799b793febbd39 b21ae71538d46d64169508589ffb1a209e6466ff
git log --oneline afeddaf39c4ae5a17969e38667799b793febbd39..b21ae71538d46d64169508589ffb1a209e6466ff
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-381` | `b21ae71538d46d64169508589ffb1a209e6466ff`（`ls-remote` 一致） |
| 已审 360 tip | `afeddaf39c4ae5a17969e38667799b793febbd39`（是 381 祖先） |
| `origin/codex/multica-ming-369` | `0ff72d19dd48c400ce75d9a303f02c5a2f8df961` |
| `origin/codex/multica-ming-373` | `a842a48d3a9b4c41a1cf5091a53b5460f98a61c4` |
| 相对 360 文件数 | **5**（`A`×3 + `M`×2，无 `D`，无未声明路径） |
| `references/annotations/luming-nayin/wuxing-jingji.json` | blob `9665e5752e6535a33705f21f3415855f753928a1`（360 = 381） |
| 紫微主本 `ziwei-doushu-quanshu.json` | blob `0ac9fcb2c1aa75768849a48c332c6658435f1940`（360 = 381） |
| 源 `SDZJ0170/text.md` SHA256 | `b4850fddeac0fc7b5fad40a7a93865f47c70622e348ca4f2c79b98f37a15a790`（360 = 381；本批未改源层） |
| `paragraphs.json` | 1070 段；注解 ID 顺序全等，`mismatch=0` |
| 产品路径 / `chart.*` / WebUI / `6c1dfa3b` | 无 |
| 本岗写出 | 仅本文件 |

相对 360 变更 5 文件（均在声明独占路径内）：

1. `A` `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp4-review.md`
2. `M` `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md`
3. `A` `docs/integration/ming-381-integration-ledger.json`
4. `A` `docs/integration/ming-381-integration-ledger.md`
5. `M` `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

`f10fa0f` 之后五笔只改 381 账本：首推账本 / SHA 占位 / lock candidate / 记录远端 / 对齐 tip。未再碰审查稿或注解。未整树迁入 369。

360 已合入 blob 未变：

| 路径 | blob（360 = 381） |
|---|---|
| `docs/book-reviews/wuxing-jingji-cp6-review.md` | `88743720827e5fd0fa5a02bcc0975415012ea866` |
| `docs/book-reviews/wuxing-jingji-cp8-review.md` | `c53ae4f26114856bbec0d96569f91e687a1d5fd7` |
| `docs/book-reviews/wuxing-jingji-cp9-review.md` | `c0c2bf5267706704d8e30f639fa9751519353c0c` |
| `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp2-review.md` | `4c0ca06a1efdc6dee2f35e1c7bfc1bcd0e05d50c` |
| `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp3-review.md` | `2b6757e7fed10c7e436cd47633455154d6c0541c` |
| `docs/integration/ming-351-integration-ledger.json` | `4eee91ca3d7053d2ba1d507e41ac00c7ceaddfbd` |
| `docs/integration/ming-351-integration-ledger.md` | `c98f9644be90cf2ad684a33e0b1d1d9cf2f75528` |
| `docs/integration/ming-360-integration-ledger.json` | `11b802b30fdc585251ed8581caab980cadd621d9` |
| `docs/integration/ming-360-integration-ledger.md` | `9b4ba1ce8d8f704d51f3dfb190da7553cd8e26d4` |
| `references/annotations/bazi/ziping-zhenquan.json` | `e6afc7e8f17ee23033a881eedab86ff254c21ebf` |
| `references/annotations/bazi/yuanhai-ziping.json` | `7d82d9f289cd3b2520dd2e70e73d3ce597edc327` |
| `references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json` | `9f713a371b7059b2986321c12933a2ceb96c5766` |
| `references/annotations/ziwei/taiwei-fu.json` | `54230d91b7f33e8e5b43fe81969de7621293ffeb` |

`bookSlug` / `sourceTitle` / `scopeNote` 相对 360 未改。大六壬 JSON 无变更。

## 2. 合入源 tip 对账

| Pack | 源 tip | cherry-pick | 路径 | blob（源 = 合入） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| SDZJ0170 注解 MING-369 | `0ff72d19dd48c400ce75d9a303f02c5a2f8df961` | `1e836b6`（`-x` from `0ff72d19`） | `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7` | entries=1070；SHA256 `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | 否 |
| （同上） | 同上 | 同上 | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-progress-2026-09-11.md` | `cae38f94383e8abb065cc9089e66e428538926aa` | 201 / 14471 | 否 |
| SDZJ0170 CP4 审 MING-373 | `a842a48d3a9b4c41a1cf5091a53b5460f98a61c4` | `f10fa0f`（`-x` from `a842a48d`） | `docs/book-reviews/ziwei-doushu-quanshu-sdzj0170-cp4-review.md` | `166471c414a27b7737a1a683c9262f410d6e5165` | 212 / 15538 | 否 |

审查稿写「结论：**通过。**」且写明 `source-reviewed` 不是人工 `verified`。合入不是空文件、不是截断、不是另写副本。源 tip `ls-remote` 与账本一致。`git diff --stat afeddaf39..b21ae715`：5 files, +2991（注解 `+2540`、progress `+51`、cp4-review `+212`、ledger json `+145`、ledger md `+43`）。

## 3. SDZJ0170：369 全等、0–899 仍等于 360

| 项 | 381 tip | 369 tip | 360 tip |
|---|---|---|---|
| tip SHA | `b21ae715` | `0ff72d19` | `afeddaf39` |
| 注解 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7` | **同** | `5ecc472f7ef5e4325fdb83371a8315aad628cd07` |
| SHA256 | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | **同** | `4409bcdd3cb6c9e8be76d428a9fa2584f0d9acfa1f81682b6c9c297aad8f5172` |
| entries | **1070** | **1070** | **900** |
| `verified=true` | 0 | 0 | 0 |
| `review=source-reviewed` / `draft` | 1010 / 60 | 1010 / 60 | 844 / 56 |
| 索引 0–899 | 与 360 **python 逐条全等** | 同（381 raw = 369 raw） | 900 条原件 |

相对 360：`paragraphId` **+170 / −0 / Δ0**。CP4 切片 900–1069：`source-reviewed` 166 / `draft` 4 / `verified=true` 0。draft 四条（均 `verified=false`，不升 sr）：

| 索引 | paragraphId 尾 | review |
|---|---|---|
| 908 | `P7356158895401730098` | draft |
| 944 | `P7356158895792062501` | draft |
| 954 | `P7356158896102277170` | draft |
| 1035 | `P7356158897943756810` | draft |

`paragraphs.json` 全书 1070 段；注解末条索引 1069 = `P7356158905573064714`；起始 CP4 = `P7356158895376760841`（索引 900）。识典段落 **nextId 无 / remaining 0**。这只是识典 SDZJ0170 段落注解收口，不是主本、不是人工 verified、不是全书完成。

## 4. 校验器独立复跑

本岗对 `b21ae715` 树复跑（本岗 worktree，非 ming-381 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json --annotations references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |
| 本文件 | true | 1 | 1 | 1070 | 1010 | `[]` |

相对已审 360（files=58 entries=42664 source_reviewed=40239）：文件数不变（该注解已在 360）、+170 entries、+166 source_reviewed，与 CP4 切片一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。CP4 语义抽样已由 MING-373 独立审查，本岗核合入 blob 全等，不重做 900–1069。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。本批 SDZJ0170 1070 条 `verified=false` 全覆盖。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-381-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `a9a520a195f0549603fd30f17777bcce972a7179`；真实远端 tip 是 `b21ae715`（其后一笔只对齐账本 candidate，并把 JSON 自指停在 `a9a520a`）。与 MING-360/351 账本自指滞后同类。不回改 381 账本（非本岗独占文件）。
2. 内容 cherry-pick tip `f10fa0f` 与本审查对账一致；其后五笔只动 ledger。不影响合入正确性。
3. 全库 `files=58` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。
4. 识典段落 remaining 0 不是主本/全书完成，也不授权升产品唯一线。CP4 语义已由 MING-373 审查，本岗只验收合入。

## 7. remaining / 下一步

- 本 Issue（MING-385）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-381：本批叠 360 合入 CP4 成立，同样有限 `done`；不升产品唯一线、不合 main。
- 识典 SDZJ0170 段落注解 remaining **0**；勿再开同 JSON 生产包。主本 `ziwei-doushu-quanshu.json` 不在本包。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 381。
- 勿重做 0–1069；勿抢产品唯一线 `6c1dfa3b`。
