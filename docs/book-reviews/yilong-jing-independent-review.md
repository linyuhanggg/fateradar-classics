# 疑龙经：独立审查主本 source-reviewed 全量（文件索引 0–95）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-441` / 分支 `codex/multica-ming-441`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/yilong-jing.md`、未抢 MING-424/431、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–95（96 条，全量）。

结论：**通过（有限范围）。** 结构校验 ok、`errors=[]`；96/96 `source-reviewed`、0 draft；`verified` 键全缺（无一为 true）；inventory 与注解 `paragraphId` 一一对应且同序；≥15 段（实际抽核 27）对照原文语义成立；疑字/合刊异文 notes 可复核且未静默改正文。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-441`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/yilong-jing.json
git rev-parse HEAD:references/annotations/fengshui/yilong-jing.json
shasum -a 256 sources/fulltext/fengshui/yilong-jing/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `f88f12dd29173e3dfd26103cca64cc2cbeb671839fb5a7f70c74f671f792491f`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `c1e804a38ed643f8fe2dceb66501e7c9a8e69a7d` |
| 源 `fulltext.md` SHA256 | `545d07301c3262342c66aea811d5071adf034b455ca83ef1e767482323cca2a4` |
| 源行数 | 755 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `yilong-jing.md` 无 diff |

路径说明：Issue 对照写 `sources/normalized/fengshui/yilong-jing.md`；仓内权威路径是 inventory 所记 `sources/fulltext/fengshui/yilong-jing/fulltext.md`。本岗按 fulltext 抽核，不另造 normalized 副本。

无越权文件。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/yilong-jing.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 96, "source_reviewed": 96,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`source_reviewed=96` 与 Issue 口径一致。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–95，96 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 96/96 |
| `review=draft` | 0 |
| `verified` 键 | **全缺**（96/96 无该字段；无一 `verified=true`） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 缺失 | 0 |
| 空 `terms` | 0 |
| `subsections` | 0 |
| `sourceAttribution` | 0 |

kind 分布：规则候选 41、理论 16、术语 16、序跋目录 12、待核实 5、操作步骤 4、案例 2。

Issue 钉死「verified 全 false」：本文件用缺省未升 verified（键缺失）表达，与「不得升人工 verified」一致；校验器仅在 `verified is True` 时报错，本包未触该条件。

Issue 钉死起 `yilong-jing:L0003-L0008`、止 `yilong-jing:L0755-L0755`：与文件索引 0、95 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/yilong-jing.json` 96 段；注解 96 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。

非空源行仅 L1 Markdown 书题 `# 疑龙经` 未入段；其余非空行落在某条 `paragraphId` 内。空行 96 处未入段（段落间隔）。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起） | `yilong-jing:L0003-L0008` | 目录：上/中/下篇 + 三附篇 |
| 索引 1 | `yilong-jing:L0010-L0022` | 上篇开篇：枝干疑龙 |
| 索引 21 | `yilong-jing:L0384-L0384` | 《疑龙十问》第一问标题 |
| 索引 42 | `yilong-jing:L0606-L0649` | 《卫龙篇》主体 |
| 索引 43–95 | `L0651`…`L0755` | 《变星篇》短句为主 |
| 索引 95（止） | `yilong-jing:L0755-L0755` | 变星收束 |

本包后该书 SR 审查 remaining **0**。这只表示 96 主段都已有 source-reviewed 注解并经本岗抽核，不是 755 行逐句影印校勘，也不是 verified。既有 `docs/book-reviews/yilong-jing.md`（生产侧账本）不覆盖、不回改。

