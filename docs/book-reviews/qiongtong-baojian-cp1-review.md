# 《穷通宝鉴》主本：独立审查 CP1（0–299）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。注解内容落地于 `a0105295523795d7e6f39580c8402358351807ce`（`docs(classics): finish all 605 Qiongtong source paragraph annotations`）；本 SHA 上注解 blob 与该提交一致，非本岗所写。工作树只读参考本 SHA，本岗写出仅本文件。未改注解 JSON、未改源文、未改引擎 / `chart.*` / golden / 他书。不是《穷通宝鉴》全书完成，不是续写 0–299，不是引擎包，也不是全项目完成。

结论：**通过。** 结构账本与 ≥15 段规则候选/案例/理论抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–604（`L0865-L0865` 起）本包不审、不改。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-223`，2026-09-11）：

```
git fetch origin bc798566da77c30e149abf9673c88ecc386702b2
git rev-parse HEAD
git ls-remote origin refs/heads/codex/full-library-completion
shasum -a 256 references/annotations/bazi/qiongtong-baojian.json
shasum -a 256 sources/fulltext/bazi/qiongtong-baojian/fulltext.md
git rev-parse HEAD:references/annotations/bazi/qiongtong-baojian.json
git rev-parse HEAD:sources/fulltext/bazi/qiongtong-baojian/fulltext.md
git log -1 --format='%H %ci %s' -- references/annotations/bazi/qiongtong-baojian.json
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解内容提交 | `a0105295523795d7e6f39580c8402358351807ce`（2026-09-08；全书 605 段一次标注，非本岗所写） |
| 注解 SHA256 | `36631481ebb4803d4169de09abd719ed77a1dc46241d838e337e78caa3ea85ce`（与 Issue 钉死值一致） |
| 注解 blob | `df06144b650cbc05ed1454fcb4310ebad719f6f0`（与 `a010529` 同 blob） |
| 源 `fulltext.md` SHA256 | `7fd1c835481b7c761f3519cce2cb4c3f16a90fd409d40cd0a09b412af1fef3cc` |
| 源 blob | `c13f903547567ded6d749bb2ffec1169234db734` |
| 段落清单 | 605 段；本包只审索引 0–299 |
| 本包索引 | 0–299；未改 300–604 |

无越权文件。源层未改。他书 / 引擎 / `chart.*` 未覆盖。不是续写包。既有 `docs/book-reviews/qiongtong-baojian.md` 是标注岗全书加工报告，本岗未改该文件，也不以其语义摘要代替对照原文抽核。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/qiongtong-baojian.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 605, "source_reviewed": 605,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`entry.get("verified") is True` 才会报错；本文件 605 条均无 `verified` 字段，等价未升 true。

## 3. verified / draft 未越权提升

全书 605 条：`review=source-reviewed` 全 605；`verified` 字段 0 条（true=0）；`draft` 0。无升 verified。

kind 全书累计：规则候选 496、案例 81、理论 23、评注或元数据 4、待核实 1。

本包 CP1（0–299）kind：规则候选 249 / 案例 33 / 理论 16 / 评注或元数据 2。待核实 0（全书唯一待核实在 CP2+）。

空白话 0；规则/理论/案例空 terms 0；空 notes 226（白话仍具体，见账本）。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。规则候选白话 249/249 互不重复。白话长度 min 25 / 中位 59 / max 103。

## 4. 索引边界

全书注解 605 段；本包审查 0–299。300–604 在同一 JSON 中已是 `source-reviewed`，本岗只读不改、不把其计入本包通过范围。

| 位置 | 实测 ID | 内容锚点 |
|---|---|---|
| 注解/源索引 0 | `qiongtong-baojian:L0005-L0005` | 五行总论起句 |
| 注解索引 299（CP1 止） | `qiongtong-baojian:L0863-L0863` | 四月戊土附近「土木重重，全无滴水」 |
| 注解索引 300（下一包起，不在本包） | `qiongtong-baojian:L0865-L0865` | 未纳入本包 |
| 源/注解索引 604（全书末） | `qiongtong-baojian:L1823-L1823` | 癸水末句一带 |

起始/止点与 Issue 钉死 ID 一致。remaining 305（300–604）。CP1 覆盖电子前言五行/十干导引、论木、甲乙四季、论火、丙丁四季、论土，以及论戊土至 `L0863`；戊土余段、己土、金水各干与待核实段不在本包。

## 5. 抽样语义（≥15 非模板，对照原文，不凭既有全书报告）

