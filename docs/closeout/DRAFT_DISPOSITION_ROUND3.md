# Draft 注解去向 · Round 3

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线 SHA：`8910542`（round2：升 213，全局 draft 3013 / source-reviewed 59826）  
范围：优先玉匣记、麻衣识典层、大六壬剩余可核条目；顺带约言 nlc-recovery notes、皇极 DZ1040、六壬秘本识典空 notes。**未重做奇门 nlc-layouts 升审。未处理全部 draft，不虚报 3013 已清空。**

同轮过程中工作树被后续提交钉过检查点（`705fa38` 玉匣 70 图占位、`1975564` 玉匣 16+大六壬 5、`b37fc2f` 保留原因 notes）。本文件按用户交付要求汇总 **round2 结束后 → 本轮结束** 的真实去向，不以中间短稿代替全量。

规则执行摘要：

- 能对照电子原文核实的，升 `source-reviewed`；`verified` 保持非 true（电子对照 ≠ 人工影印校勘）。
- 繁简/异体只用于检索，未改写引用原文。
- 缺底本、疑字、图残、跨行残、粘连待核、kind=待核实：保留 `draft`，notes 写清原因。
- 空 notes 本轮补上具体原因（六壬秘本识典层 17 条）。
- 未把理论/目录/案例/重复改成规则；择日/相法/符咒去向是知识库，未伪造成已接入算法。
- 本会话未执行 `git commit` / `git push`；未改 product 仓；未碰 `/Users/sync/code`。

## 总量

| 项 | 数量 |
|---|---|
| Round2 结束后全局 draft | 3013 |
| Round2 结束后全局 source-reviewed | 59826 |
| 本轮升 `source-reviewed` | **92**（玉匣图占位 70 + 玉匣可核正文 16 + 玉匣遗漏图占位 1 + 大六壬 5） |
| 本轮处理后全局 draft | **2921** |
| 本轮处理后全局 source-reviewed | **59918** |
| 奇门 nlc-layouts | 未打开升审（仍 1261 draft，ocr-draft 拦截） |

92 = 70 + 16 + 1 + 5。2921 = 3013 − 92。不把未升的麻衣 222、约言 162、皇极 40、大六壬剩余 812、玉匣剩余 180 算作已清空。

分提交对照（便于对账，不是又一轮）：

| SHA | 升 | 全局 draft |
|---|---:|---:|
| `8910542` round2 | 213 | 3013 |
| `705fa38` 玉匣图占位 | 70 | 2943 |
| `1975564` 玉匣单元格 16 + 大六壬 5 | 21 | 2922 |
| 本工作树未提交：玉匣遗漏图占位 1 | 1 | **2921** |

## 分文件

### 1. `references/annotations/selection/yuqia-ji--shidian-NA09036.json`

| | 前（round2） | 后 |
|---|---|---|
| draft | 267 | **180** |
| source-reviewed | 2721 | **2808** |
| 本轮升 | **87**（70 图占位 + 16 可核正文 + 1 遗漏图占位） | |

`source_status` 全是 `reference-text`（不是 ocr-draft）。择日/符咒入知识库，不接入算法。`verified` 未设 true。

#### 1a. 图占位 71（70 已在 `705fa38`，1 条本工作树补升）

电子本原文一律是：

```
〔此处为图像，未转文字；请对照本段原网页。〕
```

升审核实的是「电子本此段无转写文字」，不是对照原图内容，不是择日/六壬盘式。

**抽核：**

1. `yuqia-ji:shidian-NA09036:P7655682809017270318` — L869 图像占位（70 批首）
2. `yuqia-ji:shidian-NA09036:P7655682809017450542`
3. `yuqia-ji:shidian-NA09036:P7655682809084674099`
4. `yuqia-ji:shidian-NA09036:P7655682857407528986`（70 批近末）
5. `yuqia-ji:shidian-NA09036:P7655682857755705390` — 本工作树补升。notes 原文是「图像占位，不转写、不补图。」（比 70 批多「不补图」），电子本同样无转写。不伪装为六壬盘式。

#### 1b. 可核正文 16（`1975564`）

对照 `sources/normalized/shidianguji/NA09036/text.md`，源文是完整单元格或短条件句，白话已对照，notes 无待核/残/粘连。不改正文疑形。

