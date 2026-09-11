# 《奇门遁甲统宗》主本：独立审查 CP2（300–599）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。注解 JSON 已在该钉死树中（blob `ce5ece310f10539a8c09c9dcb2c9cce9ab4dc2fa`，SHA256 与 Issue 一致）。本岗工作树只读该 SHA，写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/qimen-dunjia-tongzhi.md` 旧总述、未创建/未抢写 `qimen-dunjia-tongzhi-cp1-review.md`（CP1=0–299 属 [MING-300](mention://issue/01a090b5-8f55-7bec-836a-ff2f48ea1d5c)）。未改引擎 / `chart.*` / golden / 他书。不是续写，不是人工 verified，不是影印校勘，也不是全项目/产品交付。审查岗未参与本包生产。紫微 CP5（1200–1499）已审，本包不涉及、不重做。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；索引 0–299 相对权威 SHA / peer 树（MING-300 同路径）字节级未改；`source-reviewed` 不是人工 `verified`；太乙书局网页电子层阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。本包后 remaining **139**（索引 600–738）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-302`，2026-09-11）：

```
git fetch origin bc798566da77c30e149abf9673c88ecc386702b2
git rev-parse HEAD
git ls-remote origin refs/heads/codex/full-library-completion
shasum -a 256 references/annotations/san-shi/qimen-dunjia-tongzhi.json
shasum -a 256 sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md
git rev-parse HEAD:references/annotations/san-shi/qimen-dunjia-tongzhi.json
git rev-parse HEAD:sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md
cmp HEAD blob vs working tree (annotations)
test ! -f docs/book-reviews/qimen-dunjia-tongzhi-cp1-review.md
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解 SHA256 | `c1ba57ce2ec6d9d6d6cbaad381711e9c8bd738a87d6a53d34e12e2aa9dab4a34`（与 Issue 钉死值一致） |
| 注解 blob | `ce5ece310f10539a8c09c9dcb2c9cce9ab4dc2fa` |
| working tree vs `HEAD` 注解 blob | 相同 |
| 源 `fulltext.md` SHA256 | `8de9995e7b185d6159373a6fa31056931c273e8b12ab2fc2acb16c659c4567c3` |
| 源 blob | `a214cf7f39320d0d0b058bb6851acf5ad453f6c3` |
| 来源层 | 主电子层为太乙书局网页转录（另有 CTP/国图影印锚点）；`source-reviewed` 只表示对照电子段，非全书影印校勘或预测有效性证明 |
| 注解 ID 与 inventory `paragraphs` | 739/739 一一对应，`mismatch=0`；CP2 kind 差=0 |
| 相对 MING-300 同路径 JSON | 全文件字节相同 |
| 本岗改动文件 | 仅新增 `docs/book-reviews/qimen-dunjia-tongzhi-cp2-review.md` |
| `qimen-dunjia-tongzhi-cp1-review.md` | 本树不存在，未创建、未改 |

无越权文件。源层未改。注解 JSON 未改。CP1 审查文件未抢写。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/qimen-dunjia-tongzhi.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 739, "source_reviewed": 739,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书与本包均无 `verified: true`（字段缺省）。

## 3. verified / draft 未越权提升

739 条：`review=source-reviewed` 全 739；`verified` 字段缺省 739（按 false 计 true=0）；`draft` 0。无升 verified。

kind 全书累计：理论 356、术语 103、重复 91、规则候选 73、序跋目录 45、操作步骤 29、评注或元数据 24、待核实 10、案例 8。

本包 CP2（300–599，300 条）：`review=source-reviewed` 全 300；`verified` 缺省 300。kind：理论 157 / 重复 91 / 术语 31 / 序跋目录 13 / 案例 3 / 待核实 2 / 评注或元数据 2 / 规则候选 1。

空白白话 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0（91 条 `重复` kind 各有独立白话，标明卷十复引，非模板填充）。`terms` 非空 300/300。`notes` 空 0。inventory `doubtful`/`missing_marker` 本包均为 0。注解 kind 与 inventory kind 300–599 差=0。

## 4. 索引 0–299 相对权威 SHA 未改

本岗 HEAD 即权威 SHA，working tree 注解字节与 `HEAD` blob 相同；与 MING-300 peer 树同路径 JSON 字节相同，故 0–299 相对钉死 SHA 未改。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起，不评） | `qimen-dunjia-tongzhi:L0003-L0013` |
| 注解索引 299（CP1 止，不评） | `qimen-dunjia-tongzhi:L0825-L0825` |
| 0–299 paragraphId 集 SHA256 | `604220ce4993bd9356151a1a2cac9ae1513a82a1f3b78aefb2020a30434c0395` |

CP1 300 条同样 `source-reviewed` / `verified` 缺省。本包不评其语义，不写 `qimen-dunjia-tongzhi-cp1-review.md`。

## 5. 索引边界（本包 300–599）

| 位置 | 实测 ID | inventory heading |
|---|---|---|
| 注解索引 300（CP2 起） | `qimen-dunjia-tongzhi:L0827-L0827` | 《奇门遁甲统宗》卷之三 |
| 注解索引 599（CP2 止） | `qimen-dunjia-tongzhi:L1515-L1515` | 《奇门遁甲统宗》卷之十一 玄机赋（中） |
| 下一未纳入 | `qimen-dunjia-tongzhi:L1517-L1517` | 《奇门遁甲统宗》卷之十一 玄机赋（中） |

起讫与 Issue 钉死 locator 一致。本包后 remaining **139**（600–738）。

CP2 覆盖：卷三子胥十二宫/太阳临时/九星与行兵杂摘 → 奇门演卦（符使/门方/世应主客/六亲六神八卦地支类象）→ 奇门演义卷四～九（八神会门赋注，含缺文标记）→ 卷十玄机赋（上）本赋与大量演义复引层 → 卷十一玄机赋（中）起至 `L1515` 庚癸/庚己格句。

heading 切换：300 卷之三 → 359 奇门演义（卷四～九）→ 450 卷十玄机赋（上）→ 583 卷十一玄机赋（中）。

## 6. 抽样语义（22 段非模板，对照原文，不凭旧总述/CP1 报告）

原文取 `sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md` 的 `start_line–end_line`。下列覆盖理论、待核实、规则、案例、术语、评注缺文、序跋、卷十复引与卷十一格句。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L0827-L0827` | 理论 / sr | 子胥十二宫遁身传说；白话标明无盘面/时间输入，不作应验案例 | 通过 |
| 301 | `L0829-L0829` | 待核实 / sr | 太阳临时法四孟仲季配干/卦位混写；保留不明转换，不直接编码 | 通过 |
| 310 | `L0847-L0847` | 序跋 / sr | 「行兵杂摘」摘录层标题 | 通过 |
| 315 | `L0893-L0893` | 案例 / sr | 符使演卦：阳一局辛巳 → 地符坤、天使离 → 火地晋；不补公历 | 通过 |
| 317 | `L0897-L0912` | 待核实 / sr | 门方演卦首句「方外门内」与八例卦名（井/泰/…）内外方向成组冲突；标待核实不改字 | 通过 |
| 319 | `L0916-L0916` | 规则 / sr | 世客应主 + 空亡旺衰；注明需六爻装支，奇门四字段不足单独支持 | 通过 |
| 323 | `L0938-L0945` | 案例 / sr | 雷地豫应期例；「破于辰」等用语差异保留，无独立结果故不 verified | 通过 |
| 340 | `L0979-L0979` | 术语 / sr | 艮：童子山人猫犬砖石 | 通过 |
| 350 | `L0999-L0999` | 术语 / sr | 卯 + 乘朱为牙行人；六神条件限定 | 通过 |
| 360 | `L1021-L1021` | 理论 / sr | 太阴会休注：二八日雨、军占守；与赋半月望/捕向东南分歧不得合并 | 通过 |
| 366 | `L1033-L1033` | 评注 / sr | 缺文标记：太阴景门注及死门赋缺；不当古代判断 | 通过 |
| 380 | `L1061-L1061` | 理论 / sr | 六合景赋：不时雷、坤兵变、西方捕；保留 `*` 残形不猜补 | 通过 |
| 400 | `L1101-L1101` | 理论 / sr | 白虎惊门：三日风、丑未良将、主得地客自倾 | 通过 |
| 423 | `L1147-L1147` | 评注 / sr | 九地伤/杜赋缺文标记；覆盖现有电子段≠恢复缺文 | 通过 |
| 440 | `L1181-L1181` | 理论 / sr | 九天杜门注：未黄云、次午雨；「解粮革来」词形不顺不猜补 | 通过 |
| 449 | `L1199-L1205` | 案例 / sr | 八将会门戊寅例腾蛇伤门；丁加癸凶格压过会奇；注明与卷十复引同段 | 通过 |
| 450 | `L1209-L1209` | 理论 / sr | 六合军赋：畏死求和、降人远调；神象≠真实投诚证据 | 通过 |
| 492 | `L1293-L1293` | 重复 / sr | 卷十复引太阴休门赋；分事项占辞，雨期/捕向须与注分读 | 通过 |
| 500 | `L1309-L1309` | 重复 / sr | 卷十复引太阴死门注；不能补已缺赋或完整组合表 | 通过 |
| 540 | `L1389-L1389` | 重复 / sr | 玄武生门注：午戌应期；僧人/游食消息属占辞非现实情报源 | 通过 |
| 590 | `L1497-L1497` | 理论 / sr | 惊门虚惊退败 / 开门四通；基础门象须结合后文时令落宫 | 通过 |
| 599 | `L1515-L1515` | 理论 / sr | 庚癸为难对敌、加己为刑；两格不可因皆凶混并天干序 | 通过 |

