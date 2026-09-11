# 玉照神应：独立审查主本 source-reviewed 全量（文件索引 0–1）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-481` / 分支 `codex/multica-ming-481`。本岗写出仅本文件。未改注解 JSON、未改源文、未覆盖已有 `docs/book-reviews/yuzhao-shenying.md`、未改识典 `yuzhao-shenying--shidian-SK1602.json`、未抢 MING-464 集成线 / MING-468 产品审查 / 本轮其他审查稿、未改他书 / 引擎 / 产品仓。审查岗未参与该书生产。不是全书影印校勘完成，不是算法交付，不是人工 verified，不冒充已接入八术页面。本包只审主本注解文件索引 0–1（2 条，全量），不要与识典 SK1602 玉照神应包混淆。

结论：**通过（有限范围）。** 结构校验 `ok`、`errors=[]`；2/2 `source-reviewed`、0 draft；`verified=true` 为 0，两条均显式 `"verified": false`；inventory 与注解 `paragraphId` 一一对应且同序；全书 2 段均对照原文语义成立。`source-reviewed` ≠ 人工 `verified`。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。该书主本 SR 审查 remaining **0**。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-481`，2026-09-12）：

```
git ls-remote origin refs/heads/codex/multica-ming-329
git rev-parse HEAD
shasum -a 256 references/annotations/luming-nayin/yuzhao-shenying.json
git rev-parse HEAD:references/annotations/luming-nayin/yuzhao-shenying.json
shasum -a 256 sources/fulltext/luming-nayin/yuzhao-shenying/fulltext.md
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解文件 SHA256 | `abe1ce2c9427f24d52800e729cad35c54d86ac4ca6e38702782cb530493f4b8a`（与 Issue 钉死一致） |
| 注解 blob @ HEAD | `bcae48a1a84decfbf685bf334b625771092219ba` |
| 源 `fulltext.md` SHA256 | `5880e5258085e63c88009a29423f6bef6b949d3ad79411c27fcd5d415c1c62fe` |
| 源行数 / 字符 | 138 行 / 16053 字 |
| 工作树相对 HEAD | 仅新增本审查文件；注解 JSON / 源文 / 既有 `yuzhao-shenying.md` / SK1602 注解无 diff |

无越权文件。注解未改。源文未改。未写产品仓。生产侧 `yuzhao-shenying.json` 随 `9118a78`（MING-324 记录）入树，本岗未参与该书生产。

对照路径确认：`sources/fulltext/luming-nayin/yuzhao-shenying/fulltext.md` 存在，与 inventory `fulltext` 字段一致。

## 2. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/luming-nayin/yuzhao-shenying.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2, "source_reviewed": 2,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。校验器对 `verified is True` 报错；本文件两条均已写 `"verified": false`，本岗不改。

## 3. verified / review 边界（未越权提升）

全书 / 本包同一范围（索引 0–1，2 条）：

| 项 | 实测 |
|---|---|
| `review=source-reviewed` | 2/2 |
| `review=draft` | 0 |
| `verified=true` | 0 |
| `verified=false` | **2/2 显式 false**（文件内 `"verified": true` 出现次数 = 0） |
| 空白话 | 0 |
| 「本段论述 / 白话从略 / 见原文 / TODO」类空模板 | 0 |
| 空 `terms` | 0 |
| `notes=[]`（主条） | 0 |
| `sourceAttribution` | 0 |
| `relatedParagraphIds` | 0 |
| `subsections` | 仅第 2 条：77 个，ID `S001`–`S077` 连续无缺号 |

kind 分布：序跋目录 1、理论 1。与 inventory `kind` 逐条一致。

**verified 说明：** Issue 表述「verified 全 false」。独立读 JSON：两条主注均显式 `"verified": false`，没有任何 `paragraphId` 被标成人工核验。本岗不回改、不提升。判定为「保持未 verified」，与「source-reviewed ≠ 人工 verified」一致。失败清单：无。

## 4. 索引边界、inventory 与 SK1602 隔离

`references/inventory/paragraphs/luming-nayin/yuzhao-shenying.json` 2 段；注解 2 条。`paragraphId` 全部命中，`missing=0`，顺序与 inventory 一致。起 `yuzhao-shenying:L0003-L0009`、止 `yuzhao-shenying:L0011-L0138`，与 Issue 钉死一致。

| 索引 | 实测 ID | heading / kind | 说明 |
|---|---|---|---|
| 0 | `yuzhao-shenying:L0003-L0009` | 玉照神应真经 / 序跋目录 | 四库提要；非经注正文 |
| 1 | `yuzhao-shenying:L0011-L0138` | 玉照神应真经 / 理论 | 题署 + 全部经注；77 子节覆盖 L11–138 |

