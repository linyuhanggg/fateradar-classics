# 兰台妙选 · 主本：独立审查 source-reviewed 全量（0–6 / 7）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-472` / 分支 `codex/multica-ming-472`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/lantai-miaoxuan.md`、未改 inventory / catalog / 引擎 / 产品仓。审查岗未参与该书生产。不要抢 MING-464–468 文件。本包只审注解文件索引 0–6（7 条，全量）。

结论：**通过。** `validate-annotations` `ok=true entries=7 source_reviewed=7 errors=[]`；`verified` 全为 `false`（7/7）；0 draft；起 `lantai-miaoxuan:L0003-L0007` 止 `lantai-miaoxuan:L0489-L0589`；注解与段落库存 7/7 ID 顺序全等。全书 7 段均对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-472`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/luming-nayin/lantai-miaoxuan.json
git rev-parse HEAD:references/annotations/luming-nayin/lantai-miaoxuan.json
git rev-parse origin/codex/multica-ming-329:references/annotations/luming-nayin/lantai-miaoxuan.json
shasum -a 256 sources/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `b56ecb0743742bd67634b32811b7f005322260bfd6d2b4becf5e98cc85da1e8c`（与 Issue 钉死一致） |
| 注解 blob | `677fbf31d8d7f84072a0a4fc776c9a28d1085dc6`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md`（589 行） |
| 源 SHA256 | `4505825efa8103ff63761b8d0f75e5ed62b39352db99f3a7428fdaaf8435d364` |
| Issue 对照路径 | `sources/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md` — **存在**；与 inventory `fulltext` 一致 |
| catalog `local_fulltext_path` | `references/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md` — **本树不存在**；本岗按 Issue/inventory 的 `sources/fulltext` 抽核 |
| 库存段落 | `references/inventory/paragraphs/luming-nayin/lantai-miaoxuan.json` 7 条，ID 顺序与注解全等 |
| 工作树相对基线 | 仅新增本审查稿；注解 JSON / 源文 / 既有 `lantai-miaoxuan.md` 无 diff |

catalog：`slug=lantai-miaoxuan`；`source_anchor_url` CTP 总页；`source_risk` 已提示现代整理 HTML 底本、未与明隆庆刻本/影印逐字校、Wikisource 591 卷目录/正文混排风险。`source_provenance_status` 属 consolidated catalog 口径。

无越权文件。注解未改。源文未改。未写产品仓。未碰 464–468 工作树或分支。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/lantai-miaoxuan.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 7, "source_reviewed": 7,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发（全部显式 `verified: false`）。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–6，7 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 7/7 |
| `review=draft` | 0 |
| `verified` | **7/7 均为 `false`**（无 true；无缺键） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 元数据段空 `notes` | 4/4（索引 0、1、3、5；结构合法） |
| 术文段非空 `notes` | 3/3（索引 2：4 条；4：3 条；6：3 条） |
| `terms` | 全非空（元数据各 2；上篇 6；中篇 4；下篇 4） |
| `relatedParagraphIds` | 全无 |
| kind | 评注或元数据 4、规则候选 3；与 inventory kind 逐条一致 |

Issue 钉死起 `lantai-miaoxuan:L0003-L0007`、止 `lantai-miaoxuan:L0489-L0589`：与文件索引 0、6 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/luming-nayin/lantai-miaoxuan.json` 7 段；注解 7 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory `id` 列表相同。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 索引 0（起） | `lantai-miaoxuan:L0003-L0007` | 来源说明（CTP 锚点 / 东里书斋底本 / 图书集成 591–592） |
| 索引 1 | `lantai-miaoxuan:L0011-L0012` | 上篇 URL + 琴堂/纳音分篇说明 |
| 索引 2 | `lantai-miaoxuan:L0014-L0410` | 上篇正文与夹注（约 397 非空行） |
| 索引 3 | `lantai-miaoxuan:L0414-L0415` | 中篇 URL + 恶煞疾病分篇说明 |
| 索引 4 | `lantai-miaoxuan:L0417-L0482` | 中篇正文与夹注 |
| 索引 5 | `lantai-miaoxuan:L0486-L0487` | 下篇 URL + 续论标签 |
| 索引 6（止） | `lantai-miaoxuan:L0489-L0589` | 下篇正文与夹注至电子末（含 2009 初校尾记） |

未入段行：L1 书题、`## 上/中/下篇` 标题与空行（L2/8–10/13/411–413/416/483–485/488）。非空未入段 4 行均为 Markdown 书题/篇题，不另造段落。本包后该书 SR 审查 remaining **0**。这只表示 7 主段都已有 source-reviewed 注解并经本岗全核，不是 589 行影印校勘，也不是 verified。

## 5. 全量语义核（7/7，对照原文）

