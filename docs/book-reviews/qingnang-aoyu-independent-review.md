# 青囊奥语 · 主本：独立审查 source-reviewed 全量（0–2 / 3）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-457` / 分支 `codex/multica-ming-457`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/qingnang-aoyu.md`、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要与青囊经 / 青囊序混淆；不要抢 MING-447 / MING-452 / MING-453。

结论：**通过。** `validate-annotations` `ok=true entries=3 source_reviewed=3 errors=[]`；`verified` 无 True（3 条均未写该字段，校验器视为未升 verified）；0 draft；起 `qingnang-aoyu:L0001-L0005` 止 `qingnang-aoyu:L0011-L0038`；注解与段落库存 3/3 顺序全等。全书 3 段对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。风水进入知识检索，不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-457`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/qingnang-aoyu.json
shasum -a 256 sources/fulltext/fengshui/qingnang-aoyu/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/qingnang-aoyu.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/qingnang-aoyu.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `bbe77941501850116fa6054fc7a874b32f82c951ea48a70eebb74c7e2e5bb29c`（与 Issue 钉死一致） |
| 注解 blob | `2b39dc425ddfd03f307a8c1f6044944b422ad744`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/qingnang-aoyu/fulltext.md`（38 行） |
| 源 SHA256 | `0718b133e0aaef6f7010d6d985809702ae0d8a2d92924e9fae591fc0431ffdc5` |
| 库存段落 | `references/inventory/paragraphs/fengshui/qingnang-aoyu.json` 3 条，ID 顺序与注解全等 |
| catalog / library | D2 表 slug=`qingnang-aoyu`；维基文库《青囊奧語》；fulltext SHA 与上表一致；版本众多、须明确底本 |
| source-quality | 电子 Wikisource raw；已记「破星」照录、部分干支配对、生克出入未给全操作定义；未宣称影印全校 |

无越权文件。本岗相对 329 只新增本审查稿。未碰 447/452/453 工作树或分支；未碰 `qingnang-jing` / `qingnang-xu` 注解。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/qingnang-aoyu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 3, "source_reviewed": 3,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

3 条：`review=source-reviewed` 全 3；无 `draft`；无 `verified: true`（字段全部缺省，校验器与「verified 全 false」同口径）。空白话 0；空 terms 仅 front matter / 来源行（结构合法）。无 `relatedParagraphIds`。kind 与库存逐条一致。

全书 kind：评注或元数据 2、操作步骤 1。

异字 / 疑点均保留原字与 notes，不补造、不升 verified：

| 索引 | paragraphId | 保留要点（对照原文） |
|---|---|---|
| 2 | `qingnang-aoyu:L0011-L0038` | L11「破星」照录，不得未经底本核对替换为「破军」 |
| 2 | 同上 | L11–12 仅部分干支↔巨门/破星/武曲/贪狼配对，无全套二十四山排盘表 |
| 2 | 同上 | L17「珠宝/火坑」=顺逆运用评价，非二十四山固定善恶分类 |
| 2 | 同上 | L19–23 十项形势观察；无测量阈值与完整坐向算法 |
| 2 | 同上 | L32–34 出入/生克主客参照缺完整操作定义；暂作规则候选 |
| 2 | 同上 | L36 他山救助不能机械推翻本龙条件 |

## 4. 索引边界

段落库存 3 段；注解覆盖 0–2，与库存 ID 列表逐项相等。`remaining=0` / 无 nextId，只相对本电子本 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `qingnang-aoyu:L0001-L0005` |
| 注解索引 1 | `qingnang-aoyu:L0009-L0009` |
| 注解索引 2（止） | `qingnang-aoyu:L0011-L0038` |

电子本结构：YAML front matter（L1–5）→ 空行 → `# 青囊奧語`（L7）→ 空行 → Source URL（L9）→ 空行 → 口诀正文 L11–38。L6–8、L10 为标题/空行，未单独入段（与库存一致）。`remaining=0` ≠ 人工 verified / ≠ 影印校勘 / ≠ 产品交付 / ≠ 已接入八术页面。

