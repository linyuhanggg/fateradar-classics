# 《滴天髓阐微》主本：独立审查 CP19（5400–5680 收口）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。注解 JSON 已在该钉死树中一次交齐（blob `477c2c80f6199f4b7c6451b3f0289d8d63b1d063`，SHA256 与 Issue 一致）。本岗工作树只读该 SHA，写出仅本文件。未改注解 JSON、未改源文、未改引擎 / `chart.*` / golden / 他书。未写、未抢 `ditiansui-chanwei-cp13-review.md`（CP13=3600–3899 属 [MING-278](mention://issue/01a090a0-7717-7dd8-8e89-9fb4f57752cf)）、`ditiansui-chanwei-cp14-review.md`（CP14=3900–4199 属 [MING-280](mention://issue/01a090a0-85d0-79fc-8f4b-0204b93b5ba1)）、`ditiansui-chanwei-cp15-review.md`（CP15=4200–4499 属 [MING-281](mention://issue/01a090a0-8cea-7a92-ad2b-a8caaf81ee89)）、`ditiansui-chanwei-cp16-review.md`（CP16=4500–4799 属 [MING-283](mention://issue/01a090a3-6512-7f18-8907-71f8849e166c)）、`ditiansui-chanwei-cp17-review.md`（CP17=4800–5099 属 [MING-284](mention://issue/01a090a3-6c0b-722f-b510-08a2db112abd)）、`ditiansui-chanwei-cp18-review.md`（CP18=5100–5399 属 [MING-285](mention://issue/01a090a5-271d-704a-8135-d42cc8b6e510)）。不是全书 5681 段人工 verified，不是续写 5400–5680，不是从 CP1–CP18 重做 0–5399，不是引擎包，也不是全项目完成。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；索引 0–5399 相对权威 SHA / 同路径 peer 树字节级未改；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。本包无新增待核实；全书仍 3 段待核实均在包外。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。本包后本 edition remaining **0**（索引尽收）；仍不是人工 verified / 影印校勘 / 全项目完成。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-286`，2026-09-11）：

