# MING-392 叠 381 合入独立验收（大六壬 CP7–12 / 秘本 CP1–3 审查稿）

审查对象：`origin/codex/multica-ming-392` @ `f94c471dfd3771830de864fe6a5d5cf11992cebd`。基线 `origin/codex/multica-ming-381` @ `b21ae71538d46d64169508589ffb1a209e6466ff`（MING-385 `9cd03c63` 已通过）。本岗工作树 `fateradar-multica-ming-399` / `codex/multica-ming-399`，写出仅本文件。未改注解 JSON、未改 392 已合入审查稿/账本、未改识典/大六壬/秘本/紫微主本 JSON、未升产品唯一线 `6c1dfa3b`。本岗未参与 MING-392 生产。不要重跑已通过的 381/385。不是人工 `verified`，不是大六壬/秘本全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 381 仅 12 路径（10 审查/验收 md `A` + 本批 ledger `A`×2）；**无** `references/annotations/**` diff；识典/大六壬/秘本三文件 SHA256 与 381 **全等**；10 份合入 md 与源 tip blob **全等**；全库校验器 `ok=true`，`errors=[]`；全库与三目标文件 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T17:11Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-381 \
  refs/heads/codex/multica-ming-392
git ls-remote origin \
  refs/heads/codex/multica-ming-381 \
  refs/heads/codex/multica-ming-392
