# 星历考原：独立审查主本 source-reviewed CP2（300–314 收口）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。工作树 `fateradar-multica-ming-311` / 分支 `codex/multica-ming-311`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/xingli-kaoyuan.md` 旧总述、未写 `xingli-kaoyuan-cp1-review.md`、未改引擎 / `chart.*` / 他书。不是星历考原人工 verified，也不是择日算法包，也不是全项目完成。太乙本 edition 0–208 勿重做；CP1 0–299 属 [MING-308](mention://issue/01a090bc-3177-71f6-969e-5309f99afa27)，本包不抢写。

结论：**通过。** 交包结构账本与本包全部 15 段（≥15）非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。本包后本 edition remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-311`，2026-09-11）：

```
git rev-parse HEAD
git rev-parse origin/codex/full-library-completion
shasum -a 256 references/annotations/selection/xingli-kaoyuan.json
git rev-parse HEAD:references/annotations/selection/xingli-kaoyuan.json
git hash-object references/annotations/selection/xingli-kaoyuan.json
git status --porcelain
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 注解 SHA256 | `f844175695c66cea2cc26222c604734890426ac0f8f95c0622e62a3d2866e0f0`（与 Issue 一致） |
| 注解 blob HEAD vs working | 同为 `04b2ba6bac559ee75ed269a20d23a93218b9fb75`（未改） |
| `bookSlug` | `xingli-kaoyuan` |
| `scopeNote` | 完整阅读现存 315 主段；只知识层；`source-reviewed` 非影印人工核验；`verified` 始终 false |
| 源全文 | `sources/fulltext/selection/xingli-kaoyuan/fulltext.md` |
| 注解 ID 与 inventory 0–314 | 315/315 一一对应，`mismatch=0` |
| 索引 0–299 相对权威 SHA | 同树同 blob，未改；未写 CP1 报告 |
| 本包覆盖 | 仅索引 300–314；起 `xingli-kaoyuan:L1699-L1700`，止 `xingli-kaoyuan:L1757-L1757` |

无越权文件。注解 JSON 未改。旧总述与 CP1 报告路径未触碰。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/selection/xingli-kaoyuan.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 315, "source_reviewed": 315,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 315 条均 `source-reviewed`；本包只审 300–314。

## 3. verified / draft 未越权提升

CP2 15 条：`review=source-reviewed` 全 15；`verified` 全 `false`；无 `draft` 字段。无升 verified。全书 315 条 `verified` 亦全 `false`。

kind（300–314）：规则候选 14、序跋目录 1。

空白话 0、空 notes 5、空 terms 1（卷六尾题）。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话字数 min/median/max = 12/30/43，与 CP1 压缩口径一致，不是空模板。

## 4. 索引边界

inventory / 注解全书 315 段；本包只审 300–314。CP1 0–299 不在本包、未重审语义全文。

| 位置 | 实测 ID | 行号 |
|---|---|---|
| 注解索引 299（CP1 止，不在本包） | `xingli-kaoyuan:L1696-L1696` | L1696 |
| 注解/源索引 300（CP2 起） | `xingli-kaoyuan:L1699-L1700` | L1699–L1700 |
| 注解索引 314（CP2 / 全书末） | `xingli-kaoyuan:L1757-L1757` | L1757 |

起始/止点与 Issue 钉死 ID 一致。本包后 remaining **0**。

约略主题覆盖：渔猎→牧养→种莳→开市交易→酝酿→纳财→进人口→开仓/解除→疗病→沐浴→剃头→整甲→破土→安葬→卷六尾题。

## 5. 抽样语义（本包 15 段全读，对照原文，不凭进度摘要）

