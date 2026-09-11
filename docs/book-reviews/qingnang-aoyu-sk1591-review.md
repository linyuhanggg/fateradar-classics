# 青囊奧語 · 识典 SK1591：独立审查全量（0–2 / 3）

审查对象：`origin/codex/multica-ming-212` @ `1335ac2c70f1d9eb6264fbb3654add6c30ad3057`（父 `bc798566da77c30e149abf9673c88ecc386702b2`）。工作树只读参考 `fateradar-multica-ming-212`，本岗写出仅本文件。未改注解 JSON、未改源文、未改主本 `qingnang-aoyu.json`、撼龙、协纪、SK1589/SK1619、引擎、`chart.*`。不是《青囊奥语》全书他本完成，也不是主本 `qingnang-aoyu:L####` 包，也不是引擎/排盘接入，也不是全项目完成。

结论：**通过。** 交包结构账本与全部 3 段非模板语义对照成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引口径 remaining 0 ≠ 人工 verified / 主本全书。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-215`，2026-09-11）：

```
git ls-remote origin refs/heads/codex/multica-ming-212
git rev-parse HEAD HEAD^
git diff HEAD^..HEAD --name-only
git diff --stat HEAD^..HEAD
shasum -a 256 sources/normalized/shidianguji/SK1591/paragraphs.json
shasum -a 256 sources/normalized/shidianguji/SK1591/text.md
git rev-parse HEAD^:sources/normalized/shidianguji/SK1591/paragraphs.json
git rev-parse HEAD:sources/normalized/shidianguji/SK1591/paragraphs.json
git rev-parse HEAD^:sources/normalized/shidianguji/SK1591/text.md
git rev-parse HEAD:sources/normalized/shidianguji/SK1591/text.md
git rev-parse HEAD^:references/annotations/fengshui/qingnang-aoyu.json
git rev-parse HEAD:references/annotations/fengshui/qingnang-aoyu.json
git rev-parse HEAD^:references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json
git rev-parse HEAD:references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-212` | `1335ac2c70f1d9eb6264fbb3654add6c30ad3057`（本岗检出基线与 `ls-remote` 一致） |
| 父提交 | `bc798566da77c30e149abf9673c88ecc386702b2` |
| 相对父提交文件 | 仅 2 个：`references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json`、`docs/book-reviews/qingnang-aoyu-sk1591-progress-2026-09-11.md` |
| diffstat | `+130`（两文件均为新增） |
| `paragraphs.json` SHA256 | `f0da58e34eca279bb49d889210d34556b357e0db032c470e8c97ffdd8ddf0c0c`（3，与 Issue 一致） |
| `text.md` SHA256 | `ab9b36f0e7547366cfee1345551cce66cc422e70a8c7bf42380a9b784f606d60` |
| 源 blob 父 vs 本提交 | paragraphs 同 `c224b129…`；text 同 `adf9567a…`（本提交未改源层） |
| 主本 `qingnang-aoyu.json` blob | 同为 `2b39dc425ddfd03f307a8c1f6044944b422ad744`，未改；仍 3 条 `qingnang-aoyu:L####` |
| 识典注解相对父提交 | 父树该文件不存在 → 本提交新建 |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` / `paragraphCount` / `figureCount` | `true` / 3 / 0 |
| 注解 ID 与 `paragraphs.json` 0–2 | 3/3 一一对应，`mismatch=0`；前缀全 `qingnang-aoyu:shidian-SK1591:`；entries 无主本 `L####` 泄漏 |

无越权文件。源层未改。主本青囊 / 他书 / 引擎 / `chart.*` 未覆盖。`scopeNote` 已写明补本不替代主本投票、不接入宅形排盘；提及 SK1589/SK1619 仅作禁止混写说明。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-212 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/qingnang-aoyu--shidian-SK1591.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 3, "source_reviewed": 3,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

3 条：`review=source-reviewed` 全 3；`verified` 全 `false`；无 `draft`。无升 verified。

kind：评注或元数据 2、操作步骤 1。

空白话 0、空 terms 0；空 notes 1（索引 0 卷端元数据，可接受）。无「本段论述 / 白话从略 / 见原文 / TODO」类空模板。白话全文重复组 0。本包 `figureCount=0`。

疑文对照集中在索引 2 notes（破軍㢲断句、左右阴阳干支区间、元空字形、若干异文），保留 unknown / 对照，不补造改正。

## 4. 索引边界

`paragraphs.json` 识典补本 3 段；本包注解覆盖 **0–2 全量**。进度 `nextId` 无、`remaining=0`（索引口径）。无错指主本 `L####` 或全书末。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `qingnang-aoyu:shidian-SK1591:P7429803488521076771`（源「欽定四庫全書」） |
| 注解索引 1 | `qingnang-aoyu:shidian-SK1591:P7429803488521109539`（源「青囊奥語唐楊筠松撰」） |
| 注解索引 2（止） | `qingnang-aoyu:shidian-SK1591:P7429807485487366179`（口诀正文 + 末行书名） |
| remaining | **0**（索引口径） |