| paragraphId | 抽核要点 |
|---|---|
| `yuqia-ji:shidian-NA09036:P7655682801099243570` | L358「乙未曰諸神在天若人作福不得小声」。只记本格禁令，吉凶在邻格 |
| `yuqia-ji:shidian-NA09036:P7655682842014728201` | 不将吉日格「丁酉戊戌」 |
| `yuqia-ji:shidian-NA09036:P7655682842014760969` | 「戊戌巳未」 |
| `yuqia-ji:shidian-NA09036:P7655682842089177114` | 「辛丑丁巳」 |
| `yuqia-ji:shidian-NA09036:P7655682842417250350` | 出行将军图月次「三月六月」 |
| `yuqia-ji:shidian-NA09036:P7655682846007541806` | 六畜日「六月亥卯未日」 |
| `yuqia-ji:shidian-NA09036:P7655682846007590958` | 六畜日「辛酉」 |
| `yuqia-ji:shidian-NA09036:P7655682857520873510` | L5247「十步送之即愈」。符咒送步，不是算法覆盖 |
| `yuqia-ji:shidian-NA09036:P7655682857520594982` | 「門上貼一道吉」 |
| `yuqia-ji:shidian-NA09036:P7655682857520578598` | 「一道吉吞二道」 |
| `yuqia-ji:shidian-NA09036:P7655682857575333926` | 「人貼房門大吉」 |
| `yuqia-ji:shidian-NA09036:P7655682857634250779` | 「用貼門上大吉」 |
| `yuqia-ji:shidian-NA09036:P7655682857699950630` | 「吞一道佩一道」 |
| `yuqia-ji:shidian-NA09036:P7655682842525138982` | 碧玉经「月晦北不利」 |
| `yuqia-ji:shidian-NA09036:P7655682842014253065` | 周堂格「床周堂路」 |
| `yuqia-ji:shidian-NA09036:P7655682842014220297` | 周堂格「行嫁死睡門」 |

邻行抽核：L354–356 甲午求福上吉 vs L358 乙未不得小声；L5241 二十步送之大吉 vs L5247 十步送之即愈。不连成月日全表。

#### 为何留下 180

| 原因（互斥） | 条数 | 说明 |
|---|---:|---|
| kind=待核实 | 34 | 卷首残字、图注残、符图残，硬规则不升 |
| 残字/残句/段残/截断 | 107 | 栏题残、圣诞格残、段未完 |
| 疑字/原文讹字 | 37 | 因申/已玄、任子葵丑、天凹、聖膏等不能唯一还原 |
| 过短/不能识 | 2 | `P7655682801630871603` 仅「月」；`P7655682801744035891` 月次表头残 |
| **合计** | **180** | |

未升例（禁止凑数）：

- `P7655682801127849993` 源文「因申、戍戌、已玄、宰丑」，疑字未唯一还原
- `P7655682801128570889` 「任子葵丑、聖膏」
- `P7655682842417135662` 「天凹…所水和合以處世字此滅」粘连/疑字
- `P7655682857755754542` 起法「大安小起…臾目日中迤」段末截断，不补起法

---

### 2. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json`

| | 前 | 后 |
|---|---|---|
| draft | 222 | **222** |
| source-reviewed | 627 | 627 |
| 本轮升 | **0** | |

Round2 已补 22 条空 notes。本轮按「无残无待核」筛：222 条几乎全是图像未转写、□/■ 缺字、阙文、句截、段末未完。唯一看起来干净的 `P7626030500910268454` 源文「两天倉，两地阁」，下段才接「为天倉」，跨行未完，**不升**。`P7598367464321368099` 仅「形厚」两字短题，**不升**。notes 已写明原因。相法入知识库，不冒充已接入八术。

留下 222：图残/图像未转写 50；残/阙/截/未完/缺字 171；短目/短题 1。

`mayi-shenxiang.json`（非识典层）本轮未改。

---

### 3. `references/annotations/san-shi/daliuren-daquan.json`

| | 前 | 后 |
|---|---|---|
| draft | 817 | **812** |
| source-reviewed | 6076 | **6081** |
| 本轮升 | **5** | |

用户口径：剩余 817 中 kind≠待核实 且 notes 无「待核/疑字/残/粘连」才考虑升。kind=待核实 695 一律不升。`source_status` 均为 `reference-text`。对照 `sources/fulltext/san-shi/daliuren-daquan/fulltext.md`。

**升 5 条（电子对照完成、无待核/疑字/残/粘连）：**

