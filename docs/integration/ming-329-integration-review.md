# MING-329 下一批合入独立审查（六壬大全/秘本、SK1602、SK1609）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。权威 `origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。叠在已审 324 tip `9118a78741f7a593105db09c058616cc4e0b7eec` 上。batch2 合入 `968319089be97adec38f726205ad850bfd6060db`。本岗工作树 `fateradar-multica-ming-331` / `codex/multica-ming-331`，写出仅本文件。未改 `references/annotations/**`、未改 324 十一文件、未改账本、未改产品仓。审查岗未参与 MING-329 生产。不是人工 `verified`，不是全库完成，不是产品交付，不合 main。

结论：**通过。** 相对 324 只新增本批 16 个 `A` 路径（4 份注解 JSON + 审查/进度稿 + `ming-329-integration-ledger.*`）；324 十一文件 blob 与 `9118a787` 全等；无 SDZJ0170 注解合入。四包 blob / 源 SHA256 / entries / source_reviewed 与原审查 Issue 一致；`verified` 全 false；draft 保留；未覆盖基线主本；未抢 323/327 产品文件。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11）：

```
git fetch origin codex/multica-ming-329 codex/multica-ming-324 codex/full-library-completion
git ls-remote origin refs/heads/codex/multica-ming-329 refs/heads/codex/multica-ming-324 refs/heads/codex/full-library-completion
git merge-base --is-ancestor 9118a787 6effd8e4
git diff --name-status 9118a78741f7a593105db09c058616cc4e0b7eec 6effd8e4f951fd17e1b1e0454942946ebc765da9
git log --oneline 9118a787..6effd8e4
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（`ls-remote` 一致） |
| 已审 324 tip | `9118a78741f7a593105db09c058616cc4e0b7eec`（是 329 祖先） |
| 基线 `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（是 324 祖先） |
| batch2 合入 | `968319089be97adec38f726205ad850bfd6060db`（单亲，父即 324 tip） |
| 相对 324 文件数 | **16**（全部 `A`，无 `M`/`D`） |
| 注解 JSON 数 | 324 的 53 → tip 57（+4） |
| 产品路径 / `chart.*` / WebUI | 无 |
| 本岗写出 | 仅本文件 |

相对 324 新增 16 文件：

1. `references/annotations/san-shi/daliuren-daquan.json`
2. `references/annotations/san-shi/liuren-miben.json`
3. `references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json`
4. `references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json`
5. `docs/book-reviews/yuzhao-shenying-sk1602-review.md`
6. `docs/book-reviews/yuzhao-shenying-sk1602-progress-2026-09-11.md`
7. `docs/book-reviews/xingxue-dacheng-sk1609-cp2-review.md`
8. `docs/book-reviews/xingxue-dacheng-sk1609-progress-2026-09-11.md`
9. `docs/book-reviews/liuren-multica-remaining-ledger-2026-09-11.json`
10. `docs/book-reviews/liuren-priority-reading-2026-09-10.md`
11. `docs/book-reviews/shenxiang-quanbian-cp2-review.md`
12. `docs/book-reviews/wuxing-jingji-cp2-review.md`
13. `docs/book-reviews/wuxing-jingji-cp4-review.md`
14. `docs/book-reviews/wuxing-jingji-cp5-review.md`
15. `docs/integration/ming-329-integration-ledger.json`
16. `docs/integration/ming-329-integration-ledger.md`

`9683190` 之后两笔只改账本：`87e59dc` 钉 batch2 SHA，`6effd8e` 记远端 tip。未再碰注解。

基线上这四份注解 **ABSENT**；合入是加法，不是整文件覆盖。324 十一文件 blob 与 `9118a787` 全等：

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

基线已有主本 blob 未变：

