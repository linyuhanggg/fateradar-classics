# 需要人工判断（可复算台账）

由 `python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md` 生成。
**本文件不写任何锚点、不改任何规则**——「不要硬锚」是硬约束；这里只做核对与登记。
全部 `verified` 仍为 `false`。

旧件是 P6/P7/P10/P11 时期的手写过程稿、无生成器，已累积失真（见各条 `论断已过时`）。

## 一、台账总览

论断 13 条：**已解决 3**、**仍未决 8**、**论断已过时 0**、**机器不可判 2**

| 论断 | 类别 | 状态 |
|---|---|---|
| `faqiao-no-fulltext` | 著作权 / 无全文 | **仍未决** |
| `pack-meta-rules` | Pack 元规则（不在书中） | **仍未决** |
| `multi-occurrence` | 原文多次出现、无法唯一落点 | **机器不可判** |
| `modern-summary` | 现代概括，书中无对应命题 | **仍未决** |
| `p7-lz-metadata-quote` | P7 恢复名单 | **仍未决** |
| `v14-low-correspondence` | V14 低对应度 | **仍未决** |
| `v11-g1-target` | V11 与 G1 | **已解决** |
| `qizheng-factgap` | 七政格局 / 行限未加 FactKey | **仍未决** |
| `catalog-titles` | 七政目录篇名 | **仍未决** |
| `procedure-kind` | 起例改 procedure | **仍未决** |
| `ziwei-palace-scope` | 紫微宫位 scope | **已解决** |
| `p6-grey-zone` | P6 灰区（对应度 0.15–0.30） | **机器不可判** |
| `restatement-census` | 190 条不可锚的根因（本轮实测新增） | **已解决** |

## 二、机器实测的规模（旧件未给、或已漂移）

- **`anchor: null` 的规则共 189 条**（旧件按「81 条」流传，那是**行数**不是条数）。
- 这 189 条的 `quote_kind` 分布：`restatement` 189。
- `validate-rules.py` 当前 warning：V11 111、V14 174，合计 285（G1 要 V11 < 50，**仍未达**）。
- `book.script` 与 fulltext 实际用字：实测 **55 本，不符 0 本**。

> ⚠️ **本节是旧件最需要的更正**：`anchor_recover.py` 在 t167 入库 31,525 源段之后重跑过一次，表观「可以锚 25 条」；加两道前置闸门（跳过 `restatement`、用 V13 判据挡劣质 quote）后**可锚数归零**——那 25 条全是被锚上的**来源标签**（如「入地眼全書龍法卷二」）或重述文本。也就是说：`anchor: null` 不是「还没找到」，是**没有可找的对象**。

| 书目 | anchor: null 条数 |
|---|---:|
| `luming-nayin/luoluzi-sanming` | 12 |
| `luming-nayin/yuzhao-shenying` | 12 |
| `bazi/yuanhai-ziping` | 11 |
| `divination/huangji-jingshi` | 10 |
| `xingming/xingming-suyuan` | 10 |
| `divination/zhouyi-zhezhong` | 9 |
| `luming-nayin/lantai-miaoxuan` | 8 |
| `physiognomy/shenxiang-quanbian` | 8 |
| `bazi/sanming-tonghui` | 7 |
| `divination/zengshan-buyi` | 7 |
| `ziwei/ziwei-doushu-quanshu` | 7 |
| `bazi/mingli-yueyan` | 6 |
| `divination/bushi-zhengzong` | 6 |
| `luming-nayin/wuxing-jingji` | 6 |
| `san-shi/liuren-zhiyin` | 6 |
| `selection/xingli-kaoyuan` | 6 |
| `bazi/shenfeng-tongkao` | 5 |
| `fengshui/dili-bianzheng` | 5 |
| `physiognomy/liuzhuang-xiangfa` | 5 |
| `bazi/qiongtong-baojian` | 4 |
| `fengshui/rudi-yan-quanshu` | 4 |
| `san-shi/taiyi-shenshu` | 4 |
| `selection/yuqia-ji` | 4 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | 4 |
| `selection/donggong-zeri` | 3 |
| `xingming/guotian-jing` | 3 |
| `fengshui/hanlong-jing` | 2 |
| `fengshui/xuexin-fu` | 2 |
| `fengshui/yangzhai-shishu` | 2 |
| `physiognomy/mayi-shenxiang` | 2 |
| `san-shi/liuren-miben` | 2 |
| `bazi/ditiansui-chanwei` | 1 |
| `divination/meihua-yishu` | 1 |
| `fengshui/shenshi-xuankong-xue` | 1 |
| `fengshui/yilong-jing` | 1 |
| `fengshui/zangshu` | 1 |
| `luming-nayin/li-xuzhong-mingshu` | 1 |
| `selection/xieji-bianfang-shu` | 1 |

