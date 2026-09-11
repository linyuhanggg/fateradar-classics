# 大六壬秘本：独立审查主本 source-reviewed CP9（索引 2400–2642 收尾）

审查对象：权威树 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-408` / 分支 `codex/multica-ming-408`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 CP1–CP8 审查稿（含并行 [MING-406](mention://issue/01a0917d-ac63-709e-9528-8129ffe3fa24) 的 `liuren-miben-cp8-review.md`）、未改大六壬大全 / 识典 SDZJ0170 / inventory / 引擎 / `chart.*`。不要重做 CP1–CP8（0–2399）。不要与并行 CP8 写同一审查稿。不要抢 [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) 已审 JSON（SHA `2789a729…` 未合入本包）。本包只审注解文件索引 **2400–2642**。这是秘本 SR 最后一包。不是秘本全书完成，也不是人工 verified。本岗未参与六壬秘本生产。

结论：**通过。** 结构校验与 ≥15 段非模板抽样语义成立；本段 **242 SR + 1 draft**，draft 保持 draft 未升 SR；`verified` 全 false；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 0–2399 相对权威 SHA 对象级未动。本包后秘本 SR 审查 remaining **0**（注解 JSON 仍待后续集成合入 397）。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-408`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
git branch --show-current
shasum -a 256 references/annotations/san-shi/liuren-miben.json
git hash-object references/annotations/san-shi/liuren-miben.json
git rev-parse HEAD:references/annotations/san-shi/liuren-miben.json
shasum -a 256 sources/fulltext/san-shi/liuren-miben/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
git status --porcelain
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（`ls-remote` 与本岗 HEAD 一致） |
| 分支 | `codex/multica-ming-408` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（与 Issue 钉死一致；397 已审 `2789a729…` 未合入） |
| 注解 blob HEAD vs working | 同为 `a7b3659fe2f951a2f4a5631bbbe6274b428c7d9f`（未改） |
| 源 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3` |
| 源行数 | 6018 |
| `bookSlug` | `liuren-miben` |
| `sourceTitle` | 大六壬秘本（现有电子主文本） |
| 对照原文 | `sources/fulltext/san-shi/liuren-miben/fulltext.md` |
| inventory 段落 ID | 本包 243/243 ID 均在 `references/inventory/paragraphs/san-shi/liuren-miben.json`（2643），全书 ID 集合全等；`missing=0`（注解文件序 ≠ inventory 行序，不以 inventory 切片对齐） |
| 本包覆盖 | 仅索引 2400–2642；起 `liuren-miben:L2503-L2503` 止 `liuren-miben:L6015-L6018`；未泄漏 0–2399；未写 CP8 审查稿 |
| `git status` | 交包前仅新增本审查稿 |

无越权文件。注解 JSON 未改。大六壬大全 / 识典路径未碰。MING-397 JSON 修复未碰。并行 CP8 审查稿未碰。

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

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。全书 entries=2643（sr=2554 + draft=89）；本包只审 2400–2642。JSON SHA 交包前后未变。`source_reviewed=2554` 不是 2643。

## 3. verified / draft 未越权提升

本包索引 2400–2642（243 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 242/243 |
| `review=draft` | 1/243（保持 draft，未升 SR） |
| `verified` | 全 `false`（全书 2643 亦无 true） |
| 空白话 | 0 |
| 空 terms | 0 |
| notes 字段缺失 | 0（`notes=[]` 20 条，属无附注，不是空话） |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 白话完全重复组 | 0 |
| 有 subsections | 0 |

kind（2400–2642）：规则候选 215、评注或元数据 28。无「术语 / 理论 / 操作步骤 / 待核实 / 序跋目录 / 案例」kind；不强制凑齐。本包有「待核实」语义的疑字，但生产岗把它们写在 SR 的 notes 里，未单开 `kind=待核实`（唯一 draft 的 kind 是评注或元数据）。

SR 白话字数 min/median/max = 20/65/196。最短为 `L2818`「此段亦不出《精蕴》。校记，不是占法步骤。」与十二类题短行，对照源行归属正确，不是空模板。

1 条 draft（`verified=false`，不补字、不升 sr）：

| 索引 | paragraphId | kind | 原因（对照源，不改正文） |
|---|---|---|---|
| 2642 | `L6015-L6018` | 评注或元数据 | 校勘说明：CTP 三处章界已据 NCL-06572 影印补字，但尚未全书逐行异校；馆藏二十卷 vs 目录/正文十七卷并行。inventory 标 `doubtful=true`。保持 draft |

符合「draft 保持 draft，不得升 SR」。

本包 15 条 **仍为 SR、只在 notes 标待核** 的条目不得回改成 draft，也不得因此升 verified：

| 索引 | paragraphId | notes 待核（本岗不改） |
|---|---|---|
| 2402 | `L2507-L2507` | 迷惑正醜逆季，醜疑丑 |
| 2417 | `L2540-L2540` | 死闲待核 |
| 2430 | `L2566-L2566` | 君须否待核 |
| 2448 | `L2602-L2602` | 奔而木待核 |
| 2451 | `L2608-L2608` | 丙辰寅卯醜，醜疑丑 |
| 2493 | `L2692-L2692` | 贼归待核 |
| 2512 | `L2730-L2730` | 虚正待核 |
| 2529 | `L2764-L2764` | 艮庚待核 |
| 2551 | `L2808-L2808` | 稿歉待核 |
| 2569 | `L2844-L2844` | 蟺热待核；金氏旁改下升并行 |
| 2602 | `L2910-L2910` | 任嘉定易待核 |
| 2606 | `L2918-L2918` | 己官待核 |
| 2607 | `L2920-L2920` | 加临替待核 |
| 2615 | `L2936-L2936` | 遥作待核 |
| 2632 | `L2970-L2970` | 替岁月待核 |

这些不是假 SR：白话已对照电子原文落实层次，疑点只记 notes。本岗不改、不降 draft、不升 verified。

十二类题（婚姻 / 疾病 / 出行 / 行人 / 谒人察善恶 / 论讼 / 田六种 / 晴雨 / 科举 / 乾禄 / 日辰人宅 / 奴婢）白话同构「…玉田歌类题。条件见后文各句，不改取传。」，首词各绑不同类题，不是空模板。

## 4. 索引边界

注解全书 2643 条。本包只审注解索引 2400–2642（按文件索引；本段内源行起点单调升序）。Issue 钉死起止与实测一致。

| 位置 | 实测 ID | 说明 |
|---|---|---|
| 注解索引 2399（CP8 止，不在本包） | `liuren-miben:L2501-L2501` | 玉成歌宅墓条（不在本包） |
| 注解索引 2400（CP9 起） | `liuren-miben:L2503-L2503` | 天目春辰顺季，占宅加日辰 |
| 注解索引 2410 | `L2523-L2523` | 玉成歌卷十一终 |
| 注解索引 2411 / 2412 | `L2528` / `L2530` | 卷十二李批附注；类题「婚姻」 |
| 注解索引 2637 | `L2980-L2980` | 卷之十二总括玉田歌终 |
| 注解索引 2638 | `L5997-L5997` | 识典补本分隔 `---`（文件序大跨，不是漏标） |
| 注解索引 2642（CP9 止＝全书文件序终） | `liuren-miben:L6015-L6018` | 校勘说明（draft） |
| 下一包 | 无 | 文件索引已尽 |

唯一「大跨」是 2637=`L2980` 接到 2638=`L5997`。卷之十三至卷十七主文已在文件索引 0–1226（CP1–CP5 范围），不在本包回改。本岗抽核该跨度两侧 ID 均能在 inventory 命中。markdown 卷题（`## 卷之十二` `L2526`、`## 卷之十三` `L2983`、附录 `##`/`###` 标题）不在 inventory，全书同类未标，不构成本包失败。

