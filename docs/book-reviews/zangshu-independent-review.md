# 葬书：独立审查主本 source-reviewed 全量（文件索引 0–16）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-448` / 分支 `codex/multica-ming-448`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/zangshu.md`、未抢 MING-439/442/443/444/445 文件、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–16（17 条，全量）。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；17/17 `source-reviewed`、0 draft；无一 `verified=true`；inventory 与注解 `paragraphId` 一一对应且同序；全书 17 段均对照原文语义成立。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-448`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/zangshu.json
git rev-parse HEAD:references/annotations/fengshui/zangshu.json
shasum -a 256 sources/fulltext/fengshui/zangshu/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `54f293ce1b4195667bac93c7525f6b189a2590df107d4a6ff25434fc204c4d04`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `b1236488f4062d7847b98186d1cf9fe307d4717c` |
| 源 `fulltext.md` SHA256 | `e637e2c91888cd398b9d4dd31c341ba7557c7bab970ee17b481afd0ac1089a3c` |
| 源行数 | 190 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `zangshu.md` 无 diff |

无越权文件。注解未改。源文未改。未写产品仓。生产侧 `zangshu.json` / `zangshu.md` 最后触及提交为 `9118a78`（MING-324 记录），本岗未参与该书生产。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/zangshu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 17, "source_reviewed": 17,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。校验器对 `verified is True` 报错；缺省键不会被它写成 `false`。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–16，17 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 17/17 |
| `review=draft` | 0 |
| `verified=true` | 0 |
| `verified` 键 | **17/17 均缺省**（文件内 `verified` 出现次数 = 0；不是布尔 `false`，也不是 `true`） |
| 空白话 | 0 |
| 白话全文重复组 | 0 |
| `notes=[]` | 0 |
| 空 `terms` | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `sourceAttribution` | 0 |
| `subsections` | 0 |
| `relatedParagraphIds` | 2 条互指：`zangshu:L0127-L0136` ↔ `zangshu:L0169-L0190` |

kind 分布：序跋目录 6、理论 6、规则候选 2、操作步骤 2、评注或元数据 1。与 inventory `kind` 逐条一致。

**verified 说明（不失败）：** Issue 表述「verified 全 false」。独立读 JSON：天玉经等同树对照文件显式写 `"verified": false`，葬书 17 条则完全没有该键。`entry.get("verified") is None`，没有任何 `paragraphId` 被标成人工核验。本岗不回改注解去补布尔 `false`。判定为「保持未 verified」，与「source-reviewed ≠ 人工 verified」一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/zangshu.json` 17 段；注解 17 条。`paragraphId` 全部命中，`missing=0`，顺序与 inventory 一致。起 `zangshu:L0003-L0003`、止 `zangshu:L0169-L0190`，与 Issue 钉死一致。

| 索引 | 实测 ID | heading | 说明 |
|---|---|---|---|
| 0 | `zangshu:L0003-L0003` | 葬書 | 收书题名，非正文 |
| 1 | `zangshu:L0007-L0025` | 敘 | 来止去与形势理气框架 |
| 2 | `zangshu:L0027-L0027` | 敘 | 孟南署记 |
| 3 | `zangshu:L0031-L0031` | 葬書目錄 | 内篇目录与字数 |
| 4 | `zangshu:L0033-L0033` | 葬書目錄 | 外篇目录与字数 |
| 5 | `zangshu:L0035-L0035` | 葬書目錄 | 杂篇目录；总分冲突 |
| 6 | `zangshu:L0037-L0044` | 葬書目錄 | 相传郭璞、蔡删吴定 |
| 7 | `zangshu:L0048-L0048` | 內篇一 | 乘生气 |
| 8 | `zangshu:L0052-L0066` | 內篇二 | 藏风得水 |
| 9 | `zangshu:L0070-L0074` | 内篇三 | 势来形止 |
| 10 | `zangshu:L0078-L0102` | 内篇四 | 支法与童断石过独 |
| 11 | `zangshu:L0106-L0112` | 外篇一 | 支陇之辨 |
| 12 | `zangshu:L0116-L0116` | 外篇二 | 龙首龙腹 |
| 13 | `zangshu:L0120-L0123` | 外篇三 | 外护与土质 |
| 14 | `zangshu:L0127-L0136` | 外篇四 | 相对四兽与水形 |
| 15 | `zangshu:L0140-L0165` | 雜篇上 | 势形方与取象 |
| 16 | `zangshu:L0169-L0190` | 雜篇下 | 四势八方、三吉六凶 |

源文 `# 葬書`（L0001）与各 `##` 标题行不在 17 段库存内，符合现有切段。电子无空格字数与目录所标字数不一致（内篇四电子 372 vs 目录「三百八字」；内篇合计电子 856 vs 目录 703），注解已说明不能用含标点的现代计字判定缺文。独立复核目录算术：

- 内篇分项 89+174+132+308 = 703，与「七百三字」一致；故「三百八字」在本目录口径是 308，不是 380。
- 外篇分项 167+74+123+177 = 541，与「五百四十一字」一致。
- 杂篇分项 281+196 = 477，与同行总数「五百七十七字」差 100。
- 内外目录合计 703+541 = 1244，与版本说明「一千二百四十六字」差 2。

