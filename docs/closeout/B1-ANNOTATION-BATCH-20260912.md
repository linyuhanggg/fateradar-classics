# B1 注解批次报告 — 独立复测与非升级裁定

- 日期：2026-09-12
- 工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`（分支 `dsh/full-library-classics`）
- 写入范围：`references/annotations/**`、本文件
- **本轮结果：升级 0 条。** 2835 条 draft 全部经逐类核查，全部命中「已记录的不升级理由」或结构上不可升级；未发现任何能满足五条硬规则的条目。
- 本文件不声称全库完成，也不声称任何条目已通过影印校勘或人工 verified。

---

## 1. 实测计数（before / after）

### 1.1 before（进入本轮时的实测值）

命令（canonical，可复现）：

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
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

输出：

```
files=79 books=53 entries=62839 source-reviewed=60004 draft=2835 verified_true=0
```

结构校验命令 `python3 tools/validate-annotations.py` 输出：

```
53 books, 62839 entries, 0 errors
```

补充实测事实：

- 实际存在的 `review` 状态**只有两种**：`draft`、`source-reviewed`。不存在 `verified` 或其他第三状态（`tools/validate-annotations.py:38` 只接受这两个值）。
- `verified == true` 全库 **0** 条。
- `terms` 字段是定读术语索引，**不作为原文证据**（本轮核查全程排除 `terms`，见 `tools/validate-annotations.py` 校验语义与 `docs/SOURCE_EDITIONS.md`）。

### 1.2 after

**与本轮 before 完全相同**（本轮 0 次写入注解语料）：

```
files=79 books=53 entries=62839 source-reviewed=60004 draft=2835 verified_true=0
53 books, 62839 entries, 0 errors
```

即：`draft` 2835 → **2835**（净变化 0），`source-reviewed` 60004 → **60004**。`references/annotations/**` 下**没有任何文件被修改**。本轮唯一新建文件是本报告。

---

## 2. 判定方法（把五条硬规则操作化）

对每条 draft：

1. 用 `tools/source_paragraphs.py:load_source_paragraphs()` 取得该 `paragraphId` 的**真实来源文件与行号区间**，读出原文。
2. 抽取 entry 内 `vernacular` / `notes` / `subsections` 中所有 `「…」`、`『…』`、`“…”` 引文（**显式排除 `terms`**，因为 `terms` 是读音索引不是原文）。
3. 逐个引文在**该段原文**做逐字子串匹配（不做任何规范化、不改异体字）；亦允许在 `relatedParagraphIds` 段内匹配。
4. 对声明位置匹配失败的引文，再在全仓 `sources/`、`references/books/`、`references/inventory/`（**排除 `references/annotations/` 自身，避免循环取证**）内定位，判断它是平行本引文还是引错了位置。
5. 凡 entry 自身笔记已记录不升级理由者，**尊重该记录**——因为在笔记仍写着「不升」/「保持 draft」的情况下改写 `review`，会造成条目自相矛盾，属于取证链断裂，正是上一轮 4 条被回退的同一失效模式。

### 2.1 结构闸门（先于语义核查）

`tools/validate-annotations.py:74-75` 硬性拒绝把 `source_status == "ocr-draft"` 的段升为 `source-reviewed`。实测复现：

```bash
mkdir -p /tmp/b1_probe   # 取一条 ocr-draft 条目，仅在 /tmp 内把 review 改为 source-reviewed
python3 tools/validate-annotations.py --annotations /tmp/b1_probe/ocr.json
```

输出（exit 1）：

```
1 books, 1 entries, 1 errors
qimen-dunjia-tongzhi:nlc-layouts:P000:L003-L008: OCR draft requires transcription review before source-reviewed annotation
```

---

## 3. 全量 draft 分类结果

对全部 **2835** 条 draft 逐条分类（首命中即归类），**可升级 = 0**：

| 类别 | 条数 | 主要文件（条数） | 不能升级的具体原因 |
|---|---|---|---|
| A1 来源 `source_status=ocr-draft` | **1423** | qimen-dunjia-tongzhi--nlc-layouts.json(1261)、mingli-yueyan--nlc-recovery.json(162) | 校验器硬拒绝（§2.1）；须先由 `pageReviews` 把页/段升为 page-reviewed / passage-reviewed，见 §6.1、§7.1 |
| B1 笔记自记「不升 / 保持 draft」 | **371** | daliuren-daquan.json(107)、liuren-miben.json(71)、liuren-miben--shidian-SDZJ0628.json(49)、huangji-jingshi--shidian-DZ1040.json(40) | 笔记已写明平行本可对字数不足或未唯一还原；改写 review 会与笔记自相矛盾 |
| B3 残片无法定列，需影印页 | **702** | daliuren-daquan.json(666)、yuqia-ji--shidian-NA09036.json(36) | 原文仅为孤立单字（如表头被抽入单元格流），列归属不可复原；仓内无该本影印 |
| B4 原文截断 / 阙文 / 图像未转写 | **304** | mayi-shenxiang--shidian-NGJ89241199903149974518.json(194)、yuqia-ji--shidian-NA09036.json(108) | 原文本身为 `□`、句未完、残题或〔此处为图像，未转文字〕；无完整原句可引，规则 3、4 不可满足 |
| B5 疑字未改（不改正文） | **35** | yuqia-ji--shidian-NA09036.json(33)、liuren-miben.json(2) | 讹字/残字未唯一还原；笔记明确「不改正文」 |
| C 无可引原文 / 引文不在声明位置 | **0** | — | 分类中间版本中该类曾残留 16 条，逐条读原文后全部为「残」类（句残／歌残／残联／残表），已归入 B4；见 §3.2 |
| D **可升级** | **0** | — | — |
| **合计** | **2835** | | |

### 3.1 抽样审计轨迹（每条含 entry id / 源文件 / 行号 / 原文）

B3（残片）— `daliuren-daquan:L1044-L1044`，源 `sources/fulltext/san-shi/daliuren-daquan/fulltext.md` **L1044**，原文全文即：

```
申
```

笔记原文：「甲日铃残格申。」＋「t2 校核：识典SK1599补本无总钤章节，六壬指南／大六壬秘本／六壬秘本无同表平行本，sources/facsimile 亦无大六壬大全影印；残格仍无法定列，须总钤影印页。」→ 原文仅一字，无课传位次，规则 2/4 不可满足。此类共 666 条（= `docs/closeout/GOAL_CHECKPOINT.md:66` 所记「大六壬总钤残格 666」，本轮**独立复现**该数字）。

B4（阙文）— `mayi-shenxiang:shidian-NGJ89241199903149974518:P7598367455463522338`，源 `sources/normalized/shidianguji/NGJ89241199903149974518/text.md` **L893**：

```
經云：眉毫不頴，耳不如头，□□□壽。
```

笔记：「原文□□□寿。」→ 缺三字，任何补字都是推测，不得写成原意。

B4（图像未转写）— `mayi-shenxiang:shidian-NGJ89241199903149974518:P7598367380087128104`，同源文件 **L9-L10**：

```
〔此处为图像，未转文字；请对照本段原网页。〕
新刊圖相麻衣相法上卷
```

B5（疑字）— `yuqia-ji:shidian-NA09036:P7655682809016975406`，源 `sources/normalized/shidianguji/NA09036/text.md` **L833**：

```
九八嵗男太隂女金星宄九歲男木星女木星
```

`嵗`／`隂`／`宄` 等字形未定读，笔记「原文疑字不改正文」。

B1（自记不升）— `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158868398899250`，源 `sources/normalized/shidianguji/SDZJ0170/text.md`。笔记：「多版本互校（电子主文本）：平行本仅 19/51 字可对（约 37%），不足全条佐证，保持 draft。」

### 3.2 针对「可升级」假阳性的三次收敛

为免漏掉真可升级条目，我做了三轮「放宽→人工读→收紧」：

| 轮次 | 筛选残留 | 人工阅读结论 |
|---|---|---|
| 第 1 轮（拒升标记集较窄） | 88 条 | 86 条为总钤残格（笔记用「仍无法定列」而非「未唯一还原」，故漏网）；2 条为单字残片（`二`、`旹`）→ 全部不可升 |
| 第 2 轮（加入「残格/无法定列」） | 20 条 | 全为「句未完」或 `□□` 阙文 → 全部不可升 |
| 第 3 轮（加入裸字「残」等变体） | **0 条** | — |

三次迭代中，**每一轮残留都被人工逐条读原文后判定为不可升**。这说明剩余 draft 是被有意保留的硬骨头，不是可用模式匹配批量收割的对象；也说明「按正则找可升级条目」本身就会过采，正是上一轮 4 条回退的成因。

---

## 4. 升级条目清单

**无。** 本轮升级条目 id 列表为空，`references/annotations/**` 无任何写入。

之所以不给「最小一批凑数」：四类拒升理由分别卡在规则 1/2（来源与位置）、规则 3（逐字引文）、规则 4（原文本身残缺，解释无从成立）；在原文只有单字、或 `□□`、或整行未转写的情况下，任何升级都只能靠推测补字，属于「发明证据」。

---

## 5. 主动拒绝升级的条目（分组，含缺什么）

按 §3 分类，2835 条全部拒绝。以下给出每组的**具体缺口**：

| 组 | 条数 | 缺什么（具体到文件/页） |
|---|---|---|
| A1-qimen | 1261 | 需先对文瑞书局影印本 `sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf`（408 页）核对，并把核对结果写入 `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layout-page-reviews.json`。现该文件 195 页**全部为 `partial`**，无任何页为 `source-reviewed`；承载 ocr-draft 段的页为：`0,20,45-46,91-210,213-279,299,312-313,319,325`（196 页）。**该文件不在本次写入范围**（范围仅 `references/annotations/**`）。 |
| A1-mingli-yueyan | 162 | 同上机制，文件 `sources/normalized/bazi/mingli-yueyan/page-reviews.json`：185 页中 158 页 `partial`、27 页 `source-reviewed`；承载 ocr-draft 段的页为 `0-2,18-23,25-28,30-36,38-82,84-110,112-162,164-179`（159 页）。亦在写入范围之外。 |
| B3-daliuren 残格 | 666 | 缺《大六壬大全》**总钤章节影印页**。已查证仓内确实没有该本影印：`find sources/facsimile -type f \| grep -iE "daliuren\|daquan"` 返回空；平行本 SK1599 补本无总钤章节，六壬指南／大六壬秘本／六壬秘本无同表平行本。 |
| B3-yuqia 残片 | 36 | 缺《玉匣记》对应影印页；残字为孤立体（如 `安`、`足`、`之大吉`）。 |
| B4-mayi 阙文/图像 | 194 | 缺可读底本文字。仓内**有**影印 `sources/facsimile/wikimedia-known/mayi-shenxiang/NLC416-12jh002690-44091 麻衣相法 第1卷.pdf` 与 `…-44092 第2卷.pdf`，但实测**无文本层**（`pdftotext -f 1 -l 3` 输出 0 字符），须先 OCR 才能比对；且笔记编辑方针为「阙文不补」，改写须新的编辑决定。 |
| B4-yuqia 残表 | 108 | 缺单元格所在原表版面；逐月凶星/值年星辰表的表头被抽入单元格流。 |
| B5 疑字 | 35 | 缺影印或另一独立本以定读（`yuqia-ji` 33 条、`liuren-miben` 2 条）。 |
| B1 平行本不足 | 371 | 已有平行本（`sources/normalized/shidianguji/*`）可对，但可比字数不足（如 19/51 字），或平行本与主本同处截断；**同一电子本的重复副本不算独立佐证**。 |

---

## 6. 与既往报告数字的矛盾（本轮实测结论）

### 6.1 被质疑的那组数字：**准确，未过期、未注水**

任务上下文称「总数 62,839；source-reviewed 60,004；draft 2,835」，并提示可能过期或注水。本轮独立实测**完全复现**：

```
files=79 books=53 entries=62839 source-reviewed=60004 draft=2835 verified_true=0
```

- 与 `docs/closeout/GOAL_CHECKPOINT.md:7` 一致。
- 与 `docs/closeout/GAP_LEDGER.json` 的 `annotations_total: 62839` 一致。
- `draft` 按文件分布与 `GOAL_CHECKPOINT.md:65-67` 所述（奇门 1261 / 大六壬 773 / 玉匣记 180 / 约言 162）一致。

### 6.2 「净升 70、回退 4」：**可由文件独立证实**

- 全库恰有 **4** 条 entry 带 `【t5 复核回退】` 标记且 `review=draft`：`liuren-miben:shidian-SDZJ0628:P7549319964404056118`、`liuren-miben:L1355-L1355`、`liuren-miben:L1361-L1361`、`liuren-miben:L1392-L1392`（命令见 §8.4）。与 `GOAL_CHECKPOINT.md:11-16` 所述 4 条一一对应。
- 计数自洽：`GOAL_CHECKPOINT.md:33` 记升级后 `60,008 / 2,831`，回退 4 条 → `60,004 / 2,835`，**与实测完全吻合**。故那 4 条回退在树内已生效。

### 6.3 找到的两处**真实文档不一致**（此前未报告）

1. **`docs/closeout/GOAL_CHECKPOINT.md` 自身前后矛盾**：头部第 7 行写 `source-reviewed 60,004 / draft 2,835`（=实测值），正文第 33 行写 `source-reviewed 60,008 / draft 2,831`（**实测不复现**，系回退前的快照）。同一文件两个计数相差正好 4。
2. **`docs/CLOSEOUT_20260912.md:8` 计数过期**：写「62,839 条注解，其中 59,610 条 source-reviewed、3,229 条 draft」。实测为 60,004 / 2,835，与 59,610 / 3,229 相差 394 条，属更早轮次快照，未随 t3/t2/t5 更新。该行若被下游引用会低估已审条数、高估待办。

---

## 7. 剩余缺口与关闭条件

1. **A1（1423 条，最大缺口）**：不是语义问题而是**流程/范围问题**。关闭条件：逐页对照影印，在
   `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layout-page-reviews.json`（196 页待核）与
   `sources/normalized/bazi/mingli-yueyan/page-reviews.json`（159 页待核）
   增补 `reviewedRanges` 或把页 `status` 由 `partial` 升为 `source-reviewed`。
   **这两条路径均不在本次写入范围（`references/annotations/**`）**，需要更宽范围的授权才能推进。
2. **B3（702 条）**：需要外部影印（大六壬大全总钤页为主）。仓内无该本，且平行本不覆盖该表。
3. **B4（304 条）**：需要能读底本。mayi 影印已在仓内但**无文本层**；需要 OCR（本机 `tesseract` 可用，但古籍 OCR 质量有限，且属新增 OCR 工作），并需要一次明确的编辑决定是否解除「阙文不补」方针。
4. **B1/B5（406 条）**：需要**新的独立本**（非同一电子本的副本）。同一电子本的重排/重传不能作为独立佐证。
5. **全局**：全库 `source-reviewed` 只表示「与电子文本一致」，**不等于影印校勘，也不等于人工 verified**；`verified==true` 仍为 0。这一点在 `GOAL_CHECKPOINT.md:68` 已注明，本轮实测确认。

---

## 8. 复现命令

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics

# 8.1 计数（本报告 §1 的 before/after）
#     见 §1.1 内联脚本；输出 files=79 books=53 entries=62839 source-reviewed=60004 draft=2835 verified_true=0

# 8.2 结构校验
python3 tools/validate-annotations.py            # → 53 books, 62839 entries, 0 errors

# 8.3 结构闸门复现（ocr-draft 不可仅凭 review 升级）
python3 tools/validate-annotations.py --annotations /tmp/b1_probe/ocr.json

# 8.4 复核「回退 4 条」是否已在树内生效
python3 - <<'PY'
import json,pathlib
for p in sorted(pathlib.Path("references/annotations").rglob("*.json")):
    for e in json.loads(p.read_text()).get("entries",[]):
        b=json.dumps(e.get("notes",[]),ensure_ascii=False)+json.dumps(e.get("vernacular",""),ensure_ascii=False)
        if "t5" in b and ("回退" in b or "复核" in b):
            print(e["paragraphId"], e.get("review"), p.name)
PY
# → 恰 4 条，全部 review=draft

# 8.5 各分类计数与逐条原文（本报告 §3 表格）
#     分类脚本按 §2 方法执行；B3 组 daliuren 666 条可用下式独立确认：
python3 -c "
import json,pathlib,collections
d=json.loads(pathlib.Path('references/annotations/san-shi/daliuren-daquan.json').read_text())
print(collections.Counter(e['review'] for e in d['entries']))
print(sum(1 for e in d['entries'] if e['review']=='draft' and '残格' in json.dumps(e.get('notes',[]),ensure_ascii=False)))"

# 8.6 核验仓内无《大六壬大全》影印
find sources/facsimile -type f | grep -iE "daliuren|daquan"   # → 空

# 8.7 核验 mayi 影印无文本层
pdftotext -f 1 -l 3 "sources/facsimile/wikimedia-known/mayi-shenxiang/NLC416-12jh002690-44091 麻衣相法 第1卷.pdf" - | tr -d '[:space:]' | wc -c   # → 0
```

---

## 9. 结论

- draft 2835 条**全部**有据可查地不可升级；本轮升级 **0** 条，`references/annotations/**` 零改动。
- 上层报告的 `62,839 / 60,004 / 2,835` 经独立实测**准确**；过期的是另外两处文档（`docs/CLOSEOUT_20260912.md:8`、`docs/closeout/GOAL_CHECKPOINT.md:33`）。
- 上一轮「净升 70、回退 4」在树内**可独立复现**（4 条带 t5 回退标记且为 draft）。
- 最大缺口 A1（1423 条）的关闭路径不在本次写入范围内，需授权后按 §7.1 推进；其余缺口需影印/独立本/OCR。
- 本批次**不表示**古籍库已完成，也不表示任何条目通过影印校勘或人工 verified。
