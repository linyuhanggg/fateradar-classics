# Draft 注解去向 · Round 1

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线 SHA：`4cb96e35e545c8496906f9d36081d211f35f86c7`  
范围：优先批次 1（奇门 NLC layouts 元数据）+ 批次 2（draft≤5 小文件）+ 批次 3 抽核（命理约言 nlc-recovery）。**未处理全部 3229 条，不虚报完成。**

规则执行摘要：

- 能对照电子原文核实的，升 `source-reviewed`；`verified` 保持非 true（电子对照 ≠ 人工影印校勘）。
- 繁简/异体只用于检索，未改写引用原文。
- 缺底本、疑字、图残、跨行残、现代元数据、以及 `sourceStatus=ocr-draft` 被校验器拦截的：保留 `draft`，notes 写清原因与影响。
- 未把理论/目录/案例/重复改成规则；风水/相法/禄命/星命去向是知识库，未伪造成已接入算法。
- 未 git commit / push；未改 product 仓；未碰 `/Users/sync/code`。

## 总量

| 项 | 数量 |
|---|---|
| 基线 draft（GAP_LEDGER） | 3229（18 文件） |
| 本轮打开并逐条处理的文件 | 9 |
| 本轮升 `source-reviewed` | **3** |
| 本轮处理仍为 draft | **1438**（奇门 1261 + 约言 162 + 小文件保留 15） |
| 本轮未打开的 draft | **1788**（3229 − 1261 − 18 − 162；大六壬、玉匣记、麻衣、星历考原、六壬秘本、紫微、皇极经世等） |
| 升后全局 draft | **3226**（3229 − 3） |

小文件原 draft 18：升 3（宅经 2 + 天玉经正零神 1），保留 15（地理辨正 4 + 天玉经 4 + 珞琭子 1 + 玉照 2 + 星学 2 + 三命通会 2）。

## 分文件

### 1. `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json`

| | 前 | 后 |
|---|---|---|
| draft | 1261 | 1261 |
| source-reviewed | 1210 | 1210 |
| 本轮升 | 0 | |

**抽核：** 22 条（≥20），白话全部自承「现代定位/恢复/校读/释字」，没有把元数据冒充原书原句。源段均为 `>` 块引用（`printed_page` / `column_position` / `transcript_scope` 等），`kind=评注或元数据`。

抽核样本 `paragraphId`：

1. `qimen-dunjia-tongzhi:nlc-layouts:P000:L003-L008` — 文瑞书局恢复档案头
2. `qimen-dunjia-tongzhi:nlc-layouts:P020:L002-L003` — 卷一印页二宫位句定位
3. `qimen-dunjia-tongzhi:nlc-layouts:P045:L002-L003` — 摘录范围 vs 圆图外圈
4. `qimen-dunjia-tongzhi:nlc-layouts:P046:L008-L008` — 与主电子本标题异文定位
5. `qimen-dunjia-tongzhi:nlc-layouts:P091:L002-L004` — 阳一局总表读表法
6. `qimen-dunjia-tongzhi:nlc-layouts:P091:L009-L009` — 从右至左第 1 列
7. `qimen-dunjia-tongzhi:nlc-layouts:P093:L002-L003` — 印页三乙丑时条定位
8. `qimen-dunjia-tongzhi:nlc-layouts:P093:L012-L014` — 「蓬休九二」现代释字
9. `qimen-dunjia-tongzhi:nlc-layouts:P099:L002-L004` — 承前局题、空数异数
10. `qimen-dunjia-tongzhi:nlc-layouts:P104:L002-L004` — 阳 2 局总表范围
11. `qimen-dunjia-tongzhi:nlc-layouts:P115:L002-L004` — 丁巳使宫一 vs 总表使宫二
12. `qimen-dunjia-tongzhi:nlc-layouts:P120:L002-L003` — 甲戌輔杜 vs 总表輔北
13. `qimen-dunjia-tongzhi:nlc-layouts:P128:L002-L003` — 乙卯任生 vs 总表仕生
14. `qimen-dunjia-tongzhi:nlc-layouts:P133:L002-L002` — 时条与总表字段差异
15. `qimen-dunjia-tongzhi:nlc-layouts:P171:L037-L037` — 阳 7 局第 3 列位
16. `qimen-dunjia-tongzhi:nlc-layouts:P183:L023-L024` — 卷六壬戌条合读范围
17. `qimen-dunjia-tongzhi:nlc-layouts:P198:L051-L051` — 阳 9 局第 4 列位
18. `qimen-dunjia-tongzhi:nlc-layouts:P213:L002-L004` — 阴 1 局总表范围
19. `qimen-dunjia-tongzhi:nlc-layouts:P267:L002-L003` — 阴五局圆图外圈摘录
20. `qimen-dunjia-tongzhi:nlc-layouts:P278:L023-L024` — 卷八癸亥末条
21. `qimen-dunjia-tongzhi:nlc-layouts:P319:L010-L010` — 阴八丙申对校
22. `qimen-dunjia-tongzhi:nlc-layouts:P325:L079-L079` — 阴 9 局第 6 列位

