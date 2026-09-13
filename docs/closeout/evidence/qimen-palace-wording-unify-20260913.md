# 奇门「原宫数」→「落宫数」措辞统一（上游来源 + 重跑验证）

日期：2026-09-13　执行：classics-audit　口径裁定：captain（批准统一，此前「只动案例元数据链」的最小口径作废）

对象：`starPalaceRaw`／`doorPalaceRaw` 这两个**印在逐时简表后两列的数字**。实测这些数字跟着**落宫**走（1,888／1,917 条与落宫一致，仅 376 条与原宫一致），故凡**描述这两个数字**的措辞一律改「落宫」；凡指「原宫」**概念本身**（值符本来所居之宫、与寄宫对照、口径句）**一律保留原样**。

## 1. 清单：逐文件待改处数与改后残留

| 文件 | 改前「原宫」 | 改动处数 | 改后残留 |
|---|---:|---:|---:|
| `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` | 267 | 266 | 1 |
| `references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json` | 1 | 0 | 1 |
| `references/annotations/san-shi/qimen-dunjia-tongzhi.json` | 3 | 0 | 3 |
| `references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` | 232 | 232 | 0 |
| `references/source-editions.json` | 1 | 1 | 0 |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/collation-notes.md` | 5 | 5 | 0 |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layout-page-reviews.json` | 45 | 45 | 0 |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md` | 45 | 45 | 0 |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/source-manifest.yaml` | 1 | 1 | 0 |
| `references/cases/source-cases.json`（生成物，由导出器重跑） | 1,220 | — | 2 |

合计上游改动 **595** 处（`qimen-component-candidates.json` 的 1 处为口径句，未改）。

### 每类改动的上下文（每类一行，代表全部同类改动）

| 文件 | 处数 | 上下文（改前 → 改后） |
|---|---:|---|
| `references/annotations/...--nlc-layouts.json` | 103 | "原宫数"（scope/terms 数组元素）→ "落宫数" |
| `references/annotations/...--nlc-layouts.json` | 102 | 后两数记录主星及主门原宫；这里只能核这四类组件。→ …主门落宫… |
| `references/annotations/...--nlc-layouts.json` | 16 | 同书总表丙戌星原宫一，PDF122逐时条星原宫七，门原宫同为七 → 星落宫一／星落宫七／门落宫同为七 |
| `references/annotations/...--nlc-layouts.json` | 4 | "原宫五"（数组元素）→ "落宫五" |
| `references/annotations/...--nlc-layouts.json` | 3 | 符使原宫一五并不同宫：天蓬原宫五并不等于九 → 落宫（两条冲突注） |
| `references/annotations/...--nlc-layouts.json` | 2 | "原宫异文" → "落宫异文"；"缺星原宫" → "缺星落宫"；"门原宫缺数" → "门落宫缺数" |
| `references/inventory/supplemental/...--nlc-layouts.json` | 212 | 符使及宫数保留原纸面值，原宫五不先改寄坤二 → …落宫五不先改寄坤二 |
| `references/inventory/supplemental/...--nlc-layouts.json` | 6 | 原列题符使及十条时支、原宫数已逐项对图 → …落宫数已逐项对图 |
| `references/inventory/supplemental/...--nlc-layouts.json` | 5 | 原宫数按纸面九二记录 → 落宫数按纸面九二记录 |
| `sources/normalized/.../nlc-layouts.md` | 18 | 只摘时柱、符使与原宫，不转录未核格断 → …符使与落宫 |
| `sources/normalized/.../nlc-layouts.md` | 17 | 只转符星、使门、时支和两项原宫数 → …两项落宫数 |
| `sources/normalized/.../nlc-layout-page-reviews.json` | 18 | 指定逐时条符使及原宫数；与总表存在字段差异 → …符使及落宫数 |
| `sources/normalized/.../nlc-layout-page-reviews.json` | 10 | DF200逐时九九，两项原宫均不同 → …两项落宫均不同 |
| `sources/normalized/.../collation-notes.md` | 3 | 原宫五确实出现／其余原宫数仍可用／原宫五不寄换二 → 落宫 |
| `sources/normalized/.../collation-notes.md` | 1 | 符使及原宫必须独立转录 → 符使及落宫必须独立转录 |
| `references/source-editions.json` | 1 | note：符使及宫数保留原纸面值，原宫五不先改寄坤二 → …落宫五不先改寄坤二 |
| `sources/normalized/.../source-manifest.yaml` | 1 | first_passage_scope：蓬休及原宫九二 → 蓬休及落宫九二 |