git merge-base --is-ancestor b21ae71538d46d64169508589ffb1a209e6466ff f94c471dfd3771830de864fe6a5d5cf11992cebd
git diff --name-status b21ae71538d46d64169508589ffb1a209e6466ff f94c471dfd3771830de864fe6a5d5cf11992cebd
git diff --name-only b21ae71538d46d64169508589ffb1a209e6466ff f94c471dfd3771830de864fe6a5d5cf11992cebd -- 'references/annotations/**'
git log --oneline b21ae71538d46d64169508589ffb1a209e6466ff..f94c471dfd3771830de864fe6a5d5cf11992cebd
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-392` | `f94c471dfd3771830de864fe6a5d5cf11992cebd`（`ls-remote` 一致） |
| 已审 381 tip | `b21ae71538d46d64169508589ffb1a209e6466ff`（是 392 祖先） |
| 相对 381 文件数 | **12**（全部 `A`，无 `M`/`D`，无未声明路径） |
| `references/annotations/**` diff | **0** |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（381 = 392） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（381 = 392） |
| 秘本 blob | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（381 = 392） |
| 紫微主本 `ziwei-doushu-quanshu.json` | blob `0ac9fcb2c1aa75768849a48c332c6658435f1940`（381 = 392） |
| 产品路径 / `chart.*` / WebUI / `6c1dfa3b` | 无 |
| 本岗写出 | 仅本文件 |

相对 381 变更 12 文件（均在声明独占/账本路径内）：

1. `A` `docs/book-reviews/daliuren-daquan-cp7-review.md`
2. `A` `docs/book-reviews/daliuren-daquan-cp8-review.md`
3. `A` `docs/book-reviews/daliuren-daquan-cp9-review.md`
4. `A` `docs/book-reviews/daliuren-daquan-cp10-review.md`
5. `A` `docs/book-reviews/daliuren-daquan-cp11-review.md`
6. `A` `docs/book-reviews/daliuren-daquan-cp12-review.md`
7. `A` `docs/book-reviews/liuren-miben-cp1-review.md`
8. `A` `docs/book-reviews/liuren-miben-cp2-review.md`
9. `A` `docs/book-reviews/liuren-miben-cp3-review.md`
10. `A` `docs/integration/ming-381-acceptance-review.md`
11. `A` `docs/integration/ming-392-integration-ledger.json`
12. `A` `docs/integration/ming-392-integration-ledger.md`

`b670186` 之后六笔只改 392 账本（首推账本 / remote tip / candidate 对齐 / delivery notes / lock / tip 指针澄清）。未再碰审查稿或注解。未整树迁入任何审查 tip（含 orphan CP8）。

## 2. 三文件 SHA 与 381 全等

| 路径 | SHA256（381 = 392） | blob |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7` |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | `66db69fdf39120e4e37733cb59b5ea01a154dcd9` |
| `references/annotations/san-shi/liuren-miben.json` | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821` | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f` |

目标文件 `verified=true`：**0**；识典 1070 / 大六壬 6893 / 秘本 2643 条均为 `verified=false`。

## 3. 合入源 tip 对账

| Pack | 源 tip | 合入方式 | 路径 | blob（源 = 合入 = 账本） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| 大六壬 CP7 MING-372 | `a05cef26ad7966cd71c42c1b56755092164b7828` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp7-review.md` | `dc833e74c000aecb4d948ff33eb526db0407501b` | 178 / 14244 | 否 |
| 大六壬 CP8 MING-374 | `43c7d593f2897c5230f3b6b1de14efd2bffd1421` | path-checkout（orphan） | `docs/book-reviews/daliuren-daquan-cp8-review.md` | `3aae45b151d2d8daba19c1443616662c7e31169d` | 165 / 13826 | 否 |
| 大六壬 CP9 MING-377 | `a457e9cc49b8406b89c5940b1e17dd91c4975ab7` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp9-review.md` | `8b7ab6e038438f41b815ffd0a16ad2e40e022cc7` | 170 / 13294 | 否 |
| 大六壬 CP10 MING-378 | `604ea3cb6136f11b95acdddd820244d31c3bea42` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp10-review.md` | `34212d8c1152bd069b15d49d0cefb2f2bd56ebab` | 189 / 16471 | 否 |
| 大六壬 CP11 MING-383 | `847fff8803033b821084e3f15cb6e630cbb4c382` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp11-review.md` | `81a15d1a140ecaa2db19156471b711a4a8fbc18a` | 206 / 19264 | 否 |
| 大六壬 CP12 MING-386 | `d0a3b24aea5a9b02f0cab97f336a1d6711a3eaf8` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp12-review.md` | `fb6f283692ce76fbf5608e801ac883e15e4db3db` | 204 / 16927 | 否 |
| 秘本 CP1 MING-379 | `d5fc8bbdea87a75c61379bdb92173b45dcd7749e` | cherry-pick `-x` | `docs/book-reviews/liuren-miben-cp1-review.md` | `165d0cd06183bef89e0518f12fea06bc048a67ad` | 211 / 12883 | 否 |
| 秘本 CP2 MING-384 | `56d130088fb9891d19c6789be45178b6aef02355` | cherry-pick `-x` | `docs/book-reviews/liuren-miben-cp2-review.md` | `a07d6b660388f4401e7186e32d42d5cfeeb2ed22` | 138 / 8672 | 否 |
| 秘本 CP3 MING-388 | `d1b8af99355417bac973cc27b599c179b0b6c82d` | cherry-pick `-x` | `docs/book-reviews/liuren-miben-cp3-review.md` | `2655b0e699d0551c2ac13177bdbe82545b38ade9` | 199 / 12811 | 否 |
| 381 验收 MING-385 | `9cd03c63cac34aee73e3341c9660a270af6bb09d` | cherry-pick `-x` | `docs/integration/ming-381-acceptance-review.md` | `b591bf52d5059e655bea95dbaaee10152efb7871` | 138 / 10298 | 否 |

十份审查/验收稿均写明通过（有限范围）且 `source-reviewed` ≠ 人工 `verified`。合入不是空文件、不是截断、不是另写副本。源 tip `ls-remote` 与账本一致。`git diff --stat b21ae715..f94c471`：12 files, +2061（全部为 md/json 账本与审查稿）。

## 4. 校验器独立复跑

本岗对 `f94c471` 树复跑（本岗 worktree，非 ming-392 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |

相对已审 381：文件数/entries/source_reviewed **不变**（本批未改注解，符合只进 md）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各 CP 语义抽样已由对应审查 Issue 完成；本岗核合入 blob 全等，不重做 381/385 或各审查包。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。三目标文件 `verified=false` 全覆盖（识典 1070、大六壬 6893、秘本 2643）。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-392-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `ebae08000802c0d2b09004f0c5c7d224dcfd6628`；真实远端 tip 是 `f94c471`（其后三笔只澄清 tip 指针 / lock candidate）。与 MING-381 账本自指滞后同类。不回改 392 账本（非本岗独占文件）。
2. 内容合入 tip `b670186` 与本审查对账一致；其后六笔只动 ledger。不影响合入正确性。
3. 未合入 MING-387 CP13（按 Issue 明确不要求等待）。不把未合入 CP13 算作本包失败。
4. 全库 `files=58` 只是本集成线上的注解文件数，不是全书/大六壬全书/秘本全书完成，更不是产品交付。
5. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 7. remaining / 下一步

- 本 Issue（MING-399）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-392：本批叠 381 合入审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 大六壬 / 秘本注解 JSON remaining 与 CP13 等后续包由协调另派；勿再开第二路集成写入抢 392 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 392。
- 勿重跑 381/385；勿抢产品唯一线 `6c1dfa3b`；勿抢 MING-397 JSON 修复。
