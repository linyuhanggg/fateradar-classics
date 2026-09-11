# MING-415 叠 407 合入独立验收（大六壬 CP17–CP21 与秘本 CP7/CP9 审查稿）

审查对象：`origin/codex/multica-ming-415` @ `065af4177522e59152afdbd1c0fc8f54f80ce703`。基线 `origin/codex/multica-ming-407` @ `e371f3a83b1d160915817cc1b0e757675419dfc4`（MING-411 `b935d17a68b8f8696dd145bf409de174431485ca` 已通过）。本岗工作树 `fateradar-multica-ming-419` / `codex/multica-ming-419`，写出仅本文件。未改注解 JSON、未改 415 已合入审查稿/账本、未改识典/大六壬/秘本/紫微主本 JSON、未升产品唯一线 `6c1dfa3b`。本岗未参与 MING-415 生产。不要重跑已通过的 407/411。不是人工 `verified`，不是大六壬/秘本全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 407 仅 9 路径（7 审查 md `A` + 本批 ledger `A`×2）；**无** `references/annotations/**` diff；识典/大六壬/秘本三文件 SHA256 与 407 **全等**；7 份合入 md 与源 tip blob **全等**；全库校验器 `ok=true`，`errors=[]`；全库与三目标文件 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T17:47Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-407 \
  refs/heads/codex/multica-ming-415 \
  refs/heads/codex/multica-ming-398 \
  refs/heads/codex/multica-ming-402 \
  refs/heads/codex/multica-ming-404 \
  refs/heads/codex/multica-ming-405 \
  refs/heads/codex/multica-ming-410 \
  refs/heads/codex/multica-ming-401 \
  refs/heads/codex/multica-ming-408 \
  refs/heads/codex/multica-ming-411
git ls-remote origin \
  refs/heads/codex/multica-ming-407 \
  refs/heads/codex/multica-ming-415
