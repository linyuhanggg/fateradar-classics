# A1 未决项逐条证据条目（《總鈐》666 残格抽样 ＋ 未确认影印底本全量）

日期：2026-09-13　执行：classics-audit（t20）　机器可读：`docs/closeout/evidence/a1-open-items-20260913.json`

> 本件是**最小可用版本**：666 残格先交 10 条抽样（不追求把 666 格搞清），未确认影印底本**全量列出**。
> 只新增 `docs/closeout/evidence/**`，**未改** `references/**`、`sources/**` 与账本；`verified`／`canonical_eligible` 保持 false。

## 计数（可复算）

| 项 | 数 |
|---|---:|
| 《總鈐》残格集合（draft＋待核实＋含「残格」） | 666 |
| 本件抽样条目 | 10（每 66 条取 1） |
| 未确认影印底本（全量） | 16 |
| **精确未决、不影响主要能力**（可作已披露限制） | **26** |
| **仍影响主要能力（须列 blocked）** | **0** |

口径：两类都「逐项可定位、有精确未决条件、有产品处理与解锁条件」，且都不阻塞八术主能力——666 残格只涉及大六壬《總鈐》表的逐格内容；未确认影印底本的文本按「待校参考」使用，本就不参与算法证据。

## 四栏（每条都有）

| 栏 | 内容 |
|---|---|
| 标识 | 666 残格＝电子本段落 ID（`daliuren-daquan:L####-L####`）＋内容首串＋神名；底本＝`system/slug（书名）`＋inventory 状态＋catalog 条目 |
| 缺什么 | 666：「列轴已可复原，但逐格内容归属不可判」（字粘连＋邻栏重叠）；底本：「无影印件、底本版本未确认」 |
| 已尝试的取证方法与结果 | 666：B2 溯源＋B4 实抓 SK1599＋t10 影印定位＋t7/t11 逐格转录＋ROUND6 更正；底本：inventory 脚本实数＋`sources/facsimile/**` 双路检索 0 命中＋catalog 与 source-editions 对照 |
| 产品处理＋解锁条件 | 两者一致：保持 draft／待校参考，**不入 executable、不猜字、不升 verified**；以「已披露限制」参与验收。解锁见各条 `product_handling` |

## 《總鈐》666 残格：现状一句话

影印**已在仓内**（`sources/facsimile/other/daliuren-daquan/liuren-daquan-juan1-siku-archive-06054168.pdf`，112 页；《總鈐》＝PDF p15 标题、十表连号 p16–p25），**「缺影印、无法定列」的旧阻塞理由已不成立**，666/666 条已追加更正 note；剩余缺口是**逐格内容归属**（印本字心距≈70px、字面宽≈100–110px，同列粘连、邻栏重叠），两半批逐格转录见 `sources/normalized/san-shi/daliuren-daquan/zongqian-cells-016-020.md`、`zongqian-cells-021-025.md`，版式普查见 `zongqian-layout-016-025.md`。**按方案「两次独立取证无新证据即登记精确未决、转做其他材料」，本条即该登记。**

抽样 10 条的标识：

- `daliuren-daquan:L1010-L1010`（内容首串：十二月辰：天煞、天空、死神、哭神、五墓、浴神、朱雀、螣蛇、月煞、迷惑、奸门）
- `daliuren-daquan:L1182-L1182`（内容首串：残格「卯乙五」）
- `daliuren-daquan:L1324-L1324`（内容首串：残格「亥申酉」）
- `daliuren-daquan:L1466-L1466`（内容首串：残格「丑午午亥丑卯」）
- `daliuren-daquan:L1608-L1608`（内容首串：残格「寅辰寅」）
- `daliuren-daquan:L1750-L1750`（内容首串：残格「戌子丑」）
- `daliuren-daquan:L1890-L1890`（内容首串：残格「子戌」）
- `daliuren-daquan:L2034-L2034`（内容首串：残格「戌丑午」）
- `daliuren-daquan:L2174-L2174`（内容首串：残格「丑寅卯巳未卯」）
- `daliuren-daquan:L2316-L2316`（内容首串：残格「寅戌」）

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

## 计数差异（请 captain 裁定）

计划文档 FATERADAR_FULL_LIBRARY_PLAN.md 与账本 A1 写「未确认底本 14 套」；磁盘实数（LIBRARY_INVENTORY.md，2026-09-12 脚本生成）为 **16 套**，且 34+5+16=55 正好等于 catalog ready 55，故以磁盘实数 16 为准；「14」少计 2 套，差在哪两套未查明（不猜），请 captain 裁定以哪一数为账本口径。

## 边界

- 本件不提升任何注解状态、不改任何数据文件、不改账本；不据数字本或期待值补字。
- 666 残格**不做全量逐条**（按方案：两次独立取证无新证据即登记精确未决）；如日后需要全量，可复用 B2 §1 的重算指令。
- 未确认影印底本的「解锁」需要**外部材料**（影印件或版本信息），本成员无法凭仓内材料推进；这是精确缺失条件，不是待办遗漏。

## 复现

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
# 666 集合重算（B2 §1 同式）
python3 - <<'PY'
import json
ann=json.load(open('references/annotations/san-shi/daliuren-daquan.json',encoding='utf-8'))
S=[e for e in ann['entries'] if e.get('review')!='source-reviewed' and e.get('kind')=='待核实' and '残格' in json.dumps(e,ensure_ascii=False)]
print(len(S))
PY
# 未确认影印底本清单（inventory 实数列）
grep -n '尚未确认影印' docs/LIBRARY_INVENTORY.md | wc -l
```
