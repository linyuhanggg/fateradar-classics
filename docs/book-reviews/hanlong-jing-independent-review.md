# 撼龙经 · 主本：独立审查 source-reviewed 全量（0–5 / 6）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。工作树 `fateradar-multica-ming-453` / 分支 `codex/multica-ming-453`。本岗写出仅本文件。未改注解 JSON、未改源文、未改 inventory / catalog / 引擎 / `chart.*` / 他书。审查岗未参与该书生产。不要抢 MING-447 / MING-448 / MING-449。不要混 `yilong-jing` 独立册、不要混 SK1609。不是影印校勘，不是算法交付，不是人工 verified，不冒充已接入八术页面。

结论：**通过。** `validate-annotations` `ok=true entries=6 source_reviewed=6 errors=[]`；`verified` 全 6 条显式 `false`（0 条 True）；0 draft；起 `hanlong-jing:L0003-L0010` 止 `hanlong-jing:L0343-L0343`；注解与段落库存 6/6 paragraphId 顺序全等。全书 6 段对照电子原文成立。`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘；`remaining=0` 只指本电子本段落集覆盖。合刊文件按书内题名分层（撼龙 / 疑龙 / 葬法倒杖），复录不计独立支持。风水材料不冒称八术算法已消费。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-453`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/fengshui/hanlong-jing.json
shasum -a 256 sources/fulltext/fengshui/hanlong-jing/fulltext.md
git rev-parse HEAD:references/annotations/fengshui/hanlong-jing.json
git rev-parse origin/codex/multica-ming-329:references/annotations/fengshui/hanlong-jing.json
git status --short
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 远端 | `https://github.com/linyuhanggg/fateradar-classics.git` |
| 注解 JSON SHA256 | `e8ce5579793799a64c944b5af16545e599bac3e280747cbe524208b0e0a0bbf4`（与 Issue 钉死一致） |
| 注解 blob | `a628c6017a8f1eb108697a6c8e56c18fcfd12102`（HEAD 与 origin/329 同） |
| 实际源文 | `sources/fulltext/fengshui/hanlong-jing/fulltext.md`（343 行） |
| 源 SHA256 | `e7b6323af6f73f77d79b7768f0e173c84f6d99538c21ec5881ef21b3d9d3928b` |
| 库存段落 | `references/inventory/paragraphs/fengshui/hanlong-jing.json` 6 条，ID 顺序与注解全等 |
| catalog `source_anchor_url` | 维基文库《撼龍經_(四庫全書本)》；`actual_fulltext_path` = `sources/fulltext/.../fulltext.md` |
| source-quality | `mixed`：合刊转写，L130 起疑龙、L229 起葬法倒杖，须依题名分层 |
| 工作树相对审查基线 | 仅新增本审查稿；注解 JSON / 源文无 diff |

无越权文件。未碰 447/448/449 工作树或分支。未改 `yilong-jing.json` / SK1609。注解未改。源文未改。未写产品仓。

## 2. 校验器独立复跑

对本岗从钉死 SHA 检出的独立副本（非 ming-329 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/hanlong-jing.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 6, "source_reviewed": 6,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。`verified is True` 会报错；本文件 0 条触发。

## 3. verified / draft 未越权提升

6 条：`review=source-reviewed` 全 6；无 `draft`；`verified: false` 全 6（显式 false，非缺省）。空白话 0；空 terms 0；空 notes 仅 1（尾题 `L0343-L0343`，结构合法）。无 `relatedParagraphIds`。注解 kind：序跋目录 1、理论 4、评注或元数据 1。库存 kind 仍全为 `待分类`（与注解不一致），只记质量账本，本岗不回改 inventory。

合刊分层与疑点均保留原字与 notes，不补造、不升 verified：

