# Codex 验收交接 · 古籍仓

## 1. 工作树、分支、提交

- 工作树：`/Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library`
- 分支：`codex/grok-full-library`
- 基准：`origin/main` @ `49d3efe`（data: complete oversize facsimile release）
- 施工时未改 `/Users/sync/code/fateradar-classics` 主工作区，也未覆盖其他工作树
- 最终提交：见本分支最新 commit（提交后填写）
- 推送：仅推自己的 `codex/grok-full-library`，不合 main、不强推

## 2. 对照总方案的完成与未完成

已完成：

- 全库真实盘点：catalog 55 包、磁盘 55 包、全文 54、排除 4
- 稳定段落 ID：`slug:Lxxxx-Lyyyy`，映射到 `sources/fulltext/.../fulltext.md` 行号
- 去向：engine 21 / knowledge 33 / excluded_copyright 1（《奇门法窍》）
- 可执行规则格式 + 《子平真诠》首条通路 4 条，全部 `verified: false`
- 疑文段保留，不猜字进原文

未完成：

- 没有把 54 部全文都抽成可执行规则（禁止批量空 JSON）
- 旧 `rules.yaml` 1356 条仍是候选，未接入运行时
- 风水/相法/择日/姓名只有清单去向，没有产品检索页
- 本仓没有规则解释器；产品仓引擎实现等价条件，不读这份 JSON
- 浏览器页面验收未做（本仓无页面）

## 3. 全库真实统计

由 `python3 tools/build-library-inventory.py` 生成：

| 口径 | 数量 |
|---|---:|
| catalog ready 资料包 | 55 |
| 磁盘 `references/books/*/*` | 55 |
| `sources/fulltext/**/fulltext.md` | 54 |
| catalog 排除项 | 4（含斗数关键、七政四余天经、七政全书大成、命海全编） |
| 稳定段落 | 53640 |
| 其中疑文段 | 1261 |
| 旧 rules.yaml 候选 | 1356，verified=0 |
| 本轮可执行规则 | 4 |
| 段落种类 | 理论 53107、评注或元数据 146、序跋目录 314、操作步骤 66、案例 7 |

清单位置：

- `docs/LIBRARY_INVENTORY.md`
- `references/inventory/library-inventory.json`
- `references/inventory/paragraphs/{system}/{slug}.json`
- `references/executable/schema.md`
- `references/executable/ziping-zhenquan.json`

55 是资料包口径，不是 55 部独立完整古籍。`qimen-faqiao` 无全文、去向 `excluded_copyright`。

## 4. 修改文件与行为变化

新增：

- `tools/build-library-inventory.py`
- `docs/LIBRARY_INVENTORY.md`
- `docs/FATERADAR_FULL_LIBRARY_PLAN.md`（从 reading 工作树拷入，远端 main 原先没有）
- `references/inventory/**`
- `references/executable/**`

行为：只派生清单和规则定义，不改 `sources/` 原文。可执行规则不是运行时加载器。

## 5. 复现命令与检查结果

```bash
cd /Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library
python3 tools/build-library-inventory.py
python3 -c "import json; d=json.load(open('references/inventory/library-inventory.json')); print(d['counts'])"
```

实际结果（2026-09-08 独立复核）：

```
catalog_ready_packs 55, disk_packs 55, fulltext_files 54, paragraphs 53640,
verified_rules 0, executable_rules_in_this_commit 4
faqiao destination=excluded_copyright
```

环境：系统 Python 3，无额外依赖。未跑付费 API。

## 6. 代表性案例

《子平真诠》`ziping-zhenquan:L0328-L0328` 月令取格、`L0361-L0399` 成败救应、`L0373-L0399` 伤官见官。

规则 ZPR-E-01..04：

- 满足：已取月令藏干并记录透藏
- 不满足：四柱天干藏干均无该干扰十神
- 信息不足：仅藏干、或救应未实现
- 救应：`unimplemented`
- verified：false

产品仓用这些条件改了 `analyzeGeju`，本仓 JSON 不被引擎 import。

## 7. Web 字段映射

本仓不跑页面。产品消费字段：

- 段落 ID → 引文定位
- `page`: geju / yongshen
- `vernacular` 模板由产品 `buildBaziFreeReading` 按本盘事实组装
- 预览地址：无
- 浏览器验收：未做

## 8. 争议、假设、风险

- 透干优先、否则本气，是实现假设，不是原文逐字程序
- 建禄/月劫另取用神尚未做成可执行分支
- 金水伤官见官例外未实现
- 刑冲破害、救应未实现，故成格/破格不得确定
- 旧 CLASSICS_STATUS.md 仍写 1357，以本清单 1356 为准
- 14 套影印 `not_confirmed`，疑文 1261 段未校勘

## 9. 版本对应

- 古籍原文：本工作树 `49d3efe` 上的 `sources/fulltext`
- 派生清单：本分支提交
- 产品代码：`fateradar-product-grok-full-library` 的 `codex/grok-full-library`

## 10. 边界确认

- 未改他人未提交工作
- 未把任何规则 `verified` 改为 true
- 未刷新 golden
- 未合 main、未部署、未改生产库、未购买服务
- 未抓取《奇门法窍》
