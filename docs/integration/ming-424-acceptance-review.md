# MING-424 叠 415 合入独立验收（397 秘本 CP4 JSON 与 CP8/22/23 + SK1573 CP3 / 飞星 CP1–CP2 审查稿）

审查对象：`origin/codex/multica-ming-424` @ `85d172a68d47508db9a1cb19a32c89eeceae977a`。基线 `origin/codex/multica-ming-415` @ `065af4177522e59152afdbd1c0fc8f54f80ce703`（独立验收 [MING-419](mention://issue/01a09191-f810-72ac-a581-f5a2222efb14) `e788977fd6aeabe48339d26de696548d9108f13e` 通过）。权威 329 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`（审查稿源对照，不是 424 祖先）。本岗工作树 `fateradar-multica-ming-431` / `codex/multica-ming-431`，写出仅本文件。未改注解 JSON、未改 424 已合入审查稿/账本、未改识典/大六壬/飞星/皇极 JSON、未升产品唯一线 `6c1dfa3b`。本岗未参与 MING-424 生产。不要重跑已通过的 415/419。不要抢 425/427/428/429/430 文件。不是人工 `verified`，不是大六壬/秘本/皇极/飞星全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 415 仅 9 路径（6 审查 md `A` + 本批 ledger `A`×2 + 秘本 JSON `M`）；注解 JSON 除秘本外 57 文件 SHA256 与 415 **全等**；秘本仅 4 条 paragraphId 的 vernacular/notes 变更，`verified` 全 false；6 份合入 md 与源 tip blob **全等**；秘本 blob 与 397/403 `6f9ae513` **全等**；全库校验器 `ok=true`，`errors=[]`；全库与目标文件 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T18:34Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-415 \
  refs/heads/codex/multica-ming-424 \
  refs/heads/codex/multica-ming-419 \
  refs/heads/codex/multica-ming-329 \
  refs/heads/codex/multica-ming-397 \
  refs/heads/codex/multica-ming-403 \
  refs/heads/codex/multica-ming-406 \
  refs/heads/codex/multica-ming-412 \
  refs/heads/codex/multica-ming-413 \
  refs/heads/codex/multica-ming-416 \
  refs/heads/codex/multica-ming-417 \
  refs/heads/codex/multica-ming-418
git ls-remote origin \
  refs/heads/codex/multica-ming-415 \
  refs/heads/codex/multica-ming-424 \
  refs/heads/codex/multica-ming-329
git merge-base --is-ancestor 065af4177522e59152afdbd1c0fc8f54f80ce703 85d172a68d47508db9a1cb19a32c89eeceae977a
git diff --name-status 065af4177522e59152afdbd1c0fc8f54f80ce703 85d172a68d47508db9a1cb19a32c89eeceae977a
git diff --name-only 065af4177522e59152afdbd1c0fc8f54f80ce703 85d172a68d47508db9a1cb19a32c89eeceae977a -- 'references/annotations/**'
git log --oneline 065af4177522e59152afdbd1c0fc8f54f80ce703..85d172a68d47508db9a1cb19a32c89eeceae977a
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-424` | `85d172a68d47508db9a1cb19a32c89eeceae977a`（`ls-remote` 一致） |
| 已审 415 tip | `065af4177522e59152afdbd1c0fc8f54f80ce703`（是 424 祖先） |
| 相对 415 文件数 | **9**（8×`A` + 1×`M`，无 `D`，无未声明路径） |
| `references/annotations/**` diff | **仅** `san-shi/liuren-miben.json` |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（415 = 424） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（415 = 424） |
| 飞星原旨 blob | `9f713a371b7059b2986321c12933a2ceb96c5766`（415 = 424） |
| 皇极 SK1573 blob | `f13177dc55c0e9bf4f49923bbd594e0c23f70659`（415 = 424） |
| 秘本 blob | 415 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f` → 424 `c9940ca0125443608cc5487e15d8174427d36fc7`（= 397/403 `6f9ae513`） |
| 注解文件数 415 = 424 | **58**；除秘本外 SHA256 **57 全等** |
| 产品路径 / `chart.*` / WebUI / `6c1dfa3b` | 无（diff 不含；`6c1dfa3b` 未出现在 415..424 patch） |
| 425/427/428/429/430 路径 | 无 |
| 本岗写出 | 仅本文件 |

相对 415 变更 9 文件（均在声明独占/账本路径内）：

1. `A` `docs/book-reviews/liuren-miben-cp8-review.md`
2. `A` `docs/book-reviews/daliuren-daquan-cp22-review.md`
3. `A` `docs/book-reviews/daliuren-daquan-cp23-review.md`
4. `A` `docs/book-reviews/huangji-jingshi-sk1573-cp3-review.md`
5. `A` `docs/book-reviews/feixing-ziwei-doushu-yuanzhi-cp1-review.md`
6. `A` `docs/book-reviews/feixing-ziwei-doushu-yuanzhi-cp2-review.md`
7. `A` `docs/integration/ming-424-integration-ledger.json`
8. `A` `docs/integration/ming-424-integration-ledger.md`
9. `M` `references/annotations/san-shi/liuren-miben.json`

`git log --oneline 065af417..85d172a` 九笔：`85b65a3` cherry-pick 397 JSON → 六份审查稿 `cherry-pick -x` → `b385004` 账本 → `85d172a` 只再测 remote tip。未整树迁入。未抢产品唯一线。未改 415/419 已审树。

## 2. SHA 与 415 全等（除秘本）

| 路径 | SHA256 | 相对 415 |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | 全等 |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | 全等 |
| `references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json` | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95` | 全等 |
| `references/annotations/divination/huangji-jingshi--shidian-SK1573.json` | `05a054d299a123ed20d5c6edaf3a921f0eb3e9fe13a2d9854ecd6ce82effb513` | 全等 |
| `references/annotations/san-shi/liuren-miben.json` | 415 `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821` → 424 `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347` | 仅此文件变 |
| 其余 53 个注解 JSON | （未列） | 全等 |

全库 58 文件逐文件 SHA256：equal 57 / diff 1（仅秘本）。识典/大六壬/飞星/皇极与 Issue 钉死值一致。

## 3. 秘本仅 L5920/22/24/26 vernacular/notes

条目总数 415 = 424 = **2643**；pid 集全等。变更 paragraphId 恰好 4 条，与声明一致：

| paragraphId | 文件索引 | 变更字段 | verified |
|---|---|---|---|
| `liuren-miben:L5920-L5920` | 1189 | vernacular + notes | false → false |
| `liuren-miben:L5922-L5922` | 1190 | vernacular + notes | false → false |
| `liuren-miben:L5924-L5924` | 1191 | vernacular + notes | false → false |
| `liuren-miben:L5926-L5926` | 1192 | vernacular | false → false |

其余字段（`kind` / `review` / `terms` 等）四条均与 415 **全等**。其余 **2639** 条对象级全等。`review` 仍为 `source-reviewed`，未升 `verified`。

对照 `sources/fulltext/san-shi/liuren-miben/fulltext.md`：这是相邻行白话错位回绑，不是另写新义。

- L5920 原文「年上吉神雖立勝…三人以上皆詳此只看行年上立」——424 把原错落到 L5922 的「三人以上/多人仍各看行年」收回本行。
- L5922 原文「同年主客以乘除如二人同年，即看主客」——424 收回原在 L5924 的同年主客句。
- L5924 原文「先起為客應為主，客是乾兮主是支。支干上下言凶吉…」——424 收回先起为客/支干上下句。
- L5926 原文「對敵從何推勝負，支干年上定贏輸…」——424 去掉错入的支干上下句。

秘本 blob 424 = 397 `6f9ae513` = 403 `a8234f0f` = `c9940ca0125443608cc5487e15d8174427d36fc7`。合入是 `cherry-pick -x` 自 397，不是另写副本。索引 1189–1192 不在 CP8（2100–2399）范围内。

秘本 `verified=true`：**0** / 2643 全 `false`。

## 4. 合入源 tip 对账

`ls-remote` 源 tip 与 424 账本钉死 SHA 一致。六份审查稿 + 397 JSON 均 `cherry-pick -x`，blob 源 = 合入 = 账本。

| Pack | 源 tip | 合入方式 | 路径 | blob（源 = 合入 = 账本） | 行数 / 字节 | 空文件 | 源稿结论 |
|---|---|---|---|---|---|---|---|
| 秘本 CP4 vern MING-397 | `6f9ae5139f3a1cdd6e26496a12f0961e8ff5cdc6` | cherry-pick `-x` → `85b65a3` | `references/annotations/san-shi/liuren-miben.json` | `c9940ca0125443608cc5487e15d8174427d36fc7` | — | 否 | 403 已独立审该 JSON |
| 秘本 CP8 MING-406 | `8197f92f566d260b3f290a59b2827bc1107b6cc6` | cherry-pick `-x` → `8b7c5ce` | `docs/book-reviews/liuren-miben-cp8-review.md` | `bb3754108ecc032ef68ad3999c9ff25024189a2d` | 153 / 10873 | 否 | 通过 |
| 大六壬 CP22 MING-412 | `f40840fd819810e192fa72581464fa377bb3a14d` | cherry-pick `-x` → `6973215` | `docs/book-reviews/daliuren-daquan-cp22-review.md` | `9d6e7b417af13899a64a110ad6701060f0175939` | 212 / 17994 | 否 | 通过（有限范围） |
| 大六壬 CP23 MING-413 | `75b9e2ba216484ef2c8a86310b0acd11cdd7994d` | cherry-pick `-x` → `f50a95b` | `docs/book-reviews/daliuren-daquan-cp23-review.md` | `9934f6928ab98dbea9ecf7921f48b2a15b0417d3` | 194 / 15906 | 否 | 通过（有限范围） |
| 皇极 SK1573 CP3 MING-416 | `a66d5d96ab9f84cfa52e0808d230e9a7dd9973f8` | cherry-pick `-x` → `800e09e` | `docs/book-reviews/huangji-jingshi-sk1573-cp3-review.md` | `fc7dce60e7bd1db15fee95166d0a7c98178c1c48` | 159 / 10944 | 否 | 通过 |
| 飞星 CP1 MING-417 | `19fb31b973891ea549c3d66e3a0506149111ea50` | cherry-pick `-x` → `62bef5a` | `docs/book-reviews/feixing-ziwei-doushu-yuanzhi-cp1-review.md` | `88d2951f1b1850c745a24ca0dc57c514fc125cc9` | 167 / 11532 | 否 | 通过 |
| 飞星 CP2 MING-418 | `21d06e608c47a5da1d3c802bebcbec82a60b4edf` | cherry-pick `-x` → `fd4106a` | `docs/book-reviews/feixing-ziwei-doushu-yuanzhi-cp2-review.md` | `23beda55115cd931b2cd66993cc403819cf43528` | 158 / 12025 | 否 | 通过 |

六份审查稿均写明通过（或有限范围）且 `source-reviewed` ≠ 人工 `verified`。合入不是空文件、不是截断、不是另写副本。`git diff --stat 065af417..85d172a`：9 files, +1292 / −7。

## 5. 校验器独立复跑

本岗对 `85d172a` 树复跑（本岗 worktree，非 ming-424 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |

相对已审 415：文件数/entries/source_reviewed **不变**（四条本就是 `source-reviewed`，只改 vernacular/notes）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各 CP 语义抽样已由对应审查 Issue 完成；本岗核合入 blob 全等与秘本四条回绑，不重做 415/419 或各审查包。

## 6. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。秘本 2643、识典、大六壬、飞星、皇极目标文件均无 `verified=true`。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 7. 非阻塞 caveat

1. `ming-424-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `b3850048a9b0261ddf8b01521a0fe9215fdf16dd`；真实远端 tip 是 `85d172a`（其后一笔只再测 remote tip）。与 MING-415 账本自指滞后同类。不回改 424 账本（非本岗独占文件）。
2. 内容合入 tip `fd4106a` 与本审查对账一致；其后两笔只动 ledger。不影响合入正确性。
3. 424 叠的是已审 415 tip `065af417`，不是 419 验收提交 `e788977f`（419 验收稿因此不在 424 树）。按 Issue 声明，不把未叠 419 文件算作本包失败。
4. 权威 329 `6effd8e4` 不是 415/424 祖先；审查稿在 329 树上写成后 `cherry-pick -x` 进来。合入 blob 已与源 tip 全等。
5. L5924 原文「客是乾兮」白话作「客是干兮」——415 已如此，非本批引入；不回改。
6. CP8 源稿记录的秘本 SHA 仍是 415 的 `30b9b2b9…`（审 329 树、索引 2100–2399）；本批叠入的 397 四条是索引 1189–1192，范围不重叠。
7. 全库 `files=58` 只是本集成线上的注解文件数，不是全书/大六壬全书/秘本全书/皇极全书/飞星全书完成，更不是产品交付。
8. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 8. remaining / 下一步

- 本 Issue（MING-431）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-424：本批叠 415 合入 397 JSON 与六份审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一集成候选由协调另派；勿再开第二路集成写入抢 424 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 424。
- 勿重跑 415/419；勿抢产品唯一线 `6c1dfa3b`；勿抢 425/427/428/429/430。
