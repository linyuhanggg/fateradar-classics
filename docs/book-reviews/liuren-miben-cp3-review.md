# 大六壬秘本：独立审查主本 source-reviewed CP3（索引 600–899）

审查对象：权威树 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`（主本生产收口见 [MING-97](mention://issue/01a08ef2-5829-7788-bf68-6849379f035b)）。工作树 `fateradar-multica-ming-388` / 分支 `codex/multica-ming-388`。本岗写出仅本文件。未改注解 JSON、未改 `sources/fulltext/san-shi/liuren-miben/fulltext.md`、未改大六壬大全/识典文件、未改 CP1/CP2 审查稿、未改进度账本。本岗未参与六壬秘本生产。不要重做 [MING-379](mention://issue/01a09153-00f1-766b-8e19-c82683b53304) CP1。不要与并行 CP2 写同一审查稿。不要从 CP1 重写注解。不要抢识典 SDZJ0170 / 大六壬大全 JSON。

结论：**通过。** 结构校验、SHA、索引边界、draft 保守处置与 ≥15 段原文对照抽样均成立。`source-reviewed` ≠ 人工 `verified`；电子阅读 ≠ 影印校勘。本包后索引 remaining **900–2642（1743）** ≠ 全书完成。下列 caveat 不构成本包失败，也不把 draft 升 SR / verified。本岗未改注解。

## 1. 指针与越权核验

独立命令（本岗树 `fateradar-multica-ming-388`，2026-09-12）：

```
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/san-shi/liuren-miben.json
shasum -a 256 sources/fulltext/san-shi/liuren-miben/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

结果：

| 项 | 实测 |
|---|---|
| 本地 HEAD | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与交包钉死 SHA 一致） |
| 注解 JSON SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死值一致；本岗未改） |
| 全文 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| `bookSlug` | `liuren-miben` |
| `sourceTitle` | 大六壬秘本（现有电子主文本） |
| entries | 2643（sr=2554 + draft=89）；verified=0 |
| 本包索引 | 600–899：起 `liuren-miben:L4596-L4596` 止 `liuren-miben:L5247-L5260` |
| 本段 review | **296 SR + 4 draft**（与交包一致） |
| inventory 对照 | CP3 300 条 ID 与 `references/inventory/paragraphs/san-shi/liuren-miben.json` 切片 `2011–2310` 顺序全等；全书 2643 ID 集合与 inventory 全等（注解数组整体非全文行序，按生产包序；本包切片内部行序单调） |

无越权文件。本岗仅新增本审查稿。未触碰 CP1/CP2 审查路径、注解 JSON、大六壬大全/识典。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2643, "source_reviewed": 2554,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

与交包一致。JSON SHA 未变。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

本批 300 条（索引 600–899）：

| 项 | 实测 |
|---|---|
| `verified` | 全 `false`（300/300；全书 2643/2643 亦全 false） |
| `review` | source-reviewed 296、draft 4 |
| kind | 规则候选 189、理论 82、评注或元数据 21、操作步骤 4、待核实 3、案例 1 |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文」类空模板 | 0 |
| 白话完全重复组 | 0 |
| 整段原文粘进 vernacular | 0 |

draft 4（均 `verified=false`，不补字、不升 sr）：

| 索引 | paragraphId | kind | 原因（对照源，不改正文） |
|---|---|---|---|
| 722 | `L4840-L4840` | 待核实 | 句首「◎上臾下贝午…」疑字；不据疑字补德诏召徵条件 |
| 809 | `L5064-L5064` | 待核实 | 三奇「甲子旬丑」vs 大全甲子旬奇戌；用神旺相三光 vs 大全三处并行；不改 adapter |
| 817 | `L5083-L5083` | 待核实 | 「酒尘」疑洒；有气带刑必速 vs 休废空亡略，条件不删 |
| 872 | `L5193-L5193` | 规则候选 | 「阴凌阴」疑阴凌阳；支伤干女凌 vs 干胜支女伤不得对调；强娶≠凡求婚皆成 |

4 处均保持 draft，未见擅自升 `source-reviewed`。

## 4. 索引边界

| 位置 | 实测 ID |
|---|---|
| 注解索引 599（上包止，只读） | `liuren-miben:L4594-L4594` |
| 注解索引 600（本批起） | `liuren-miben:L4596-L4596` |
| 注解索引 899（本批止） | `liuren-miben:L5247-L5260` |
| 下一包起点（索引 900） | `liuren-miben:L5262-L5262` |
| 全书末条（索引 2642） | `liuren-miben:L6015-L6018` |

