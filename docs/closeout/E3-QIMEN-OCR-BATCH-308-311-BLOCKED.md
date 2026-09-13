# E3 · 《奇門遁甲統宗》PDF 308–311 页 OCR 转写——**阻塞批次（未完成）**

> **2026-09-14：本文件不再代表现状。** 四页已转写，并已按列左断语／跨页最右续文修订。见 `E3-QIMEN-OCR-BATCH-308-311.md` 与 `nlc-layouts.md` PDF第308–311页。以下为 2026-09-13 读图授权阻塞时的历史登记，勿当完成门槛。

日期：2026-09-13　执行：classics-audit（团队任务 t2）
状态：**转写未完成，原因＝视觉能力待用户授权（modlens reuse 门）。**

> **一句话结论：影印页可用、取向与版面已实测，但本成员在本会话读不到图，因此 308–311 的逐格转写一字未写。**
> 本文件只登记**可复核的非视觉产物**，不冒充已核：本批**未新增 page-review 记录、未提升任何注解条目、
> 未改 `nlc-layouts.md`、未改 `nlc-layout-page-reviews.json`、未改 `source-manifest.yaml`**。
> `canonical_eligible` 与 `verified` 全部保持 `false`。

---

## 0. 为什么停在这里（环境事实，非能力缺陷）

- `read_image`（modlens 视觉桥）两次调用均失败，错误原文：
  `Error: claude-cli provider failed with code 1. Hint: this machine has vision reachable through codex,
  which modlens is not yet allowed to reuse. Ask the user, then: modlens config set reuse.<harness> true.`
- 队长（captain）独立复测，得到**完全相同的错误**——这是全局能力门，不是本批专有问题。
- modlens 的 engines／reuse grants／guard rules 在 `~/.modlens/config.json`，与所有 harness 共享；
  本机**无 modlens 可执行**（`npx` 拉包失败，离线），该开关只能由 harness／用户侧执行。
- 本机确有可用视觉 CLI（`codex` 已登录、`codex exec -i <png>` 支持贴图），但**未经用户明示同意不得复用**。
- 按团队纪律：**不用 OCR 引擎（tesseract／macOS Vision）与电子本代填，不凭相邻页补字，不把未读页写成已核。**
  故本批以「阻塞」收口，而不是交一份看起来完整、实际未读图的转写。

**已完成的非视觉工作**（下图 1–5 节）全部可复现；**未完成的是唯一的实质步骤：读图取字。**

---

## 1. 影印可用性与上批停在哪里

| 项 | 值 |
|---|---|
| 影印 | `sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf`（408 页，sha256 `08b041e0863c2c81ae8be525f68288a81e54fe9b17186716ebe707bb345a0da6`） |
| 渲染命令 | `pdftoppm -r 400 -f 308 -l 311 -png <pdf> /tmp/ca/qm/render400/pg` |
| 渲染产物 | `/tmp/ca/qm/render400/pg-308.png`（556,254 B）· `pg-309.png`（485,817 B）· `pg-310.png`（545,637 B）· `pg-311.png`（336,915 B） |
| 本区卷次 | 四页版心均为**卷九**；据 `ocr-batch-0300-0311.md` 的登记，300 起为「陰七局」区（局式圆图＋逐时表） |
| **上批停在哪** | `ocr-batch-0300-0311.md` 把 300–311 登记为 **B 级版面事实**，并在 `doubt_308`–`doubt_311` 写明「**未逐格转写**」；`ocr-batch-cell-level-0283-0324.md` §5b 只做到 **284–291**（其标题虽写「284–291、303–311」，正文只有 284–291）；`ocr-batch-cell-level-314-0324.md` 覆盖 314–324。**故 308–311 至今没有任何单元格级转写**——这正是 t2 要补的洞 |

---

## 2. 取向与门槛实测（四页 UPRIGHT）

