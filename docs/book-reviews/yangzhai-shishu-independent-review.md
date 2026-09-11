# 阳宅十书：独立审查主本 source-reviewed 全量（文件索引 0–8）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-465` / 分支 `codex/multica-ming-465`。本岗写出仅本文件。未改注解 JSON、未改源文、未抢 MING-458–464 文件、未改他书 / 引擎 / 产品仓。本岗未参与该书生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。不与《阳宅三要》混淆。本包只审注解文件索引 0–8（9 条，全量）。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；9/9 `source-reviewed`、0 draft；9/9 显式 `verified: false`，无一 `verified=true`；inventory 与注解 `paragraphId` 一一对应且同序；全书 9 段均对照原文语义成立（4 个理论主段的 subsection 连续覆盖父段行号、无空白白话）。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-465`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/yangzhai-shishu.json
git rev-parse HEAD:references/annotations/fengshui/yangzhai-shishu.json
ls sources/fulltext/fengshui/yangzhai-shishu/fulltext.md
shasum -a 256 sources/fulltext/fengshui/yangzhai-shishu/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `21238e12e1540192735402044d11b47bd78d47fb5f8b2813df34ebad4b22ab1a`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `443cd31afc975969b027cdcc830310fce671fba9` |
| 源路径 | `sources/fulltext/fengshui/yangzhai-shishu/fulltext.md`（存在） |
| 源 `fulltext.md` SHA256 | `5b1e6fbcf3c50d5f6e115e2b1d713a0aa4259cf6a0abc2485972b90195b90355` |
| 源行数 | 3051 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文无 diff |

无越权文件。注解未改。源文未改。未写产品仓。未触 `yangzhai-sanyao.json`。生产侧 `yangzhai-shishu.json` 最后触及提交为 `9118a78`（MING-324 记录），本岗未参与该书生产。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/yangzhai-shishu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 9, "source_reviewed": 9,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–8，9 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 9/9 |
| `review=draft` | 0 |
| `verified=true` | 0 |
| `verified=false` | **9/9 显式布尔 false**（与 Issue「verified 全 false」一致） |
| 空白白话 | 0 |
| 白话全文重复组 | 0 |
| `notes=[]` | 5（均为短元数据段 0/1/3/5/7；理论主段均有 notes） |
| 空 `terms` | 9/9（父段与 subsection 均 `terms=[]`；不构成本包失败，亦不据此升 verified） |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `sourceAttribution` | 0 |
| `relatedParagraphIds` | 0 |
| `subsections` | 4 个理论主段：66 + 49 + 62 + 23 = 200 节；行号连续覆盖父段、无重叠、无空白 vern |

kind 分布：评注或元数据 5、理论 4。inventory 9 段均为 `待分类` / `unclassified`；注解 kind 为注解侧分类，与 inventory 初筛不一致，**不回改 inventory**，不构成本包失败。

