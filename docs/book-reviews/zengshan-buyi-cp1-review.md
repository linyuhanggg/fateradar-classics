# 《增删卜易》主本：独立审查 CP1（0–299）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。工作树只读参考本 SHA，本岗写出仅本文件。未改注解 JSON、未改源文、未改 `zengshan-buyi--wikisource-volume1`、未改引擎 / `chart.*` / golden / 他书。不是《增删卜易》全书完成，不是续写 0–299，不是引擎包，也不是全项目完成。测试岗未参与本文件生产。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。录入者评语与原剑增订已标现代层，未冒充野鹤原典。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–3124（`L0936-L0936` 起）本包不审、不改。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-224`，2026-09-11）：

```
git fetch origin bc798566da77c30e149abf9673c88ecc386702b2
git rev-parse HEAD
git ls-remote origin refs/heads/codex/full-library-completion
shasum -a 256 references/annotations/divination/zengshan-buyi.json
shasum -a 256 sources/fulltext/divination/zengshan-buyi/fulltext.md
git rev-parse HEAD:references/annotations/divination/zengshan-buyi.json
git rev-parse HEAD:sources/fulltext/divination/zengshan-buyi/fulltext.md
```

结果：

| 项 | 实测 |
|---|---|
| 本岗 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `8acccbd8511fe63564087159f4e61bacd7ab9f9ada270d1c8ed2339af6ad750f`（与 Issue 钉死值一致） |
| 注解 blob | `205a55ba0548603cd15f0ae921713b10a2eca99a` |
| 源 `fulltext.md` SHA256 | `90876203ab27a69da13e615bca83c031bf961ece3c2b3794e892340195c97e65` |
| 源 blob | `8b9cac56c3739b9f3cb3c9e824bd4678d7c34b97` |
| `scopeNote` | 3125 段全处理；source-reviewed 只对照电子文字；卷一正文错位于 L6504–7730；卷首/原剑为现代层 |
| 段落清单 | 3125 段；`classification_note` 写明 source-reviewed 不等同人工影印核验 |
| 注解 ID 与 `paragraphs.json` | 3125/3125 一一对应，`mismatch=0` |
| 本包索引 | 0–299；未改 300–3124 |

无越权文件。源层未改。他书 / 引擎 / `chart.*` 未覆盖。不是续写包。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/zengshan-buyi.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 3125, "source_reviewed": 3125,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`entry.get("verified") is True` 才会报错；本文件 3125 条均无 `verified` 字段，等价未升 true。

## 3. verified / draft 未越权提升

全书 3125 条：`review=source-reviewed` 全 3125；`verified` 字段 0 条（true=0）；`draft` 0。无升 verified。

本包 CP1（0–299）kind：案例 233 / 评注或元数据 34 / 理论 13 / 序跋目录 9 / 规则候选 5 / 操作步骤 4 / 术语 2。

其中 `diagramTranscription` 183（均为案例爻行字面转录）；非图行 117。

空 vernacular 0；空 notes（`[]`）35；空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。vernacular 长度 min 11 / 中位 30 / max 124。图行 vernacular 有同构重复（如「本行是兄弟爻，丑土…」）属相同爻符结构，不是目录套话模板。

## 4. 索引边界

`paragraphs.json` 全书 3125 段；本包审查 0–299。300–3124 在同一 JSON 中已是 `source-reviewed`，本岗只读不改、不把其计入本包通过范围。

| 位置 | 实测 ID | heading / 说明 |
|---|---|---|
| 注解/源索引 0（CP1 起） | `zengshan-buyi:L0007-L0007` | 錄入者言 |
| 注解索引 299（CP1 止） | `zengshan-buyi:L0934-L0934` | 增刪卜易卷之二（爻行图） |
| 注解索引 300（下一包起，不在本包） | `zengshan-buyi:L0936-L0936` | 增刪卜易卷之二 |
| 源/注解索引 3124（全书末） | `zengshan-buyi:L7959-L7964` | 书末 |

起始/止点与 Issue 钉死 ID 一致。remaining 2825（300–3124）。CP1 覆盖：卷首录入者/原剑现代层、四卷目录、卷二月破章至进退章及相关占验图行；独发两现星煞千金赋天时及卷三起不在本包。

## 5. 抽样语义（≥15 非模板，对照原文，不凭既有全书报告）

