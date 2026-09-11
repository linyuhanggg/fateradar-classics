# 命理约言 · NLC 恢复本：独立审查 source-reviewed CP2（300–599）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树只读参考权威树；本岗写出仅本文件。未改注解 JSON、未改 `nlc-recovery.md` / `page-reviews.json` / `fulltext.md`、未改主本 `mingli-yueyan.json`、未改 CP1 审查稿、未改六壬/秘本/皇极/飞星紫微/星學大成/奇门 NLC。不是全书完成，也不是人工 `verified`。本岗未参与该 edition 生产。不重做 CP1（0–299，已 done MING-423）；不抢天玉经 / MING-424–427 文件。

结论：**通过（本包 254 SR）。** 结构账本与 ≥15 段非模板 SR 抽样对照恢复稿成立；`source-reviewed` 不是人工 `verified`；图文对照不是人工影印终审。46 条 draft 保持 draft，未升格。下列 caveat / 质量账本不构成本包 254 SR 失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-428`，2026-09-12）：

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
| edition | `nlc-recovery`；源头 `sourceStatus`/恢复说明为 ocr-draft 级；`canonical_eligible` 仍 false；page-reviews 顶层 `verified=false` |
| page-reviews | 185 页：`source-reviewed=27` / `partial=158`；本包 PDF 页 087–134 中仅 **P111** 为整页 `source-reviewed`，其余均为 `partial` |
| 本岗 diff | 仅新增本审查文件；注解 / 源 / 主本 / CP1 审查稿未改 |

无越权文件。源层未改。主本 `mingli-yueyan.json`（540 条、无 edition 字段）与本包 `nlc-recovery` 781 条不是同一索引空间。

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
| 本包 300–599 | 300 | 254 | 46 | 0 |
| remaining 600–780 | 181 | 136 | 45 | 0 |

本包 kind（300）：评注或元数据 145、规则候选 71、理论 61、术语 14、操作步骤 7、序跋目录 2。

SR kind：评注或元数据 99、规则候选 71、理论 61、术语 14、操作步骤 7、序跋目录 2。  
draft kind：评注或元数据 46（**全部**为页级 `page_review` / `running_title` 模板白话「本段为恢复稿PDF第…页的校核状态…」）。

空白话 0；SR 全文 vernacular 重复组（≥3）0；SR `terms=[]` 0。无 `ocr-draft`→SR 越权（条目层无单独 `source_status` 字段；draft 仅落在版面元数据）。46 draft 保持 draft，本审查未升格。

P111（整页 `source-reviewed`）的 `P111:L002-L003` / `P111:L005-L006` 为卷末标题/页码 SR 元数据，**不是** partial 页上的 draft 模板——与 46 条 draft 分流，不混算失败。

## 4. 索引边界

| 位置 | 实测 ID |
|---|---|
| 注解索引 299（CP1 止，不在本包） | `mingli-yueyan:nlc-recovery:P087:L021-L021` |
| 注解/源索引 300（CP2 起） | `mingli-yueyan:nlc-recovery:P087:L023-L023` |
| 注解索引 599（CP2 止） | `mingli-yueyan:nlc-recovery:P134:L005-L005` |
| 源索引 600（下一包起，不在本包） | `mingli-yueyan:nlc-recovery:P134:L007-L008` |
| 全书末条（索引 780） | `mingli-yueyan:nlc-recovery:P185:L005-L005` |

300 条 paragraphId 与源段落库一一对应，`mismatch=0`。未泄漏 0–299 / 600+。remaining **600–780（181，其中 SR 136）** 与 Issue「600–780（181）」一致。起始/止点与 Issue 钉死 ID 一致。

## 5. 抽样语义（≥15 非模板 SR，对照恢复稿）

原文取 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 的页内 `Lxxx`（含空行与 `>` 元行计数）。抽核覆盖运论小注、流年/官杀财印食伤比劫赋、从格小注、合化助破、卷三目录与干合/刑法/太岁论；**不以** 46 条 draft 模板充数。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `P087:L023-L023` | 评注 / sr | 小注「来去」：凶运已去无祸、吉运未至无祥 | 通过 |
| 301 | `P087:L025-L025` | 理论 / sr | 「命吉运凶。若良马坚」跨页起句；notes 标跨页 | 通过 |
| 304 | `P088:L007-L008` | 操作 / sr | 流年赋：岁干岁支、先岁日再岁运、犯岁合岁非自动灾 | 通过 |
| 308 | `P089:L005-L005` | 规则 / sr | 同神因岁建上下不同而喜畏；干支生制加减 | 通过 |
| 315 | `P089:L019-L020` | 术语 / sr | 正官赋：阴阳相异之克；甲辛/乙庚透藏 | 通过 |
| 348 | `P092:L011-L011` | 规则 / sr | 去官两端：用食或伤；非无条件并用 | 通过 |
| 350 | `P092:L015-L015` | 规则 / sr | 合杀宜清；独杀成权/众杀有制仍须日主条件 | 通过 |
| 359 | `P092:L033-L033` | 评注 / sr | 从杀小注：滋根=扶身；只属从格 | 通过 |
| 383 | `P094:L015-L015` | 操作 / sr | 印财先后不拘隅，问日主旺衰 | 通过 |
| 389 | `P095:L007-L008` | 术语 / sr | 正财赋：甲己/乙戊及支藏 | 通过 |
| 397 | `P096:L013-L013` | 规则 / sr | 贪财再逢煞官运；与身强任财官路线不同 | 通过 |
| 400 | `P096:L019-L019` | 评注 / sr | 从财小注：生身反不利仅指弃命从财 | 通过 |
| 401 | `P096:L021-L021` | 理论 / sr | 从杀忌杀生印；从财可财生官杀；喜运表不可混用 | 通过 |
| 409 | `P097:L018-L018` | 序跋 / sr | 「食神赋」标题；正文在次页 | 通过 |
| 420 | `P098:L023-L023` | 评注 / sr | 食多喜枭 / 食少制枭：条件分支非绝对矛盾 | 通过 |
| 445 | `P101:L011-L012` | 术语 / sr | 比劫赋；照录「天干」疑误不擅改；比劫≠禄刃 | 通过 |
| 449 | `P102:L005-L005` | 规则 / sr | 身强添劫；阳日劫可合杀 | 通过 |
| 450 | `P102:L007-L007` | 评注 / sr | 阳日败财皆可合杀；非必然化杀 | 通过 |
| 461 | `P102:L029-L029` | 理论 / sr | 四干整齐「未必便堪欣悦」 | 通过 |
| 488 | `P105:L019-L019` | 评注 / sr | 助化破化：甲己化土与运干配合例 | 通过 |
| 505 | `P107:L013-L013` | 规则 / sr | 破神救应；干支方局轻重无数字权重 | 通过 |
| 521 | `P109:L011-L011` | 理论 / sr | 冲格/合格「果真」「如确」为前提 | 通过 |
| 541 | `P112:L005-L007` | 序跋 / sr | 卷三韦选论四十八篇；篇数≠已实现规则数 | 通过 |
| 550 | `P115:L005-L005` | 理论 / sr | 驳五合性情标签；照录「忘说」不改妄说 | 通过 |
| 566 | `P121:L005-L005` | 理论 / sr | 刑法质疑；新刑表未敢定例；选择性归因 | 通过 |
| 573 | `P124:L005-L005` | 操作 / sr | 旺相休囚作时气进退消息 | 通过 |
| 599 | `P134:L005-L005` | 理论 / sr | 驳独取岁干/犯晦一律凶；天克地冲间有不利 | 通过 |

共 **27** 段非模板 SR 抽核，均通过。关联源行（抽核，非转引进度表）：约 file L1176–L1951（P087–P134 主体）。

## 6. source-reviewed ≠ 人工 verified

edition 恢复头与 page-reviews 顶层均为未 verified / 非整书 canonical。254 条电子语义阅读升 `source-reviewed`，只表示对照恢复稿落实了层次/条件/目录/元数据去向，不是影印逐字终审，也不是预测有效证据。韦选四卷不等于陈氏原十卷。不得把 254 / 614 条 source-reviewed 写成已人工 verified。本包不是命理约言全帙，也不是产品交付。

本包 252/254 条 SR 落在 page-reviews `partial` 页；仅 P111 两条落在整页 `source-reviewed`（卷末无命理正文）。引用须按 page-reviews `reviewedRanges`，不整本/整页抬升。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| **46 draft 页元数据** | 均为 `Pxxx:L002-L003` 模板白话，对应源 `>` page_review / running_title | 保持 draft。不升 SR |
| **P111 例外** | 整页 status=`source-reviewed`；`L002-L003`/`L005-L006` 为卷末标题 SR，非模板 draft | 与 partial 页 draft 分流。不回改 |
| **跨页续句** | 本包至少 5 条 notes 含「跨页」（含包首 `P087:L025`） | 接入须连读邻段。不回改 |
| **比劫赋「天干」疑误** | `P101:L011-L012` notes 已照录不擅改 | 正确保留。不回改 |
| **「忘说」原字** | `P115:L005` 五合性情驳论；notes 保留影印用字 | 不暗改。不回改 |
| **MING-129/139 五段回归** | 仍在权威树为 draft（索引 83/97/131/258/695）；**均不在 CP2** | 只记账；修复另派。本包不充数、不回改 |
| **主本不可代** | `mingli-yueyan.json` 无 nlc-recovery ID | 禁止用主本审查代替本包 |

## Caveat（不改注解，留给后续 pack）

1. **partial 页上的 passage SR**：252 条 SR 所在页 page-reviews 为 `partial`。引用只跟 reviewedRanges，不整页抬升。
2. **跨页续句**：运论、流年、从财等止于页界；白话已声明连读处，单段不可当完整规则卡。
3. **从格 / 合杀 / 助化破化 / 天克地冲**：本版条件分支与异说，不得静默覆盖他派表或写成必然灾祸。
4. **刑法与五合性情**：作者明确质疑/驳斥的内容，不得反向产品化为可执行标签。
5. **MING-129/139 五段回归**仍在包外；协调应另派修复，禁止把本审查当成「五段仍 SR」的证书。

## 未决（本岗不施工）

- 46 draft（页级校核/版心元数据）保持 draft。
- 全书 `canonical_eligible` 仍 false；引用资格按 page-reviews 逐段范围。
- remaining **600–780（181，SR 136）** 留给后续包；本岗不续写、不重做 0–299 / 300–599。
- 不把任何条目标成人工 verified；不 OCR、不补造缺卷、不改注解。
- MING-129/139 五段恢复另派，不在本审查写出范围。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-428`。远端：`linyuhanggg/fateradar-classics`。
