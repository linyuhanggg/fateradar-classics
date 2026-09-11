# 玉照定真經 · 识典 SK1602：独立审查（13 条全量）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-484` / 分支 `codex/multica-ming-484`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖既有 `yuzhao-shenying-sk1602-review.md` / progress、未改主本 `yuzhao-shenying.json`、未抢 MING-481 玉照主本审查稿、未改 SK1605 / 他书 / 引擎 / 产品仓。本岗未参与识典 SK1602 生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审识典 SK1602（13 条），不要与主本 2 条 `Lxxxx` 包混淆。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；11/13 `source-reviewed`、2 draft；`verified=true` 为 0，13 条均显式 `"verified": false`；`paragraphs.json` 与注解 `paragraphId` 一一对应且同序；11 条 SR 对照电子原文语义成立，2 条 draft 保持 draft（源即无可转存文字）。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified、不把 draft 升 SR。本岗未改注解。该书识典 SK1602 SR 审查 remaining **0**；draft remaining **2**（索引 6、12）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-484`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json
shasum -a 256 sources/normalized/shidianguji/SK1602/text.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json --json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `622fc897613ebee6829b191cbd803e2bdafde5769d72038fee4c69d62e17d982`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `b8853cb49b03e217fa7c2c61a392759db08becd6` |
| 源 `text.md` SHA256 | `996873796425cdcd58e36c6e5971757e2de572577b5c161c9b3ba8f02e92f8bc` |
| 源行数 / 字符 | 1004 行 / 18736 字 |
| `provenance.json` `sourceStatus` | `reference-text` |
| 工作树相对 HEAD | 仅新增本审查文件与同 Issue 另一书审查稿；注解 JSON / 源文 / 既有 sk1602 review·progress 无 diff |

无越权文件。注解未改。源文未改。未写产品仓。未碰主本玉照文件。

对照路径确认：`sources/normalized/shidianguji/SK1602/text.md` 与 `paragraphs.json` 存在，与 provenance 一致。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 13, "source_reviewed": 11,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

13 条：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 11/13 |
| `review=draft` | **2**（索引 6、12） |
| `verified=true` | 0（文件内 `"verified": true` 出现次数 = 0） |
| `verified=false` | **13/13 显式 false** |
| 空白话 / 「本段论述 / 白话从略 / 见原文 / TODO」 | 0 |
| 空 `terms` | 0 |
| 三长段 subsections | 15 / 12 / 13，ID 连续；非空行覆盖全段无缺口；子节 vernacular 无空 |

draft 两条：

- `yuzhao-shenying:shidian-SK1602:P7639282082212053002`（索引 6，源 L60）
- `yuzhao-shenying:shidian-SK1602:P7639282082213412874`（索引 12，源 L1003）

源即占位「无可转存文字」，白话声明不能补字或升规则；保持 draft、`verified=false`。索引 11 的 `figureCount=1` 仅段末 L1001 图像占位，该条因 L675–1000 有经注而保持 `source-reviewed`，图像本身未转写、未升为可引用条文。

## 4. 索引边界与主本隔离

`sources/normalized/shidianguji/SK1602/paragraphs.json` 13 段；注解 13 条。`paragraphId` 全部命中，`missing=0`，顺序与 inventory 一致。起 `yuzhao-shenying:shidian-SK1602:P7639282082211954698`、止 `…P7639282082213412874`，与 Issue 钉死一致。

主本隔离：`references/annotations/luming-nayin/yuzhao-shenying.json` 主本 ID（`Lxxxx`）与本识典 `P…` ID **交集为空**。本包不审主本，不把主本 2 条算进识典 remaining。与同 Issue SK1605 识典 ID 亦无交集。

inventory `kind=待分类`；注解用序跋/评注/规则候选/待核实，与生产侧一致；本岗不回改。

## 5. 13 段全部对照原文（不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1602/text.md` 的 `start_line–end_line`。未发现模板空话；无把整段原文粘进 vernacular 冒充处理。

