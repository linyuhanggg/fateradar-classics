# A1 未决项逐条索引（《總鈐》666 残格全量 ＋ 未确认影印底本 16 套）

日期：2026-09-13　执行：classics-audit（t20）　机器可读：`docs/closeout/evidence/a1-open-items-20260913.json`

> 本件是**可定位性索引**，不是取证：666 行按已定类级口径同构展开（未为 656 条重做判断）。
> 只新增／更新 `docs/closeout/evidence/**`，**未改** `references/**`、`sources/**` 与账本；`verified`／`canonical_eligible` 保持 false。

## 1. 计数与自检

| 项 | 数 |
|---|---:|
| 《總鈐》残格集合（draft＋待核实＋含「残格」） | 666 |
| 《總鈐》逐条索引（本件） | **666** |
| 其中带影印页映射者 | 664（其余 2 条为月表型，页级映射未建立） |
| 未确认影印底本（全量） | 16 |
| 文件内条目合计 | **682** |
| **精确未决、不影响主要能力** | **682** |
| **仍影响主要能力（须列 blocked）** | **0** |

自检（脚本断言）：666 行 ✓｜id 无重复（unique 666）✓｜四栏非空（empty = 0）✓｜class 一致 ✓｜段落范围 L1010–L2468 ✓。

## 2. 每行四栏

| 栏 | 内容 |
|---|---|
| `id` | `總鈐残格·daliuren-daquan:L####-L####`（与电子本段落 ID 一一对应，逐条唯一） |
| `locator` | `paragraphId`＋**`line_range`（行范围）**＋**`facsimile_page`（影印页，表级）**＋`facsimile_page_basis`（映射依据：该条自述标目）＋`facsimile_scope`（十表 p16–p25；逐格/逐列映射未建立的声明）＋`column_within_table`（列与格位：未建立，不推算）＋`content_lead`＋`terms`＋`kind`＋`review` |
| `class` | 一律 `precise-undecided-not-blocking` |
| `product_handling` | 保留〔?〕、不入规则：保持 draft，不入 `references/executable`、不进算法、不猜字、不补格、不连成月日全表、不升 verified；只作「已披露限制」参与验收。**解锁条件＝取得可判归属的清晰影印或平行本**，再由独立复核把已定格升 `passage-reviewed` |
| （附）`what_is_missing` | **影印在仓、逐格归属不可判**（旧记「缺影印件」已推翻）：四庫本卷一影印在仓（112 页，sha256 7790f774…），字心距≈70px、字面宽≈100–110px → 同列粘连成 200–250px 墨条、邻栏 x 重叠 |
| （附）`attempts` | B2 溯源／B4 实抓 SK1599 比对／t10 影印定位／t7·t11 版式普查与逐格转录／ROUND6 §3 的 666/666 更正 note |

### 影印页分布（由各条自述标目映射，可复算）

| 影印页 | 表 | 条数 |
|---|---|---:|
| p16 | 六甲日 | 53 |
| p17 | 六乙日 | 70 |
| p18 | 六丙日 | 59 |
| p19 | 六丁日 | 77 |
| p20 | 六戊日 | 61 |
| p21 | 六己日 | 80 |
| p22 | 六庚日 | 58 |
| p23 | 六辛日 | 83 |
| p24 | 六壬日 | 62 |
| p25 | 六癸日 | 61 |
| —（月表型，页级映射未建立） | 十二月辰／十二月亥 | 2 |
| **合计** |  | **666** |

## 3. 子群检查：是否存在「其实可判」的不同类别

| 子群 | 条数 | 说明 |
|---|---:|---|
| 十表·格内残字型（`残格「X」。在…标目下…`） | 664 | 均可映射到六甲日–六癸日十表之一（见上表）；条目自身写明「待核，不补三传、不改正文」 |
| 月表·神名串型（`十二月X：神名…`） | 2 | `L1010`（十二月辰）、`L1038`（十二月亥）；同为待核，且无页级映射 |
| 自述「归属已定／已定格／已可定列」 | **0** | 无一条声称归属已解决 → **不存在可单独升级或另立类别的子群** |

结论：两个子群只是**内容形态**不同（十表格内残字 vs 月表神名串），**类别一律相同**；`kind`／`review` 全为 待核实／draft，note 覆盖 666/666。
「逐项」的意义即在于此：每条都能定位到**行范围＋影印表页**，且明确写出**为什么不能定归属**、**产品怎么处理**、**什么条件下才解锁**。

## 4. 方案「特殊资料 2 套」的归属（回答 captain 第 3 问）

