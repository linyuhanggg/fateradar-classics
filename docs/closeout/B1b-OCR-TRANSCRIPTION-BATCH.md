# B1b · OCR 转写复核批次（闸门机制核查 + 批次执行结果）

日期：2026-09-12
分支：`dsh/full-library-classics`
范围：`sources/normalized/**`、`references/annotations/**`、本报告
结果：**复核影印页 0 页，提升 0 条**。原因见 §3（本会话模型无图像输入能力），
并有一个比闸门本身更重要的结构发现见 §2：**这 1,423 条“被打回”的条目里，只有 1 条是古籍正文，其余 1,422 条是恢复稿自己的著录元数据。**

---

## 0. 一句话结论

`OCR draft requires transcription review` 这道闸门**拦的不是知识，是台账**：
被拦的 1,423 条注解，其源段落 `kind` 全部是 `评注或元数据`——即恢复稿写给自己的
`> page_review:` / `> running_title:` / `> printed_entry:` / `> excerpt_scope:` 定位与状态行。
**库里没有任何一条待提升的实质论述（理论/规则候选/案例/操作步骤/术语）被这道闸门挡住。**
其中唯一一条源段落属实质文本（`待分类`）的，是约言封面缺字的题名行，其自身注记就写着
“源层 ocr-draft 且缺字，保持 draft”。

因此本轮**提升 0 条是正确结果，不是失败**；而“1,423 条 OCR 积压待清”这一表述本身需要修正。

---

## 1. 闸门机制（逐行核实，非推测）

### 1.1 报错点

`tools/validate-annotations.py:74-75`（唯一的报错点，全库仅此一处）：

```python
        if source.get("source_status") == "ocr-draft" and entry.get("review") == "source-reviewed":
            errors.append(f"{key}: OCR draft requires transcription review before source-reviewed annotation")
```

`source` 来自 `tools/source_paragraphs.py` 的 `load_source_paragraphs(ROOT)`（`validate-annotations.py:50,89`）。
**校验器自己不读任何 page-review 文件**——它只比较 `source_status` 这一个字符串。

### 1.2 决定 `source_status` 的唯一代码路径

`tools/source_paragraphs.py:87-109`。对每个补充版本先装载页审记录，再逐段判定：

```python
    for edition in supplemental_editions(root):
        reviews = {}
        if edition.get("pageReviews"):
            review_data = json.loads((root / edition["pageReviews"]).read_text())
            if review_data["sourcePath"] != edition["file"]:
                raise ValueError(f"Page review refers to another edition: {edition['id']}")
            reviews = {item["pdfPage"]: item for item in review_data["pages"]}
        for row in edition_paragraphs(root, edition):
            review = reviews.get(row.get("pdf_page"), {})
            if review.get("status") == "source-reviewed" and not review.get("unresolved"):
                row["source_status"] = "page-reviewed"
                row["source_label"] = edition["label"] + " · 本页已对照影印"
                row["source_notes"] = ["本页转写已按记录范围对照影印；不代表整本校完或命盘判断已成立。", review.get("scope", "本页转写"), *review.get("notes", [])]
            elif row.get("pdf_page") and row["kind"] != "评注或元数据":
                matched = next((span for span in review.get("reviewedRanges", [])
                                if span["startLine"] <= row["page_start_line"] and row["page_end_line"] <= span["endLine"]), None)
                if matched:
                    row["source_status"] = "passage-reviewed"
```

**精确机制：**

| 项 | 值 |
| --- | --- |
| 文件 | 由 `references/source-editions.json` 中该 edition 的 `pageReviews` 键指定 |
| 两道闸门 | ① 整页路径：`pages[].status == "source-reviewed"` **且** `pages[].unresolved` 为空（falsy）→ `page-reviewed` |
| | ② 段落路径：`pages[].reviewedRanges[]` 有 `startLine ≤ page_start_line` 且 `page_end_line ≤ endLine` → `passage-reviewed` |
| 键 | `status` / `unresolved` / `reviewedRanges[].startLine|endLine`；页主键 `pdfPage` |
| 通过条件 | 结果 `source_status != "ocr-draft"`（`page-reviewed` 与 `passage-reviewed` 都放行） |
| 行号坐标系 | **页内相对行号**，`## PDF第N页` 标题行为 0；与 `split_edition()` 的 `page_start_line = start - page_line` 一致 |

