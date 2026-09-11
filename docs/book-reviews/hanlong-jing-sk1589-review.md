# 撼龍經合刊 · 识典 SK1589：独立审查（0–85 / 86）

审查对象：`origin/codex/multica-ming-204` @ `ffcb187a0b8b9d936a9aa40537b7f72da5cd74e5`（父 `1fd3a37fae846d9b7cdf53824434f2fe47c868ee`）。工作树只读参考 `fateradar-multica-ming-204`，本岗写出仅本文件。未改注解 JSON、未改源文、未改主本 `hanlong-jing.json`、青囊、协纪、SK1619/SK1591、引擎、`chart.*`。不是撼龙经全书他本完成，也不是主本 `hanlong-jing:L####` 包，也不是引擎/排盘接入，也不是全项目完成。

结论：**通过。** 交包结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引口径 remaining 0 ≠ 人工 verified / 主本全书。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-211`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-204
git rev-parse HEAD HEAD^
git diff HEAD^..HEAD --name-only
git diff --stat HEAD^..HEAD
shasum -a 256 sources/normalized/shidianguji/SK1589/paragraphs.json
shasum -a 256 sources/normalized/shidianguji/SK1589/text.md
git rev-parse HEAD^:references/annotations/fengshui/hanlong-jing.json
git rev-parse HEAD:references/annotations/fengshui/hanlong-jing.json
git rev-parse HEAD^:sources/normalized/shidianguji/SK1589/paragraphs.json
git rev-parse HEAD:sources/normalized/shidianguji/SK1589/paragraphs.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-204` | `ffcb187a0b8b9d936a9aa40537b7f72da5cd74e5`（本岗 HEAD 与 `ls-remote` 一致） |
| 父提交 | `1fd3a37fae846d9b7cdf53824434f2fe47c868ee` |
| 相对父提交文件 | 仅 2 个：`references/annotations/fengshui/hanlong-jing--shidian-SK1589.json`、`docs/book-reviews/hanlong-jing-sk1589-progress-2026-09-11.md` |
| diffstat | `+1369`（两文件均为新增） |
| `paragraphs.json` SHA256 | `7b83cd6f40c5c734cdb6fb8a7240d6a5a1253c5610bdbe5815fb5139d7b242b0`（86，与 Issue 一致） |
| `text.md` SHA256 | `a7aa4b66010d8cacfb28764a76bb3ff812d533277e70f97519b419040df02320` |
| 源 blob 父 vs 本提交 | paragraphs / text 均同 blob，本提交未改源层 |
| 主本 `hanlong-jing.json` blob | 同为 `a628c6017a8f1eb108697a6c8e56c18fcfd12102`，未改；仍 6 条 `hanlong-jing:L####` |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 51，未补造） |
| `paragraphCount` / `figureCount` | 86 / 0 |
| 注解 ID 与 `paragraphs.json` 0–85 | 86/86 一一对应，`mismatch=0`；前缀全 `hanlong-jing:shidian-SK1589:`；无主本 `L####` 泄漏 |

无越权文件。源层未改。主本撼龙 / 他书 / 引擎 / `chart.*` 未覆盖。`scopeNote` 已写明补本不替代主本投票、不接入宅形排盘。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-204 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/hanlong-jing--shidian-SK1589.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 86, "source_reviewed": 86,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

86 条：`review=source-reviewed` 全 86；`verified` 全 `false`；无 `draft`。无升 verified。

kind：规则候选 45、操作步骤 17、评注或元数据 8、序跋目录 7、理论 5、术语 3、待核实 1。

空白话 0、空 terms 0；空 notes 14（卷端/题署类元数据，可接受）。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。本包 `figureCount=0`。

待核实仅索引 81 `hanlong-jing:shidian-SK1589:P7639188276951466022`（源 L1851 残句「须傍藉生生之气，借资化」；`relatedParagraphIds` ↔ 82；notes 写 unknown，不补造）。

## 4. 索引边界