起始/止点与 Issue / MING-212 钉死 3 ID 一致。remaining 0 只表示识典 SK1591 这 3 段索引齐，不是主本 L 行号包完成，也不是他本全书完成。

## 5. 抽样语义（全部 3 段非模板，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1591/text.md` 的 `start_line–end_line`。条件/评价/观察项与未知去向分层多数成立；旧象福禄官灾不作现实验证；星名属本篇堪舆口诀，不套紫微命盘同名字段；不写成已接入宅形排盘。下列为非模板抽核（本包仅 3 段，全部对照）。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `…P7429803488521076771` | 评注 / sr | 源 L9 仅「欽定四庫全書」。白话：四库著录，不是断法 | 通过 |
| 1 | `…P7429803488521109539` | 评注 / sr | 源 L11「青囊奥語唐楊筠松撰」。题署≠作者已考定；notes 标明网站章节名≠印本卷号 | 通过结构；见 caveat |
| 2 | `…P7429807485487366179` | 操作 / sr | L13–35：坤壬乙巨门；艮丙辛 / 破軍㢲 / 辰亥武曲；甲癸申贪狼；左右阴阳（子丑至戌亥 / 午巳至申未）；雌雄元空；不寻纳甲；颠倒珠宝 vs 逆顺火坑；认金龙经纬；十义至十真；倒杖/掌模/化气/五星/高低/鬼曜/向放水；进退生克与他山救助空劳；末行「青囊奥语」书名。notes 保留断句与异文对照，不补造 | 通过 |

关键条件与源行（抽核，非转引进度表）：

- 四库著录行：L9
- 书名与杨筠松题署：L11
- 干支—星曜开篇：L13–14
- 左右阴阳行度：L14–15
- 雌雄 / 元空 / 纳甲：L15–17
- 颠倒珠宝 / 逆顺火坑 / 金龙：L17–19
- 十项观察（第一义…第十真）：L19–24
- 倒杖至向放水：L24–30
- 进退 / 生入剋入 / 龙歇他山：L30–33
- 再辨星辰 / 郭璞 / 末行书名：L33–35

十项与进退主条件均在白话；开篇配对未扩成全套排盘表；珠宝/火坑写为顺逆评价而非山向固有善恶。异文断句与主本区间差异只记 notes，未改源、未混写 `L####`。

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。3 条电子语义阅读升 `source-reviewed`，只表示对照本电子段落实了层次/条件/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本 `qingnang-aoyu.json`（3 条 L 行号），不计独立投票。当前产品无宅形/龙砂穴水输入，不得写成已接入风水排盘。remaining 0（索引口径）≠ 人工 verified，≠ 《青囊奥语》全书他本完成。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 索引 1 外传说 | 白话写入「杨益/杨救贫」同层保留；本段源止于「青囊奥語唐楊筠松撰」，无杨益句 | 外传说渗入说明层。不回改 |
| kind「操作步骤」 | 索引 2 为长段口诀/观察项，非可执行测量程序 | 结构合法（kind 在允许集）。见 caveat。不回改 |
| 破軍㢲断句 | notes 对照通行「艮丙辛，位位是破軍；巽辰亥…」；本电子本标点未定 | unknown 对照成立。不回改 |
| 左右阴阳区间 | 本补本「子丑至戌亥 / 午巳至申未」；notes 对照主本维基「子癸至亥壬 / 午丁至巳丙」 | 按本电子原文，不作他本替换。不回改 |
| terms「功曹」 | 源作「功曺」；notes 已列异文 | 术语规范化，非改源。不回改 |
| scopeNote 提及 SK1589/SK1619/L | 仅禁止混写；entries 无他本 ID | 合法。不回改 |
| 空 notes | 索引 0 notes=[] | 卷端元数据可接受。不回改 |

## Caveat（不改注解，留给后续 pack）

1. **索引 1**：题署语义成立，但白话掺入本段未见的「杨益/杨救贫」传闻层；后续若引用作者考据，须回源 L11，不能只看白话。
2. **索引 2 kind**：口诀与观察顺序标「操作步骤」。接入规则库时只能当形势口诀层，不能当可执行坐向/放水算法。
3. **索引 2 异文**：破軍㢲断句、左右干支区间、元空/功曺等与他本差异已在 notes；引用时以本电子原文为准，不混主本 `L####`。
4. **本岗不施工**：上述 caveat 不回改注解，不升 verified。

## 未决（本岗不施工）

- 破軍㢲断句与左右阴阳区间保持对照 / unknown；不补造、不升 verified。
- 识典待校。3 条 source-reviewed 不是人工 verified，也不是预测有效，也不等同风水排盘已接入。
- 主本 3 条 `qingnang-aoyu:L####` 不在本包范围；识典 0–2 审完不等于《青囊奥语》全书完成。
- 本审查不把任何条目标成人工 verified。本岗不改注解。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-215`。