```
git rev-parse HEAD
git ls-remote origin refs/heads/codex/full-library-completion
shasum -a 256 references/annotations/bazi/ditiansui-chanwei.json
shasum -a 256 sources/fulltext/bazi/ditiansui-chanwei/fulltext.md
git rev-parse HEAD:references/annotations/bazi/ditiansui-chanwei.json
git rev-parse HEAD:sources/fulltext/bazi/ditiansui-chanwei/fulltext.md
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解 SHA256 | `1a98143c934f4395dfe9c15e1b17082cb9caa0a45f03d7e2a7cd3da30f9f56fb`（与 Issue 钉死值一致） |
| 注解 blob | `477c2c80f6199f4b7c6451b3f0289d8d63b1d063` |
| 源 `fulltext.md` SHA256 | `2eca5a1a22582650f3ca64b6d33b3758bd0ba2a19f48393a1604947e0ee5cd65` |
| 源 blob | `6f03dda3706d03224d3f5482300f91b45ce30a22` |
| 段落清单 | 5681 段；条目 notes 写明 source-reviewed 不等同人工影印核验 |
| 注解 ID 与源段 | validator 结构通过；`entries=5681`，`mismatch` 无 |
| 0–5399 相对 `fateradar-multica-ming-271` / `274` / `275` / `278` / `281` / `284` 同路径 JSON | 全文件字节相同；0–5399 条目 JSON 序列化差集空（SHA256 `0b19ab6393749ae9…`） |
| 本包索引 | 5400–5680（281 段，本 edition 收口）；未改 0–5399 |
| CP13–CP18 写出 | 未创建 / 未修改对应 `ditiansui-chanwei-cp{13,14,15,16,17,18}-review.md` |

无越权文件。源层未改。他书 / 引擎 / `chart.*` 未覆盖。不是续写包。以钉死树中该 blob 为准。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/bazi/ditiansui-chanwei.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 5681, "source_reviewed": 5681,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`entry.get("verified") is True` 才会报错；本文件 5681 条均无 `verified` 字段，等价未升 true。

## 3. verified / draft 未越权提升

5681 条：`review=source-reviewed` 全 5681；`verified` 字段 0 条（true=0 / false 显式=0）；`draft` 0。无升 verified。

kind 全书累计：评注或元数据 4777、案例 511、理论 253、规则候选 92、术语 37、操作步骤 8、待核实 3。

本包 CP19（5400–5680）kind：评注或元数据 220 / 案例 27 / 理论 23 / 术语 5 / 规则候选 4 / 操作步骤 2 / 待核实 0。

空白白话 0、理论/案例空 terms 0、空 notes 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。理论+案例 50/50 白话互不重复。

220 条评注中：219 条为盘例表列（年/月/日/时柱或大运项 +「盘例资料」）；1 条非表列收口元数据（`L13619-L13646` 任氏贞元河洛/纳甲/身后运文化解释，见 caveat）。盘表句式合法，去向是表列而非命盘判断规则。另有 22 条表列 notes 标明「稳定段落粘连多个表格单元」，按连续干支对拆读，不把四字当单柱。

## 4. 索引边界与 0–5399 未改

`entries` 全书 5681 段；本包审查 5400–5680。0–3599 已由 CP1–CP12 独立审查；3600–5399 属 CP13–CP18（MING-278/280/281/283/284/285），本岗只读确认相对权威 SHA 未改、不抢其写出。本岗字节级比对确认 0–5399 与 peer 树同路径 JSON 全文件相同。

| 位置 | 实测 ID | 章节位置 |
|---|---|---|
| 注解索引 5399（CP18 止，本包不重做） | `ditiansui-chanwei:L12976-L12976` | 二十六、出身无名例大运项（前包止） |
| 注解索引 5400（CP19 起） | `ditiansui-chanwei:L12978-L12978` | 二十六、出身无名例大运项（壬子） |
| 注解索引 5680（CP19 / 全书末） | `ditiansui-chanwei:L13619-L13646` | 二十九、贞元任氏收口 |

起始/止点与 Issue 钉死 ID 一致（起 `L12978-L12978`，止 `L13619-L13646`）。本包后 remaining **0**（本 edition 索引尽收）。CP19 覆盖：二十六、出身续例（`L12978`–约 `L13008`）；二十七、地位（`L13012` 起）；二十八、岁运（`L13398` / 注解约 `L13398`–`L13598`）；二十九、贞元（`L13602`–`L13646`）。

待核实：本包 0 段；包外仍有 `476` `L1377-L1377`、`1177` `L3102-L3102`、`4730` `L11498-L11498`。不得在本包改字或升 verified。

## 5. 抽样语义（≥15 非模板，对照原文，不凭既有全书报告）

原文取 `sources/fulltext/bazi/ditiansui-chanwei/fulltext.md` 的 `start_line–end_line`。下列为理论/案例/术语/规则/操作步骤/非表列元数据抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 5405 | `L12988` | 案例 / sr | 丙春官透无根；游幕捐县与丁丑受损为原叙；病亡不作确定事件 | 通过 |
| 5415 | `L13008` | 案例 / sr | 辛辰酉丁无根；捐职无实缺与家业退为原叙 | 通过 |
| 5416 / 5417 / 5418 | `L13012`–`L13016` | 理论 / sr | 地位=清气权势旧官职论；难断职位；真神有情≠品格证明 | 通过 |
| 5423 / 5428 / 5433 / 5438 | `L13026`–`L13056` | 案例 / sr | 董/刘/钱/秦复引同形；清气≠改写主用；异称不合并身份 | 通过；见 caveat |
| 5439 / 5440 / 5441 | `L13058`–`L13069` | 理论 / sr | 刃杀神清；阴干刃本书口径并列五阳刃；文官武将断语不产品化 | 通过 |
| 5451 / 5461 / 5471 / 5481 | `L13089`–`L13149` | 案例 / sr | 酉/午/子/卯刃承杀；干支制化可复算；官阶为原例 | 通过 |
| 5482 / 5483 / 5484 | `L13151`–`L13155` | 理论 / sr | 地方官财官协调；利民之心不由组合证明 | 通过 |
| 5494 / 5504 / 5514 / 5524 | `L13175`–`L13255` | 案例 / sr | 印化/伤财/春金任火/印过重癸运；子女存亡与病期不产品化 | 通过 |
| 5535 / 5536 / 5537 | `L13257`–`L13274` | 理论 / sr | 清浊形影；干清支浊分层；贵贱词不给人分等 | 通过 |
| 5547 / 5557 / 5567 / 5577 | `L13294`–`L13354` | 案例 / sr | 支藏清处；干杂≠全局浊；合支破干；财坏印≠成就归零 | 通过 |
| 5587 | `L13374` | 案例 / sr | 电子「天干三戌」实为三戊；保留疑字不改天干事实 | 通过结构；见 caveat |
| 5598 / 5599 / 5600 | `L13398`–`L13407` | 理论+操作 / sr | 岁运比较；运重支年重干；一运十年勿截看（PDF 502） | 通过 |
| 5601 / 5602 / 5603 / 5604 | `L13409`–`L13428` | 理论+术语+规则 / sr | 喜运列举；盖头截脚；庚寅半减修辞；甲申截脚有救应 | 通过；见 caveat |
| 5615 / 5625 / 5635 / 5645 | `L13455`–`L13522` | 案例 / sr | 干支分叙仍整柱；反化合长生名；喜金须可用；盖头使同支不同运 | 通过 |
| 5646 / 5647 / 5648 | `L13524`–`L13533` | 术语+理论+规则 / sr | 战=干克；岁克运非一律凶；成败看所需方与救应 | 通过 |
| 5658 / 5668 | `L13553` / `L13573` | 案例 / sr | 同庚运丙寅年因用神相反断语相反；病亡非死亡触发器 | 通过；见 caveat |
| 5669–5677 | `L13575`–`L13598` | 术语+理论+规则 / sr | 冲/和/好定义；子午冲支援；合化与绊；得禄根 | 通过；见 caveat |
| 5678 / 5679 / 5680 | `L13602`–`L13646` | 理论+元数据 / sr | 贞元循环哲学；十五年象征分段；身后运不证实家族命运 | 通过；见 caveat |
| 5400 / 5680 | `L12978` / `L13619-L13646` | 表列 / 元数据 | 包起出身大运壬子；包止贞元任氏收口 | 通过 |

原文条件与源行（抽核，非转引既有全书报告）：

- 二十六、出身续：`L12978`–约 `L13008`
- 二十七、地位：`L13012`–约 `L13394`
- 二十八、岁运：`L13398`–约 `L13598`
- 二十九、贞元：`L13602`–`L13646`（全书末）

## 6. 出身续 / 地位 / 岁运 / 贞元分层

Issue 要求：kind/白话/疑文/版本与原文 ID 一致；失败写具体 paragraphId，禁止自改。

| 主题 | 本包位置 | 判定 |
|---|---|---|
| 二十六、出身续例 | `L12978`–约 `L13008` | 通过：财官通路与名义官职可核；履历/病亡为原叙 |
| 二十七、地位清气/刃杀 | `L13012`–约 `L13149` | 通过：清气≠主用；同形异称保留；刃杀时令口径并列 |
| 地位地方官/清浊 | `L13151`–约 `L13394` | 通过：干支清浊分层；电子三戌已注 |
| 二十八、岁运操作与术语 | `L13398`–约 `L13428` | 通过：运年比较、盖头截脚、喜运列举与 PDF 校记一致 |
| 岁运战冲和好案例 | `L13455`–约 `L13598` | 通过：同流年因用神相反分断；残表不推精确灾期 |
| 二十九、贞元收口 | `L13602`–`L13646` | 通过：哲学收束；身后运/祖德不作验证结论 |

## 7. Caveat（不构成本包失败；禁止升 verified）

1. **电子疑文保留**：`L13374` 电子「天干三戌」实列盘三戊；`L13409-L13414` 电子戌申 vs PDF 503 戊申；`L13416-L13419` 电子乙卯 vs PDF 503 己卯；`L13428` 电子壬登讹；`L13579-L13586` 运年称谓/例表残误。本岗不改源文/注解。
2. **同形复引**：`L13026`/`L13036`/`L13046`/`L13056`/`L13255` 等同形只确认四柱输入，不合并历史人物、不重复计应验。
3. **官职/道德/身后运**：地位章清气权势、利民理想、贞元身后运与祖德，一律历史/文化叙述；不得作现代职位、品格或家族命运产品结论。
4. **病亡与岁克运**：`L12988`、`L13553` 等病亡为原例个案；不把岁克运直接作死亡触发。
5. **比例修辞**：`L13421-L13426`「十分减半」等为作者经验修辞，无统计校准，不写为现代概率权重。
6. **包边界 / remaining**：本 edition 索引 5400–5680 收口后 remaining **0**；仍不是人工 verified，不是影印校勘，不是全项目完成。包外 3 段待核实保留。

## 8. 交付边界

- 写出仅 `docs/book-reviews/ditiansui-chanwei-cp19-review.md`
- 未改 `references/annotations/bazi/ditiansui-chanwei.json`
- 未抢 CP13–CP18 审查稿
- `source-reviewed` ≠ 人工 `verified`；本 edition remaining **0**
- 不宣称全书 / 项目完成