本包覆盖：论争讼后半 → 论富贵 / 论课名（至《管辂神书》卷之十五终）→ 卷之十六《六壬心镜经》占候（晴雨风水、人宅修造、求婚访人、主人善恶、迁官）。本包后 remaining：**索引 900–2642（1743）**。只表示本审查包结束，**不是**大六壬秘本全书 / 引擎 / 产品完成。识典补本不得与主文本混计；本包未触及。

## 5. 抽样语义（≥15，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md`。抽核 **43** 段（含 4 draft + 39 sr），覆盖争讼将神分层、履狱旧事再发、空亡半惊、白虎出行过旬、德诏疑字、贪贿民告、论富贵/课名标题、涉害孟仲、别责柔日三合、官民数十二将、三光三阳三奇六仪、风雨酒尘、宅上雀虎分条、修造三煞、黄道起例、求婚阴凌、访人合例、迁官文龙武常两套迁期。未发现空模板；无整段原文粘进 vernacular；白话无完全重复。条件/救应/反转多数分层清楚。draft 未见擅自升 sr。案例 `L5201` 保持 `verified=false`。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 600 | `L4596` | 理论 / sr | 木金口舌诀；破耗劫争分见注 | 通过 |
| 601 | `L4598` | 规则 / sr | 金木+破碎二耗破才；劫煞勾陈争讼；破才读破财不改正文 | 通过 |
| 610 | `L4616` | 规则 / sr | 贵乘亥克干；官符争田宅 vs 病符阴小灾分绑 | 通过 |
| 612 | `L4620` | 规则 / sr | 履狱干贵不见 vs 贵传生+官符旧事再发 | 通过 |
| 625 | `L4646` | 理论 / sr | 朱寅官符官讼；病符火灾分见 | 通过 |
| 638 | `L4672` | 规则 / sr | 勾罗网争讼；入空亡半惊减实 | 通过 |
| 651 | `L4698` | 理论 / sr | 劫煞刑伤制贵；归避是救应 | 通过 |
| 664 | `L4724` | 理论 / sr | 午官符+吉神诏仪禄马；讼不成见注 | 通过 |
| 676 | `L4748` | 理论 / sr | 后合出门阴私 | 通过 |
| 689 | `L4774` | 规则 / sr | 天空虚诈；与卷十四将空同向不合并 | 通过 |
| 700 | `L4796` | 规则 / sr | 白坐年辰入空行不成；带游神要过旬 | 通过 |
| 702 | `L4800` | 规则 / sr | 虎+旺鬼+诸煞才官符争讼 | 通过 |
| 715 | `L4826` | 规则 / sr | 阴后临酉加丁则财被妇争，非有财 | 通过 |
| 722 | `L4840` | 待核实 / draft | 句首疑字德诏；不补条件 | 通过 |
| 729 | `L4854` | 规则 / sr | 贪贿叠层 vs 下克上谩语天祸民告 | 通过 |
| 742 | `L4880` | 规则 / sr | 朱官符岁刑罗网讼凶 vs 六合合申捕贼分条 | 通过 |
| 750 | `L4896` | 规则 / sr | 龙克年+用喜破＝破财大祸；谨慎救应 | 通过 |
| 754 | `L4904` | 理论 / sr | 龙入渊钩竿诗 | 通过 |
| 757 | `L4910` | 评注 / sr | 论富贵标题；不改九宗门 | 通过 |
| 767 | `L4930` | 理论 / sr | 丁马入空不去不来 | 通过 |
| 769 | `L4934` | 评注 / sr | 论课名标题；不改大全取传 | 通过 |
| 780 | `L4977-L4986` | 规则 / sr | 涉害孟仲；刚柔上神 vs 大全见机察微并行；不默认取季 | 通过 |
| 793 | `L5012` | 规则 / sr | 别责柔日取三合位上神；与大全阴日存疑并行 | 通过 |
| 800 | `L5043-L5046` | 规则 / sr | 官民数；鬼乘夜病/日讼；十二将分条 | 通过 |
| 806 | `L5058` | 规则 / sr | 时逢富贵+将得时临才平民得志 | 通过 |
| 809 | `L5064` | 待核实 / draft | 三光三阳；三奇甲子丑 vs 大全戌；入狱有救 | 通过 |
| 810 | `L5066` | 评注 / sr | 卷之十五终 | 通过 |
| 817 | `L5083` | 待核实 / draft | 龙虎风雨；酒尘疑洒 | 通过 |
| 821 | `L5091` | 理论 / sr | 水升火降位诀 | 通过 |
| 833 | `L5115` | 规则 / sr | 宅上恶将+雀官事 vs +虎疾病 | 通过 |
| 844 | `L5137` | 操作 / sr | 修造家长行年加岁支；起例未完接下文 | 通过 |
| 846 | `L5141` | 规则 / sr | 岁煞 vs 月煞临日恶 | 通过 |
| 850 | `L5149` | 规则 / sr | 月龙/黑龙忌方；非凡亥子 | 通过 |
| 857 | `L5163` | 操作 / sr | 黄道天罡诀起例 | 通过 |
| 859 | `L5167` | 规则 / sr | 登明危玉堂、功曹司命开通 | 通过 |
| 872 | `L5193` | 规则 / draft | 支伤干女凌；阴凌阴疑字 | 通过 |
| 873 | `L5195` | 评注 / sr | 访人/约来分题 | 通过 |
| 874 | `L5197` | 操作 / sr | 先看居处对神，非日辰上神 | 通过 |
| 876 | `L5201` | 案例 / sr | 戌例合/三合证；verified false | 通过 |
| 886 | `L5221` | 规则 / sr | 辰主人日客；相生+旺相才长者 | 通过 |
| 890 | `L5229` | 规则 / sr | 见贵取青龙小吉 | 通过 |
| 893 | `L5235` | 操作 / sr | 使来伪真先看日辰 | 通过 |
| 899 | `L5247-L5260` | 规则 / sr | 文龙武常；外战罪累/内战疾病；两套迁期；马折足龙化蛇 | 通过 |

