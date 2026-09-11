# 卜筮正宗 · 主本：独立审查 source-reviewed 全量（0–8 / 9）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-467` / 分支 `codex/multica-ming-467`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / executable / `references/books/divination/bushi-zhengzong/*`、未抢 MING-458–464、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不要与《增删卜易》混淆（凡例仅列书名，另有独立 slug）。本包只审注解文件索引 0–8（9 条，全量）。

结论：**通过。** 结构校验 `ok=true entries=9 source_reviewed=9 errors=[]`；`verified` 全为 `false`（9/9 显式键）；0 draft；起 `bushi-zhengzong:L0003-L0004` 止 `bushi-zhengzong:L3471-L4448`；注解与段落库存 9/9 ID 顺序全等。全书 9 段均对照电子原文核读成立；四正文 vernacular / subsections 小节数 **80 / 83 / 72 / 50** 共 **285**，与 scopeNote「正文分80/83/72/50节」一致，小节行锚全部落在所属 paragraphId 范围内且无空隙、无越界、无非空未覆盖行。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。卜筮进入知识检索，不冒称六爻引擎 / 八术页面已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-467`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/divination/bushi-zhengzong.json
git rev-parse HEAD:references/annotations/divination/bushi-zhengzong.json
git rev-parse origin/codex/multica-ming-329:references/annotations/divination/bushi-zhengzong.json
shasum -a 256 sources/fulltext/divination/bushi-zhengzong/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `d68c8870215d52c4ccc455379fa050d86fb47344f4a8f14785bb3d6bf70d4612`（与 Issue 钉死一致） |
| 注解 blob @ HEAD / origin/329 | `25bcd694bbe3868f8caff20b80161dbf14290382`（同） |
| 实际源文 | `sources/fulltext/divination/bushi-zhengzong/fulltext.md`（4448 行） |
| 源 SHA256 | `c1778106eaf4f8515f56601d4cad6ecc147523112ae70e56ac7c49078046a8a7` |
| 库存段落 | `references/inventory/paragraphs/divination/bushi-zhengzong.json` 9 条，ID 顺序与注解全等 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / inventory 无 diff |

对照路径：Issue 写 `sources/fulltext/divination/bushi-zhengzong/fulltext.md`，路径存在且与 inventory 一致。

catalog：`slug=bushi-zhengzong`；`source_anchor_url` CTP《卜筮正宗》总页；`source_provenance_status=consolidated_catalog`；`source_risk` 已提示 CTP OCR/截断异文须与影印 PDF 校，以及疾病、寿命、官讼、失踪等占断须安全改写。catalog.notes 另记章首乱码、十八论缺段、重录、案例数与目录不符——与本审查抽核一致。

无越权文件。注解未改。源文未改。未写产品仓。未碰 458–464 工作树或分支。未碰 `zengshan-buyi` 注解。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/bushi-zhengzong.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 9, "source_reviewed": 9,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–8，9 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 9/9 |
| `review=draft` | 0 |
| `verified` | **9/9 显式 `false`**（无一 `true`） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| `notes` 空（元数据段） | 5（索引 0/1/3/5/7，结构合法） |
| 空 `terms` | 5（同上元数据段） |
| 正文 subsections | 80+83+72+50=285；行锚无越界、无重叠、无非空未覆盖 |
| scopeNote | 四 CTP 现有文字 SR；识典 627 补充段未随之提升；乱码/缺段/重录/题盘矛盾保留 |

kind 分布：评注或元数据 5、理论 4。

Issue 钉死「verified 全 false」：本文件显式 `verified: false`，与「不得升人工 verified」一致。

Issue 钉死起 `bushi-zhengzong:L0003-L0004`、止 `bushi-zhengzong:L3471-L4448`：与文件索引 0、8 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/divination/bushi-zhengzong.json` 9 段；注解 9 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory 相同。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `bushi-zhengzong:L0003-L0004` |
| 1 | `bushi-zhengzong:L0008-L0009` |
| 2 | `bushi-zhengzong:L0011-L1178` |
| 3 | `bushi-zhengzong:L1182-L1183` |
| 4 | `bushi-zhengzong:L1185-L2281` |
| 5 | `bushi-zhengzong:L2285-L2286` |
| 6 | `bushi-zhengzong:L2288-L3464` |
| 7 | `bushi-zhengzong:L3468-L3469` |
| 注解索引 8（止） | `bushi-zhengzong:L3471-L4448` |

