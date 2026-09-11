# 御纂周易折中 · 识典 HY2301：独立审查 CP2（300–680）

审查对象：`origin/codex/multica-ming-184` @ `a0532d6f3a1b7567f9bb00dc4889051df39eb3ee`（父 CP1 `origin/codex/multica-ming-176` @ `4a6b4d9cad94aa6730fe7592db08bf89eee7215f`）。工作树只读参考 `fateradar-multica-ming-184`，本岗写出仅本文件。未改注解 JSON、未改源文、未改主本 `zhouyi-zhezhong.json`、HY1521 / SK1609 / SDZJ0170、引擎 / `chart.*`。不是御纂周易折中全书完成，也不是主本折中包，也不是引擎包，也不是全项目完成。source-reviewed ≠ 人工 verified。禁止重做主本 0–899。禁止重做识典补本 0–680。

结论：**通过。** 交包结构账本与 ≥15 段非模板抽样语义成立；索引 468 / 490 本义「當闕」「極字未詳」保留 unknown，未补造。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。`remaining=0` 只指识典 HY2301 补本 681 段已 source-reviewed，不是人工 verified，也不是主本全书。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-187`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-184
git rev-parse HEAD HEAD^
git diff --name-only 4a6b4d9cad94aa6730fe7592db08bf89eee7215f..HEAD
git diff --stat 4a6b4d9cad94aa6730fe7592db08bf89eee7215f..HEAD
shasum -a 256 sources/normalized/shidianguji/HY2301/paragraphs.json
shasum -a 256 sources/normalized/shidianguji/HY2301/text.md
git rev-parse 4a6b4d9:sources/normalized/shidianguji/HY2301/paragraphs.json
git rev-parse HEAD:sources/normalized/shidianguji/HY2301/paragraphs.json
git rev-parse 4a6b4d9:sources/normalized/shidianguji/HY2301/text.md
git rev-parse HEAD:sources/normalized/shidianguji/HY2301/text.md
git cat-file -e 4a6b4d9:references/annotations/divination/zhouyi-zhezhong.json
git cat-file -e HEAD:references/annotations/divination/zhouyi-zhezhong.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-184` | `a0532d6f3a1b7567f9bb00dc4889051df39eb3ee`（本岗检出基线与 `ls-remote` 一致） |
| 父提交 | `4a6b4d9cad94aa6730fe7592db08bf89eee7215f` |
| 相对父提交文件 | 仅 2 个：`references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json`、`docs/book-reviews/zhouyi-zhezhong-hy2301-progress-2026-09-11.md` |
| diffstat | `+6602 / -27` |
| 源 `paragraphs.json` SHA256 | `511d3e2a9a022444133ab985197a51f879d6d0f50d3e0f423243c9206a63c86c`（681 段，与 Issue / 进度一致） |
| 源 `text.md` SHA256 | `3daa58177a204d86c55bbe4156fc645f408e03a6990a07a7ee45104c1d617fc1` |
| 源 blob 父 vs 本提交 | `paragraphs.json` 同为 `23d84953106b9b0e778eb37c9c6a8ac05cbf12a4`；`text.md` 同为 `a526d7549cd522f7d4c2e0380e505808e4aeee8a`（本提交未改源层） |
| 主本 `zhouyi-zhezhong.json` | 父提交与本提交均不存在该路径。相对父提交未新增、未改写 |
| 0–299 条目 | 与父提交 JSON 全等，`changed=0`；未回头改 CP1 |
| 顶层 `scopeNote` | 仅追加「本文件覆盖识典补本索引 0–680（CP1+CP2）…」一句；0–299 条目未动 |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 107 条，未补造） |
| `paragraphCount` / `figureCount` | 681 / 38；本包 38 条图像占位与 `figureCount>0` 段落集合一一对应 |
| 注解 ID 与 `paragraphs.json` | 681/681 一一对应，`mismatch=0`；无主本 `zhouyi-zhezhong:L####` 混写 |

无越权文件。源层未改。主本折中 / 他书 / 引擎 / `chart.*` 未覆盖。`scopeNote` 已写明补本不替代主本、不作独立投票、网站章节名不直接等同印本卷号。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-184 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 681, "source_reviewed": 681,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

681 条：`review=source-reviewed` 全 681；`verified` 全 `false`；无 `draft` 字段。无升 verified。

kind 全书：规则候选 477、理论 166、序跋目录 38。CP2（300–680）规则候选 201、理论 151、序跋目录 29。与进度一致。

空白话 0、空 notes 0、空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。

CP2 notes 含「保留 unknown」仅 2 条：索引 468 / 490（Issue 指定项）。CP1 既有 23 / 26 / 27 未改。

## 4. 索引边界与 remaining

