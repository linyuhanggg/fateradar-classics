# Codex 验收交接 · 古籍仓

## 1. 工作树、分支、提交

- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library`
- 分支：`codex/grok-full-library`
- 基准：`origin/main` @ `49d3efe`（data: complete oversize facsimile release）
- 施工时未改 `/Users/sync/code/fateradar-classics` 主工作区，也未覆盖其他工作树
- 最终提交：`15904af35d83bba0a961f267a6b2cf72e86480d3`
- 推送：仅推自己的 `codex/grok-full-library`，不合 main、不强推

## 2. 对照总方案的完成与未完成

已完成：

- 全库真实盘点：catalog 55 包、磁盘 55 包、全文 54、排除 4
- 稳定段落 ID：`slug:Lxxxx-Lyyyy`
- 去向：engine 21 / knowledge 33 / excluded_copyright 1（《奇门法窍》）
- 可执行规则 ZPR-E-01..17 与 QTB-E-01（穷通调候透藏），全部 `verified: false`
- 知识库检索索引：`references/inventory/knowledge-index.json`（33 包）与 `docs/KNOWLEDGE_SEARCH_INTERFACE.md`
- 疑文段保留，不猜字进原文

未完成：

- 没有把 54 部全文都抽成可执行规则（禁止批量空 JSON）
- 旧 `rules.yaml` 1356 条仍是候选
- 知识库没有产品检索页（只提供索引和接口）
- 本仓没有规则解释器；产品仓实现等价条件
- 浏览器页面验收未做（本仓无页面）

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
| 本轮可执行规则 | 18 |
| 知识库包 | 33 |

清单位置：

- `docs/LIBRARY_INVENTORY.md`
- `references/inventory/library-inventory.json`
- `references/inventory/knowledge-index.json`
- `references/inventory/paragraphs/{system}/{slug}.json`
- `references/executable/schema.md`
- `references/executable/ziping-zhenquan.json`
- `docs/KNOWLEDGE_SEARCH_INTERFACE.md`

55 是资料包口径。`qimen-faqiao` 无全文、去向 `excluded_copyright`。

## 4. 修改文件与行为变化

- `references/executable/ziping-zhenquan.json`：ZPR-E-01..17
- `references/executable/qiongtong-baojian.json`：QTB-E-01 调候透藏
- `tools/build-library-inventory.py`：可执行规则数从 JSON 实数统计
- `tools/build-knowledge-index.py`：知识库检索索引
- 不改 `sources/` 原文

## 5. 复现命令与检查结果

```bash
cd /Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library
python3 tools/build-library-inventory.py
python3 tools/build-knowledge-index.py
python3 -c "import json; d=json.load(open('references/inventory/library-inventory.json')); k=json.load(open('references/inventory/knowledge-index.json')); print(d['counts']); print('knowledge', k['pack_count'])"
```

实际结果（2026-09-08）：

```
catalog_ready_packs 55, fulltext_files 54, paragraphs 53640,
executable_rules_in_this_commit 18, knowledge packs 33
faqiao destination=excluded_copyright
```

## 6. 代表性案例

《子平真诠》`ziping-zhenquan:L0398-L0399` 透印以解；`L1116` 金水伤官可见官；`L0363-L0401` 无刑冲破害；`L0401` 刑冲而会合以解之。

产品仓 `analyzeGeju` 实现这些条件。本仓 JSON 不被引擎 import。

## 7. Web 字段映射

- 段落 ID → 引文定位
- `page`: geju / yongshen
- 知识库：`docs/KNOWLEDGE_SEARCH_INTERFACE.md`
- 预览地址：无
- 浏览器验收：未做

## 8. 争议、假设、风险

- 透干优先否则本气：实现假设
- 金水按日主五行
- 六破用通行表
- 会合解救要求合会支在刑冲组外；半合半会为信息不足；破害不套用
- 会合解刑冲已实现组外合会；破害不套会合，标信息不足；财印位置与力量未论，故成格/破格不得确定
- 14 套影印 `not_confirmed`，疑文 1261 段未校勘

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