源文 L1 Markdown 书题 `# 玉照神应真经`、L2 / L10 空行不在 2 段库存内，符合现有切段。L3 行首夹四库「欽定四庫全書 / 子部七」馆题，与提要连在同一主 ID，注解白话以提要案语为主，不把馆题抽成独立断法。

第 2 条 77 子节：`startLine` 最小 11、`endLine` 最大 138；L11–138 无漏行。相邻子节在经注连续文本上共享边界行（74 处），不是缺段或串段。父条 vernacular 含全部 77 条子节白话，且以 `【标题，L…】` 分层，不是整卷空概述。

识典 SK1602 隔离：`references/annotations/luming-nayin/yuzhao-shenying--shidian-SK1602.json` 13 条，ID 形如 `yuzhao-shenying:shidian-SK1602:P…`，与主本 2 个 `Lxxxx` ID **交集为空**。本包不审该文件，不把识典章节名或网站卷号算进主本 remaining。

inventory 第 2 段 `automatic_kind=操作步骤`，注解 / inventory `kind=理论`。连续经注里规则候选与操作步骤都有，标「理论」与生产侧一致；本岗不回改。本包后该书主本 SR 审查 remaining **0**。既有 `docs/book-reviews/yuzhao-shenying.md`（生产侧账本）不覆盖、不回改。

## 5. 全核语义（2/2 主 ID，对照原文，不凭进度摘要）

原文取 `sources/fulltext/luming-nayin/yuzhao-shenying/fulltext.md` 的行范围。全书仅 2 段，按 Issue 要求全核。第 2 段因覆盖整卷经注，另独立抽核子节条件、例外与疑文，不把生产账本当证书。