全量 1261 条 vernacular 均含「现代 / 定位说明 / 恢复档案 / 校读 / 对校 / 释字」一类标记，0 条把元数据写成古书原句。notes 中 1256 条已否定原书证据；5 条原先只写来源层或「下方原时条字段单列」，本轮补了「不作古书原句」说明（仍为 draft）。

**不能升的原因（硬拦截，不是偷懒）：**

`references/source-editions.json` 中 `nlc-layouts` 的 `sourceStatus` 是 `ocr-draft`。`tools/source_paragraphs.py` 只把「整页 page-reviewed 且无 unresolved」或「非元数据且落入 reviewedRanges」的段落升为 `page-reviewed` / `passage-reviewed`。这 1261 条源 kind 全是「评注或元数据」，源 status 实测全是 `ocr-draft`。

`tools/validate-annotations.py`：

```
if source.get("source_status") == "ocr-draft" and entry.get("review") == "source-reviewed":
    OCR draft requires transcription review before source-reviewed annotation
```

因此：**即使白话已经明确「这是现代恢复档案/定位说明、不作古书原句」，也不能把这 1261 条标成 source-reviewed，否则校验失败。** 升审必须先完成该 edition 的转录审读（改 page-reviews / 源层状态），不是改注解层能单独完成的。本轮不改源层、不改校验器。

本轮对 JSON 的改动：仅 5 条 notes 补强，review 不动。

保留 draft 原因分类（1261）：

| 原因 | 条数 |
|---|---|
| 现代元数据 + 源层 ocr-draft（校验器禁止升审） | 1261 |

白话模板分布（未改 vernacular）：「现代转录定位说明…分栏范围」1060；「现代页位与对校说明…字段差异」58；各局「仅转录总表的范围；不作古书原句引用」18×7=126；其余定位/释字/异文 17。

---

### 2. 小文件（draft≤5）逐条

#### `references/annotations/fengshui/huangdi-zhaijing--shidian-DZ0282.json`

| | 前 | 后 |
|---|---|---|
| draft | 2 | **0** |
| source-reviewed | 29 | **31** |
| 本轮升 | **2** | |

升审样本：

- `huangdi-zhaijing:shidian-DZ0282:PDZ0282_1_48` — 阳宅二十四路刑祸方。对照识典 DZ0282 `text.md` L249–300。修日与姓忌、北方不用壬子丁巳仍在 notes。段末「丙明堂」邻段 `PDZ0282_1_50` 已是 source-reviewed，本段电子原文可核。
- `huangdi-zhaijing:shidian-DZ0282:PDZ0282_1_54` — 阴宅乾亥壬子。对照 L354–364。宫明姓七月吉、北方不用壬子丁巳分层保留。邻段 `PDZ0282_1_56` 已接续。

`verified` 未设 true。notes 写明：风水宅法入知识库，不接入八术算法。kind 仍为「规则候选」（原书路法条目，不是新造算法接线）。

#### `references/annotations/fengshui/tianyu-jing--shidian-SK1592.json`

| | 前 | 后 |
|---|---|---|
| draft | 5 | **4** |
| source-reviewed | 185 | **186** |
| 本轮升 | **1** | |

升：

- `tianyu-jing:shidian-SK1592:P7640236331671683110` — 正神上山/零神下水、四龙顺逆。对照 SK1592 L950–977。零山零向抱养 vs 正向奸生、向克山虽发福人丁不旺、与「正神行水吉」并存，均保留。风水入知识库，不接入算法。