**scopeNote 陈旧（不失败）：** 文件顶层 `scopeNote` 仍写「第677卷…父段 draft，L2072起未读」。独立读 entries：索引 6（`L1865-L2605`）已是完整 `source-reviewed` 且 `verified: false`，62 节连续覆盖至卷末。以 entries 的 `review`/`verified` 为准；本岗不回改 scopeNote。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/yangzhai-shishu.json` 9 段；注解 9 条。`paragraphId`/`id` 全部命中，`missing=0`，顺序一致。起 `yangzhai-shishu:L0001-L0006`、止 `yangzhai-shishu:L2611-L3051`，与 Issue 钉死一致。

| 索引 | 实测 ID | 注解 kind | 说明 |
|---|---|---|---|
| 0 | `yangzhai-shishu:L0001-L0006` | 评注或元数据 | YAML 头：艺术典 675–678 / 符镇图锚 |
| 1 | `yangzhai-shishu:L0010-L0010` | 评注或元数据 | 第 675 卷 Wikisource URL |
| 2 | `yangzhai-shishu:L0012-L1213` | 理论 | 《阳宅十书一》；66 节 |
| 3 | `yangzhai-shishu:L1217-L1217` | 评注或元数据 | 第 676 卷 URL |
| 4 | `yangzhai-shishu:L1219-L1859` | 理论 | 《阳宅十书二》；49 节 |
| 5 | `yangzhai-shishu:L1863-L1863` | 评注或元数据 | 第 677 卷 URL |
| 6 | `yangzhai-shishu:L1865-L2605` | 理论 | 《阳宅十书三》；62 节 |
| 7 | `yangzhai-shishu:L2609-L2609` | 评注或元数据 | 第 678 卷 URL |
| 8 | `yangzhai-shishu:L2611-L3051` | 理论 | 《阳宅十书四》符镇；23 节 |

源文分卷结构：艺术典第 675–678 卷四收录分卷对应十论实际篇次，不是「只含原书前四论」。本包后该书 SR 审查 remaining **0**。

## 5. 全核语义（9/9，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/yangzhai-shishu/fulltext.md` 的行范围。全书仅 9 父段；4 个理论主段按 subsection 标题与行号对读，并抽核关键数值/歌诀/卷末。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0001-L0006` | 评注或元数据 / SR | YAML：`藝術典第675-678卷`、`陽宅十書一至四`、符镇图锚不转写符形；白话作版本范围说明，不作全帙影印证明 | 通过 |
| 1 | `L0010-L0010` | 评注或元数据 / SR | 单行 Source URL 指向艺术典第 675 卷；白话要求按此版本追溯 | 通过 |
| 2 | `L0012-L1213` | 理论 / SR | 卷目外形/福元；外形图说多处 `[圖]`；福元=福德宫/伏位；三元九宫男逆女顺、中五男坤女艮；上/中/下元甲子表各 60 组独立复算与原文一致；`己末`（L968）疑 `己未` 已记；宅元≠婚元（婚元上男七女五等）；东四/西四门房井灶用例与游年简称一致；西四图仅占位收尾。66 节连续 L12–1213 | 通过 |
| 3 | `L1217-L1217` | 评注或元数据 / SR | 第 676 卷 URL；白话强调不可沿 675 卷重排行号 | 通过 |
| 4 | `L1219-L1859` | 理论 / SR | 大游年歌乾六天五…兑生祸延绝与首卷口诀同层；三吉/凶星五列+辅弼；十二宅图 L1268/L1284 为 `{{{2}}}` 缺题；乾门图说坎六煞/艮天乙/震五鬼等与原文一致；穿宫层进与元空装卦（非玄空飞星）；门尺前八后八寸名目与 L1845–1859 一致。49 节连续 | 通过 |
| 5 | `L1863-L1863` | 评注或元数据 / SR | 第 677 卷 URL；第三收录分卷 | 通过 |
| 6 | `L1865-L2605` | 理论 / SR | 放水九星来去、净阴阳分组、黄泉煞四句、24 山放水定局 24 条「X山水宜放」齐全；火唵八宫灶方与火路歌异文及原注质疑离乙；命前五神起法与丙辛巳命例内部不合已保留；生命表/月表差异与太阴太阳图旁录边界写明；`docs/review/yangzhai-vol677-images-2026-09-09/` 存在。62 节连续；父段图占位计数 46 与白话「46既有图」一致 | 通过 |
| 7 | `L2609-L2609` | 评注或元数据 / SR | 第 678 卷 URL；符镇第十与编后问答 | 通过 |
| 8 | `L2611-L3051` | 理论 / SR | 符镇宗旨与黄石公归属说；五岳/十二支/三教八方等题名错接旁注边界；卷末「王子既輯…不可執定宅術」与 L3043–3051 一致。23 节连续。正文 `[圖]` 137 处；图审 manifest 写明「137占位=136符图+1字形图」，与白话「136个既有图」口径一致；`docs/review/yangzhai-vol678-images-2026-09-09/manifest.json` 存在 | 通过 |

### 独立数值抽核（不替代人工 verified）

- **福德宫三元表（L846–1033）：** 上元男起坎逆 / 女起中寄艮顺、中元男巽女坤、下元男兑女艮；各 60 干支组解析后与算法复算 **0 mismatch**；中元 `己末` 按 `己未` 年序理解后仍一致。
- **婚元口诀（L1034–1038）：** 「上元男七女五…下元男四女五…五位男坤女艮」与注解「婚元≠宅元、下元女五不改八」一致。
- **大游年歌（L1238–1245）：** 与注解所引乾/坎/艮/震/巽/离/坤/兑简称序列一致。
- **24 山放水（L1976–2008）：** 解析得 24 条「山水宜放」，含坤/申分列。
- **卷末问答（L3043–3051）：** 命运天时 / 地利一半 / 修德积恶 / 不可执定宅术，与注解限制语一致。

抽核未发现空模板白话、把图书集成「一至四」误读成原书仅四论、把游年九星套成紫微星盘、把元空装卦改称玄空飞星、把符镇写成已验证工程方案、或把任何条 `verified` 置 true。未与 `yangzhai-sanyao` 混书。

分类可争但不失败：父段 `terms` 全空、inventory 仍待分类、顶层 scopeNote 落后于 entries——均记录为 caveat，本岗不回改注解。

## 6. 明确非结论

- 本包 **不** 证明影印/符式逐笔已校或传统断语经验证。
- 本包 **不** 把任何条升为人工 `verified`。
- 本包 **不** 表示风水材料已接入 FateRadar 八术页面。
- 本包 **不** 覆盖或取代生产侧图审旁录目录；仅确认其路径存在且与注解 notes 引用一致。
- 图形占位、缺题模板、生命/月表内部差异、太阴太阳旁录 draft、符式未逐笔释读等，均保持注解已写边界；不据电子文本改字或补图。

## 7. 交付

| 项 | 值 |
|---|---|
| Issue | MING-465 |
| 工作树 | `fateradar-multica-ming-465` |
| 分支 | `codex/multica-ming-465` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/yangzhai-shishu-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后可将本 Issue `done`；无需重做 0–8；无需回改注解。