**两条硬性限制（本轮最关键的发现）：**

1. **`评注或元数据` 段落永远拿不到段落路径。** 第 100 行 `row["kind"] != "评注或元数据"` —
   元数据段只能靠“整页 `source-reviewed` 且 `unresolved` 为空”升级。这就是为什么
   大量元数据条目卡在 draft。
2. **`pdf_page == 0` 的段落拿不到段落路径。** 第 100 行 `row.get("pdf_page")` 用了真值判断，
   `0` 为 falsy。两个 page-review 文件都**没有** `pdfPage: 0` 记录（实测：约言 185 页，
   min=1；奇门 195 页，min=20）。页码 0 是文件头块（`> source_pdf:` 等），**不存在对应的影印页**。

### 1.3 已满足闸门的既有范式（27 页先例）

约言 `page-reviews.json` 中 27 页为 `status: source-reviewed` + `unresolved: []`；对应段落
`source_status` 实测为 `page-reviewed`，其上的元数据注解**已被提升**为 `source-reviewed`
（实测 51 条 `page-reviewed`+`source-reviewed`，另有 122 条 `passage-reviewed`+`source-reviewed`）。
即：**先例确实存在，机制可用**——元数据条目在整页核清后是可以合法提升的。

### 1.4 闸门端到端复现（本轮实测，非阅读代码推断）

```
$ python3 tools/validate-annotations.py --annotations /tmp/b1b_probe/ocr.json
1 books, 781 entries, 1 errors
mingli-yueyan:nlc-recovery:P018:L002-L002: OCR draft requires transcription review before source-reviewed annotation
[exit 1]
```
（探针：把 `mingli-yueyan:nlc-recovery:P018:L002-L002` 一条由 `draft` 改为 `source-reviewed`，
写入 `/tmp`，未触碰仓库文件。）

装载器实测四例，证明机制按上述分支工作：

```
metadata line on a PARTIAL page        P018:L002-L002  kind='评注或元数据'  -> ocr-draft
metadata line on a source-reviewed page P003:L002-L003  kind='评注或元数据'  -> page-reviewed
substantive line inside a reviewedRange P018:L008-L009  kind='待分类'        -> passage-reviewed
file header block (pdf_page 0)          P000:L003-L011  kind='评注或元数据'  -> ocr-draft
```

**闸门可以被诚实的本地证据满足（有 27 页先例），本轮的障碍不在闸门设计，在于我无法看图（§3）。**

---

## 2. 比闸门更重要的发现：1,423 条的真实身份

### 2.1 逐条分类（全库 2,835 draft × 源段落状态）

对全部 draft 条目按 `source_status == "ocr-draft"` 过滤后，再按**源段落** `kind` 分类：

| 书 | draft 数 | 源段落 kind | 条数 |
| --- | --- | --- | --- |
| qimen-dunjia-tongzhi | 1,261 | `评注或元数据` | **1,261**（全部） |
| mingli-yueyan | 162 | `评注或元数据` | **161** |
| mingli-yueyan | | `待核实`（封面缺字题名行） | **1** |
| 合计 | **1,423** | | |

**实质论述类（`理论`/`规则候选`/`案例`/`操作步骤`/`术语`）被本闸门挡住者：0 条。**

### 2.2 这些条目写的是什么（原文抽样，非概括）

- `qimen-dunjia-tongzhi:nlc-layouts:P000:L003-L008`
  源文：`> source_pdf: …` `> source_edition: …` `> source_scope: …`（文件头块）
  注解白话：「这是现代恢复档案，记录文瑞书局影印来源与引用资格。」