保留 draft：

| paragraphId | 原因分类 | 影响 |
|---|---|---|
| `…P7640236008973942794` | 跨行残 | 段仅「兩邊安」，不能独立成完整经句 |
| `…P7640236008974221322` | 跨行残 | 截于「贵」，鼓角红旆例未完 |
| `…P7640236333096845338` | 跨行残 | 截于「惊动」，辰戌对冲未完 |
| `…P7640236333096878106` | 缺文 | 原文两处「闕」，不补造 |

#### `references/annotations/fengshui/dili-bianzheng--shidian-SDZJ0504.json`

| | 前 | 后 |
|---|---|---|
| draft | 4 | 4 |
| source-reviewed | 989 | 989 |
| 本轮升 | 0 | |

| paragraphId | 原因分类 | 影响 |
|---|---|---|
| `…P7561132737982218286` | 疑字 | 蒋序讹字过密（五才/养告/恙狗），不能唯一还原；不作完整义疏 |
| `…P7561132737982234670` | 疑字 | 「怡谕密/云书」等不能唯一还原；玉尺不得当蒋派正法 |
| `…P7549187521222246439` | 跨行残/疑字 | 「淬正。直解卷乙四都天實照經」过短，不能定为卷题 |
| `…P7549187521223295015` | 跨行残/疑字 | 「辨正。直解人卷之四…四」过短，不能定为卷题 |

风水材料入知识库。未改 kind。

#### `references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json`

| | 前 | 后 |
|---|---|---|
| draft | 1 | 1 |
| 本轮升 | 0 | |

- `luoluzi-sanming:shidian-SK1605:P7640185840559439882` — **现代元数据/缺底本**。源文为「〔源段仅含版面标记，无可转存文字。〕」。不能补字。禄命入知识库。

#### `references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json`

| | 前 | 后 |
|---|---|---|
| draft | 2 | 2 |
| 本轮升 | 0 | |

- `…P7639282082212053002`、`…P7639282082213412874` — 同上，版面标记占位。

#### `references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json`

| | 前 | 后 |
|---|---|---|
| draft | 2 | 2 |
| 本轮升 | 0 | |

- `…P7430056317387145267` — 现代元数据/缺底本（版面标记）
- `…P7640428574264541234` — 缺文（源文仅「阙」），不补造格局或诗句

星命入知识库，不接入八术算法。

#### `references/annotations/bazi/sanming-tonghui--shidian-HY1521.json`

| | 前 | 后 |
|---|---|---|
| draft | 2 | 2 |
| 本轮升 | 0 | |

- `…P7467786007220338740` — **图残**：河图洛书点数图被线性化，白/黑点数与近尾近头近肩不能唯一还原；不写入河洛算法
- `…P7458198190622310419` — **疑字**：后句「相芜」不可读，不能写成天人各半量化规则

---

### 3. `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`（有时间故抽核，未批量升）

| | 前 | 后 |
|---|---|---|
| draft | 162 | 162 |
| source-reviewed | 619 | 619 |
| 本轮升 | 0 | |

161 条 `评注或元数据` + 1 条封面缺字 `待核实`。白话均标明「恢复稿 / 现代恢复说明 / 封面缺字 / 页外馆藏」，0 条冒充原书理论。notes 158 条已写「只作来源追踪；不计正文白话或规则候选」。

抽核样本：

1. `mingli-yueyan:nlc-recovery:P000:L003-L011` — 扫描底本与处理方式（对照 nlc-recovery.md L3–11）
2. `mingli-yueyan:nlc-recovery:P001:L002-L003` — 封面 partial 状态
3. `mingli-yueyan:nlc-recovery:P001:L005-L005` — 「精選命〔題名字跡缺失〕約言」，不猜补「理」
4. `mingli-yueyan:nlc-recovery:P001:L009-L009` — 封面留白与未释篆印
5. `mingli-yueyan:nlc-recovery:P002:L002-L003` — 页外馆藏号不作正文
6. `mingli-yueyan:nlc-recovery:P097:L002-L003` — 第 097 页校核状态/版心
7. `mingli-yueyan:nlc-recovery:P178:L002-L003` — 第 178 页同上模板

