# 珞琭子三命消息賦註 · 识典 SK1605：独立审查（16 条全量）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-484` / 分支 `codex/multica-ming-484`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖既有 `luoluzi-sanming-sk1605-review.md`、未改主本 `luoluzi-sanming.json`、未抢玉照主本 / SK1602 注解文件、未改他书 / 引擎 / 产品仓。本岗未参与识典 SK1605 生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审识典 SK1605（16 条），不要与主本或其他书混成一段结论。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；15/16 `source-reviewed`、1 draft；`verified=true` 为 0，16 条均显式 `"verified": false`；`paragraphs.json` 与注解 `paragraphId` 一一对应且同序；15 条 SR 对照电子原文语义成立，1 条 draft 保持 draft（源即无可转存文字）。「仁而不仁」保留电子源「巳」，未误改「己」。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified、不把 draft 升 SR。本岗未改注解。该书识典 SK1605 SR 审查 remaining **0**；draft remaining **1**（索引 5）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-484`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json
shasum -a 256 sources/normalized/shidianguji/SK1605/text.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json --json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `3db6dca03a55761a2cdbe970756e28943eeea8aa6a675ecc273d40397219fcfa`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `2c028a7c17ebd9e894894206309fd37deca70e8b` |
| 源 `text.md` SHA256 | `a5b639ad155b4de2b12ac23a8e37028c46d07923bc5a16a4f406eed8855b97c8` |
| 源行数 / 字符 | 857 行 / 25587 字 |
| `provenance.json` `sourceStatus` | `reference-text` |
| 工作树相对 HEAD | 仅新增本审查文件与同 Issue 另一书审查稿；注解 JSON / 源文 / 既有 sk1605 review 无 diff |

无越权文件。注解未改。源文未改。未写产品仓。

对照路径确认：`sources/normalized/shidianguji/SK1605/text.md` 与 `paragraphs.json` 存在，与 provenance 一致。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/luoluzi-sanming--shidian-SK1605.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 16, "source_reviewed": 15,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

16 条：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 15/16 |
| `review=draft` | **1**（索引 5） |
| `verified=true` | 0（文件内 `"verified": true` 出现次数 = 0） |
| `verified=false` | **16/16 显式 false** |
| 空白话 / 「本段论述 / 白话从略 / 见原文 / TODO」 | 0 |
| 空 `terms` | 0 |
| 四长段 subsections | 5 / 4 / 5 / 5，ID 连续；非空行覆盖全段无缺口；子节 vernacular 无空 |

draft 一条：

- `luoluzi-sanming:shidian-SK1605:P7640185840559439882`（索引 5，源 L90）

源即占位「无可转存文字」，白话声明不能补字或升规则；保持 draft、`verified=false`。索引 15 的 `figureCount=1` 仅段末图像占位，该条因 L677–855 有赋注而保持 `source-reviewed`，图像本身未转写、未升为可引用条文。

## 4. 索引边界与主本隔离

`sources/normalized/shidianguji/SK1605/paragraphs.json` 16 段；注解 16 条。`paragraphId` 全部命中，`missing=0`，顺序与 inventory 一致。起 `luoluzi-sanming:shidian-SK1605:P7640185840559357962`、止 `…P7640185856267976750`，与 Issue 钉死一致。

主本隔离：主本 `luoluzi-sanming.json` ID 与本识典 `P…` ID **交集为空**。本包不审主本。与同 Issue SK1602 识典 ID 亦无交集。

inventory `kind=待分类`；注解用序跋/评注/规则候选/待核实，与生产侧一致；本岗不回改。

## 5. 16 段全部对照原文（不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1605/text.md` 的 `start_line–end_line`。未发现模板空话；无把整段原文粘进 vernacular 冒充处理。

