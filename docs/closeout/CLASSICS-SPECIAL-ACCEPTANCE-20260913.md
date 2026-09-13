# 古籍专项验收报告（供全项目总负责人汇总）

日期：2026-09-13  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
仓：`linyuhanggg/fateradar-classics`  
分支：`dsh/full-library-classics` = `main`（快进合入）  
本文件**不是**全项目八项验收完成声明，只覆盖古籍加工与数据交付。

## 1. 结论

古籍专项在「不要求疑字清零、不编写产品算法」的口径下，**可交付**：现有资料均有可定位去向；已完成加工已入库；必要校验与独立复核已通过并合入 main。  
真正未决已逐项留证。外部阻塞（奇门 308–311 读图授权）保留，最小解锁条件见 §4。  
不宣称算法、Web 或全项目完成。产品 pin 由算法/Web 任务更新。

## 2. 基线（本工作树实测，非转抄旧账本）

| 项 | 值 |
|---|---|
| 注解 | 62,839 条 / 79 文件 / 53 书 |
| `source-reviewed` | **60,108** |
| `draft` | **2,731** |
| `verified=true` | **0** |
| 分账 | 台账元数据 1,531 / 实质待审 1,192 / 待转写 1 / 归档 7 |
| 实质待审具名覆盖 | **1,192 / 1,192**（notes 或 vernacular 含未决/残/疑/截/阙/图像/批次登记） |
| 可执行规则 | 258 条 / 15 文件；救应 self 117 / none 106 / unimplemented 30 / 交叉 5；`named_gaps` 42 |
| 本 Goal 批次 | t24 +8、t25 +28、t26 +38、t27 +21 记录性锚点（均 `verified=false`） |
| 父 SHA | `d01ea097e332d691ea3f48967fbf30e997ca9c07` |

复现：

```
python3 tools/validate-annotations.py --json
python3 tools/validate-executable.py --json
```

应分别为 annotations ok、62839、60108、0 errors；executable ok、258、named_gaps 42、0 errors。

## 3. 正式数据入口

| 入口 | 路径 |
|---|---|
| 注解 | `references/annotations/**` |
| 规则定义 | `references/executable/*.json`（schema：`references/executable/schema.md`） |
| 原书案例 | `references/cases/source-cases.json`（本专项未改导出器） |
| draft 逐条分账 | `docs/closeout/review/a1-draft-disposition-20260913.json` |
| 《總鈐》666 + 未确认底本 16 | `docs/closeout/evidence/a1-open-items-20260913.json` |
| 未决压缩清单 | `docs/closeout/CLASSICS-OPEN-ITEMS-20260913.md` |
| 给算法的版本说明 | `docs/closeout/CLASSICS-DATA-CHANGE-FOR-ALGO-20260913.md` |

## 4. 未决（不笼统「待处理」）

| 类 | 规模 | 产品处理 | 解锁条件 |
|---|---|---|---|
| 《總鈐》残格 | 666 | 保持 draft，不入 executable | 可判归属的清晰影印或平行本 |
| 大六壬其余实质待审 | 86（含 t23b2 规则候选 58） | 保持 draft | 影印或可唯一还原的平行句 |
| 奇门 NLC 台账 | 1,261 ledger-metadata | 不提升、不入审读队列 | 随影印转写状态变化 |
| 奇门 308–311 逐格 OCR | 4 页 | 未转写、`canonical_eligible=false` | 用户授权 modlens reuse 或明示允许用已登录 Codex 读这 4 页 |
| 命理约言 OCR 待转写 | 1 | 不得据电子本代填 | 页审完成 |
| 其余实质待审 | 见分账 14 文件 | 已具名；不批量升级 | 各条 notes 中的解锁条件 |
| unimplemented 22 条实现缺口 | 规则 JSON 已 `named_gaps` | **算法任务**，本专项不写代码 | 见 executable `named_gaps` |
| 未确认影印底本 | 16 套 | 磁盘 `sources/facsimile` 0 命中 | 取得合法影印 |

## 5. 本专项不做 / 未做

- 不改产品仓、不改 `/Users/sync/code/**`
- 不跑 `export-source-cases.py`（避免覆盖手工案例）
- 不更新产品 pin
- 不把 `source-reviewed` 写成影印 `verified`
- 页面引文回读属 A2/产品侧

## 6. 校验与合入

独立复核：`docs/closeout/review/INDEPENDENT-REVIEW-CLASSICS-SPECIAL-20260913.md` → **PASS**（数字与校验器一致）。

合入后核对远端 SHA 与 `validate-rules` CI。
