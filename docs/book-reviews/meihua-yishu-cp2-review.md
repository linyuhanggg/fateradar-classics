# 《梅花易数》主本：独立审查 CP2（300–622 收口）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。注解 JSON 已在该钉死树中（blob `0ac958247cd32398b9ccee669dd7ef137cd034ca`，SHA256 与 Issue 一致）。本岗工作树只读该 SHA，写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/meihua-yishu.md` 旧总述、未创建/未改 `meihua-yishu-cp1-review.md`、未改引擎 / `chart.*` / golden / 他书。不是续写，不是人工 verified，不是影印校勘，也不是全项目/产品交付。审查岗未参与本包生产。[MING-297](mention://issue/01a090b1-9c60-7e59-9c1b-b002fb24e71f) 独占 CP1（0–299）；本包不抢写。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；维基文库电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。本包后本 edition remaining **0**（623/623 均已独立审查覆盖：CP1 0–299 + CP2 300–622）；仍不是人工 verified。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-298`，2026-09-11）：

```
git rev-parse HEAD
shasum -a 256 references/annotations/divination/meihua-yishu.json
shasum -a 256 sources/fulltext/divination/meihua-yishu/fulltext.md
git rev-parse HEAD:references/annotations/divination/meihua-yishu.json
git rev-parse HEAD:sources/fulltext/divination/meihua-yishu/fulltext.md
cmp HEAD blob vs working tree (annotations)
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / 钉死权威 SHA | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 注解 SHA256 | `790969e2bbbedcc0695cc57458f12473839b8d5332e51459bcd6147715d24374`（与 Issue 钉死值一致） |
| 注解 blob | `0ac958247cd32398b9ccee669dd7ef137cd034ca` |
| working tree vs `HEAD` 注解 blob | 相同 |
| 源 `fulltext.md` SHA256 | `220aeb83f087ec4085c9ecf8e8381f0db51cd5376ccb1f3ce14943d8c14d6f50` |
| 源 blob | `902a968091fbaf8f039f0d2268bb19f022753962` |
| `scopeNote` | 按现存维基文库通行电子本文字逐稳定段整理；`source-reviewed` 只表示对照电子原文，非影印逐字核验或预测有效性证明 |
| 注解 ID 与 `references/inventory/paragraphs/divination/meihua-yishu.json` | 623/623 一一对应，`mismatch=0`；CP2 kind 差=0 |
| 本岗改动文件 | 仅新增 `docs/book-reviews/meihua-yishu-cp2-review.md` |
| `meihua-yishu-cp1-review.md` | 本树不存在，未创建、未改 |

无越权文件。源层未改。注解 JSON 未改。CP1 审查文件未抢写。

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

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书与本包均无 `verified: true`（字段缺省）。

## 3. verified / draft 未越权提升

623 条：`review=source-reviewed` 全 623；`verified` 字段缺省 623（按 false 计 true=0）；`draft` 0。无升 verified。

kind 全书累计：规则候选 207、术语 188、操作步骤 51、理论 48、序跋目录 37、案例 37、待核实 32、评注或元数据 23。

本包 CP2（300–622，323 条）：`review=source-reviewed` 全 323；`verified` 缺省 323。kind：规则候选 119 / 术语 66 / 理论 38 / 待核实 23 / 操作步骤 23 / 评注或元数据 20 / 案例 18 / 序跋目录 16。

空白白话 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。`terms` 非空 323/323。`notes` 空 197（术语 47 / 规则候选 79 / 理论 18 / 评注 18 / 序跋 15 / 操作 8 / 案例 8 / 待核实 4；短表项与卷题以 terms+vernacular 自足，不构成本包失败）。inventory `doubtful`/`missing_marker` 本包均为 0。注解 kind 与 inventory kind 300–622 差=0。

## 4. 索引 0–299 相对权威 SHA 未改

本岗 HEAD 即权威 SHA，working tree 注解字节与 `HEAD` blob 相同，故 0–299 相对钉死 SHA 未改。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起，不评） | `meihua-yishu:L0005-L0005` |
| 注解索引 299（CP1 止，不评） | `meihua-yishu:L0905-L0905` |
| 0–299 paragraphId 集 SHA256 | `5e0bede9fadfbd8e8ac3223488bf4918d743b10e072a2677f75c0d8008a65d79` |

CP1 300 条同样 `source-reviewed` / `verified` 缺省。本包不评其语义，不写 `meihua-yishu-cp1-review.md`。

## 5. 索引边界（本包 300–622 收口）

| 位置 | 实测 ID | inventory heading |
|---|---|---|
| 注解索引 300（CP2 起） | `meihua-yishu:L0907-L0907` | 八卦萬物屬類 |
| 注解索引 622（CP2 / 本 edition 止） | `meihua-yishu:L2557-L2557` | 卦應（與前八卦類象，大同小異，觀者可以互參） |

起讫与 Issue 钉死 locator 一致。本包后本 edition remaining **0**。

CP2 覆盖：八卦万物属类续（离味→艮/兑分项与类推收束）→ 占卜总诀与体用断事（婚、病、饮食等）→ 外应（草木/人事等）→ 卷三断占/体用互变/辨物 → 坐端与观物歌诀案例 → 十应与十大应现场姿态 → 卦应表收口（止 `L2557` 兑卦应）。

## 6. 抽样语义（26 段非模板，对照原文，不凭旧总述/CP1 报告）

原文取 `sources/fulltext/divination/meihua-yishu/fulltext.md` 的 `start_line–end_line`。下列覆盖属类续表、规则、理论、操作、案例、评注、十应与待核实。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L0907-L0907` | 术语 / sr | 「五味：苦。」接离属类；白话限味觉项，不扩成全卦 | 通过 |
| 301 | `L0909-L0909` | 序跋 / sr | `'''艮卦'''` 表头；开始艮分项，不并入兑 | 通过 |
| 310 | `L0927-L0927` | 规则 / sr | 艮时序：冬春、丑寅、七五十、土类并列；白话禁止把不同层次标签直接相加当应期 | 通过 |
| 333 | `L0973-L0973` | 待核实 / sr | 「兌為金…澤山鹹」卦名与五行混写；保留原字并注通行兑/咸，不覆写 | 通过 |
| 350 | `L1007-L1007` | 规则 / sr | 兑出行：不宜远行/口舌损失 vs 西行秋占有利，分条件并存 | 通过 |
| 362 | `L1031-L1031` | 理论 / sr | 「庶事之多不止於此…各以其類而推之」；类推须有依据，不把新猜冒充表内原文 | 通过 |
| 365 | `L1056-L1056` | 操作 / sr | 成卦先看爻辞（乾初九/九二例）；notes 标明非全书路径均强制先看爻辞 | 通过 |
| 400 | `L1255-L1255` | 规则 / sr | 占婚：体为本家、用为所婚之家；旺衰/生克分层；不固定按男女分配体用；嫁奁属古代语境 | 通过 |
| 411 | `L1295-L1295` | 评注 / sr | 饮食人事类回查前文万物属类，不另造字典 | 通过 |
| 426 | `L1391-L1391` | 案例 / sr | 乾上坤下初爻动→震，互巽艮，占病「逢生之日即愈」；保留卦形事实，不伪造日期、不把「即愈」当验证结果 | 通过 |
| 450 | `L1532-L1532` | 规则 / sr | 草木外应芝兰/松柏/苗菰等；notes 禁止以草木象判母婴或病人生死 | 通过 |
| 474 | `L1608-L1608` | 理论 / sr | 人事外应两路：归卦五行 vs 事情情状；不可混成「见某类人必吉凶」 | 通过 |
| 500 | `L1908-L1908` | 序跋 / sr | `=卷三=` 卷题；后续断占/体用/辨物 | 通过 |
| 509 | `L1948-L1948` | 案例 / sr | 履体用金、互木火、变乾；无起卦数则不补日期 | 通过 |
| 531 | `L2060-L2060` | 操作 / sr | 坐端：以所坐为中、八方应兆与体用生克；须固定坐标 | 通过 |
| 539 | `L2076-L2076` | 评注 / sr | 「奇占巧卜者，则在乎人」仅为引端；不扩成任意联想规则 | 通过 |
| 550 | `L2254-L2263` | 理论 / sr | 观物戏验：形色性位、乾刚坤柔及配兑坎离震巽坤艮条件；猜物线索≠唯一编码 | 通过 |
| 568 | `L2401-L2401` | 案例 / sr | 鼎变恒、鼎玉铉、互乾兑→玉绦环破；叙事揭物≠独立预测验证 | 通过 |
| 575 | `L2452-L2452` | 序跋 / sr | 「變應」十应小标题 | 通过 |
| 587 | `L2476-L2476` | 规则 / sr | 天时应：晴离/雨坎/风巽/雷震；与「天时不分体用」分路；「火见雷为比和」与常行五行异，保留待校不改比和定义 | 通过 |
| 590 | `L2482-L2482` | 序跋 / sr | 「人事應」标题 | 通过 |
| 591 | `L2484-L2484` | 操作 / sr | 人事应：笑哭辅象 + 人物归卦再与体比；不由他人哭笑证明问事者同事件 | 通过 |
| 600 | `L2504-L2504` | 待核实 / sr | 跣足；「病有孝至」主客不清，不补谁必有丧 | 通过 |
| 613 | `L2539-L2539` | 待核实 / sr | 乾疾病「于太阳脉弦紧…目熟」电子句不通顺；保留历史病象，不作医学处置 | 通过 |
| 620 | `L2553-L2553` | 术语 / sr | 艮卦应列至「其於木也、為」中断；notes 标明接续「坚多节」，非类象缺失 | 通过 |
| 622 | `L2557-L2557` | 术语 / sr | 兑卦应泽/少女/巫/口舌/毁折/附决/刚卤/妾/羊；本 edition 止此 | 通过 |

