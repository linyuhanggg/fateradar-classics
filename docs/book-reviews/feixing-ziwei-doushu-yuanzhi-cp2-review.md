# 飛星紫微斗數原旨：独立审查主本 source-reviewed CP2（300–335 收尾）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-418` / 分支 `codex/multica-ming-418`。本岗写出仅本文件。未改注解 JSON、未改 `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md`、未改 CP1 审查稿、未改 SDZJ0170 / 主本紫微引擎 / chart / 大六壬 / 秘本 / 皇极。本岗未参与飞星紫微斗数原旨生产。不是飞星紫微斗数原旨全书人工 verified，也不是引擎包，也不是全项目完成。

结论：**通过。** 交包结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；OCR 电子主文本不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。本包后该书 SR 审查 remaining **0**。全书库存 336 段电子语义注解已尽，仍不是人工 verified。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-418`，2026-09-12）：

```
git fetch origin refs/heads/codex/multica-ming-329
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
shasum -a 256 sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md
git rev-parse HEAD:references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
git status --short references/annotations/ziwei/feixing-ziwei-doushu-yuanzhi.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致；远端在 `linyuhanggg/fateradar-classics`） |
| 注解 JSON SHA256 | `c98f9f305f8f40a2a3c102458f5de9ea39bd78dda3e102240f6ac6b402a67c95`（与 Issue 钉死一致；与 MING-344 CP1 对象全等） |
| 注解 blob | `9f713a371b7059b2986321c12933a2ceb96c5766` |
| 源 `fulltext.md` SHA256 | `3a103d51839ff9a150c4b1b21a13c1d4866ca0c6327d19cd332e0f9e842436cb` |
| `sourceFile` | `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md` |
| 头信息 `reviewScope` | 至 page-116 末叶；全书 336 段电子语义注解已尽；明确 source-reviewed ≠ 影印人工核验 |
| 工作区注解 JSON | `git status --short` 空（本岗未改） |
| 独占写出 | 仅本审查稿；未触 JSON / CP1 审查稿 / 六壬 / 秘本 / 皇极 |

无越权文件。源层未改。注解 JSON 未改。CP1 审查稿不在本树（对象基线 `6effd8e`），本岗也未拷入、未回改。

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

本包 36 条（索引 300–335）：`review=source-reviewed` 全 36；`verified` 全 `false`；无 `draft`。全书 336 条同样 `verified` 全 false、`source-reviewed` 全 336。无升 verified。失败写具体 paragraphId：无。

kind（本包）：理论 18、评注或元数据 18、案例 0。

空白话 0、空 notes 0、空 terms 0。未见「本段论述 / 白话从略 / 见原文 / TODO」类空模板。`relatedParagraphIds` 非空 36/36，且全部指向库存内 ID。注解 span 两两无重叠；相邻 span 间隙最大 4 行（`## page-104` … `## page-116` 与 `# 勘誤表` 标题骨架，可接受）。11 条有 subsections，起止连续覆盖父 span，无缺口/重叠。

## 4. 索引边界

全书注解 336 条；本包只审 300–335。起止与 Issue 钉死一致。0–299 相对 CP1 对象 SHA 全等，抽核 ID/kind/review/verified 与 MING-344 审查稿所列一致，不重做 CP1。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起，不在本包） | `feixing-ziwei-doushu-yuanzhi:L0003-L0004` |
| 注解索引 299（CP1 止，不在本包） | `feixing-ziwei-doushu-yuanzhi:L4081-L4081` |
| 注解索引 300（CP2 起） | `feixing-ziwei-doushu-yuanzhi:L4083-L4116` |
| 注解索引 335（CP2 / 全书末条） | `feixing-ziwei-doushu-yuanzhi:L4586-L4586` |

