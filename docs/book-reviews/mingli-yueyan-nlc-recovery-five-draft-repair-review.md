# 命理约言 · NLC 恢复本：独立审查五段 draft→SR 修复（MING-442）

审查对象：[MING-439](mention://issue/01a091bb-b3eb-76a6-8d7a-96a18df7d7b5) `origin/codex/multica-ming-439` @ `e4870ee31d5ad59834d94cd749b00be447549897`。基线 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-442` / 分支 `codex/multica-ming-442`。本岗未参与 MING-439 修复生产；未改注解 JSON、未改 439 修复稿、未改 CP1–CP3 审查稿；不抢 424/431。只核这五段，不扩成全书重审。不是命理约言全书完成，也不是人工 `verified`。

结论：**通过。** `diff 329..439` 仅 2 路径；JSON 内容级仅 5 条 `paragraphId` 变更；五段 vernacular/notes 对照 `nlc-recovery.md` 与 `page-reviews.json` 成立，已清除 draft 空模板；`validate-annotations` `ok=true errors=[]`、`source_reviewed=619`、`verified` 全 false（781 条均无 `verified` 键）；其余 776 条与 329 全等。`source-reviewed` ≠ 人工 `verified`。

## 1. 指针与越权

独立命令（本岗树，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-439
git rev-parse origin/codex/multica-ming-329 origin/codex/multica-ming-439
git diff --name-only origin/codex/multica-ming-329..origin/codex/multica-ming-439
git diff --stat origin/codex/multica-ming-329..origin/codex/multica-ming-439
shasum -a 256 references/annotations/bazi/mingli-yueyan--nlc-recovery.json
git show origin/codex/multica-ming-329:references/annotations/bazi/mingli-yueyan--nlc-recovery.json | shasum -a 256
shasum -a 256 sources/normalized/bazi/mingli-yueyan/nlc-recovery.md
shasum -a 256 sources/normalized/bazi/mingli-yueyan/page-reviews.json
```

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-439`（`ls-remote`） | `e4870ee31d5ad59834d94cd749b00be447549897` |
| 基线 `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 相对 329 文件 | 仅 2：`references/annotations/bazi/mingli-yueyan--nlc-recovery.json`、`docs/book-reviews/mingli-yueyan-nlc-recovery-five-draft-repair.md` |
| diffstat | 注解 `+34/-30` + 修复稿 `+69` |
| 439 注解 SHA256 | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928`（与 Issue 一致） |
| 329 注解 SHA256 | `d23db1d8e2df46c63224e573b0a1466a9632bff71cbf13324f8053058f5a0be6`（与 Issue 一致） |
| `nlc-recovery.md` SHA256 | `7bd1425da62c9ca202e251ad4e06182c2c84e56818802b43be946bcf3a5e9b25`（本包未改） |
| `page-reviews.json` SHA256 | `1dd1444e1ae5568fdfb80a1e92585dc01789c923e3ff0c860d26d55fbae0bdbc`（本包未改） |
| JSON 内容级变更 | 仅下列 5 条；其余 **776** 条与 329 字节级全等 |
| 同页正文 L005 | `P024/P029/P037:L005-L005` 与 329 全等，仍为 source-reviewed |

本审查写出仅本文件。未改 JSON / 源 / page-reviews / fulltext / 主本 / 439 修复稿 / CP1–CP3。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/mingli-yueyan--nlc-recovery.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 781, "source_reviewed": 619,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

| 状态 | entries | source-reviewed | draft | verified 键 / true |
|---|---|---|---|---|
| 329 基线 | 781 | 614 | 167 | 0 / 0 |
| 439 对象 | 781 | 619 | 162 | 0 / 0 |

与交包自称及 Issue 钉死 SR=619 一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. 五段语义对照（对照原文，非转引修复稿）

原文取 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 页头元数据，并交叉 `page-reviews.json`。基线五条均为模板句「本段为恢复稿PDF第…页的校核状态、版心或定位信息…」+ `review=draft`；修复后模板已清除。

| # | paragraphId（索引） | 源页要点 | 修复后 vernacular 要点 | 判定 |
|---|---|---|---|---|
| 1 | `P024:L002-L003`（idx 83） | L447–450：全页对图+跨页衔接；版心「精選命理約言 卷一 法」；印刷页码七。page-reviews：主体 L5 已核 | 页码七、卷一法、跨页；声明非命理正文 | 通过 |
| 2 | `P029:L002-L003`（idx 97） | L494–497：主体对图；版心卷一法；页码一二；不释读黑底。正文含分日/三六五与三七二矛盾 | 页码一二、黑底不作字；分日论推同页正文；非藏干分日理论 | 通过 |
| 3 | `P037:L002-L003`（idx 131） | L632–635：主体对图；页码二〇；黑底排版标记不作字。正文含官/从官条件 | 页码二〇、版面标记；声明非看官法正文 | 通过 |
| 4 | `P083:L002-L002`（idx 258） | L1073–1079：卷末装饰页；卷名卷一法；页码六六。page-reviews `reviewedRanges=[]` | 装饰结页、六六；不补造正文 | 通过 |
| 5 | `P163:L002-L002`（idx **695**） | L2258–2264：卷三卷末；卷名卷三論；页码五二。page-reviews 无正文规则 | 卷三结页、五二；不补造正文 | 通过 |

五条 `kind` 均为「评注或元数据」；notes 均声明 source-reviewed ≠ 人工 verified / 不混入规则或断语。无空 vernacular、无「白话从略 / TODO」类空模板。

## 4. verified / 范围未越权

- 781 条均无 `verified` 键；无升 verified。
- 仅上述五段 `draft→source-reviewed`；其余 162 draft 未动。
- 未改 `nlc-recovery.md` / `page-reviews.json` / `fulltext.md` / 主本 `mingli-yueyan.json`。
- 未碰 424/431 独占范围；未重写 CP1–CP3。

## 5. source-reviewed ≠ 人工 verified

本审查只确认：相对 329 的五段元数据回改对照恢复稿成立，且 validator / 计数 / 范围与 Issue 钉死一致。不是人工影印终审，不是预测验证，不抬升全书 `canonical_eligible`，不代表命理约言 NLC 恢复本全书完成。

## 未决（本岗不施工）

- 其余 162 draft（多为 cover/layout 模板）保持 draft。
- 全书人工 verified / 正式升格不在本包。

## 判定摘要

| 检查项 | 结果 |
|---|---|
| diff 仅 2 路径 | 通过 |
| JSON 仅五段 | 通过 |
| 五段非空模板、对照源成立 | 通过 |
| validator ok；errors=[]；SR=619 | 通过 |
| verified 全 false | 通过 |
| 失败 paragraphId | 无 |
