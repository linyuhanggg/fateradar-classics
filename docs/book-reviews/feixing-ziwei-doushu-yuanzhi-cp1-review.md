# 飛星紫微斗數原旨：独立审查主本 source-reviewed CP1（0–299）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-417` / 分支 `codex/multica-ming-417`。本岗写出仅本文件。未改注解 JSON、未改 `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md`、未改 SDZJ0170 / 主本紫微引擎 / chart / 六壬 / 秘本 / 皇极 / CP2 审查稿。本岗（资料工程师 A）未参与飞星紫微原旨生产。不是飞星紫微斗数原旨全书完成，也不是引擎包，也不是全项目完成。

查重：同 SHA / 同文件范围已有 [MING-344](mention://issue/01a0910d-9c10-7759-97b4-9cc038580e60) done（`018d27d`）。本 Issue 为另一岗独立复审确认，不重做注解生产，不回改 JSON。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；OCR 电子主文本不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–335 remaining **36** 不在本包（CP2 已由他岗审查，本岗不抢）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-417`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
shasum -a 256 sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md
git rev-parse HEAD:references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
git status --short references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95`（与 Issue 钉死一致） |
| 注解 blob | `9f713a371b7059b2986321c12933a2ceb96c5766` |
| 源 `fulltext.md` SHA256 | `3a103d51839ff9a150c4b1b21a13c1d4866ca0c6327d19cd332e0f9e842436cb` |
| `sourceFile` | `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md` |
| 头信息 `source_status` | `ocr_reviewed_complete_candidate`（L3–L4） |
| `reviewScope` | 至 page-116；全书 336 段电子语义注解已尽；明确 source-reviewed ≠ 影印人工核验 |
| 工作区注解 JSON | `git status --short` 空（本岗未改） |
| 独占写出 | 仅本审查稿；未触六壬/秘本/皇极/CP2 审查稿 |

无越权文件。源层未改。注解 JSON 未改。

## 2. 校验器独立复跑

对本岗树 `6effd8e`：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 336, "source_reviewed": 336,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

本包 300 条（索引 0–299）：`review=source-reviewed` 全 300；`verified` 全 `false`；无 `draft`。全书 336 条同样 `verified` 全 false、`source-reviewed` 全 336。无升 verified。

kind（本包）：理论 180、评注或元数据 106、序跋目录 9、案例 5。

空白话 0、空 notes 0、空 terms 0。白话全文完全重复组 0。未见「本段论述 / 白话从略 / 见原文 / TODO」类空模板。`relatedParagraphIds` 非空 300/300。注解 span 两两无重叠；相邻 span 间隙最大 4 行（页间空行/标题骨架，可接受）。

## 4. 索引边界

全书注解 336 条；本包只审 0–299。起止与 Issue 钉死一致。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起） | `feixing-ziwei-doushu-yuanzhi:L0003-L0004` |
| 注解索引 299（CP1 止） | `feixing-ziwei-doushu-yuanzhi:L4081-L4081` |
| 注解索引 300（下一包起，不在本包） | `feixing-ziwei-doushu-yuanzhi:L4083-L4116` |
| 注解索引 335（全书末条） | `feixing-ziwei-doushu-yuanzhi:L4586-L4586` |

CP1 止于 page-103 对图标记；remaining **36**（索引 300–335）与 Issue 一致。不宣称全书审查完成（CP2 属他岗）。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md` 的 `Lxxxx` span。本岗独立抽核 **22** 段（元数据 / 序跋 / 理论 / 全部 5 条案例；样本索引与 MING-344 不完全相同）。前半对照源文成立；繁简转换导致的字面 token 差不记为失败。套语后缀见 §7。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0004` | 元数据 / sr | slug + `ocr_reviewed_complete_candidate`；本地来源，非断法 | 通过 |
| 4 | `L0018-L0018` | 序跋 / sr | 「華山陳希夷先生飛星紫微斗數原旨」书名题署；陈希夷不收案例 | 通过 |
| 6 | `L0025-L0025` | 序跋 / sr | 「斗數觀測錄序」；与观云居士《紫微斗数宣微》同手笔 | 通过 |
| 7 | `L0027-L0069` | 序跋 / sr | 清季流通稀少、改革后无人问津、雷君必变抄本 | 通过 |
| 10 | `L0078-L0116` | 序跋 / sr | 雷迅氏录；戊寅仲秋碧云拾稿；四相天地人命；戊寅≠四柱 | 通过 |
| 18 | `L0169-L0190` | 理论 / sr | 诸星桃花心性：紫微土、破军水、七煞金、贪狼木、廉贞/太阳火、太阴水 | 通过 |
| 27 | `L0291-L0291` | 理论 / sr | 命理→相理→地理；人假地假人真地真；已发未发 | 通过 |
| 35 | `L0313-L0357` | 理论 / sr | 危险期/红鸾大耗/王治馨历史人名无四柱不收；跨页 span=45 | 通过 |
| 48 | `L0451-L0468` | 理论 / sr | 羊刃主武职；朱子桥甲戌正月廿三日卯时——仅历日不收案例 | 通过 |
| 55 | `L0579-L0617` | 理论 / sr | 白虎申酉/丧门寅卯/吊客巳午；咸池即桃花煞；文末截于「遇半」 | 通过 |
| 72 | `L0933-L0933` | 理论 / sr | 鼻歪脸偏与坟地相应；文末截于「地枯」 | 通过 |
| 105 | `L1449-L1481` | 案例 / sr | 吴先生辛巳庚子辛丑戊子 + 夫人甲午甲戌丁酉甲辰；红鸾大耗克妻 | 通过 |
| 115 | `L1617-L1617` | 理论 / sr | 陀罗伤残/灵柩；丙子小运行午父故母早亡；刑死不转写 | 通过 |
| 130 | `L1816-L1841` | 理论 / sr | 无名女命辛丑壬辰丁丑辛丑；巨门天机卯；不收案例 | 通过 |
| 148 | `L2068-L2089` | 案例 / sr | 顾瑞年癸亥己未壬午辛亥；破军申紫微午；杀破狼 | 通过 |
| 155 | `L2134-L2156` | 案例 / sr | 叶字英壬辰庚戌乙亥乙酉；巨门子石中隐玉 | 通过 |
| 165 | `L2295-L2348` | 案例 / sr | 谢先生己丑丙寅己卯甲子；廉破卯；文末截 | 通过 |
| 172 | `L2395-L2395` | 案例 / sr | 顾叔明乙酉癸未丙子丁酉；铃星机梁；文末截于「十」 | 通过 |
| 200 | `L2688-L2688` | 理论 / sr | 韩恒忠之母辛巳十月十三日亥时仅历日；贪狼子克夫羊疯 | 通过 |
| 240 | `L3193-L3193` | 理论 / sr | 宝筏开觉匾；王子千无四柱不收；流年文昌 | 通过 |
| 275 | `L3727-L3727` | 理论 / sr | 王胜千己未十二月初五日寅时仅历日；右弼亥；文末截 | 通过 |
| 299 | `L4081-L4081` | 元数据 / sr | page-103 对图标记；本包止此 | 通过 |

关键条件与源行（抽核）：

- 头信息 slug / ocr_reviewed：L3–L4
- 书名题署：L18
- 斗数观测录序 / 观云居士 / 雷君必变：L25–L69
- 雷迅氏录 / 斗数别录 / 四相：L78–L116
- 诸星桃花心性：L169–L190
- 危险期 / 王治馨：L313–L357
- 羊刃 / 朱子桥历日：L451–L468
- 白虎丧门吊客 / 咸池：L579–L617
- 吴先生+夫人双四柱案例：L1449–L1481
- 顾瑞年案例：L2068–L2089
- 叶字英石中隐玉：L2134–L2156
- 谢先生廉破：L2295–L2348
- 顾叔明铃星截句：L2395
- 韩恒忠之母历日：L2688
- 王胜千历日：L3727
- CP1 止 page-103：L4081
- 下一包起：`L4083-L4116`

## 6. source-reviewed ≠ 人工 verified

主文本 `source_status=ocr_reviewed_complete_candidate`。300 条电子语义阅读升 `source-reviewed`，只表示对照 OCR 电子段落实了层次/条件/案例收录边界/未知去向，不是影印逐字校勘，也不是预测有效证据。不得把 300（或全书 336）条 source-reviewed 写成已人工 verified。本包不是全书完成，也不是产品/引擎交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 注解 SHA256 | 与 Issue 钉死一致 | 继承成立 |
| validator | `ok=true` entries=336 sr=336 errors=[] | 结构通过 |
| verified | 336/336 false；本包 300/300 false | 未越权提升 |
| 对图标记套语 | 约 103 条白话同构「…是电子文本校次说明，不是古书断法」 | 元数据层，不是空模板。不回改 |
| notes「待分类作…」 | 绝大多数以「待分类」起首 | 套语，前半 kind 分层仍成立。不回改 |
| 白话安全后缀 | 大量「无人名连续四柱不收案例 / 不转写 / 不把行限当出生柱」 | 政策套语，前半对照源文。不回改 |
| 案例收录边界 | 仅 5 条 kind=案例（吴先生夫妇、顾瑞年、叶字英、谢先生、顾叔明）；均人名+连续四柱 | 与 reviewScope / notes 一致 |
| 历日非案例 | 朱子桥、韩恒忠之母、王胜千、王子千等仅历日/无名 → 理论 | 边界清楚。不回改 |
| 文末截句 | 多页跨页截断，notes 标与下页相连 | 不补造。不回改 |
| 同 SHA 前审 | MING-344 done @ `018d27d` | 查重复用结构结论；本岗另做抽样 |
| remaining | 36（300–335） | 本岗不续写；不抢 CP2 |

## Caveat（不改注解，留给后续 pack）

1. **对图标记密度高**：CP1 约 1/3 为 `reviewed_against_image` 元数据条。结构正确，但不增加术数语义深度；不得据此升 verified。
2. **notes / 白话套语重**：几乎每条都有「待分类」「不收案例」「不转写」后缀。是否空模板看前半是否对照源文——抽核前半成立，故本包通过；后续若需压缩套语，另开生产包，审查岗不回改。
3. **OCR 候选**：`ocr_reviewed_complete_candidate` ≠ 影印人工 verified。缺字/截句/跨页粘连保留电子态。
4. **案例政策**：仅「人名 + 连续四柱」入案例；历日生辰、无名命例保持理论。与书中吴先生夫人顾瑞年叶字英谢先生顾叔明叙述一致。
5. **不改算法**：多条 notes 写明「不改已落地紫微算法」——本审查确认未触引擎/chart。
6. **繁简字面差**：白话多简体、源文多繁体；不得仅凭 token 字面重合率判失败。

## 未决（本岗不施工）

- 索引 300–335 remaining **36** 属 CP2 范围；本岗不续写、不抢并行 CP2 审查稿。
- 识典/OCR 待校、段末截断、套语压缩，一律不回改注解。
- 六壬/秘本/皇极、SDZJ0170、产品仓不在本包。
- 本审查不把任何条目标成人工 verified。
- 不宣称飞星原旨全书 / 紫微引擎 / 全项目完成。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-417`。对象 commit `6effd8e4f951fd17e1b1e0454942946ebc765da9`。远端推送至 `linyuhanggg/fateradar-classics`。