400dpi 原页、墨迹阈值 `gray < 140`、自相关取 λ∈[15,420] 且 `acf>0.08` 的局部极大：

| 页 | 文字块（宽×高 px） | X 基频（列距） | Y 基频（字距） | 判定 |
|---|---|---:|---:|---|
| 308 | 1430 × 1813 | **227** | **67** | UPRIGHT（正立竖排） |
| 309 | 1446 × 1669 | **227** | **68** | UPRIGHT |
| 310 | 1428 × 1830 | **225** | **67** | UPRIGHT |
| 311 | 1460 × 1589 | **228** | **67** | UPRIGHT |

与既有 t14 登记的 `Xcol≈225–230／Ychar≈67` **独立吻合**。判据：竖排汉文的列距落在 X、字距落在 Y，
且列距显著大于字距 → 页面正立；本批四页全部正立，**不需要任何旋转派生图**。

**一次自我更正（保留过程，避免后续误用）**：我的第一版测量脚本把自相关上限设成 `maxlag=200`，
而列距 227 **超出该窗口**，于是最强的 227 峰被截掉，脚本据此把四页误判为 `SIDEWAYS`。
把窗口放宽到 420 后，X 峰 227（acf 0.599 等）重新成为首峰，判定改为 UPRIGHT。
**教训**：测量窗口必须覆盖待测周期，否则「测不到」会被写成「不存在」。
（同一轮里我还试过按墨迹带合并列：`merge_gap=26` 时列被并成一条，说明参数必须报出来；
最终列带参数见 §3。）

---

## 3. 版面结构与逐页列带（crop 规划用）

**结构（ASCII 墨迹密度图 + 投影实测）**：四页均为**逐时表**——页首一行小题块，
主体是**自右向左若干竖排列**（每列＝一个大字行头 ＋ 其下小字断语的窄带对），右缘另有版心／小条。
以 308 为例：页首块 y≈583–742；主体 y≈795–2120；右缘小条 y≈2173–2226。

**列带实测（400dpi 像素坐标；列投影 > 0.25×max、runs ≥ 15px、间隙 ≤ 120px 合并）**：

| 页 | 列带（自左向右，x 区间） | 组间距（px） |
|---|---|---|
| 308 | (308,404) (535,631) (761,858) (989,1086) (1232,1259) (1444,1539) (1700,1727) | 227 · 226 · 228 · 243 · 212 · 256 |
| 309 | (348,375) (536,631) (765,860) (1100,1198) (1328,1424) (1556,1650) | 188 · 229 · 335 · 228 · 228 |
| 310 | (447,543) (675,770) (900,991) (1124,1218) (1347,1441) (1579,1669) | 228 · 225 · 224 · 223 · 232 |
| 311 | (307,346) (965,1058) (1204,1300) (1430,1527) (1664,1753) | 658 · 239 · 226 · 234 |

- 主间距集中在 **223–228px**，与 X 基频 227 一致；309／311 出现的 335／658 是**该行墨迹稀疏导致漏检**的合并带，
  不是「列不存在」——**本表只作裁切规划，不作内容判定**。
- 每列内部还量到 **两族窄带（间距≈50–52px）**（大字行头与断语带），这是后续逐格裁切要分开处理的原因。
- 311 文字块明显偏矮（1460×1589），与「本区末页、余文不足」相符；**成因本批不判定**。

原始数字另存为可复核产物：`docs/closeout/evidence/qimen-308-311-geometry-20260913.json`
（含渲染文件与字节数、方法参数、四页峰位与列带）。

---

## 4. 「进入正式数据」到底是哪几步（管线核实结论）

读 `tools/source_paragraphs.py` + `references/source-editions.json` 实测所得（**本批未改这些文件**）：

1. `nlc-layouts.md` 是影印层的**正式登记**：`## PDF第NNN页` 分节 → `split_edition()` 生成 `pageScoped`
   段落（ID 形如 `qimen-dunjia-tongzhi:nlc-layouts:P308:L007-L009`），并给出页内相对行号
   （标题行记为 0，其后按页内相对行号）。