原文取 `sources/fulltext/divination/zengshan-buyi/fulltext.md` 的 `start_line–end_line`。下列为录入者分层、月破/飞伏/进退关键规则与非图行案例抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0007-L0007` | 评注 / sr | 录入者言：占卜作辅助、不信命定。vernacular 明标「现代录入者立场」；notes 禁止署为野鹤原典 | 通过 |
| 1 | `L0009-L0009` | 评注 / sr | 「百试百灵」为录入者称赞；notes 不得抽作准确率宣传 | 通过 |
| 2 | `L0011-L0011` | 评注 / sr | 地摊文言+糊涂白话、未细校。电子本质量声明保留 | 通过 |
| 3 | `L0015-L0015` | 评注 / sr | 原剑增订纳甲/六神/世应/旬空等；notes 标现代层，不替代缺失卷一古文入口 | 通过 |
| 5 | `L0021-L0022` | 评注 / sr | 乾甲壬坤乙癸、三男丙戊庚、三女丁己辛。kind 评注，非野鹤规则 | 通过 |
| 29 | `L0158-L0188` | 序跋 / sr | 卷一 31 章目录；白话说明正文错位于 L6504–7730，目录后无文≠全书缺失 | 通过 |
| 37 | `L0373-L0373` | 操作 / sr | 逐月月破支：正申…十二未。须先取月建 | 通过 |
| 38 | `L0375-L0375` | 理论 / sr | 「诸书」月破如枯根全无用；白话标明是下段野鹤反对的旧说，未合并成作者规则 | 通过 |
| 39 | `L0377-L0377` | 规则 / sr | 野鹤：动/变月破仍可作用；出月、填实、逢合；静无助才到底破 | 通过 |
| 70 | `L0443-L0452` | 案例 / sr | 寅官世被申克、子元破空；与幕客忌元同动必升争辩，书报七月非、冬月降调。notes 保留分歧 | 通过 |
| 103 | `L0529-L0529` | 规则 / sr | 伏神有用六类（日月生、旺、飞生、动生、冲克飞、飞空破衰墓绝） | 通过 |
| 104 | `L0531-L0531` | 理论 / sr | 黄金策「空下伏神」；notes 空下=飞神空，非伏神自空 | 通过 |
| 106 | `L0535-L0535` | 规则 / sr | 伏神无用五类；第五项含休囚限定，不得删成凡空皆无用 | 通过 |
| 108 | `L0539-L0539` | 理论 / sr | 反驳「伏居空地事与心违」：旺而空可出空日出现 | 通过 |
| 125–126 | `L0573` / `L0575` | 理论 / sr | 旧法跨宫补用 vs 野鹤再占、有伏亦先不用。notes 标不宜默认执行他家法 | 通过 |
| 149 | `L0621-L0627` | 案例 / sr | 三卦同见亥伤、寿姓医、亥月绝。notes：隐瞒后段与事后结果≠独立先验验证 | 通过 |
| 165 | `L0665-L0666` | 理论 / sr | 反驳丙辛化水寻子：世未已变亥、子日亦可用水 | 通过 |
| 169 / 171 | `L0674` / `L0678` | 规则 / sr | 进/退神地支列；notes 未写戌→丑 / 丑→戌，不补造 | 通过 |
| 181 | `L0698-L0698` | 案例 / sr | 酉官暗动+五爻官进+财生，书报连捷。notes 须保留多条件 | 通过 |
| 247 | `L0830-L0830` | 案例 / sr | 久病逢冲父世，化退≠病退；书报丑月卒 | 通过 |
| 287 | `L0910-L0910` | 案例 / sr | 世寅月破化进，出月/亥月逢合才行；notes 出月≠事先精确亥月 | 通过 |
| 41 / 299 | `L0381` / `L0934` | 案例图 / sr | 两栏爻行字面转录（父母未世/戌；兄弟酉/酉）。`literal-two-column-row` 与源符一致 | 通过 |

关键条件与源行（抽核，非转引既有全书报告）：

- 录入者 / 原剑现代层：L7、L9、L11、L15、L21–22
- 卷一目录与错位说明：L158–188（正文实际 L6504–7730，本包不审该区）
- 月破表与旧说/野鹤修正：L373、L375、L377
- 伏神六有用 / 五无用 / 空下 / 跨宫 / 再占：L529、L531、L535、L539、L573、L575
- 进退列与案例：L674、L678、L698、L830、L910
- 图行字段：L381、L934

## 6. 录入者评语 ≠ 野鹤原典

Issue 要求：录入者评语不得当成野鹤原典。

| 层 | 本包位置 | 判定 |
|---|---|---|
| 錄入者言 | 索引 0–2，`L0007`–`L0011` | kind=评注或元数据；白话/notes 明标录入者、非野鹤、非准确率证明 |
| 原劍增訂及卷首公式/图 | 索引 3–28（納甲/六神/世应/藏干/八纯/旬空/生旺/天乙/反吟伏吟/卜筮原理） | 全部 kind=评注或元数据；无泄漏为规则候选/理论/案例 |
| 卷二署名行 | 索引 33–35 | 野鹤著 / 李坦鉴定 / 李文辉增删分列责任者，不混为单一作者规则 |
| 野鹤正文起点 | 索引 36+ 月破章 | 旧说与野鹤反驳分层（如 L375 vs L377）；被引「彼断/黄金策」与「予断」分开 |

无把录入者「百试百灵」或原剑公式写成野鹤原典规则的缺陷段 ID。卷首若干条 vernacular 未逐条复写「现代」二字（如 `L0024`），但仍在评注 kind 与原剑增订范围内，不升为失败。

## 7. source-reviewed ≠ 人工 verified

300 条电子语义阅读保持 `source-reviewed`（全书累计 3125），只表示对照当前电子段落实了白话、种类、术语、图行转录与校记/去向，不是影印逐字校勘，不是人类专家验盘，不是预测有效证据，也不是算法可执行。不得把 3125 条 source-reviewed 写成已人工 verified。本包不是卷二余章+卷三卷四+错位卷一全文交付，也不是产品交付。

既有 `docs/book-reviews/zengshan-buyi.md` 是标注岗全书加工报告，不是本岗独立审查证书；本文件才是 CP1 独立复核。

## 8. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 空 notes | CP1 35 条（`[]`；案例 21 / 序跋 6 / 评注 4 / 理论 3 / 术语 1） | vernacular 仍具体。不回改 |
| 图行 vernacular 同构重复 | 25 组，最大重复 3（如兄弟申金阳爻行） | 同符结构合法；不是空模板。不回改 |
| `verified` 缺省 | 3125 条无该字段 | 校验器按「不是 True」放行。不得补 true |
| 书中「果…」应验句 | 多条案例 notes 已标非独立验证 | 不升 verified、不作统计准确率 |
| 卷一正文错位 | 目录在 CP1；正文 L6504–7730 不在本包 | 不把目录当缺失；不在本包续写错位区 |
| 既有全书报告 | `zengshan-buyi.md` 已在权威树 | 本岗未改该文件 |

## Caveat（不改注解，留给后续 pack）

1. **月破**：`L0375` 是被反驳的旧说；`L0377` 才是野鹤条件化修正。接入规则库不得合并成「月破永无用」或「凡破立刻全有效」。
2. **伏神**：六有用/五无用须合读；空下=飞神空；作者本人倾向再占、跨宫补用被质疑。不得只取六类支持关键词当最终吉凶。
3. **进退**：进≠吉、退≠凶；空破待填等条件在后文。`L0674`/`L0678` 未列的土支循环不得静默补全。
4. **图行**：183 条 `literal-two-column-row` 是爻符字段，不是 183 个独立断例；不得按段落数计规则数。
5. **应验叙事**：书中果报、隐瞒后段、复占分时解释均属原叙事；无公历/独立样本，不可当预测验证。
6. **电子源**：录入者自承未细校；本地无对应影印。照电子本 source-reviewed，不升 verified。

## 未决（本岗不施工）

- 索引 300–3124 留给后续独立审查，nextId `zengshan-buyi:L0936-L0936`，remaining 2825。含卷二余章、卷三卷四门类、错位卷一正文区与书末图。
- 影印逐字校勘、争议裁决、规则机器实现、独立现实预测验证仍不在 `source-reviewed` 口径内。
- 本审查不把任何条目标成人工 verified。
- 勿重做 0–299 续写；勿改注解 JSON。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-224`。
