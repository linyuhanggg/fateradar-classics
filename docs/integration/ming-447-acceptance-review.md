# MING-447 叠 424 合入已审审查稿独立验收（不含 439 JSON）

审查对象：`origin/codex/multica-ming-447` @ `77291945bc3d1290099fb6ef617cf07934bfd42d`。基线 `origin/codex/multica-ming-424` @ `85d172a68d47508db9a1cb19a32c89eeceae977a`（独立验收 [MING-431](mention://issue/01a091a8-bddc-7c83-b1ed-ec94acd89f08) `8a5b69242409cc3a4909c1a40984eaf1f90a09c2` 通过）。本岗工作树 `fateradar-multica-ming-454` / `codex/multica-ming-454`，写出仅本文件。未改注解 JSON、未改 447 已合入审查稿/账本、未合入 [MING-439](mention://issue/01a091bb-b3eb-76a6-8d7a-96a18df7d7b5) JSON、未升产品唯一线 `6c1dfa3b`。本岗未参与 MING-447 生产。不要重跑已通过的 424/431。不要另开第二路集成写入。不是人工 `verified`，不是古籍/八术全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 424 仅 18 路径（16 审查/验收 md `A` + 本批 ledger `A`×2）；`references/annotations/**` **无** diff；58/58 注解 blob 与 424 **全等**（秘本 SHA256 仍 `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347`）；16 份合入 md 与各自源 tip / 账本 blob **全等**；命理约言 NLC JSON 447 = 424 ≠ 439；全库校验器 `ok=true`，`errors=[]`；全库 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11T18:54Z）：

```
git fetch origin \
  refs/heads/codex/multica-ming-424 \
  refs/heads/codex/multica-ming-447 \
  refs/heads/codex/multica-ming-431 \
  refs/heads/codex/multica-ming-439 \
  refs/heads/codex/multica-ming-425 \
  refs/heads/codex/multica-ming-426 \
  refs/heads/codex/multica-ming-441 \
  refs/heads/codex/multica-ming-440 \
  refs/heads/codex/multica-ming-422 \
  refs/heads/codex/multica-ming-429 \
  refs/heads/codex/multica-ming-433 \
  refs/heads/codex/multica-ming-437 \
  refs/heads/codex/multica-ming-421 \
  refs/heads/codex/multica-ming-430 \
  refs/heads/codex/multica-ming-434 \
  refs/heads/codex/multica-ming-438 \
  refs/heads/codex/multica-ming-423 \
  refs/heads/codex/multica-ming-428 \
  refs/heads/codex/multica-ming-435 \
  refs/heads/codex/multica-ming-442 \
  refs/heads/codex/multica-ming-443 \
  refs/heads/codex/multica-ming-444 \
  refs/heads/codex/multica-ming-445
git ls-remote origin \
  refs/heads/codex/multica-ming-424 \
  refs/heads/codex/multica-ming-447 \
  refs/heads/codex/multica-ming-431 \
  refs/heads/codex/multica-ming-439
git merge-base --is-ancestor 85d172a68d47508db9a1cb19a32c89eeceae977a 77291945bc3d1290099fb6ef617cf07934bfd42d
git diff --name-status 85d172a68d47508db9a1cb19a32c89eeceae977a 77291945bc3d1290099fb6ef617cf07934bfd42d
git diff --name-only 85d172a68d47508db9a1cb19a32c89eeceae977a 77291945bc3d1290099fb6ef617cf07934bfd42d -- 'references/annotations/**'
git log --oneline 85d172a68d47508db9a1cb19a32c89eeceae977a..77291945bc3d1290099fb6ef617cf07934bfd42d
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-447` | `77291945bc3d1290099fb6ef617cf07934bfd42d`（`ls-remote` 一致） |
| 已审 424 tip | `85d172a68d47508db9a1cb19a32c89eeceae977a`（是 447 祖先，`merge-base --is-ancestor` 退出 0） |
| 已审 431 验收 | `8a5b69242409cc3a4909c1a40984eaf1f90a09c2`（本批合入其验收稿，不重跑 424/431） |
| 相对 424 文件数 | **18**（18×`A`，无 `M`，无 `D`，无未声明路径） |
| `references/annotations/**` diff | **空** |
| 注解文件数 424 = 447 | **58**；blob **58/58 全等** |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（424 = 447） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（424 = 447） |
| 飞星原旨 blob | `9f713a371b7059b2986321c12933a2ceb96c5766`（424 = 447） |
| 皇极 SK1573 blob | `f13177dc55c0e9bf4f49923bbd594e0c23f70659`（424 = 447） |
| 秘本 blob | `c9940ca0125443608cc5487e15d8174427d36fc7`（424 = 447） |
| 命理约言 NLC blob | `4877af70002217fded78e17cecb3564e1b772d4c`（424 = 447 ≠ 439 `b78b2aaed02653306fa546b763445131053a98ea`） |
| 星學主本 blob | `ad59a73379148f9ba45a4634ca4d1d2f1d886d65`（424 = 447） |
| 奇门 NLC layouts blob | `a7a4c66578d108cf44a1ab70b3fd161ca6ff54e4`（424 = 447） |
| 产品路径 / `chart.*` / WebUI | 无（diff 不含） |
| 442/443/444/445 独占路径 | 与本批 18 文件交集 **空** |
| 本岗写出 | 仅本文件 |

相对 424 变更 18 文件（均在声明审查稿/账本路径内）：

1. `A` `docs/book-reviews/guotian-jing-independent-review.md`
2. `A` `docs/book-reviews/tianyu-jing-independent-review.md`
3. `A` `docs/book-reviews/yilong-jing-independent-review.md`
4. `A` `docs/book-reviews/rudi-yan-quanshu-independent-review.md`
5. `A` `docs/book-reviews/xingxue-dacheng-cp1-review.md`
6. `A` `docs/book-reviews/xingxue-dacheng-cp2-review.md`
7. `A` `docs/book-reviews/xingxue-dacheng-cp3-review.md`
8. `A` `docs/book-reviews/xingxue-dacheng-cp4-review.md`
9. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp1-review.md`
10. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp2-review.md`
11. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp3-review.md`
12. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp4-review.md`
13. `A` `docs/book-reviews/mingli-yueyan-nlc-recovery-cp1-review.md`
14. `A` `docs/book-reviews/mingli-yueyan-nlc-recovery-cp2-review.md`
15. `A` `docs/book-reviews/mingli-yueyan-nlc-recovery-cp3-review.md`
16. `A` `docs/integration/ming-424-acceptance-review.md`
17. `A` `docs/integration/ming-447-integration-ledger.json`
18. `A` `docs/integration/ming-447-integration-ledger.md`

`git log --oneline 85d172a..77291945` 二十笔：十六份审查/验收稿 `cherry-pick -x`（内容合入 tip `0ca6fb6`）→ `c3a911a` 账本 → 三笔账本 pin/verify/repair（`6a4a900` / `b69e1eb` / `7729194`）。未整树迁入。未抢产品唯一线。未改 424/431 已审树。

## 2. SHA 与 424 全等（含秘本）

| 路径 | SHA256 | 相对 424 |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | 全等 |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | 全等 |
| `references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json` | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95` | 全等 |
| `references/annotations/divination/huangji-jingshi--shidian-SK1573.json` | `05a054d299a123ed20d5c6edaf3a921f0eb3e9fe13a2d9854ecd6ce82effb513` | 全等 |
| `references/annotations/san-shi/liuren-miben.json` | `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347` | 全等（Issue 钉死值） |
| `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` | `d23db1d8e2df46c63224e573b0a1466a9632bff71cbf13324f8053058f5a0be6` | 全等（≠ 439 `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`） |
| `references/annotations/xingming/xingxue-dacheng.json` | `11316f4428dd25142e7cbfba26c8eb5e17ef9ff10d0033655dbe33335e92dd20` | 全等 |
| `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` | `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca` | 全等 |
| 其余 50 个注解 JSON | （未列） | 全等 |

全库 58 文件逐文件 blob：equal 58 / diff 0。秘本未在本批再改。识典/大六壬/飞星/皇极/秘本与 424 及 Issue 钉死值一致。

## 3. 未合入 MING-439 JSON

`origin/codex/multica-ming-439` 现 tip `e4870ee31d5ad59834d94cd749b00be447549897`。相对 424，439 的 `mingli-yueyan--nlc-recovery.json` blob 为 `b78b2aaed02653306fa546b763445131053a98ea`（SHA256 `09cdbccf…3928`）。447 该文件仍是 424 的 `4877af70…2d4c` / `d23db1d8…0be6`。本 tip 故意未含 439 JSON，符合 Issue 禁令。

## 4. 合入源 tip 对账

`ls-remote` 十六个源 tip 与 447 账本 `sourceSha` **全等**。十六份 md 均 `cherry-pick -x`，blob 源 = 合入 = 账本；无一空文件、无一截断、无另写副本。

| Pack | 源 tip | 合入 | 路径 | blob（源 = 合入 = 账本） | 行 / 字节 | 空 | 源稿结论 |
|---|---|---|---|---|---|---|---|
| 424 验收 MING-431 | `8a5b69242409cc3a4909c1a40984eaf1f90a09c2` | `a8e9ba3` | `docs/integration/ming-424-acceptance-review.md` | `f1765802b58bab43be61f537143a33430f2d4387` | 154 / 12452 | 否 | 通过 |
| 果老 MING-425 | `b10ae285aae9a34e82c70fc9f8562e5f9cfaf9c6` | `8d9ac07` | `docs/book-reviews/guotian-jing-independent-review.md` | `290f2fa6192bcbfd51bfd11e74d55739bb98fc3a` | 170 / 15915 | 否 | 通过（有限范围） |
| 天玉 MING-426 | `f06a6874444036787190bcad4f0821c8d810c639` | `8ba6f00` | `docs/book-reviews/tianyu-jing-independent-review.md` | `8a0c8a65adfec0d23de5a96b759c943d89cfcc29` | 140 / 8304 | 否 | 通过（有限范围） |
| 疑龙 MING-441 | `297638d6519673406f8d29be40c47dca7fd32066` | `52cce6c` | `docs/book-reviews/yilong-jing-independent-review.md` | `ce8be619270c9e9a7365b12945f39728fdcaf898` | 164 / 10885 | 否 | 通过（有限范围） |
| 入地眼 MING-440 | `4c12db7fc3918624a04ce86147247f97c2b8f33b` | `a4d2614` | `docs/book-reviews/rudi-yan-quanshu-independent-review.md` | `329c9af6c525bdd62459b93d897d5ab35e496a02` | 163 / 11918 | 否 | 通过 |
| 星學 CP1 MING-422 | `d83e4b4ceecb117ad4eefde01e29edb0c60ea39b` | `bc56ecd` | `docs/book-reviews/xingxue-dacheng-cp1-review.md` | `3e49b535a9d48c30c5eb8f815c9948c51e616335` | 179 / 12793 | 否 | 通过 |
| 星學 CP2 MING-429 | `d9db9829deb9a016739a6a2542246f112c686b89` | `b192969` | `docs/book-reviews/xingxue-dacheng-cp2-review.md` | `48af4f65e166dbac19ba7515f3b9eb781984eb87` | 186 / 14371 | 否 | 通过 |
| 星學 CP3 MING-433 | `b3516875d041ad1a20dc5547dca1f1825785c963` | `906bb18` | `docs/book-reviews/xingxue-dacheng-cp3-review.md` | `946eca9a550d5b21c4a8d6c01f4b41527e4ae958` | 193 / 15675 | 否 | 通过 |
| 星學 CP4 MING-437 | `e0d8bc0ce063aadedd0f662f5724c9de9d971e11` | `83ad16f` | `docs/book-reviews/xingxue-dacheng-cp4-review.md` | `cd3f16ded4488a4177f414e473f84a342dc13943` | 195 / 15872 | 否 | 通过 |
| 奇门 NLC CP1 MING-421 | `839e2840893f621a3c57fe6d54efc3683e321355` | `e0c6b03` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp1-review.md` | `d56e3c923ddacdc033663af5c4b76cc5bc483b81` | 149 / 10685 | 否 | 通过 |
| 奇门 NLC CP2 MING-430 | `05dd8bf74fa29693bf296a748a273748ac090999` | `0f0b8cf` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp2-review.md` | `a6c998d2773661617a35f7efbe476f2a789337a3` | 154 / 11090 | 否 | 通过 |
| 奇门 NLC CP3 MING-434 | `e5a58e81a8c2572f8e0d13557219d40364d30db1` | `6597c7a` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp3-review.md` | `a8807c44f21e9dd0625e952f1d4fa75ac5337509` | 153 / 10759 | 否 | 通过 |
| 奇门 NLC CP4 MING-438 | `884c4acc5cba557616814af1230041b41731d3a2` | `ba5b1a1` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-cp4-review.md` | `d3766a7c29210674cef7dd7eb8d9754cd3f79ce6` | 154 / 10999 | 否 | 通过 |
| 约言 NLC CP1 MING-423 | `61fe88b75a33727cb80cfcfcba1caa0d2a66597f` | `a19ae0b` | `docs/book-reviews/mingli-yueyan-nlc-recovery-cp1-review.md` | `617723c3ec642bd49c8f155cc0e8e0a5a18270b6` | 174 / 12525 | 否 | 通过（本包 224 SR） |
| 约言 NLC CP2 MING-428 | `d6a0714ed1983af34575398510031a061f1b76c1` | `9fa5f47` | `docs/book-reviews/mingli-yueyan-nlc-recovery-cp2-review.md` | `c2712865b1c15608faf9d9622eaf4cc90b673a06` | 154 / 11305 | 否 | 通过（本包 254 SR） |
| 约言 NLC CP3 MING-435 | `9153372ad0f77dce2bf02dc2e2f20bee39d1e3b6` | `0ca6fb6` | `docs/book-reviews/mingli-yueyan-nlc-recovery-cp3-review.md` | `624f39470a6d5abc27e1b66487d3a12fc7657f2c` | 148 / 11501 | 否 | 通过（本包 136 SR） |

十六份源稿均写明通过（或有限范围），且 `source-reviewed` ≠ 人工 `verified`。`git diff --stat 85d172a..77291945`：18 files, +3003 / −0。

## 5. 校验器独立复跑

本岗对 `77291945` 树复跑（本岗 worktree，非 ming-447 活生产树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40405 | `[]` |

相对已审 424：文件数 / entries / source_reviewed **不变**（本批未改任何注解）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各审查包语义抽样已由对应审查 Issue 完成；本岗核合入 blob 全等与注解未动，不重做 424/431 或各审查包。

## 6. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。其中显式 `false` 24904、缺键 17930（与奇门 NLC / 约言 NLC 等源稿记录一致），无一为 true。秘本 / 识典 / 大六壬 / 飞星 / 皇极 / 约言 NLC / 星學 / 奇门 NLC 目标文件均无 `verified=true`。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 7. 非阻塞 caveat

1. `ming-447-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `c3a911ac03d9be483c2243d6b9e86cd8228338cf`；真实远端 tip 是 `77291945`（其后三笔只修账本 tip 行）。账本 `note` 已声明以 `ls-remote` 为准。与 MING-424 账本自指滞后同类。不回改 447 账本（非本岗独占文件）。
2. 内容合入 tip `0ca6fb6` 与本审查对账一致；其后四笔只动 ledger。不影响合入正确性。
3. 十六份审查稿多数在权威 329 树上写成后 `cherry-pick -x` 进来。合入 blob 已与源 tip 全等。
4. `6c1dfa3b` 仅作为「禁止升产品唯一线」政策文字出现在账本/既有验收稿，不构成升线。diff 不含产品路径。
5. 442/443/444/445 现 tip 相对 424 的文件集与本批 18 路径交集为空；本岗不审这些在跑包。
6. 全库 `files=58` 只是本集成线上的注解文件数，不是全书 / 果老 / 天玉 / 疑龙 / 入地眼 / 星學 / 奇门 NLC / 命理约言全书完成，更不是产品交付。
7. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。

## 8. remaining / 下一步

- 本 Issue（MING-454）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-447：本批叠 424 合入 16 份已审审查/验收稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一集成候选由协调另派（439 JSON 与 442–445 仅在其独立审查通过后）。勿再开第二路集成写入抢 447 树。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 447。
- 勿重跑 424/431；勿抢产品唯一线 `6c1dfa3b`；勿合入尚未独立审查的 439 JSON。
