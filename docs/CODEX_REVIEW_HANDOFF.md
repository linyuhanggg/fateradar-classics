# Codex 验收交接 · 古籍仓

## 1. 工作树、分支、提交

- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library`
- 分支：`codex/grok-full-library`
- 基准：`origin/main` @ `49d3efe`（data: complete oversize facsimile release）
- 施工时未改 `/Users/sync/code/fateradar-classics` 主工作区，也未覆盖其他工作树
- 最终提交：`b107154ca1d28db79fd5e0c6cf8e40e98d7c57f9`
- 推送：仅推自己的 `codex/grok-full-library`，不合 main、不强推

## 2. 对照总方案的完成与未完成

已完成：

- 全库真实盘点：catalog 55 包、磁盘 55 包、全文 54、排除 4
- 稳定段落 ID：`slug:Lxxxx-Lyyyy`
- 去向：engine 21 / knowledge 33 / excluded_copyright 1（《奇门法窍》）
- 可执行规则 24 条，全部 `verified: false`
  - 八字：ZPR-E-01..17、QTB-E-01
  - 紫微：ZWD-E-01 生年干四化落宫
  - 六爻：ZSB-E-01 用神旬空、ZSB-E-02 用神月破
  - 梅花：MHY-E-01 体用生克方向
  - 奇门：QMD-E-01 伏吟、QMD-E-02 反吟
- 知识库检索索引：`references/inventory/knowledge-index.json`（33 包）与 `docs/KNOWLEDGE_SEARCH_INTERFACE.md`
- 疑文段保留，不猜字进原文

未完成：

- 没有把 54 部全文都抽成可执行规则（禁止批量空 JSON）
- 旧 `rules.yaml` 1356 条仍是候选
- 知识库没有产品检索页（只提供索引和接口）
- 本仓没有规则解释器；产品仓实现等价条件
- 浏览器页面验收未做（本仓无页面）
- 六壬、七政、神煞逐步程序未抽可执行规则

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
| 本轮可执行规则 | 24 |
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
- `docs/KNOWLEDGE_SEARCH_INTERFACE.md`

55 是资料包口径。`qimen-faqiao` 无全文、去向 `excluded_copyright`。

## 4. 修改文件与行为变化

- `references/executable/ziwei-doushu-quanshu.json`：ZWD-E-01
- `references/executable/zengshan-buyi.json`：ZSB-E-01、ZSB-E-02
- `references/executable/meihua-yishu.json`：MHY-E-01
- `references/executable/qimen-dunjia-tongzhi.json`：QMD-E-01、QMD-E-02
- 盘点脚本重跑，可执行规则 18→24
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
executable_rules_in_this_commit 24, knowledge packs 33
verified_rules 0
faqiao destination=excluded_copyright
```

## 6. 代表性案例

《紫微斗数全书》`ziwei-doushu-quanshu:L1770-L1776`：甲生人廉贞化禄、破军化权、武曲化科、太阳化忌。

《增删卜易》`zengshan-buyi:L0539-L0539`：用神旺相而遇旬空，出空之日则出矣。`L0373-L0377`：目下虽破，出月则不破。

《梅花易数》`meihua-yishu:L1239-L1239`：用克体不宜，体克用则吉；只记方向，不投票。

《奇门遁甲统宗》`qimen-dunjia-tongzhi:L0309-L0311`：伏吟本星加本宫，反吟星加对宫。歌诀「最凶」不进入运行结论。

产品仓实现这些条件。本仓 JSON 不被引擎 import。

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
