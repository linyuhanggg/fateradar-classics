# 奇门遁甲统宗 · 演義 vol4–9 补充层：独立审查 source-reviewed 全量（0–93 / 94）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-462` / 分支 `codex/multica-ming-462`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/qimen-dunjia-tongzhi.md`、未改 inventory / catalog / NLC layouts / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-447 / MING-452。不要与 `qimen-dunjia-tongzhi--nlc-layouts` 或统宗主本注解文件混淆。

结论：**通过。** `validate-annotations` `ok=true entries=94 source_reviewed=94 errors=[]`；`verified` 字段全缺省（0 条 True，与「verified 全 false」同口径）；0 draft；起 `qimen-dunjia-tongzhi:yanyi-vol4-9:L0003-L0003` 止 `qimen-dunjia-tongzhi:yanyi-vol4-9:L0189-L0189`；94 条 ID 覆盖补充源文奇数行 3…189，与 `source-editions` 登记 `yanyi-vol4-9` paragraphs=94 一致。抽读 ≥20 段对照实际补充原文成立；91 条「重复」首条 `relatedParagraphIds` 与主电子本同文（忽略空白）。`source-reviewed` 不是人工 `verified`；网页补充层不是纸本卷四至九局式；`remaining=0` 只指本补充层 paragraphId 集合。不冒称八术页面接入。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-462`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json
shasum -a 256 sources/fulltext/san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md
git rev-parse HEAD:references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json
git rev-parse origin/codex/multica-ming-329:references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json --json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `a584d3beb81cc43b1b261ed9286f758dd74b31d864e82fc62899a3537d21942a`（与 Issue 钉死一致） |
| 注解 blob | `c957a3dbf1289527da7f4e59108616203589b3b3`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md`（189 行） |
| 源 SHA256 | `a86fc6d52b7f56a3fa51bfbf349439a4a8244456e965b8f4a9b1b4fc32ee4814` |
| `source-editions` | id `yanyi-vol4-9`；label「奇门演义网页对照层 · 与主文本重叠」；paragraphs/annotations 94 |
| 主本 fulltext | `sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`（对照同文用，本包不改） |
| NLC layouts | `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json` 存在且未打开施工；本包不混审 |

无越权文件。本岗相对 329 只新增本审查稿。未碰 447/452 工作树或分支，未改 NLC / 主本注解。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/qimen-dunjia-tongzhi--yanyi-vol4-9.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 94, "source_reviewed": 94,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

94 条：`review=source-reviewed` 全 94；无 `draft`；无 `verified: true`（字段全部缺省）。空白话 0；空 terms 0；空 notes 0。

全书 kind：重复 91、评注或元数据 3。

元数据 3 段（无 `relatedParagraphIds`）：