本包后该书 SR 审查 remaining **0**。不宣称人工 verified，不宣称产品/引擎/全项目完成。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md` 的 `start_line–end_line`。抽核 **19** 段（覆盖理论跨页截句、历日非案例、无名四柱、对图元数据、勘误表、空白末叶）。前半对照源文成立；套语后缀见 §7，不按空模板失败。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L4083-L4116` | 理论 / sr | 戊寅九月初五日未时占候；巨机居卯、天梁守身、地空地劫相夹；小孩钻入被服；无名历日不收案例 | 通过 |
| 301 | `L4121-L4121` | 元数据 / sr | page-104 对图标记；校次说明不是断法 | 通过 |
| 302 | `L4123-L4168` | 理论 / sr | 天刑入庙=天喜神；兵刑为一、僧道原书所有；辛巳贪居亥子泛水桃花、紫贪并论；文末截 | 通过 |
| 304 | `L4175-L4221` | 理论 / sr | 接上页诸吉共朝；紫微升殿、双禄化权、破军汤浇雪、陕甘汽车；夫人盘巨日禄存仅旁证；辛巳仍无名 | 通过 |
| 306 | `L4228-L4228` | 理论 / sr | 「未得亲视」跨页残句；刑死不转写 | 通过 |
| 307 | `L4230-L4274` | 理论 / sr | 紫贪狐仙/舌头/水口；唙咕原字不改；贪狼临子女宫为陷；文末截 | 通过 |
| 309 | `L4281-L4281` | 理论 / sr | 其贪若狼其性为狐；范蠡文种共患难不可共安乐 | 通过 |
| 310 | `L4283-L4317` | 理论 / sr | 某人壬辰五月初二日巳时；紫破守命、至淫、红鸾大耗；无名历日不收 | 通过 |
| 312 | `L4324-L4350` | 理论 / sr | 斗数发微论；玄媼=天姚；扫气嚣；架杻囚徒；原字不改 | 通过 |
| 313 | `L4352-L4352` | 理论 / sr | 某西医甲午丁卯甲戌甲戌、木三局、双禄重逢中奖；有连续四柱因无名不收案例 | 通过 |
| 315 | `L4359-L4377` | 理论 / sr | 接上页到手成空；财宫大耗陀罗；官禄巨机落劫；曾任军医 | 通过 |
| 316 | `L4379-L4403` | 理论 / sr | 赵君己未十一月十五日酉时；天府令星卯、武杀酉；历日无连续四柱 | 通过 |
| 318 | `L4410-L4448` | 理论 / sr | 赵君坟茔坐东向西=坐天府向武杀，迁丑未=坐紫破向天相；疾病刑死不转写 | 通过 |
| 321 | `L4483-L4483` | 理论 / sr | 杜友棠乙酉三月初四日辰时火六局；武府守命、紫府朝垣；有人名无连续四柱 | 通过 |
| 323 | `L4490-L4527` | 理论 / sr | 接初行大运；行未入劫欲上仙梯；巳卯双禄；不把行限当出生柱 | 通过 |
| 324 | `L4529-L4529` | 理论 / sr | 延君甲午四月卅日子时木三局；天府单守、武贪三奇；文末截於山西军来 | 通过 |
| 327 | `L4538-L4538` | 理论 / sr | 十二宫活用假借为新发明；万勿以批命看之，只作命理草案 | 通过 |
| 333 | `L4558-L4579` | 元数据 / sr | 勘误表页/行/字误正（七页不→为、籍→藉、守下落身等）；不是另行断法 | 通过 |
| 335 | `L4586-L4586` | 元数据 / sr | 空白末叶 / 馆藏印残；全书电子注解止此 | 通过 |

关键条件与源行（抽核）：

- 戊寅巨机占候 / 小孩钻被服：L4083–L4116
- page-104 对图：L4121
- 天刑入庙 / 泛水桃花：L4123–L4168
- 紫微升殿 / 汤浇雪：L4175–L4221
- 紫贪狐仙 / 唙咕：L4230–L4274
- 某人壬辰紫破至淫：L4283–L4317
- 斗数发微论 / 扫气嚣：L4324–L4350
- 某西医甲午丁卯甲戌甲戌：L4352
- 赵君己未天府令星：L4379–L4403
- 坟茔坐向：L4410–L4448
- 杜友棠武府 / 紫府朝垣：L4483
- 十二宫活用草案：L4538
- 勘误表：L4558–L4579
- 空白末叶：L4586

