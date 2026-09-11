# 命理约言 · NLC 恢复本：独立审查（MING-129 五段语义）

审查对象：`origin/codex/multica-ming-129` @ `be137a187193ecb8c2ee3998a5f5f442804934da`（父 `c86a06e`，corpus-2 基线）。工作树只读参考 `fateradar-multica-ming-129`，本岗写出仅本文件。未改注解 JSON、未改 `nlc-recovery.md` / `page-reviews.json`、未改旧导航 `mingli-yueyan.json`、未改 HY1521 / SK1605 / SK1602 / `geju-transit*` / 引擎 / chart。不是全书完成，也不是人工 `verified`。

结论：**通过。** 交包结构账本与这 5 段对照恢复稿成立；`source-reviewed` 不是人工 `verified`；图文对照不是人工影印终审。下列 caveat 不构成本包失败，也不把其余 162 draft 升格。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-139`，2026-09-11）：

```
git fetch origin codex/multica-ming-129
git rev-parse origin/codex/multica-ming-129
git diff be137a1^..be137a1 --name-only
shasum -a 256 sources/normalized/bazi/mingli-yueyan/nlc-recovery.md
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-129` | `be137a187193ecb8c2ee3998a5f5f442804934da` |
| 相对父提交文件 | 仅 2 个：`references/annotations/bazi/mingli-yueyan--nlc-recovery.json`、`docs/book-reviews/mingli-yueyan-nlc-progress-2026-09-11.md` |
| 注解条目变化 | 仅下列 5 条 `draft`→`source-reviewed`；ID 未增删（781=781） |
| 源 `nlc-recovery.md` SHA256 | `7bd1425da62c9ca202e251ad4e06182c2c84e56818802b43be946bcf3a5e9b25`（与父提交相同） |
| `page-reviews.json` | 本提交未改 |
| 全书 `verified` 键 | 781 条均无该字段；`true` 计数 0 |

无越权文件。源层未改。

## 2. 校验器独立复跑

在本岗从 `be137a1` 检出的独立副本上（非 ming-129 活树）：

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

父提交：`entries=781`，`source-reviewed=614`，`draft=167`。本提交：`619 / 162`。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

781 条均无 `verified=true`。本包只把 5 条模板 draft 升为 `source-reviewed`：

| # | paragraphId | 父 review | 本 review |
|---|---|---|---|
| 1 | `mingli-yueyan:nlc-recovery:P024:L002-L003` | draft | source-reviewed |
| 2 | `mingli-yueyan:nlc-recovery:P029:L002-L003` | draft | source-reviewed |
| 3 | `mingli-yueyan:nlc-recovery:P037:L002-L003` | draft | source-reviewed |
| 4 | `mingli-yueyan:nlc-recovery:P083:L002-L002` | draft | source-reviewed |
| 5 | `mingli-yueyan:nlc-recovery:P163:L002-L002` | draft | source-reviewed |

这 5 条 **不在** 剩余 162 draft 里。剩余 162：`评注或元数据` 161 + `待核实` 1（封面缺字 `P001:L005-L005`）。其中 161 落在 page-reviews 状态 `partial` 的页，1 条为稿首 `P000`。157 条仍以「本段为恢复稿PDF第…页的校核状态、版心或定位信息…」起句。本包未升格它们。

## 4. 本包不是 162 封面/版面 draft 包

page-reviews 文件层：`verified=false`，`defaultStatus=ocr-draft`，185 页中 `source-reviewed=27`、`partial=158`。本包 5 页均在这 27 页内，不是 `partial`/`ocr-draft` 封面包。

父提交这 5 条白话是同一套模板（只换页码）。本提交换成页审实写。模板句在这 5 条中已不存在。

## 5. 五段对照恢复稿（不凭进度摘要）

原文取 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 该页相对行（`## PDF第N页` 为 0）。页审取 `page-reviews.json` 对应 `pdfPage`。未发现「本段论述 / 见原文 / 白话从略」类空模板；无把同页理论/规则正文写进这 5 条 vernacular。

