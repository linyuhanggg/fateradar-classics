# 入地眼全书 · 主本：独立审查 source-reviewed 全量（0–125 / 126）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-440` / 分支 `codex/multica-ming-440`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/rudi-yan-quanshu.md`、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-424 / MING-431。

结论：**通过。** `validate-annotations` `ok=true entries=126 source_reviewed=126 errors=[]`；`verified` 无 True（126 条均未写该字段，校验器视为未升 verified）；0 draft；起 `rudi-yan-quanshu:L0005-L0005` 止 `rudi-yan-quanshu:L1023-L1034`；注解与段落库存 126/126 顺序全等。抽读 ≥15 段对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。风水进入知识检索，不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-440`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/rudi-yan-quanshu.json
shasum -a 256 sources/fulltext/fengshui/rudi-yan-quanshu/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/rudi-yan-quanshu.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/rudi-yan-quanshu.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `e682c8044af0fefc9478db62d4869c348e6fde276b69ccf528f2b52c467ac64a`（与 Issue 钉死一致） |
| 注解 blob | `cdb416af9494d48a312fbb1d64a2b1b9619ded49`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/rudi-yan-quanshu/fulltext.md`（1034 行） |
| 源 SHA256 | `c8fe62724f10366fae5a8cfde2fad34eb7d49f3dddcca4602cfcb2fdb19044c4` |
| Issue 所写 `sources/normalized/fengshui/rudi-yan-quanshu.md` | **本树不存在**；段落库存 `fulltext` 指向 `sources/fulltext/.../fulltext.md` |
| 库存段落 | `references/inventory/paragraphs/fengshui/rudi-yan-quanshu.json` 126 条，ID 顺序与注解全等 |
| 非空源行覆盖 | 905/905，未覆盖非空正文 0 |
| catalog `source_anchor_url` | 维基文库单页整理本；`source_provenance_status=consolidated_catalog`；LIBRARY_INVENTORY「尚未确认影印」 |

无越权文件。本岗相对 329 只新增本审查稿。未碰 424/431 工作树或分支。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/rudi-yan-quanshu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 126, "source_reviewed": 126,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

126 条：`review=source-reviewed` 全 126；无 `draft`；无 `verified: true`（字段全部缺省，校验器与「verified 全 false」同口径）。空白话 0；白话全文重复组 0；空 terms 0；空 notes 69（结构合法）。`relatedParagraphIds` 46 条、106 个外键，全部落在本书 126 个 ID 内。kind 与库存逐条一致。

全书 kind：序跋目录 56、理论 26、规则候选 26、操作步骤 6、术语 5、待核实 5、评注或元数据 1、案例 1。

待核实仅 5 段，均保留 unknown，不补造：

| 索引 | paragraphId | 保留原因（对照原文） |
|---|---|---|
| 6 | `rudi-yan-quanshu:L0055-L0076` | 万跋「恍然不畢合」与后文冰释衔接不顺；「遊癢序」「玷汙弗暇」待校 |
| 11 | `rudi-yan-quanshu:L0086-L0086` | 例言两见「古蘭經」，地理引据语境未明，未改成某部宗教经典或「古经」 |
| 27 | `rudi-yan-quanshu:L0227-L0238` | 「土一星 / 下一廟 / 下九天」含混，不新增一颗土星天体 |
| 41 | `rudi-yan-quanshu:L0317-L0325` | 「貪狠」不默认为贪狼；「根龍 / 入根」与艮混用，原字保留 |
| 90 | `rudi-yan-quanshu:L0738-L0747` | 「遂無不合一之致」不擅改成无法统一 |

## 4. 索引边界

段落库存 126 段；注解覆盖 0–125，与库存 ID 列表逐项相等。`remaining=0` / 无 nextId，只相对本电子本 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `rudi-yan-quanshu:L0005-L0005` |
| 注解索引 125（止） | `rudi-yan-quanshu:L1023-L1034` |