- `qimen-dunjia-tongzhi:nlc-layouts:P020:L002-L003`
  源文：`> printed_entry: 卷一印页二，左起第三竖列中下部…` `> transcript_scope: …`
  注解白话：「现代转录定位说明，交代本条在纸面的次序与原字的释义分栏范围。」
- `mingli-yueyan:nlc-recovery:P018:L002-L002`
  源文：`> page_review: partial; 主体文字已对照扫描转写，黑底项目序号与版心不作正文…`
  注解白话：「本段为恢复稿 PDF 第018页的校核状态、版心或定位信息，由本次整理生成…不属于古籍理论。」

### 2.3 段落级总量（证明实质内容早已提升完毕）

| 版本 | 源段落 | 实质段（非元数据） | 其中仍未校 | 元数据段 | 其中仍未校 |
| --- | --- | --- | --- | --- | --- |
| `mingli-yueyan:nlc-recovery` | 781 | 592 | **1** | 189 | 161 |
| `qimen-dunjia-tongzhi:nlc-layouts` | 2,471 | 1,210 | **0** | 1,261 | 1,261 |

奇门 1,210 条实质段（局式总表逐格转录）**已全部 `passage-reviewed`**，无一条被拦。
约言 592 条实质段中 537 `passage-reviewed` + 54 `page-reviewed`，仅 1 条 `ocr-draft`。

### 2.4 那唯一一条实质 `ocr-draft`

```
paragraphId: mingli-yueyan:nlc-recovery:P001:L005-L005   kind: 待核实
原文: 精選命〔題名字跡缺失〕約言
自身 notes: "源层 ocr-draft 且缺字，保持 draft。"
P1 review: status=partial, unresolved=["封面题名缺字；印文未释读，不影响正文"],
           reviewedRanges 只覆盖 L007（署名行），不含 L005
```
封面「命」与「約」之间**确实无字迹**（恢复记录 documented），所以它**应当**保持 draft。
把它提升为 `source-reviewed` 等于声称从封面上认出了不存在的字——正是禁止的伪造。

---

## 3. 我能看到的与我看不到的（证据链诚实交代）

| 证据 | 状态 | 说明 |
| --- | --- | --- |
| 影印 PDF（约言） | ✅ 本地存在 | `sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf`，185 页，4,471,099 B，未加密 |
| 影印 PDF（奇门） | ✅ 本地存在 | `sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf`，**408 页**，8,832,333 B |
| 正文文本层 | ❌ **两个 PDF 都无** | `pdftotext -f 18 -l 20` 各只有 3 字节（换页符）。**没有可用的文字证据路径。** |
| 渲染工具 | ✅ 可用 | `/opt/homebrew/bin/pdftoppm`、`pdfimages`、`magick`、`sips` |
| 渲染产物 | ✅ 已生成 | `/tmp/b1b-render/yueyan-018.png`（59,740 B，150dpi） |
| **我读图的能力** | ❌ **无** | `read_image` 返回：`model "deepseek-flash" does not declare image input; switch to an image-capable model to read images` |

**因此：本轮没有任何一页的转写是在“我实际看过影印图”的基础上核对的。**
我拒绝在没有看图的情况下改任何 `status`/`unresolved`。

### 3.1 明确排除的三条“伪证据”路径

1. **不能用电子本互校代替对图。** `collation-notes.md` 记录了大量纸本/电子本**刻意保留的差异**
   （如 PDF99 己亥纸面一九 vs 总表二九；PDF115 丁巳八一 vs 总表八二）。电子本与纸本在此处
   本就分歧，用电子本“投票”会直接抹掉已记录的异文——违反既有规则
   「补充来源不能作为投票证据」。
2. **不能用 `/private/tmp/mingli-pdf-recovery/` 的初识 OCR 当证据。**
   该目录仍在（556 个文件，`all-pages.json` 含 185 页 macOS Vision 初识 + `recognitionRows` 置信度）。
   但它**正是被复核的对象**（`recovery_method` 记载为初识层），OCR 校 OCR 是循环论证，不是对图。