## 三、逐条论断与复核

### 著作权 / 无全文

#### `faqiao-no-fulltext` — **仍未决**

- 旧件原文：san-shi/qimen-faqiao QM-P26、QM-P36：仓库无 fulltext，禁止抓现代出版社整理本。
- 写法校正：QM-P26 / QM-P36（与当前 rule_id 一致）
- 涉及规则 2 条
- 复核结论：旧件的顾虑是著作权（不得抓现代整理本）。现两条 anchor 指向 `sources/excerpts/qimen-faqiao-chaibu-v1.md`，是仓内自制选段、非抓取版，故该顾虑不再阻塞；是否接受「以选段为据」仍需人认可。

### Pack 元规则（不在书中）

#### `pack-meta-rules` — **仍未决**

- 旧件原文：statement 含「安全改写 / reframe / 不替代 / 并读 / 调用本 pack」等，原文无对应句：`bazi/shenfeng-tongkao` R01–R05；`luming-nayin/lantai-miaoxuan` M01、R01–R07；`divination/bushi-zhengzong` R01–R06；`xingming/xingming-suyuan` XINGMINGSUYU-042/043。
- 写法校正：R01–R05 / M01 / R01–R07 / R01–R06 是 **statement 前缀**，不是 rule_id；按 id 检索会全部落空。此处换成当前真实 id。
- 涉及规则 21 条
- 复核结论：21 条全部仍 anchor: null，论断成立：原文确实没有对应句，不能锚。这批是**永久性**的（除非人决定把它们单独归类成 pack 元规则而不列入待复核），不是待办。
    - **旧件字面写法有 19 个 id 检索不到**（说明照抄旧件会找不到条目）：bazi/shenfeng-tongkao R01（不存在）、bazi/shenfeng-tongkao R02（不存在）、bazi/shenfeng-tongkao R03（不存在）、bazi/shenfeng-tongkao R04（不存在）、bazi/shenfeng-tongkao R05（不存在）、luming-nayin/lantai-miaoxuan M01（不存在）…

### 原文多次出现、无法唯一落点

#### `multi-occurrence` — **机器不可判**

- 旧件原文：`xingming/xingming-suyuan` 五曜连珠（4 处）、度主为正、飞廉、转生、闌干煞、流年三方对照；`divination/meihua-yishu` 乾兑属金（五行配卦多次）；`divination/zhouyi-zhezhong` 「形而上者谓之道」「见几而作」等经文多次；`luming-nayin/wuxing-jingji` 纳音 / 华盖单字标题过短。
- 写法校正：以篇名/术语描述，未给 rule_id。
- 复核结论：旧件只给术语、不给 id，机器无从逐条核对；且「哪一处算唯一落点」是**人的判断**，不能由机器定。要推进必须先补 id 清单。
    - 未给 rule_id，且「唯一落点」属人的判断

### 现代概括，书中无对应命题

#### `modern-summary` — **仍未决**