## 6. source-reviewed ≠ 人工 verified

主文本 `reviewScope` 写明对照电子主文本至 page-116 末叶，不代表影印人工核验。本包 36 条电子语义阅读升 `source-reviewed`，只表示对照 OCR 电子段落实了层次/条件/案例收录边界/未知去向，不是影印逐字校勘，也不是预测有效证据。不得把 36（或全书 336）条 source-reviewed 写成已人工 verified。本包是该书 SR 审查收尾，不是全书人工完成，也不是产品/引擎交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 注解 SHA256 | 与 Issue / CP1 对象钉死一致 | 继承成立；0–299 冻结 |
| validator | `ok=true` entries=336 sr=336 errors=[] | 结构通过 |
| verified | 336/336 false；本包 36/36 false | 未越权提升 |
| 对图标记 | 13 条 page-104…page-116 白话同构「…是电子文本校次说明，不是古书断法」 | 元数据层，不是空模板。不回改 |
| notes「待分类作…」 | 36/36 | 套语，前半 kind 分层仍成立。不回改 |
| 白话安全后缀 | 36/36「不收案例」；17 条「不转写」 | 政策套语，前半对照源文。不回改 |
| 案例收录边界 | 本包 kind=案例 **0**。全书案例仍仅 CP1 五条（吴先生夫妇、顾瑞年、叶字英、谢先生、顾叔明） | 与 reviewScope / 人名+连续四柱政策一致 |
| 历日/无名非案例 | 戊寅占候、辛巳、某人壬辰、赵君、杜友棠、延君仅历日或无名 → 理论 | 边界清楚。不回改 |
| 无名四柱 | 仅 313 `某西医` 列 `甲午丁卯甲戌甲戌`，因无名保持理论 | 政策一致，见 caveat。不回改 |
| 文末截句 | 多页跨页截断，notes 标与下页相连 | 不补造。不回改 |
| remaining | 本包后该书 SR 审查 **0** | 不续写、不宣称 verified |

## Caveat（不改注解，留给后续 pack）

1. **元数据密度高**：本包 18/36 为对图标记、页眉页码、勘误表、空白末叶。结构正确，但不增加术数语义深度；不得据此升 verified。
2. **notes / 白话套语重**：每条都有「待分类」「不收案例」后缀。是否空模板看前半是否对照源文——抽核前半成立，故本包通过；后续若需压缩套语，另开生产包，审查岗不回改。
3. **OCR 候选**：电子主文本不是影印人工 verified。缺字/截句/跨页粘连（如 L4221「在外奔走」无句号、L4228「。未得親視。」）保留电子态。
4. **案例政策**：仅「人名 + 连续四柱」入案例。`某西医` 有完整四柱但无姓名；`杜友棠`/`延君`/`赵君` 有称呼但仅历日。与 CP1 五条已收案例的边界一致，不在本包改 kind。
5. **勘误表 L4579**：源表「一〇四 / 八 / 一 / 醫 / 醫」误正同字，注解标「醫原字不改」，对照成立，不是新断法。
6. **不改算法**：多条 notes 写明「不改已落地紫微算法」——本审查确认未触引擎/chart。
7. **标题骨架未入注解**：`## page-N` 与 `# 勘誤表` 落在 span 间隙，与 CP1 页间空行处理相同，可接受。

## 未决（本岗不施工）

- 该书 SR 审查 remaining **0**；识典/OCR 待校、段末截断、套语压缩、无名四柱是否另立案例，一律不回改注解。
- 本审查不把任何条目标成人工 verified。
- SDZJ0170、大六壬、秘本、皇极、CP1 审查稿、MING 集成不在本包。
- 不宣称飞星原旨全书人工完成 / 紫微引擎 / 全项目完成。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-418`。对象 commit `6effd8e4f951fd17e1b1e0454942946ebc765da9`。远端仓 `linyuhanggg/fateradar-classics`。
