# 《子平真诠》建禄月劫 P0：独立审查条件闭环

审查对象：[MING-347](mention://issue/01a0910d-b0fe-773f-b4cd-d948a467dc43) / `origin/codex/multica-ming-347` @ `02574d0042345b19ec43456badf645c00ecd6047`。  
底：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。  
工作树 `fateradar-multica-ming-350` / 分支 `codex/multica-ming-350`。本岗写出仅本文件。  
未改 `references/annotations/bazi/ziping-zhenquan.json`、未改源文、未改引擎/`chart.*`/`chart-defaults`/`qimen-markers`、未抢 [MING-348](mention://issue/01a09113-7a20-7874-a01c-18df3a37cdde) 飞星收口。  
本岗未参与 MING-347 生产。不是八字引擎实现，不是全书完成，不是人工 verified。

结论：**通过。** 相对 329 仅该 P0 文档；validator `entries=556 source_reviewed=556 errors=[]`；无 `verified=true`。条件可对照电子原文复核，非引擎实现。下列 caveat 不构成本包失败，也不把任何条升 verified。

---

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-350`，2026-09-11）：

```
git fetch origin codex/multica-ming-347 codex/multica-ming-329
git rev-parse HEAD
git rev-parse origin/codex/multica-ming-347 origin/codex/multica-ming-329
git diff --name-only 6effd8e4f951fd17e1b1e0454942946ebc765da9..HEAD
git diff --stat 6effd8e4f951fd17e1b1e0454942946ebc765da9..HEAD
shasum -a 256 references/annotations/bazi/ziping-zhenquan.json
git rev-parse HEAD:references/annotations/bazi/ziping-zhenquan.json
git hash-object references/annotations/bazi/ziping-zhenquan.json
git rev-parse 6effd8e4f951fd17e1b1e0454942946ebc765da9:references/annotations/bazi/ziping-zhenquan.json
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` / `origin/codex/multica-ming-347` | `02574d0042345b19ec43456badf645c00ecd6047` |
| 底 `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 相对 329 name-only | **仅** `docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0.md`（+256） |
| 注解 SHA256 | `f557e5d8bb02e3216aa712c9a59a2c1d2fddac3ebc926fc9c32990a7bc4216c5`（与 Issue `f557e5d8` 前缀一致） |
| 注解 blob HEAD / working / 329 | 同为 `e6afc7e8f17ee23033a881eedab86ff254c21ebf`（未改） |
| 引擎 / `chart.*` / 他书注解 | name-only 无这些路径 |

无越权文件。注解 JSON 未改。

---

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/ziping-zhenquan.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 556, "source_reviewed": 556,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

---

## 3. verified / source-reviewed 边界

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 556/556 |
| `verified` 字段 | **条目无此键**（0 条含 `verified`）；无任何 true |
| 升 human verified | 无。P0 文明确禁止，本审查亦不升 |

`source-reviewed ≠ 人工 verified`。电子全文对照不是影印校勘。本包不宣称《子平真诠》全书完成。

覆盖索引 387–403（17 条）与 Issue 一致：起 `L1310-L1310`、止 `L1353-L1353`。其中 `L1341`/`L1343` 为源页元数据与卷题，P0 未硬抽条件，合理。`L1355`/`L1357` 已标 remaining，未越权写出。

---

## 4. 条件闭环对照原文（非引擎）

原文取 `sources/fulltext/bazi/ziping-zhenquan/fulltext.md` 对应行。下列为独立抽核，不凭交包摘要。

### 4.1 定义 / 成败 / 救应

| 条件 ID | 源行要点 | 判定 |
|---|---|---|
| JL-DEF-01/03 | L1310：建禄=月建逢禄堂；禄即是劫；「禄堂透出即可依以为用」—**非也**；透干合支别取财官煞食 | 通过 |
| JL-DEF-02/04 | L349–353：月令与日同类不可直接为用；另取用神；「非用而即用神」；东里按语张力保留 | 通过 |
| JL-DEF-05 | L1345：「即以禄劫所成之局，分而配之」 | 通过 |
| JL-OK-01/02/03 | L371：透官而逢财印 / 透财而逢食伤 / 透煞而遇制伏 | 通过（或关系） |
| JL-OK-04 | L1329：无财官用伤食；「唯春木秋金」 | 通过 |
| JL-BAD-01 | L381：无财官，透煞印 → 败 | 通过 |
| JL-BAD-02/03、JL-SAVE-05 | L1333：孤官更小；透伤食破格；合伤存官可贵 | 通过 |
| JL-BAD-04、JL-OK-05 | L1335：不透伤食难发福；一位不杂、支根多可富不贵 | 通过 |
| JL-BAD-05 | L787：建禄用官而运逢伤 = 败运类 | 通过 |
| JL-SAVE-01/02 | L409：用官遇伤而伤被合；用财带煞而煞被合 | 通过 |
| JL-SAVE-03/04 | L1325 合财去党煞+支局制；L1327 合煞存财 | 通过 |
| JL-SAVE-06 / JL-PAR-01 | L1331：官煞竞出取清；两官竞出须制伏 | 通过 |

### 4.2 取运分支

| 源行 | P0 映射 | 判定 |
|---|---|---|
| L1347 印护 / 财生 | JL-YUN-OFF-A*/B*；并保留与 L787「用官运伤」在印护路径的 **相并未知**（JL-PAR-U2） | 通过 |
| L1349 财食重/轻 | JL-YUN-WEA-*；重/轻无阈值 → unknown | 通过 |
| L1351 食煞轻重 | JL-YUN-KIL-*；无量化阈值 | 通过 |
| L1353 合煞存财 vs 合财存煞 | JL-YUN-MIX-*；合留对象先于取运 | 通过 |

未发现把 P0 写成可执行引擎/统一喜忌向量。消费契约 §7 与「非实现包」边界成立。

### 4.3 隔位 / 未知边界

| ID | 对照 | 判定 |
|---|---|---|
| JL-SEP-01 | L1317「以官隔之」；王少师干序印–官–日–财 | 通过 |
| JL-SEP-U1–U3、JL-PAR-U1–U3 | 距离函数/地支替代/阈值/跨段冲突/半合成局均标 unknown | 通过（未静默定死） |

---

## 5. 原例表层复算（独立，缺输入如实）

「可复算」= 四柱字形 + 日主禄堂 + 透干十神/合对象表层；**无**公历、地点、起运、大运 → 不可复算运程吉凶。

| # | 四柱 | 建禄 | 表层核对 | 判定 |
|---|---|---|---|---|
| E1 金丞相 | 庚戌 戊子 癸酉 癸亥 | 癸日·子月·禄子 ✓ | 干：正印、正官、比、比 → 印护官 | 通过 |
| E2 王少师 | 庚午 戊子 癸卯 丁巳 | 同上 ✓ | 印–官–日–偏财；官在印财之间 | 通过 |
| E3 张都统 | 甲子 丙子 癸丑 丙辰 | 同上 ✓ | 食神+正财透干；伤食化劫生财线 | 通过 |
| E4 娄参政 | 丁巳 壬子 癸卯 己未 | 同上 ✓ | 丁壬合财；己七杀；正文「卯未会局」口径 | 通过 |
| E5 袁内阁 | 戊辰 癸亥 壬午 丙午 | 壬日·亥月·禄亥 ✓ | 戊癸合 → 合煞存财 | 通过 |
| E6 王总兵 | 己酉 乙亥 壬戌 庚子 | 壬日·亥月 ✓ | 乙庚合；正文「去伤存官」（本书伤食统称） | 通过 |

不成立 / 未知例 N1–N3、U1–U3：对照 L1310 / L381 / L1333 / L1319 notes「半合式成局须另核」/ L1337 缺运程 / L1347↔L787 冲突 — **成立，未造假盘、未发明阈值**。

Caveat（不失败）：E3 表写作「甲伤」而严格十神为食神；E6 正文称伤而乙对壬为食神。属原文「伤食」统称，P0 跟书，不升 verified。

---

## 6. 结论与 remaining

- **通过** MING-347 P0 条件闭环审查。  
- 注解 blob/SHA256 未变；validator 绿；无 human verified。  
- remaining（本包外）：同章取运 `L1355`、`L1357`；算法实现须另开 Issue。  
- 本岗唯一写出：`docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0-review.md`。