| # | ID | 源行（相对） | 源层要点 | 白话是否页特异 | 判定 |
|---|---|---|---|---|---|
| 1 | `P024:L002-L003` | L2 `page_review`：全页正文、版心与页码已对图，正文跨页保留衔接；L3 `running_title`：精選命理約言 卷一 法，印刷页码七 | 页审 status=`source-reviewed`；notes 记「非诚/损伤」「而竟/有成」跨页。同页 L5 为格局/暗神理论，另条 `P024:L005-L005` | 写明页码七、卷一法、跨页衔接；声明不是命理正文 | 通过 |
| 2 | `P029:L002-L003` | L2 主体已对图、范围见 page-reviews；L3 卷一 法，印刷页码一二 | 页审 scope 明确「不释读黑底项目符号」。同页 L5 批旧例分日与三百六十五／三百七十二，另条 `P029:L005-L005` | 写明页码一二、黑底不作字；notes 把分日论推给另段 | 通过 |
| 3 | `P037:L002-L003` | L2 主体逐字对图，版面项目标记不作正文；L3 卷一 法，印刷页码二〇 | 页审：「标题前黑底排版标记不作为字句」。同页 L5 为看官法（官多食伤仍不作杀、从官≠从杀），另条 `P037:L005-L005` | 写明页码二〇、黑底不作字；声明不是看官法正文 | 通过 |
| 4 | `P083:L002-L002` | L2「图像对照补录：本页为卷末装饰页。」；L4 精選命理約言 卷一 法；L6 六六 | 页审 `reviewedRanges=[]`；notes：只有卷名、法、页码六六及装饰，无正文规则 | 写明卷一结页、装饰、六六；不补造正文。卷名/六六另有 `L004`/`L006` | 通过 |
| 5 | `P163:L002-L002` | L2「图像对照补录：本页为卷末页。」；L4 精選命理約言 卷三 論；L6 五二 | 页审 notes：只有卷名、论与页码五二，无正文规则 | 写明卷三结页、论、五二；不作杂论/附录。卷名/五二另有 `L004`/`L006` | 通过 |

同页正文抽核（证明元数据没有吞规则）：

- P024 L5：得时得局杀伤可富贵、失时失局官印可贫贱；暗神助格破格；不必胶执取格；从化欲生扶其所从所化；欲清不欲混、欲虚不欲实。在 `P024:L005-L005`（理论 / source-reviewed），不在本包元数据条。
- P029 L5：藏气「但有其气，非能分诸支之位」；亥有戊、寅申有己被驳；四时三百六十五 vs 每支三十一日共三百七十二。在 `P029:L005-L005`。本包 notes 指向该段，未把「各干分日万不可拘」写成元数据规则。
- P037 L5：官多须食伤「然不作杀论」；从官与从杀同法但分名；张神峰年时虚官可用被驳为偏僻。在 `P037:L005-L005`（规则候选）。本包 notes 指向该段，未混入。

## 6. source-reviewed ≠ 人工 verified

这 5 条 `source-reviewed` 只表示：对照恢复稿页头元数据与 page-reviews 写了页特异去向，并与同页正文分层。不是人工盖章、不是版本学终审、不是预测有效证据。`page-reviews.json` 顶层 `verified` 仍为 false。不得把 619 条 source-reviewed 写成已人工 verified，也不得把韦选四卷写成陈氏原十卷完成。

## Caveat（不改注解，留给后续 pack）

1. **用词**：交包写「源层 page-reviewed」。`page-reviews.json` 这 5 页的 `status` 实际是 `source-reviewed`（27/185），没有名为 `page-reviewed` 的枚举。与「158 页 partial + default ocr-draft」相对，不构成失败。
2. **P083/P163 L002** 白话概括了同页 L4/L6 已单独著录的卷名与印刷页码。L002 源行本身只写「卷末（装饰）页」。这是页级去向说明，不是模板，也没有引入规则；不据此判失败。
3. **其余 162 draft**：多数仍是模板句，且所在页 page-reviews 为 `partial`（不是这 27 页）。升格须先动源层 page-reviews，属另包。本审查不把它们算进本包通过范围。
4. **进度摘要略缩**：进度表把五段写成「卷一法页审+版心页码」。以注解正文与恢复稿为准。

## 未决（本岗不施工）

- 162 draft（封面缺字、馆藏条码、`partial` 页版面状态）保持 draft。
- 全书 `canonical_eligible` 仍 false；引用资格继续按 page-reviews 逐段范围，不整本抬升。
- 不把任何条目标成人工 verified。
- 不 OCR、不补造缺章、不改注解。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-139`。