## 2. 保留未改的「概念性原宫」（逐处列出，共 5 处上游 + 2 处生成物）

  - `qimen-dunjia-tongzhi--nlc-layouts.json`：…符伏吟。五宫寄坤后天芮可回到本宫显示位置，所以判伏吟时要区分原宫数和寄宫后的落点。原注同时列开震、伤坤相迫及戌刑未；庚日…
  - `qimen-dunjia-tongzhi--yanyi-vol4-9.json`：…独立原例或应验。",         "最小布局例还须独立核原宫与寄宫；日干只给乙庚组，不补公历或选一个具体日干。", …
  - `qimen-dunjia-tongzhi.json`：…       "vernacular": "伏吟在本表是星回原宫，不等于八门、奇仪等所有层必都不动；后文还有整体伏吟与可…
  - `qimen-dunjia-tongzhi.json`：…校勘或预测验证。",         "最小布局例还须独立核原宫与寄宫；日干只给乙庚组，不补公历或选一个具体日干。", …
  - `qimen-dunjia-tongzhi.json`：…独立原例或应验。",         "最小布局例还须独立核原宫与寄宫；日干只给乙庚组，不补公历或选一个具体日干。", …

生成物 `source-cases.json` 里的概念性残留（口径句所在）：
  - …宫数」）经实测跟着落宫走：1,888／1,917 条与落宫一致、仅 376 条与原宫一致，故字段名与说明按落宫命名，原值一律不改；键名为兼容保留，含义即落宫数。…
  - …原星五、门一，条称星符伏吟。五宫寄坤后天芮可回到本宫显示位置，所以判伏吟时要区分原宫数和寄宫后的落点。原注同时列开震、伤坤相迫及戌刑未；庚日才添日格。",   …

判据：这些句子说的是**概念对照**（原宫 vs 寄宫落点／星回原宫／与「原宫」数值比对），改成「落宫」会让句子自相矛盾或变成假话，故按裁定保留。

## 3. 重跑导出器的验证（先固定快照）

- 快照：把导出器实际读取的六个路径（`references/inventory`、`references/annotations`、`references/cases`、`references/source-editions.json`、`sources/fulltext`、`sources/normalized`）从工作树复制到 `/tmp/ca/snap`，再对每个被改文件记 md5（下表），随后调用导出器自身的 `collect_cases(snapshot)`——**不是**在移动的 HEAD 上跑。

| 被改文件（快照 md5） | md5 |
|---|---|
| `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` | `eafabf77139e3fa5a9cedd8605df234a` |
| `references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json` | `10392e1a8f1f3226f695b86e8546b248` |
| `references/annotations/san-shi/qimen-dunjia-tongzhi.json` | `8305bf2cd712d614e224d3ec4678f7d2` |
| `references/inventory/supplemental/qimen-dunjia-tongzhi--nlc-layouts.json` | `db29af7c0367b4939d319270ae2b3272` |
| `references/source-editions.json` | `07d7076d25c34b3e015f9e7f6d65f97d` |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/collation-notes.md` | `a8b5f7bb5af8b4c0851c4e0630e8ec9e` |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layout-page-reviews.json` | `84a1d6a60f5b63a07209f0f2cd26ae5a` |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/nlc-layouts.md` | `3cc5a22a5e997186accdcf0b3e6ec7a0` |
| `sources/normalized/san-shi/qimen-dunjia-tongzhi/source-manifest.yaml` | `d3b0cb54530ccc946a3840d670ca6ed1` |
| `references/cases/qimen-component-candidates.json` | `0217563fcee6edde09454eedb97e5351` |

- 重跑结果：`cases=3568`；`值符落宫数=1918`、`值符原宫数=0`；1,920 条 qimen 案例中 1,105 条与旧产物不同，差异**全部**是「原宫→落宫」这一处文本（逐条 diff 抽验，无其它字段变化）。

- 自检：`python3 tools/test-source-cases.py` → 18 tests OK；`python3 tools/validate-executable.py` → OK 15 packages／258 records／579 spans／42 named gaps；`python3 tools/validate-annotations.py` → 53 books／62,839 entries／0 errors。

- 与「提交后重跑」的等价性：导出器 `main()` 用 `git archive HEAD` 取输入；本批把工作树中这六个路径原样复制成快照，因此 captain 提交这批改动后，普通重跑（archive 取到新 HEAD）得到的就是同一份内容（仅 `sourceRevision` 字段随 HEAD 变化）。

## 4. 未纳入本次统一的位置（明确声明）

- `docs/**` 报告与账本：属**历史记录**（记录当时的测量与判定），不改；其中 `docs/closeout/CAPTAIN-VERIFICATION-20260913.md`、`DELIVERY_ACCEPTANCE.json` 等处的「原宫」多为**概念性**表述（与「原宫一致」的比对结论），本就不该改。

- 产品仓：`product:src/lib/engine/fixtures/qimen-source-layouts.json`（同源副本）与 `product:scripts/art-verdict-source-case-recompute.ts` 的说明文字仍在产品侧，需 captain／algo-impl 侧同步（本成员不得改产品仓）。

- `source-cases.json` 由 captain 提交（本成员不 commit）。

