# MING-464 叠 447 合入 439 JSON 与本轮已审审查稿独立验收

审查对象：`origin/codex/multica-ming-464` **远端 tip** `538fd1422053e449c9543b33c6a7c7ce5cbc0108`（不是仅内容 SHA）。基线 `origin/codex/multica-ming-447` @ `77291945bc3d1290099fb6ef617cf07934bfd42d`（独立验收 [MING-454](mention://issue/01a091d0-2ff8-7b0d-affe-3902da90c072) `2b56087ae8f445516ef899c9f45c8f10b37580a6` 通过）。内容合入 tip `893cff12f7bfd12323fe05542568c679472e8e2b`，其后五笔只动 464 账本。本岗工作树 `fateradar-multica-ming-469` / `codex/multica-ming-469`，写出仅本文件。未改注解 JSON、未改 464 已合入审查稿/账本、未升产品唯一线 `6c1dfa3b`。本岗未参与 [MING-464](mention://issue/01a091de-9848-7445-b624-ab42b10efea9) 合入。不要重跑已通过的 424/431/447/454。不要另开第二路集成写入。不是人工 `verified`，不是古籍/八术全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 447 仅 17 路径（14 审查/验收/修复 md `A` + 本批 ledger `A`×2 + 约言 NLC JSON `M`）；注解除命理约言 NLC 外 **57/58 blob 与 447 全等**；约言 SHA256 **命中** `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`（= 439 tip `e4870ee`，≠ 447 `d23db1d8…0be6`）；JSON 内容级仅 5 条 `paragraphId` 由 draft→`source-reviewed`，无增删条目、无 `verified=true`；15 份合入路径 blob 与各自源 tip / 账本 **全等**；447 已有约言 CP1–CP3 审查稿 **未覆盖**；未合入 452 产品定义 ID、未合 461–463/466 独占文件；全库校验器 `ok=true`，`errors=[]`；全库 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T19:24Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-447 \
  refs/heads/codex/multica-ming-454 \
  refs/heads/codex/multica-ming-464 \
  refs/heads/codex/multica-ming-439 \
  refs/heads/codex/multica-ming-442 \
  refs/heads/codex/multica-ming-443 \
  refs/heads/codex/multica-ming-444 \
  refs/heads/codex/multica-ming-445 \
  refs/heads/codex/multica-ming-448 \
  refs/heads/codex/multica-ming-449 \
  refs/heads/codex/multica-ming-450 \
  refs/heads/codex/multica-ming-451 \
  refs/heads/codex/multica-ming-453 \
  refs/heads/codex/multica-ming-455 \
  refs/heads/codex/multica-ming-456 \
  refs/heads/codex/multica-ming-457 \
  refs/heads/codex/multica-ming-461 \
  refs/heads/codex/multica-ming-462 \
  refs/heads/codex/multica-ming-463 \
  refs/heads/codex/multica-ming-466
git ls-remote origin \
  refs/heads/codex/multica-ming-447 \
  refs/heads/codex/multica-ming-454 \
  refs/heads/codex/multica-ming-464 \
  refs/heads/codex/multica-ming-439
git merge-base --is-ancestor 77291945bc3d1290099fb6ef617cf07934bfd42d 538fd1422053e449c9543b33c6a7c7ce5cbc0108
git merge-base --is-ancestor 893cff12f7bfd12323fe05542568c679472e8e2b 538fd1422053e449c9543b33c6a7c7ce5cbc0108
git diff --name-status 77291945bc3d1290099fb6ef617cf07934bfd42d 538fd1422053e449c9543b33c6a7c7ce5cbc0108
git diff --name-status 77291945bc3d1290099fb6ef617cf07934bfd42d 538fd1422053e449c9543b33c6a7c7ce5cbc0108 -- 'references/annotations/**'
git log --oneline 77291945bc3d1290099fb6ef617cf07934bfd42d..538fd1422053e449c9543b33c6a7c7ce5cbc0108
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-464` | `538fd1422053e449c9543b33c6a7c7ce5cbc0108`（`ls-remote` 一致；验收对象是远端 tip） |
| 已审 447 tip | `77291945bc3d1290099fb6ef617cf07934bfd42d`（是 464 祖先，`merge-base --is-ancestor` 退出 0） |
| 已审 454 验收 | `2b56087ae8f445516ef899c9f45c8f10b37580a6`（本批合入其验收稿 blob，不重跑 447/454） |
| 内容合入 tip | `893cff12f7bfd12323fe05542568c679472e8e2b`（是 538fd14 祖先） |
| 相对 447 文件数 | **17**（16×`A` + 1×`M`，无 `D`，无未声明路径） |
| `references/annotations/**` diff | **仅** `mingli-yueyan--nlc-recovery.json` `M` |
| 注解文件数 447 = 464 | **58**；blob **57/58 全等**，1 个为声明合入的约言 NLC |
| 命理约言 NLC SHA256 | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`（Issue 钉死值；= 439 ≠ 447） |
| 命理约言 NLC blob | `b78b2aaed02653306fa546b763445131053a98ea`（464 = 439 ≠ 447 `4877af70…2d4c`） |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（447 = 464） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（447 = 464） |
| 飞星原旨 blob | `9f713a371b7059b2986321c12933a2ceb96c5766`（447 = 464） |
| 皇极 SK1573 blob | `f13177dc55c0e9bf4f49923bbd594e0c23f70659`（447 = 464） |
| 秘本 blob | `c9940ca0125443608cc5487e15d8174427d36fc7`（447 = 464） |
| 星學主本 blob | `ad59a73379148f9ba45a4634ca4d1d2f1d886d65`（447 = 464） |
| 奇门 NLC layouts blob | `a7a4c66578d108cf44a1ab70b3fd161ca6ff54e4`（447 = 464） |
| 产品路径 / `chart.*` / `definition-id` / WebUI | 无（diff 不含；树内无 definition-id 路径） |
| 461/462/463/466 独占路径 | 与本批 17 文件交集 **空**；其独占审查稿在 464 **不存在** |
| 本岗写出 | 仅本文件 |

相对 447 变更 17 文件（均在声明审查稿/439 JSON/账本路径内）：

1. `A` `docs/book-reviews/hanlong-jing-independent-review.md`
2. `A` `docs/book-reviews/huangdi-zhaijing-independent-review.md`
3. `A` `docs/book-reviews/mingli-yueyan-nlc-recovery-five-draft-repair-review.md`
4. `A` `docs/book-reviews/mingli-yueyan-nlc-recovery-five-draft-repair.md`
5. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp5-review.md`
6. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp6-review.md`
7. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp7-review.md`
8. `A` `docs/book-reviews/qingnang-aoyu-independent-review.md`
9. `A` `docs/book-reviews/qingnang-jing-independent-review.md`
10. `A` `docs/book-reviews/xingxue-dacheng-cp5-review.md`
11. `A` `docs/book-reviews/xuexin-fu-independent-review.md`
12. `A` `docs/book-reviews/zangfa-daozhang-independent-review.md`
13. `A` `docs/book-reviews/zangshu-independent-review.md`
14. `A` `docs/integration/ming-447-acceptance-review.md`
15. `A` `docs/integration/ming-464-integration-ledger.json`
16. `A` `docs/integration/ming-464-integration-ledger.md`
17. `M` `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`

`git log --oneline 77291945..538fd14` 十九笔：十四份 `cherry-pick -x`（内容合入 tip `893cff1`）→ `4241da0` 账本 → 四笔账本 pin/finalize/record/align（`5de4024` / `9f915a9` / `8792ca3` / `538fd14`）。未整树迁入。未抢产品唯一线。未改 424/431/447/454 已审树。`git diff --stat 77291945..538fd14`：17 files, +2487 / −30。

## 2. SHA 与 447 对照

| 路径 | SHA256 | 相对 447 |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | 全等 |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | 全等 |
| `references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json` | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95` | 全等 |
| `references/annotations/divination/huangji-jingshi--shidian-SK1573.json` | `05a054d299a123ed20d5c6edaf3a921f0eb3e9fe13a2d9854ecd6ce82effb513` | 全等 |
| `references/annotations/san-shi/liuren-miben.json` | `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347` | 全等 |
| `references/annotations/xingming/xingxue-dacheng.json` | `11316f4428dd25142e7cbfba26c8eb5e17ef9ff10d0033655dbe33335e92dd20` | 全等 |
| `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` | `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca` | 全等 |
| `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928` | **本批声明合入**（≠ 447 `d23db1d8e2df46c63224e573b0a1466a9632bff71cbf13324f8053058f5a0be6`） |
| 其余 50 个注解 JSON | （未列） | 全等 |

全库 58 文件逐文件 blob：equal 57 / changed 1。秘本未在本批再改。识典/大六壬/飞星/皇极/秘本/星學/奇门 NLC 与 447 及既有钉死值一致。

## 3. 命理约言 NLC JSON（已审 439，本批故意合入）

`origin/codex/multica-ming-439` 现 tip `e4870ee31d5ad59834d94cd749b00be447549897`。独立审查 [MING-442](mention://issue/01a091c2-7a02-73ab-9245-257a5002f80f) `cadfad3dee1e56dfb65377d1865a0df404e0b8ef`。447 故意未含此 JSON（MING-454 已记录 447=424 ≠ 439）；本 tip 合入后 SHA256 / blob 与 439 **全等**。

内容级 diff（781 条，无增删 id）：仅 5 条 `paragraphId` 变 `notes` / `review` / `terms` / `vernacular`：

| paragraphId | 447 `review` | 464 `review` | `verified` |
|---|---|---|---|
| `P024:L002-L003` | draft | source-reviewed | 键缺 |
| `P029:L002-L003` | draft | source-reviewed | 键缺 |
| `P037:L002-L003` | draft | source-reviewed | 键缺 |
| `P083:L002-L002` | draft | source-reviewed | 键缺 |
| `P163:L002-L002` | draft | source-reviewed | 键缺 |

约言全书 781：`source-reviewed` 614→619，`draft` 167→162。全库 `source_reviewed` 40405→40410（+5）。五段均无 `verified` 键。447 已有 CP1–CP3 审查稿 blob 与 447 **全等**（`617723c3…` / `c2712865…` / `624f3947…`），未被较旧整文件覆盖。

## 4. 合入源 tip 对账

`ls-remote` 十四个源 tip 与 464 账本 `sourceSha` **全等**。十四笔内容提交均 `cherry-pick -x`，blob 源 = 合入 = 账本；无一空文件、无一截断、无另写副本。

| Pack | 源 tip | 合入 | 路径 | blob（源 = 合入 = 账本） | 行 / 字节 | 空 | 源稿结论 |
|---|---|---|---|---|---|---|---|
| 447 验收 MING-454 | `2b56087ae8f445516ef899c9f45c8f10b37580a6` | `9d0fae1` | `docs/integration/ming-447-acceptance-review.md` | `e5efab96a21893307d2644956a65e9c2a31ab365` | 170 / 14847 | 否 | 通过 |
| 约言 JSON MING-439 | `e4870ee31d5ad59834d94cd749b00be447549897` | `0827d1f` | `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` | `b78b2aaed02653306fa546b763445131053a98ea` | 10648 / 405915 | 否 | 已审五段修复 |
| 约言修复说明 MING-439 | `e4870ee31d5ad59834d94cd749b00be447549897` | `0827d1f` | `docs/book-reviews/mingli-yueyan-nlc-recovery-five-draft-repair.md` | `e128ea66cf1a00e751adcdfed0d0179dcd2566f9` | 69 / 4165 | 否 | 修复说明 |
| 约言五段审查 MING-442 | `cadfad3dee1e56dfb65377d1865a0df404e0b8ef` | `095aaa8` | `docs/book-reviews/mingli-yueyan-nlc-recovery-five-draft-repair-review.md` | `cd34682578ac7d6a4d283d13d78ec19b4e638461` | 98 / 6402 | 否 | 通过 |
| 星學 CP5 MING-443 | `057619eb3a3256eef07868b11e749a2acaf19404` | `c0b761c` | `docs/book-reviews/xingxue-dacheng-cp5-review.md` | `a6b99eb9d79cc43fff55b6602f808c088069f5f8` | 192 / 15548 | 否 | 通过 |
| 奇门 NLC CP5 MING-444 | `1ba8a44ec43e9da25531621339393cbfa0fad366` | `2850fb9` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp5-review.md` | `896dd9de5cccf6bfce1172a9c33beb4666c31b7d` | 154 / 11324 | 否 | 通过 |
| 雪心赋 MING-445 | `4a3b5fe8f3d2ffadd7a1a9de9b1ffb3a16300dd4` | `478d7f0` | `docs/book-reviews/xuexin-fu-independent-review.md` | `ef8e58a01b3266a6a78b2bf8f8dd2e1396387824` | 155 / 10746 | 否 | 通过（有限范围） |
| 葬书 MING-448 | `8965ddd9a858963de36c4c67c15609dd91a4c048` | `b27175b` | `docs/book-reviews/zangshu-independent-review.md` | `757ee0a47c5fef0df16b9ca07e74d86a83bd42bb` | 154 / 10833 | 否 | 通过（有限范围） |
| 奇门 NLC CP6 MING-449 | `99421c59f1b08ab926add0a29c7683cb6f194a0a` | `84cb0f7` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp6-review.md` | `9a30a2801de30779c5c21ae5c01fa6b24089207e` | 156 / 11679 | 否 | 通过 |
| 青囊经 MING-450 | `091c2de609465a4df2ac02895a3b7fb2ae73744d` | `e5b57f5` | `docs/book-reviews/qingnang-jing-independent-review.md` | `33c20705f827777f840e411122db7475737f6ce2` | 163 / 11092 | 否 | 通过 |
| 黄帝宅经 MING-451 | `63917f80c5ec021d52b6d766b92be266d08d083c` | `773e976` | `docs/book-reviews/huangdi-zhaijing-independent-review.md` | `677238f491cf43840f3a301f81ebc6ab47fe9293` | 158 / 11386 | 否 | 通过 |
| 撼龙经 MING-453 | `90ae6a6cb518ee5051d4b0305035b538d07c2546` | `0b9c6ad` | `docs/book-reviews/hanlong-jing-independent-review.md` | `4e54612ecbce884a3d85205f730d56691e9b95ab` | 165 / 11094 | 否 | 通过 |
| 奇门 NLC CP7 MING-455 | `cf154ddee43fb61d5a7041678aba6e713b0e1d3c` | `99414f9` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp7-review.md` | `d5fe4f94bf4e357fa1a28ada14ea33aea1548431` | 155 / 11798 | 否 | 通过 |
| 葬法倒杖 MING-456 | `4c2b0f99204619a843d8b6c605c5f2d77be5f8a6` | `4e4fa27` | `docs/book-reviews/zangfa-daozhang-independent-review.md` | `802b99f8ecda2d099d0da8f55b33fb7854f4acf7` | 160 / 11454 | 否 | 通过 |
| 青囊奥语 MING-457 | `4a79f218d36398005b1405386b11d4b044c16221` | `893cff1` | `docs/book-reviews/qingnang-aoyu-independent-review.md` | `a1f1ed11a2db0c146125fec2220b0170db44c3a2` | 144 / 9956 | 否 | 通过 |

源稿均写明通过（或有限范围），且 `source-reviewed` ≠ 人工 `verified`。本岗核合入 blob 全等与注解范围，不重做 424/431/447/454 或各审查包语义。

## 5. 未合入 452 / 461–463 / 466

- 古籍仓 **无** `codex/multica-ming-452`；464 树无 `definition-id` / `chart.*` / 账号 / 支付 / 后端路径。
- `origin/codex/multica-ming-461` `402393af`、`462` `e92efab9`、`463` `80a1734b`、`466` `54c7d0a5` **都不是** 464 祖先。相对 447 的文件集与本批 17 路径交集为空。
- 其独占审查稿在 464 **均不存在**：`qimen-dunjia-tongzhi-nlc-layouts-remaining-2100-2470-review.md`（461）、`qimen-dunjia-tongzhi-yanyi-vol4-9-independent-review.md`（462）、`shenfeng-tongkao-independent-review.md`（463）、`qingnang-xu-independent-review.md`（466）。
- 458–460 在本古籍仓无对应施工分支；diff 亦不含产品定义 ID。

## 6. 校验器独立复跑

本岗对 `538fd14` 树复跑（本岗 worktree，非 ming-464 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40410 | `[]` |

相对已审 447：文件数 / entries 不变；`source_reviewed` **+5**（约言五段 draft→SR，与 JSON 内容级 diff 一致）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各审查包语义抽样已由对应审查 Issue 完成。

## 7. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。其中显式 `false` 24904、缺键 17930。约言 781 条全部缺 `verified` 键。秘本 / 识典 / 大六壬 / 飞星 / 皇极 / 星學 / 奇门 NLC 目标文件均无 `verified=true`。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 8. 非阻塞 caveat

1. `ming-464-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` / `remoteSha` 仍写 `8792ca32354a7108ff500fb365b972ea61fc31a6`；真实远端 tip 是 `538fd142`（其后一笔 `538fd14` 只修账本 tip 行，未把上述三字段改到自身）。账本 `note` 已声明以 `ls-remote` 为准。与 MING-447 账本自指滞后同类。不回改 464 账本（非本岗独占文件）。
2. 内容合入 tip `893cff1` 与本审查对账一致；其后五笔只动 ledger。不影响合入正确性。
3. `2b56087`（454 分支 tip）**不是** 464 的 git 祖先，因为验收稿是 `cherry-pick -x` 为 `9d0fae1`。blob 已与源 tip 全等。
4. `6c1dfa3b` 仅作为「禁止升产品唯一线」政策文字出现在账本/既有验收稿，不构成升线。diff 不含产品路径。
5. 461–463/466 现 tip 在 464 交包后可能已完成，但其独占文件未进本 tip；本岗不审这些包，也不把「当时未完成」写成「永远不合」。
6. 全库 `files=58` / `source_reviewed=40410` 只是本集成线上的注解文件数，不是全书 / 星學 / 奇门 NLC / 命理约言 / 风水诸书完成，更不是产品交付。
7. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 9. remaining / 下一步

- 本 Issue（MING-469）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-464：本批叠 447 合入 439 JSON 与本轮已审审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一集成候选由协调另派（452 产品定义 ID 与 461–463/466 仅在其独立审查通过后）。勿再开第二路集成写入抢 464 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 464。
- 勿重跑 424/431/447/454；勿抢产品唯一线 `6c1dfa3b`。