## 5. 抽样语义（≥15，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/yilong-jing/fulltext.md` 的行范围。下列为非模板抽核（覆盖序跋、理论、规则、操作、待核实、案例、术语；含十问、卫龙、变星）：

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0008` | 序跋 / SR | 六行目录；附篇名繁体与后文标题不完全一致，notes 已记 | 通过 |
| 1 | `L0010-L0022` | 理论 / SR | 星峰或为枝；旗枪护送；「金不作」未定死金星规则 | 通过 |
| 2 | `L0024-L0040` | 规则候选 / SR | 虚花/结实、一叠 vs 三五重、尽处仍忌风吹水劫 | 通过 |
| 4 | `L0062-L0076` | 操作步骤 / SR | 先舆图水源；军州县分等；「斡长」疑干，不改正文 | 通过 |
| 6 | `L0095-L0114` | 操作步骤 / SR | 关峡≠明堂；YL L109「外天攔」vs 撼龙合刊「外無攔」异文 notes 可核 | 通过 |
| 8 | `L0135-L0152` | 待核实 / SR | 喝石/海孺等疑字不径改地名；海岸风荡散不自动最优 | 通过 |
| 9 | `L0154-L0208` | 操作步骤 / SR | 背面/落头/罗星；上坡下坡例外并列；疑字不补操作 | 通过 |
| 11 | `L0236-L0257` | 理论 / SR | 十山同聚辨主客；「只论长」与不论贵转折保留 | 通过 |
| 15 | `L0303-L0315` | 案例 / SR | 城邑比附非现代选址实证；「六七存」不补定禄存 | 通过 |
| 20 | `L0370-L0382` | 案例 / SR | 明堂案山与周秦/申伯感应说；不作国运判定 | 通过 |
| 21 | `L0384-L0384` | 序跋 / SR | 十问第一问标题；答文在下段 | 通过 |
| 24 | `L0413-L0438` | 理论 / SR | 公位/河图九宫沿革分层；坎中男与离列不拼一表 | 通过 |
| 28 | `L0468-L0476` | 待核实 / SR | 「性穴小」vs「要穴大」不顺；合刊「怕穴小」对照，不静默改版 | 通过 |
| 30 | `L0480-L0480` | 规则候选 / SR | 两宅；葬小居大；吕才不补书名 | 通过 |
| 38 | `L0538-L0563` | 待核实 / SR | 花假穴；「假穴在后亦堪下」与排除语气不顺，不擅补主语 | 通过 |
| 40 | `L0567-L0602` | 规则候选 / SR | 干不问祖 vs 枝必顾宗分两类；变星节数法 | 通过 |
| 42 | `L0606-L0649` | 理论 / SR | 卫龙/天池；垣局比附；「不央过」等疑字；合刊可对「中央過」 | 通过 |
| 45 | `L0655-L0655` | 术语 / SR | 贪变巨门「方磊落如屏」；不说成巨门唯一样 | 通过 |
| 49 | `L0663-L0663` | 规则候选 / SR | 禄存带禄长短穴正形；依赖前段形态 | 通过 |
| 55 | `L0675-L0675` | 规则候选 / SR | 石间/深潭异穴并列，非操作指令 | 通过 |
| 62 | `L0689-L0689` | 规则候选 / SR | 盖天旗限定，非凡旗山皆君相 | 通过 |
| 70 | `L0705-L0705` | 规则候选 / SR | 不变星乳突/窝；合刊〔闕〕不补本单篇后续 | 通过 |
| 76 | `L0717-L0717` | 待核实 / SR | 「我他说」不明，不圆成秘义 | 通过 |
| 82 | `L0729-L0729` | 规则候选 / SR | 捍门+罗星→公候；候/侯不一不径改 | 通过 |
| 90 | `L0745-L0745` | 理论 / SR | 时师误下之戒，无现实事故核验 | 通过 |
| 93 | `L0751-L0751` | 待核实 / SR | 「魂惡」「瞿」疑字不按通顺改 | 通过 |
| 95 | `L0755-L0755` | 理论 / SR | 心镜昭圆收束；非新操作、非预测能力证明 | 通过 |

抽核未发现空模板白话、把合刊异文覆盖本版、把案例升实证、或把 `verified` 置 true。待核实条（索引 8/28/38/76/93）疑字 notes 成立。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1 书题「疑龙经」；L3–755 入段）。96 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/疑字去向，不是影印逐字校勘，也不是风水断语有效证据，也不等于寻龙/明堂/变星已写入产品引擎。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是疑龙经全书产品交付，也不覆盖生产侧 `docs/book-reviews/yilong-jing.md`。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| Issue 路径 `normalized/...` | 仓内无该文件；inventory=`fulltext.md` | 按 fulltext 抽核。不回改 Issue 历史措辞 |
| `verified` 键缺失 | 96/96 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 「外天攔」vs「外無攔」 | YL L109 vs 撼龙合刊同段 | notes 已记。分版保留 |
| 「性穴小」vs「怕穴小」 | YL L0470 vs 合刊 | 并读方向清楚。不改正文 |
| 「不央過」vs「中央過」 | 卫龙篇 | 合刊对照。不静默补字 |
| 候/侯 | 源内「公候」「公侯」并存 | 不径改 |
| 案例城邑/史事 | 冀州太原建康长安、周秦申伯等 | 按传统比附。不升实证 |
| 变星短句密集 | 索引 43–95 多为单行 | SR 成立于句级条件。非拆 ID |

## Caveat（不改注解，留给后续 pack）

1. **疑字与合刊异文不是已校定。** 「外天攔」「性穴小」「不央過」「我他说」「魂惡」等仍待校；合刊只作对照。
2. **十问公位/河图列法有多层沿革。** 不得拼成一张无分层位置表去驱动产品。
3. **案例与贵显断语** 是传统人地感应论述，不是城市选址或官贵核验证据。
4. **既有 `yilong-jing.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。

## 8. 交付

| 项 | 值 |
|---|---|
| Issue | MING-441 |
| 分支 | `codex/multica-ming-441` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/yilong-jing-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后闭环；无需重做 0–95；无需回改注解。