- 旧件原文：`divination/huangji-jingshi` HR-01 元会运世换算、HUANGJIJINGS-007/020/021「非占断 / 非国运 / 非个人命术」；`xingming/xingming-suyuan` 卷四后篇案例总述。
- 写法校正：HR-01 等与当前 rule_id 一致
- 涉及规则 4 条
- 复核结论：4 条仍 anchor: null，论断成立。「卷四后篇案例总述」旧件未给 id，机器不可判。

### P7 恢复名单

#### `p7-lz-metadata-quote` — **仍未决**

- 旧件原文：`LZ`（`physiognomy/liuzhuang-xiangfa`）quote 是 `source_base:` 元数据，P7 恢复名单误列，已改回 `anchor: null`。
- 写法校正：LZ
- 涉及规则 1 条
- 复核结论：仍 anchor: null，且 quote 仍含元数据形态；论断成立。

### V14 低对应度

#### `v14-low-correspondence` — **仍未决**

- 旧件原文：`FEIXINGZIWEI-008` 对应度 0.140、`ZIWEIDOUSHUQ-ZW-05` 对应度 0.106，V14 WARN。
- 写法校正：两个 id 与当前一致
- 涉及规则 2 条
- 复核结论：实测对应度与旧件一致（0.14 / 0.106），论断成立。这两条是「statement 概括性强」而非 quote 有问题——V14 本身已注明该档不必据以动手。
    - ziwei/feixing-ziwei-doushu-yuanzhi FEIXINGZIWEI-008：对应度 0.140
    - ziwei/ziwei-doushu-quanshu ZIWEIDOUSHUQ-ZW-05：对应度 0.106

### V11 与 G1

#### `v11-g1-target` — **已解决**

- 旧件原文：G1 要求 V11 < 50，当前约 112。需人决定：是否按 fulltext 实际用字改正 `book.script`，或接受 V11 残留。
- 写法校正：—
- 复核结论：**旧件给的这个「需人决定」项，本轮用测量结案**：55 本书的 `book.script` 与各自 fulltext 实际用字**全部一致（0 处不符）**，所以没有「按实际用字改正 book.script」这回事——该选项是空的。V11 的真实成因是引文形态（未锚条目用另一种字形的概述），不是 script 登记错。
- 结案：book.script 无需更正（实测 0 处不符）

### 七政格局 / 行限未加 FactKey

#### `qizheng-factgap` — **仍未决**

- 旧件原文：任务书 3a 要求加 `qizheng_geju`、`xingxian`；3c 要求引擎必须从已有排盘结果取出。实测 `buildQizheng` 只有星曜宫位宿度庙旺，没有格局名或行限字段。按 3c 不加这两个 key。约 35 条七政未映射规则本轮仍空。
- 写法校正：GUOTIANJING-GR-02 / -GR-05 / GR-03（旧件混用了裸 id 与带前缀 id）
- 涉及规则 3 条
- 复核结论：三条仍无可写谓词。「加 qizheng_geju / xingxian」需要新写五曜格局与洞微百六限算法，属算法开发，不在语料轮次范围。**数字已漂移**：旧件说「约 35 条七政未映射」，实测 **65 条**。
    - **数字漂移**：七政未映射 旧件记 35，实测 65

### 七政目录篇名

#### `catalog-titles` — **仍未决**

- 旧件原文：P11 把 31 条 `xingming-suyuan` 未映射规则改归「目录篇名，不是可判定规则」，并从谓词覆盖率分母剔除。下列 statement 带一点判定语气，但仍保守留在目录篇名：XINGMINGSUYU-XR-03、XR-04、XINGMINGSUYU-XR-04、XR-06、XINGMINGSUYU-038、XINGMINGSUYU-047、XR-07。
- 写法校正：与当前一致
- 涉及规则 7 条
- 复核结论：7 条确实都在 `CATALOG_TITLE_RULE_IDS` 名单内（已从覆盖率分母剔除并单独计数），论断成立。

