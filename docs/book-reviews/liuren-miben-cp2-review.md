# 大六壬秘本：独立审查主本 source-reviewed CP2（300–599）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-384` / 分支 `codex/multica-ming-384`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1 审查稿、未改大六壬大全 / 识典 SDZJ0170 / inventory / 引擎 / `chart.*`。不要重做已 done [MING-379](mention://issue/01a09153-00f1-766b-8e19-c82683b53304) CP1（0–299）。不要与并行 CP3 写同一审查稿。本包只审索引 300–599。不是秘本全书完成，也不是人工 verified。本岗未参与六壬秘本生产。

结论：**通过。** 结构校验与 ≥15 段非模板抽样语义成立；本段 283 SR + 17 draft，draft 保持 draft 未升 SR；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–299 相对权威 SHA 对象级未动。索引 600–2642（remaining **2043**）不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-384`，2026-09-12）：

```
git rev-parse HEAD
git branch --show-current
shasum -a 256 references/annotations/san-shi/liuren-miben.json
git hash-object references/annotations/san-shi/liuren-miben.json
git rev-parse HEAD:references/annotations/san-shi/liuren-miben.json
shasum -a 256 sources/fulltext/san-shi/liuren-miben/fulltext.md
git status --porcelain
```

结果：

| 项 | 实测 |
|---|---|
| `HEAD` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（与 Issue 钉死权威 tip 一致） |
| 分支 | `codex/multica-ming-384` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死一致） |
| 注解 blob HEAD vs working | 同为 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（未改） |
| 源 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| `bookSlug` | `liuren-miben` |
| 对照原文 | `sources/fulltext/san-shi/liuren-miben/fulltext.md` |
| inventory 段落 ID | 本包 300/300 均在 `references/inventory/paragraphs/san-shi/liuren-miben.json`（2643），`missing=0` |
| 本包覆盖 | 仅索引 300–599；未泄漏续写 600+；未写 CP1 / CP3 审查稿 |
| `git status` | 交包前仅新增本审查稿 |

无越权文件。注解 JSON 未改。大六壬大全 / 识典路径未碰。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2643, "source_reviewed": 2554,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 entries=2643（sr=2554 + draft=89）；本包只审 300–599。JSON SHA 交包前后未变。

## 3. verified / draft 未越权提升

本包索引 300–599（300 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 283/300 |
| `review=draft` | 17/300（保持 draft，未升 SR） |
| `verified` | 全 `false`（全书 2643 亦无 true） |
| 空白话 | 0 |
| 空 terms | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 有 subsections | 21 |

kind（300–599）：规则候选 193、理论 80、术语 12、评注或元数据 8、序跋目录 4、案例 2、操作步骤 1。

SR 白话字数 min/median/max = 5/47/352。最短为刑名标目「一曰自刑。」等术语行与「卷之十四终。」收束行，对照源文归属正确，不是空模板。

17 条 draft 均因电子本粘连/叠字/异文/范围冲突等显式保留，白话写明「不改正文」或待核点，符合「draft 保持 draft，不得升 SR」。

## 4. 索引边界

注解全书 2643 条。本包只审注解索引 300–599。

| 位置 | 实测 ID | 行号 |
|---|---|---|
| 注解索引 299（CP1 止，冻结） | `liuren-miben:L3749-L3749` | L3749 |
| 注解索引 300（CP2 起） | `liuren-miben:L3751-L3759` | L3751–L3759 |
| 注解索引 599（CP2 止） | `liuren-miben:L4594-L4594` | L4594 |
| 注解索引 600（下一包起，不在本包） | `liuren-miben:L4596-L4596` | L4596 |

起止与 Issue 钉死一致。本包后 remaining **2043**（索引 600–2642）。

约略覆盖（按源行）：朱恆「中式心法」自序与洪武署年 →「大六壬毕法略说」摘句与三十类收束 →「司天苗达过将法」十二节换将表 → 空亡/刑害/丁神/太阳照等发断歌注 → 至 L4594 木土关锁牢狱与水土官符田宅争讼。不延伸至下一 `L4596`。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（优先 SR；draft 抽核但不升格）。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `L3751-L3759` | 序跋 / sr | 右中式心法一通；黄帝太一壬遁；五要权衡；作者自序不是取传 | 通过 |
| 305 | `L3769-L3769` | 规则 / sr | 六阴相逐；旺禄临身徒妄作；权摄不正禄临支；限制条件保留 | 通过 |
| 320 | `L3799-L3799` | 规则 / sr | 丧吊挂缟；空空事休追；宾主不投刑在上 | 通过 |
| 326 | `L3811-L3811` | 操作 / sr | 学壬决断七处：日辰三传年命+类神；不把七处改成六处 | 通过 |
| 340 | `L3859-L3859` | 理论 / sr | 干禄得地可荣身；略有伤则支用寻 | 通过 |
| 360 | `L3930-L3930` | 规则 / sr | 妻虽入空，旺气所钟，喜病并见 | 通过 |
| 380 | `L3970-L3970` | 规则 / sr | 龙空则财半得不能全获 | 通过 |
| 400 | `L4010-L4010` | 规则 / sr | 空鬼玄武五盗二耗；朱批出《六壬经纬》，不当正文算法 | 通过 |
| 420 | `L4050-L4050` | 理论 / sr | 破神入干内欺、临支外侮 | 通过 |
| 460 | `L4224-L4224` | 规则 / sr | 丁神动静；带吉则吉动带凶则凶动，不定凡丁皆凶 | 通过 |
| 480 | `L4281-L4281` | 规则 / sr | 旺丁凶煞刑支+破耗主家败；三交游煞孤寡或子星主过继，两支分绑 | 通过 |
| 498 | `L4342-L4342` | 案例 / sr | 乙亥日未加未女人讼示例，细则下挂太阴官符条件 | 通过 |
| 500 | `L4346-L4346` | 理论 / sr | 太阳一照歌句；细则见下行分将 | 通过 |
| 520 | `L4436-L4436` | 规则 / sr | 巳双女亥双鱼两事象；三路条件齐全才两事 | 通过 |
| 540 | `L4476-L4476` | 理论 / sr | 隔地投机话；直性前行骂；他乡牵挂 | 通过 |
| 560 | `L4516-L4516` | 理论 / sr | 子木入水；得才读财不改正文 | 通过 |
| 580 | `L4556-L4556` | 规则 / sr | 干支相克为两敌须带马丁；缺马丁不套输赢难定 | 通过 |
| 599 | `L4594-L4594` | 规则 / sr | 木土关锁牢狱 vs 水土朱雀官符田宅争，分绑 | 通过 |
| 332 | `L3833-L3833` | 规则 / draft | 「巳一亥」粘连疑一刻；不改正文、不升 SR | 通过（draft 保留） |
| 344 | `L3871-L3871` | 规则 / draft | 「看二」与夹注「看救」异文并存；不据一行改 | 通过（draft 保留） |
| 440 | `L4108-L4108` | 规则 / draft | 歌「月上」与注「日上」并行待核 | 通过（draft 保留） |
| 503 | `L4352-L4363` | 规则 / draft | 寅到酉 / 酉至寅两段「不照」范围冲突；不据常见昼卯夜酉改字 | 通过（draft 保留） |

抽核未见把 draft 升 SR、未见把 verified 置 true、未见空模板白话冒充 SR。失败 paragraphId：无。

## 6. Caveat（不构成本包失败）

1. 17 条 draft 的电子本粘连、叠字、歌注异文、范围冲突等仍待核；本审查只确认处置正确，不重写、不升格。
2. 部分 SR 条 `notes` 为空，但白话与 terms 非空且对照源文成立；不据此失败。
3. 最短白话（刑名标目、卷终行）信息量低，但与源行一一对应，不是「白话从略」模板。
4. source-reviewed ≠ 人工 verified；电子全文不是影印校勘。
5. 本包不覆盖索引 0–299（CP1 已 done）与 600–2642（后续包）。

## 7. 交包边界

| 项 | 值 |
|---|---|
| 权威 tip | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（未变） |
| 本岗写出 | 仅 `docs/book-reviews/liuren-miben-cp2-review.md` |
| 结论 | **通过** |
| remaining | 索引 **600–2642**（2043 条） |
| 下一未纳入 | `liuren-miben:L4596-L4596` |
