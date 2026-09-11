# MING-324 首批合入独立审查（HY1521 / SK1605 / SK1573）

审查对象：`origin/codex/multica-ming-324` @ `9118a78741f7a593105db09c058616cc4e0b7eec`。基线 `origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。batch1 合入 `de2105601a59f5afa18b63cc16dc4e5b7cb57fff`。本岗工作树 `fateradar-multica-ming-328` / `codex/multica-ming-328`，写出仅本文件。未改 `references/annotations/**`、未改已合入审查稿、未改账本、未改产品仓。审查岗未参与 MING-324 生产。不是人工 `verified`，不是全库完成，不是产品交付，不合 main。

结论：**通过。** 相对权威只新增声称的 11 文件；三包 blob / 源 SHA256 / entries / source_reviewed 与原审查 Issue 一致；`verified` 全 false；draft / 待核实保留；未覆盖基线主本；未抢 320/322 产品文件。`source-reviewed` 不是人工 `verified`。下列 caveat 不构成本包失败。

## 1. 指针与越权

独立命令（本岗树，2026-09-11）：

```
git fetch origin codex/multica-ming-324 codex/full-library-completion
git ls-remote origin refs/heads/codex/multica-ming-324 refs/heads/codex/full-library-completion
git diff --name-status bc798566da77c30e149abf9673c88ecc386702b2 9118a78741f7a593105db09c058616cc4e0b7eec
git log --oneline bc798566..9118a787
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-324` | `9118a78741f7a593105db09c058616cc4e0b7eec`（`ls-remote` 一致） |
| 基线 `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2` |
| batch1 merge | `de2105601a59f5afa18b63cc16dc4e5b7cb57fff`（父即基线） |
| 相对基线文件数 | **11**（全部 `A`，无 `M`/`D`） |
| 注解 JSON 数 | 基线 50 → tip 53（+3 识典包） |
| 产品路径 / `chart.*` / WebUI | 无 |
| 本岗写出 | 仅本文件 |

相对基线 11 文件：

1. `references/annotations/bazi/sanming-tonghui--shidian-HY1521.json`
2. `references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json`
3. `references/annotations/divination/huangji-jingshi--shidian-SK1573.json`
4. `docs/book-reviews/sanming-hy1521-cp7-cp8-review.md`
5. `docs/book-reviews/sanming-hy1521-progress-2026-09-11.md`
6. `docs/book-reviews/luoluzi-sanming-sk1605-review.md`
7. `docs/book-reviews/huangji-jingshi-sk1573-cp1-review.md`
8. `docs/book-reviews/huangji-jingshi-sk1573-cp2-review.md`
9. `docs/book-reviews/huangji-jingshi-sk1573-progress-2026-09-11.md`
10. `docs/integration/ming-324-integration-ledger.json`
11. `docs/integration/ming-324-integration-ledger.md`

`9118a787` 之后四笔只改账本 JSON/MD 的 tip 记录（`a3091be` / `206734d` / `1552362` / `9118a78`），未再碰注解。

基线上这三份识典注解 **ABSENT**；合入是加法，不是整文件覆盖。基线已有主本 blob 未变：

| 主本 | baseline blob | tip blob |
|---|---|---|
| `references/annotations/luming-nayin/wuxing-jingji.json` | `9665e5752e6535a33705f21f3415855f753928a1` | 同 |
| `references/annotations/bazi/sanming-tonghui.json` | `453b20ac9d2c35ca926bd4902522b6175c17eeb6` | 同 |
| `references/annotations/luming-nayin/luoluzi-sanming.json` | `468ec8fe3f7c88ad521cedef2f68a824fbecf275` | 同 |

`huangji-jingshi.json` / `huangji-jingshi--shidian-DZ1040.json` 基线与 tip 均不存在，本批未伪造主本。

未抢产品仓：`9118a787` 不在 `cosmic-fortune-lab` 缓存；本 diff 无前端/chart 路径。MING-320 仍 `in_review`、MING-325 仍 `in_progress`，本批未碰。

## 2. 与原审查 Issue 对账

| Pack | 源 SHA | 审查 SHA | 注解 blob（源 = 合入） | 源 text.md SHA256 | entries / sr / draft / verified=true |
|---|---|---|---|---|---|
| HY1521 | MING-98 `9e2f2f2df140d72244a47fa2dc93b8b7f8069499` | MING-130 `71a417553831c1ef9c746668b07cde0170205886` | `3b98d6441e59f3947d14cc34bc9f1a20709c3db9` | `707ac9bc6796bdb679833fc280040485d95b36da6f7aca0b3e2adbb9e57d19d3` | 2340 / 2338 / 2 / 0 |
| SK1605 | MING-102 `5f9a25a1ceddad888e3656022038af24c746cc11` | MING-107 `8fa7dedd394228f13c2e4f95dcd8e9d74661d579` | `2c028a7c17ebd9e894894206309fd37deca70e8b` | `a5b639ad155b4de2b12ac23a8e37028c46d07923bc5a16a4f406eed8855b97c8` | 16 / 15 / 1 / 0 |
| SK1573 | MING-168 `a4c1eda8d1a0d21564c4f8bc8967eba5b46f72f5` | MING-174 `e3336c0133dd7b9c01ea74812a4512dc70f28779` + CP1 MING-163 `005690c76f90796ae0cad9ba8de2250c64909b43` | `f13177dc55c0e9bf4f49923bbd594e0c23f70659` | `c101c5a29e96da89e45fdb3b01c879308c74767d1071531e202706c50791e34a` | 670 / 670 / 0 / 0 |

注解 content SHA256 与账本一致：HY1521 `82ff378a…` / SK1605 `3db6dca0…` / SK1573 `05a054d2…`。

审查稿 blob 与原审查提交一致：

- HY1521 CP7–CP8：`92edadb07b3c817564c26e4d4f3505513bc6b165`
- SK1605：`14d807c5554428c0c134eae8b16fc57162a58d6d`
- SK1573 CP1：`c74c0cf0c14bb882edfe40bb12e0e2eb212a5468`
- SK1573 CP2：`d78f5f2775fcc310b2c1f1afc31d96a7e65e32df`

进度稿：HY1521 / SK1573 与源提交 blob 一致。SK1605 源提交另有 `docs/book-reviews/luoluzi-sanming-progress-2026-09-11.md`，本批未带入；独立审查稿已在，不构成本包失败，下一批可只汇该进度稿。

## 3. 校验器独立复跑

本岗对 `9118a787` 树复跑（非 ming-324 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations <pack> --json
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --json
```

| 范围 | ok | files | entries | source_reviewed | errors |
|---|---|---|---|---|---|
| HY1521 | true | 1 | 2340 | 2338 | `[]` |
| SK1605 | true | 1 | 16 | 15 | `[]` |
| SK1573 | true | 1 | 670 | 670 | `[]` |
| 全库 | true | 53 | 31817 | 30386 | `[]` |

与 MING-324 交包及账本 `validateAnnotationsFull` 一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 4. verified / draft / unknown 未越权提升

本岗未改注解。实测：

- 三包 `verified=true` 均为 0；HY1521 2340、SK1605 16、SK1573 670 条 `verified=false`。
- HY1521 `review=draft` 仍仅两处（与 MING-130 一致）：`sanming-tonghui:shidian-HY1521:P7467786007220338740`、`P7458198190622310419`。
- SK1605 `review=draft` 仍仅 `luoluzi-sanming:shidian-SK1605:P7640185840559439882`。
- SK1573 无 draft；待核实 kind 仍为索引 26 `P7637910921877143603`、38 `P7637910921877340211`、516 `P7637911011882680347`（与 MING-163 / MING-174 一致，未补造）。

`source-reviewed ≠ 人工 verified`。电子阅读不是影印校勘。

## 5. paragraphId

- 三包内部重复：0
- 三包交叉重复：0
- 与库内其他注解 JSON 交叉重复：0

未发现合入造成的 ID 串包。

## 6. 315/316/318/319 当时未合入

本 diff 无神相全编 CP2、无五行精纪主本改动、无 315/316/318/319 审查稿。账本把它们列为 `pendingIndependentReview` / `in_review` 是合入当时的正确冻结。现看板：MING-315/316/318/319 均为 `done`。下一批可只汇已审审查稿，且不得覆盖较新的基线 `wuxing-jingji.json`（本批已遵守）。

## 7. 非阻塞 caveat

1. `ming-324-integration-ledger.md`「远端核验」仍写 tip `1552362ff3…`；真实远端 tip 是 `9118a787`（只补了一行核验说明）。账本 JSON 的 `candidateIntegrationSha` / `batch1MergeSha` 仍正确钉在 `de21056`。不回改账本。
2. SK1605 进度稿未随批合入，见 §2。
3. 全库 `files=53` 只是本集成线上的注解文件数，不是 55 套资料包完成，更不是产品交付。

## 8. remaining / 下一步

- 本 Issue（MING-328）：审查结论通过，交协调核对后 `done`（有限范围）。
- MING-324：本批合入成立，同样有限 `done`；不升产品唯一线、不合 main。
- 下一批已开 MING-329（六壬大全/秘本、SK1602、SK1609）；本岗不重开同包。
- 315/316/318/319 审查稿可作后续「只汇审查稿」候选，禁止覆盖基线主本。
- 禁止把本批算作全书/八术/Web 完成。
