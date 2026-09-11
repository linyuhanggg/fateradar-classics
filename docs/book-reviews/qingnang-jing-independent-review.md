# 青囊经 · 主本：独立审查 source-reviewed 全量（0–23 / 24）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-450` / 分支 `codex/multica-ming-450`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 `docs/book-reviews/qingnang-jing.md`、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要与青囊奥语 / 青囊序混淆；不要抢 MING-447 / MING-448。

结论：**通过。** `validate-annotations` `ok=true entries=24 source_reviewed=24 errors=[]`；`verified` 无 True（24 条均未写该字段，校验器视为未升 verified）；0 draft；起 `qingnang-jing:L0005-L0005` 止 `qingnang-jing:L0641-L0816`；注解与段落库存 24/24 顺序全等。抽读 ≥15 段对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。风水进入知识检索，不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-450`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/qingnang-jing.json
shasum -a 256 sources/fulltext/fengshui/qingnang-jing/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/qingnang-jing.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/qingnang-jing.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `3d16051b3770b53a928e34f8c4b9518b1d03652d26929d1fee3c2b14e3cfb4bb`（与 Issue 钉死一致） |
| 注解 blob | `72f57fe53e613aecb4ac8e39752977275eb896a8`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/qingnang-jing/fulltext.md`（816 行） |
| 源 SHA256 | `ddff7d3ea10f12ed14b6ffe5ce6266761f6feff24186a092930657cffdc9ec26` |
| 库存段落 | `references/inventory/paragraphs/fengshui/qingnang-jing.json` 24 条，ID 顺序与注解全等 |
| catalog / library | `source_anchor_url` = 维基文库《青囊經》；`actual_fulltext_path` = `sources/fulltext/.../fulltext.md`；版本众多、须明确底本与是否含注疏 |
| source-quality | `text-present`；已记异字 / L460–464 缺接 / 宿名疑点；未宣称影印全校 |

无越权文件。本岗相对 329 只新增本审查稿。未碰 447/448 工作树或分支；未碰 `qingnang-aoyu` / `qingnang-xu`。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/qingnang-jing.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 24, "source_reviewed": 24,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

24 条：`review=source-reviewed` 全 24；无 `draft`；无 `verified: true`（字段全部缺省，校验器与「verified 全 false」同口径）。空白话 0；空 terms 仅评注/引语段（结构合法）。`relatedParagraphIds` 全部落在本书 24 个 ID 内。kind 与库存逐条一致。

全书 kind：理论 11、序跋目录 6、评注或元数据 4、重复 3。

异字 / 疑点均保留原字与 notes，不补造、不升 verified：

| 索引 | paragraphId | 保留要点（对照原文） |
|---|---|---|
| 9 | `qingnang-jing:L0024-L0024` | 前录「太微南垣」（L24）；后录「太极南垣」（L425）。不立第五星垣 |
| 13 | `qingnang-jing:L0032-L0032` | 「气囿于形」「因变北」vs 后录「气囿于地」「因变化」分录保留 |
| 16 | `qingnang-jing:L0039-L0042` | 「临制/制临」「纪纲/纪网」「弘/宏」「柔生于刚/柔生始刚」等异文分记 |
| 17 | `qingnang-jing:L0044-L0420` | 「有七必有六」（L88）、卦体行文疑点；原字保留 |
| 20 | `qingnang-jing:L0430-L0635` | L460–464 木岁星→中央/季夏/信缺接；宿名「氏」「昂」「亢失」等不静默改字；四垣含少微 |
| 23 | `qingnang-jing:L0641-L0816` | 「乙太极」「天地万他」；「然此诸方之气」相邻重复（L700–701） |

## 4. 索引边界

段落库存 24 段；注解覆盖 0–23，与库存 ID 列表逐项相等。`remaining=0` / 无 nextId，只相对本电子本 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `qingnang-jing:L0005-L0005` |
| 注解索引 23（止） | `qingnang-jing:L0641-L0816` |