电子本结构：标题 → CTP 采集 front matter（L3–4）→ 四章交替「章节 URL/行范围元数据 + 正文」；章界 L1179–1181 / L2282–2284 / L3465–3467。`remaining=0` ≠ 人工 verified / ≠ 影印校勘 / ≠ 产品交付 / ≠ 已接入八术页面。

## 5. 全书语义（9/9 对照原文，不凭进度摘要）

原文取 `sources/fulltext/divination/bushi-zhengzong/fulltext.md` 的 `start_line–end_line`。元数据 5 段全文核读；四正文段按 subsections 全覆盖，并对乱码、缺段、重录、案例数、试问等关键点抽核。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0004` | 评注或元数据 / sr | 源 L3–4：CTP Wiki 四章节抽取说明与 part/local/global 行号保留。白话正确标为现代采集说明，非原书卷次证明 | 通过 |
| 1 | `L0008-L0009` | 评注或元数据 / sr | 源 L8–9：chapter=889452 URL；`global 1-958; local rows 958`。采集行号 ≠ Markdown 物理行号，白话已区分 | 通过 |
| 2 | `L0011-L1178` | 理论 / sr | 80 小节。见下锚定；题署王洪绪、凡例飞伏异议、纳音/装卦表、飞伏定例至用神问答；末「原忌仇神论第四 / 凡占卦」跨章 | 通过 |
| 3 | `L1182-L1183` | 评注或元数据 / sr | 源 L1182–1183：chapter=801184；`global 959-1787; local rows 829`。白话标明续文有乱码、采集齐≠文句齐 | 通过 |
| 4 | `L1185-L2281` | 理论 / sr | 83 小节。首行乱码承接原忌仇；十八论第十一后见第十六；黄金策辑录层；学馆篇末跨章 | 通过 |
| 5 | `L2285-L2286` | 评注或元数据 / sr | 源 L2285–2286：chapter=944578；`global 1788-2781; local rows 994` | 通过 |
| 6 | `L2288-L3464` | 理论 / sr | 72 小节。学馆续乱码；词讼/十八问案例；第二问 11 例 vs 目录 16、第七问 13 vs 14；第八问后两盘跨第 4 章 | 通过 |
| 7 | `L3468-L3469` | 评注或元数据 / sr | 源 L3468–3469：chapter=909268；`global 2782-3472; local rows 691` | 通过 |
| 8 | `L3471-L4448` | 理论 / sr | 50 小节。第八问续表→第十八问；损/无妄已知结果试问分类；末例母病/父使子占问意更正。读至 L4448 | 通过 |

锚定条件与源行（抽核，非转引进度表）：

**Part 1 / 索引 2**

- 题署王洪绪辑、先天秘旨：L11
- 凡例反对乾坤来往 / 爻爻有飞伏旧说：L15
- 凡例列《增删卜易》等书名（≠ 本书 slug）：L16–20
- 目录「第二问…十六卦」后紧接「第二问生用神…四卦」（目录第三问误标第二问）：L66–67
- 纳音歌：L140；三钱起卦：L204
- 装卦表「天风垢」「风天少畜」原字：L218、L254
- 飞伏定例起：L560；变爻有用不再寻伏：L1137 一带
- 原忌仇论第四 +「凡占卦」跨页：L1177–1178

**Part 2 / 索引 4**

- 章首乱码：L1185；续文「弱，或伏藏…」：L1186
- 飞神正论第五：L1195；旬空论第十：L1232；反吟定例第十一：L1234；绝处逄生…论第十六：L1241（缺第十二至十五完整篇）
- 黄金策总断千金赋直解：L1610
- 学馆篇末「两福自冲，鬼谷值」断句：L2281

**Part 3 / 索引 6**

- 章首乱码：L2288；词讼：L2295
- 第一问–第八问题干：L2732、L2790、L2897、L3421 等
- 第八问后两盘仅题/表头：L3459–3464

**Part 4 / 索引 8**

- 续表「伏」起：L3471；第九问：L3516；第十二问：L3836；第十八问：L4371
- 损/无妄已知结果试问：约 L3930–3948（注解 S021）
- 全书末母病流年与父使子占问意更正：L4447–4448

抽核未发现空模板白话、静默把「垢」改「姤」或「少畜」改「小畜」进引文、把章首乱码补成完整论、把目录案例数当正文已审数、把已知结果试问混计盲测成功、或把 `verified` 置 true。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本为 CTP 四章节 Wiki 抽取（4448 行）。9 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/异字与残缺去向，不是影印逐字校勘，也不是六爻断语有效证据，也不等于飞伏/纳甲/月破已写入产品引擎。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是卜筮正宗全书产品交付，也不覆盖 `zengshan-buyi`，更不冒充已接入八术页面。识典 627 补充段未随本包提升。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified: false` | 9/9 显式 | 保持。不升 true |
| 章首乱码 L1185 / L2288 | 原文乱码字节仍在 | notes/白话已记。不猜补 |
| 十八论第十一→第十六 | L1234 后 L1241 | 缺第十二至十五；不称十八论齐全 |
| 「垢」「少畜」原字 | L218 / L254 | 检索可映射；不改引文 |
| 目录案例数 vs 正文 | 第二问 16→11；第七问 14→13 | 按实记；不补盘 |
| 黄金策辑录层 | Part2 起 L1610 等 | 与独立 `huangjin-ce` 同文不计双证 |
| 重录块 | 求名/仕宦/求财、词讼、避乱等 | 保留原位；不计独立支持 |
| 损/无妄试问 | 第十二问内 | 分类为已知结果试问，非前瞻 |
| 月破「当前作用」措辞 | 专论与后例 | notes 已标前后不一；待案例，不改文 |
| 与《增删卜易》 | 凡例仅列书名 | 本审查不覆盖 `zengshan-buyi` |
| 鹰注分层 | Part2 括注 | 不与王氏正文混同 |