约略覆盖（按源行）：

- 卷十一《玉成歌》收束：天目 / 迷惑 / 金神四煞 / 旺相总则 → `L2523` 卷十一终
- 卷之十二《玉田歌》：婚姻、疾病、出行、行人、谒人、论讼、田六种、晴雨、科举、乾禄、日辰人宅、奴婢（含金氏旁改与「不出精蕴」校记）→ `L2980` 卷十二终
- 识典补本：`L5997` 分隔 → 跨章影印补字三处 → 卷之三标题截断 → `L6015-L6018` 校勘说明（draft）

不要把 CP9 写成「inventory[2400–2642]」或从 `L2400` 起。

本包后 remaining **0**（文件索引）。全书仍有 **89 draft**（本包 1 条 + 0–2399 的 88 条），0–2399 的 draft 不在本包回改范围。注解 JSON 仍待后续集成合入 397，不等于已进唯一产品线。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 的 `start_line–end_line`。下列为非模板抽核（优先 SR；draft 抽核但不升格）。覆盖本包两种 kind：规则 / 评注。

| 索引 | ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 2400 | `L2503-L2503` | 规则 / sr | 天目春辰顺季行，占家宅加日辰才宅中鬼神；起例春辰顺季＝辰未戌丑。不得凡见天目皆宅鬼 | 通过 |
| 2402 | `L2507-L2507` | 规则 / sr | 迷惑煞正醜逆季，加年命才昏迷；又正月戌逆十二。两路起例并行。醜疑丑，不改正文 | 通过（待核留 notes） |
| 2405 | `L2513-L2513` | 规则 / sr | 金神孟酉仲巳季醜；四煞＝三合墓。并吉将迟疑 vs 吉凶将战难成 vs 无害相生忧不成凶，三层不得塌。季日醜写作丑 | 通过 |
| 2408 | `L2519-L2519` | 规则 / sr | 总不出旺相生克死囚法合。不改九宗门取传，不覆盖前文专条例外 | 通过 |
| 2410 / 2412 | `L2523` / `L2530` | 评注 / sr | 卷十一终不混卷十二。类题「婚 姻」条件见后文，不改取传 | 通过 |
| 2413 | `L2532-L2532` | 规则 / sr | 乾为天、支为地；幹即夫宫支即妻。须干夫支妻逆互。本条专主婚姻，不混干人支宅总论 | 通过 |
| 2417 | `L2540-L2540` | 规则 / sr | 须龙战在支上才病困；无救助且死闲、天后所乘才早亡。死闲待核，不改正文 | 通过（待核留 notes） |
| 2430 | `L2566-L2566` | 规则 / sr | 无气及病由看变处求残疾之因。「君须否」待核。不覆盖后文专条 | 通过（待核留 notes） |
| 2448 | `L2602-L2602` | 规则 / sr | 魁罡为鬼 vs 传入病支分读。「奔而木」句涩待核，不改正文 | 通过（待核留 notes） |
| 2493 | `L2692-L2692` | 规则 / sr | 须占时傍日辰。刚伏吟顺传 vs 伏阴逆连茹。「贼归」疑则归，不改正文。不改伏吟取传 | 通过（待核留 notes） |
| 2512 | `L2730-L2730` | 规则 / sr | 蛇虎勾朱怒忿 / 六合虚正非谦 / 天后迟疑 / 太阴懒困，四路分将。「虚正」待核 | 通过（待核留 notes） |
| 2529 | `L2764-L2764` | 规则 / sr | 须用初官鬼而求财乡，克命才喜。「艮庚」待核，不补官名 | 通过（待核留 notes） |
| 2551 / 2556 | `L2808` / `L2818` | 规则+评注 / sr | 亥上寅初丰；迟中早占法同，不得只断早稻。「稿歉」待核。`L2818` 不出精蕴＝校记不是占法 | 通过 |
| 2569 | `L2844-L2844` | 规则 / sr | 蛇化龙飞＝雨 vs 龙蛇蟺热＝晴。金氏旁改「龙蛇」作「下升」与正文并行，不改正文 | 通过（待核留 notes） |
| 2589 | `L2884-L2884` | 规则 / sr | 无禄四上克下 vs 绝嗣四下克上。天网用时同克日。飞魂正亥顺 vs 天鬼正酉逆仲。止于科举，不混乾禄 | 通过 |
| 2602 / 2606 | `L2910` / `L2918` | 规则 / sr | 趋部须支生干上。「任嘉定易」待核。日命二禄皆空+用死逆+玄空阴后才失职。「己官」待核 | 通过（待核留 notes） |
| 2615 / 2632 | `L2936` / `L2970` | 规则 / sr | 天后临支且所乘作日鬼，女掌权非美。「遥作」待核。死气死神临支阳＝缠患。「替岁月」待核 | 通过（待核留 notes） |
| 2637 / 2638 / 2641 | `L2980` / `L5997` / `L6011` | 评注 / sr | 卷十二终。补本分隔不是术数规则。卷之三标题据目录恢复旬中神煞，不是神煞起例 | 通过 |
| 2640 | `L6005-L6007` | 评注 / sr | 三处章界补字据 NCL-06572 页码逐录，不以语义猜补。不入主文本计数 | 通过 |
| 2642 | `L6015-L6018` | 评注 / draft | 尚未全书逐行异校；二十卷元数据 vs 十七卷目录正文并行。inventory doubtful。保持 draft | 通过（draft 保留） |

