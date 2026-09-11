# 阳宅三要：独立审查主本 source-reviewed 全量（0–1 / 2）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-478` / 分支 `codex/multica-ming-478`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / 引擎 / `chart.*` / 他书。本岗未参与该书生产。不要抢 MING-464/集成线与本轮其他审查稿。不要与《阳宅十书》混淆。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审注解文件索引 0–1（2 条，全量）。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；2/2 `source-reviewed`、0 draft；2/2 显式 `verified: false`，无一 `verified=true`；inventory 与注解 `paragraphId` 一一对应且同序；全书 2 段均对照原文语义成立（理论主段 135 子节连续覆盖 L7–1476、无空白白话、无全文重复白话）。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-478`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/fengshui/yangzhai-sanyao.json
git rev-parse HEAD:references/annotations/fengshui/yangzhai-sanyao.json
ls sources/fulltext/fengshui/yangzhai-sanyao/fulltext.md
shasum -a 256 sources/fulltext/fengshui/yangzhai-sanyao/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/yangzhai-sanyao.json --json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `b9ab48331b72930accd0be9f00aacc2aac19e6a6db8c092ed41dac3129a1f235`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `19eec40c33459564d7fa8a992547a0935ba71132` |
| 源路径 | `sources/fulltext/fengshui/yangzhai-sanyao/fulltext.md`（存在；inventory `fulltext` 同路径） |
| 源 `fulltext.md` SHA256 | `05e6a32844cfc8a425a45bde3742b73c62fd5a2bc0180cf99b6162208a1b7f33` |
| 源行数 | 1476 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文无 diff |

无越权文件。注解未改。源文未改。未写产品仓。未触 `yangzhai-shishu.json`。生产侧 `yangzhai-sanyao.json` 最后触及提交为 `9118a78`（MING-324 记录），本岗未参与该书生产。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/yangzhai-sanyao.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2, "source_reviewed": 2,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–1，2 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 2/2 |
| `review=draft` | 0 |
| `verified=true` | 0 |
| `verified=false` | **2/2 显式布尔 false**（与 Issue「verified 全 false」一致） |
| 空白白话 | 0（父段与 135 子节均有非空 vern） |
| 白话全文重复组 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes=[]` | 仅索引 0（元数据段）；索引 1 有 3 条 notes，标明补充层分层、版式损失与 verified 边界 |
| 空 `terms` | 0（索引 0：1 词；索引 1：4 词） |
| `sourceAttribution` | 0 |
| `relatedParagraphIds` | 0 |
| `subsections` | 索引 1：135 节；行号连续 L7–1476、无间隙、无重叠、无空白 vern |

kind 分布：评注或元数据 1、理论 1。顶层 `scopeNote` 与 entries 一致（2 主段、L7–1476、135 子节、verified 边界）。未与《阳宅十书》串档（注解内无「十书」/`yangzhai-shishu`）。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/fengshui/yangzhai-sanyao.json` 2 段；注解 2 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。起 `yangzhai-sanyao:L0003-L0005`、止 `yangzhai-sanyao:L0007-L1476`，与 Issue 钉死一致。

| 索引 | 实测 ID | 注解 kind | 说明 |
|---|---|---|---|
| 0 | `yangzhai-sanyao:L0003-L0005` | 评注或元数据 | 网页文字本说明 + 源/影印锚点 |
| 1 | `yangzhai-sanyao:L0007-L1476` | 理论 | 正文四卷至尾；135 子节 |

非空源行未入段：仅 L1 书题 `# 阳宅三要…`（结构标题）。L2 空行。正文与元数据覆盖 1473/1476 行。本包后该书 SR 审查 remaining **0**。

## 5. 全核语义（2/2，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/yangzhai-sanyao/fulltext.md` 的行范围。全书仅 2 父段；理论主段按 subsection 标题与行号对读，并抽核关键口诀、卷界、疑文与卷四编号。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0005` | 评注或元数据 / SR | L3 明确「第一风水网…1989…李德明翻印」「光绪六年扫叶山房 PDF 锚点」「未逐页 OCR」；L4–5 为 source/scan URL。白话区分文字本与影印锚点、否认已证实逐字相同——与源一致，未升为清刊校定 | 通过 |
| 1 | `L0007-L1476` | 理论 / SR | 见下分层抽核；135 节连续覆盖至尾；现代补充、缺文与矛盾保留；notes 禁止整文件归赵氏原著、禁止升 verified | 通过 |