`paragraphs.json` 全书 681 段；本包注解覆盖 300–680，与 0–299 合计 681。进度 remaining **0**，只指识典 HY2301 补本段落全集已 source-reviewed。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（CP1 起，本包未改） | `zhouyi-zhezhong:shidian-HY2301:P7675240779413241875` |
| 注解索引 299（CP1 止，本包未改） | `zhouyi-zhezhong:shidian-HY2301:P7675240944312877099` |
| 注解/源索引 300（CP2 起） | `zhouyi-zhezhong:shidian-HY2301:P7675240944312893483` |
| 注解/源索引 680（CP2 止 / 补本末） | `zhouyi-zhezhong:shidian-HY2301:P7510771359308382243` |

网站章节覆盖（源 `heading`，不是印本卷号）：象下傳 300–501 / 本圖書第一 502–517 / 啓蒙附論 518–657 / 御纂周易折中卷第二十二 658 / 序卦雜卦明義 659–660 / 序卦 661–680。索引 501「卷第十二」、657「卷第二十一」、658「卷第二十二」白话均标「章节名不等于印本卷号核定；属目录/卷端」，未把网站章名写成印本卷次。起始/止点与 Issue 钉死 ID 一致。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/HY2301/text.md` 的 `start_line–end_line`。象下分层保留本义·程传·集说·案；短象辞不单面取用；图书/启蒙附论作理论不升单爻断；网站卷端不作印本卷号；本义「當闕 / 未詳」不补造。下列为非模板抽核。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `P…893483` | 规则 / sr | 「覆公餗，信如何也。」短象辞 + 不单句取象后缀。L1854 | 通过 |
| 301 | `P…909867` | 规则 / sr | 本义「言失信也」；程传大臣失职则「信如何」；集说杨氏简。覆餗条件句，不单面信 | 通过 |
| 302 | `P…926251` | 规则 / sr | 「鼎黃耳，中以爲實也。」短象辞。L1863 | 通过 |
| 320 | `P…221163` | 规则 / sr | 艮大象「兼山艮。君子以思不出其位」。源跨两行，白话合读 | 通过 |
| 335 | `P…721386` | 规则 / sr | 渐大象本义「疑賢字衍，或善下有脫字」照录；案升与渐（地中生木 / 山上有木）分层。未改字补贤 | 通过结构；见 caveat |
| 349 | `P…226211` | 规则 / sr | 归妹大象本义「合之不正」知其终敝；案「不当以泽从雷，当以泽感雷」。程传后部压缩 | 通过结构；见 caveat |
| 351 | `P…950762` | 规则 / sr | 归妹初本义「恆，謂有常久之德」；案「女而自归非常，惟娣从嫡乃常」。条件句 | 通过 |
| 364 | `P…422867` | 规则 / sr | 丰初本义「戒占者不可求勝」；案「過旬災」经意/传意相备，不单取无咎 | 通过 |
| 400 | `P…922473` | 规则 / sr | 巽五程传「得正中则吉…失中则悔」。中正条件，不可外推 | 通过 |
| 430 | `P…413993` | 规则 / sr | 涣上程传「血字下脫去字」照录电子切分；集说项氏逖≠惕。未补脱字 | 通过 |
| 450 | `P…350911` | 规则 / sr | 中孚鹤鸣程传「誠意所。願也」（源点断如此）。未改字 | 通过 |
| 468 | `P…629439` | 规则 / sr | 本义「爻義未明，此亦當闕」。notes「保留 unknown，不补造」。程传/集说/案仍对源 | 通过 |
| 490 | `P…185491` | 规则 / sr | 本义「極字未詳…今且闕之」。notes「保留 unknown」。程传「程傳、」电子顿号照录，未把极补成敬 | 通过 |
| 501 | `P…365715` | 序跋 / sr | 「御纂周易折中卷第十二」。网站章名 ≠ 印本卷号 | 通过 |
| 502 / 518 | `P…001398` / `P…504683` | 序跋 / sr | 「本圖書第一」「啓蒙附論」。短题目录，不是筮法 | 通过 |
| 521 | `P…434831` | 理论 / sr | 源即「〔此处为图像，未转文字…〕」；figureCount=1。不升爻变规则 | 通过 |
| 658 | `P…688374` | 序跋 / sr | 「御纂周易折中卷第二十二」。网站章名 ≠ 印本卷号 | 通过 |
| 660 | `P…652559` | 理论 / sr | 序卦杂卦明义：文王序/杂、韩孔疑反对、欧公斥序卦为妄、胡氏端绪。说理不升断法 | 通过结构；见 caveat |
| 680 | `P…382243` | 理论 / sr | 补本末：系辞九卦与上下篇相对；「略其终始而取其中间」。止 `P7510771359308382243` | 通过 |

关键条件与源行（抽核，非转引进度表）：

- CP2 起覆公餗：L1854
- 鼎覆餗失信本义/程传：L1856–1861
- 鼎黄耳：L1863
- 艮思不出其位：L1930–1931
- 渐本义贤字衍、案升与渐：L1986–1992
- 归妹合之不正 / 案泽感雷：L2038–2042
- 归妹以娣以恆：L2047–2053
- 丰过旬灾经传相备：L2106–2111
- 巽五正中失中则悔：L2258–2261
- 涣血字下脱 / 项氏逖：L2374–2377
- 中孚中心愿：L2456–2459
- 本义「爻義未明，此亦當闕」：L2525–2526
- 本义「極字未詳…今且闕之」：L2614–2615
- 网站卷第十二：L2660
- 本图书第一 / 启蒙附论题：L2664、L2812
- 图像占位原文：L2824 等同型 38 处
- 网站卷第二十二：L3647
- 序卦杂卦明义：L3653–3662
- 补本末九卦相对：L3771–3777

## 6. source-reviewed ≠ 人工 verified；remaining=0 的范围

识典补本 `sourceStatus=reference-text`。681 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/体例/本义·程传·集说·案/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本，不计独立投票，不等同易学引擎已实现。网站章节「象下傳」「本圖書第一」「啓蒙附論」「卷第二十二」是识典目录名，不是印本卷次核定。

**remaining=0** 只覆盖识典 HY2301 这一补本的 681 段 source-reviewed 账本。不得写成：

- 人工 verified 已完成；
- 主本 `zhouyi-zhezhong.json` 全书完成；
- 御纂周易折中全帙 / 产品交付 / 引擎已实现。

不得把 681 条 source-reviewed 写成已人工 verified。勿再派同书续包；缺章 107 与 figure 38 仍是电子源缺口。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 包级 notes 套语 | CP2 381 条 notes[0] 均为「识典 HY2301 电子语义审读…不是影印校勘或人工 verified」 | 否定升 verified，不是空白话。不回改 |
| 短象辞白话后缀 | 99 条以「象传原文：…须连同本义、程传与集说…不单句取象作断」起式；notes 尾「短象辞不单面取用」99 | 套语后缀，前半对照源文（换行合读）。不是空模板。不回改 |
| 图像占位 | 38 条白话含「〔此处为图像，未转文字〕」，与 `paragraphs.json` `figureCount>0` 集合全等；源文本身即该占位句 | 跟源，不补绘图。不回改 |
| 索引 468 / 490 unknown | 本义當闕 / 極字未詳照录；notes「保留 unknown，不补造」 | Issue 指定项成立。不回改 |
| 索引 335 贤字衍 | 白话照录本义「疑賢字衍」，notes 未另标 unknown | 未补造。标记弱于 468/490。不回改 |
| 索引 349 压缩 | 程传「少女之说…观归妹则当思永终之戒」及集说崔氏/吴氏未入白话，只留案语 | 大段压缩。引用须回源。不回改 |
| 索引 301 集说人名 | 源「楊氏。𥳑曰」；白话「如楊氏」 | 人名压缩。本义/程传对源。不回改 |
| 索引 430 / 450 / 490 电子点断 | 「血字下脫去字」「誠意所。願也」「程傳、」照录 | 电子切分，不改字、不补脱文。不回改 |
| 索引 660 压缩 | 明义末「详推二篇…目曰明义以附焉」白话截于「详…」 | 压缩漏尾。不回改 |
| 短题作序跋 | 如 568「若自上而下，作三層，亦如之。」标序跋目录 | 电子短行。不升筮法。不回改 |
| terms 偏泛 | CP2 `周易折中` 169/381；其余卦名零散 | 结构合法。抽核不以 terms 当规则。不回改 |
| 网站卷端 | 501 卷十二 / 657 卷二十一 / 658 卷二十二均标明非印本卷号 | 与 CP1 卷第九处理一致。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **索引 468 / 490**：本义明确當闕 / 未詳。白话已引用且 notes 标 unknown。引用过卦九四「遇」或未济濡尾「極」时，不得把程传/集说读成本义已补字。本义阙文仍 unknown。
2. **索引 335**：本义「疑賢字衍，或善下有脫字」已入白话，但 notes 未单列 unknown。不得把「居贤德善俗」当已校定经文。
3. **索引 349**：归妹大象程传后半与集说未入白话。引用「永终知敝 / 征凶无攸利」须回源 L2038–2042。
4. **索引 430**：程传「血字下脫去字」是电子切分，不是已补出的脱文校定。项氏逖/惕之辨在集说，白话只点名。
5. **99 条短象辞**：原文句对源，解释在邻段本义/程传。单抽「象传原文」句不能当已分层规则。
6. **38 图**：电子源未转写。图书/启蒙/序卦图位不得当已录入象数规则。
7. **网站卷十二 / 二十一 / 二十二**：识典卷端标记。本包象下续鼎→未济后接图书、启蒙附论、序卦，不得按印本卷次理解范围。
8. **remaining=0**：只关闭识典 HY2301 补本续写。主本折中、人工 verified、缺章 107、figure 38 仍未决。

## 未决（本岗不施工）

- 468 當闕、490 極字未詳、335 贤字衍/脱字、430 血字下脱：保持 unknown / 电子切分，不升 verified。
- 识典待校。681 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同易学引擎已实现。
- 主本 `zhouyi-zhezhong.json` 不在本包范围；识典 0–680 审完不等于御纂周易折中全书完成。
- 勿再派识典 HY2301 同书续包；勿重做 0–680；勿改主本折中。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-187`。