| 索引 | paragraphId | 保留要点（对照原文） |
|---|---|---|
| 0 | `L0003-L0010` | 旧题杨筠松与宋无名氏记录同存；撼龙是否辨龙无可考；李国本注图已删 |
| 1 | `L0012-L0126` | 九星/官鬼/空亡为形势术语；末歌简断与前文例外同存；不作现实效验 |
| 2 | `L0128-L0173` | L128 撼龙尾题 / L130 疑龙上篇分层；L173〔阙〕不补 |
| 3 | `L0175-L0225` | 「二闯」原留；L224 变辅星后〔阙〕；十问+卫龙+变星三层附文 |
| 4 | `L0227-L0341` | L237「四法」实列斩截队；十二法题下仅 11 标题；L260〔阙〕；L337「避凶就凶假也塋」疑句 |
| 5 | `L0343-L0343` | 尾题复录，非新规则 |

## 4. 索引边界

段落库存 6 段；注解覆盖 0–5，与库存 ID 列表逐项相等。`remaining=0` / 无 nextId，只相对本电子本 paragraphId 集合。

| 位置 | 实测 ID |
|---|---|
| 注解/源索引 0（起） | `hanlong-jing:L0003-L0010` |
| 注解索引 5（止） | `hanlong-jing:L0343-L0343` |

非空源行除 L1 Markdown 标题 `# 撼龙经` 外全部入段。正文覆盖：四库提要 → 撼龙九星全文 → 疑龙上中下 → 疑龙十问/卫龙/变星 → 葬法倒杖（太极至二十四砂）→ 尾题。`remaining=0` ≠ 人工 verified / ≠ 影印校勘 / ≠ 合刊三书已拆独立册 / ≠ 产品交付。

电子本题卷结构（合刊，非单本撼龙）：

1. L3–10 四库提要（三书合论）
2. L12–126 撼龙经正文（九星形势）
3. L128–173 疑龙经上中下
4. L175–225 疑龙十问 + 卫龙篇 + 变星篇
5. L227–341 葬法倒杖（含倒杖十二法、二十四砂）
6. L343 葬法倒杖尾题

另有独立注解册 `yilong-jing.json`（96 条）；本审查只核合刊文件 `hanlong-jing.json`，不计作另一册证据，也不混 SK1609。

## 5. 全书语义（6/6 对照原文，不凭进度摘要）