关键条件与源行（抽核）：

- 离苦味 / 艮表头 / 艮时序：L0907–L0927
- 兑宫混写待核、兑出行、类推边界：L0973–L1031
- 占卜总诀先看爻辞、占婚体用：L1056–L1255
- 饮食类象索引、否卦初动案例：L1295–L1391
- 草木外应、人事两路：L1532–L1608
- 卷三、履变乾简式、坐端、八端引例：L1908–L2076
- 观物歌诀、鼎变恒揭物：L2254–L2401
- 变应 / 天时应 / 人事应：L2452–L2484
- 十大应跣足、乾疾病待核、艮/兑卦应收口：L2504–L2557

## 7. source-reviewed ≠ 人工 verified

主本为维基文库通行电子本。本包 323 条电子语义阅读升/保持 `source-reviewed`，只表示对照电子段落实了条件/边界/疑点，不是影印逐字校勘，也不是预测有效证据。案例多 `expected` 缺省或显式不把叙事揭物当验证。不得把 623 条 source-reviewed 写成已人工 verified。本包收口本 edition remaining 0，仍不是人工 verified，也不是全项目完成。

## 8. Caveat（不构成本包失败）

1. `source-reviewed` ≠ 人工 `verified`；维基电子本 ≠ 影印校勘。
2. 本包 23 条 `待核实` 已显式保留疑点，未静默改字或升 verified。代表项：`L0973` 兑宫金/鹹混写；`L1944`/`L1952`/`L1958`/`L1964`/`L1970` 卷三表图/变卦对应不清；`L1991` 观梅恒卦与前革例冲突；`L2199`/`L2238` 饮食取象电子残句；`L2273`/`L2275` 观物标题与对象错位或语意中断；`L2490`–`L2508` 十大应条件省略；`L2537`/`L2539` 乾上下位与疾病栏文字不通顺。
3. `notes` 空 197 多为属类短表/卷题；白话与 terms 仍非空，无模板填充。
4. `L2476`「火见雷为比和」与常行震木生离火并存；注解保留待校，不改产品比和定义。
5. 索引 0–299 属 MING-297；本包确认未改、不评语义、不写 CP1 文件。

## 9. 交付账本

| 项 | 值 |
|---|---|
| Issue | MING-298 |
| 工作树 | `fateradar-multica-ming-298` |
| 分支 | `codex/multica-ming-298` |
| 基线 SHA | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 写出 | 仅 `docs/book-reviews/meihua-yishu-cp2-review.md` |
| 注解改动 | 无 |
| validator | `ok=true` entries=623 source_reviewed=623 errors=[] |
| CP2 范围 | 300–622 = `L0907` … `L2557` |
| 本 edition remaining | **0** |
| 结论 | **通过**（独立审查；非人工 verified；非影印校勘；非全书人工完成） |