| paragraphId | 抽核要点 |
|---|---|
| `daliuren-daquan:L6352-L6352` | 勾陈制玄武/游都必胜；玄武克勾必败。原文「太禽」按太常通读，不改正文。兵占 overlay 不改取传 |
| `daliuren-daquan:L6549-L6549` | 将星故未解：月将/登明/岁破/勾陈四说并存，unknown，不改 adapter |
| `daliuren-daquan:L10751-L10759` | 订讹三奇：止有干奇不名三奇不得删。电子本「癸日戊」不改正文戌 |
| `daliuren-daquan:L7070-L7070` | 本段下贼上名元首利客。与九宗门上克下为元首两歧，只归档本段 |
| `daliuren-daquan:L7072-L7072` | 本段上克下名重审利主。与九宗门下贼上为重审两歧，只归档本段 |

**过滤后仍不升、只补 notes 的典型：**

| paragraphId | 原因 |
|---|---|
| `L9187` | 「于亥日」缺天干、「午加加申」衍加 |
| `L9252-L9262` | 「如《心镜?」残缺 |
| `L9280` | 地支行是否天将待核 |
| `L9483` | 叠字「必必待」疑字 |
| `L9171` | 「矿决」疑「故决」 |
| `L11172-L11186` | 「朱誉」疑朱雀 |
| `L6507` `L6635-L6690` `L7223-L7230` | 已/己混 |
| `L10781-L10790` | 「戊寅日己卯日」粘连 |
| `L9423` `L9443` `L9749` `L9989` | 先克/先举/存疑，信息不足 |

**为何留下 812：**

| 原因（互斥） | 条数 |
|---|---:|
| kind=待核实 | 695 |
| 疑字/疑读 | 45 |
| 待核 | 37 |
| 残/缺字 | 22 |
| 粘连 | 9 |
| 信息不足/明确不升 | 4 |
| **合计** | **812** |

未升例：`L0098` 井栏粘连待文渊阁；`L9691`「宙」疑寅。

---

### 4. `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`

| | 前 | 后 |
|---|---|---|
| draft | 162 | **162** |
| source-reviewed | 619 | 619 |
| 本轮升 | **0** | |

162 条源层全是 `ocr-draft`。校验器：`source_status==ocr-draft` 不得标 `source-reviewed`。本轮只补 notes，不升。

- 4 条原先已写「源层 ocr-draft，保持 draft」
- 158 条补：「源层 ocr-draft，校验器禁止升 source-reviewed，保持 draft。」

抽核：`mingli-yueyan:nlc-recovery:P000:L003-L011`（恢复稿来源说明）、`P001:L005-L005`（封面缺字，kind=待核实）、`P179:L002-L003`（页末定位元数据）。白话均自承现代恢复/定位，不作古书原句。

---

### 5. `references/annotations/divination/huangji-jingshi--shidian-DZ1040.json`

| | 前 | 后 |
|---|---|---|
| draft | 40 | **40** |
| source-reviewed | 2221 | 2221 |
| 本轮升 | **0** | |

40 条全是段末未完/截断、OCR 断行、残表、□ 缺字或疑倒。按与大六壬相同规则 **不升**，notes 补「段末未完/截断/疑字/残表，不升 source-reviewed。」

抽核：

- `huangji-jingshi:shidian-DZ1040:P7377235377297457161` — 星辰序「辰。/辰」疑阙
- `P7377302235006369819` — 「国曰□」不补国名
- `P7377302290190925875` — 残表 ○ 不补格
- `P7377302333119545394` — 「德不可有」疑倒，不改正文

`huangji-jingshi--shidian-SK1573.json` 本轮无 draft，未改。

---

### 6. `references/annotations/san-shi/liuren-miben--shidian-SDZJ0628.json`

| | 前 | 后 |
|---|---|---|
| draft | 61 | **61** |
| source-reviewed | 1118 | 1118 |
| 本轮升 | **0** | |

Round2 写明本文件未打开。本轮发现 17 条 draft **空 notes**（全局仅此 17 条）。全部补原因，**不升**（残行、过短、kind=待核实）。

| paragraphId | 补上的原因 |
|---|---|
| `P7549319963380187175` | 甲申旬仪神残行，kind=待核实 |
| `P7549319963380252711` | 甲辰旬仪神旬表残 |
| `P7549319963380269095` | 奇神未标旬名，衔接不明 |
| `P7597138910159306803` | 仅「酸醋类」过短 |
| `P7570421055468060672` | 宿度续行残，不补十二将 |
| `P7549319971295494207` | 「同意甲子旬在辰」过短 |
| `P7570421063827718179` | 仅「二宿」残字 |
| `P7570421063827734563` | 仅「传」过短残字 |
| `P7549319972829577252` | 远近贵人前/后残句，不补里程公式 |
| `P7570421064408006656` | 仅「巳」残字 |
| `P7570421067089788980` | 仅「晓」残字 |
| `P7570421067089903668` | 戌亥辰巳过短，不补孤虚表 |
| `P7549319979125391396` | 孤虚残表；神符玉女禹步不当成起课步骤 |
| `P7570421070316306467` | 仅「昼」残字 |
| `P7573648484054745107` | 仅「下」残字 |
| `P7573648484054892563` | 仅「罡」残字 |
| `P7549319993108742198` | 「来远近皆可俱同是无之义」过短 |