原文取 `sources/fulltext/fengshui/hanlong-jing/fulltext.md` 的 `start_line–end_line`。本书仅 6 段，本岗全量对照，非抽样。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0010` | 序跋目录 / sr | 提要：旧题杨筠松、史传不足信；撼龙九星、疑龙干枝到头、倒杖倚盖撞黏；宋无名氏与今本题署并存；删李国本注图；纪昀等署校 | 通过 |
| 1 | `L0012-L0126` | 理论 / sr | 须弥骨脉与平洋两水夹；九星贪巨禄文廉武破辅弼形变、剥换护送、官鬼空亡、罗星关栏、三垣辅弼、穴形与末歌；星名借天象取类非现代天文 | 通过 |
| 2 | `L0128-L0173` | 理论 / sr | 疑龙上中下：干枝迎送、飞峰护从、真假朝、明堂护关、肥瘦配护、背面罗星、怪穴随星、L173 阙 | 通过 |
| 3 | `L0175-L0225` | 理论 / sr | 十问（抱养/公位/阳宅/主客/花假/剥换等）+ 卫龙垣局 + 变星异穴；「二闯」与 L224 阙保留 | 通过 |
| 4 | `L0227-L0341` | 理论 / sr | 太极两仪四象；盖粘倚撞斩截等穴法；倒杖十一标题 vs「十二法」；二十四砂各形条件；疑句/阙文保留 | 通过 |
| 5 | `L0343-L0343` | 评注或元数据 / sr | 「葬法倒杖」尾题复录 | 通过 |

关键条件与源行（全量核，非转引进度表）：

- 旧题杨筠松 / 玉函逃难不足尽信：L5–6
- 撼龙九星、疑龙三篇、倒杖诸法提要：L6–7
- 须弥山天地骨 / 两水夹处是真龙：L14–15
- 贪狼尖圆平直小为正；廉作贪祖：L23–24
- 前官后鬼须细辨 / 空亡穴后仰瓦：L70–72
- 干上寻龙 / 寻得星峰却是枝：L131
- 明堂惜水如惜血：L141
- L173「占得山川万古〔阙〕」：L173
- 「二闯公位」：L180
- 葬小居大：L193
- L224「变作辅星〔阙〕」：L224
- 认太极圆晕小明堂：L230
- L237「已上四法」但仅斩截队三法：L237
- 倒杖标题顺逆缩离没穿斗截对缀犯（11）：L270–290
- L260 挨法段〔阙〕：L260
- L337「避凶就凶假也塋」：L337

## 6. source-reviewed ≠ 人工 verified

本电子本来源为维基文库四库整理本合刊转写。6 条 `source-reviewed` 只表示对照当前电子段落落实了提要署名辨析、撼龙九星形势、疑龙干枝背面与十问附篇、葬法倒杖穴法及缺文/条数/疑句去向，不是影印逐字校勘，也不是风水效验证据。合刊物理文件 ≠ 三书已各自独立校定。风水材料进入可检索知识库，当前页面没有对应输入与算法，不得冒称已接入八术。不得把 6 条 source-reviewed 写成已人工 verified。`remaining=0` 仅对本电子本注解覆盖而言。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| `verified: false` | 6/6 显式 false | 与「全 false」同口径。不回改 |
| 库存 kind `待分类` | 6/6 与注解 kind 不一致 | 只记。不回改 inventory |
| 合刊边界 | L130 疑龙、L229 倒杖；source-quality=`mixed` | 注解已 `sourceAttribution` 分层。不计独立册 |
| 〔阙〕三处 | L173 / L224 / L260 | notes 已记。不补 |
| L237 四法漏列 | 斩截队 3 + 后文吊 | notes 已记。不凑第四法名 |
| 「十二法」11 标题 | 顺…犯，无第十二 | notes 已记。不补 |
| 「二闯」 | L180 | notes 已记。不改「二问」 |
| L337 疑句 | 「避凶就凶假也塋」 | 原字保留。不回改 |
| 空 notes | 仅尾题 L343 | 结构合法。不回改 |
| 独立 `yilong-jing` | 另 96 条 | 本岗不混、不核、不改 |
| SK1609 | 星學大成 | 本岗不碰 |

## Caveat（不改注解，留给后续 pack）

1. **合刊非单本**：同一 `hanlong-jing` 文件含撼龙、疑龙、葬法倒杖；引用与产品消费必须按题名分层，不能整文件当撼龙正文。
2. **无同书影印**：source-reviewed 停在电子语义；三处〔阙〕、十二法条数、L337 疑句保持 unknown/待校。
3. **九星 ≠ 紫微/天文**：贪狼等是形势取类，不可直接接紫微斗数或现代星表。
4. **官鬼空亡 ≠ 八字六爻**：本书指前朝后撑与穴后卷空，不是干支官鬼或旬空。
5. **倒杖/二十四砂不是施工规范**：古法放棺深浅与培土描述，不得当作现代墓葬工程或安全指导。
6. **`remaining=0`**：只表示本电子本 6 个 paragraphId 已尽；不是人工 verified、不是全书校勘、不是产品交付、不是疑龙独立册已审。

## 未决（本岗不施工）

- 阙文、十二法缺一、L237 漏列、L337 疑句、库存 kind 待分类：保持 notes / 回源，不升 verified。
- 6 条 source-reviewed 不是人工 verified，也不是风水效验，也不等同风水算法已实现。
- 本岗不回改注解、不拆合刊、不碰 `yilong-jing` / 447/448/449 / SK1609。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-453`。该书 SR 审查 remaining **0**。