### 5.1 两条主注

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0009` | 序跋目录 / SR | 原文「舊本題晉郭璞撰張顒註」「晉書璞傳不言」「隋志唐志宋志…皆不著録」「晚出依託」「多涉江南方言疑書與注文均出自張顒」「永樂大典所載首尾備具」「珞琭子及李虚中命書遺意」「外親女婿…牽强附㑹」。白话保留「疑」不升级作者已确考；切理与附会都标为馆臣评价 | 通过 |
| 1 | `L0011-L0138` | 理论 / SR | 题署「玉照定真經 / 張顒 注」；经句短断 + 括号注加年月日時胎、纳音、季节与假令。77 子节覆盖题署至「謹須照下細推呈」。白话同步各子节，不是只留整卷概述 | 通过 |

### 5.2 第 2 段高风险子节抽核（对照原文）

下列条件、例外、方向与疑文均在电子原文中找得到对应句，注解没有删否定词、没有改成现代日干中心八字、没有接到奇门/七政/产品盘：

| 子节 | 原文锚点 | 注解是否贴原文 | 判定 |
|---|---|---|---|
| S001 题署 | L11–12「玉照定真經」「張顒 注」 | 不把郭璞写成已证作者 | 通过 |
| S002 生气天德合 | 「三合生方…須要日時」「長生亦名生氣」；天德「二坤…五乾…八艮…十一巽」；己亥六月有干合、壬子四月「然無干合」；庚午「二月天德在坤」 | 生气两套口径；四仲天德保持卦位，不改成日支 | 通过 |
| S003 身命刑返克 | 「支與納音」；辛巳五月丙寅「寅刑巳下火又尅金」；壬申四月乙巳「巳又刑申」 | 刑与音克同时成立，不是见刑即同断 | 通过 |
| S004/S005 阴尊阳尊 | 年胎月日時五处；例四阳一阴 / 四阴一阳 | 不是四柱现代八字；阴尊不升母亲预后 | 通过 |
| S006 干轻音重 | 「干尅在頭面音尅在身…干輕音重」；丁亥土生金则轻；六月丁为官、五月为鬼 | 季节与印支持保留 | 通过 |
| S007 伏返吟 | 「值本命則伏吟若相衝則返吟」；本命本地 / 他乡；「見干則近支又次下納音又逺」；胎小年月初日中时末 | 不一律吉凶 | 通过 |
| S008 尊卑递克 | 「年尊胎次月又次日又次時」；时克日、日克月、月克年 | 干递克与音递克分层 | 通过 |
| S014 墓库 | 干墓「甲乙在未丙丁到戌庚辛到丑戊巳壬癸到辰」；无旺气墓、有旺气库；甲寅十月非墓、甲子五月为墓 | 不把辰戌丑未一概当墓 | 通过 |
| S018 丙丁亥子 | 「又須視無合而言之」；丙见辛亥、丁见壬子「不為前說」 | 例外条件未删 | 通过 |
| S028 月德月合 | 三合阳干为德、五合阴干为合；单德与德合不同；阳德贵助、阴合阴人 | 旧象，不作现实助力证明 | 通过 |
| S029/S076 十二宫三限 | 命兄妻子财田官奴厄福貌父；生月加子到生时；25 前月、25–50 日、50 后时、15 前胎 | 本书宫序与岁界，不接七政/紫微盘 | 通过 |
| S031 本卦返克 | 本家三合须旺；「水旺相無土則不成氣象」；不得时「客卦」；返克卦另条 | 三支全不等于吉 | 通过 |
| S040 延月 | 「生時與胎月合者主延月…日與胎合者非也」 | 日胎合明确不取 | 通过 |
| S043 前五后五 | 「甲乙丙丁戊為陽干」实为前五位，含乙丁 | 不改成甲丙戊庚壬 | 通过 |
| S048 九宫 | 甲子「上下十八數」相加；乙卯「六八四十八」相乘后「五九四十五外有三」 | 算术不一，不补现代数表 | 通过 |
| S050 前五位推亲 | 胎/月/日/时各前五位拟祖父母自身子孙 | 馆臣已批外亲穿凿，不跳过 | 通过 |
| S062 自刑 | 「辰午酉亥為自刑」；例戊申遇乙酉 | 与常表不完全贴合处保留原文 | 通过 |
| S065 六合方向 | 子合丑不顺 / 丑合子顺；亥寅、戌卯、酉辰、巳申、午未各分来去 | 不改成无向相合 | 通过 |
| S067 分野 | 甲齐乙夷…「午周木秦」 | 「木秦」字疑保留，不补现代籍贯 | 通过 |
| S069 正道歌 | 真五行须长生建旺；「非孤辰寡宿乃是…孤令」 | 孤门不并入孤寡神煞 | 通过 |
| S070 递生救神 | 上生下贫、下生上进；先食后鬼为官；「須向局中問救神」「金人見火…有水為救神」 | 互克要问救神 | 通过 |
| S071 天禄马 / 神煞 | 「此法非本禄本馬」；「神殺刼亡非本理」；「不尅身者無咎」 | 神煞非根本 | 通过 |
| S072 三奇年仪 | 「甲戊庚」阳奇顺、「乙丙丁」阴奇逆，本干在时有气才真；年仪旬中顺干、月仪月建，**不等于奇门六仪** | 虚奇不升真贵 | 通过 |
| S073 借气 | 「待月日時中干音借用…胎則不取」 | 胎不取，不因五处并列而扩大 | 通过 |
| S077 印墓物性 | 五印甲戌火壬辰水丙辰土乙丑金癸未木；「氣旺為印氣敗為墓若輕建旺為庫」；甲木乙草丙火丁灰 | 物名不替换五行；旺墓句义仍待校 | 通过 |

抽核未发现空模板白话、把四库提要「疑」写成作者已确考、删掉「不為前說 / 日與胎合者非也 / 胎則不取」、把年仪月仪并成奇门六仪、把十二宫接到产品现盘、把识典 SK1602 段落 ID 混入主本，或把任何条的 `verified` 置 true。

## 6. 明确非结论 / 不失败的 caveat

- 本包 **不** 证明影印已校或传统断语经验验。
- 本包 **不** 把任何条升为人工 `verified`。
- 本包 **不** 表示禄命 / 玉照材料已接入 FateRadar 八术页面。
- 本包 **不** 覆盖或取代已有 `docs/book-reviews/yuzhao-shenying.md`，也 **不** 审查或回改识典 SK1602。
- 包名「玉照神应真经」不等于底本题《玉照定真经》；张顒 / 张颙为繁简对应，不据电子文本改字。
- 提要白话未逐点复述菉竹堂书目、纪昀等校上衔名，属提要压缩，不构成语义失败。
- 电子文本常见巳/己混用（如「乙辛丁巳亥酉」标题 vs 注「己亥赤口」；阴干「乙丁巳辛癸」）。注解按标题或文义分层，未暗改原文；保持待校。
- 九宫甲子相加与乙卯相乘、前五称阳干而含乙丁、自刑例与常表、木秦等字、空亡偏正一句含糊，均已在 notes 保留，不据常见表补造。

## 7. 交付

| 项 | 值 |
|---|---|
| Issue | MING-481 |
| 工作树 | `fateradar-multica-ming-481` |
| 分支 | `codex/multica-ming-481` |
| 基线 SHA | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 独占文件 | `docs/book-reviews/yuzhao-shenying-independent-review.md` |
| 远端仓 | `linyuhanggg/fateradar-classics` |
| 结论 | **通过（有限范围）**；主本 SR remaining 0 |

下一步：协调者快速核对证据后可将本 Issue `done`；无需重做 0–1；无需回改注解；无需把 SK1602 算进本包 remaining。
