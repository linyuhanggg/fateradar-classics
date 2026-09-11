# 命理约言 · NLC 恢复本：独立审查 source-reviewed CP1（0–299）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树只读参考权威树；本岗写出仅本文件。未改注解 JSON、未改 `nlc-recovery.md` / `page-reviews.json` / `fulltext.md`、未改主本 `mingli-yueyan.json`、未改六壬/秘本/皇极/飞星紫微/星學大成/奇门 NLC。不是全书完成，也不是人工 `verified`。本岗未参与该 edition 生产。主本与仅 5 段的 MING-129/139 **不能**代替本包。

结论：**通过（本包 224 SR）。** 结构账本与 ≥15 段非模板 SR 抽样对照恢复稿成立；`source-reviewed` 不是人工 `verified`；图文对照不是人工影印终审。76 条 draft 保持 draft，未升格。下列 caveat / 质量账本不构成本包 224 SR 失败，也不把任何条升 verified。本岗未改注解。

**具名回归（不重做、不回改）：** MING-129/139 已审五段在本权威树相对 `be137a1` **已回改为 draft 模板**（全书 SR 619→614）。本包不以这五段充数；只记账，留给后续修复 Issue。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-423`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/bazi/mingli-yueyan--nlc-recovery.json
shasum -a 256 sources/normalized/bazi/mingli-yueyan/nlc-recovery.md
shasum -a 256 sources/fulltext/bazi/mingli-yueyan/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/mingli-yueyan--nlc-recovery.json --json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与本岗 HEAD / Issue 钉死一致） |
| 注解 SHA256 | `d23db1d8e2df46c63224e573b0a1466a9632bff71cbf13324f8053058f5a0be6`（与 Issue 一致） |
| 源 `nlc-recovery.md` SHA256 | `7bd1425da62c9ca202e251ad4e06182c2c84e56818802b43be946bcf3a5e9b25` |
| 源 `fulltext.md` SHA256 | `c71948c2dffa79257cf4ca2c5c0d4897c80ee830262dae86ad9be00fd7397b73`（对照用，非本包写入口） |
| 注解 blob | `4877af70002217fded78e17cecb3564e1b772d4c` |
| `be137a1` 同路径 blob | `b78b2aaed02653306fa546b763445131053a98ea`（**不同**；见 §7） |
| edition | `nlc-recovery`；`sourceStatus=ocr-draft`；`pageScoped=true`；`canonical_eligible` 仍 false（见 P000 元数据） |
| page-reviews | 顶层 `verified=false`；185 页：`source-reviewed=27` / `partial=158` |
| 本岗 diff | 仅新增本审查文件；注解 / 源 / 主本未改 |

无越权文件。源层未改。主本 `mingli-yueyan.json`（540 条、无 edition 字段、ID 形如 `mingli-yueyan:L…`）与本包 `nlc-recovery` 781 条不是同一索引空间。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/mingli-yueyan--nlc-recovery.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 781, "source_reviewed": 614,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`errors=[]`。

## 3. verified / draft 未越权提升

| 范围 | entries | source-reviewed | draft | verified=true |
|---|---|---|---|---|
| 全书 | 781 | 614 | 167 | 0（781 条均无 `verified` 键） |
| 本包 0–299 | 300 | 224 | 76 | 0 |
| remaining 300–780 | 481 | 390 | 91 | 0 |

本包 kind（300）：理论 75、规则候选 46、评注或元数据 120、序跋目录 33、操作步骤 13、术语 12、待核实 1。

CP1 段落层 `source_status`：`passage-reviewed` 172 / `page-reviewed` 56 / `ocr-draft` 72。SR 仅落在 `passage-reviewed`（172）与 `page-reviewed`（52）；**无** `ocr-draft`→SR。76 draft = 72 ocr-draft + 4 page-reviewed（含已回改的 MING-129 四条，见 §7）。

空白话 0；SR 全文 vernacular 重复组（≥3）0。draft 中 71 条仍含「本段为恢复稿PDF第…页的校核状态…」模板句——保持 draft，本审查未升格。

待核实仅 `mingli-yueyan:nlc-recovery:P001:L005-L005`（封面缺字「精選命〔題名字跡缺失〕約言」），review=draft，不冒充认出「理」字。

## 4. 索引边界

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（CP1 起） | `mingli-yueyan:nlc-recovery:P000:L003-L011` |
| 注解索引 299（CP1 止） | `mingli-yueyan:nlc-recovery:P087:L021-L021` |
| 源索引 300（下一包起，不在本包） | `mingli-yueyan:nlc-recovery:P087:L023-L023` |
| 全书末条（索引 780） | `mingli-yueyan:nlc-recovery:P185:L005-L005` |

300 条 paragraphId 与源段落库一一对应，`mismatch=0`。未泄漏 300+。remaining **300–780（481，其中 SR 390）** 与 Issue 一致。起始/止点与 Issue 钉死 ID 一致。

## 5. 抽样语义（≥15 非模板 SR，对照恢复稿，不含 MING-129/139 五段）

原文取 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 的 `start_line–end_line`。抽核覆盖序跋/目录、操作步骤、术语、理论、规则候选、评注小注、包尾运论；**不以**已回改的五段元数据充数。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 3 | `P001:L007-L007` | 评注 / sr | 源「許世英題」。仅题署，不是理论 | 通过 |
| 6 | `P002:L005-L006` | 序跋 / sr | 袁序：陈之遴/素庵、原十卷、见二卷后再得缺卷本。选四卷≠原十卷 | 通过 |
| 10 | `P004:L005-L005` | 序跋 / sr | 韦选加注二十赋、删杂论；补录凡例。版本判断，不抬全书 | 通过 |
| 40 | `P013:L005-L028` | 序跋 / sr | 卷一目录后半：禄刃至小儿命法。目录含采用与驳论导航 | 通过 |
| 43 | `P014:L005-L018` | 序跋 / sr | 卷二赋目录余项：财印食伤、从化、女命等 | 通过 |
| 56 | `P018:L008-L009` | 操作 / sr | 看命总法：日干月支、本气透干、扶抑；禄刃不取格。末句跨页 | 通过 |
| 58 | `P019:L004-L004` | 理论 / sr | 弃/顺；合化、一气两神、暗冲合例外；驳奇正按时世固定搭配 | 通过 |
| 63 | `P020:L009-L011` | 术语 / sr | 正官兼印=官印格、兼财=财官格。名称≠条件完备 | 通过 |
| 68 | `P021:L018-L020` | 术语 / sr | 食神制杀 / 食神生财。路线不同 | 通过 |
| 70 | `P021:L026-L031` | 规则 / sr | 从官/财/伤/杀/食五类表；无根满局仍须核实 | 通过 |
| 80 | `P023:L019-L024` | 规则 / sr | 暗合表：甲辰多辰合酉等四式称合官格；虚邀仍须查实神/冲合排除 | 通过 |
| 84 | `P024:L005-L005` | 理论 / sr | 暗神助破格；从化/一行/两神欲清欲虚。同页 L002 元数据**不**在本抽核充数 | 通过 |
| 98 | `P029:L005-L005` | 理论 / sr | 藏气不可分日；驳 365 vs 372。数字照图保留疑点 | 通过 |
| 117 | `P032:L007-L008` | 操作 / sr | 看生时法：归宿、喜忌引至时上；过旺喜神可制泄 | 通过 |
| 119 | `P033:L005-L005` | 理论 / sr | 时要紧≠只按时取格；须合全柱 | 通过 |
| 132 | `P037:L005-L005` | 规则 / sr | 看官：财印正偏搭配；官多食伤仍不作杀；从官≠从杀；驳张神峰月令官不可用 | 通过 |
| 138 | `P039:L007-L008` | 规则 / sr | 官杀去留：轻重不对称；两停再看食伤 | 通过 |
| 171 | `P052:L007-L008` | 术语 / sr | 禄=纯粹、刃=刚暴；阴刃在寅申巳亥；驳阴无刃/辰戌丑未阴刃 | 通过 |
| 182 | `P056:L005-L005` | 规则 / sr | 墓神透干不必刑冲；强弱开库 vs 克倒；土本无墓库 | 通过 |
| 188 | `P058:L007-L008` | 操作 / sr | 看化局：先查真化再改生克；合≠立刻改写十神。跨页 | 通过 |
| 224 | `P071:L005-L005` | 理论 / sr | 和平≠安静；人事可改吉凶结果。不是公式 | 通过 |
| 266 | `P084:L016-L016` | 评注 / sr | 小注：七杀=偏官；「反是」指阴阳非生克 | 通过 |
| 295–299 | `P087:L013…L021` | 规则/评注/理论 / sr | 运重支须合干；一运干支互害/互助；神煞缓于实在干支；驳交运必咎；离任/候选官喻运界 | 通过 |

关键源行（抽核，非转引进度表）：

- 许世英题：约 L20
- 袁序十卷/二卷：约 L29–30
- 韦选删注凡例：约 L44
- 卷一目录后半：约 L168–191
- 卷二赋目录：约 L206–219
- 看命总法：约 L309–310
- 弃顺/奇正：约 L316
- 正官兼印兼财：约 L330–332
- 食神制杀生财：约 L352–354
- 从格五类：约 L360–365
- 暗神助破格：约 L（P024 正文）
- 分日不可拘 / 365·372：约 L（P029）
- 看生时 / 全柱取格：约 L586–594
- 看官法：约 L（P037）
- 官杀去留：约 L656–657
- 比劫禄刃 / 阴刃：约 L769–770
- 墓库开库克倒：约 L806
- 看化局：约 L825–826
- 和平安静：约 L946
- 偏官/反是小注：约 L1097
- 运论与交运俗说、离任喻：约 P087 L13–L21（本包止）

## 6. source-reviewed ≠ 人工 verified

edition `sourceStatus=ocr-draft`，page-reviews 顶层 `verified=false`。224 条电子语义阅读升 `source-reviewed`，只表示对照恢复稿落实了层次/条件/目录/元数据去向，不是影印逐字终审，也不是预测有效证据。韦选四卷不等于陈氏原十卷。不得把 224 / 614 条 source-reviewed 写成已人工 verified。本包不是命理约言全帙，也不是产品交付。

大量 SR 落在 page-reviews `partial` 页上的 `passage-reviewed` 段：局部范围可引，**整页**仍非全页 source-reviewed。引用须按 page-reviews `reviewedRanges`，不整本抬升。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| **MING-129/139 五段回改** | `be137a1` 五条均为 `source-reviewed`（非模板页特异白话）；本树同 ID 均为 `draft`，白话回到「本段为恢复稿PDF第…页的校核状态…」模板。SR 计数 619→614。ID：`P024:L002-L003`、`P029:L002-L003`、`P037:L002-L003`、`P083:L002-L002`、`P163:L002-L002`（末条在索引 695，不在 CP1） | **具名回归。** 不重做、不改 JSON。后续修复 Issue 应以 `be137a1` / MING-139 审查稿为准恢复，勿从 CP1 再写一遍 |
| 同页正文未吞 | P024/P029/P037 的 `L005` 正文仍为 SR，内容与源一致 | 元数据回改未抹掉同页理论/规则。不回改 |
| draft 模板 71 | CP1 内「本段为恢复稿PDF第…」 | 保持 draft。不升 SR |
| P001 封面缺字 | `待核实` + draft；不补「理」 | 正确保留 unknown |
| P014:L002-L003 | 源为 page_review/running_title；白话概括页在目录卷界中的位置 | 页级去向，略宽于两行元数据。不据此失败 |
| SR 空 terms | 2 条 terms=[] | 结构合法。不回改 |
| 跨页截断 | 看命总法、看生时、看化局、看官等多处 notes 已标跨页 | 接入须连读邻段。不回改 |
| 主本不可代 | `mingli-yueyan.json` 540 条 / 无 nlc-recovery ID | 禁止用主本审查代替本包 |

## Caveat（不改注解，留给后续 pack）

1. **MING-129/139 五段回归**：本权威树相对已审 tip 回改为 draft 模板。协调应开修复包（或并入下一注解写出岗）按原五 ID 恢复；**禁止**把本审查当成「五段仍 SR」的证书。
2. **partial 页上的 passage-reviewed**：172 条 SR 所在页 page-reviews 为 `partial`。引用只跟 reviewedRanges，不整页抬升。
3. **跨页续句**：总法、生时、化局、官杀去留等止于页界；白话已声明连读，单段不可当完整规则卡。
4. **P029 365/372**：源内算术疑点已保留；source-reviewed 只确认归属，不静默改数。
5. **阴刃 / 从格五类 / 土无墓库**：本版异说，不得静默覆盖他派表。

## 未决（本岗不施工）

- 76 draft（封面缺字、馆藏/版面元数据、回改的四条 page 元数据 + 包外 P163）保持 draft。
- 全书 `canonical_eligible` 仍 false；引用资格按 page-reviews 逐段范围。
- remaining **300–780（481，SR 390）** 留给后续包；本岗不续写、不重做 0–299。
- 不把任何条目标成人工 verified；不 OCR、不补造缺卷、不改注解。
- MING-129/139 五段恢复另派，不在本审查写出范围。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-423`。远端：`linyuhanggg/fateradar-classics`。
