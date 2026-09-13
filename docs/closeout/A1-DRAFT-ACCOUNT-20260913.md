# A1 · 2,835 条 draft 逐项去向分账（2026-09-13）

范围：`references/annotations/**` 全部 `review != source-reviewed` 的条目（17 文件）。
方法：**不采信台账快照**——逐条用 `tools/source_paragraphs.load_source_paragraphs()` 重算源段落状态
（含影印层 `pageReviews` 的 `reviewedRanges` 判定），再按类落去向。逐条结果：
`docs/closeout/review/a1-draft-disposition-20260913.json`（2,835 行，一行一条：file／bookSlug／paragraphId／kind／source_status／disposition／action）。

## 0. 两条先说的结论

1. **「已处理未入库」实测为 0 条。** 没有一条 draft 的源段落处于「已核」（`passage-reviewed`／`page-reviewed`）
   而注解仍未提升的状态。也就是说：A1 的余量不是「把已做好的搬进来」，而是**审读/转写本身还没做**。
2. **1,531 条 draft 是台账，不是知识。** 其中 1,422 条的源段落状态是 `ocr-draft`（恢复稿写给自己的
   `page_review`／定位／状态行），109 条是电子本侧的同类元数据。这与 `B1b-OCR-TRANSCRIPTION-BATCH.md`
   的 1,423 条闸门结论一致（1,422 评注或元数据 + 1 待核实）；**这道闸门拦的是台账**。

## 1. 四类分账（合计 2,835）

| 类 | 条数 | 定义 | 去向（本轮即处置） |
|---|---:|---|---|
| 台账元数据 `ledger-metadata` | **1,531** | 定位/状态行（`> page_review:` 等），非论述 | **保持 draft、不提升、不排入审读队列**；随所属影印层转写状态变化。最大两块：qimen `nlc-layouts` 1,261、mingli-yueyan `nlc-recovery` 161 |
| 实质条目待审 `entry-review-pending` | **1,296** | 理论/规则候选/案例/术语/操作步骤/待核实 等正文级条目 | **逐条审读**（不批量升级）；来源为电子本（`reference-text`） |
| 待转写 `source-transcription-pending` | **1** | 源段落 `ocr-draft` 且非台账（mingli-yueyan 1 条） | 待影印转写与页审；**不得据电子本代填** |
| 归档 `archived-out-of-scope` | **7** | 重复 2、序跋目录 5 | 归档，不再审读 |

### 按 kind 复核（与分账交叉一致）

| kind | 条数 | 落在哪类 |
|---|---:|---|
| 评注或元数据 | 1,531 | 全部 `ledger-metadata` |
| 待核实 | 795 | 全部 `entry-review-pending` |
| 规则候选 | 297 | `entry-review-pending` |
| 术语 | 106 | `entry-review-pending` |
| 案例 | 73 | `entry-review-pending` |
| 理论 | 16 | `entry-review-pending` |
| 操作步骤 | 10 | `entry-review-pending` |
| 序跋目录 / 重复 | 5 / 2 | `archived-out-of-scope` |

（1,296 = 795 + 297 + 106 + 73 + 16 + 10 − 1：其中 1 条「待核实」的源段落是 `ocr-draft`，归 `source-transcription-pending`。）

## 2. 逐文件（按 draft 数降序）

| 文件 | draft | 分账 |
|---|---:|---|
| qimen-dunjia-tongzhi--nlc-layouts.json | 1,261 | 台账 1,261 |
| daliuren-daquan.json | 773 | 待审 769 · 台账 4 |
| mayi-shenxiang--shidian-NGJ89241199903149974518.json | 222 | 待审 177 · 台账 42 · 归档 3 |
| yuqia-ji--shidian-NA09036.json | 180 | 待审 125 · 台账 55 |
| mingli-yueyan--nlc-recovery.json | 162 | 台账 161 · 待转写 1 |
| liuren-miben.json | 74 | 待审 72 · 台账 2 |
| liuren-miben--shidian-SDZJ0628.json | 50 | 待审 42 · 台账 5 · 归档 3 |
| huangji-jingshi--shidian-DZ1040.json | 40 | 待审 40 |
| ziwei-doushu-quanshu--shidian-SDZJ0170.json | 40 | 待审 40 |
| mayi-shenxiang.json | 17 | 待审 16 · 归档 1 |
| dili-bianzheng--shidian-SDZJ0504.json | 4 | 待审 4 |
| tianyu-jing--shidian-SK1592.json | 4 | 待审 4 |
| sanming-tonghui--shidian-HY1521.json | 2 | 待审 2 |
| xingxue-dacheng--shidian-SK1609.json | 2 | 待审 2 |
| yuzhao-shenying--shidian-SK1602.json | 2 | 待审 2 |
| luoluzi-sanming--shidian-SK1605.json | 1 | 待审 1 |
| xingli-kaoyuan--shidian-SK1618.json | 1 | 台账 1 |

## 3. 对 A1 验收的含义（边界）

- **「不能笼统待处理」这一条现在满足了**：2,835 条每条都有 category＋去向（机器可读逐条表）。
- **但 A1 仍不能判 pass**：`entry-review-pending` 1,296 条是**审读余量**，需要逐条读原文并决定
  （提升／保持 draft／改 kind），这不能靠一次分账完成，也不能批量升级。
- 台账 1,531 条的「去向」是**不提升**，这是明确处置，不是「待处理」；其中 1,261 条 qimen 台账
  与 t2 的影印转写批次同源（308–311 仍是未转写页，见 `E3-QIMEN-OCR-BATCH-308-311-BLOCKED.md`）。
- 数字对照：账本 `measured_baseline` 的 draft 2,835 / source-reviewed 60,004 与本轮重算一致；
  `GAP_LEDGER.json#counts` 里的 2,905／59,934 是过期快照（已在 A1 remaining 登记）。

## 4. 复现

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
export PATH="$HOME/.bun/bin:$HOME/.local/bin:$PATH"
# 逐条分账（重算 source_status 后落 disposition）
python3 tools/validate-annotations.py        # 全库注解校验（应 0 errors）
# 逐条结果
python3 -c "import json;d=json.load(open('docs/closeout/review/a1-draft-disposition-20260913.json',encoding='utf-8'));print(d['draft_total'],d['by_disposition'])"
```
