# 《增删卜易》主本：独立审查 CP11（3000–3124 收口）

审查对象：`origin/codex/full-library-completion` @ `bc798566da77c30e149abf9673c88ecc386702b2`。工作树只读参考本 SHA，本岗写出仅本文件。未改注解 JSON、未改源文、未改引擎 / `chart.*` / golden / 他书。不是《增删卜易》全书人工 verified，不是续写 3000–3124，不是引擎包，也不是全项目完成。MING-224…MING-273 已审 0–2699，MING-276 已审 CP10（2700–2999）；本岗未抢写 `zengshan-buyi-cp9-review.md` / `zengshan-buyi-cp10-review.md`，勿重做。

结论：**通过。** 结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。错位卷一尾段重复互链、应期/生旺墓绝候选、李我平评注层、全图读法注、八宫静图疑字保留等均标清，未冒充野鹤原典通则。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–2999 相对权威 SHA / CP1–CP10 对象未改。本包后本 edition 索引 remaining **0**（3125/3125 均已 source-reviewed 且 CP1–CP11 独立审查覆盖）；仍不是人工 verified，不是影印校勘。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-279`，2026-09-11）：

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
| 本岗基线 HEAD / `origin/codex/full-library-completion` | `bc798566da77c30e149abf9673c88ecc386702b2`（`rev-parse` 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `8acccbd8511fe63564087159f4e61bacd7ab9f9ada270d1c8ed2339af6ad750f`（与 Issue 钉死值一致） |
| 注解 blob | `205a55ba0548603cd15f0ae921713b10a2eca99a` |
| 源 `fulltext.md` SHA256 | `90876203ab27a69da13e615bca83c031bf961ece3c2b3794e892340195c97e65` |
| 源 blob | `8b9cac56c3739b9f3cb3c9e824bd4678d7c34b97` |
| `scopeNote` | 3125 段全处理；source-reviewed 只对照电子文字；卷一正文错位于 L6504–7730；卷首/原剑为现代层 |
| 本包索引 | 3000–3124；未改 0–2999 |
| CP9 / CP10 写出文件 | 本树不存在 `zengshan-buyi-cp9-review.md` / `zengshan-buyi-cp10-review.md`；未抢写 |

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

本包 CP11（3000–3124）kind：重复 50 / 序跋目录 24 / 操作步骤 24 / 案例 8 / 术语 8 / 理论 4 / 规则候选 4 / 评注或元数据 3。

`diagramTranscription` 0（本包无图行字面转录字段；八宫静图以 `操作步骤` 排爻）。`relatedParagraphIds` 50（均为 `kind=重复` 互链 `wikisource-volume1`）。

空 vernacular 0；空 notes（`[]`）64（全非图行：序跋目录 24 / 操作步骤 17 / 案例 8 / 术语 8 / 理论 3 / 评注或元数据 2 / 规则候选 2）；空 terms 0。无「本段论述 / 白话从略 / 见原文 / TODO / 待补」类空模板。vernacular 长度 min 9 / 中位 30 / max 89。最短若干为八宫「下一图…」转题短句（如 `L7812`「下一图是讼与同人。」）与宫五行标签（如 `L7792`「离宫以火为六亲基准。」）。`kind=重复` 50 条 notes 均含错位附入说明并互链 `wikisource-volume1`，不计新增独立规则。

## 4. 索引边界与 CP1–CP10 未改

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 注解索引 0（CP1 起，本包只核未改） | `zengshan-buyi:L0007-L0007` | 与权威 SHA / MING-224…276 同 blob |
| 注解索引 299（CP1 止） | `zengshan-buyi:L0934-L0934` | 同上 |
| 注解索引 300（CP2 起） | `zengshan-buyi:L0936-L0936` | 同上 |
| 注解索引 599（CP2 止） | `zengshan-buyi:L1593-L1593` | 同上 |
| 注解索引 600（CP3 起） | `zengshan-buyi:L1595-L1595` | 同上 |
| 注解索引 899（CP3 止） | `zengshan-buyi:L2255-L2255` | 同上 |
| 注解索引 900（CP4 起） | `zengshan-buyi:L2257-L2257` | 同上 |
| 注解索引 1199（CP4 止） | `zengshan-buyi:L2878-L2878` | 同上 |
| 注解索引 1200（CP5 起） | `zengshan-buyi:L2880-L2880` | 同上 |
| 注解索引 1499（CP5 止） | `zengshan-buyi:L3572-L3572` | 同上 |
| 注解索引 1500（CP6 起） | `zengshan-buyi:L3574-L3574` | 同上 |
| 注解索引 1799（CP6 止） | `zengshan-buyi:L4221-L4221` | 同上 |
| 注解索引 1800（CP7 起） | `zengshan-buyi:L4223-L4223` | 同上 |
| 注解索引 2099（CP7 止） | `zengshan-buyi:L4860-L4860` | 同上 |
| 注解索引 2100（CP8 起） | `zengshan-buyi:L4862-L4862` | 同上 |
| 注解索引 2399（CP8 止） | `zengshan-buyi:L5531-L5531` | 同上 |
| 注解索引 2400（CP9 起，本包只核未改） | `zengshan-buyi:L5533-L5533` | 同上 |
| 注解索引 2699（CP9 止） | `zengshan-buyi:L6269-L6269` | 同上 |
| 注解索引 2700（CP10 起，本包只核未改） | `zengshan-buyi:L6271-L6271` | 同上 |
| 注解索引 2999（CP10 止） | `zengshan-buyi:L7448-L7448` | 同上 |
| 注解索引 3000（本包起） | `zengshan-buyi:L7450-L7455` | 错位卷一家人图续 |
| 注解索引 3124（本包止 / edition 末） | `zengshan-buyi:L7959-L7964` | 坤宫需/比静图收口 |

起始/止点与 Issue 钉死 ID 一致。本包后 remaining **0**。

**CP1–CP10 未改核验：** 本树注解 SHA256 与 `bc798566…` blob、MING-273 / MING-276 工作树注解文件相同（`8acccbd8…`）；`entries[0:3000]` 与两棵已审树深比较 `identical=True`（全书 entries 亦 identical）。未重做 0–2999；未改写 CP9/CP10 审查文件。

本包覆盖：错位卷一尾（家人/痘例/反伏/空亡/生旺墓绝/应期总表，至 `L7730`）→ 全图读法注 → 八宫静图装卦（乾…坤游归魂，至 `L7959–7964`）。真正错位卷一正文区止于 `L7730`（与 `scopeNote` 一致）；其后为全图教学层，不是新卷新规则。

## 5. 抽样语义（≥15 非模板，对照原文，不凭既有全书报告）

原文取 `sources/fulltext/divination/zengshan-buyi/fulltext.md` 的 `start_line–end_line`。下列为错位卷一尾、评注层、规则候选、全图疑字抽核。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 3000 | `L7450-L7455` | 重复 / sr | 家人四五动变离图行；互链 wikisource；不计新例 | 通过 |
| 3004 / 3010 | `L7463` / `L7485` | 案例 / sr | 女痘坤师日期疑字保留；卯父动化子回生、李我平反酉冲散一律 | 通过 |
| 3015 / 3018 | `L7495–7506` / `L7512` | 理论 / sr | 离坎/震兑整体回克；九月丁亥≠冬月已限；外观内静教学例 | 通过 |
| 3021 / 3030 | `L7518–7531` / `L7583` | 重复+评注 / sr | 反伏分题用旺；李我平对比比井/临中孚，反吟须看用 | 通过 |
| 3035 / 3041 | `L7598` / `L7620` | 案例 / sr | 求财家人贲、远行大畜；重载占例 | 通过 |
| 3050 / 3052 | `L7651` / `L7655` | 规则候选 / sr | 金巳酉丑寅；土水同申子辰巳；禁与八字十二运混算 | 通过 |
| 3058 / 3061 | `L7681–7687` / `L7700–7718` | 评注+规则 / sr | 土长生流派引述与「万古不易」立场；应期条件总表非唯一日期 | 通过 |
| 3067 / 3068 | `L7730` / `L7732` | 理论+评注 / sr | 游归魂仍以用神为主；全图装卦注为读图说明 | 通过 |
| 3071 / 3078 | `L7738–7743` / `L7767–7772` | 操作 / sr | 乾姤遁；兑困萃；辰士/来土/困初卯疑字保留不静默校 | 通过 |
| 3092 / 3094 | `L7825–7830` / `L7834–7839` | 操作 / sr | 震豫解；恒升井；士/妻则疑字 notes 已限 | 通过 |
| 3110 / 3122 / 3124 | `L7901–7906` / `L7950–7955` / `L7959–7964` | 操作 / sr | 「官鬼五上」损坏不替；夬缺符不补；需比收口 | 通过 |

关键条件与源行（抽核，非转引既有全书报告）：

- 错位重复 / 痘财例：`L7450–7455`、`L7463`、`L7485`、`L7598`、`L7620`
- 回克 / 反伏 / 评注：`L7495–7506`、`L7512`、`L7518–7531`、`L7583`
- 生旺墓绝 / 应期：`L7651`、`L7655`、`L7681–7687`、`L7700–7718`
- 错位终界 / 全图：`L7730`、`L7732`、`L7738–7743`、`L7767–7772`、`L7825–7839`、`L7901–7906`、`L7950–7964`

## 6. 评语层 ≠ 野鹤原典

Issue 要求：录入者评语不得当成野鹤原典。本包李我平评注、全图读法注、疑字校记与「重复」互链均已分层。

| 层 | 本包位置 | 判定 |
|---|---|---|
| 李我平反吟须看用 | `L7583` | kind=评注；对比例教法 ≠ 单独可执行通则表 |
| 土长生流派 /「万古不易」 | `L7681–7687` | 引述立场；源戌/戊疑字不静默统一 |
| 全图装卦注 | `L7732` | 初学读图说明，非野鹤占断原文 |
| 八宫图疑字校记 | `L7738`/`L7767`/`L7825`/`L7834`/`L7901`/`L7950` 等 | notes 保留原图，不替成「正确」纳支 |
| 应期 / 困卦教学例 | `L7700–7718` | 条件总表 + 限定旬/季教学，不补完整日期案例 |
| 错位卷一重复 | `L7450` 等 50 条 | 互链已审卷一释义；不计新增独立规则或占例 |
| 土水同长生 | `L7655` | notes 禁与八字十二运未经声明混算 |

无把李我平/录入者校记、全图说明或疑字猜测写成野鹤原典规则的缺陷段 ID。

## 7. source-reviewed ≠ 人工 verified

125 条电子语义阅读保持 `source-reviewed`（全书累计 3125），只表示对照当前电子段落实了白话、种类、术语、图行/静图转录与校记/去向，不是影印逐字校勘，不是人类专家验盘，不是预测有效证据，也不是算法可执行。不得把 3125 条 source-reviewed 写成已人工 verified。本包是本 edition 索引收口独立审查，不是产品交付，也不是影印校勘完成。

既有 `docs/book-reviews/zengshan-buyi.md` 是标注岗全书加工报告，不是本岗独立审查证书；本文件才是 CP11 独立复核。MING-224…MING-276 各 CP 报告在其审查分支；本岗未改写 CP9/CP10 文件。

## 8. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 空 notes | CP11 64 条（`[]`；全非图行） | vernacular 仍具体。不回改 |
| 短 vernacular | 「下一图…」/宫五行 min 9 | 对照源为转题或标签句，非空模板。不回改 |
| `kind=重复` 50 | 均含错位说明+wikisource 互链 | 不计新规则。不回改 |
| `L7655` 土水同长生 | notes 已禁混算 | 不回改 |
| `L7681–7687` 流派立场 | 「万古不易」已分层 | 不升野鹤唯一表 |
| 八宫疑字 `辰士`/`来土`/`妻则`/`官鬼五上`/夬缺符 | notes 保留原图 | 不静默校定、不升 verified |
| `verified` 缺省 | 3125 条无该字段 | 校验器按「不是 True」放行。不得补 true |
| CP1–CP10 0–2999 | 与权威 SHA 及已审树深比较 identical | 不回改、不重做、不抢 CP9/CP10 |
| 既有全书报告 | `zengshan-buyi.md` 已在权威树 | 本岗未改该文件 |

## Caveat（不改注解，留给后续 pack）

1. **错位卷一**：`L6504–7730` 为旧采集附入；本包 3000–3067 仍属该区尾；不得当新卷新规则。
2. **`kind=重复`**：与固定卷一逐字互链，沿用已审释义，不计新增占例库存。
3. **应期总表**：多条件候选，不是唯一应日算法。
4. **生旺墓绝**：本书五行表与八字十二运不得未经声明混算；土长生有流派分歧。
5. **李我平评注**：教法对比层，不单独升为野鹤原典通则。
6. **全图读法注**：初学装卦说明。
7. **八宫静图疑字 / 缺符**：保留原图；不得凭「通常应对」静默替换。
8. **三列静图**：同屏多卦是独立装卦列，不能串成动变链。
9. **事后应验 / 日期疑字**：如九月丁亥≠冬月、已未日疑字，是书记差异，非现实验证证书。
10. **电子源**：录入者自承未细校；本地无对应影印。照电子本 source-reviewed，不升 verified。

## 未决（本岗不施工）

- 本 edition 索引 0–3124 的独立审查覆盖已齐；**remaining 0**。仍不是人工 verified，不是影印校勘。
- 影印逐字校勘、争议裁决、规则机器实现、独立现实预测验证仍不在 `source-reviewed` 口径内。
- 本审查不把任何条目标成人工 verified。
- 勿重做 0–2999（MING-224…MING-276）；勿改注解 JSON；勿抢写 CP9/CP10 审查文件。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-279`。