## Caveat（不改注解，留给后续 pack）

1. **CTP 章首乱码与跨页残句** 未校复；不得静默补全原忌仇论或学馆断句。
2. **十八论正文缺第十二至十五**；不得拼成完整十八论驱动产品。
3. **多栏装卦/藏干/合冲表展平** 列界不清处不得生成替换运行表。
4. **目录卦例数与正文题盘数不符**；不得按目录补造案例。
5. **黄金策与重录块** 不计独立证据；已知结果试问、事后改释、问意更正须分类。
6. **疾病/寿命/官讼/风水后验** 只作文本释义，不作诊治、命运或风水因果证据。
7. **维基/CTP 电子本** 不能证明与某影印底本一致；source-reviewed ≠ 人工 verified。
8. **卜筮知识包 ≠ 八术页面交付**；不得宣称 FateRadar WebUI / 六爻引擎已消费本书。
9. **不要与增删卜易混淆**；本书 slug=`bushi-zhengzong`。

## 交付边界

- 写出：仅 `docs/book-reviews/bushi-zhengzong-independent-review.md`
- 禁止：改注解 JSON / 源文 / inventory / 他书审查 / main 合并 / 部署 / force push
- 推送：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-467`
- remaining 本包后：**0**（相对本电子本 9 段 SR 覆盖）
