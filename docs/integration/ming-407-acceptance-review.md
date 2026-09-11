# MING-407 叠 392 合入独立验收（大六壬 CP13–CP16 审查稿）

审查对象：`origin/codex/multica-ming-407` @ `e371f3a83b1d160915817cc1b0e757675419dfc4`。基线 `origin/codex/multica-ming-392` @ `f94c471dfd3771830de864fe6a5d5cf11992cebd`（MING-399 `1442440` 已通过）。本岗工作树 `fateradar-multica-ming-411` / `codex/multica-ming-411`，写出仅本文件。未改注解 JSON、未改 407 已合入审查稿/账本、未改识典/大六壬/秘本/紫微主本 JSON、未升产品唯一线 `6c1dfa3b`。本岗未参与 MING-407 生产。不要重跑已通过的 392/399。不是人工 `verified`，不是大六壬全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 392 仅 6 路径（4 审查 md `A` + 本批 ledger `A`×2）；**无** `references/annotations/**` diff；识典/大六壬/秘本三文件 SHA256 与 392 **全等**；4 份合入 md 与源 tip blob **全等**；全库校验器 `ok=true`，`errors=[]`；全库与三目标文件 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T17:31Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-392 \
  refs/heads/codex/multica-ming-407 \
  refs/heads/codex/multica-ming-387 \
  refs/heads/codex/multica-ming-390 \
  refs/heads/codex/multica-ming-394 \
  refs/heads/codex/multica-ming-395
git ls-remote origin \
  refs/heads/codex/multica-ming-392 \
  refs/heads/codex/multica-ming-407
git merge-base --is-ancestor f94c471dfd3771830de864fe6a5d5cf11992cebd e371f3a83b1d160915817cc1b0e757675419dfc4
git diff --name-status f94c471dfd3771830de864fe6a5d5cf11992cebd e371f3a83b1d160915817cc1b0e757675419dfc4
git diff --name-only f94c471dfd3771830de864fe6a5d5cf11992cebd e371f3a83b1d160915817cc1b0e757675419dfc4 -- 'references/annotations/**'
git log --oneline f94c471dfd3771830de864fe6a5d5cf11992cebd..e371f3a83b1d160915817cc1b0e757675419dfc4
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-407` | `e371f3a83b1d160915817cc1b0e757675419dfc4`（`ls-remote` 一致） |
| 已审 392 tip | `f94c471dfd3771830de864fe6a5d5cf11992cebd`（是 407 祖先） |
| 相对 392 文件数 | **6**（全部 `A`，无 `M`/`D`，无未声明路径） |
| `references/annotations/**` diff | **0** |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（392 = 407） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（392 = 407） |
| 秘本 blob | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（392 = 407） |
| 紫微主本 `ziwei-doushu-quanshu.json` | blob `0ac9fcb2c1aa75768849a48c332c6658435f1940`（392 = 407） |
| 产品路径 / `chart.*` / WebUI / `6c1dfa3b` | 无 |
| 本岗写出 | 仅本文件 |

相对 392 变更 6 文件（均在声明独占/账本路径内）：

1. `A` `docs/book-reviews/daliuren-daquan-cp13-review.md`
2. `A` `docs/book-reviews/daliuren-daquan-cp14-review.md`
3. `A` `docs/book-reviews/daliuren-daquan-cp15-review.md`
4. `A` `docs/book-reviews/daliuren-daquan-cp16-review.md`
5. `A` `docs/integration/ming-407-integration-ledger.json`
6. `A` `docs/integration/ming-407-integration-ledger.md`

`1c50bbd` 之后五笔只改 407 账本（首推账本 / 记录 tip / remote tip / candidate 对齐 / tip 指针澄清）。未再碰审查稿或注解。未整树迁入任何审查 tip。未合入 MING-398 CP17，未合入 MING-397 秘本 JSON。

## 2. 三文件 SHA 与 392 全等

| 路径 | SHA256（392 = 407） | blob |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7` |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | `66db69fdf39120e4e37733cb59b5ea01a154dcd9` |
| `references/annotations/san-shi/liuren-miben.json` | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821` | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f` |

目标文件 `verified=true`：**0**；识典 1070 / 大六壬 6893 / 秘本 2643 条均为 `verified=false`。

## 3. 合入源 tip 对账

| Pack | 源 tip | 合入方式 | 路径 | blob（源 = 合入 = 账本） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| 大六壬 CP13 MING-387 | `38a9cafeb07a9505d653be5a2374c0c8397164de` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp13-review.md` | `3fd28b6fabfc77062acba470ca4f5094fa8ec0c4` | 207 / 20311 | 否 |
| 大六壬 CP14 MING-390 | `7f2f0fdb41eb44bcfee1ea8d82d7fc8dd6380881` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp14-review.md` | `ceefbded65335b542d867a90b9135999f6785d6c` | 184 / 15170 | 否 |
| 大六壬 CP15 MING-394 | `f8a166678fad11430572efc3c73245d6ebc3e96f` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp15-review.md` | `15985cb12c5de1790f8909e1d65e332f6159fd69` | 202 / 16208 | 否 |
| 大六壬 CP16 MING-395 | `0e051e2beaaa98421f637616b80fb1c98e2511a8` | cherry-pick `-x` | `docs/book-reviews/daliuren-daquan-cp16-review.md` | `36c80d673ec3e91a459cfcda1547b67d2d15d17a` | 207 / 19557 | 否 |

四份审查稿均写明通过（有限范围）且 `source-reviewed` ≠ 人工 `verified`。合入不是空文件、不是截断、不是另写副本。源 tip `ls-remote` 与账本一致。`git diff --stat f94c471..e371f3a`：6 files, +997（全部为 md/json 账本与审查稿）。

## 4. 校验器独立复跑

本岗对 `e371f3a8` 树复跑（本岗 worktree，非 ming-407 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |

相对已审 392：文件数/entries/source_reviewed **不变**（本批未改注解，符合只进 md）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各 CP 语义抽样已由对应审查 Issue 完成；本岗核合入 blob 全等，不重做 392/399 或各审查包。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。三目标文件 `verified=false` 全覆盖（识典 1070、大六壬 6893、秘本 2643）。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-407-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `26b3b07c94b3e8b70395a3d50511180a4da60e5d`；真实远端 tip 是 `e371f3a8`（其后两笔只澄清 tip 指针）。与 MING-392 账本自指滞后同类。不回改 407 账本（非本岗独占文件）。
2. 内容合入 tip `1c50bbd` 与本审查对账一致；其后五笔只动 ledger。不影响合入正确性。
3. 407 叠的是已审 392 tip `f94c471`，不是 399 验收提交 `1442440`（399 审查稿因此不在 407 树）。按 407 Issue 声明，不把未叠 399 文件算作本包失败。
4. 未合入 MING-398 CP17、未合入 MING-397 秘本 JSON（按 Issue 明确不要求、禁止抢写）。不把未合入项算作本包失败。
5. 全库 `files=58` 只是本集成线上的注解文件数，不是全书/大六壬全书/秘本全书完成，更不是产品交付。
6. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 7. remaining / 下一步

- 本 Issue（MING-411）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-407：本批叠 392 合入审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 大六壬 / 秘本注解 JSON remaining 与 CP17 等后续包由协调另派；勿再开第二路集成写入抢 407 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 407。
- 勿重跑 392/399；勿抢产品唯一线 `6c1dfa3b`；勿抢 MING-398 CP17 迁入；勿合入 MING-397 JSON。