3. **不能用另一个 OCR 引擎的输出当“复核”。** 换引擎只能提供第二意见，不能确认字与图一致。

### 3.2 关于图像能力：配置里有，但不在我的路由权限内

`~/.dsh/settings.yaml` 中确实配置了可读图模型：

```yaml
llm-deepseek:
  models:
    - id: deepseek-v4-flash-vision-exp
      name: DeepSeek-V4-Flash-Vision-Exp
      inputModalities: [text, image]
      imagePixelBudget: 640000
      imageMaxBytes: 1048576
```

但本会话固定在 `provider: deepseek-official / model: deepseek-flash`（纯文本）。我能调用的
委派工具（`subagent`、`subagent_fork`、`dev_mode_subagent`）**均不提供 model/provider 覆盖**，
且我作为被委派子代理的权限在启动时已固定、无法自行放宽。故**未**绕道取用该视觉模型——
这属于超出我路由范围的能力，交由队长决定（§7 给出可直接执行的交接方案）。

---

## 4. 未完成的部分与精确阻塞原因

### 4.1 页级批次：0 / 目标 20-40 页

未复核任何页。阻塞原因（按优先级）：

| # | 阻塞 | 影响 | 精确说明 |
| --- | --- | --- | --- |
| 1 | **本会话模型无图像输入** | 全部页 | 见 §3。`read_image` 被拒；两个 PDF 无文本层。这是唯一的硬阻塞。 |
| 2 | 结构性地不能走段落路径 | 1,422 条 | `source_paragraphs.py:100` 排除 `评注或元数据`；只能整页提升 |
| 3 | `pdf_page == 0` | 2 条 | 无对应影印页，且 `row.get("pdf_page")` 对 0 为假 → 双路径皆不可达 |

### 4.2 若拿到视觉能力，真实的页级工作清单（本轮已算好，可直接执行）

**约言（185 页 = 27 `source-reviewed` + 158 `partial`）：** 158 页 `partial`，**全部都有 `reviewedRanges`**
（即实质正文已开放），阻塞点是版面上的黑底标记未释读：

| 页数 | `unresolved` 原因 |
| --- | --- |
| 120 | 版面项目符号未释读；仅 reviewedRanges 正文可引用 |
| 8 | 版面项目标记未释读；仅 reviewedRanges 主体可引用 |
| 6 | 版面项目标記未释字；只开放 reviewedRanges 内正文 |
| 5 | 黑底排版标记未转写；已核主体正文通过 reviewedRanges 单独开放 |
| 4 | 黑底项目符号不作正文，其内部字形未录 |
| 4 | 装饰项目符号未释读，已与正文分开 |
| 11 | 其余（封面缺字、印文、手写分类号等，多数**应当**保持 unresolved） |

→ ~~约 147 页的阻塞点是同一类：**黑底项目符号/序号**。看清并如实录入这些符号，
即可整页转 `source-reviewed`，从而解锁其上的 161 条元数据注解。~~

> **更正（2026-09-12，逐页看图后推翻；证据：`sources/normalized/bazi/mingli-yueyan/partial-blocker-review-001-030.md`）**
>
> 1. **那 147 不是一处实物的计数，而是这张表里几种不同措辞的行和**：147 = 120+8+6+5+4+4。全表真正写「黑底」的只有 **9 页**，**134 页**写的是「版面项目符号／项目标记未释读」等，被本报告并成了同一类。**措辞不同不等于阻塞物相同**，这一步合并是本报告的方法错误。
> 2. **纸面上确有标记，但标记里没有字**：那是**空心方形装饰性段首标记**（实心黑方框、白心），固定位于小题之上，如 p21「■偏官格 ■印格 ■財格 ■食神格 ■傷官格 ■從格 ■化格」、p18「■看命總法」、p26「■看生年法」、p30「■舊例」。10× 最近邻放大后，白心**除一个白方块外空无一笔**。标记内无字形 → 它**无从「释读」**，也**不构成阻塞**；其下的小题是普通排版文字，草稿里已有。
> 3. **前 30 页逐页计数**：真正的黑底项目符号 **0 页**；空心方框段首标记 **11 页**（18–23、25–28、30，共 18 处）；完全无阻塞物 **19 页**（3–17、24、29；p24/p29 实测零标记）。
> 4. **故「录入这些符号即可整页转 source-reviewed、解锁 161 条注解」这条路径不成立**：这些页是 `partial` 并非因为标记未释读。**「158 页 partial」这个计数经核验是对的**（185 = 27 `source-reviewed` + 158 `partial`），错的只有**阻塞归因**。
> 5. **未做**：31–185 页未核。134/147 条用的是同一种「版面项目符号」措辞，很可能同样归因错误，但那需另跑一次机械复核，**不能由本页样本外推**。
> 6. 本页其余结论不受影响 —— 包括奇门的结构性缺口（408 页、台账只收 195 页、区间内 111 页缺失、1–19 页未收）与「奇门真正的积压是逐时格断与圆图尚未全转」。

