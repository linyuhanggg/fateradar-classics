# 李虚中命书 · 主本：独立审查 source-reviewed 全量（0–7 / 8）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-473` / 分支 `codex/multica-ming-473`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / executable、未抢 MING-464–472 文件、未改他书 / 引擎 / 产品仓。本岗未参与该书生产。不要与识典 SK1601 另版、子平日主十神表或奇门三奇表混为一源。本包只审注解文件索引 0–7（8 条，全量）。

结论：**通过。** 结构校验 `ok=true entries=8 source_reviewed=8 errors=[]`；`verified` 全为 `false`（8/8）；0 draft；起 `li-xuzhong-mingshu:L0003-L0011` 止 `li-xuzhong-mingshu:L0187-L0242`；注解与段落库存 8/8 ID 顺序全等。全书 8 段均对照电子原文抽核成立；三长卷 subsections 66+23+31=**120**，父段行号全覆盖、无空白 vern、无越出父段；卷上 60 甲子标题与六十循环全等且柱名均落在所标行。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本 8 主段 SR 审查覆盖。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-473`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/luming-nayin/li-xuzhong-mingshu.json
git rev-parse HEAD:references/annotations/luming-nayin/li-xuzhong-mingshu.json
shasum -a 256 sources/fulltext/luming-nayin/li-xuzhong-mingshu/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解文件 SHA256 | `dcd13e160fe203258b95701006a9616cf17ae3681ab309e6977311b0964c4dc2`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `36f6bb64363c6d9f0beee4ef9336791b22959bc4` |
| 实际源文 | `sources/fulltext/luming-nayin/li-xuzhong-mingshu/fulltext.md`（242 行） |
| 源 SHA256 | `fbd630e9c4a46e300d77832ede94ec58e12df9c382e40ab044f75ad3641d9d31` |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / inventory 无 diff |

对照路径：Issue 写 `sources/fulltext/luming-nayin/li-xuzhong-mingshu/fulltext.md`，与 inventory `fulltext` 字段一致。catalog 另记 `references/fulltext/...` 与不同 SHA（`0e449020…`），属蒸馏包路径；本岗按 inventory / Issue 钉死的 `sources/fulltext` 抽核，不另造副本。

catalog：`slug=li-xuzhong-mingshu`；`title=李虚中命书`；`source_anchor_url` CTP wiki `res=390795`；`source_risk` 已提示四庫本正文与注文混排；`source_provenance_status=consolidated_catalog`。生产侧注解最后触及提交为 `9118a78`（MING-324 记录），本岗未参与该书生产。

无越权文件。注解未改。源文未改。未写产品仓。未碰 464–472 工作树或分支。未采用识典 SK1601 替文。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/li-xuzhong-mingshu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 8, "source_reviewed": 8,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发（全部显式 `verified: false`）。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–7，8 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 8/8 |
| `review=draft` | 0 |
| `verified` | **8/8 均为 `false`**（无 true；无缺键） |
| 空白白话 | 0（父段与 120 子节 vern 均非空） |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 元数据段空 `terms` / 空 `notes` | 索引 2/4/6（三处丛书题署）空 terms+notes；结构合法 |
| `relatedParagraphIds` | 全无 |
| 额外键 | 有 `subsections`（仅 3 条长卷：66+23+31=120；标题均嵌回父段 `vernacular` 的 `【…】`） |

kind 分布（注解）：序跋目录 5、规则候选 1、理论 2。inventory kind 与注解 kind **8/8 一致**（无 inventory 初筛冲突需记账处）。

Issue 钉死起 `li-xuzhong-mingshu:L0003-L0011`、止 `li-xuzhong-mingshu:L0187-L0242`：与文件索引 0、7 一致。

## 4. 索引边界与 inventory

`references/inventory/paragraphs/luming-nayin/li-xuzhong-mingshu.json` 8 段；注解 8 条。`ann_not_in_inv=0`，`inv_not_in_ann=0`；文件顺序与 inventory `id` 列表相同。

| 位置 | 实测 ID | kind | 说明 |
|---|---|---|---|
| 索引 0（起） | `li-xuzhong-mingshu:L0003-L0011` | 序跋目录 | 四庫提要：托名/著录参差/唐旧宋增 |
| 索引 1 | `li-xuzhong-mingshu:L0013-L0015` | 序跋目录 | 原序 + 馆臣「元和称载」辨伪 |
| 索引 2 | `li-xuzhong-mingshu:L0017-L0017` | 序跋目录 | 丛书题署 |
| 索引 3 | `li-xuzhong-mingshu:L0021-L0085` | 规则候选 | 卷上：60 甲子纳音 + 贵人分层 |
| 索引 4 | `li-xuzhong-mingshu:L0087-L0087` | 序跋目录 | 卷上后丛书题署 |
| 索引 5 | `li-xuzhong-mingshu:L0091-L0181` | 理论 | 卷中：通理→三元四柱→25 多寡→清浊 |
| 索引 6 | `li-xuzhong-mingshu:L0183-L0183` | 序跋目录 | 卷中后丛书题署 |
| 索引 7（止） | `li-xuzhong-mingshu:L0187-L0242` | 理论 | 卷下：衰旺亲属→九限→合德秀合→水土存疑 |

未入段行主要为卷题（`### 李虛中命書卷上/中/下`）与空行，与 8 稳定段口径一致。同文件内多柱共行（如 L26 己巳+庚午）属源文排版，子节共享起止行**不是**越界或漏覆盖。本包后该书 SR 审查 remaining **0**。这只表示 8 主段都已有 source-reviewed 注解并经本岗全核，不是 242 行逐句影印校勘，也不是 verified。

