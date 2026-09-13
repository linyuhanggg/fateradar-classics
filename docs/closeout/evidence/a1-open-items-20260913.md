# A1 未决项逐条证据条目（《總鈐》666 残格全量 ＋ 未确认影印底本全量）

日期：2026-09-13（2026-09-13 二次提交：總鈐部分由 10 条抽样扩为**全量 666 条**）　执行：classics-audit（t20）
机器可读：`docs/closeout/evidence/a1-open-items-20260913.json`

> 只新增 `docs/closeout/evidence/**`，**未改** `references/**`、`sources/**` 与账本；`verified`／`canonical_eligible` 保持 false。
> 666 条为**机械展开**：四栏（`what_is_missing`／`attempts`／`product_handling`／`locator`）按已定类级口径同构填充，**没有**为 656 条重做取证；`locator` 逐条唯一（段落 ID＋内容首串＋神名）。

## 计数

| 项 | 数 |
|---|---:|
| 《總鈐》残格集合（draft＋待核实＋含「残格」） | 666 |
| 《總鈐》逐条条目（本件） | **666**（全量，非抽样） |
| 未确认影印底本（全量） | 16 |
| 文件内条目合计 | **682** |
| **精确未决、不影响主要能力**（可作已披露限制） | **682** |
| **仍影响主要能力（须列 blocked）** | **0** |

## 自检（脚本断言，可复跑）

| 检查 | 结果 |
|---|---|
| 總鈐条目数 = 666 | 通过（666） |
| id 无重复 | 通过（unique 666） |
| 四栏均非空 | 通过（empty = 0） |
| class 一致 | 通过（666 条全为 `precise-undecided-not-blocking`） |
| 段落范围 | L1010–L2468（与 B2 报告一致） |

## 四栏口径（666 条同构、逐字一致）

| 栏 | 内容 |
|---|---|
| `what_is_missing` | **影印在仓、逐格归属不可判**（旧记「缺影印件」已推翻）：四庫本卷一影印在仓内（112 页，sha256 7790f774…；《總鈐》＝PDF p15 标题、十表连号 p16–p25，另有逐格转录件 `zongqian-cells-016-020／021-025`）；仍未决的是**逐格内容归属**——字心距≈70px、字面宽≈100–110px，同列粘连成 200–250px 墨条、邻栏 x 重叠 → 「某处有哪些字」可读、「该字属哪一格」不可判 |
| `attempts` | B2 溯源（集合识别与重算指令）／B4 实抓识典 SK1599 比对／t10 影印定位（p15 标题、p16–p25 十表）／t7·t11 版式普查与逐格转录两半批／ROUND6 §3 的 666/666 更正 note |
| `product_handling` | 保留〔?〕、**不入规则**：保持 draft（kind=待核实），不入 `references/executable`、不进算法、不猜字、不补格、不连成月日全表、**不升 verified**；只作「已披露限制」参与验收。**解锁条件＝取得可判归属的清晰影印或平行本**，再由独立复核把已定格升 `passage-reviewed` |
| `locator` | `paragraphId`（`daliuren-daquan:L####-L####`）＋`content_lead`（该条内容首串）＋`terms`（神名，前 8）＋`kind`＋`review` |

## 子群检查（是否存在「其实可判」的不同类别）

对 666 条做了内容类型与自述状态扫描：

| 子群 | 条数 | 说明 |
|---|---:|---|
| 十表·格内残字型（`残格「X」。在…标目下…`） | 664 | 例：`daliuren-daquan:L1044-L1044`「残格「申」。在甲巳甲午甲未甲申标目下。所属日与课传位次信息不足，待核，不补三传、不改正文」 |
| 月表·神名串型（`十二月X：神名…`） | 2 | `L1010`（十二月辰）、`L1038`（十二月亥）；同为待核，无更优判据 |
| 自述「归属已定／已定格／已可定列」 | **0** | 无一条声称归属已解决 → **不存在可单独升级的子群** |

因此 666 条**一律同类别**（`precise-undecided-not-blocking`）；上面两个子群只是内容形态不同，**不改变类别**。
（另：`kind`／`review` 全部为 待核实／draft；含 note 的条目 666/666；无 note 的 0 条。）

## 未确认影印底本：16 套全量

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

## 计数差异（已按磁盘实数记账）

计划文档 FATERADAR_FULL_LIBRARY_PLAN.md 与账本 A1 写「未确认底本 14 套」；磁盘实数（LIBRARY_INVENTORY.md，2026-09-12 脚本生成）为 **16 套**，且 34+5+16=55 正好等于 catalog ready 55，故以磁盘实数 16 为准；「14」少计 2 套，差在哪两套未查明（不猜），请 captain 裁定以哪一数为账本口径。

## 复现

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
python3 - <<'PY'
import json
d=json.load(open('docs/closeout/evidence/a1-open-items-20260913.json',encoding='utf-8'))
zq=[i for i in d['items'] if i['id'].startswith('總鈐')]
print(len(zq), len({i['id'] for i in zq}), sum(1 for i in zq if any(not i.get(f) for f in ('what_is_missing','attempts','product_handling','locator'))))
PY
```