**奇门：结构性未完成远大于页审问题。** PDF 共 **408 页**，`nlc-layouts.md` 只收 **195 页**；
review 覆盖同一 195 页（实测两集合完全相同），范围 20–325，其中区间内有 **111 页缺失**：
`21-44, 47-90, 211-212, 280-298, 300-311, 314-318, 320-324`；且 **1–19 页完全未收**。
`collation-notes.md` 已自述「纸本卷四至九全量布局仍未恢复」。
**奇门真正的积压是“逐时格断与圆图尚未全转”，不是提升这 1,261 条台账。**

> **补记（2026-09-12，逐页看图后更正缺口口径；转写见 `sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-0211-0212.md` 等 5 个新批次）**
>
> 1. **缺口的 111 页里，有 9 页不是本书正文**，因此「111 页待转写」这个口径偏高：
>    - `211–212`：**211 为空叶**（墨迹 0.84%，唯一墨迹为 371×371 圆记），**212 为第三册扉页**（书名＋「第 三 冊」＋牌记「上海文明書局印行」）→ **0 页正文**；
>    - `292–298`：**292、297 为空叶**，**293–296 是上海文明书局自家的广告页**（「各種尺牘」「商業用書」「現代論丈彙刊」「新文選」，署「上海文明書局發行」），**298 为第四册扉页** → 该段 19 页中**正文仅 12 页**（280–291 卷八局式）。
>    - 故**待转写的正文页数应为 111 − 9 = 102 页**（把空叶、扉页、书商广告排除在正文缺口之外；这些页仍登记性质与页码，但不计入正文缺口）。
> 2. **册次实测连续**：冊二 090 / 冊三 212 / 冊四 298；而同批叶的版心却作 卷八／卷九 —— **册次与卷次不一致**，照录为观察项，不作调和。
> 3. **缺口已全部有页级登记**（211–212、280–298、300–311、314–318、320–324 共 51 页，5 个新批次文件），其中 30 页当时只到版面级登记。
>    **该「小字不可读」的理由已被实测推翻并更正**：t14 原记「400dpi ≈10–12px/字」是**把页面级节距当成字高**算出来的，**实测为 400dpi ≈42–47px/字、900dpi ≈106px/字（字高中位数，区间 82–128）**，比原记**高约 4 倍**。故「小字无法逐字担保」**不成立** —— 本见证完全支持逐格转写。
>    更正后已建 t17 并完成门槛测量与标准：逐格原生裁切、**先行标（天干＋日支）后断语**、读数标准（可读／〔?〕／〔A／B〕／〔■〕）写入文件头，**PDF 第 283 页已逐格转写为样板**（行标 乙亥／丙子／丁丑／戊寅／己卯）。
>    **剩余 29 页的预算是量出来的、不是估的**：每页 216–430 字 → 合计约 9,500 字、约 100–160 次读图。见 `sources/normalized/san-shi/qimen-dunjia-tongzhi/ocr-batch-cell-level-0283-0324.md`。
> 4. **两处悬案均已用测量结案**（同上文件）：九页 X 节距异常的原因是**同页并存「多字列（节距≈510px）」与「单字列（≈114–120px）」**，整页 X 只取决于哪一族占墨多 —— 决定性的对照是 t14 判为「正常」的 283/285 内部是**同一对带**，即「正常/异常」之分不携带任何取向或字号信息；九页**均正立**（以逐列字序自上而下、Y 节距稳定 150px 证之，不经指纹）。第 324 页 858px 块宽经 900dpi 复测为 1929–1932px÷2.25=859px，**真实存在**，其字号与邻页一致；**唯「为何只有半幅有字」仍不臆断**。
> 5. 本书至此**无未登记页**；未转写的正文页是**已知清单**，不再是未知缺口。

