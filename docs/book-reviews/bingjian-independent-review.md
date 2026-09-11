# 冰鉴 · 主本：独立审查 source-reviewed 全量（0–25 / 26）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-480` / 分支 `codex/multica-ming-480`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / executable、未抢 MING-464 集成线与本轮其他审查稿。本岗未参与该书生产。不要与曾国藩托名俗传、麻衣/柳庄坊本或八术产品面相页混为一源。本包只审注解文件索引 0–25（26 条，全量）。

结论：**通过。** 结构校验 `ok=true entries=26 source_reviewed=26 errors=[]`；`verified` **0/26 为 true**（键均缺省，等价保持未升 verified；校验器仅在 `verified is True` 时报错，本文件 0 条触发）；0 draft；起 `bingjian:L0003-L0011` 止 `bingjian:L0162-L0162`；注解与段落库存 26/26 ID 顺序全等。全书 26 段均对照电子原文抽核成立；无空白 vern、无「本段论述 / 白话从略 / 见原文 / TODO」类空模板；无 subsections。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本 26 主段 SR 审查覆盖。相法材料不冒充已接入八术页面。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-480`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/physiognomy/bingjian.json
git rev-parse HEAD:references/annotations/physiognomy/bingjian.json
shasum -a 256 sources/fulltext/physiognomy/bingjian/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `810cdfb7ede3127e0927a559cd06e46e8fdf1a0cc65056783c0fa652807ad67d`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `fd8e50aae37bb08811fb7cfdc99cd047533b1ae8` |
| 实际源文 | `sources/fulltext/physiognomy/bingjian/fulltext.md`（162 行；与 inventory `fulltext` 一致） |
| 源 SHA256 | `fe3ffd01e9247917fc5b3de9bdf7b86fdef18d59ce0c5d0eb69f649627de7f01` |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / inventory 无 diff |

对照路径：Issue 写 `sources/fulltext/physiognomy/bingjian/fulltext.md`，先确认后与 inventory 一致。catalog `references/books/physiognomy/bingjian/index.md`：`slug=bingjian`；`source_layer=side_evidence`；`source_status=partial`；源链 Wikisource；version_notes 已提示曾国藩托名争议，本 pack 用民国简沙侣抄简熙尧校本（题署清·罗祖真人）。生产侧注解最后触及提交为 `9118a78`（MING-324 记录），本岗未参与该书生产。

无越权文件。注解未改。源文未改。未写产品仓。未碰 464/集成线或其他审查稿独占文件。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/physiognomy/bingjian.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 26, "source_reviewed": 26,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发（无 `verified: true`；键亦未写入）。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–25，26 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 26/26 |
| `review=draft` | 0 |
| `verified` | **0/26 为 true**；26/26 无 `verified` 键（缺省=未升；非显式 `false`，但不违反校验器，且未升 verified） |
| 空白白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 空 `terms` / 空 `notes` | 0（每条 terms≥2、notes≥2） |
| `relatedParagraphIds` | 全无 |
| `subsections` | 0 |

kind 分布（注解）：评注或元数据 1、序跋目录 2、理论 21、操作步骤 1、术语 1。inventory kind 与注解 kind **26/26 一致**。

Issue 钉死起 `bingjian:L0003-L0011`、止 `bingjian:L0162-L0162`：与文件索引 0、25 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/physiognomy/bingjian.json` 26 段；注解 26 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory `id` 列表相同。

| 位置 | 实测 ID | kind | 说明 |
|---|---|---|---|
| 索引 0（起） | `bingjian:L0003-L0011` | 评注或元数据 | Wikisource header 模板（罗祖真人 / 清） |
| 索引 1 | `bingjian:L0015-L0027` | 序跋目录 | 民国沙侣抄本序 |
| 索引 2 | `bingjian:L0031-L0031` | 理论 | 神骨章总纲 |
| 索引 3 | `bingjian:L0033-L0033` | 理论 | 清浊 / 邪正 / 动静 |
| 索引 4 | `bingjian:L0035-L0035` | 操作步骤 | 断续、脱略、针线 |
| 索引 5 | `bingjian:L0037-L0037` | 理论 | 骨九起 / 五主 |
| 索引 6 | `bingjian:L0039-L0039` | 理论 | 骨色骨质与断语 |
| 索引 7 | `bingjian:L0043-L0054` | 理论 | 刚柔外五行顺逆合 |
| 索引 8 | `bingjian:L0056-L0056` | 理论 | 内刚柔 |
| 索引 9 | `bingjian:L0060-L0060` | 理论 | 容貌总论 |
| 索引 10 | `bingjian:L0062-L0062` | 理论 | 「整」与形体配合 |
| 索引 11 | `bingjian:L0064-L0072` | 理论 | 科名星 / 阴骘纹 |
| 索引 12 | `bingjian:L0074-L0074` | 理论 | 目鼻口耳贵贱征 |
| 索引 13 | `bingjian:L0078-L0078` | 理论 | 情态章总论 |
| 索引 14 | `bingjian:L0080-L0080` | 理论 | 四恒态 |
| 索引 15 | `bingjian:L0082-L0082` | 理论 | 时态 +「不必定人终身」 |
| 索引 16 | `bingjian:L0086-L0103` | 理论 | 须眉：眉 |
| 索引 17 | `bingjian:L0105-L0116` | 理论 | 须 |
| 索引 18 | `bingjian:L0120-L0120` | 理论 | 声音章总论 |
| 索引 19 | `bingjian:L0122-L0135` | 术语 | 声 / 音区分与分型 |
| 索引 20 | `bingjian:L0137-L0137` | 理论 | 音为声之余 |
| 索引 21 | `bingjian:L0141-L0141` | 理论 | 命 / 运与气色尺度 |
| 索引 22 | `bingjian:L0143-L0143` | 理论 | 终身年月一日气色 |
| 索引 23 | `bingjian:L0145-L0145` | 理论 | 科名气色例 |
| 索引 24 | `bingjian:L0147-L0158` | 理论 | 青白忌色与例外 / 四恶象 |
| 索引 25（止） | `bingjian:L0162-L0162` | 序跋目录 | 吴荣光跋 |

