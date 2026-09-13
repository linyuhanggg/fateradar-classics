# 古籍专项验收报告（2026-09-14 修订；供全项目总负责人汇总）

日期：2026-09-14  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
仓：`linyuhanggg/fateradar-classics`  
分支：`dsh/full-library-classics`  
本文件**不是**全项目八项验收完成声明，只覆盖古籍加工与数据交付。  
**本文件取代** 2026-09-13 仍写「奇门 308–311 读图授权阻塞」「總鈐 666」的完成口径。

## 1. 结论

已知复验退回的两项已施工：

1. 奇门 PDF 308–311：按「小字在时支左侧、跨页最右＝前页最左续文」重配归属，写入 `nlc-layouts.md`、批次稿、page-reviews。`verified` / `canonical_eligible` 仍 false。
2. 1192 分型：L1010／L1038 从总钤残格移出（664+2）；39 图像与 25 语义已逐项尝试，能改电子分段的 3 条已改类，其余保持 draft。

结构校验已通过（见 §2）。奇门 308–311 归属三份独立读图 pass；漏字／串次经独立复验 pass。1192 分型独立审核 pass（416/664/54/19/39）。  
不宣称算法、Web 或全项目完成。

## 2. 基线（本工作树实测）

| 项 | 值 |
|---|---|
| 注解 | 62,839 条 / 79 文件 / 53 书 |
| `source-reviewed` | **60,108** |
| `draft` | **2,731** |
| `verified=true` | **0** |
| 分账 | 台账元数据 1,531 / 实质待审 1,192 / 待转写 1 / 归档 7 |
| 实质待审分型（t30） | 664 總鈐残格 / 416 真疑字 / 54 电子分段 / 39 图像 / 19 残联 |
| 可执行规则 | 258 条 / 15 文件；`named_gaps` 42 |
| 父 SHA | `e90da1abd98fb3e71dfe3210500305d05ba19940` |

```
python3 tools/validate-annotations.py --json
python3 tools/validate-executable.py --json
```

2026-09-14 实测：annotations ok、62839、60108、0 errors；executable ok、258、named_gaps 42、0 errors。校验器只做结构与源 ID，不认证语义。

## 3. 正式数据入口

| 入口 | 路径 |
|---|---|
| 注解 | `references/annotations/**` |
| 规则定义 | `references/executable/*.json` |
| 原书案例 | `references/cases/source-cases.json`（本专项未改导出器） |
| 奇门 308–311 转写 | `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md`；批次 `ocr-batch-cell-level-0308-0311.md` |
| 列归属映射 | `docs/closeout/evidence/qimen-308-311-column-map-20260914.md` |
| draft 分账 | `docs/closeout/review/a1-draft-disposition-20260913.json` |
| 未决 | `docs/closeout/evidence/a1-open-items-20260913.json`（664 总钤 + 2 神煞疑字 + 16 底本） |
| 分型 | `docs/closeout/evidence/t30-pending-typed-disposition-20260914.json` |
| 给算法 | `docs/closeout/CLASSICS-DATA-CHANGE-FOR-ALGO-20260913.md` |

## 4. 未决（不笼统「待处理」）

| 类 | 规模 | 产品处理 | 解锁条件 |
|---|---|---|---|
| 《總鈐》残格 | **664**（L1040 起） | 保持 draft，不入 executable | 可判「字→格」的清晰影印或平行本 |
| 十二月神煞疑字 | **2**（L1010 浴神、L1038 灾神） | 保持 draft；**不是**总钤残格 | 神煞名平行本或可核印本 |
| 大六壬其余实质待审 | 86 | 保持 draft | 影印或可唯一还原的平行句 |
| 奇门 NLC 台账 | 1,261 ledger-metadata | 不提升 | 随影印转写状态变化 |
| 奇门 308–311 | 4 页已转写并修订归属 | 可作转写证据；`canonical_eligible=false` | 独立读图复核通过后仍不自动升 verified |
| 麻衣识典图 | 39 | 保持 draft | 本版图文件落地或页图映射后再读图 |
| 命理约言封面缺字 | 1 | 不得据电子本代填 | 题名「命」「約」之间纸面留白，已照录 |
| 其余实质待审 | 见 t30 | 已具名；不批量升级 | 各条 notes |
| unimplemented | `named_gaps` 42 | **算法任务** | 见 executable |
| 未确认影印底本 | 16 套 | 磁盘 0 命中 | 取得合法影印 |

## 5. 本专项不做 / 未做

- 不改产品仓、不改 `/Users/sync/code/**`
- 不跑 `export-source-cases.py`（避免覆盖手工案例）
- 不更新产品 pin
- 不把 `source-reviewed` 写成影印 `verified`
- 不把 300–307 旧批次半读稿当成 308–311 同类已修

## 6. 校验与合入

独立复核：`docs/closeout/review/INDEPENDENT-REVIEW-QIMEN-308-311-20260914.md`、`docs/closeout/review/INDEPENDENT-REVIEW-T30-20260914.md`。**不以** T29／CLASSICS-SPECIAL 旧 PASS 代替本轮。

合入后核对远端 SHA 与 `validate-rules` CI。