### 起例改 procedure

#### `procedure-kind` — **仍未决**

- 旧件原文：`GR-01` / `GR-03` 已改 `kind: procedure`。
- 写法校正：裸 id。同书另有 `GUOTIANJING-GR-01` / `-GR-03` 两条**不同**规则，前者 doctrine、后者 procedure——旧件不写明前缀会让复核者改错条。
- 涉及规则 2 条
- 复核结论：两条确实都是 procedure，论断成立（但 id 写法必须带准，见 doc_notation）。

### 紫微宫位 scope

#### `ziwei-palace-scope` — **已解决**

- 旧件原文：24 条规则、54 个谓词按 statement 写了 `scope.palace`。未加 scope 的包括：星性、夹命、地支居子/居午、未点名宫位的同宫、宫位专章无列星、`TAIWEIFU-004` 天马。G10 未达标：仍无法在不改 `ziwei.ts` / 不改断言的前提下让默认 top-6 两盘不同。
- 写法校正：TAIWEIFU-004
- 涉及规则 1 条
- 复核结论：**G10 已不成立**：本轮实测产品仓 `tests/rules/predicate-matching.test.ts` 的「两盘 ruleId 集合不同」对六个 art（含 ziwei）**全部通过**，即该阻塞已消失，不需要改 `ziwei.ts`、也不需要为凑差异补宫位。TAIWEIFU-004 仍无 scope.palace（留给 V15 reverse6 用例）。
- 结案：G10 阻塞已消失（产品仓该断言现为绿）

### P6 灰区（对应度 0.15–0.30）

#### `p6-grey-zone` — **机器不可判**

- 旧件原文：任务书要求机器不动这一档，留人抽检。不要为了覆盖率把任务 5 已降级的 `<0.15` 填回去。
- 写法校正：—
- 复核结论：这是**政策**而非待办：机器不得动 0.15–0.30 档。本轮未动该档任何条目。
    - 政策声明，无逐条对象

### 190 条不可锚的根因（本轮实测新增）

#### `restatement-census` — **已解决**

- 旧件原文：旧件把这些条目分列为「无全文 / pack 元规则 / 原文多次出现 / 现代概括 / P7 名单 / V11」六类，读起来像是六种不同的待办。
- 写法校正：—
- 复核结论：**实测：全部 189 条不可锚规则的 `quote_kind` 都是 `restatement`（编者重述），一条不例外。**也就是说它们的 `quote` 本身就是现代概述、**原文里根本没有对应句子可指**——「不要硬锚」在这里不是政策限制，而是逻辑后果：没有可锚的对象。本条同时解释了 §二 的 V11：未锚条目用概述、且概述多为另一种字形，于是与 `book.script` 的字形统计不同向。
    - 未锚 189 条的 quote_kind：['restatement']
- 结案：归类归并：189 条的真问题只有一个——是否把重述换成真引文（会改动 quote），不是 189 个各自找锚点

## 四、仍需人决定的事（机器不能代劳）

1. **`multi-occurrence` 那一档要先补 rule_id 清单**：旧件只给术语，「哪一处算唯一落点」是人的判断，机器不能定，也不能为提高覆盖率擅自选一处锚上。
2. **V11 的残留怎么处置**：`book.script` 已实测无需更正，所以只剩两条路——逐条补锚（把概述换成原文，但会改动 `quote`）或接受残留。两条都要人拍板。
3. **pack 元规则（21 条）是否单列一类**：它们「原文无对应句」是**永久事实**、不是待办，继续留在「待人工判断」里会稀释这一页的信号。
4. **P6 灰区（对应度 0.15–0.30）**：政策要求机器不动该档，仍需人抽检；本轮未动该档任何条目。

## 五、可复跑

```bash
python3 tools/needs-human-review-report.py
python3 tools/needs-human-review-report.py --json
python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md
```