| 主本 | baseline = 324 = 329 tip |
|---|---|
| `references/annotations/luming-nayin/wuxing-jingji.json` | `9665e5752e6535a33705f21f3415855f753928a1` |
| `references/annotations/luming-nayin/yuzhao-shenying.json` | `bcae48a1a84decfbf685bf334b625771092219ba` |
| `references/annotations/xingming/xingxue-dacheng.json` | `ad59a73379148f9ba45a4634ca4d1d2f1d886d65` |

`references/annotations/xiangfa/shenxiang-quanbian.json` 基线 / 324 / 329 均不存在；本批只汇审查稿，未伪造主本。

SDZJ0170：tip 仅有基线已有的 `sources/normalized/shidianguji/SDZJ0170/*`，**无** `references/annotations/**` 合入。相对 324 无 SDZJ0170 路径。

未抢产品仓：329 在 `fateradar-classics`，相对 324 无前端/`chart.*`/tsx。MING-323 仍 `in_review`（新版联动/导出），MING-327 为产品测试矩阵且已 done；本 diff 未碰 `cosmic-fortune-lab`。未重做 MING-328。

## 2. 与原审查 Issue 对账

| Pack | 源 SHA | 审查 / 收口 | 注解 blob（源 = 合入） | 源 text SHA256 | entries / sr / draft / verified=true |
|---|---|---|---|---|---|
| 六壬大全 | MING-97 `d84e26ba883f31d403eedb4cef8c6ac034f2aeae` | MING-97 协调核验 `01a08f57` + 用户收口 `01a08f5c` WORK_PACKAGE_COMPLETE | `66db69fdf39120e4e37733cb59b5ea01a154dcd9` | `e0c5cd12773bdf00a73cf2ce2e00fc8b0522b55d4855f09c0af290e155904441` | 6893 / 6048 / 845 / 0 |
| 六壬秘本 | 同上 | 同上 | `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f` | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` | 2643 / 2554 / 89 / 0 |
| SK1602 | MING-114 `59de8bf6f5a268ff6525fec570420251769fec08` | MING-124 `562681f0ef25b4a966689cee54bf70d4048626d6` | `b8853cb49b03e217fa7c2c61a392759db08becd6` | `996873796425cdcd58e36c6e5971757e2de572577b5c161c9b3ba8f02e92f8bc` | 13 / 11 / 2 / 0 |
| SK1609 | MING-135 `3b578879499082cc67d9eb12ed7c9efb54515bd1` | MING-150 `8dec744768bfbdac4da95d172071491c3f55fb8d`（CP1 钉 `8def9f05`） | `a10d1dc5d103b1cd9688db563002c504da98393c` | `0d0f3106f2865b4e4b2f10a9c9433785b6009575b53105bbf8718dde48ffa948` | 398 / 396 / 2 / 0 |

注解 content SHA256 与账本一致：大全 `c9321794…` / 秘本 `30b9b2b9…` / SK1602 `622fc897…` / SK1609 `ea891c69…`。四份源文 SHA256 在基线、324、329、源提交上全等。

审查稿 blob 与原提交一致：

- SK1602 审查：`2ec9aaa23999bf11c08a6f5946801d737ef372bd`（MING-124）
- SK1602 进度：`57bfd980e8483d25234ba74dd9d43cca7cea5391`（MING-114）
- SK1609 CP2 审查：`12e1ae1e7e04bfc6a8bc2c31a7994a86655bcb0b`（MING-150）
- SK1609 进度：`3c9d00e9f6da62d58d341d688d0aea6462625644`（MING-135）
- 六壬 remaining 账本 / 优先阅读：与 `d84e26ba` 全等
- 315/316/318/319 审查-only：`shenxiang-quanbian-cp2-review.md` `15789e0e…`、`wuxing-jingji-cp2-review.md` `74ab2201…`、`wuxing-jingji-cp4-review.md` `41a66465…`、`wuxing-jingji-cp5-review.md` `3df0b3e4…`；源提交均只改对应审查稿，未改注解 JSON

SK1609 CP1 `8def9f05` 的 300 条 paragraphId 是 tip 398 条的前缀（`prefix match True`）。CP1 审查稿 `docs/book-reviews/xingxue-dacheng-sk1609-cp1-review.md`（MING-137 `edb422e9`，blob `b5ceae4a…`）本批未带入，见 §7。

六壬没有像 124/150 那样的独立审查 Issue；收口证据是协调者对 `d84e26ba` 的独立复跑（大全 6893 / 秘本 2643、verified 全 false）加用户 `01a08f5c`。本岗复跑与源 blob 全等，不构成盲合。不是人工 verified。

## 3. 校验器独立复跑

本岗对 `6effd8e4` 树复跑（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations <pack> --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|
| 六壬大全 | true | 1 | 6893 | 6048 | `[]` |
| 六壬秘本 | true | 1 | 2643 | 2554 | `[]` |
| SK1602 | true | 1 | 13 | 11 | `[]` |
| SK1609 | true | 1 | 398 | 396 | `[]` |
| 全库 | true | 57 | 41764 | 39395 | `[]` |

与 MING-324 已审全库（files=53 entries=31817 source_reviewed=30386）相加：`31817+6893+2643+13+398=41764`，`30386+6048+2554+11+396=39395`。与 329 交包及账本 `validateAnnotationsFull` 一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 4. verified / draft / unknown 未越权提升

本岗未改注解。实测：

- 四包 `verified=true` 均为 0；大全 6893、秘本 2643、SK1602 13、SK1609 398 条 `verified=false`。
- SK1602 `review=draft` 仍仅两处（与 MING-124 一致）：`yuzhao-shenying:shidian-SK1602:P7639282082212053002`、`P7639282082213412874`（无字，保持 draft）。
- SK1609 `review=draft` 仍仅：`xingxue-dacheng:shidian-SK1609:P7430056317387145267`、`P7640428574264541234`（无可转存 / 缺文标记）。
- 大全 draft 845、秘本 draft 89 仍在；`review=unknown` 本批为 0。kind=待核实未抬升。

`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 5. paragraphId

