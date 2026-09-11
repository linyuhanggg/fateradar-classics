# 命理约言 · NLC 恢复本：独立审查 source-reviewed CP3（600–780 收尾）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树只读参考权威树；本岗写出仅本文件。未改注解 JSON、未改 `nlc-recovery.md` / `page-reviews.json` / `fulltext.md`、未改主本 `mingli-yueyan.json`、未改 CP1/CP2 审查稿、未改六壬/秘本/皇极/飞星紫微/星學大成/奇门 NLC/天玉经。不是全书人工 `verified`，也不是产品交付。本岗未参与该 edition 生产。不重做 CP1（0–299，已 done MING-423）或 CP2（300–599，已 done MING-428）；不抢天玉经 / MING-424/426/427/431 文件；不在本包回写 MING-129/139 五段 JSON。

结论：**通过（本包 136 SR）。** 结构账本与 ≥15 段非模板 SR 抽样对照恢复稿成立；`source-reviewed` 不是人工 `verified`；图文对照不是人工影印终审。45 条 draft 保持 draft，未升格。下列 caveat / 质量账本不构成本包 136 SR 失败，也不把任何条升 verified。本岗未改注解。全书 SR 审查收尾后 remaining **0**（仅就本 edition 的 SR 审查队列而言；draft 回改与 verified 另派）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-435`，2026-09-12）：

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
| edition | `nlc-recovery`；源头 `verified=false` / `canonical_eligible=false`；page-reviews 顶层 `verified=false` |
| page-reviews | 185 页：`source-reviewed=27` / `partial=158`；本包 PDF 页 134–185 中整页 `source-reviewed` 为 **P163、P180–P185**（7 页），其余均为 `partial` |
| 本岗 diff | 仅新增本审查文件；注解 / 源 / 主本 / CP1/CP2 审查稿未改 |

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
| 本包 600–780 | 181 | 136 | 45 | 0 |
| remaining（本包后） | 0 | — | — | — |

本包 kind（181）：理论 80、评注或元数据 69、规则候选 11、案例 11、序跋目录 5、术语 3、操作步骤 2。

SR kind：理论 80、评注或元数据 24、规则候选 11、案例 11、序跋目录 5、术语 3、操作步骤 2。  
draft kind：评注或元数据 45（**全部**为页级 `page_review` / `running_title` 模板白话「本段为恢复稿PDF第…页的校核状态…」）。

空白话 0；SR 全文 vernacular 重复组（≥3）0；SR `terms=[]` 仅 2 条（P163 卷末题记/页码元数据，合理）。无 draft→SR 越权升格。45 draft 保持 draft，本审查未升格。

整页 `source-reviewed` 上的卷末/跋/广告元数据（见 §7）是 **SR 元数据**，不是 partial 页上的 draft 模板——与 45 条 draft 分流，不混算失败。

## 4. 索引边界

| 位置 | 实测 ID |
|---|---|
| 注解索引 599（CP2 止，不在本包） | `mingli-yueyan:nlc-recovery:P134:L005-L005` |
| 注解/源索引 600（CP3 起） | `mingli-yueyan:nlc-recovery:P134:L007-L008` |
| 注解索引 780（CP3 / 全书止） | `mingli-yueyan:nlc-recovery:P185:L005-L005` |

181 条 paragraphId 均可按 `Pxxx:Laaa-Lbbb` 从 `nlc-recovery.md` 对应 PDF 页相对行抽出，`extract miss=0`。未泄漏 0–299 / 300–599。起始/止点与 Issue 钉死 ID 一致。关联源行约 file L1946–L2517（PDF 第 134–185 页）。本包后 SR 审查 remaining **0**。

## 5. 抽样语义（≥15 非模板 SR，对照恢复稿）

原文取 `sources/normalized/bazi/mingli-yueyan/nlc-recovery.md` 的页内 `Lxxx`（含空行与 `>` 元行计数）。抽核覆盖卷三神煞诸论、干支一气案例、卷四杂论/调候引化、操作前提与术语统一、后跋与末页元数据；**不以** 45 条 draft 模板充数。另抽 2 条整页 SR 卷末元数据以核分流口径。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 600 | `P134:L007-L008` | 理论 / sr | 月煞论：反每月神煞断吉凶；主张月干支+时令；「月将」同名异义须区分 | 通过 |
| 602 | `P135:L005-L005` | 理论 / sr | 流日流时过细则穿凿；精度自我限制 | 通过 |
| 603 | `P135:L007-L008` | 规则 / sr | 天月二德起例；四仲月不论天德；勿静默改通用神煞表 | 通过 |
| 606 | `P136:L007-L008` | 规则 / sr | 天乙贵人夏至后/冬至后两套临支；非双贵并查表 | 通过 |
| 609 | `P137:L007-L008` | 规则 / sr | 月将=中气后太阳躔次；雨水后–春分前取亥例 | 通过 |
| 611 | `P138:L005-L005` | 规则 / sr | 月将遇空亡仍不以空论；例外不可扩到全部神煞 | 通过 |
| 615 | `P139:L007-L008` | 规则 / sr | 日旬空亡；真空/半空与「减十之七/三」为传统说法非现代概率 | 通过 |
| 618 | `P140:L007-L008` | 术语 / sr | 劫煞论起句；与亡神同列≠最终都采用 | 通过 |
| 624 | `P142:L007-L008` | 序跋 / sr | 神趣八法目录起句；不可八名皆当新算法 | 通过 |
| 627 | `P143:L007-L008` | 术语 / sr | 大小运定义起句；小运取舍在续页 | 通过 |
| 632 | `P145:L005-L005` | 案例 / sr | 四甲戌结构推演；运变财官伤；非整整齐齐即贵 | 通过 |
| 635 | `P145:L011-L011` | 案例 / sr | 四丁未；食神生财流通 vs 火土燥 | 通过 |
| 640 | `P145:L021-L021` | 案例 / sr | 四壬寅；食财流通与申冲食支 | 通过 |
| 699 | `P164:L005-L007` | 序跋 / sr | 卷四杂论二十四则+张神峰附十一则；附录须分署 | 通过 |
| 707 | `P167:L005-L005` | 规则 / sr | 盖头：柱干论令、运支论方；同元素不同方位 | 通过 |
| 713 | `P168:L009-L009` | 规则 / sr | 寒暖燥湿；夏水须成象通根；「化囚为生」照录 | 通过 |
| 716 | `P169:L007-L007` | 规则 / sr | 引化：官杀→印、食伤→财；财印太强不可照搬 | 通过 |
| 734 | `P173:L007-L007` | 操作 / sr | 先问六亲履历再推；不知背景勿妄断 | 通过 |
| 735 | `P173:L009-L009` | 术语 / sr | 官≠日禄、财≠驿马；少用生肖代干支 | 通过 |
| 741 | `P175:L005-L005` | 操作 / sr | 收集命例编底本；非现代验证方案 | 通过 |
| 761 | `P180:L005-L006` | 序跋 / sr | 后跋：星命存废立场；≠科学证实证书 | 通过 |
| 764 | `P181:L005-L005` | 序跋 / sr | 跋文赞《约言》与韦氏刊行；≠规则验证 | 通过 |
| 696 | `P163:L004-L004` | 评注 / sr | 卷三卷末题记；整页 SR；非 draft 模板 | 通过 |
| 697 | `P163:L006-L006` | 评注 / sr | 印刷页码「五二」；纸本索引元数据 | 通过 |
| 780 | `P185:L005-L005` | 评注 / sr | 末页 facsimile_note 数字 1；非原书句子 | 通过 |

共 **25** 段 SR 抽核（含 22 非模板正文/跋 + 3 卷末/末页元数据分流核），均通过。

## 6. source-reviewed ≠ 人工 verified

edition 恢复头与 page-reviews 顶层均为未 verified / 非整书 canonical。136 条电子语义阅读升 `source-reviewed`，只表示对照恢复稿落实了层次/条件/案例/操作/元数据去向，不是影印逐字终审，也不是预测有效证据。韦选四卷不等于陈氏原十卷。不得把 136 / 614 条 source-reviewed 写成已人工 verified。本包是该书 SR 审查收尾，**不是**命理约言人工终审完成，也不是产品交付。

本包 113/136 条 SR 落在 page-reviews `partial` 页；23 条落在整页 `source-reviewed`（P163 卷末、P180–185 跋/广告/末页）。引用须按 page-reviews `reviewedRanges`，不整本/整页抬升。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| **45 draft 页元数据** | 均为 `Pxxx:L002-L003`（或同类）模板白话，对应源 `>` page_review / running_title | 保持 draft。不升 SR |
| **整页 SR 元数据例外** | P163 题记/页码；P180–185 的 L002–L003 page_review 行及 P185 facsimile_note 为 SR，非 partial 页 draft 模板 | 与 draft 分流。不回改 |
| **reviewedRanges 空/未覆盖 9 条** | 696/697（P163 rr=[]）、760/763/766/771/775（跋广告页 L002–L003）、779/780（P185） | 属整页 SR 版面元数据；引用仍不得当命理证据。不回改 |
| **「化囚为生」原字** | `P168:L009` notes 照录 | 正确保留。不回改 |
| **MING-129/139 五段** | 索引 83/97/131/258/**695** 仍为 draft；**695 在本包**（`P163:L002-L002`） | 只记账；修复另派。本包不充数、不回写 JSON |
| **主本不可代** | `mingli-yueyan.json` 无 nlc-recovery ID | 禁止用主本审查代替本包 |

## Caveat（不改注解，留给后续 pack）

1. **partial 页上的 passage SR**：113 条 SR 所在页 page-reviews 为 `partial`。引用只跟 reviewedRanges，不整页抬升。
2. **神煞异说**：天月二德四仲月、天乙贵人分至、月将空亡例外、真空半空比例等，不得静默覆盖产品通用表或写成数值权重。
3. **结构案例无署名人名/公历**：四柱整齐例仅为推演，不作历史事件验证。
4. **后跋/广告/润例/牌记**：即使整页 source-reviewed，也不得作命理或预测证据。
5. **MING-129/139 五段回归**（含本包索引 695）仍为 draft；协调应另派修复，禁止把本审查当成「五段已 SR」的证书。

## 未决（本岗不施工）

- 45 draft（页级校核/版心元数据）保持 draft；全书另有包外 draft（含五段回归）另派。
- 全书 `canonical_eligible` 仍 false；引用资格按 page-reviews 逐段范围。
- SR 审查 remaining **0**；不宣称人工 verified / 全书完成 / 可上产品。
- 不 OCR、不补造缺卷、不改注解、不回写 129/139 五段。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-435`。远端：`linyuhanggg/fateradar-classics`。