原文取 `sources/fulltext/selection/xingli-kaoyuan/fulltext.md` 的 `start_line–end_line`。本包仅 15 段，不足「抽 ≥15」时按 Issue 要求全读。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L1699-L1700` | 规则 / sr | 渔猎：捕鱼雨水后立夏前、畋猎霜降后立春前；天恩天赦不可渔猎止宜捕捉；曹氏獭祭/豺祭时令 | 通过 |
| 301 | `L1703-L1704` | 规则 / sr | 牧养宜六仪母仓等；纳畜另宜定；戌日忌纳犬 | 通过 |
| 302 | `L1708-L1708` | 规则 / sr | 种植母仓四相生气；栽植再加六仪；忌九焦地火及乙日等 | 通过 |
| 303 | `L1712-L1713` | 规则 / sr | 开市与交易分条；立券忌巳、受田忌戊，不混成一种商业活动 | 通过 |
| 304 | `L1717-L1717` | 规则 / sr | 酿酒醯醢宜成定，忌辛破 | 通过 |
| 305 | `L1721-L1721` | 规则 / sr | 受田纳财 / 收敛宜收日 / 出货忌耗虚除，三层不并成一条「发财」 | 通过 |
| 306 | `L1725-L1725` | 规则 / sr | 进人口宜收满黄道等，忌月害五离四穷及建除破平 | 通过 |
| 307 | `L1729-L1730` | 规则 / sr | 开仓出财与解除分题；建日遇要安可解安例外保留 | 通过 |
| 308 | `L1734-L1735` | 规则 / sr | 疗病分针刺/疗目/服药/问卜；曹氏缩血支血忌只限针刺 | 通过 |
| 309 | `L1739-L1739` | 规则 / sr | 沐浴申酉亥子 vs 洗头按月日序表，两层不同 | 通过 |
| 310 | `L1743-L1743` | 规则 / sr | 天宝历剃头月组亥酉巳卯、季月午；忌丁建十五与头人神 | 通过 |
| 311 | `L1747-L1747` | 规则 / sr | 整甲丑寅及六月六/晦/初六十六；忌建破平收 | 通过 |
| 312 | `L1751-L1751` | 规则 / sr | 破土等宜鸣吠对；忌密重复土神、太岁同干支、土王后；异于安葬正鸣吠 | 通过 |
| 313 | `L1755-L1755` | 规则 / sr | 安葬等宜鸣吠；忌密重复建破平收开；与破土条日类不同保留 | 通过 |
| 314 | `L1757-L1757` | 序跋 / sr | 「御定星历考原卷六」尾题；本 edition 收口 | 通过 |

关键条件与源行（全读，非转引进度表）：

- 渔猎时令与天恩捕捉：L1699–L1700
- 牧养/纳畜戌犬：L1703–L1704
- 种莳栽植乙日：L1708
- 开市 vs 交易/立券巳受田戊：L1712–L1713
- 酝酿成定忌辛破：L1717
- 纳财三分出货：L1721
- 进人口：L1725
- 开仓与解除例外：L1729–L1730
- 疗病分项+曹氏血忌：L1734–L1735
- 沐浴/洗头：L1739
- 剃头月组：L1743
- 整甲：L1747
- 破土鸣吠对：L1751
- 安葬鸣吠：L1755
- 卷六尾题：L1757

## 6. source-reviewed ≠ 人工 verified

主本电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/条件/异说/未知去向，不是影印逐字校勘，也不是择日效果验证，也不等于七政/贵人/月令产品算法已实现或已被本注解覆盖。渔猎捕捉、疗病禁日、破土/安葬鸣吠等须保留书内分层，不得只抽宜忌表。不得把 15 条（或全书 315 条）source-reviewed 写成已人工 verified。本包收口本 edition remaining 0，仍不是产品交付，也不是人工 verified 全书。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 白话压缩 | CP2 白话中位约 30 字；索引 304 仅 12 字 | 对照源仍有对应要点，不是空模板。不回改 |
| 空 notes 5 | 301/303/304/311/314 | 结构合法；关键分层多已写入 vernacular。不回改 |
| 空 terms 1 | 索引 314 卷六尾题 | 合法。不回改 |
| 索引 300 | 白话略压缩收日执日危日枚举，保留时令与天恩捕捉分层 | 压缩口径同 CP1。不回改 |
| 索引 303 | 开市/交易/立券巳/受田戊分清 | 正确不混算。不回改 |
| 索引 305 | 纳财/收敛收日/出货忌耗虚除三分 | 正确。不回改 |
| 索引 307 | 电子段把开仓与解除粘在相邻行；注解分题+建日要安例外 | 正确。不回改 |
| 索引 308 | 血支血忌曹氏只限针刺 | 正确不扩到全部疗病。不回改 |
| 索引 312/313 | 鸣吠对 vs 鸣吠；破土另忌土神/太岁同干支/土王后 | 正确不并表。不回改 |
| 索引 314 inventory heading 仍挂「安葬」 | 正文为卷六尾题；注解 kind=序跋目录 | 电子 heading 粘连；注解分类正确。不回改 |
| 索引 0–299 | 与权威 SHA 同 blob，未改 | 不抢 CP1。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **白话压缩**：多数条目是条件摘要而非逐句今译；接入规则或对外引用须回源行，不能只依赖白话。
2. **索引 300**：渔猎与捕捉在天恩天赦日分流；产品表不得把捕捉并入渔猎禁。
3. **索引 303 / 305 / 307**：开市≠交易≠受田；纳财≠出货；开仓≠解除。不得并成单一商业/仓储标签。
4. **索引 308**：历史医疗禁日不可用于延误诊治；血支血忌按曹氏只限针刺。
5. **索引 312 / 313**：破土用鸣吠对、安葬用鸣吠；土神/太岁同干支/土王后等忌项不得从破土条静默拷到安葬条。
6. **「密日」**：索引 312 notes 已记起法未详、不擅补；保持 unknown。
7. **本 edition remaining 0**：勿再开星历考原主本续写包；质量 caveat 与未知项不回改注解，也不升 verified。

## 未决（本岗不施工）

- 密日起法、土王用事后边界、人神在头日具体排法：保持 unknown，不升 verified。
- 电子源非影印校勘。15 条（及全书 315 条）source-reviewed 不是人工 verified，也不是择日有效性证明，也不等同产品算法已实现。
- 不重做 CP1 0–299；不重做太乙 0–208；不改旧总述。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-311`。
