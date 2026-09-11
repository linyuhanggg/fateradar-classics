# 《梅花易数》主本：独立审查 CP1（0–299）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。注解 JSON 已在该钉死树中（blob `0ac958247cd32398b9ccee669dd7ef137cd034ca`，SHA256 与 Issue 一致）。本岗工作树只读该 SHA，写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/meihua-yishu.md` 旧总述、未改引擎 / `chart.*` / golden / 他书 / 滴天髓·增删·渊海已审范围。不是全书 623 段完成，不是续写 0–299，不是引擎包，也不是全项目完成。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；维基文库电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–622（`L0907-L0907` 起）本包不审、不改。remaining 本包后 323。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-297`，2026-09-11）：

```
git fetch origin bc798566da77c30e149abf9673c88ecc386702b2
git rev-parse HEAD
git ls-remote origin refs/heads/codex/full-library-completion
shasum -a 256 references/annotations/divination/meihua-yishu.json
shasum -a 256 sources/fulltext/divination/meihua-yishu/fulltext.md
git rev-parse HEAD:references/annotations/divination/meihua-yishu.json
git rev-parse HEAD:sources/fulltext/divination/meihua-yishu/fulltext.md
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解 SHA256 | `790969e2bbbedcc0695cc57458f12473839b8d5332e51459bcd6147715d24374`（与 Issue 钉死值一致） |
| 注解 blob | `0ac958247cd32398b9ccee669dd7ef137cd034ca` |
| 源 `fulltext.md` SHA256 | `220aeb83f087ec4085c9ecf8e8381f0db51cd5376ccb1f3ce14943d8c14d6f50` |
| 源 blob | `902a968091fbaf8f039f0d2268bb19f022753962` |
| `scopeNote` | 按现存维基文库通行电子本文字逐稳定段整理；`source-reviewed` 只表示对照电子原文，非影印逐字核验或预测有效性证明 |
| 注解 ID 与 `paragraphs.json` | 623/623 一一对应，`mismatch=0` |
| 本包索引 | 0–299；未改 300–622 |
| 旧总述 `meihua-yishu.md` | 只读，未改 |

无越权文件。源层未改。他书 / 引擎 / `chart.*` 未覆盖。不是续写包。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/meihua-yishu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 623, "source_reviewed": 623,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书与本包均无 `verified: true`。

## 3. verified / draft 未越权提升

623 条：`review=source-reviewed` 全 623；`verified` true=0；字段缺省（非显式 false）623；`draft` 0。无升 verified。

kind 全书累计：规则候选 207、术语 188、操作步骤 51、理论 48、序跋目录 37、案例 37、待核实 32、评注或元数据 23。

本包 CP1（0–299）kind：术语 122 / 规则候选 88 / 操作步骤 28 / 序跋目录 21 / 案例 19 / 理论 10 / 待核实 9 / 评注或元数据 3。

空白白话 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。`terms` 非空 300/300。`notes` 空 228（多为八卦万物属类短表项：术语 116 / 规则候选 67 / 操作步骤 19 / 序跋目录 14 / 理论 8 / 案例 3 / 评注 1；短表项以 terms+vernacular 自足，不构成本包失败）。inventory `doubtful`/`missing_marker` 本包均为 0。注解 kind 与 inventory kind 0–299 差=0。

## 4. 索引边界

`paragraphs.json` 全书 623 段；本包审查 0–299。300–622 在同一 JSON 中已是 `source-reviewed`，本岗只读不改、不把其计入本包通过范围。

| 位置 | 实测 ID | heading |
|---|---|---|
| 注解/源索引 0 | `meihua-yishu:L0005-L0005` | 序 |
| 注解索引 299（CP1 止） | `meihua-yishu:L0905-L0905` | 八卦萬物屬類 |
| 注解索引 300（下一包起，不在本包） | `meihua-yishu:L0907-L0907` | 八卦萬物屬類 |
| 源/注解索引 622（全书末） | `meihua-yishu:L2557-L2557` | 卦應…（本包不审） |

起始/止点与 Issue 钉死 ID 一致。remaining 323（300–622）。

CP1 覆盖：序署与破枕/观梅传承叙事 → 《宋史》邵雍传附录 → 先天数 / 后天数 / 体用互变 → 卦气旺与干支数 → 玩法与互卦起例 → 一字至十一字占 → 为人占与八卦类象 → 观梅 / 西林寺牌额 / 鸡鸣 / 枯枝等案例 → 听声音占 → 八卦万物属类（乾至离分项，止于离五色 `L0905`）。离姓字之后与兑/艮等续表 `L0907` 起不在本包。

## 5. 抽样语义（≥15 非模板，对照原文，不凭旧总述）

原文取 `sources/fulltext/divination/meihua-yishu/fulltext.md` 的 `start_line–end_line`。下列覆盖序跋、起例、案例、属类表与待核实。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0005` | 评注 / sr | 「清黃宗羲撰」；署名为电子本信息≠作者考定 | 通过 |
| 1 | `L0007-L0038` | 序跋 / sr | 破枕得书、观梅；先天先数后天先卦；年月「某」不补公历 | 通过 |
| 13 | `L0093-L0093` | 序跋 / sr | 《宋史》提醒事后附会前知；与序神验叙事对读 | 通过 |
| 17 | `L0101-L0101` | 术语 / sr | 先天横图乾1…坤8；不可混洛书九宫 | 通过 |
| 21 | `L0109-L0148` | 操作 / sr | 年月日时起卦与物声字占分列；先天看象后天兼爻辞 | 通过 |
| 22 | `L0150-L0156` | 理论 / sr | 体用互变、体党旺衰、比和先后；非吉凶票数 | 通过 |
| 28 | `L0178-L0178` | 规则 / sr | 卦气旺四季与辰戌丑未土；旺≠事成 | 通过 |
| 42 | `L0224-L0224` | 待核实 / sr | 「又云」乾坤无互、互其变卦；与普通互卦并存，未改产品算法 | 通过 |
| 50 | `L0258-L0258` | 操作 / sr | 四字平上去入取数；传统四声≠普通话；与十一字改字数并存 | 通过 |
| 82 | `L0344-L0349` | 案例 / sr | 观梅：34→兑、43→离、初爻动革→咸；年支农历复算成立 | 通过 |
| 91 | `L0405-L0405` | 案例 / sr | 西林寺牌额剥卦阴人之祸为传说推断，不推广现实性别归因 | 通过 |
| 107 | `L0497-L0509` | 操作 / sr | 听声音：次数/方位/声源分类；悲喜仅辅象 | 通过 |
| 125 | `L0555-L0555` | 待核实 / sr | 乾人事「高上下屈」不顺；保留原字不擅改 | 通过 |
| 152 | `L0609-L0609` | 待核实 / sr | 「澤天決」对应通行夬；保留电子原字并标对应 | 通过 |
| 198 | `L0703-L0703` | 规则 / sr | 震谋旺宜动、秋不遂；不推广到全卦全事 | 通过 |
| 200 | `L0707-L0707` | 待核实 / sr | 「行移取甚反復」不清；不补司法程序 | 通过 |
| 246 | `L0799-L0799` | 待核实 / sr | 「資賊」字义待核；不改写成另一身份 | 通过 |
| 272 | `L0851-L0851` | 待核实 / sr | 「末濟」对应未济；保留原字 | 通过 |
| 285 | `L0877-L0877` | 规则 / sr | 离婚姻：不成/中女/夏可/冬不利多分支并存 | 通过 |
| 296 | `L0899-L0899` | 待核实 / sr | 「立人旁士姓氏」待校；不自造姓氏名单 | 通过 |
| 299 | `L0905-L0905` | 术语 / sr | 离五色赤紫红；本包止此 | 通过 |