关键条件与源行（抽核）：

- 金木口舌分层：L4596、L4598
- 履狱再发：L4620
- 勾罗网空亡半惊：L4672
- 白虎出行过旬：L4796
- 德诏疑字 draft：L4840
- 贪贿/民告：L4854
- 涉害孟仲并行大全：L4977–4986
- 别责柔日三合：L5012
- 官民数十二将：L5043–5046
- 三奇甲子丑 draft：L5064
- 酒尘疑洒：L5083
- 宅雀虎分条：L5115
- 求婚阴凌 draft：L5193
- 访人戌例：L5201
- 迁官两套迁期+马折足：L5247–5260
- 本批止：索引 899 `L5247-L5260`

## 6. source-reviewed ≠ 人工 verified

本批 296 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/条件/救应/反转/未知去向，不是影印逐字校勘，也不是预测有效证据。案例（访人戌例）一律 `verified=false`。不得把 2554 条累计 source-reviewed 写成已人工 verified。本包 remaining 1743 ≠ 全书完成。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 对象 commit / JSON SHA | `6effd8e4` / `30b9b2b9…` | 与 Issue 钉死一致；本岗未改 JSON |
| validator | `ok=true` entries=2643 sr=2554 errors=[] | 结构通过 |
| verified | 全书 2643 false | 未越权提升 |
| CP3 review 比 | 296 sr + 4 draft | 与交包一致；draft 不升 |
| 空模板 / 粘贴原文 | 0 / 0 | 无模板失败 |
| inventory 切片 | 2011–2310 ≡ 注解 600–899 | ID 顺序成立 |
| 涉害刚柔上神 | vs 大全见机察微并行 | notes 已标；不合并 adapter |
| 别责柔日三合 | vs 大全阴日存疑 | 并行；不改 adapter |
| 三奇甲子旬丑 | vs 大全旬奇戌 | draft 809；不改 adapter |
| 迁官迁期 | 位数法 vs 长生月法两套 | 并行；马折足龙化蛇否定 |
| remaining | 900–2642 = 1743 | 不是全书完成 |

## Caveat（不改注解，留给后续 pack）

1. **电子疑字**：德诏句首、酒尘、阴凌阴等，白话已标疑、不改正文；相关条保持 draft。不得据此升 verified。
2. **与大全并行**：涉害取法、别责柔日、三光/三阳、三奇旬位，notes 已标并行/存疑，宁保守不升 sr（809 已 draft），可接受。
3. **标题与起例未完**：论富贵/课名/诸占标题只标范围；修造行年加岁支起例接下文，不把未完起例写成完整算法。
4. **注解数组序 ≠ 全文行序**：全书 entries 按生产包序；本 CP3 切片内部行序成立。后续审查须按 **索引/paragraphId** 匹配。
5. **reference-text**：电子阅读 ≠ 影印校勘 ≠ 预测有效。

## 未决（本岗不施工）

- 本批 4 条 draft 保持 draft。
- 疑字、大全并行存疑，一律 unknown/draft，不升 verified。
- 不改注解 JSON；不从 CP1 重写；不与 CP2 同稿。
- 不抢大六壬大全 / 识典 SDZJ0170。
- remaining 1743 交后续 CP；本审查不宣称全书完成。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-388`。对象 commit `6effd8e4f951fd17e1b1e0454942946ebc765da9`。
