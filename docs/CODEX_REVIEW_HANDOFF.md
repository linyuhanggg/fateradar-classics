# Codex 验收交接 · 古籍仓

## 1. 工作树、分支、提交

- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library`
- 分支：`codex/grok-full-library`
- 基准：`origin/main` @ `49d3efe`（data: complete oversize facsimile release）
- 施工时未改 `/Users/sync/code/fateradar-classics` 主工作区，也未覆盖其他工作树
- 最终提交：`38941f955ab1e5c523a90875b1e7769c4c76a5f8`
- 推送：仅推自己的 `codex/grok-full-library`，不合 main、不强推

## 2. 对照总方案的完成与未完成

已完成：

- 全库真实盘点：catalog 55 包、磁盘 55 包、全文 54、排除 4
- 稳定段落 ID：`slug:Lxxxx-Lyyyy`
- 去向：engine 21 / knowledge 33 / excluded_copyright 1（《奇门法窍》）
- 可执行规则 58 条，全部 `verified: false`
  - 八字：ZPR-E-01..17、QTB-E-01、SMTH-E-01 天乙落柱、SMTH-E-02 驿马落柱、SMTH-E-03 咸池桃花落柱、SMTH-E-04 华盖落柱、SMTH-E-05 将星落柱、SMTH-E-06 孤辰落柱、SMTH-E-07 寡宿落柱、SMTH-E-08 劫煞落柱、SMTH-E-09 亡神落柱、SMTH-E-10 灾煞落柱、SMTH-E-11 天喜来源分条、SMTH-E-12 金舆落柱、SMTH-E-13 羊刃落柱、SMTH-E-14 飞刃落柱、SMTH-E-15 禄神落柱、SMTH-E-16 天德落柱、SMTH-E-17 月德落柱、SMTH-E-18 文昌来源分条、SMTH-E-19 学堂来源分条、SMTH-E-20 太极落柱、SFTK-E-01 流霞落柱、SFTK-E-02 红艳落柱
  - 紫微：ZWD-E-01 生年干四化落宫
  - 六爻：ZSB-E-01 用神旬空、ZSB-E-02 用神月破
  - 梅花：MHY-E-01 体用生克方向
  - 奇门：QMD-E-01 伏吟、QMD-E-02 反吟
  - 六壬：DLD-E-01..09 九宗门取传（贼克、比用、涉害、遥克、昴星、别责、八专、伏吟、返吟）
  - 七政：XXDC-E-01 命宫来源分条、XXDC-E-02 庙旺来源分条、XXDC-E-03 日月落宫定位
- 知识库检索索引：`references/inventory/knowledge-index.json`（33 包）与 `docs/KNOWLEDGE_SEARCH_INTERFACE.md`
- 疑文段保留，不猜字进原文

未完成：

- 没有把 54 部全文都抽成可执行规则（禁止批量空 JSON）
- 旧 `rules.yaml` 1356 条仍是候选
- 知识库没有产品检索页（只提供索引和接口）
- 本仓没有规则解释器；产品仓实现等价条件
- 浏览器页面验收未做（本仓无页面）
- 七政五星宿度旺宫、戌方入庙未按原文逐步程序接入运行；只与现行黄道本宫分条
- 神煞除已接入落柱的条目外仍有名单未抽；天喜未按四季覆盖；阴干羊刃未按子平无刃覆盖；文昌学堂只分条未改表；戊己太极未补申；流霞未按星学大成辛逐虎覆盖；红艳甲乙未补申；国印未把三命天印并入；天医月支前一位与择日正月戌、六壬月建前二不是同一套

## 3. 全库真实统计

由 `python3 tools/build-library-inventory.py` 生成：

| 口径 | 数量 |
|---|---:|
| catalog ready 资料包 | 55 |
| 磁盘 `references/books/*/*` | 55 |
| `sources/fulltext/**/fulltext.md` | 54 |
| catalog 排除项 | 4 |
| 稳定段落 | 53640 |
| 其中疑文段 | 1261 |
| 旧 rules.yaml 候选 | 1356，verified=0 |
| 本轮可执行规则 | 58 |
| 知识库包 | 33 |

清单位置：

- `docs/LIBRARY_INVENTORY.md`
- `references/inventory/library-inventory.json`
- `references/inventory/knowledge-index.json`
- `references/inventory/paragraphs/{system}/{slug}.json`
- `references/executable/schema.md`
- `references/executable/ziping-zhenquan.json`
- `references/executable/ziwei-doushu-quanshu.json`
- `references/executable/zengshan-buyi.json`
- `references/executable/meihua-yishu.json`
- `references/executable/qimen-dunjia-tongzhi.json`
- `references/executable/daliuren-daquan.json`
- `references/executable/xingxue-dacheng.json`
- `references/executable/sanming-tonghui.json`
- `references/executable/shenfeng-tongkao.json`
- `docs/KNOWLEDGE_SEARCH_INTERFACE.md`

55 是资料包口径。`qimen-faqiao` 无全文、去向 `excluded_copyright`。

## 4. 修改文件与行为变化

- `references/executable/ziwei-doushu-quanshu.json`：ZWD-E-01
- `references/executable/zengshan-buyi.json`：ZSB-E-01、ZSB-E-02
- `references/executable/meihua-yishu.json`：MHY-E-01
- `references/executable/qimen-dunjia-tongzhi.json`：QMD-E-01、QMD-E-02
- `references/executable/daliuren-daquan.json`：DLD-E-01..09
- `references/executable/xingxue-dacheng.json`：XXDC-E-01、XXDC-E-02、XXDC-E-03
- `references/executable/sanming-tonghui.json`
- `references/executable/shenfeng-tongkao.json`：SMTH-E-01..20
- `references/executable/shenfeng-tongkao.json`：SFTK-E-01、SFTK-E-02
- 盘点脚本重跑，可执行规则 56→58
- 不改 `sources/` 原文

## 5. 复现命令与检查结果

```bash
cd /Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library
python3 tools/build-library-inventory.py
python3 -c "import json; d=json.load(open('references/inventory/library-inventory.json')); print(d['counts'])"
```

实际结果（2026-09-08）：

```
catalog_ready_packs 55, fulltext_files 54, paragraphs 53640,
executable_rules_in_this_commit 58, knowledge packs 33
verified_rules 0
faqiao destination=excluded_copyright
```

## 6. 代表性案例

《紫微斗数全书》`ziwei-doushu-quanshu:L1770-L1776`：甲生人廉贞化禄、破军化权、武曲化科、太阳化忌。

《增删卜易》`zengshan-buyi:L0539-L0539`：用神旺相而遇旬空，出空之日则出矣。`L0373-L0377`：目下虽破，出月则不破。

《梅花易数》`meihua-yishu:L1239-L1239`：用克体不宜，体克用则吉；只记方向，不投票。

《奇门遁甲统宗》`qimen-dunjia-tongzhi:L0309-L0311`：伏吟本星加本宫，反吟星加对宫。歌诀「最凶」不进入运行结论。

《大六壬大全》`daliuren-daquan:L0064-L0066`：一下克上曰重审，一上克下曰元首。课名只说明取传。
`L0092-L0094` 伏吟、`L0096-L0098` 返吟、`L0076-L0078` 蒿矢弹射、`L0068-L0070` 比用、`L0080-L0082` 昴星、`L0084-L0086` 别责、`L0088-L0090` 八专：只记取传，不是近处、失脱、外助、出奇、已经停住或已经反复。

《星学大成》`xingxue-dacheng:L0075-L0075`：卯上分明是命宫。与本盘上升点分条。
`L0187-L0189` 星辰本宫为庙堂；`L0184-L0185` 白羊金牛与娄胃宿度旺宫；`L0201` 日月戌方云入庙。三套与现行黄道本宫/对宫不是同一程序，入庙不是已经得福。

《三命通会》`sanming-tonghui:L1391-L1400`：天乙落柱；歌诀泥而不通，不得输出吉神断语。
`L1466` 文昌甲蛇乙猪与本盘通行表分条、`L1471-L1474` 纳音学堂与本盘日干长生分条、`L1461-L1465` 太极贵人：只记落柱，不是科名或学业。戊己喜申未覆盖。
《神峰通考》`shenfeng-tongkao:L2545-L2546` 流霞、`L2550` 红艳：只记落柱，不是死丧或情欲。辛逐虎、甲乙申未覆盖。

## 7. Web 字段映射

- 段落 ID → 引文定位
- `page`: geju / yongshen / ziwei / liuyao / meihua / qimen
- 知识库：`docs/KNOWLEDGE_SEARCH_INTERFACE.md`
- 预览地址：无
- 浏览器验收：未做

## 8. 争议、假设、风险

- 紫微本命四化按斗数年干，不按节气年干覆盖安星
- 六爻旬空按日干取旬；月破按地支六冲
- 梅花动爻所在卦为用
- 奇门伏吟按值符归本位，不采用「伏吟为最凶」
- 七政入庙用热带黄道本宫，不按娄胃亢斗翼室鬼宿度或戌方入庙覆盖
- 华盖将星只按年支三合库土/中位，不按日支、空破、亡神夹贵改写
- 孤辰寡宿只按年支三方进退，不按隔角、惆怅或贵格包裹改写
- 劫煞亡神灾煞只按年支三合绝处、临官、冲将星，不按十六般或福神相助改写
- 天喜本盘按年支三合，不按春戌夏丑秋辰冬未覆盖
- 金舆按日干禄前二辰，不按马前二辰覆盖
- 羊刃按日干禄前一辰，十干都标；不按子平五阴干无刃覆盖
- 飞刃按羊刃对冲；禄神按日干临官支
- 天德按月支正月丁二月申等，柱干或柱支命中即标；月将伤破未论
- 月德按月支三合丙壬庚甲；德合伤破未论
- 文昌本盘按通行表，不按甲蛇乙猪覆盖
- 学堂本盘按日干长生，不按纳音长生同类覆盖
- 太极按甲乙子午、丙丁卯酉、庚辛寅亥、壬癸巳申、戊己辰戌丑未；不把戊己申补进表
- 流霞按日干甲酉乙戌丙未丁申戊巳己午庚辰辛卯壬亥癸寅；不按星学大成辛逐虎覆盖
- 红艳按日干甲午乙午丙寅丁未戊辰己辰庚戌辛酉壬子癸申；不把甲乙申补进表
- 14 套影印 `not_confirmed`，疑文 1261 段未校勘
- 成格/破格力量未论，不得确定

## 9. 版本对应

- 古籍原文：本工作树 `49d3efe` 上的 `sources/fulltext`
- 派生清单与规则：本分支
- 产品代码：`fateradar-product-grok-full-library` 的 `codex/grok-full-library`

## 10. 边界确认

- 未改他人未提交工作
- 未把任何规则 `verified` 改为 true
- 未刷新 golden
- 未合 main、未部署、未改生产库、未购买服务
- 未抓取《奇门法窍》