**不能升：** 162 条源 status 全是 `ocr-draft`（edition `nlc-recovery` 同样 `sourceStatus=ocr-draft`）。与奇门 layouts 同一校验器拦截。封面 `P001:L005-L005` 另外还有缺字。本轮只给 4 条空 notes 补了原因，review 不动。

保留 draft 原因分类（162）：

| 原因 | 条数 |
|---|---|
| 现代元数据 + 源层 ocr-draft | 161 |
| 缺字（封面题名）兼 ocr-draft | 1 |

---

## 本轮保留 draft 的原因分类（仅已处理条目）

| 原因 | 条数 | 说明 |
|---|---|---|
| 现代元数据 + 源层 ocr-draft（校验器禁止升审） | 1422 | 奇门 1261 + 约言 161 |
| 缺字兼 ocr-draft | 1 | 约言封面 |
| 疑字（电子原文不能唯一还原） | 3 | 地理辨正蒋序 2 + 三命通会「相芜」1 |
| 跨行残 | 5 | 天玉经 3 + 地理辨正残卷题 2（后者兼疑字，计入本行 2、不重复计入疑字） |
| 缺文 / 阙 | 2 | 天玉经两处阙 + 星学大成「阙」（天玉 1 + 星学 1） |
| 图残 | 1 | 三命通会河洛碎行 |
| 现代元数据/缺底本（版面标记，非 ocr-draft） | 4 | 珞琭子 1 + 玉照 2 + 星学版面 1 |
| **已处理仍为 draft 合计** | **1438** | 1261+162+15 |
| **本轮升 source-reviewed** | **3** | 宅经 2 + 天玉经正零神 1 |

跨行残细目：天玉「兩邊安」「截于贵」「截于惊动」3；地理辨正两条残卷题 2。缺文：天玉两处阙 1、星学阙 1。疑字：地理辨正蒋序 2、三命「相芜」1；两条残卷题虽兼疑字，为避免重复只计入跨行残。

未处理（本轮不动）：1788 = 3229 − 1261 − 18 − 162。其中 18 是小文件原 draft 数（升 3 后小文件剩 15 draft）。

## 实际修改的 JSON

1. `references/annotations/fengshui/huangdi-zhaijing--shidian-DZ0282.json` — 2 条 review→source-reviewed，补 notes
2. `references/annotations/fengshui/tianyu-jing--shidian-SK1592.json` — 1 条升审，4 条补原因
3. `references/annotations/fengshui/dili-bianzheng--shidian-SDZJ0504.json` — 4 条补原因
4. `references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json` — 1 条补原因
5. `references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json` — 2 条补原因
6. `references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json` — 2 条补原因
7. `references/annotations/bazi/sanming-tonghui--shidian-HY1521.json` — 2 条补原因
8. `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` — 5 条 notes 补强，review 未升
9. `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` — 4 条空 notes 补齐，review 未升

`paragraphId` 无改动。`verified: true` 出现次数仍为 0。

## 下一轮建议（不在本轮做）

1. 若产品确认「元数据对照说明层」可以绕过 ocr-draft 拦截，应先改 `validate-annotations.py` 与 `source_paragraphs.py` 的元数据例外，再回头升奇门 1261 + 约言 161。本轮按现校验器执行，故未升。
2. 大六壬大全 845、玉匣记 267、麻衣 222、星历考原 185 等仍全是 draft，需要按底本可核程度另开轮次，禁止批量标「不支持」。
3. 风水/禄命/星命已核条目只进知识库，不要在产品仓接线。

## 验证命令与结果

工作目录：`/Users/yuhanglin/fateradar-goal-20260912/classics`

```bash
python3 tools/validate-annotations.py
python3 tools/validate-annotations.py --json
```

纯文本结果：

```
53 books, 62839 entries, 0 errors
```

JSON 摘要：

```json
{
  "ok": true,
  "books": 53,
  "files": 79,
  "entries": 62839,
  "source_reviewed": 59613,
  "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
  "errors": []
}
```

对照 GAP_LEDGER 基线 `source_reviewed` 59610 / `draft` 3229：本轮 +3 source-reviewed、−3 draft，与宅经 2 + 天玉经 1 一致。校验器声明这只是结构与段落 ID 检查，不是语义证书，更不是人工 verified。

未执行 `git commit` / `git push`。`git status` 仅古籍工作树注解 JSON 与本文件。