电子本题卷：天星卷一（L92）→ 龙法卷二（L643）→ 砂法卷四（L728，文内「凡二卷」）→ 水法卷六（L791，文内「凡上下卷」）→ 向法卷九（L923）→ 阳宅卷十（L960）。标题跳号不是本包失败条件；见 caveat。`remaining=0` ≠ 人工 verified / ≠ 十卷完帙 / ≠ 影印校勘 / ≠ 产品交付。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/rudi-yan-quanshu/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0005` | 评注或元数据 / sr | 源 L5「宋-靜道」。仅朝代名号，不补作者生平 | 通过 |
| 1 | `L0007-L0007` | 序跋目录 / sr | 源「週兆熊序」。白话称周，notes 保留「週」 | 通过 |
| 16 | `L0096-L0123` | 理论 / sr | 易传套语落到天帝顺行十二宫、太阳逆行十二宫；「幹道成男」不改乾 | 通过 |
| 21 | `L0173-L0192` | 规则候选 / sr | 标题乾龙法、正文「幹龍」；不可与亥同行；五备/鬼气 | 通过 |
| 25 | `L0207-L0223` | 规则候选 / sr | 亥龙单清过脉；五龙难下兼左兼右则房分受害。草稿「不单清」已不在现行稿 | 通过 |
| 29 | `L0242-L0246` | 规则候选 / sr | 壬地紫微一白；不可与亥同行（龙身带曜）；三条路径分说 | 通过 |
| 59 | `L0433-L0460` | 规则候选 / sr | 来龙不兼甲乙 ≠ 水向阴阳相配；八十/六十/四十/二十原文说寿数 | 通过 |
| 66 | `L0533-L0541` | 规则候选 / sr | 乙龙必须单乙；催官口诀辛山乙向 / 乙水坤向 | 通过 |
| 76 | `L0617-L0617` | 案例 / sr | 巽巳双来、孙膑祖茔；源「劊足」，白话作刖足传说，不补史实 | 通过 |
| 85 | `L0661-L0695` | 操作步骤 / sr | 寻龙以少祖/父母为主；胎息孕育；面背由水来合与砂向内判断 | 通过 |
| 93 | `L0753-L0753` | 术语 / sr | 火星尖利＝廉贞/燥火；双峰＝双荐/文笔。不是紫微廉贞星曜算法 | 通过 |
| 95 | `L0757-L0762` | 术语 / sr | 金星正体太阳/左辅；方而带圆＝右弼/太阴。砂名，不是天文或八字 | 通过 |
| 102 | `L0795-L0809` | 理论 / sr | 水以形象第一，斜飞直冲虽吉方仍祸；末「凡上下卷」 | 通过 |
| 104 | `L0813-L0844` | 规则候选 / sr | L826「不出半紀而發」+ L827「十二年為一紀」⇒ 半纪六年，不是十二年 | 通过 |
| 111 | `L0937-L0951` | 规则候选 / sr | 翻卦四阳乾离坎坤 / 四阴艮巽震兑，不能换成后文阳宅东四西四 | 通过 |
| 112 | `L0953-L0958` | 理论 / sr | 「紅黑一盤詳水路，究來不必辨龍神」与前文龙为根本分语境保留 | 通过 |
| 115 | `L0964-L0982` | 理论 / sr | 西四乾坤兑艮、东四坎离巽震；七政＝贪巨禄文廉武破，不是日月五星 | 通过 |
| 123 | `L0998-L1008` | 操作步骤 / sr | 「逆生而入」但明列金→水→木→火→土→金，不倒转五行相生 | 通过 |
| 124 | `L1010-L1021` | 操作步骤 / sr | 变宅六七栋改取游星，不能只按相生漏掉星选择 | 通过 |
| 125 | `L1023-L1034` | 操作步骤 / sr | 九栋末右弼生气木；「如止八重」末重改右弼生气木，不得截在八栋五鬼火 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 宋-静道：L5
- 週兆熊序：L7
- 天帝顺行 / 太阳逆行：L121–L122
- 幹龙不可与亥同行：L173–L174
- 二十四龙五龙难下、单清过脉：L211–L219
- 来龙孤虚 ≠ 水向夫妇相配：L433–L449
- 半纪 / 一纪十二年：L826–L827
- 砂法卷四 + 凡二卷：L728、L747
- 水法卷六 + 凡上下卷：L791、L809
- 翻卦四阴四阳：L942–L947
- 阳宅东四西四：L976–L977
- 七政游星加辅弼为九曜：L981
- 竹节贯井相生：L998–L1004
- 八栋化宅右弼生气木：L1023–L1034
- 古兰经：L86
- 根龙 / 贪狠：L317–L325

## 6. source-reviewed ≠ 人工 verified

本电子本来源为维基文库整理本，LIBRARY_INVENTORY 记「尚未确认影印」。126 条 `source-reviewed` 只表示对照当前电子段落实了序跋层次、龙法兼带、砂水形象、翻卦与阳宅分组、待核实去向，不是影印逐字校勘，也不是风水效验证据。风水材料进入可检索知识库，当前页面没有对应输入与算法，不得冒称已接入八术。不得把 126 条 source-reviewed 写成已人工 verified。`remaining=0` 仅对本电子本注解覆盖而言。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 字段缺省 | 126 条均无 `verified` 键；0 条 True | 与「全 false」同口径。不回改 |
| 空 notes | 69/126 | 结构合法。抽核白话非空。不回改 |
| 待核实 5 段 | 见 §3 | 正确保留 unknown。不回改 |
| 卷次跳号 | 见卷一、二、四、六、九、十；缺卷三/五/七/八标题 | 砂法「凡二卷」、水法「凡上下卷」为合卷线索，不凭标题断言整卷缺失。不回改 |
| 异体/疑字 | 週/周、幹/乾、醜/丑、根/艮、劊足/刖足 | 引文不改原字。白话可解释。不升 verified |
| 旧 skill `chapter-map.md` | `source_lines: 255`，与现行 1034 行全文不一致 | 过期蒸馏表，不在本包写出范围。不回改 |
| Issue 源路径 | `sources/normalized/fengshui/rudi-yan-quanshu.md` 不存在 | 对照实际 `sources/fulltext/.../fulltext.md`。不回改路径 |

## Caveat（不改注解，留给后续 pack）

1. **无同书影印**：source-reviewed 停在电子语义；古兰经、根/艮、遊癢序、不毕合、无不合一之致保持 unknown。
2. **卷次不连续**：电子本题跳号；完整性须另本/目录/影印，不能从 remaining=0 推出十卷完帙。
3. **阳宅七政 ≠ 天文七政 ≠ 阴宅翻卦分组**：东四西四与净阴净阳、贪巨禄文廉武破与日月五星，接入时必须分表，禁止混层。
4. **竹节贯井**：原文「逆生而入」容易误读成逆转相生；现行白话已按金水木火土金保存。八栋不得截用九栋的第八位五鬼火。
5. **孙膑条**：源作「劊足」；白话用刖足传说。引用须回 L617，不当作史实。
6. **`remaining=0`**：只表示本电子本 126 个 paragraphId 已尽；不是人工 verified、不是全书校勘、不是产品交付。

## 未决（本岗不施工）

- 5 条待核实与卷次完整性：保持 unknown / 回源，不升 verified。
- 126 条 source-reviewed 不是人工 verified，也不是风水效验，也不等同风水算法已实现。
- 本岗不回改注解、不改 `rudi-yan-quanshu.md`、不碰 424/431。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-440`。
