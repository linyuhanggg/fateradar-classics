# 《柳庄相法》主本：独立审查全量（2 段）

审查对象：[MING-210](mention://issue/01a09036-3839-7b8e-bb8e-b7c2d3f42523) `origin/codex/multica-ming-210` @ `9bb4d4a4e5cf85182d245aaf20556b0f356fe6eb`（父 `bc798566da77c30e149abf9673c88ecc386702b2`）。工作树只读参考 `fateradar-multica-ming-210`，本岗写出仅本文件。未改注解 JSON、未改源文、未改青囊 / 撼龙 / 协纪 / 麻衣 / 神相全编 / 冰鉴 / 引擎 / `chart.*`。不是相法全书校勘，不是续写，不是八术算法覆盖，也不是全项目完成。

结论：**通过。** 相对父提交仅注解+进度；独立复跑 `validate-annotations` `ok=true entries=2 errors=[]`；`verified` 全 false；长段 `L0007-L0933` 135 子节非空模板；疑文标 unknown 且源文未改。`remaining=0` 只指本 inventory 2 段索引齐，**不是**人工 verified。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。失败段 ID 见 §8，均属白话压缩误差，不是空模板、不是改正文。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-217`，2026-09-11）：

```
git fetch origin 9bb4d4a4e5cf85182d245aaf20556b0f356fe6eb bc798566da77c30e149abf9673c88ecc386702b2
git rev-parse HEAD HEAD^
git ls-remote origin refs/heads/codex/multica-ming-210
git diff --name-status bc798566da77c30e149abf9673c88ecc386702b2..9bb4d4a4e5cf85182d245aaf20556b0f356fe6eb
git rev-parse bc79856:sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md
git rev-parse HEAD:sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md
shasum -a 256 sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-210` | `9bb4d4a4e5cf85182d245aaf20556b0f356fe6eb`（本岗检出 SHA 与 `ls-remote` 一致） |
| 父提交 | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 相对父提交文件 | 仅 2 个新增：`references/annotations/physiognomy/liuzhuang-xiangfa.json`、`docs/book-reviews/liuzhuang-xiangfa-progress-2026-09-11.md` |
| diffstat | `+2051`（两文件均为新增） |
| 父树该注解 / 进度 | **不存在** → 本提交新建 |
| 源 `fulltext.md` SHA256 | `d94f837fd8fb1e3f636d9cf21d73fdf6300c7cc61669c9a8f0015da4eb72adfe`（与交包钉死值一致） |
| 源 blob 父 vs 本提交 | 同 `0406d7b63abb3e27a018005d06d437db05507128`（未改源层） |
| 源行数 | 933；末行非空 |
| 注解 blob | `66deb5b7e3d44e04756d580b67bec312117ab9be` |
| inventory | 2 段；注解 ID 与 inventory 一一对应 |
| `shenxiang-quanbian.json` / `bingjian.json` | blob 与父提交相同 |
| 青囊 / 撼龙 / 协纪 / 引擎 / `chart.*` | 不在 diff |

无越权文件。源层未改。他书未覆盖。不是续写包。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-210 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/physiognomy/liuzhuang-xiangfa.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2, "source_reviewed": 2,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`entry.get("verified") is True` 才会报错；本文件 2 条均为显式 `false`。

## 3. verified / draft 未越权提升

2 条：`review=source-reviewed` 全 2；`verified` 全 `false`；`draft` 0。无升 verified。

| paragraphId | kind | review | verified | subsections |
|---|---|---|---|---|
| `liuzhuang-xiangfa:L0003-L0005` | 评注或元数据 | source-reviewed | false | 0 |
| `liuzhuang-xiangfa:L0007-L0933` | 理论 | source-reviewed | false | 135（S001–S135） |

长段子节：ID 唯一、起迄 `L7–933` 无缺口无重叠；白话 / terms / notes 均非空；白话互不重复；无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。子节白话长度 min 20 / 中位 34 / max 67。进度表九个区段行号与子节起迄一致。134/135 题名落在该子节首行原文（S001 题作「上册标记」，源仅「1. 上册」）。

## 4. 索引边界

inventory `references/inventory/paragraphs/physiognomy/liuzhuang-xiangfa.json` 仅 2 段。本包覆盖 **2/2**。进度 `nextId` 无、`remaining=0`（本注解 paragraphId 集合口径）。

| 位置 | 实测 ID | 源据 |
|---|---|---|
| 注解/源起 | `liuzhuang-xiangfa:L0003-L0005` | 文件 L3–5：`source_base` / `ctext_anchor` / `normalized_note` |
| 长段 | `liuzhuang-xiangfa:L0007-L0933` | 文件 L7「1. 上册」至 L933「出嫁夫」截断 |
| remaining | **0** | 仅本 inventory 2 段 |

起始/止点与 Issue 钉死 ID 一致。remaining 0 只表示这两段索引齐，不是影印校勘完成，不是麻衣/神相全编/冰鉴完成，也不是相法接入八术。

## 5. 抽样语义（对照原文，不凭进度摘要）

原文取 `sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md` 的文件行。下列为元数据、方法声明、部位论、十二宫、清单、永乐百问与疑文抽核。

| 子节 | 源行 | kind 层 | 对照要点 | 判定 |
|---|---|---|---|---|
| 条目 `L0003-L0005` | L3–5 | 评注 | 三行采集元数据：CTP Wiki、NLC PDF 锚点、高风险声明。白话不把元数据当断法 | 通过 |
| S001 | L7 | 题记 | 源仅「上册」。分册标记，不是断语 | 通过 |
| S004 | L14–16 | 临盆 | 印堂/准头/口角/颧/仑下库配丙丁戊己等「曰」；右手心乾坎明堂。notes 保留「曰期」 | 通过；疑文未改正文 |
| S014 | L81–82 | 方法 | 「不可定一理而推」：美处有破、恶处可取；审声音与五官六府 | 通过 |
| S016 | L85–88 | 传授 | 夷相法 / 麻衣授陈翁 / 七十三家 / 今人薄削。notes 保留「夷相法」 | 通过 |
| S023 | L109–147 | 寿夭 | 骨坚肉实、眉毫耳毫寿斑枕骨，及耳项头皮唇时限。未合成单一寿命公式 | 通过结构 |
| S036 | L180–181 | 土星 | 源作「兰台**延慰**」；白话写「兰台**廷尉**」。notes 称异写并存 | 通过结构；见 caveat |
| S042 | L212–258 | 乾坤赋 | 女相柔清贵浊贱；印目鼻颧等宜忌与诗句。题署「近永乐」未当史证 | 通过 |
| S074 | L421–469 | 十二宫 | 命财兄弟田宅男女奴仆妻妾疾厄迁移官禄福德相貌。notes 标明不与紫微十二宫合并 | 通过 |
| S077 | L509–527 | 十八下贵 | 纳粟承差九品提牌都吏等 18 条。首行夹「以上十八中贵」收束 | 通过结构；见 caveat |
| S078 | L528–600 | 七十二贱 | 源 1–72 齐全；第 33 条「皮滑舅油」仍在 L561。白话点名清单+污名限制 | 通过；疑文未改正文 |
| S087 | L756–760 | 寒通 | 寒/通/得/失分层；L760 止于「气色定行年休咎，」 | 通过；疑脱文未补造 |
| S089 | L763–775 | 古望人 | 太宗/关羽/孟堂君/刘备/杨六郎等气色故事。「孟堂君夜津阔津」保留 | 通过 |
| S096 | L806–834 | 五行形赋 | 金木水火土真形与赋末拗口句。末句未改字 | 通过 |
| S098 | L836–837 | 百问 1 | 王位：龙生凤长、身面腰步须长合龙相 | 通过 |
| S100 | L840 | 百问 3 | 天庭低不忌：日月角辅弼、头平面圆、五行相配 | 通过 |
| S101 | L841–842 | 百问 4 | 问欲面方为配；对曰面方是虎面杀星、凤形面圆才贵。白话写成「强调面方匹配」 | **语义写反**；见 §8。非空模板 |
| S104 | L847 | 百问 7 | 问答同行：项下红丝、耳轮多赤难逃刀斧 | 通过 |
| S105 | L848 | 百问 8 | 源仅问句「曰月交锋，反得善终」；次行已是第 9 问。白话称「答文在次行」 | **无对曰**；见 §8。非空模板 |
| S111 | L860–861 | 百问 14 | 舜目凤目细长 vs 「办有」/项目鸡眼圆露。notes 保留「办有」 | 通过 |
| S118 | L873–874 | 五露五反 | 一至四露递加不利、五露俱全反贵；「挂紫友」未补字 | 通过 |
| S120 | L882–888 | 南北 | 自称古书无、先生心法；「太原乃陕西」未改正文 | 通过 |
| S126 | L910–911 | 三停 | 面三停（发际–山根 / 准头 / 人中–地阁）与身三停（颈腰脚）分层 | 通过 |
| S129 | L916–917 | 三阳 | 眼下卧蚕/男女宫 与 印准颧 两套同名 | 通过 |
| S135 | L932–933 | 百问 38 | 厨灶空、奸门陷、鱼尾多纹；文止「出嫁夫」。unknown 不补造 | 通过 |

关键源行（抽核，非转引进度表）：

- 采集元数据：L3–5
- 上册题记：L7
- 「临盆可定曰期」与产妇诀：L14–16
- 「不可定一理」：L81–82
- 夷相法 / 七十三家：L85–88
- 兰台延慰：L181
- 十二宫命宫：L421–425
- 七十二贱第 33「舅油」：L561
- 寒通「气色定行年休咎，」：L760
- 孟堂君夜津阔津：L766
- 五行赋末拗口句：L834
- 永乐百问题：L835
- 面方虎面 vs 凤形：L841–842
- 「曰月交锋」无对曰：L848
- 「办有重瞳」：L860–861
- 「挂紫友」：L874
- 「太原乃陕西」：L887
- 两套三停 / 两套三阳：L911、L917
- 文末「出嫁夫」：L933

## 6. source-reviewed ≠ 人工 verified

2 条电子语义阅读升 `source-reviewed`，只表示对照当前 CTP 行号电子段落实了层次、清单结构、问答与疑文去向，不是影印逐字校勘，不是人类专家看相验人，不是预测有效证据，也不是算法可执行。不得把 `source-reviewed=2` 或 `remaining=0` 写成已人工 verified。本包是主本 inventory 2 段一次性标注，不是相法类全书，也不是产品交付。

既有 `docs/book-reviews/liuzhuang-xiangfa-progress-2026-09-11.md` 是标注岗进度，不是本岗独立审查证书。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 疑文仍在源 | `曰期` L14、`夷相法` L86、`延慰` L181、`舅油` L561、`孟堂君夜津阔津` L766、`办有重瞳` L860、`挂紫友` L874、赋末 L834、`出嫁夫` L933 | 与父提交逐字相同。不回改 |
| 长段 kind=理论 | 900 余行含方法、部位、清单、歌赋、君臣问答 | 结构合法（kind 在允许集）。接入只能分层消费子节。不回改 |
| 清单白话压缩 | 七十二贱 / 三十六刑伤 / 五十一孤等只点类型与样例，未逐条抄 | 非空模板。接入须回源编号。不回改 |
| S077 首行夹层 | L509 同时收束「十八中贵」并起「十八下贵」 | 源行粘连，不是切段错误。不回改 |
| 父条白话 | 长段 vernacular 是 135 子节摘要串接，8359 字 | 与子节题名全覆盖。不回改 |
| `verified` 显式 false | 2/2 | 不得补 true |

## 8. Caveat（不改注解，留给后续 pack）

1. **S101 `L841–842` 白话写反**：源问欲得「面方」妃；对曰「凡面方者为虎面，必犯杀星，岂能入宫」，真贵是「凤形面圆」。白话「强调面方匹配」把问句当成答意。接入须回源对曰，不能按白话做匹配规则。不构成本包失败（非空模板、未改正文）。
2. **S105 `L848` 无对曰**：源该行只有问句「曰月交锋，反得善终，为何？」；L849 已是第 9 问吴尚书母。白话「答文在次行」不成立。此问保持 unknown，不得从邻条发明条件。
3. **S036 廷尉/延慰**：本电子源只有「兰台延慰」，无「廷尉」。白话与 notes「异写并存于文」是用通行相法词对照，不是本页两写。未改正文；接入引文须用「延慰」。
4. **kind 过宽**：清单与百问标在同一「理论」条目下。规则库若抽取，必须按子节，不能把七十二贱或选妃问答当成一条可执行规则。
5. **同名分层**：三停（面/身）、三阳（眼下/印准颧）、十二宫（相法部位宫 ≠ 紫微十二宫）、五官（采听等官名 ≠ 星曜）已在 notes 提示。禁止自动合并。
6. **remaining 0 正确**：inventory 2/2。不要从 L0933 后续写、不要开相法全书校勘、不要把本包算进八术页面交付。

## 未决（本岗不施工）

- 文末截断、曰期/舅油/办有/挂紫友/延慰/孟堂君等疑文：保持 unknown，不 OCR、不补造、不升 verified。
- S101 / S105 白话误差：记录在案，不回改 JSON。
- NLC PDF 仅锚点，未逐页校勘；CTP 与影印是否同版仍 unknown。
- 2 条 source-reviewed 不是人工 verified，也不是预测有效，也不是算法覆盖。
- 勿重做这两段；勿改注解 JSON；勿开麻衣/神相全编续包冒充本审查。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-217`。