- 四包内部重复：0
- 四包交叉重复：0
- 与库内其他注解 JSON 交叉重复：0

未发现合入造成的 ID 串包。

## 6. 315/316/318/319 仅审查稿

本 diff 含四份已 done 审查稿，均只新增 `docs/book-reviews/*`，未改 `wuxing-jingji.json` / 神相注解 JSON。符合 329「可选带入、不改五行精纪/神相注解」与 328「下一批可只汇已审审查稿、不得覆盖基线主本」。

## 7. 非阻塞 caveat

1. `ming-329-integration-ledger.json` 的 `integrationBranchTipAtDelivery` 仍写 `87e59dc1…`；真实远端 tip 是 `6effd8e4`（只补了一行核验说明）。`candidateIntegrationSha` / `batch2MergeSha` 仍正确钉在 `9683190`。不回改账本。
2. SK1609 CP1 审查稿 `xingxue-dacheng-sk1609-cp1-review.md`（MING-137 `edb422e9`）未随批合入；CP2 审查稿与累计 398 条注解已在。独立审查稿缺这一份不构成本包失败，下一批可只汇该审查稿。
3. 六壬收口走 MING-97 协调核验 + 用户 WORK_PACKAGE_COMPLETE，不是单独审查 Issue。本岗已按独立审查标准复跑，blob/计数一致。
4. 全库 `files=57` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。

## 8. remaining / 下一步

- 本 Issue（MING-331）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-329：本批合入成立，同样有限 `done`；不升产品唯一线、不合 main。
- 禁止重做 324/328；禁止覆盖 `wuxing-jingji.json` / 玉照主本 / 星学主本。
- SDZJ0170 仍排除（tip blob 可能缺 CP2），不得盲合。
- 禁止把本批算作全书/八术/Web 完成。