原文取 `sources/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md` 的 `start_line–end_line`。元数据 4 段全文核读；三篇规则候选按 vernacular 条件组对照夹注，抽核关键取象、疑字去向与「不作预测/不升 verified」边界。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0007` | 评注 / SR | 源 L3 东里书斋底本 + CTP 锚点 + 图书集成 591/592；白话标明「写有权威锚点≠已逐字对照」 | 通过 |
| 1 | `L0011-L0012` | 评注 / SR | L11 donglishuzhai chapter/3764；L12「原出琴堂，此專以納音地支取象」；白话标为现代元数据非原赋格法 | 通过 |
| 2 | `L0014-L0410` | 规则候选 / SR | 34 组覆盖上篇：三命六旬（L17–20）→马化龙驹/蛇化青龙/宝剑冲牛斗/灵槎（L33–41）→兔入月宫/子归母腹/水遶花堤（L45–65）→三奇拱贵 vs 三奇逢德名称倒置（L127 vs L153）→凤舞顺风/破碎捲帘（L134–135）→贵人捧印墓库 vs 贵临印绶相生印（L144 vs L270）→水火旣濟「上者年月、下者日時」、否定干支当上下（L188–189）→年为本日为主（L191）→杨柳拖金/石榴喷火（L196–200）→五星朝北明文非实星、万派流东虚拱卯（L405–408）。疑字与脚注 1–11 记入 notes，不改源 | 通过 |
| 3 | `L0414-L0415` | 评注 / SR | L414 URL chapter/3765；L415 专论恶煞疾病夭折贫愚；白话不升疾病诊断 | 通过 |
| 4 | `L0417-L0482` | 规则候选 / SR | 13 组覆盖中篇：鬼人鬼物/悬针（L422–425）→白虎衔尸/元武披发→阴鬼蹑足相克链→飞廉月表「二、六、十、三、七、十一，卯」黏连缺项（L479）→己未太阴水与上篇天上火张力（L462–463）→黑煞/枭神收束。刑伤、自残、性行为等断语均标为书中取象 | 通过 |
| 5 | `L0486-L0487` | 评注 / SR | L486 URL chapter/3766；L487 纳音/三元四柱续论标签；白话声明正文从下一主段起 | 通过 |
| 6 | `L0489-L0589` | 规则候选 / SR | 13 组覆盖下篇：日轮当表/画桥/桃花滚浪（L492–496）→一德昇天与重复季月注（L505–512）→「金运」疑金莲（L537–538）→正格破空「无破则一生迍邅」否定疑义（L560–561）→脚注 20/21/23 图书集成所无（L576）→2009 初校尾记（L589）。不把编辑层当各本共有原文 | 通过 |

锚定抽核（非转引进度表）：

- 来源说明东里书斋 / 591–592：L3–L7
- 上篇琴堂纳音：L12；正文起「蘭臺妙選一 / 上篇」：L14–L16
- 三命天地元人元 / 六旬：L17–L20
- 宝剑冲于牛斗（源用「冲」）：L37；灵槎入天河：L41
- 水遶花堤（源用「遶」）：L65；藏珠渊海甲子乙丑珠：L69–L72
- 三奇拱贵乙丙丁天上 / 三奇逢德甲戊庚天上：L127、L153
- 水火旣濟上年月下日时：L188–L189；年为本日为主：L191
- 五星朝北「卽非五星」：L406
- 中篇飞廉月表：L479；己未太阴水：L463
- 下篇金运脚注 16：L537–L538；正格破空：L560–L561；图书集成无注声明：L576；2009 初校：L589

抽核未发现空模板白话、静默改正文、把纳音取象升实证预测、把现代分篇 URL 当原赋、或把 `verified` 置 true。元数据空 notes 合理；三篇术文 notes 与疑点对应。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本为东里书斋三篇 HTML 抽取，夹注与正文混排；CTP 与图书集成卷次仅作锚点/线索。7 条升 `source-reviewed` 只表示对照电子段落实了层次、条件、疑字去向与「书中判断≠现实证据」边界，不是明隆庆刻本或影印逐字校勘，也不是格局断语有效证据，也不等于纳音/三奇/神煞已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是兰台妙选产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified: false` | 7/7 | 保持。不升 true |
| 三奇天地名称前后倒置 | L127 vs L153 | notes 已记；不统一改字 |
| 日月分秀日昼月夜 vs 戊午得亥子丑 | 上篇 notes | 保留张力 |
| 己未上篇天上火 / 中篇太阴水 | L462–463 vs 上篇月象 | 不默换纳音 |
| 飞廉月表二六十支位黏连 | L479 | 不从通行表补齐 |
| 正格破空「无破则一生迍邅」 | L561 | 记否定疑义；不建无破也凶规则 |
| 「金运」疑「金莲」；戊辰疑戊戌 | 脚注 16–17 | 不擅改 |
| 脚注 20/21/23 图书集成所无 | L576 | 未外部复核；不当各本一致 |
| catalog `references/fulltext` 路径本树缺失 | 蒸馏包路径 | 本岗只核 Issue/inventory 的 `sources/fulltext` |
| 未入段 Markdown 书题/篇题 | L1、L9、L412、L484 | 不另造段；remaining=0 仅相对 7 主段 |
| 既有生产审读稿 `lantai-miaoxuan.md` | 存在 | 本岗只读不覆盖 |

## 8. 交付边界

- 本 Issue 写出：仅 `docs/book-reviews/lantai-miaoxuan-independent-review.md`
- 远端：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-472`
- 基线：`6effd8e4f951fd17e1b1e0454942946ebc765da9`
- 注解 SHA256：`b56ecb0743742bd67634b32811b7f005322260bfd6d2b4becf5e98cc85da1e8c`
- 本包后 remaining：**0**
- 不宣称产品交付、不宣称人工 verified、不 main 合并、不部署