## 5. 全书语义（3/3 对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/qingnang-aoyu/fulltext.md` 的 `start_line–end_line`。全书仅 3 段，全部逐段核读。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0001-L0005` | 评注或元数据 / sr | 源 L1–5 YAML：`title: 青囊奧語`、`slug: qingnang-aoyu`、`source: Wikisource raw page`。白话正确标为追踪用 front matter，非术数正文；notes 禁止转成命盘规则 | 通过 |
| 1 | `L0009-L0009` | 评注或元数据 / sr | 源 L9 `Source: https://zh.wikisource.org/wiki/%E9%9D%92%E5%9B%8A%E5%A5%A7%E8%AA%9E`。白话强调回查地址≠影印校勘证明；notes 保留来源、不冒称已校 | 通过 |
| 2 | `L0011-L0038` | 操作步骤 / sr | 见下锚定；白话覆盖方位干支↔巨门/破星/武曲/贪狼、左右阴阳雌雄玄空、十项察龙、倒杖五星高低、生入克入进退；明确星名≠紫微命盘、财富官位灾祸≠已验证现实。terms/notes 与原文要点对齐且不过度补全 | 通过 |

锚定条件与源行（全书核读，非转引进度表）：

- front matter 书题/slug：L2–3
- 维基文库 Source 行：L9
- 坤壬乙→巨門；艮丙辛→破星：L11
- 巽辰亥→武曲；甲癸申→貪狼：L12
- 左陽子癸至亥壬 / 右陰午丁至巳丙：L13
- 雌雄交會玄空；山水祸福相关；明玄空只在五行、不须寻纳甲：L14–16
- 顛顛倒珠宝 / 順逆行火坑：L17
- 十项：龍身行止→來脈明堂→傳送功曹→明堂十字→前後青龍→八國城門→天心十道→屈曲流神→平地青雲→一缺非真：L19–23
- 倒杖 / 掌模太极 / 化气生克 / 五星方圆尖秀 / 高低 / 鬼曜 / 向放水生旺休囚：L24–27
- 二十四山分五行；翻天倒地对不同、密秘在玄空；认龙立穴、辨天心、向中放水：L28–31
- 从外出入=进；从内生出=退；出入克入=旺：L32–34
- 龙歇脉寒；他山救助空劳禄马：L35–36
- 再辨星辰；识得真微妙、又见郭璞：L37–38

抽核未发现空模板白话、把「破星」静默改成「破军」、把部分干支配对补成全二十四山排盘表、把珠宝/火坑写成山本身固定善恶、把生克出入升为可执行算法、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1–5 front matter；L7 标题；L9 来源；L11–38 口诀）。3 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/异字去向，不是影印逐字校勘，也不是风水断语有效证据，也不等于二十四山/玄空/倒杖已写入产品引擎。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是青囊奥语全书产品交付，也不覆盖生产侧 `docs/book-reviews/qingnang-aoyu.md`，更不冒充已接入八术页面。不要与 `qingnang-jing` / `qingnang-xu` 混为一书。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺失 | 3/3 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 「破星」字形 | L11 原文「破星」 | notes 已记。不静默改为破军 |
| 部分干支↔星配对 | L11–12 四组 | 不自行补全二十四山表 |
| 珠宝 / 火坑 | L17 | 顺逆运用评价，非山固定善恶 |
| 十项观察 | L19–23 | 无阈值/坐向算法；不作可运行规则 |
| 出入 / 生克 | L32–34 | 缺完整主客定义；规则候选不执行 |
| 他山救助 | L36 | 不机械当已化解 |
| 紫微星名同名 | 巨门/武曲/贪狼 | 白话已声明≠紫微命盘星曜 |
| 与青囊经/序 | 本书 slug=`qingnang-aoyu` | 本审查不覆盖另两书 |

## Caveat（不改注解，留给后续 pack）

1. **「破星」未经底本核定。** 不得静默替换为破军或并入紫微破军语义。
2. **L11–12 仅部分干支配对**；不得拼成完整二十四山→九星排盘表驱动产品。
3. **珠宝/火坑、生入克入进退** 缺完整操作定义与测量阈值；只作阅读说明，不升可执行引擎。
4. **维基文库电子本** 不能证明版本完整或与某影印底本一致；来源行仅供回查。
5. **既有 `qingnang-aoyu.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。
6. **风水知识包 ≠ 八术页面交付**；不得宣称 FateRadar WebUI 已消费本口诀。

## 交付边界

- 写出：仅 `docs/book-reviews/qingnang-aoyu-independent-review.md`
- 禁止：改注解 JSON / 源文 / inventory / 他书审查 / main 合并 / 部署 / force push
- 推送：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-457`
- remaining 本包后：**0**（相对本电子本 3 段 SR 覆盖）