抽核未见把 draft 升 SR、未见把 verified 置 true、未见空模板白话冒充 SR、未见邻段 vernacular 错位。失败 paragraphId：无。

关键源行（抽核）：L2503–2523 玉成歌收束与卷十一终；L2528–2980 玉田歌各类（含金氏旁改、精蕴校记、无禄绝嗣）；L5997–6018 识典补本与校勘说明。

## 6. Caveat（不构成本包失败）

1. 1 条 draft（`L6015-L6018`）与 15 条 SR notes 待核（醜/丑、死闲、奔而木、贼归、虚正、艮庚、稿歉、蟺热、任嘉定易、己官、加临替、遥作、替岁月等）仍待核；本审查只确认处置正确，不重写、不升格。
2. 部分 SR 条白话内标疑字但仍标 SR；条件绑定与源文一致，不据此失败，也不升 verified。
3. 十二类题白话同构、最短校记信息量低，但与源行一一对应，不是「白话从略」模板。
4. `L5997` 源文是 markdown 分隔 `---`，标 SR 评注「识典补本起始分隔」合理；不是占法。
5. source-reviewed ≠ 人工 verified；电子全文不是影印校勘。CTP 抄录本无明确底本、跨章断裂不得补字等旧 caveat 仍在。
6. 本包不覆盖索引 0–2399（CP1–CP8）。卷十三至卷十七主文在文件序前部，不在本包。
7. [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) 已审 SHA `2789a729…` 未合入本包；本审查钉死 SHA `30b9b2b9…`。后续若合入 397，须另核，不以 397 未合入阻断本包。
8. 本包后秘本 **SR 审查** remaining 0，不等于注解已进唯一产品线，也不等于 89 条 draft 已消，更不等于人工 verified 或全书交付。

## 7. 交包边界

| 项 | 值 |
|---|---|
| 权威 tip | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 注解 SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821`（未变） |
| 本岗写出 | 仅 `docs/book-reviews/liuren-miben-cp9-review.md` |
| 结论 | **通过** |
| remaining | 秘本 SR 审查 **0**（JSON 仍待集成合入 397） |
| 下一未纳入 | 无（文件索引 2642 为全书终） |