**结论：两者不是等价说法，是层级混用＋旧计数；磁盘实数 16 为准。**

| 核对项 | 实测 |
|---|---|
| `LIBRARY_INVENTORY.md` 的影印status 桶 | 只有三类：已存影印 34 ＋ Release 影印 5 ＋ **尚未确认影印 16** ＝ 55；**没有第四类「特殊资料」桶** |
| `sources/fulltext/**` 下非 `fulltext.md` 的 Markdown | **正好 2 份**：`san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md`、`san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md` —— 与方案同句的「2 份补充 Markdown」吻合，但它们是**既有 pack 内的补充文件**（liuren-zhiyin 与 qimen-dunjia-tongzhi 都在 34「已存影印」桶内），属**文件级**，不是包级 |
| catalog 中类别字段独特的 pack | `qimen-faqiao`（唯一 `source_layer=primary`＋唯一 `ancient_text_public_domain_with_mit_transcription_provenance`＋唯一 `verified_excerpt_distributed`＋唯一 `fixed_commit_hash_and_scan_crosscheck`）；`feixing-ziwei-doushu-yuanzhi`（唯一 `commentary_or_late_observation`）。但二者分属不同桶（qimen-faqiao 在 16 内、feixing 在 34 内），**推不出「14＋2」** |

故：**34＋5＋16＝55** 是包级、脚本实算、可复现；**34＋5＋14＋2＝55** 把「2 份补充 Markdown（文件级）」当成两个 pack 一起加，属于层级混用，且其中的 14 是**旧计数**。账本已按 16 记账，本件与之一致。

## 5. 未确认影印底本 16 套（全量）

| # | system | slug | 书名 | `sources/facsimile/**` 命中 |
|---:|---|---|---|---:|
| 1 | bazi | `qiongtong-baojian` | 穷通宝鉴 | 0 |
| 2 | divination | `huangjin-ce` | 黄金策 | 0 |
| 3 | divination | `meihua-yishu` | 梅花易数 | 0 |
| 4 | divination | `zengshan-buyi` | 增删卜易 | 0 |
| 5 | fengshui | `qingnang-jing` | 青囊经 | 0 |
| 6 | fengshui | `rudi-yan-quanshu` | 入地眼全书 | 0 |
| 7 | fengshui | `shenshi-xuankong-xue` | 沈氏玄空学 | 0 |
| 8 | fengshui | `yangzhai-shishu` | 阳宅十书 | 0 |
| 9 | luming-nayin | `lantai-miaoxuan` | 兰台妙选 | 0 |
| 10 | physiognomy | `bingjian` | 冰鉴 | 0 |
| 11 | physiognomy | `shenxiang-quanbian` | 神相全编 | 0 |
| 12 | san-shi | `qimen-faqiao` | 奇门法窍（V5.1 核验摘录） | 0 |
| 13 | selection | `yuqia-ji` | 玉匣记 | 0 |
| 14 | xingming | `guotian-jing` | 果天经/果老星宗 | 0 |
| 15 | ziwei | `taiwei-fu` | 太微赋 | 0 |
| 16 | ziwei | `ziwei-doushu-quanshu` | 紫微斗数全书 | 0 |

计划文档 FATERADAR_FULL_LIBRARY_PLAN.md 与账本 A1 写「未确认底本 14 套」；磁盘实数（LIBRARY_INVENTORY.md，2026-09-12 脚本生成）为 **16 套**，且 34+5+16=55 正好等于 catalog ready 55，故以磁盘实数 16 为准；「14」少计 2 套，差在哪两套未查明（不猜），请 captain 裁定以哪一数为账本口径。

## 6. 复现

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
# 666 行／唯一 id／四栏非空 自检
python3 -c "import json;d=json.load(open('docs/closeout/evidence/a1-open-items-20260913.json',encoding='utf-8'));z=[i for i in d['items'] if i['id'].startswith('\u7e3d\u9210')];print(len(z),len({i['id'] for i in z}),sum(1 for i in z if any(not i.get(f) for f in ('what_is_missing','attempts','product_handling','locator'))))"
# 影印桶实算（应为 34/5/16 = 55）
python3 -c "import re,collections;t=open('docs/LIBRARY_INVENTORY.md',encoding='utf-8').read().splitlines();c=collections.Counter([l.strip('|').split('|')[-1].strip() for l in t if l.startswith('| ') and len(l.strip('|').split('|'))>=10 and l.strip('|').split('|')[0].strip()!='system']);print(dict(c))"
```