---

## 5. 命令（逐字可复现）

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics

# 闸门定位
grep -rn "OCR draft requires transcription review" tools/validate-annotations.py
sed -n '87,109p' tools/source_paragraphs.py

# 文本层探测（结果：各 3 字节，无文本层）
pdftotext -f 18 -l 20 sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf - | wc -c
pdftotext -f 18 -l 20 sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf - | wc -c

# 页数与渲染
pdfinfo sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf | grep Pages   # 185
pdfinfo sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf | grep Pages # 408
mkdir -p /tmp/b1b-render
pdftoppm -f 18 -l 18 -r 150 -png sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf /tmp/b1b-render/yueyan
#   → /tmp/b1b-render/yueyan-018.png 生成成功；read_image 失败（本会话模型无图像输入）

# draft 按「源段落 kind × source_status」分类（§2.1/§2.3 的数字）
python3 - <<'EOF'
import json, sys, collections
from pathlib import Path
sys.path.insert(0,'tools')
from source_paragraphs import load_source_paragraphs
paras=load_source_paragraphs(Path('.'))
ann={}
for p in sorted(Path('references/annotations').rglob('*.json')):
    d=json.loads(p.read_text())
    for e in d['entries']: ann[e['paragraphId']]=e
for book,ed in (('mingli-yueyan','nlc-recovery'),('qimen-dunjia-tongzhi','nlc-layouts')):
    rows=[(k,v) for k,v in paras.items() if k.startswith(f'{book}:{ed}:')]
    c=collections.Counter((v['kind'],v['source_status']) for _,v in rows)
    print(f'== {book}:{ed} paragraphs={len(rows)}'); [print('   ',k,v) for k,v in sorted(c.items())]
    sub=[(k,v) for k,v in rows if v['kind']!='评注或元数据']
    print('    substantive=',len(sub),' noch=',sum(1 for k,v in sub if v['source_status']=='ocr-draft'))
EOF

# 闸门端到端探针（只写 /tmp，不碰仓库）
python3 - <<'EOF'
import json,subprocess,pathlib
src=pathlib.Path('references/annotations/bazi/mingli-yueyan--nlc-recovery.json')
d=json.loads(src.read_text())
for e in d['entries']:
    if e['paragraphId']=='mingli-yueyan:nlc-recovery:P018:L002-L002': e['review']='source-reviewed'; break
out=pathlib.Path('/tmp/b1b_probe/ocr.json'); out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(d,ensure_ascii=False))
r=subprocess.run(['python3','tools/validate-annotations.py','--annotations',str(out)],capture_output=True,text=True)
print(r.stdout.strip()); print('exit',r.returncode)
EOF

# 页审覆盖范围（奇门缺页）
python3 -c "
import json;ps=sorted(p['pdfPage'] for p in json.load(open('sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layout-page-reviews.json'))['pages'])
s=set(ps);print(len(ps),ps[0],ps[-1]);print('missing:',[n for n in range(ps[0],ps[-1]+1) if n not in s])"

# 计数器
python3 tools/validate-annotations.py
python3 - <<'PY'
import json,pathlib,collections
files=sorted(pathlib.Path("references/annotations").rglob("*.json"))
c=collections.Counter(); n=0; v=0; books=set()
for p in files:
    d=json.loads(p.read_text()); books.add(d.get("bookSlug"))
    for e in d.get("entries",[]):
        n+=1; c[e.get("review")]+=1
        v+= (e.get("verified") is True)