`paragraphs.json` 全书 86 段；本包注解覆盖 0–85 全量。进度 nextId 无、remaining 0（索引口径）与源末条一致。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `hanlong-jing:shidian-SK1589:P7351705562645561382` |
| 注解索引 81（残句） | `hanlong-jing:shidian-SK1589:P7639188276951466022` |
| 注解索引 85（止） | `hanlong-jing:shidian-SK1589:P7639188276951531558` |

网站章节覆盖：四库子部七 / 撼龙经 / 疑龙经上·中篇 / 葬法倒杖（认太极、分两仪、倍八卦）。网站章节名 ≠ 印本卷号。起始/止点与 Issue 钉死 ID 一致。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1589/text.md` 的 `start_line–end_line`。条件/救应/反转/末歌与正文分层多数成立；旧象福禄刑杀不作现实验证；不写成已接入宅形排盘。下列为非模板抽核。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `P…561382` | 评注 / sr | 「钦定四库全书」。卷端元数据，不是断法 | 通过 |
| 1 | `P…594150` | 序跋 / sr | 合刊撼龙/疑龙/葬法倒杖、术数类、提要。网站章 ≠ 印本卷 | 通过 |
| 2 | `P…610534` | 序跋 / sr | 提要：杨筠松史传不见、书录解题/宋史救贫、术家广明玉函传说不足信；九星形势；疑龙上中下；葬法倚盖撞黏、倒杖十二+二十四砂；删李国本注。分层成立。白话有压缩/窜入，见 caveat | 通过结构 |
| 3 / 4 | `P…626918` / `P…534835` | 评注 / sr | 总纂纪昀等；总校陆费墀。馆臣署名 | 通过 |
| 8 | `P…950574` | 理论 / sr | 须弥干枝、黄河川江、两水夹、罗城、平洋凹窠/勾夹螺穴、霜降水涸。条件与反转（山反水散）在 | 通过 |
| 9 | `P…966958` | 理论 / sr | 北辰垣局难识 → 垣外九星贪巨禄文廉武破辅弼；取类 ≠ 天文实测 | 通过 |
| 10 | `P…983342` | 规则 / sr | 贪狼笋峰；斜枝破面、乘龙带剑；侧峰直去未必停结 | 通过 |
| 15 | `P…834862` | 规则 / sr | 巨门方体顿笏、穿帐护卫、旌节刀剑 | 通过 |
| 20 | `P…916782` | 规则 / sr | 破碎作怪、欃枪 vs 旌幢；顿鼓似武曲须分有足禄存；人物刑杀旧断不实证 | 通过 |
| 25 | `P…998702` | 规则 / sr | 禄存第六平洋巨浪；护龙同向、随水；忌左右驳杂 | 通过 |
| 30 | `P…080622` | 规则 / sr | 廉贞独火龙楼宝殿、穿心出帐、两池天汉；恶石可为祖 | 通过 |
| 40 | `P…244462` | 规则 / sr | 左辅幞头杖鼓本形 vs 武曲旁辅分层 | 通过 |
| 45 | `P…326382` | 理论 / sr | 骨节相称、忌反弓伸颈；末歌起处，不覆盖前文例外 | 通过 |
| 50 | `P…408302` | 规则 / sr | 文曲末歌散形忌；与间峰救应分层 | 通过 |
| 53 | `P…457454` | 理论 / sr | 三盖总纲、州郡县邑旧象 ≠ 实证；收束撼龙经 | 通过 |
| 60 | `P…230323` | 规则 / sr | 疑龙中篇：背面、缠护、明堂宽狭、罗星水口；长段压缩但核心条件在 | 通过结构 |
| 70 | `P…285798` | 操作 / sr | 平地阳龙正求架折：狭中心、阔迎气、深四角立石、浅中半 | 通过 |
| 75 | `P…367718` | 操作 / sr | 斩法：息横、忌侵顶近足、先审息象 | 通过 |
| 80 | `P…449638` | 操作 / sr | 折法浅窟风杀、砂水均应/龙虎相登。段末已起「挨者…闕」，白话未写入，见 caveat | 通过结构 |
| 81 | `P…466022` | 待核实 / sr | 残句「借资化」；related→82；unknown 不补造 | 通过 |
| 82 | `P…482406` | 操作 / sr | 接「化之机」完足挨法；倚切宽之别、转皮仰掌 | 通过 |
| 83–85 | `P…498790` 等 | 操作 / sr | 并取短、斜切避顶弦、插乘过续之中；85 收束全量 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 四库行 / 合刊类目：L9、L11–13
- 提要杨筠松/九星/疑龙三篇/葬法倒杖/删李注：L15–56
- 须弥干枝、两水夹、平洋：L78–128
- 北辰→九星：L130–140
- 贪狼笋峰破面：L142–148
- 巨门穿帐：L232–246
- 禄存破碎欃枪 / 有足无足：L316–342
- 禄存第六平洋护龙：L391–401
- 廉贞独火出帐天汉：L485–535
- 左辅本形 vs 武旁：L920–934
- 骨节 / 末歌起：L1120–1136
- 文曲末歌：L1180–1186
- 三盖总纲：L1213–1230
- 疑龙中篇背面缠护：L1431–1581
- 正求架折：L1636–1644
- 斩法：L1715–1730
- 折法 + 段末挨者阙：L1827–1849
- 残句借资化：L1851
- 挨法完足：L1853–1858
- 并 / 斜 / 插：L1860–1897

跨段残句：80→81→82（挨者阙 / 借资化 / 化之机）在 81–82 用 `relatedParagraphIds` 标明；81 不补造。80 白话漏写段末起笔，见 caveat，不判失败。

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。86 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/条件/救应/反转/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本 `hanlong-jing.json`（6 条 L 行号），不计独立投票。九星官鬼空亡在本书为形势术语，不套八字六爻或现代天文同名字段。当前产品无宅形/龙砂穴水输入，不得写成已接入风水排盘。remaining 0（索引口径）≠ 人工 verified，≠ 撼龙经全书他本完成。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 索引 2 提要压缩 | 白话「中篇论穴形、下篇论星峰」；源为中篇「寻龙到头、面背朝迎」、下篇「结穴形势+十问」。葬法/倒杖并作「二十四法」，略混倚盖撞黏与十二倒杖+二十四砂 | 压缩偏差。不回改 |
| 索引 2 窜入 | 白话「后至乾宁中以卜葬术行，世称救贫」；本段源止于广明玉函、往来处州，无乾宁句 | 外传说渗入。不回改 |
| 索引 80 跨段 | 源段末已起「挨者，傍也…阙」；白话只写折法；跨段标注在 81–82 | 漏写段末起笔。不回改 |
| 进度区段止点 ID | 进度表 0–4 止写成索引 3 的 ID；5–7 / 54 / 61 起 ID 与实测不符 | 进度笔误；以注解/paragraphs 为准。不回改 |
| 空 notes | 14 条卷端题署类 notes=[] | 结构合法。不回改 |
| scopeNote 提及 SK1619/SK1591/L | 仅作禁止混写说明；entries 无他本 ID | 合法。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **索引 2**：提要白话压缩把疑龙中/下篇题旨写偏，并混葬法与倒杖附法；另窜入本段未见的「乾宁」救贫传闻。后续若引用作者考据或三书结构，须回源 L15–56，不能只看白话。
2. **索引 80**：折法专释成立，但段末「挨者…阙」已开跨段，白话未点明；完整挨法以 81–82 为准。
3. **进度文档 ID**：区段起讫个别 ID 笔误；审查对象是注解 JSON，不是进度缩写。
4. **长段压缩**：疑龙中篇（60）等百余行段，主条件在、不是每条例证入白话。未据此判失败。

## 未决（本岗不施工）

- 索引 81 残句保持 unknown / 待核实；不补造、不升 verified。
- 识典待校。86 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同风水排盘已接入。
- 主本 6 条 `hanlong-jing:L####` 不在本包范围；识典 0–85 审完不等于撼龙经全书完成。
- 本审查不把任何条目标成人工 verified。本岗不改注解。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-211`。