补完后全局 draft 空 notes = 0。

---

### 7. 本轮明确不做

- `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json`：1261 draft，ocr-draft 校验拦截。Round1/2 已说明。本轮不重做升审。

## 本轮保留 draft 的原因分类（仅已打开文件）

| 原因 | 条数 | 文件 |
|---|---:|---|
| kind=待核实 | 755 | 大六壬 695 + 玉匣 34 + 秘本识典 26 |
| 残/缺字/段末未完/截断 | 300 | 玉匣 107 + 麻衣 171 + 大六壬 22 |
| 疑字/疑读 | 82 | 玉匣 37 + 大六壬 45 |
| 待核 | 37 | 大六壬 |
| 图残/图像未转写 | 50 | 麻衣（玉匣图占位已升） |
| ocr-draft 元数据（不得升） | 1423 | 奇门 1261 + 约言 162 |
| 皇极段末/OCR/残表 | 40 | 皇极 DZ1040 |
| 粘连 | 9 | 大六壬 |
| 信息不足/明确不升 | 4 | 大六壬 |
| 过短/短题 | 3 | 玉匣 2 + 麻衣 1 |
| 秘本识典层其余（已有 notes 的 draft） | 35 | 61 − 26 已计入待核实；17 空 notes 已补仍 draft |

打开文件剩余：玉匣 180 + 麻衣 222 + 大六壬 812 + 约言 162 + 皇极 40 + 秘本识典 61 + 奇门 1261 = **2738**。  
全局 2921 − 2738 = **183** 是未作为本轮主目标打开的文件（六壬秘本主文本 88、紫微 60、星历考原 1、麻衣主文本、round1 小文件保留等）。

本轮升 92。全局仍余 **2921**。不虚报清空。

## 实际修改的 JSON

1. `references/annotations/selection/yuqia-ji--shidian-NA09036.json` — 87 条 review→source-reviewed（70+16+1），若干保留条补疑字原因
2. `references/annotations/san-shi/daliuren-daquan.json` — 5 条升审；过滤后仍 draft 的补「不升」原因
3. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json` — 2 条短目/短题补原因，review 未升
4. `references/annotations/bazi/mingli-yueyan--nlc-recovery.json` — 158 条补 ocr-draft 不得升
5. `references/annotations/divination/huangji-jingshi--shidian-DZ1040.json` — 40 条补不升原因
6. `references/annotations/san-shi/liuren-miben--shidian-SDZJ0628.json` — 17 条空 notes 补原因，review 未升

`paragraphId` 无改动。`verified: true` 出现次数仍为 0。

## 下一轮建议（不在本轮做）

1. 大六壬剩下 812 以 kind=待核实 695 为主，须先能对照电子本还原残格/疑字，禁止批量标不支持。
2. 麻衣识典层 222 仍全是残图/□/句截，不要整文件升。
3. 奇门 nlc-layouts 1261 仍被 ocr-draft 拦截；升审必须先改源层，不是注解层能单独完成。
4. 约言 162 同样必须先完成转录审读。
5. 择日/相法/符咒已核条目只进知识库，不要在产品仓接线。

## 验证命令与结果

工作目录：`/Users/yuhanglin/fateradar-goal-20260912/classics`

```bash
python3 tools/validate-annotations.py
python3 tools/validate-annotations.py --json
```

纯文本结果：

```
53 books, 62839 entries, 0 errors
```

JSON 摘要：

```json
{
  "ok": true,
  "books": 53,
  "files": 79,
  "entries": 62839,
  "source_reviewed": 59918,
  "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
  "errors": []
}
```

对照 Round2 结束 `source_reviewed` 59826 / `draft` 3013：本轮 +92 source-reviewed、−92 draft，与玉匣 87 + 大六壬 5 一致。校验器声明这只是结构与段落 ID 检查，不是语义证书，更不是人工 verified。

本会话未执行 `git commit` / `git push`。