关键条件与源行（抽核）：

- 序署 / 破枕观梅传承 / 《宋史》附录：L0005–L0093
- 先天数、后天数、体用互变、卦气旺：L0101–L0178
- 互卦特例、四字声调占：L0224–L0258
- 观梅复算（34%8=2 兑，43%8=3 离，43%6=1 初爻）：L0344–L0349
- 听声音占、乾人事待核、坤宫決字：L0497–L0609
- 震谋/官讼、坎人物屋舍、离宫末濟与婚姻五色：L0703–L0905

## 6. Caveat（不构成本包失败）

1. `source-reviewed` ≠ 人工 `verified`；维基电子本 ≠ 影印校勘。
2. 本包 9 条 `待核实`（`L0224` 乾坤互特例、`L0555` 高上下屈、`L0609` 決/夬、`L0707` 行移取甚、`L0799` 資賊、`L0801` 內序以利、`L0809` 花酒長器/混地、`L0851` 末濟、`L0899` 立人旁士）均已显式保留疑点，未静默改字或升 verified。
3. `notes` 空 228 多为属类短表；白话与 terms 仍非空，无模板填充。
4. 观梅等案例可按原文农历/时辰复算，但不补绝对公历年；应验叙述与可复算卦形已分层。
5. 索引 300–622 已 `source-reviewed` 但本包不审、不计入通过范围。

## 7. 交付账本

| 项 | 值 |
|---|---|
| Issue | MING-297 |
| 工作树 | `fateradar-multica-ming-297` |
| 分支 | `codex/multica-ming-297` |
| 基线 SHA | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 写出 | 仅 `docs/book-reviews/meihua-yishu-cp1-review.md` |
| 注解改动 | 无 |
| validator | `ok=true` entries=623 source_reviewed=623 errors=[] |
| CP1 范围 | 0–299 = `L0005` … `L0905` |
| 下一未纳入 | `meihua-yishu:L0907-L0907`（索引 300） |
| remaining | 323 |
| 结论 | **通过**（独立审查；非人工 verified；非全书完成） |
