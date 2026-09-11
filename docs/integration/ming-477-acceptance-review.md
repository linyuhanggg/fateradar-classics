# MING-477 叠 464 合入本轮已审审查稿独立验收

审查对象：`origin/codex/multica-ming-477` **远端 tip** `b19190593107fa2337bdeef565fa7cba57d52562`（不是仅内容 SHA）。基线 `origin/codex/multica-ming-464` @ `538fd1422053e449c9543b33c6a7c7ce5cbc0108`（独立验收 [MING-469](mention://issue/01a091e7-f2bb-79c5-b4da-55e68142c828) `91b1264ccd551b32c711391f665472c21a11c6ed` 通过）。内容合入 tip `2314c3b4672849d57ee4d1031f0ef20334cd8401`，其后四笔只动 477 账本。本岗工作树 `fateradar-multica-ming-485` / `codex/multica-ming-485`，写出仅本文件。未改注解 JSON、未改 477 已合入审查稿/账本、未升产品唯一线 `6c1dfa3b`。本岗未参与 [MING-477](mention://issue/01a091f6-4803-77f5-b021-150d6452cd30) 合入。不要重跑已通过的 424/431/447/454/464/469。不要另开第二路集成写入。不要抢 [MING-482](mention://issue/01a091f9-4a23-7568-bbc7-0c91381714a2)。不是人工 `verified`，不是古籍/八术全书完成，不是产品交付，不合 main。

结论：**通过。** 相对 464 仅 **12** 路径（10 审查/验收 md `A` + 本批 ledger `A`×2）；`references/annotations/**` **0** diff；注解 **58/58 blob 与 464 全等**；10 份合入路径 blob 与各自源 tip / 账本 / 合入 commit **全等**；464 相对 447 的 17 路径 blob **未覆盖**；未合入 452/468 产品定义 ID，未合 478–481 独占审查稿；全库校验器 `ok=true`，`errors=[]`；全库 `verified=true` **0**。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗稀疏树，复用 `/Users/sync/code/fateradar-classics` 对象，未复制 `sources/` / PDF / `node_modules`，2026-09-11T19:48Z）：

```
git ls-remote origin \
  refs/heads/codex/multica-ming-477 \
  refs/heads/codex/multica-ming-464 \
  refs/heads/codex/multica-ming-469 \
  refs/heads/codex/multica-ming-461 \
  refs/heads/codex/multica-ming-462 \
  refs/heads/codex/multica-ming-463 \
  refs/heads/codex/multica-ming-465 \
  refs/heads/codex/multica-ming-466 \
  refs/heads/codex/multica-ming-467 \
  refs/heads/codex/multica-ming-472 \
  refs/heads/codex/multica-ming-473 \
  refs/heads/codex/multica-ming-474 \
  refs/heads/codex/multica-ming-478 \
  refs/heads/codex/multica-ming-479 \
  refs/heads/codex/multica-ming-480 \
  refs/heads/codex/multica-ming-481
git merge-base --is-ancestor 538fd1422053e449c9543b33c6a7c7ce5cbc0108 b19190593107fa2337bdeef565fa7cba57d52562
git merge-base --is-ancestor 2314c3b4672849d57ee4d1031f0ef20334cd8401 b19190593107fa2337bdeef565fa7cba57d52562
git diff --name-status 538fd1422053e449c9543b33c6a7c7ce5cbc0108 b19190593107fa2337bdeef565fa7cba57d52562
git diff --name-status 538fd1422053e449c9543b33c6a7c7ce5cbc0108 b19190593107fa2337bdeef565fa7cba57d52562 -- 'references/annotations/**'
git log --oneline 538fd1422053e449c9543b33c6a7c7ce5cbc0108..b19190593107fa2337bdeef565fa7cba57d52562
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-477` | `b19190593107fa2337bdeef565fa7cba57d52562`（`ls-remote` 一致；验收对象是远端 tip） |
| 已审 464 tip | `538fd1422053e449c9543b33c6a7c7ce5cbc0108`（是 477 祖先，`merge-base --is-ancestor` 退出 0） |
| 已审 469 验收 | `91b1264ccd551b32c711391f665472c21a11c6ed`（本批合入其验收稿 blob；**不是** 477 的 git 祖先） |
| 内容合入 tip | `2314c3b4672849d57ee4d1031f0ef20334cd8401`（是 b191905 祖先） |
| 相对 464 文件数 | **12**（12×`A`，无 `M`/`D`，无未声明路径） |
| `references/annotations/**` diff | **空** |
| 注解文件数 464 = 477 | **58**；blob **58/58 全等** |
| 命理约言 NLC SHA256 | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`（= 464） |
| 识典 SDZJ0170 blob | `1f369f996da7ea96c6e4bd3388510af24e8d1ea7`（464 = 477） |
| 大六壬 blob | `66db69fdf39120e4e37733cb59b5ea01a154dcd9`（464 = 477） |
| 飞星原旨 blob | `9f713a371b7059b2986321c12933a2ceb96c5766`（464 = 477） |
| 皇极 SK1573 blob | `f13177dc55c0e9bf4f49923bbd594e0c23f70659`（464 = 477） |
| 秘本 blob | `c9940ca0125443608cc5487e15d8174427d36fc7`（464 = 477） |
| 星學主本 blob | `ad59a73379148f9ba45a4634ca4d1d2f1d886d65`（464 = 477） |
| 奇门 NLC layouts blob | `a7a4c66578d108cf44a1ab70b3fd161ca6ff54e4`（464 = 477） |
| 产品路径 / `chart.*` / `definition-id` / WebUI | 无（diff 不含；树内无 definition-id 路径） |
| 产品唯一线 `6c1dfa3b` | 本仓 **无此 git 对象**；diff 仅账本政策文字 |
| 478–481 独占路径 | 与本批 12 文件交集 **空**；四条均不是 477 祖先 |
| 本岗写出 | 仅本文件 |

相对 464 变更 12 文件（均在声明审查稿/账本路径内）：

1. `A` `docs/book-reviews/bushi-zhengzong-independent-review.md`
2. `A` `docs/book-reviews/lantai-miaoxuan-independent-review.md`
3. `A` `docs/book-reviews/li-xuzhong-mingshu-independent-review.md`
4. `A` `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-remaining-2100-2470-review.md`
5. `A` `docs/book-reviews/qimen-dunjia-tongzhi-yanyi-vol4-9-independent-review.md`
6. `A` `docs/book-reviews/qingnang-xu-independent-review.md`
7. `A` `docs/book-reviews/shenfeng-tongkao-independent-review.md`
8. `A` `docs/book-reviews/taiwei-fu-independent-review.md`
9. `A` `docs/book-reviews/yangzhai-shishu-independent-review.md`
10. `A` `docs/integration/ming-464-acceptance-review.md`
11. `A` `docs/integration/ming-477-integration-ledger.json`
12. `A` `docs/integration/ming-477-integration-ledger.md`

`git log --oneline 538fd14..b191905` 十四笔：十份 `cherry-pick -x`（内容合入 tip `2314c3b`）→ `96bf844` 账本 → 三笔账本 record/pin/align（`63ecf0b` / `04789b7` / `b191905`）。未整树迁入。未抢产品唯一线。未改 424/431/447/454/464/469 已审树。`git diff --stat 538fd14..b191905`：12 files, +1850 / −0。

## 2. SHA 与 464 对照

| 路径 | SHA256 | 相对 464 |
|---|---|---|
| `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` | `d65d93d8f579d2cf181a27d4af707d20d2bac276b785eb4b8c6442fd2982a261` | 全等 |
| `references/annotations/san-shi/daliuren-daquan.json` | `c9321794bbea0e9df31069bdbf146ec18b61529fb85b9d34729c19ca3d74059a` | 全等 |
| `references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json` | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95` | 全等 |
| `references/annotations/divination/huangji-jingshi--shidian-SK1573.json` | `05a054d299a123ed20d5c6edaf3a921f0eb3e9fe13a2d9854ecd6ce82effb513` | 全等 |
| `references/annotations/san-shi/liuren-miben.json` | `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347` | 全等 |
| `references/annotations/xingming/xingxue-dacheng.json` | `11316f4428dd25142e7cbfba26c8eb5e17ef9ff10d0033655dbe33335e92dd20` | 全等 |
| `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` | `86eb7aa43138fe67d1247a5e520411cfb26f71beb9a220a3cd28d6dcb87bf5ca` | 全等 |
| `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928` | 全等 |
| 其余 50 个注解 JSON | （未列） | 全等 |

全库 58 文件逐文件 blob：equal 58 / changed 0。约言 NLC / 秘本 / 识典 / 大六壬 / 飞星 / 皇极 / 星學 / 奇门 NLC 与 464 及既有钉死值一致。`tools/validate-annotations.py`、`tools/source_paragraphs.py`、`references/source-editions.json`、`references/inventory/**`、`sources/**` 相对 464 **0** diff。

## 3. 合入源 tip 对账

`ls-remote` 十个源 tip 与 Issue 指定及 477 账本 `sourceSha` **全等**。十笔内容提交均 `cherry-pick -x`，blob 源 = 合入 = 账本；无一空文件、无一截断、无另写副本。464 相对 447 的 17 路径在 477 **blob 全等**（无较旧整文件覆盖）。

| Pack | 源 tip | 合入 | 路径 | blob（源 = 合入 = 账本） | 行 / 字节 | 空 | 源稿结论 |
|---|---|---|---|---|---|---|---|
| 464 验收 MING-469 | `91b1264ccd551b32c711391f665472c21a11c6ed` | `9eaa90e` | `docs/integration/ming-464-acceptance-review.md` | `8cf1d858fdff5c775dd93265ae2cb42226399775` | 187 / 17012 | 否 | 通过 |
| 奇门 NLC remaining 2100–2470 MING-461 | `402393affff7175ed2ed7afee2fc47fc03503a89` | `e9466b9` | `docs/book-reviews/qimen-dunjia-tongzhi-nlc-layouts-remaining-2100-2470-review.md` | `03adcd4ebd918f3bbbaecfc203d40ab3ff765daa` | 157 / 12347 | 否 | 通过 |
| 奇门演義 vol4–9 MING-462 | `e92efab9a3f97ab2faf0316aed79f08134714b83` | `0194126` | `docs/book-reviews/qimen-dunjia-tongzhi-yanyi-vol4-9-independent-review.md` | `101e3955959c984c317a100ae176f733b8a6a255` | 162 / 11814 | 否 | 通过 |
| 神峰通考 MING-463 | `80a1734b8be003ff450527c84615450c245db953` | `4def1e9` | `docs/book-reviews/shenfeng-tongkao-independent-review.md` | `67e00b6bdee8eabdd6326b85ac2fc29f109b2e04` | 158 / 12070 | 否 | 通过 |
| 阳宅十书 MING-465 | `c2cf06a70149d84a78f5d3ad32be81c4ee09542c` | `c3ac2fd` | `docs/book-reviews/yangzhai-shishu-independent-review.md` | `e732e565f017a1a302aea8d54a058f83e6198419` | 141 / 10539 | 否 | 通过（有限范围） |
| 青囊序 MING-466 | `54c7d0a58f4fa25c71e09a8d4b4336900731f7d1` | `cfb4d65` | `docs/book-reviews/qingnang-xu-independent-review.md` | `46ad2801bc8629ea53c48c617fb346b89a2b9bf0` | 140 / 10173 | 否 | 通过（有限范围） |
| 卜筮正宗 MING-467 | `bfeb02dfc15855d5d89e1dd4d749cf7331fb74e0` | `1d7e60c` | `docs/book-reviews/bushi-zhengzong-independent-review.md` | `9c0157061cd94cb46a3d3e406bdf0e64a1310a4c` | 187 / 12427 | 否 | 通过 |
| 兰台妙选 MING-472 | `2d608eba47dbf152422c68ab4c7dcf02c5886ceb` | `c868160` | `docs/book-reviews/lantai-miaoxuan-independent-review.md` | `4e9efa057acb62c1b7989ed7b4ed2310e3460936` | 151 / 11379 | 否 | 通过 |
| 李虚中命书 MING-473 | `5a8c5daf467b76f343c069a9e2af888d6e0250fd` | `fce2158` | `docs/book-reviews/li-xuzhong-mingshu-independent-review.md` | `dc9bd0bb1ff7982713c1d3f10ccf7ace8394c97c` | 150 / 12226 | 否 | 通过 |
| 太微赋 MING-474 | `98b4573eb69f1282b29c9d841bf26fa96eccb0a4` | `2314c3b` | `docs/book-reviews/taiwei-fu-independent-review.md` | `537ac99d6ba96d4c5a8650d5beec5c2670e32ddc` | 149 / 10405 | 否 | 通过 |

源稿均写明通过（或有限范围），且 `source-reviewed` ≠ 人工 `verified`。本岗核合入 blob 全等与注解范围，不重做 424/431/447/454/464/469 或各审查包语义。

## 4. 未合入 452/468 / 478–481

- 古籍仓 **无** `codex/multica-ming-452` / `codex/multica-ming-468`；477 树无 `definition-id` / `chart.*` / 账号 / 支付 / 后端路径。
- `origin/codex/multica-ming-478` `25bfe8c0`、`479` `6596a106`、`480` `a054e819`、`481` `d226ec75` **都不是** 477 祖先，477 也不是它们的祖先。相对 464 的 12 路径与其独占审查稿交集为空。
- 其独占审查稿在 477 **均不存在**：`yangzhai-sanyao-independent-review.md`（478）、`dili-bianzheng-independent-review.md`（479）、`bingjian-independent-review.md`（480）、`yuzhao-shenying-independent-review.md`（481）。
- 本岗不审这些包，也不把「当时未完成」写成「永远不合」。

## 5. 校验器独立复跑

注解 / inventory / `source-editions.json` / `tools/validate-annotations.py` / `sources/**` 相对 464 均为 0 diff。本岗稀疏树未检出 `sources/`（约 1.2G 全文，按磁盘控制复用已冻结对象）。在 **已冻结** `fateradar-multica-ming-477` @ `b1919059`（`git status --porcelain` 空、HEAD 与 `ls-remote` 一致）只读复跑，`PYTHONDONTWRITEBYTECODE=1`，未写该树：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | books | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|---|
| 全库 | true | 48 | 58 | 42834 | 40410 | `[]` |

相对已审 464：文件数 / entries / `source_reviewed` **不变**（注解 0 diff 的必然结果）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。各审查包语义抽样已由对应审查 Issue 完成。

## 6. verified 未越权提升

本岗未改注解。实测全库 58 文件 / 42834 条：`verified=true` **0**。其中显式 `false` 24904、缺键 17930。约言 781 条全部缺 `verified` 键。秘本 / 识典 / 大六壬 / 飞星 / 皇极 / 星學 / 奇门 NLC 目标文件均无 `verified=true`。`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 7. 非阻塞 caveat

1. `ming-477-integration-ledger.json` 的 `candidateIntegrationSha` / `integrationBranchTipAtDelivery` / `remoteSha` 仍写 `04789b7d734c041bee57029b82193910bde884bd`；真实远端 tip 是 `b1919059`（其后一笔 `b191905` 只修账本 tip 行，未把上述三字段改到自身）。账本 `note` 已声明以 `ls-remote` 为准。与 MING-464 账本自指滞后同类。不回改 477 账本（非本岗独占文件）。
2. 内容合入 tip `2314c3b` 与本审查对账一致；其后四笔只动 ledger。不影响合入正确性。
3. `91b1264`（469 分支 tip）**不是** 477 的 git 祖先，因为验收稿是 `cherry-pick -x` 为 `9eaa90e`。blob 已与源 tip 全等。
4. `6c1dfa3b` 仅作为「禁止升产品唯一线」政策文字出现在账本，本仓无此 commit 对象，不构成升线。diff 不含产品路径。
5. 478–481 现 tip 在 477 交包后可能已完成，但其独占文件未进本 tip；本岗不审这些包。
6. 全库 `files=58` / `source_reviewed=40410` 只是本集成线上的注解文件数，不是全书 / 奇门 NLC / 风水诸书 / 禄命完成，更不是产品交付。
7. 禁止把本批算作升产品唯一线 `6c1dfa3b` 的依据。
8. 校验器因稀疏检出缺补充全文，改在已冻结 477 树只读复跑；输入 blob 与 464 全等，结果与 469 验收口径一致。不把 477 施工树当写出目标。

## 8. remaining / 下一步

- 本 Issue（MING-485）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-477：本批叠 464 合入 469 验收稿与 461–463/465–467/472–474 审查稿成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一集成候选由协调另派（478–481 仅在其独立审查通过后）。勿再开第二路集成写入抢 477 树。勿抢 MING-482 磁盘回收。
- 禁止把本批算作全书 / 八术 / Web 完成。
- 禁止本岗改合入内容；失败路径已无，无需返工 477。
- 勿重跑 424/431/447/454/464/469；勿升产品唯一线 `6c1dfa3b`。