2. `nlc-layout-page-reviews.json` 的 `reviewedRanges`（页内相对 `startLine`/`endLine`）决定该段落能否升级：
   - 整页 `status: source-reviewed` 且 `unresolved` 为空 → `page-reviewed`；
   - 否则命中 reviewedRange 的**正文块** → `passage-reviewed`；
   - 其余（含 `> doubt_*`／`> page_type:` 这类元数据块）保持 `ocr-draft`。
3. `annotations` 侧闸门：`validate-annotations.py` 只比较 `source_status`——源为 `ocr-draft` 时，
   注解**不得**标 `source-reviewed`。故「转写＋page-review」是注解可引用性的前提。
4. `source-manifest.yaml` 的 `paper_layout_recovery` 计数是汇总元数据；
   `canonical_eligible`／`verified` 在本轮保持 `false`。

**干跑验证（合成根，正反例都跑通）**：
- 正例：页分节内的正文块被 reviewedRange 覆盖 → `passage-reviewed`（实测 6 个正文块升级，
  3 个元数据块仍 `ocr-draft`）；
- 反例：reviewedRange 落在元数据块上时，正文块**不升级**（说明范围必须落在真正读过的正文行上）。
- 落库脚本（会话内 `/tmp/ca/land_qm_pages.py`）按上述规则生成分节与 reviewedRanges，
  并用真实加载器回归验证；**因为读不到图，本批没有对主库执行它**。

结论：**只要拿到字形，落库是一步到位的机械动作**（分节 → reviewedRanges → 加载器复核 → 测试）。

---

## 5. 电子本对照：一条关键负面结论

- 主电子本 `sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md` 共 **2,036 行**（题《奇门遁甲统宗大全》，
  卷之十至十二为玄机赋，卷四至九以「奇门演义」网页层补入）。
- 全文逐字检索：「卷九」**0**、「陰七局／阴七局」**0**、「上元七局」**0**、「總表／总表」**0**（「七局」5 处、「符使」7 处）。
- 故 **308–311 的局式逐时表在电子本中没有对应段落**——这批页面属**影印独有证据**，
  「先看电子本填空」在本区**没有对象**，转写只能是读图。这也意味着：本区不存在「电子段可校」的替代路径。

---

## 6. 授权到位后如何继续（交接清单）

1. 渲染与裁切：`pdftoppm -r 400`（或 900dpi 逐格）→ 按 §3 列带逐列裁切，**原生正立、不旋转**。
2. 读数标准沿用 `ocr-batch-cell-level-0283-0324.md` §3：行标先、断语后；符号五级
   （可读／`〔?〕`／`〔A／B〕`／`〔■〕`／不写即未读）。
3. 疑字**精确登记**格式：`自右向左第 n 列 · 列内自上而下第 m 字 · 现象 · 处理`，逐条进 `> doubt_30X:`。
4. 落库：分节写进 `nlc-layouts.md` ＋ page record 进 `nlc-layout-page-reviews.json`（reviewedRanges 只覆盖真读过的正文块）。
5. 复核：`tools/source_paragraphs.py` 加载器复核 + `tools/validate-annotations.py` + 相关测试。
6. 未做即不写：未读格不列、不补、不类推；`verified` 不提升。

---

## 7. 边界（明确声明）

- 本文件**不含任何转写结论**；§2／§3 只有像素测量与版面事实。
- **未使用** tesseract、macOS Vision、第二见证、电子本填空；**未**据相邻页或句式补字。
- **未改** `nlc-layouts.md`、`nlc-layout-page-reviews.json`、`collation-notes.md`、`source-manifest.yaml`、`references/**`。
- 本批的页面级状态**仍是未核**：`ocr-batch-0300-0311.md` 的 B 级登记与 `doubt_308`–`doubt_311` 继续有效。