| 索引 | paragraphId | 对照要点 |
|---|---|---|
| 0 | `…:L0003-L0003` | 源为太乙书局 URL；白话声明不能据补充文件名增加独立证据 |
| 1 | `…:L0005-L0005` | 源题「奇门演义(…卷之四～九）」；白话区分网页标题与纸本阴阳十八局式 |
| 2 | `…:L0007-L0007` | 源为零宽空字符；白话作排版残留，不计有效正文 |

91 条「重复」均带 `relatedParagraphIds`（89 条 3 个、2 条 4 个）：首条相关 ID 与本段忽略空白后同文 91/91；第二条多为卷十复引同文；其余为赋/注配对或邻接缺文上下文，**不要求**字面同文。本包确认「重复」指与主电子本/卷十层重叠，不是把配对注强行改写成同文。

## 4. 索引边界

补充源文 189 行；非空行 95（含 L1 标题 `# …`）；注解覆盖奇数行 L3…L189 共 94 段。未覆盖非空正文仅 L1 文件标题行（合理，不计入 paragraph 集）。`remaining=0` / 无 nextId，只相对本补充层 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `qimen-dunjia-tongzhi:yanyi-vol4-9:L0003-L0003` |
| 注解索引 93（止） | `qimen-dunjia-tongzhi:yanyi-vol4-9:L0189-L0189` |

`remaining=0` ≠ 人工 verified / ≠ 纸本卷四至九局式已补 / ≠ NLC 对图完成 / ≠ 产品交付。

## 5. 抽样语义（≥20 非模板要点，对照补充原文）

原文取 `sources/fulltext/san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md` 的 `start_line–end_line`。下列抽核；「重复」条白话均以「此补充网页段与主电子文本同文。」起句，下表记其非模板要点与同文首相关 ID。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003` | 评注或元数据 / sr | 来源 URL；不可增独立证据 | 通过 |
| 1 | `L0005` | 评注或元数据 / sr | 网页卷四～九题 ≠ 纸本十八局 | 通过 |
| 2 | `L0007` | 评注或元数据 / sr | 零宽字符排版残留 | 通过 |
| 3 | `L0009` | 重复 / sr | 太阴值休门赋；阴雨/无桥/主不宜战；同文 `L1019` | 通过 |
| 4 | `L0011` | 重复 / sr | 太阴会休门注；二八日应；赋东南 vs 注或东或西，白话保留分歧 | 通过 |
| 9 | `L0021` | 重复 / sr | 太阴值杜门赋；对应注缺，不填通用杜门 | 通过 |
| 10 | `L0023` | 重复 / sr | 「注缺。太阴会景门，及太阴会死门赋，均缺。」不作古代判断 | 通过 |
| 14 | `L0031` | 重复 / sr | 太阴值开门；丑日晴、东风利主；捕分男女 | 通过 |
| 19 | `L0041` | 重复 / sr | 六合会生门；蓬星午时雷雨；午时是占期非观测验证 | 通过 |
| 24 | `L0051` | 重复 / sr | 六合景兮不时雷；坤兵变；捕西方 | 通过 |
| 29 | `L0061` | 重复 / sr | 六合会惊门；丁奇大旱；午未主方警语 | 通过 |
| 34 | `L0071` | 重复 / sr | 白虎加生；午后巽风三日；客防粮地火 | 通过 |
| 39 | `L0081` | 重复 / sr | 白虎会杜门；雾霉风；「不足」疑误字不猜补 | 通过 |
| 44 | `L0091` | 重复 / sr | 白虎加惊；三日狂风；丑未良将 | 通过 |
| 49 | `L0101` | 重复 / sr | 玄武会休；白云晴/雹雨分条件；有奇可进仍无大胜 | 通过 |
| 54 | `L0111` | 重复 / sr | 玄武兮杜门；甲寅晴；渡口防贼 | 通过 |
| 59 | `L0121` | 重复 / sr | 玄武会死；大溪阻、西南小路；近燃火僧道 | 通过 |
| 64 | `L0131` | 重复 / sr | 九地会休；问雨反晴；西北行 | 通过 |
| 67 | `L0137` | 重复 / sr | 「注缺，九地会伤门，九地会杜门赋诀，均缺」；完整覆盖≠缺文已恢复 | 通过 |
| 69 | `L0141` | 重复 / sr | 九地会景；无奇雨、奇至巳午晴 | 通过 |
| 74 | `L0151` | 重复 / sr | 九地会惊；客有奇+太阴助可胜，不可只取「客多疑」 | 通过 |
| 79 | `L0161` | 重复 / sr | 九天生门；连雨/冬雪；主休征副将坐营 | 通过 |
| 84 | `L0171` | 重复 / sr | 九天会杜；未时黄云次午雨；「解粮革来」不猜补 | 通过 |
| 89 | `L0181` | 重复 / sr | 九天惊门；寅巳晴、午未雨、丑子雷 | 通过 |
| 91 | `L0185` | 重复 / sr | 九天开门赋；午未风、冬雪；水火利乾 | 通过 |
| 93 | `L0189` | 重复 / sr | 八将会门例：阳二局乙庚日戊寅时；天盘值使；丁加癸凶格不可照一般吉辞放行；同文 `L1199-L1205` | 通过 |

关键条件与源行（抽核）：

- 太乙 URL / 卷题 / 零宽：L3、L5、L7
- 太阴值休门赋与会休门注：L9、L11
- 太阴杜门赋与注缺景/死门：L21、L23
- 六合会生门午时雷雨：L41
- 白虎会杜「不足」：L81
- 九地缺文标记：L137
- 九地会惊客方救应：L151
- 八将会门阳二局戊寅例与丁加癸：L189
- 主本同文锚点示例：`L1019`/`L1021`、`L1031`/`L1033`、`L1199-L1205`

## 6. source-reviewed ≠ 人工 verified

本层为太乙书局网页补充对照，`source-editions` 明示与主文本重叠。94 条 `source-reviewed` 只表示对照本补充电子段落实了来源/卷题/排版残留、演义赋注与主本同文关系、两处缺文标记与末条例局约束，不是影印逐字校勘，也不是奇门应验或算法正确性证明。纸本真正卷四至九是阴阳十八局式（见既有 `qimen-dunjia-tongzhi.md` / NLC），网页「演義卷四～九」标题不能证明那些图表已由本层补齐。不得把 94 条 source-reviewed 写成已人工 verified。`remaining=0` 仅对本补充层注解覆盖而言。不冒称八术页面已接入本层。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 字段缺省 | 94 条均无 `verified` 键；0 条 True | 与「全 false」同口径。不回改 |
| kind=重复 91 | 首相关 ID 同文 91/91；另含卷十复引与赋注配对 | 结构合理。不回改 |
| 缺文标记 2 | `L0023`、`L0137` | 正确保留为缺文说明。不回改 |
| 网页题 vs 纸本卷次 | L5 与 PDF 目录十八局 | 白话已区分。不回改 |
| 末段换行 | 生产说明「90 段原样相同，末段仅换行不同」；本岗同文比对忽略空白后末段亦匹配 | 不升 verified |
| NLC layouts / 主本注解 | 本包未打开施工 | 勿与本补充层混验收 |
| Issue 对照路径 | 实际为 `supplemental-taiyi-qimen-yanyi-vol4-9.md`，非凭文件名臆造 | 已定位 |

## Caveat（不改注解，留给后续 pack）

1. **网页重叠层**：不增加独立原例证据数量；引用须回主本或本补充 ID，勿三计。
2. **纸本卷四至九局式**：属 NLC / 十八局恢复线，不在本 94 段范围内。
3. **缺文**：太阴景/死门赋、九地伤/杜门赋等仍缺；`remaining=0` 不表示缺文已恢复。
4. **赋注分歧与疑字**：如休门捕向东南 vs 或东或西、杜门注「不足」、解粮革来等，保持字面，不猜补。
5. **八将会门例**：乙庚日组不补具体公历日干；丁加癸凶格不得被一般吉辞覆盖；最小布局仍须另核原宫/寄宫。
6. **`remaining=0`**：只表示本补充层 94 个 paragraphId 已尽；不是人工 verified、不是统宗全书校勘、不是产品交付。

## 未决（本岗不施工）

- 94 条 source-reviewed 不是人工 verified，也不是奇门效验，也不等同算法已实现。
- 纸本局式 / NLC 对图继续走既有专线；本岗不回改注解、不改 `qimen-dunjia-tongzhi.md`、不碰 447/452。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-462`。远端 `linyuhanggg/fateradar-classics`。