| # | 尾 ID | 源行 | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|---|
| 0 | `P…1954698` | 9 | 序跋 / sr | 「欽定四庫全書」馆题，非断法 | 通过 |
| 1 | `P…1971082` | 11 | 序跋 / sr | 书名「玉照定真經一卷」；网站章节≠印本卷号已校 | 通过 |
| 2 | `P…1987466` | 15 | 序跋 / sr | 网站章节名「提要」，馆臣案语在下段 | 通过 |
| 3 | `P…2003850` | 17–46 | 评注 / sr | 馆臣提要：晋书/隋唐宋史志不著录、叶盛一册不著撰人、江南方言疑书注均出张颙、大典辑存；外亲女婿穿凿不得跳过。「切近中理亦多有可採」是馆臣评价，不能当已应验。原文「大㫖」「依託」「附㑹」不改正文 | 通过 |
| 4 | `P…2020234` | 48–54 | 序跋 / sr | 总纂官纪昀、陆锡熊、孙士毅 | 通过 |
| 5 | `P…2036618` | 56–58 | 序跋 / sr | 总校官陆费墀 | 通过 |
| 6 | `P…2053002` | 60 | 待核实 / draft | 源即占位「无可转存文字」，未补字、未升 sr/verified | 通过 |
| 7 | `P…3330954` | 64 | 序跋 / sr | 正文前重复馆题 | 通过 |
| 8 | `P…3347338` | 66 | 序跋 / sr | 「玉照定真經張顒注」题署≠作者已考定，回指提要 | 通过 |
| 9 | `P…3363722` | 68–362 | 规则 / sr | subsections×15。生气须日時见三合或干长生；身命须支刑且纳音克；干轻音重、六月丁可为官五月为鬼；伏吟在家返吟他处；墓有旺为库无旺为墓；丙亥丁子真合则「不为前说」；本卦须得时否则客卦；段末「只有东王翁也，」跨下段 | 通过 |
| 10 | `P…3380106` | 364–673 | 规则 / sr | subsections×12。承接薫风中阳；本主干合为内合、别组为外合；延月只胎时干合、日胎合不算；九宫甲子加得十八、乙卯乘六八得四十八，算术不一标 unknown；前五位推亲连读提要穿凿批评；段末「木入烟中」跨下段 | 通过 |
| 11 | `P…3396490` | 675–1001 | 规则 / sr | subsections×13。续完「同耳」后开进退/三交四聚；六害与六合有主客方向不能对调后仍贴原意；正道歌真化须长生建旺；救神问克后有生；神杀劫亡非本理；借气明说胎不取；空亡偏正含糊保留 unknown；段末图像占位不补字 | 通过 |
| 12 | `P…3412874` | 1003 | 待核实 / draft | 源即占位「无可转存文字」，未补字、未升 sr/verified | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 生气须日時 / 长生亦名生气：L70
- 支与纳音身命刑克：L78
- 干轻音重：L94
- 伏吟 / 返吟：L101–102
- 有旺气为库：L146
- 丙亥丁子「不为前说」：L178
- 客卦：L315
- 东王翁跨段：L362 → 下段 L364「乃薫风中阳也」
- 延月：L425–426
- 九宫「十八」与算术不一：L508–509
- 无可转存：L60、L1003

## 6. Caveat（不构成本包失败）

1. 源层 `reference-text`，电子阅读不是影印校勘。
2. 网站章节名不等于印本卷号；注解已标明。
3. 2 条 draft 因版面无字保持 draft，不升 SR / verified。
4. 索引 11 段末图像未转写；不补字、不升为可引用条文。
5. 九宫算术动作不一、空亡偏正含糊处保持 unknown，不凑现代数表。
6. `source-reviewed` ≠ 人工 `verified`；本岗不回改、不提升。
7. 既有生产侧 `yuzhao-shenying-sk1602-review.md` 不覆盖、不回改；本文件为 MING-484 独立审查稿。

## 7. Remaining

| 项 | 值 |
|---|---|
| 本包范围 | 识典 SK1602 全 13 条 |
| SR 审查 remaining | **0** |
| draft remaining | **2**（L60、L1003 版面占位；保持 draft） |
| verified | 仍全 false |
| 下一步 | 协调收件；draft 不另派升格，除非源层补出可转存文字 |

失败清单：无。