关键条件与源行（抽核）：

- 子胥十二宫 / 太阳临时 / 行兵杂摘：L0827–L0847
- 符使晋卦、门方内外冲突、世客应主、雷地豫应期：L0893–L0945
- 艮/卯类象、太阴休注、缺文标记：L0979–L1033
- 六合景 / 白虎惊 / 九地缺文 / 九天杜：L1061–L1181
- 八将会门例、卷十六合起、太阴休复引 / 死门复引：L1199–L1309
- 玄武生门复引、惊开基础门象、庚癸刑格收口：L1389–L1515

## 7. source-reviewed ≠ 人工 verified

主本为太乙书局网页电子层（另有影印锚点）。本包 300 条电子语义阅读升/保持 `source-reviewed`，只表示对照电子段落实了条件/边界/疑点/复引关系，不是影印逐字校勘，也不是预测有效证据。案例均无独立公历与已发生结果，不得升 verified。不得把 739 条 source-reviewed 写成已人工 verified。本包后 remaining 139，仍不是人工 verified，也不是全项目完成。

## 8. Caveat（不构成本包失败）

1. `source-reviewed` ≠ 人工 `verified`；网页电子本 ≠ 影印校勘。
2. 本包 2 条 `待核实` 已显式保留疑点：`L0829` 太阳临时干支/卦位混写；`L0897–L0912` 门方演卦内外方向成组冲突。未静默改字或升 verified。
3. 电子缺文标记 `L1033`、`L1147` 等：覆盖现有段不代表缺赋/缺注已恢复。
4. 卷十 `重复` 91 条（`L1293`–`L1479`）为演义复引层；白话标明复引，不算新的独立原例或三次应验（如八将会门与 `L1199–L1205` 同段）。
5. 赋/注应期或捕向分歧（如太阴休门半月望 vs 二八日、东南 vs 或东或西）须分读，不得合并成精准算法。
6. 索引 0–299 属 MING-300；本包确认未改、不评语义、不写 CP1 文件。

## 9. 交付账本

| 项 | 值 |
|---|---|
| Issue | MING-302 |
| 工作树 | `fateradar-multica-ming-302` |
| 分支 | `codex/multica-ming-302` |
| 基线 SHA | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 写出 | 仅 `docs/book-reviews/qimen-dunjia-tongzhi-cp2-review.md` |
| 注解改动 | 无 |
| validator | `ok=true` entries=739 source_reviewed=739 errors=[] |
| CP2 范围 | 300–599 = `L0827` … `L1515` |
| 下一未纳入 | `L1517` |
| remaining | **139** |
| 结论 | **通过**（独立审查；非人工 verified；非影印校勘；非全书人工完成） |