未入段行主要为书题 `# 冰鉴`、七章标题与跋题（L1/13/29/41/58/76/84/118/139/160）及空行，与 26 稳定段口径一致。本包后该书 SR 审查 remaining **0**。这只表示 26 主段都已有 source-reviewed 注解并经本岗全核，不是 162 行逐句影印校勘，也不是 verified。

## 5. 全量语义核（26/26，对照原文）

原文取 `sources/fulltext/physiognomy/bingjian/fulltext.md`。元数据 / 序跋全文核读；七章各段按 vernacular 要点与 terms 锚回所标行，核对断语、条件、例外与「不作预测 / 不升 verified」边界。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0011` | 元数据 / SR | header 模板 title=冰鑑、author=羅祖真人、times=清；白话标明非正文，并与跋「不著撰人」分层 | 通过 |
| 1 | `L0015-L0027` | 序跋 / SR | 沙侣—朱启明抄本离合；吴荷屋鉴识为其所述；辛巳/癸未/二澳保留待核；不作他人命运案例 | 通过 |
| 2 | `L0031-L0031` | 理论 / SR | 脱谷/山石比神骨；精神在目、骨相在面；文人先观神骨为总纲。白话以「眼睛」对应「两目」，层次正确 | 通过 |
| 3 | `L0033-L0033` | 理论 / SR | 清浊易、邪正难；动静合看；含珠水发 vs 萤光流水/半睡鹿骇；敗器/隱流与「託跡二清」对应 notes 保留疑点，不擅配对 | 通过 |
| 4 | `L0035-L0035` | 操作 / SR | 抖擞易见、断续难见；小心看脱略、大胆看针线；向内 vs 情态。断续句义 notes 保留 | 通过 |
| 5 | `L0037-L0037` | 理论 / SR | 九起具名；头三面二为主；一至四数量判语分层，不凑成九分人格模型 | 通过 |
| 6 | `L0039-L0039` | 理论 / SR | 青紫白次序；联/匾/碎；鼻骨犯眉、颧与眼争等断语保留为历史话语，不改写亲属寿命/生育出口 | 通过 |
| 7 | `L0043-L0054` | 理论 / SR | 先天种子；顺合/逆合；金火水土木方向对举（金带火≠火带金等）；三十死/孤寒/刀剑为相术断语；不接八字喜忌 | 通过 |
| 8 | `L0056-L0056` | 理论 / SR | 内刚柔喜怒伏跳深浅；粗蠢奸 + 豁达周密变体；「十得八九」为作者自许非实验准确率 | 通过 |
| 9 | `L0060-L0060` | 理论 / SR | 七尺/两仪；五方四气；相顾相称。七尺不作现代身高标准 | 通过 |
| 10 | `L0062-L0062` | 理论 / SR | 「整」非机械整齐；豕茅熊鹊修辞；五短两大；罗纹秀骨配神骨。不羞辱现实体型 | 通过 |
| 11 | `L0064-L0072` | 理论 / SR | 清古奇秀让位于科名星/阴骘纹；13–39 / 19–46 岁范围；印堂眉尾/眼角喉间；早迟发。不作考试结果检验 | 通过 |
| 12 | `L0074-L0074` | 理论 / SR | 目渊鼻山；贵征/贱征职官钱谷；鹰准「食人」不作犯罪倾向；「文人不伤在眼」待核 | 通过 |
| 13 | `L0078-L0078` | 理论 / SR | 容貌佐骨、情态佐神；久注 vs 乍见；大家/小儿语境。白话「补充」对应「之余」，正确 | 通过 |
| 14 | `L0080-L0080` | 理论 / SR | 弱狂疏懒周旋四态 + 不媚/不譁/真诚/健举条件；非单标签好坏 | 通过 |
| 15 | `L0082-L0082` | 理论 / SR | 时态三组负面例；明文「三者不必定人终身」与判语同保留 | 通过 |
| 16 | `L0086-L0103` | 理论 / SR | 眉早须晚；紫面无眉/暴腮缺须例外；郭令公/霍剽姚例名保留不擅订；彩/疏爽/倒竖/剑帚 | 通过 |
| 17 | `L0105-L0116` | 理论 / SR | 须眉相称；多寡宜忌；螺纹解索张戟银条；辅须/短髭等负面断语不作现实仕途结论 | 通过 |
| 18 | `L0120-L0120` | 理论 / SR | 清浊气；丹田→唇；五音；自成一家；闻声不必见面。「决雌雄」不改现代性别判定 | 通过 |
| 19 | `L0122-L0135` | 术语 / SR | 声主张发处、音主敛歇处；喜怒哀乐四喻；钟锣雉蛙；远近起止；市井之夫分层 | 通过 |
| 20 | `L0137-L0137` | 理论 / SR | 音为声之余；有声无音/有音无声；禽兽喻；开谈余响。贫贱/尖巧不作声学事实 | 通过 |
| 21 | `L0141-L0141` | 理论 / SR | 面命气色运；珠玉瓦砾/缯帛布葛；一生 vs 三月。不并入八字运限定义 | 通过 |
| 22 | `L0143-L0143` | 理论 / SR | 精神/气色；少淡长明壮艳老素；四季色；朔望；早昼晚暮。不作肤色等级 | 通过 |
| 23 | `L0145-L0145` | 理论 / SR | 黄色正色；黄云盖顶等部位—断语表；学堂为相部名，不并八字同名词 | 通过 |
| 24 | `L0147-L0158` | 理论 / SR | 忌青白 + 青紫/白光例外；土庚相当待核；太白夹日月等四恶象。非「凡青白都凶」 | 通过 |
| 25 | `L0162-L0162` | 序跋 / SR | 吴荣光：七篇不著撰人、无刻本、孔孟观人；与 header 罗祖题署并存不单选定作者 | 通过 |

锚定抽核（非转引进度表）：

- header 羅祖真人 / 清：L6–7
- 沙侣序「吳荷屋」「澳門」「癸未孟秋」：L17、L20、L27
- 神骨「兩目」「面部」「開門見山」：L31
- 「澄清到底」「敗器」「隱流」「託跡二清」：L33
- 「脫略」「針線」：L35
- 九起 / 五者備：L37
- 「鼻骨犯眉」「顴與眼爭」：L39
- 逆合「金形帶火」「火形帶金則三十死」：L51–52
- 「十得八九」：L56
- 科名星 13–39、陰騭紋 19–46：L65–66
- 「三者不必定人終身」：L82
- 「霍剽姚」：L91
- 「聲主張」「音主斂」：L123–124
- 「土庚相當」「太白夾日月」：L155、L157
- 跋「不著撰人姓名」「七篇」：L162；电子末行 L162

抽核未发现空模板白话、静默改正文（如改霍剽姚题称、删「不必定人终身」、把顺逆合方向抹平）、把断语升实证预测、把相法五行并入八字喜忌、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本为 Wikisource / 民国沙侣抄简熙尧校本平铺，header 题署罗祖真人，跋称七篇不著撰人；catalog 另记曾国藩托名争议。26 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/例外/疑字去向，不是影印逐字校勘，也不是相法断语有效证据，也不等于神骨刚柔等已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是冰鉴产品交付，更不冒充已接入八术页面。`source_layer=side_evidence` 边界保持。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺省（非显式 false） | 26/26 无键；0 true | 保持。不升 true；不为本审查回写 JSON |
| header 罗祖真人 vs 跋不著撰人 vs 曾国藩托名俗传 | 三层并存 | 不单选定作者；不补俗传名入正文 |
| 「均之。託跡二清」与敗器/隱流配对 | notes 已标断句/对应待校 | 保留；不擅改配对 |
| 「断者出处断，续者闭处续」 | notes 已标语义不明 | 原字保留；不补测量时长/分值 |
| 「霍剽姚」题称 | notes 已标 | 不擅订为正史称谓 |
| 「文人不伤在眼」 | notes 待核 | 不补成眼部健康结论 |
| 「土庚相当」 | notes 待核 | 不改成推测五行组合 |
| 顺逆合方向对举 | 原文明文 | 不得抹平为「金火同现即同格」 |
| 「不必定人终身」 | L82 明文 | 不得截取时态例单独贴标签 |
| 忌青白 + 例外 | L147–156 | 不得写成「凡青白都凶」 |
| 相法五行形 ≠ 八字干支 | 刚柔章 | 不接喜忌/寿命规则；不入 executable |
| catalog `side_evidence` / partial | index.md | 旁证层；不作硬判出口 |
| 章题未入段 | L29 等 10 处标题行 | 与 26 段口径一致；不另造段落 |

## 8. 交包边界

- 写出：仅 `docs/book-reviews/bingjian-independent-review.md`
- 未改：`references/annotations/physiognomy/bingjian.json` 及任何源文 / inventory / catalog
- 远端：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-480`
- 本包后该书主本 SR 独立审查 remaining **0**
- 下一步：协调核对本报告与 SHA；不派重写；不因本包升 verified；不接八术页面
