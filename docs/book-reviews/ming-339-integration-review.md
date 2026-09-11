# MING-339 审查稿增量独立审查（312/313/317/335）

审查对象：`origin/codex/multica-ming-339` @ `642dbc4683b5e352de45f97265b2794a881be3cb`。基线 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`（MING-331 `9ed9c624` 已审）。本岗工作树 `fateradar-multica-ming-341` / `codex/multica-ming-341`，写出仅本文件。未改 `references/annotations/**`、未改 `docs/integration/ming-324-*` / `ming-329-*` / `ming-339-*`、未改 `wuxing-jingji.json`、未合 SDZJ0170。审查岗未参与 MING-339 生产。不是人工 `verified`，不是全库完成，不是产品交付，不合 main。

结论：**通过。** 相对 329 只新增 6 个 `A` 路径（4 份审查稿 + `ming-339-integration-ledger.*`）；无注解 JSON、无 SDZJ0170 注解、无 324 十一文件、无 `wuxing-jingji.json` 变更。四份审查稿 blob 与源 tip 全等，非空。全库校验器 `ok=true`，`verified` true=0。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11）：

```
git fetch origin codex/multica-ming-339 codex/multica-ming-329 \
  codex/multica-ming-312 codex/multica-ming-313 \
  codex/multica-ming-317 codex/multica-ming-335 \
  codex/multica-ming-334 codex/multica-ming-333
git ls-remote origin refs/heads/codex/multica-ming-339 refs/heads/codex/multica-ming-329
git merge-base --is-ancestor 6effd8e4 642dbc46
git diff --name-status 6effd8e4f951fd17e1b1e0454942946ebc765da9 642dbc4683b5e352de45f97265b2794a881be3cb
git log --oneline 6effd8e4..642dbc46
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-339` | `642dbc4683b5e352de45f97265b2794a881be3cb`（`ls-remote` 一致） |
| 已审 329 tip | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（是 339 祖先） |
| 相对 329 文件数 | **6**（全部 `A`，无 `M`/`D`） |
| 注解 JSON 变更 | **无** |
| SDZJ0170 注解 JSON | tip **ABSENT**（与基线相同） |
| `wuxing-jingji.json` | blob `9665e5752e6535a33705f21f3415855f753928a1`（基线 = 329 = 339） |
| 产品路径 / `chart.*` / WebUI | 无 |
| 本岗写出 | 仅本文件 |

相对 329 新增 6 文件：

1. `docs/book-reviews/shenxiang-quanbian-cp1-review.md`
2. `docs/book-reviews/wuxing-jingji-cp1-review.md`
3. `docs/book-reviews/wuxing-jingji-cp3-review.md`
4. `docs/book-reviews/wuxing-jingji-cp7-review.md`
5. `docs/integration/ming-339-integration-ledger.json`
6. `docs/integration/ming-339-integration-ledger.md`

`f86eeec` 之后四笔只改 339 账本：钉 SHA / 远端核验 / 再钉 / 对齐。未再碰审查稿或注解。

324 十一文件 blob 与 `6effd8e4` 全等：

| 324 已交文件 | blob |
|---|---|
| `references/annotations/bazi/sanming-tonghui--shidian-HY1521.json` | `3b98d6441e59f3947d14cc34bc9f1a20709c3db9` |
| `references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json` | `2c028a7c17ebd9e894894206309fd37deca70e8b` |
| `references/annotations/divination/huangji-jingshi--shidian-SK1573.json` | `f13177dc55c0e9bf4f49923bbd594e0c23f70659` |
| `docs/book-reviews/sanming-hy1521-cp7-cp8-review.md` | `92edadb07b3c817564c26e4d4f3505513bc6b165` |
| `docs/book-reviews/sanming-hy1521-progress-2026-09-11.md` | `5d050063e43272d95013959728487630701bfd95` |
| `docs/book-reviews/luoluzi-sanming-sk1605-review.md` | `14d807c5554428c0c134eae8b16fc57162a58d6d` |
| `docs/book-reviews/huangji-jingshi-sk1573-cp1-review.md` | `c74c0cf0c14bb882edfe40bb12e0e2eb212a5468` |
| `docs/book-reviews/huangji-jingshi-sk1573-cp2-review.md` | `d78f5f2775fcc310b2c1f1afc31d96a7e65e32df` |
| `docs/book-reviews/huangji-jingshi-sk1573-progress-2026-09-11.md` | `455c79054d21981eb0790a9a2e2a379b85b7935b` |
| `docs/integration/ming-324-integration-ledger.json` | `9c9ed4ca63cf9070ce7294ecd61c8b948669b742` |
| `docs/integration/ming-324-integration-ledger.md` | `88486e0a31b4f387fe0f5035d7cdf83ed5337874` |

329 四包注解 JSON 与 329 tip 全等：大全 `66db69fd…` / 秘本 `a7b3659f…` / SK1602 `b8853cb4…` / SK1609 `a10d1dc5…`。`ming-329-integration-ledger.json` `ad612252…` / `.md` `c9b91795…` 未改。

329 已带 315/316/318/319 审查稿 blob 未变：神相 CP2 `15789e0e…`、五行 CP2 `74ab2201…`、CP4 `41a66465…`、CP5 `3df0b3e4…`。

SDZJ0170：tip 仅有基线已有的 `sources/normalized/shidianguji/SDZJ0170/*`，**无** `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`。相对 329 无 SDZJ0170 路径。

未抢产品仓：本 diff 无前端 / `chart.*` / tsx。未改并行生产/审查稿。

## 2. 四份审查稿与源 tip 对账

| Pack | 源 SHA | cherry-pick | 路径 | blob（源 = 合入） | 行数 / 字节 | 空文件 |
|---|---|---|---|---|---|---|
| 神相 CP1 MING-312 **done** | `28a23af6ae6a61a9bdd45f409d3fd7aded833ef7` | `3a94c654`（`-x` 自 28a23af6） | `docs/book-reviews/shenxiang-quanbian-cp1-review.md` | `c808ca675b356f0fabb22db69e0999dc83bb15e9` | 176 / 11745 | 否 |
| 五行 CP1 MING-313 **done** | `2eacfd480c47ea08405361a4f0f7de17df60cae3` | `56f0af46`（`-x` 自 2eacfd48） | `docs/book-reviews/wuxing-jingji-cp1-review.md` | `0e6ba50947eb900cf21e243103d6886e01e60c12` | 192 / 12543 | 否 |
| 五行 CP3 MING-317 **done** | `d8e979896522d21450cb419683eb9d1218c8ae01` | `626ee01d`（`-x` 自 d8e97989） | `docs/book-reviews/wuxing-jingji-cp3-review.md` | `545a6efb520c44cbe39c79286fd1b3462eeae88c` | 201 / 14064 | 否 |
| 五行 CP7 MING-335 **done** | `26e22fc681149662c328d7ce45e1ae317eccdb11` | `a0f01b10`（`-x` 自 26e22fc6） | `docs/book-reviews/wuxing-jingji-cp7-review.md` | `455f6823771aff0ff4b4f4a7517bb8e89540c703` | 184 / 13219 | 否 |

四笔源 commit 与 cherry-pick 均只含对应 1 个 `docs/book-reviews/*` 文件。源 tip `ls-remote` 与账本 `sourceSha` 一致。抽核四稿均有「结论：**通过。**」且写明 `source-reviewed` 不是人工 `verified`。合入不是空文件、不是截断、不是另写副本。

## 3. 校验器独立复跑

本岗对 `642dbc46` 树复跑（非 ming-339 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 57 | 41764 | 39395 | `[]` |

与 MING-331 已审全库（files=57 entries=41764 source_reviewed=39395）一致：本批无注解增减。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 4. verified 未越权提升

本岗未改注解。实测全库 57 文件 / 41764 条：`verified=true` **0**。本 diff 不含任何 `references/annotations/*.json`，不可能把条目标成人工 verified。

`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 5. 声称跳过独立核实

| 项 | 339 交包时 | 本岗复核时 | 判定 |
|---|---|---|---|
| MING-334 CP6 | 账本记 `in_review`，tip `9d15790` 仅 `docs/book-reviews/wuxing-jingji-cp6-review.md` | Issue 现 **done**；blob `88743720…` 13277 字节；**未**出现在 339 tip | 交包时跳过成立。现已 done 且审查-only，下一批可只汇该稿。不构成本包失败。 |
| MING-333 SDZJ0170 | 生产中 / 禁止合注解 | Issue 现 **done**；`origin/codex/multica-ming-333` @ `60495cc6` 相对 329 **会删** 324/329 十一文件与四包注解、**会改** `wuxing-jingji.json`、**会新增** `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | 跳过正确。即使现已 done，也不得把该分支叠进本线。 |

## 6. 非阻塞 caveat

1. `ming-339-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` 仍写 `461671398abe8d6e941ca8ee8d8e91b16f786acb`；真实远端 tip 是 `642dbc46`（该 commit 本身把字段从 `dda6d940…` 改到 `46167139…`）。与 MING-331 账本自指滞后同类。不回改 339 账本（非本岗独占文件）。
2. MING-334 现已 done，本 tip 未带 `wuxing-jingji-cp6-review.md`。缺这一份不构成本包失败，下一批可只汇该审查稿。
3. 全库 `files=57` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。

## 7. remaining / 下一步

- 本 Issue（MING-341）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-339：本批审查稿增量成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一批可评估 **MING-334** CP6 审查-only 增量（现 done，单文件 `wuxing-jingji-cp6-review.md`）。
- **仍不合** SDZJ0170 / MING-333 分支：该 tip 会覆盖 `wuxing-jingji.json` 并拆掉 324/329 已审文件。
- 禁止覆盖 `wuxing-jingji.json` / 324 十一文件 / 329 四包注解。
- 禁止把本批算作全书 / 八术 / Web 完成。