电子本结构：前录上卷化始（L5）→ 中卷化机（L20）→ 下卷化成（L28）→ 分隔线后「青囊经。蒋大鸿注」（L34–35）→ 蒋注上/中/下三卷重录经文 + 注文至 L816。`remaining=0` ≠ 人工 verified / ≠ 影印校勘 / ≠ 产品交付 / ≠ 已接入八术页面。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/qingnang-jing/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（16 段）。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0005-L0005` | 序跋目录 / sr | 源 L5「第一節 上卷 化始」。仅卷题，无可执行判断 | 通过 |
| 2 | `L0009-L0009` | 理论 / sr | 一六/二七/三八/四九/五十；白话强调数对≠生日姓名断语；五行方位留给蒋注 | 通过 |
| 3 | `L0011-L0011` | 理论 / sr | 阖辟、五兆、八体、子母；notes 防字面套征兆/亲子 | 通过 |
| 4 | `L0013-L0013` | 理论 / sr | 天地定位等四组相对；「不相射」非现代物理；与后天九宫分表 | 通过 |
| 5 | `L0015-L0016` | 理论 / sr | 中五立极 + 阳以相阴；notes 洛书方位一北…九南与蒋注 L263–271 一致 | 通过 |
| 6 | `L0018-L0018` | 理论 / sr | 「此之謂化始」；形气相依，非命盘/房屋直接结论 | 通过 |
| 9 | `L0024-L0024` | 理论 / sr | 五星/五行、因形察气；「四七」「七政」；「太微南垣」；非历算替换 | 通过 |
| 10 | `L0026-L0026` | 理论 / sr | 阴阳相见 vs 相乘分说；形止气蓄；「鬼福及人」待校，不推现实后代 | 通过 |
| 13 | `L0032-L0032` | 理论 / sr | 理气形、乘风界水；顺五兆…布八门…因变北；八门≠时家奇门起局 | 通过 |
| 14 | `L0034-L0035` | 评注或元数据 / sr | 「青囊經。蔣大鴻注」；署名依电子文件，未以影印鉴定作者 | 通过 |
| 16 | `L0039-L0042` | 重复 / sr | 重录化始；闢闔/制临/纪网/宏/柔生始刚 vs 前录，不合并成两票 | 通过 |
| 17 | `L0044-L0420` | 理论 / sr | 河图生成数、先天相对/后天流行、洛书坎一…离九；「窃以为」图书同时是注者立场；有七必有六等疑点保留 | 通过 |
| 19 | `L0424-L0428` | 重复 / sr | 「太極南垣」「地之所盛」异字；关联前录 L24/L26 | 通过 |
| 20 | `L0430-L0635` | 理论 / sr | 因形察气；L460–464 缺接不可抽完整五星表；宿名疑字不改；葬骨感应非现实因果证明 | 通过 |
| 22 | `L0639-L0639` | 重复 / sr | 「气囿于地」「因变化」；与 L32 分录 | 通过 |
| 23 | `L0641-L0816` | 理论 / sr | 物物一太极；内气=外气止蓄；风/水须乘与界；布八门=八风开阖；非住宅/奇门/医学可运行算法 | 通过 |

锚定条件与源行（抽核，非转引进度表）：

- 上卷化始题：L5
- 一六共宗…五十同途：L9
- 太微南垣 / 太极南垣：L24 vs L425
- 气囿于形 / 因变北：L32
- 蒋大鸿注署：L35
- 柔生始刚 / 制临 / 纪网：L40–41
- 有七必有六：L88
- 洛书九宫方位与坎一…离九：L263–295
- 木岁星→中央/季夏/信：L460–464
- 角亢氏…奎娄胃昂…亢失娄鬼…氏女胃柳：L482–500
- 气囿于地 / 因变化：L639
- 乙太极 / 物物一太极：L658、L664
- 然此诸方之气 重复：L700–701
- 风原不能散 / 病在乎乘；水原不能止 / 妙在乎界：L759–764
- 布八门，以八风之开阖审气：L778–779

抽核未发现空模板白话、把再录异文覆盖前录、把蒋注升为无注经文、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本（L1–2 书题；L3–816 入段）。24 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/异字去向，不是影印逐字校勘，也不是风水断语有效证据，也不等于河图洛书/乘风界水已写入产品引擎。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是青囊经全书产品交付，也不覆盖生产侧 `docs/book-reviews/qingnang-jing.md`，更不冒充已接入八术页面。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified` 键缺失 | 24/24 无字段；无 true | 等价未升 verified。不回填 false 键 |
| 太微 vs 太极南垣 | L24 vs L425 | notes 已记。分版保留 |
| 气囿于形/地；因变北/变化 | L32 vs L639 | 分录。不擅自择一回写 |
| 柔生于刚 / 柔生始刚等 | L16 vs L41 | 异文账本。不统一 |
| L460–464 五星缺接 | 木岁星后接中央/季夏/信 | notes 已记。不抽完整方令德表 |
| 宿名字形 | 氏/氐、昂/昴、亢失、萁 等 | 不静默改正 |
| 「布八门」 | 蒋注=八风开阖 | 不得冒充时家奇门转布 |
| 葬骨 / 鬼福感应 | 注文立场 | 不升现实验证 |
| 与奥语/序 | 本书 slug=`qingnang-jing` | 本审查不覆盖另两书 |

## Caveat（不改注解，留给后续 pack）

1. **前录 / 蒋注重录异字不是已校定。** 太微/太极、形/地、变北/变化、柔生于刚/始刚等仍待底本。
2. **L460–464 五星条目缺接**；不得拼成完整五星方令德表驱动产品。
3. **宿名与「乙太极」「有七必有六」等疑字** 保留原字；合刊/他本只作对照，不静默覆盖。
4. **「布八门」=八风开阖**；与项目奇门八门算法同名不同义。
5. **既有 `qingnang-jing.md`** 为生产侧审读账本；本独立审查文件并存，不互相覆盖。

## 8. 交付

| 项 | 值 |
|---|---|
| Issue | MING-450 |
| 分支 | `codex/multica-ming-450` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/qingnang-jing-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；SR remaining 0 |

下一步：协调者快速核对证据后闭环；无需重做 0–23；无需回改注解。