这些冲突已写入对应 notes，未改源文。本包后该书 SR 审查 remaining **0**。既有 `docs/book-reviews/zangshu.md`（生产侧账本）不覆盖、不回改。

## 5. 全核语义（17/17，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/zangshu/fulltext.md` 的行范围。全书仅 17 段，按 Issue 要求全核（覆盖评注 / 序跋 / 理论 / 规则候选 / 操作步骤）：

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0003` | 评注或元数据 / SR | 原文「地理眞詮一集·葬書」；白话作收书信息，不抽地形规则 | 通过 |
| 1 | `L0007-L0025` | 序跋目录 / SR | 「來者…入首」「止者，穴也」「去者，向放水」；正零=得时/失时，非正负号；星运分金未给完整算法 | 通过 |
| 2 | `L0027-L0027` | 序跋目录 / SR | 蒋、章汇录；葬书与天元五歌「只載正文」；「孟南氏識」。国初年代不填刊年 | 通过 |
| 3 | `L0031-L0031` | 序跋目录 / SR | 内篇四篇节数与 89/174/132/308、合计 703 与原文一致；导航而非算法 | 通过 |
| 4 | `L0033-L0033` | 序跋目录 / SR | 外篇四篇 167/74/123/177、合计 541；后文外篇一至四标题均在 | 通过 |
| 5 | `L0035-L0035` | 序跋目录 / SR | 上 281、下 196 相加 477 ≠ 577；保留原文、记冲突，不断言缺一百字 | 通过 |
| 6 | `L0037-L0044` | 序跋目录 / SR | 「相傳」郭璞；俗本二十、蔡季通存八；吴澂识 / 「公徵刪定」待校；1246 vs 目录 1244 | 通过 |
| 7 | `L0048-L0048` | 理论 / SR | 「葬者，乘生氣也」「本骸得氣，遺體受廕」；遗体作子孙观念；铜山灵钟为感应论，非用户事实 | 通过 |
| 8 | `L0052-L0066` | 理论 / SR | 「得水爲上，藏風次之」；「涸燥者宜淺…坦夷者宜深」；土为气体、气为水母，不换成现代物理 | 通过 |
| 9 | `L0070-L0074` | 理论 / SR | 「千尺爲勢，百尺爲形，勢來形止，是謂全氣」；富贵语不转财产预测；不抽「形止」孤立规则 | 通过 |
| 10 | `L0078-L0102` | 规则候选 / SR | 经曰「童斷石過獨」五项可识别；「氣以生和而童，山」句读不改正文；「十一不具」不补十一条 | 通过 |
| 11 | `L0106-L0112` | 操作步骤 / SR | 「大則特小，小則特大」；「支葬其巓，壠葬其麓」；「主客同情，所不葬也」否定保留 | 通过 |
| 12 | `L0116-L0116` | 理论 / SR | 万马来势、负扆、龙首鼻额角目耳唇、龙腹脐与胸胁；身体比喻，非真人器官 | 通过 |
| 13 | `L0120-L0123` | 规则候选 / SR | 外无以聚 / 左空右缺为散；「土欲細而堅，潤而不澤」；「疉㬪」「穴粟」待校不改字 | 通过 |
| 14 | `L0127-L0136` | 理论 / SR | 相对左右前后四兽；水忌湍激、「瀦而後洩」；「來無源…去無流」不生成无源条件；与杂篇下四势互参但不合并 | 通过 |
| 15 | `L0140-L0165` | 理论 / SR | 势难、形次、方又次；势形顺逆合看；现有句读下不生成「形状→祸福」配对表 | 通过 |
| 16 | `L0169-L0190` | 操作步骤 / SR | 寅申巳亥四势、八卦八方；土圭玉尺无现代单位；「閭厚」待校；三吉六凶；「穴吉葬凶，與棄尸同」 | 通过 |

抽核未发现空模板白话、把序言理气步骤冒充郭璞正文算法、删掉「所不葬也」的「不」、把四兽与寅申巳亥四势并成同一枚举、或把任何条的 `verified` 置 true。

分类可争但不失败：外篇一、杂篇下标「操作步骤」，其中也含筛选条件与吉凶条目，标「规则候选」同样说得通；与 inventory 一致，本岗不回改。

## 6. 明确非结论

- 本包 **不** 证明影印已校或传统断语经验证。
- 本包 **不** 把任何条升为人工 `verified`，也不补写缺省的 `verified: false`。
- 本包 **不** 表示风水材料已接入 FateRadar 八术页面。
- 本包 **不** 覆盖或取代已有 `docs/book-reviews/zangshu.md`。
- 目录字数冲突、署记用字、童山句读、十一不具、杂篇上取象配对、「来无源去无流」义项，均保持待校；不据电子文本改字或补条件。

## 7. 交付

| 项 | 值 |
|---|---|
| Issue | MING-448 |
| 工作树 | `fateradar-multica-ming-448` |
| 分支 | `codex/multica-ming-448` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/zangshu-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后可将本 Issue `done`；无需重做 0–16；无需回改注解。