## 5. 全量语义核（8/8，对照原文）

原文取 `sources/fulltext/luming-nayin/li-xuzhong-mingshu/fulltext.md`。元数据段全文核读；三长卷按全部 vernacular 小节标题行锚核对起止原文，并抽核纳音/正气分层、四柱定义、九限反例、合支异字与「不作预测/不升 verified」边界。120 处小节行锚，**0** 处越出所属 paragraphId；父段行集合被子节并集全覆盖。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0011` | 序跋 / SR | 提要：鬼谷撰李注、唐志无书、宋志卷数参差、永乐大典厘三卷；前部六十甲子不及生时近韩志，后半四柱与宋官称后出 → 真伪夹杂。白话分层正确，不把全书归唐李虚中一人 | 通过 |
| 1 | `L0013-L0015` | 序跋 / SR | 原序元和初载 + 案语天宝至德称载、元和称载即作伪证。传说与辨伪两层分开 | 通过 |
| 2 | `L0017-L0017` | 序跋 / SR | `欽定四庫全書` 题署一行；白话短注合法 | 通过 |
| 3 | `L0021-L0085` | 规则 / SR | 66 节：甲子→癸亥 60 柱标题=六十循环且柱名均在所标行；总论轻重；本家贵人+「丙寅火得酉」反问；贵神优劣表；干合支合/紫虚；贵合贵食。戊辰「忌火金」又「养于金」、丙午纳音水、壬子纳音木、癸巳喜音中无土、乙卯喜土清等与原文一致；夹注分层保留，不改成日主十神喜忌表 | 通过 |
| 4 | `L0087-L0087` | 序跋 / SR | 卷上后丛书题署 | 通过 |
| 5 | `L0091-L0181` | 理论 / SR | 23 节：通理物化→乾坤数→真运→纳音起数/变体→干禄驿马分层→三元（干禄/支命/纳音身）→四柱胎月日時与「年本日主」两层并存→轻重得时→水火木金土五本×多寡→禄马食煞→空亡源末→真假→夫妇非六合→升降清浊；敏少宰/王安中官称落在 L172–173，作后世层线索。不把日主升成现代八字唯一中心 | 通过 |
| 6 | `L0183-L0183` | 序跋 / SR | 卷中后丛书题署 | 通过 |
| 7 | `L0187-L0242` | 理论 / SR | 31 节：衰旺季节→父母妻子/节气→不利与可用条件→五种三奇（非奇门乙丙丁单表）→诸合魁罡→伤迟速→大运小运气运（甲巳土运等明文「國家運祚」）→九限具名（破碎「非死限」、布素十年可有五年吉）→天承地禄 30 合德→秀合（保留庚申乙酉）→神头正气（丙午火/壬子水，不得回改卷上纳音）→十二将（乙未太常 vs 卷上己未火神头表述不一，不擅订）→水土名用「未可究其指…待来者」 | 通过 |

锚定抽核（非转引进度表）：

- 提要「唐書藝文志亦無是書」/「後半乃多稱四柱」/宋职官：L5–8
- 原序「元和初載」+「作偽之一證」：L15
- 卷上甲子金、戊辰木忌火金又养于金、丙午「至陰之水」、壬子「體柔用剛之木」：L21、L25、L55、L60
- 「丙寅火得酉則火至此焉足為貴」：L74
- 贵合贵食：L83–85
- 三元干禄支命纳音身：L122–123
- 四柱「胎月日時」与「年為本則日為主」：L125、L128
- 敏少宰 / 王安中：L172–173
- 國家運祚（甲巳土運文）：L217
- 破碎限非死限 / 布素五年：L221–222
- 庚申乙酉秀合：L232
- 神头正气壬子水、丙午火：L234–235；乙未土为太常：L237
- 水土「未可究其指故存之以待來者」：L242；电子末行 L242

抽核未发现空模板白话、静默改正文（如把庚申乙酉改乙巳）、把书内取象升实证预测、把纳音层与神头正气层互相覆盖、或把 `verified` 置 true。短元数据 3 段空 terms/notes 合理；三长卷 notes 非空且与疑点对应。

## 6. source-reviewed ≠ 人工 verified

现存电子主文本为四庫本平铺（CTP/本地 sources），正文与夹注混排，馆臣已明言唐旧与宋以后阑入并存。8 条升 `source-reviewed` 只表示对照电子段落实了层次/条件/反例/疑字去向，不是影印逐字校勘，也不是命理断语有效证据，也不等于纳音喜忌/三元九限/合德已写入产品引擎或八术页面。0 条 draft 不等于 0 条疑点。不得把本包写成已人工 verified。本包不是李虚中命书产品交付，更不冒充已接入八术页面。不要与识典 SK1601 另版混为同一文字层。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified: false` | 8/8 | 保持。不升 true |
| 馆臣辨伪 / 唐旧宋增 | 提要+原序案语已分层 | 不回改源结构；不把全书归一人一时 |
| 戊辰忌金又养于金；贵合例与先述贵支不一 | 注解 notes 已标 | 保留；不静默改例 |
| 纳音（丙午水/壬子木）≠ 神头正气（丙午火/壬子水） | 卷上 vs L234–235 | 两层并存；后文不得覆盖前文 |
| 四柱胎月日時 vs 年本日主 | L125–128 | 两层保留；不改成唯一现代年月日時表 |
| 甲巳土运等为国家运祚 | L217 | 不作个人气运出口 |
| 破碎非死限；布素可有五年吉 | L221–222 | 反例保留 |
| 庚申乙酉 / 乙未太常 vs 己未神头 | L232、L237 vs L66 | 原字保留；不擅订正 |
| 水土「未可究其指」 | L242 | 不补现代土长生唯一算法 |
| catalog `references/fulltext` SHA ≠ `sources/fulltext` | 蒸馏包 vs 权威源路径 | 本岗只核 Issue/inventory 的 `sources/fulltext` |
| 同文件多柱共行 | 源文排版（如 L26） | 子节共享行号合法；覆盖仍全 |

## 8. 交包边界

- 写出：仅 `docs/book-reviews/li-xuzhong-mingshu-independent-review.md`
- 未改：`references/annotations/luming-nayin/li-xuzhong-mingshu.json` 及任何源文 / inventory / catalog
- 远端：`linyuhanggg/fateradar-classics` 分支 `codex/multica-ming-473`
- 本包后该书主本 SR 独立审查 remaining **0**
- 下一步：协调核对本报告与 SHA；不派重写；不因本包升 verified