### 理论主段分层抽核（对照原文）

- **题署与目录（L7–14）：** 「赵九峰著·1989…」「卷一…衙署」「卷二西四…」「卷三东四…」「卷四六十四灶/门」与白话目录概括一致；题署属网页文字本，注解未冒充清刊校定。
- **三要定义（L15–22）：** 「门、主、灶」「高大者即是」「不可独重厨灶」「门生主、主生灶、灶生门」「生命之福元」均落到白话；黄石公/杨救贫与游年八宅熟读要求保留为文献层。
- **河图洛书（L23–30）：** 一六水丙辛…甲己土与「戴九履一」位置与注解「数、干合、九宫是不同表」边界一致。
- **现代补充层（L31–100）：** L31 起显标「补充」；九宫数阵与三元九运表独立成节。**年份差：** L95「2144—2164年六运」与 L97 下元「2164—2223」在 2164 年边界重叠，注解保留未擅改——与原文一致。
- **八门游年（L101–110）：** 乾六天五…巽天五六…与「生、天、延为三吉」；注解标明本法 ≠ 蒋氏玄空挨星。
- **东西四宅（L190–204）：** 乾坤艮兑 / 坎离震巽分组、相混即凶与白话一致。
- **三元命宫与五法（L520–536）：** 男五寄坤、女五寄艮；「看门、看主、看灶、看灶口、看命宫」与注解五项总纲一致。
- **卷后门主灶重述（L740–750）：** 与卷首同层而 L750 另有「三宫相生可比和即可不必考虑年命游年」简化语；注解记「简化差异」——正确，未抹平差异。
- **卷二–三门主八灶（L751–1326）：** 独立计数 `X门Y主` 标题 **64** 组（8 门×8 主），每组配八灶；与注解「64 门主各八灶」及「与卷四 64 灶门卦分开」一致。抽核乾门坎主（L752–760）：六煞/天门落水、八灶吉凶标签与白话方向一致。
- **卷四灶门配卦（L1328–1471）：** 引言承认古今格局差别、盼考证修正。抽核：
  - 乾灶八门（L1337–1353）：比和/姤/遁/否/履/无妄/讼/同人卦名与五行断语齐全。
  - 震灶丰条（L1420–1421）：标题「雷火丰」，断曰起句「震卦喜遇贪狼」——注解保留标题与歌句差异，不另造第九条。
  - 巽灶观条（L1435）：正文「火盗木气，木来克土」——注解保留「火盗」与巽坤二卦不对应之疑文，不凭此加入离火第三对象。
  - 离灶编号（L1439–1454）：未济仅一行、噬嗑无序号、随后晋仍标「五」；实际八门齐备——注解「不能依据末号七误报漏一门」成立；鼎条正文「纯阴」而断曰「纯阳」并存待校。
  - 坎灶兑门（L1458）：「土克水，水泄金气」——注解保留与坎兑五行不符之疑误；蹇题「山水蹇」与灶坎门艮上下卦次序问题保留待版本核对。
- **后记与网页尾（L1472–1476）：** 可灶配主、门主灶循环互用 +「验者存之不验者去」——注解标明扩用声明 ≠ 现代检验结果；末四行为转载声明/站名/导航，不计赵氏正文。

抽核未发现空模板白话、把网页补充层写成赵氏清刊原文、把游年法改称玄空飞星、把 64 门主八灶与卷四 64 灶门卦混并、把任何条 `verified` 置 true、或与 `yangzhai-shishu` 串档。

分类可争但不失败：图示多栏展平成行、缺字 `****`、歌句与标题/五行局部矛盾——均已记入 notes 或子节白话，本岗不回改注解。

## 6. 明确非结论

- 本包 **不** 证明清刊影印逐字校定或疾病/财丁/应期旧说经验证。
- 本包 **不** 把任何条升为人工 `verified`。
- 本包 **不** 表示风水材料已接入 FateRadar 八术页面。
- 本包 **不** 覆盖或取代《阳宅十书》审查；两书文件与内容未混用。
- 现代补充气场/九运表、图示版式损失、疑文与编号缺漏，均保持注解已写边界；不据电子文本改字或补图。

## 7. 交付

| 项 | 值 |
|---|---|
| Issue | MING-478 |
| 工作树 | `fateradar-multica-ming-478` |
| 分支 | `codex/multica-ming-478` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/yangzhai-sanyao-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后可将本 Issue `done`；无需重做 0–1；无需回改注解。
