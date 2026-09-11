# 《子平真诠》建禄月劫 P0 续段 L1355/L1357：独立审查

审查对象：[MING-356](mention://issue/01a09120-daa8-7c11-b5e1-d4a2c9b0deb8) / `origin/codex/multica-ming-356` @ `3be246beeba1fba62610a0b5ca927373ef1d5a59`。  
底：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。  
已审 P0（只读对照，不重做）：[MING-347](mention://issue/01a0910d-b0fe-773f-b4cd-d948a467dc43) @ `02574d0042345b19ec43456badf645c00ecd6047`；审查 [MING-350](mention://issue/01a09116-d7eb-7a3b-b051-71c65905e3b1) @ `9cca06799d3f2b3efb5fe65bfff17671f50e7b6b` 已通过。  
工作树 `fateradar-multica-ming-358` / 分支 `codex/multica-ming-358`。本岗写出仅本文件。  
未改 `references/annotations/bazi/ziping-zhenquan.json`、未改源文、未改引擎/`chart.*`/`chart-defaults`/`qimen-markers`、未改 347/350 已交文档、未抢大六壬 / SDZJ0170。  
本岗未参与 MING-356 生产。不是八字引擎实现，不是全书完成，不是人工 verified。

结论：**通过。** 相对 329 仅该续段文档；validator `entries=556 source_reviewed=556 errors=[]`；无 `verified=true`。L1355/L1357 条件可对照电子原文复核，非模板、非引擎实现。下列 caveat 不构成本包失败，也不把任何条升 verified。

---

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-358`，2026-09-11）：

```
git fetch origin codex/multica-ming-356 codex/multica-ming-329 codex/multica-ming-347 codex/multica-ming-350
git rev-parse HEAD origin/codex/multica-ming-356 origin/codex/multica-ming-329
git diff --name-only 6effd8e4f951fd17e1b1e0454942946ebc765da9..HEAD
git diff --stat 6effd8e4f951fd17e1b1e0454942946ebc765da9..HEAD
shasum -a 256 references/annotations/bazi/ziping-zhenquan.json
git rev-parse HEAD:references/annotations/bazi/ziping-zhenquan.json
git hash-object references/annotations/bazi/ziping-zhenquan.json
git rev-parse 6effd8e4f951fd17e1b1e0454942946ebc765da9:references/annotations/bazi/ziping-zhenquan.json
git ls-tree HEAD -- docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0.md \
  docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0-review.md
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` / `origin/codex/multica-ming-356` | `3be246beeba1fba62610a0b5ca927373ef1d5a59` |
| 底 `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 相对 329 name-only | **仅** `docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0-l1355.md`（+184） |
| 注解 SHA256 | `f557e5d8bb02e3216aa712c9a59a2c1d2fddac3ebc926fc9c32990a7bc4216c5`（与 Issue 钉值一致） |
| 注解 blob HEAD / working / 329 / 347 | 同为 `e6afc7e8f17ee23033a881eedab86ff254c21ebf`（未改） |
| 347 P0 文档 / 350 审查稿 | 本树 `ls-tree` **不存在**（356 从 329 另开，未回改、未覆盖） |
| 引擎 / `chart.*` / 他书注解 | name-only 无这些路径 |

无越权文件。注解 JSON 未改。347/350 已交文档未改。

Caveat（不失败）：章四六取运 `L1345`–`L1353` 条件账本在 347 树，不在本分支。交包所称「文档层 remaining = 0」是跨包账本（347+356），不是本树已合并 347。

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

独立计数：`entries=556`，`review=source-reviewed` 556/556；含 `verified` 键 0 条，`verified=true` 0 条。  
校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

覆盖本包：索引 **404** = `ziping-zhenquan:L1355-L1355`，**405** = `ziping-zhenquan:L1357-L1357`，均 `kind=规则候选`、`review=source-reviewed`、无 `verified`。与 Issue 钉值一致。

---

## 3. verified / source-reviewed 边界

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 556/556 |
| `verified` 字段 | **条目无此键**（0 条含 `verified`）；无任何 true |
| 升 human verified | 无。续段文明确禁止，本审查亦不升 |

`source-reviewed ≠ 人工 verified`。电子全文对照不是影印校勘。本包不宣称《子平真诠》全书完成，也不是八字引擎实现。

---

## 4. 条件对照原文（非引擎、非模板）

原文取 `sources/fulltext/bazi/ziping-zhenquan/fulltext.md` 对应行。下列为独立抽核，不凭交包摘要。摘录与全文逐字相符。

### 4.1 `L1355-L1355` 用伤食取运

原文：

> 祿劫而用傷食，財運最宜，煞亦不忌，行印非吉，透官不美。若命中傷食太重，則財運固利，而印亦不忌矣。

| 条件 ID | 源行要点 | 判定 |
|---|---|---|
| JL-YUN-OUT-01 | 财运最宜 | 通过 |
| JL-YUN-OUT-02 | 「煞亦不忌」标**非忌声明**，未升成「见煞反喜」必要 | 通过 |
| JL-YUN-OUT-03 | 行印非吉 | 通过 |
| JL-YUN-OUT-04 | 透官不美 | 通过 |
| JL-YUN-OUT-05/06/07 | 「伤食太重」门闩；财运固利不变；**只**翻印忌，不扩散官煞 | 通过 |
| 与 `JL-YUN-WEA-*` 区分 | L1349 是「用财而带伤食」，本段是「用伤食」成局线 | 通过 |

未知边界：

| ID | 对照 | 判定 |
|---|---|---|
| JL-YUN-OUT-U1 | 「太重」无数量/透藏/根气阈值 | 通过（未静默定死） |
| JL-YUN-OUT-U2 | 「透官」干透 vs 支藏权重未定义 | 通过 |
| JL-YUN-OUT-U3 | 本段无整盘、无大运，不能复算流年 | 通过 |
| JL-YUN-OUT-U4 | L1329「唯春木秋金」未在取运句重申 | 通过（不得取消季节门闩，也不得把非春木秋金泄秀局静默套表） |

Caveat（不失败）：类型栏把「非吉 / 不美」写成「忌」，语气略强于原文，但未升级为「立见其灾」；例外覆盖范围仍贴原文。

### 4.2 `L1357-L1357` 官煞并出取清后取运

原文：

> 祿劫而【校：「而」字據中州本補】官煞並出，不論合煞留官，存官制煞，運喜傷食，比劫亦宜，印綬未爲良圖，財官亦非福運。

校记与注解 `notes` 一致。不据此改 JSON。

| 条件 ID | 源行要点 | 判定 |
|---|---|---|
| JL-YUN-CLR-00 | 「不论合煞留官，存官制煞」= 两条取清路径共用运表；叠加 L1331「必须取清」 | 通过 |
| JL-YUN-CLR-00b | L1357「存官制煞」与 L1331「制煞留官」作同义路径标签，不另立第三术 | 通过 |
| JL-YUN-CLR-00c | 未取清不得套本运表称贵运已配 | 通过 |
| JL-YUN-CLR-01/02 | 运喜伤食；比劫亦宜 | 通过 |
| JL-YUN-CLR-03/04 | 印绶未为良图；财官亦非福运 | 通过 |
| 岁运财官 ≠ 去掉原局留官 | 取运章「财官亦非福运」指岁运再逢，不是否定命中已留之官 | 通过 |

未知边界：

| ID | 对照 | 判定 |
|---|---|---|
| JL-YUN-CLR-U1 | L1331「两官竞出须制伏」是否完全同本运表；L1357 只点名合煞留官 / 存官制煞 | 通过 |
| JL-YUN-CLR-U2 | 合留对象运中被冲合回混 — 原文无回混规则 | 通过 |
| JL-YUN-CLR-U3 | 不得回写覆盖 L1347 纯用官印护/财生两子路径 | 通过 |
| JL-YUN-CLR-U4 | 正例有四柱，仍无公历/起运/大运 | 通过 |

不成立例 N-OUT-1/2、N-CLR-1/2 均可回锚原文，未造假盘。

---

## 5. 原例表层复算（独立，缺输入如实）

「可复核」= 四柱字形 + 日主禄堂 + 透干十神/合制对象表层；**无**公历、地点、起运、大运 → 不可复算运程吉凶。注解 `canRecompute=true` 仅指四柱输入。

| # | 四柱 | 建禄 | 表层核对 | 判定 |
|---|---|---|---|---|
| E-OUT-1 张状元 | 甲子 丙寅 甲子 丙寅 | 甲日·寅月·禄寅 ✓ | 干透丙食神；无金土透用；寅月春木 | 通过（成局前置，无运程） |
| E-OUT-2 金水相涵 | 癸卯 庚申 庚子 庚辰 | 庚日·申月·禄申 ✓ | 干透癸伤官；申月秋金 | 通过（成局前置；见 caveat） |
| E-CLR-1 一平章 | 辛丑 庚寅 甲辰 乙亥 | 甲日·寅月 ✓ | 辛正官+庚七杀并透；乙庚合 → 合煞留官 | 通过（JL-YUN-CLR-00 门闩，无运程） |
| E-CLR-2 制煞留官 | 辛亥 庚寅 甲申 丙寅 | 甲日·寅月 ✓ | 辛官+庚杀；丙食制庚 → 制煞留官 / 「存官制煞」标签 | 通过（无运程） |

四柱与注解 `L1329`/`L1331` `cases` 一致，未另造盘。

Caveat（不失败）：E-OUT-2 年支卯对庚为偏财，原文仍作「无财官而用伤食」正例。本包只作前置成局对照，不在本包重判成格，与已审 MING-347 口径一致。

---

## 6. 结论与 remaining

- **通过** MING-356 建禄月劫取运 P0 续段 L1355/L1357 审查。  
- 注解 blob/SHA256 未变；validator 绿；无 human verified。  
- 相对 329 仅续段文档；未改 347/350 已交文档。  
- remaining（本包外）：算法消费须另开 Issue；文档层章四六取运正文跨 347+356 已闭合，仍非引擎实现、非全书完成。  
- 本岗唯一写出：`docs/book-reviews/ziping-zhenquan-jianlu-yuejie-p0-l1355-review.md`。