print(f"files={len(files)} books={len(books)} entries={n} " + " ".join(f"{k}={x}" for k,x in c.most_common()) + f" verified_true={v}")
PY
```

---

## 6. before / after 计数

| 项 | before | after | 净变化 |
| --- | --- | --- | --- |
| 注解条目 | `files=79 books=53 entries=62839 source-reviewed=60004 draft=2835 verified_true=0` | **完全相同** | **0** |
| 结构校验 | `53 books, 62839 entries, 0 errors` | `53 books, 62839 entries, 0 errors` | 0 |
| 已复核页（page-review JSON） | 约言 `source-reviewed` 27 / `partial` 158；奇门 `partial` 195 | **完全相同** | **0** |
| 提升条目 | — | **0** | 0 |

**`references/annotations/**` 与 `sources/normalized/**` 本轮零字节修改。**
未新建任何 page-review 记录，未改任何 `status`/`unresolved`/`reviewedRanges`。
`git status --porcelain` 仅显示本报告（及前一轮既有的 `B1-ANNOTATION-BATCH-20260912.md`）。

### 6.1 一处越界写入及其回滚（主动披露）

执行 `python3 tools/build-knowledge-index.py`（为寻找“条目计数器”而试运行）时，
该脚本写入了 `references/inventory/knowledge-index.json`——**超出本轮授权范围**。
已确认该文件 mtime 即为该命令运行时刻，随即按 HEAD 内容还原并逐字节校验：

```bash
git show HEAD:references/inventory/knowledge-index.json > /tmp/ki-restore.json
cp /tmp/ki-restore.json references/inventory/knowledge-index.json
cmp /tmp/ki-restore.json references/inventory/knowledge-index.json   # → 一致
git status --porcelain   # → 该文件不再出现
```

工作树已恢复干净。**该索引文件相对当前注解语料确已陈旧**（还原前的 diff 显示大量段落
仍标 `annotation_review: null`，而注解语料中已是 `source-reviewed`）——但**是否重建由队长决定**，
本轮不代为执行。使用的 git 命令仅 `status` / `diff` / `show`（只读），
未执行 commit / push / reset / clean / checkout。

---

## 7. 交接：拿到视觉能力后应该怎么做

1. **用具备图像输入的会话重跑本轮**（`provider: deepseek-official`，`model: deepseek-v4-flash-vision-exp`）。
   渲染命令与页审机制已在 §5 备好，可直接复用。
2. **约言优先**：挑 20-40 页黑底项目符号页（如 P18、P19 一类的卷一首批），
   300dpi 渲染 → 逐字核对 → 如实录入符号 → 整页转 `source-reviewed` → 提升其元数据条目。
   注意：解锁的是**台账**，不是理论条文；理论条文早已全数提升。
3. **不要为了数字提升元数据。** 2,835 条 draft 中 1,422 条的“价值”是记录恢复稿自身状态；
   把它们标成 `source-reviewed` 只是让台账自证，不增加任何古籍知识。
4. **奇门的真积压另立任务**：408 页 PDF 中 195 页有稿、1–19 页与多段中段未收
   （`21-44, 47-90, 211-212, 280-298, 300-311, 314-318, 320-324`），
   逐时格断与圆图未全转。这才是奇门该做的转写复核。
5. **不要用 `/private/tmp/mingli-pdf-recovery/` 初识 OCR 或电子本充当证据**（§3.1）。

---

## 8. 边界声明

- 本轮**没有**发明任何页审记录；0 提升是诚实结果。
- 本轮**没有**声称 OCR 积压已完成——恰恰相反，§4.2 给出了奇门结构性缺页的完整清单。
- `verified: false` 的全库事实不变（1,423 以外的 1,412 条 draft 属另一类阻塞，非本闸门，
  不在本批次范围）。
- 本报告的每一条数字都可由 §5 的命令逐字复现。