git merge-base --is-ancestor e371f3a83b1d160915817cc1b0e757675419dfc4 065af4177522e59152afdbd1c0fc8f54f80ce703
git diff --name-status e371f3a83b1d160915817cc1b0e757675419dfc4 065af4177522e59152afdbd1c0fc8f54f80ce703
git diff --name-only e371f3a83b1d160915817cc1b0e757675419dfc4 065af4177522e59152afdbd1c0fc8f54f80ce703 -- 'references/annotations/**'
git log --oneline e371f3a83b1d160915817cc1b0e757675419dfc4..065af4177522e59152afdbd1c0fc8f54f80ce703
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-415` | `065af4177522e59152afdbd1c0fc8f54f80ce703`（`ls-remote` 一致） |
| 已审 407 tip | `e371f3a83b1d160915817cc1b0e757675419dfc4`（是 415 祖先） |
| 相对 407 文件数 | **9**（全部 `A`，无 `M`/`D`，无未声明路径） |
| `references/annotations/**` diff | **0** |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（407 = 415） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（407 = 415） |
| 秘本 blob | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（407 = 415；≠ MING-397 `2789a729…`） |
| 紫微主本 `ziwei-doushu-quanshu.json` | blob `0ac9fcb2c1aa75768849a48c332c6658435f1940`（407 = 415） |
| 产品路径 / `chart.*` / WebUI / `6c1dfa3b` | 无 |
| 飞星 / 皇极审查稿 / 秘本 CP8 | 无 |
| 本岗写出 | 仅本文件 |

相对 407 变更 9 文件（均在声明独占/账本路径内）：

1. `A` `docs/book-reviews/daliuren-daquan-cp17-review.md`
2. `A` `docs/book-reviews/daliuren-daquan-cp18-review.md`
3. `A` `docs/book-reviews/daliuren-daquan-cp19-review.md`
4. `A` `docs/book-reviews/daliuren-daquan-cp20-review.md`
5. `A` `docs/book-reviews/daliuren-daquan-cp21-review.md`
6. `A` `docs/book-reviews/liuren-miben-cp7-review.md`
7. `A` `docs/book-reviews/liuren-miben-cp9-review.md`
8. `A` `docs/integration/ming-415-integration-ledger.json`
9. `A` `docs/integration/ming-415-integration-ledger.md`

`ea1572a` 之后七笔只改 415 账本（首推账本 / 记录 tip / 定稿 tip / 实测澄清 / remote tip / 指针 markdown / 再测 remote tip）。未再碰审查稿或注解。未整树迁入任何审查 tip。未合入 MING-397 秘本 JSON。未抢 MING-406 CP8。未抢飞星/皇极审查稿。

## 2. 三文件 SHA 与 407 全等

| 路径 | SHA256（407 = 415） | blob |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7` |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | `66db69fdf39120e4e37733cb59b5ea01a154dcd9` |
| `references/annotations/san-shi/liuren-miben.json` | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821` | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f` |

目标文件 `verified=true`：**0**；识典 1070 / 大六壬 6893 / 秘本 2643 条均为 `verified=false`。

## 3. 合入源 tip 对账

`ls-remote` 源 tip 与 415 Issue / 账本钉死 SHA 一致。七份均 `cherry-pick -x`，blob 源 = 合入 = 账本。

| Pack | 源 tip | 合入方式 | 路径 | blob（源 = 合入 = 账本） | 行数 / 字节 | 空文件 | 源稿结论 |
|---|---|---|---|---|---|---|---|
| 大六壬 CP17 MING-398 | `307f4ed043b107ad5a9cc3b0a8a7bb4e4dad7d42` | cherry-pick `-x` → `5562e90` | `docs/book-reviews/daliuren-daquan-cp17-review.md` | `ba54d35a4d38a583adee959be609d7958cd2ae49` | 160 / 13484 | 否 | 通过（有限范围） |
| 大六壬 CP18 MING-402 | `aafe566a6dbbae77f845823eaa89fbf842418670` | cherry-pick `-x` → `ac5f38c` | `docs/book-reviews/daliuren-daquan-cp18-review.md` | `1e03f1916c9d1e52623bee6c84a1994e321237dd` | 187 / 15842 | 否 | 通过（有限范围） |
| 大六壬 CP19 MING-404 | `d6d7aa255480ce6eef3da2d9134e2bfc84784ba8` | cherry-pick `-x` → `4829e89` | `docs/book-reviews/daliuren-daquan-cp19-review.md` | `46791e9051369e7e5ae0e50aeee48591431fbf18` | 196 / 17203 | 否 | 通过（有限范围） |
| 大六壬 CP20 MING-405 | `7c99eabd99b0bb5b908e6de7cb34e999faeffee5` | cherry-pick `-x` → `2c1598b` | `docs/book-reviews/daliuren-daquan-cp20-review.md` | `647124ab931c7dcc38ed634a97b8953820a47602` | 209 / 17344 | 否 | 通过（有限范围） |
| 大六壬 CP21 MING-410 | `b82e6074d23a7e36c7eb221c18a0d8fb6d0eeb05` | cherry-pick `-x` → `0753f04` | `docs/book-reviews/daliuren-daquan-cp21-review.md` | `8cc4179b5d9366e5322956c41d257d78c69afba1` | 202 / 17815 | 否 | 通过（有限范围） |
| 秘本 CP7 MING-401 | `9df671c01ec2caf3e48098725b78c998fbfcec76` | cherry-pick `-x` → `1bae97d` | `docs/book-reviews/liuren-miben-cp7-review.md` | `83a3257ead5f9e0331bcab58afc94520dd1617d0` | 163 / 11039 | 否 | 通过 |
| 秘本 CP9 MING-408 | `c7eb6be4f90d08b444340e89b6cadde24c2ec1ca` | cherry-pick `-x` → `ea1572a` | `docs/book-reviews/liuren-miben-cp9-review.md` | `2a2fc19f23f121649096e2158e04c65ac885f0ef` | 190 / 14768 | 否 | 通过 |

七份审查稿均写明通过（有限范围）且 `source-reviewed` ≠ 人工 `verified`。合入不是空文件、不是截断、不是另写副本。`git diff --stat e371f3a..065af417`：9 files, +1546（全部为 md/json 账本与审查稿）。

## 4. 校验器独立复跑

本岗对 `065af417` 树复跑（本岗 worktree，非 ming-415 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |

相对已审 407：文件数/entries/source_reviewed **不变**（本批未改注解，符合只进 md）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各 CP 语义抽样已由对应审查 Issue 完成；本岗核合入 blob 全等，不重做 407/411 或各审查包。

## 5. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。三目标文件 `verified=false` 全覆盖（识典 1070、大六壬 6893、秘本 2643）。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 6. 非阻塞 caveat

1. `ming-415-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `9b704c7d2ed8770d54b4cca0bd8cfa22157f527d`；真实远端 tip 是 `065af417`（其后一笔只再测 remote tip）。与 MING-407 账本自指滞后同类。不回改 415 账本（非本岗独占文件）。
2. 内容合入 tip `ea1572a` 与本审查对账一致；其后七笔只动 ledger。不影响合入正确性。
3. 415 叠的是已审 407 tip `e371f3a`，不是 411 验收提交 `b935d17`（411 验收稿因此不在 415 树）。按 415 Issue 声明，不把未叠 411 文件算作本包失败。
4. 未合入 MING-406 CP8、未合入 MING-397 秘本 JSON、未等 CP22/CP23（按 Issue 明确不要求、禁止抢写）。秘本 SHA 仍 `30b9b2b9…`，不是 397 的 `2789a729…`。不把未合入项算作本包失败。
5. 全库 `files=58` 只是本集成线上的注解文件数，不是全书/大六壬全书/秘本全书完成，更不是产品交付。
6. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 7. remaining / 下一步

- 本 Issue（MING-419）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-415：本批叠 407 合入审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一集成候选由协调另派：合入已审 MING-397 秘本 JSON 与 CP8/CP22/CP23 等；勿再开第二路集成写入抢 415 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 415。
- 勿重跑 407/411；勿抢产品唯一线 `6c1dfa3b`；勿抢飞星/皇极审查稿；勿合入 MING-397 JSON。
