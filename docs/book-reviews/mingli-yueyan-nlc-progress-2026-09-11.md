# 命理约言 · NLC 恢复本语义审读进度 · 2026-09-11

独占文件：`references/annotations/bazi/mingli-yueyan--nlc-recovery.json` 与本进度文档。只读 corpus-2 源树；未改 `nlc-recovery.md` / `page-reviews.json`、旧导航 `mingli-yueyan.json`、HY1521、SK1605、SK1602、`geju-transit*`、引擎或 chart。

## WORK_PACKAGE_COMPLETE

本包剩余 5 段（page-reviewed 源状态、注解原为模板 draft）一次做完：全部升为 `source-reviewed`，白话按页审与版心实写，禁止模板套话；`verified` 未设（保持非人工 verified）。剩余 ID：无。不是全书完成，也不是人工盖章。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-129`
- 分支：`codex/multica-ming-129`（基线继承 `codex/grok-fast-corpus-2-20260910` @ `c86a06e`）
- `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` SHA256 = `7bd1425da62c9ca202e251ad4e06182c2c84e56818802b43be946bcf3a5e9b25`（与 Issue 一致）
- 本包 5 段源层均为 `page-reviewed`，故可写注解 `source-reviewed`；其余仍为 `ocr-draft` 的版面 draft 未触碰（校验器禁止 OCR draft 上挂 source-reviewed）
- source-reviewed = AI 按恢复稿与 page-reviews 语义处理，≠ 人工 verified / 预测效果

## 段落账本（5/5）

| # | paragraphId | kind | review | 去向摘要 |
|---|---|---|---|---|
| 1 | `…:P024:L002-L003` | 评注或元数据 | source-reviewed | 卷一法页审+版心页码七；跨页衔接元数据 |
| 2 | `…:P029:L002-L003` | 评注或元数据 | source-reviewed | 卷一法页审+版心页码一二；分日论另段 |
| 3 | `…:P037:L002-L003` | 评注或元数据 | source-reviewed | 卷一法页审+页码二〇；黑底标记不作字 |
| 4 | `…:P083:L002-L002` | 评注或元数据 | source-reviewed | 卷一结页装饰；卷名+六六，无正文规则 |
| 5 | `…:P163:L002-L002` | 评注或元数据 | source-reviewed | 卷三结页；卷名+五二，无正文规则 |

起讫（Issue 书签）：`mingli-yueyan:nlc-recovery:P024:L002-L003`–`mingli-yueyan:nlc-recovery:P163:L002-L002`（中间仅此 5 条为 page-reviewed×draft 可升级项）。

## 计数变化

| 项 | 本包前 | 本包后 |
|---|---|---|
| entries | 781 | 781 |
| source-reviewed | 614 | 619 |
| draft | 167 | 162 |

162 draft 仍为封面缺字/馆藏条码/ocr-draft 版面状态等，本包不升格、不 OCR、不补造缺章。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/mingli-yueyan--nlc-recovery.json --json
```

预期：`ok=true`，`errors=[]`，`entries=781`，`source_reviewed=619`。校验器只做结构与 ID，不是语义证书。

## 边界

不 main 合并/部署/force push；不改源文与 page-reviews。下一 ID：无（本包收束）。全书其余 ocr-draft 元数据若需升格，须先改源层 page-reviews，另开包。