原文取 `sources/fulltext/bazi/qiongtong-baojian/fulltext.md` 的 `start_line–end_line`。下列为理论/规则候选/案例抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0005` | 理论 / sr | 「五行者…故谓之行」。白话把「行」说成流转不息，不写成五种可称量物质 | 通过 |
| 1 | `L0007-L0007` | 理论 / sr | 方位阴阳生寒热风燥温；相生相维、相克相制。白话反对生一律吉、克一律凶 | 通过 |
| 5 | `L0015-L0015` | 理论 / sr | 水一火二木三金四土五；生旺加倍、死绝减半。白话标明不直接当现有旺衰权重 | 通过 |
| 12 | `L0049-L0049` | 规则 / sr | 冬木喜土火、恶水盛；金总多不能剋伐。季节条件保留 | 通过 |
| 25 | `L0095-L0095` | 规则 / sr | 无水、戊己透、支成土局才弃命从财。notes 标明不能替代他派从格审核 | 通过 |
| 40 | `L0127-L0127` | 规则 / sr | 土多而干上有乙，「切勿」弃命从才。排除条件未删 | 通过 |
| 55 | `L0159-L0159` | 规则 / sr | 金局庚透为木被金伤；得丙丁仍主老来暗疾。救应未写成完全消除 | 通过 |
| 65 | `L0179-L0179` | 案例 / sr | 戊戌壬戌甲子甲申称支成水局但无辰。白话/notes 拒绝按申子辰已成处理 | 通过 |
| 100 | `L0257-L0257` | 规则 / sr | 丙透火局阳焦；无癸必夭见壬可解；火土太多另论。条件分支保留 | 通过 |
| 140 | `L0343-L0343` | 规则 / sr | 冬火喜木火、土制水；见金为难任财。不等于冬月一律排除金水 | 通过 |
| 160 | `L0399-L0399` | 规则 / sr | 月时二辛卯、日丙子争合；年丁制辛分支；木局另条件。不补全四柱 | 通过 |
| 176–177 | `L0446` / `L0448` | 规则 / sr | 「即有.」未完接「一二癸水」。notes 互指连读，未拆成独立完整断句 | 通过 |
| 220 | `L0601-L0601` | 规则 / sr | 庚金壬癸得己透制水。制衡分支，不是任何己都为终用 | 通过 |
| 240 | `L0660-L0660` | 案例 / sr | 「刑子息」私用区字符；notes 保留缺义。部分柱不补整盘 | 通过 |
| 280 | `L0809-L0809` | 规则 / sr | 正二月无丙除寒 vs 有丙无甲癸春旱；火局看壬癸。缺暖与缺润分开 | 通过 |
| 286 | `L0821-L0821` | 案例 / sr | 丁未癸卯戊寅乙卯；月支卯，不因三月讨论改成辰。化火作作者解释 | 通过 |
| 290 | `L0840-L0840` | 规则 / sr | 四月戊先甲疏土，丙癸为佐；外实内虚仍需阳气。不认夏月丙恒忌 | 通过 |
| 299 | `L0863-L0863` | 规则 / sr | 土木重重全无滴水。润泽缺失可提取；僧道孤贫不作实预测 | 通过 |

关键条件与源行（抽核，非转引既有全书报告）：

- 五行流行定义：L0005
- 相生相维 / 相克相制：L0007
- 五行数与生旺死绝加减：L0015
- 冬木培养 / 火暖 / 水盛：L0049
- 三月甲从财三条件：L0095
- 有乙勿从财：L0127
- 金局庚透伤木、丙丁仍暗疾：L0159
- 无辰却称水局例：L0179
- 丙透火局 / 壬解：L0257
- 冬火取用与难任财：L0343
- 争合与年丁：L0399
- 「即有」跨段：L0446–L0448
- 庚壬癸得己制：L0601
- 未释字符与部分柱：L0660
- 春旱 / 无丙除寒：L0809
- 武科探花例月支卯：L0821
- 四月戊先甲：L0840
- CP1 止土木无水：L0863
- 下一包起：L0865

## 6. source-reviewed ≠ 人工 verified

300 条电子语义阅读保持 `source-reviewed`（全书累计 605），只表示对照当前电子段落实了白话、种类、术语与条件/例外或疑点去向，不是影印逐字校勘，不是人类专家验盘，不是预测有效证据，也不是调候算法可执行。不得把 605 条 source-reviewed 写成已人工 verified。本包不是戊己金水全帙，也不是产品交付。

既有 `docs/book-reviews/qiongtong-baojian.md` 是标注岗全书加工报告，不是本岗独立审查证书；本文件才是 CP1 独立复核。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 空 notes | CP1 226 条（规则 191 / 案例 24 / 理论 9 / 元数据 2） | 白话仍具体、非空模板。不回改 |
| 私用区 / 缺义字符 | `L0660`、`L0785`、`L0789`、`L0795-L0801` 等 notes 已标未释 | 保留缺义，不猜填。不回改 |
| 跨段未完句 | `L0446`「即有.」↔ `L0448`「一二癸水」 | notes 互指。不回改 |
| 命例不可当标准盘 | `L0179` 无辰称水局；`L0821` 月支卯不改辰 | 已标。不回改 |
| 六亲配属重复句 | 如用丙/用癸「木妻火子 / 金妻水子」多月复现 | 按月保留，白话不合并成一条全局公式。不回改 |
| `verified` 缺省 | 605 条无该字段 | 校验器按「不是 True」放行。不得补 true |
| 既有全书报告 | `qiongtong-baojian.md` 已在权威树 | 本岗未改该文件 |

## Caveat（不改注解，留给后续 pack）

1. **电子源疑字与私用区字符**：多段含 `\ue10f` 等未释字；notes 已隔离。接入规则库只能消费可读条件，不得把缺义补成确定用神程序。
2. **命例可复算 ≠ 应验**：表序「时日月年」；CP1 内多例缺公历、地点、起运。`L0179` / `L0821` 等结构疑点已标，不可当历史事实。
3. **从财/从杀/从化/炎上**：各段条件不同（无水+透干+成局、有乙勿从、假从五月六月差异等）。不得抽成无条件从格公式。
4. **调候 ≠ 子平格局表**：本书暖润疏制泄引护各有月令前提；本轮未改产品调候表。`source-reviewed` 不证明算法已实现。
5. **空 notes 比例高**：不构成本包失败（白话非模板），但后续若要机器消费例外，应优先回源而非只读 notes。

## 未决（本岗不施工）

- 索引 300–604 留给后续独立审查，nextId `qiongtong-baojian:L0865-L0865`，remaining 305。含戊土余段、己土、金水各干及全书唯一待核实段。
- 影印逐字校勘、争议裁决、规则机器实现、独立现实预测验证仍不在 `source-reviewed` 口径内。
- 本审查不把任何条目标成人工 verified。
- 勿重做 0–299 续写。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-223`。
