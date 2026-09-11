# 命理约言 · NLC 恢复本：MING-129/139 五段 draft 模板回改修复（MING-439）

基线：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-439` / 分支 `codex/multica-ming-439`。本岗未参与这五段原生产；不重做 CP1–CP3 审查稿；不抢 424/431。不是全书完成，也不是人工 `verified`。

结论：**已修复。** 权威树相对 `be137a1` 回改的五段 draft 模板，已按 NLC 恢复稿与 `page-reviews.json` 恢复为页特异 vernacular/notes（及对应 terms），`review` 回 `source-reviewed`。其余 776 条未改；同页 `L005` 正文 SR 未改；781 条均无 `verified` 键。

## 1. 指针与范围

| 项 | 实测 |
|---|---|
| 基线 HEAD | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 修复前注解 SHA256 | `d23db1d8e2df46c63224e573b0a1466a9632bff71cbf13324f8053058f5a0be6`（与 Issue / MING-423 一致） |
| 修复后注解 SHA256 | `09cdbccf314e365dc4a416aec31f1d5c336fd56a93520b86282e423c0faa3928` |
| 源 `nlc-recovery.md` SHA256 | `7bd1425da62c9ca202e251ad4e06182c2c84e56818802b43be946bcf3a5e9b25`（未改） |
| `page-reviews.json` SHA256 | `1dd1444e1ae5568fdfb80a1e92585dc01789c923e3ff0c860d26d55fbae0bdbc`（未改） |
| 对照原生产 | `be137a1`（MING-129）；独立审查 `e93febb`（MING-139） |
| 写出文件 | 仅 `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`（五段）+ 本报告 |

## 2. 校验器

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

| 状态 | entries | source-reviewed | draft | verified=true |
|---|---|---|---|---|
| 修复前（权威树） | 781 | 614 | 167 | 0 |
| 修复后 | 781 | 619 | 162 | 0 |

与 `be137a1` 账本一致（619/162）。内容级 diff 仅上述 5 条 paragraphId。

## 3. 五段修复明细（对照恢复稿）

模板句「本段为恢复稿PDF第…页的校核状态、版心或定位信息…」已从这五条清除。白话按页审/源页头重写，不吞同页理论正文。

| # | paragraphId | 源要点 | 修复后要点 | review |
|---|---|---|---|---|
| 1 | `P024:L002-L003` | L2 全页对图+跨页衔接；L3 卷一法、印刷页码七 | 页码七、卷一法、跨页；声明非命理正文 | draft→source-reviewed |
| 2 | `P029:L002-L003` | L2 主体对图；L3 卷一法、页码一二；不释读黑底 | 页码一二、黑底不作字；分日论推给同页 L5 | draft→source-reviewed |
| 3 | `P037:L002-L003` | L2 主体对图；L3 卷一法、页码二〇；黑底不作字 | 页码二〇、版面标记；声明非看官法正文 | draft→source-reviewed |
| 4 | `P083:L002-L002` | 卷末装饰页；卷名卷一法；印刷页码六六 | 装饰结页、六六；`reviewedRanges=[]`；不补造正文 | draft→source-reviewed |
| 5 | `P163:L002-L002` | 卷三卷末；卷名卷三论；印刷页码五二 | 卷三结页、五二；不补造正文 | draft→source-reviewed |

同页正文 `P024/P029/P037:L005-L005` 仍为既有 source-reviewed，本包未改。`P083/P163` 的 `L004`/`L006` 卷名与页码条亦未改。

## 4. 未越权

- 其余 776 条 annotation 字节级未动（含其余 template draft）。
- 未改 `nlc-recovery.md` / `page-reviews.json` / `fulltext.md` / 主本 `mingli-yueyan.json`。
- 未设任何 `verified`；未升其余 draft。
- 未重写 CP1–CP3 审查稿；未碰 424/431 独占范围。

## 5. source-reviewed ≠ 人工 verified

本修复只恢复对照恢复稿成立的页特异元数据注解，并回补 MING-423 质量账本所记 SR 619→614 回归。不是人工影印终审，不是预测验证，不抬升全书 `canonical_eligible`。

## 未决（本岗不施工）

- 其余 162 draft（多为 `partial` 页模板）保持 draft。
- 独立语义复审可由协调另派；本包以源/页审对照 + validator 为交包证据。