| # | 尾 ID | 源行 | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|---|
| 0 | `P…9357962` | 9 | 序跋 / sr | 「欽定四庫全書」馆题，非断法 | 通过 |
| 1 | `P…9374346` | 11 | 序跋 / sr | 网站章节名「提要」，细则在下段 | 通过 |
| 2 | `P…9390730` | 13–76 | 评注 / sr | 馆臣提要：否定周子晋/陶弘景、八字晚出、大典辑二卷；《三命通会》异文伪中之伪。原文「陶宏景」「已瘧編」「三命通㑹」不改正文。分层：提要≠赋≠注 | 通过 |
| 3 | `P…9407114` | 78–84 | 序跋 / sr | 总纂官纪昀、陆锡熊、孙士毅 | 通过 |
| 4 | `P…9423498` | 86–88 | 序跋 / sr | 总校官陆费墀 | 通过 |
| 5 | `P…9439882` | 90 | 待核实 / draft | 源即占位「无可转存文字」，未补字、未升 sr/verified | 通过 |
| 6 | `P…0111626` | 94 | 序跋 / sr | 卷上前重复馆题 | 通过 |
| 7 | `P…0128010` | 96 | 序跋 / sr | 卷上题名；网站章节≠印本卷次已校 | 通过 |
| 8 | `P…0144394` | 98 | 序跋 / sr | 「宋徐子平撰」题署≠作者已考定，回指提要 | 通过 |
| 9 | `P…0160778` | 100–321 | 规则 / sr | subsections×5。时干旺相/死囚晚成；甲六月下旬有官、上旬中气无官，年月时申巳酉丑运行西方为例外；将星扶德而本主休囚只虚名；根元无官印则运临不发；当生元有七杀运再逢则重；段末「使甲被」未完 | 通过 |
| 10 | `P…0177162` | 323–443 | 规则 / sr | subsections×4。紧用不可受害；不损外尊才逢灾自愈；闻喜不喜金囚休虽见不成庆；十月十一月火无气不能制金；建禄不富≠生月带禄；夹禄忌太岁填实；五阳见五阴劫财克妻、五阴见五阳败财不克妻 | 通过 |
| 11 | `P…7911214` | 447 | 序跋 / sr | 卷下前馆题 | 通过 |
| 12 | `P…7927598` | 449 | 序跋 / sr | 卷下题名 | 通过 |
| 13 | `P…7943982` | 451 | 序跋 / sr | 卷下题署，同卷上分层 | 通过 |
| 14 | `P…7960366` | 453–675 | 规则 / sr | subsections×5。生月带禄=甲乙秋、丙丁冬、戊己春、庚辛夏、壬癸四季；八月火死木绝故有火不损官、有木不劫财；伏吟吉凶两存；天衝内地动、地击外冲不动；丑未/辰戌对运不得作反吟；段末父病妻灾例跨下段 | 通过 |
| 15 | `P…7976750` | 677–856 | 规则 / sr | subsections×5。三宫元吉则凶运祸迟、始末皆凶则吉运灾速；干推两重注云「此论未详」不按已解；仁而不仁保留电子源「巳」；身克杀轻（不贵）/杀克身重（官来克我为贵）；末行图像占位未补字 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 时干旺相 / 死囚晚成：L109
- 甲六月下旬有官、上旬或中气无官；申巳酉丑再行西方却有官：L129
- 将星扶德、本主休囚只虚名：L171
- 根元无则运临官印不发：L272–273
- 「使甲被」跨段至「尅」：L321 / L323
- 闻喜不喜；十月十一月火无气：L334–338
- 建禄不富 vs 生月带禄：L455 / L453
- 五阳五阴劫财（原文「刼財」）：L440
- 天衝地击（原文「天衝地擊」）：L484、L493
- 丑未/辰戌不得谓之反吟：L527–538 一带
- 三宫元吉：L679
- 干推两重「此论未详」：L698
- 仁而不仁电子源「甲見巳」：L712–718（注解无「甲见己」「乙见己」）
- 身克杀轻 / 杀克身重：L769–773
- 无可转存：L90

## 6. Caveat（不构成本包失败）

1. 源层 `reference-text`，电子阅读不是影印校勘。
2. 网站章节名不等于印本卷号；注解已标明。
3. 1 条 draft 因版面无字保持 draft，不升 SR / verified。
4. 索引 15 段末图像未转写；不补字、不升为可引用条文。
5. 「仁而不仁」赋题「戊巳」与注例「巳」并存：巳/己字形争议保留，不改正文；本岗确认注解已用电子源「巳」。
6. 干推两重「此论未详」保持未知，不硬解。
7. `source-reviewed` ≠ 人工 `verified`；本岗不回改、不提升。
8. 既有生产侧 `luoluzi-sanming-sk1605-review.md` 不覆盖、不回改；本文件为 MING-484 独立审查稿。

## 7. Remaining

| 项 | 值 |
|---|---|
| 本包范围 | 识典 SK1605 全 16 条 |
| SR 审查 remaining | **0** |
| draft remaining | **1**（L90 版面占位；保持 draft） |
| verified | 仍全 false |
| 下一步 | 协调收件；draft 不另派升格，除非源层补出可转存文字 |

失败清单：无。
