# Draft 注解去向 · Round 5

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线 SHA：`3191806`（round4：升 16，全局 draft 2905 / source-reviewed 59934）  
范围：优先玉匣记识典剩余 180、六壬秘本主文本 86、紫微识典 SDZJ0170 48、麻衣主文本 17 与识典层 222、小文件 4+4+2+2+2+1+1。**未重做奇门 nlc-layouts 升审。未重做约言 nlc-recovery 升审。未重做已升条目。大六壬 kind=待核实 695 不升。未处理全部 draft，不虚报 2905 已清空。**

规则执行摘要：

- 能对照电子原文核实、且 notes 无待核/疑/残/粘连的，才升 `source-reviewed`；`verified` 保持非 true（电子对照 ≠ 人工影印校勘）。
- 繁简/异体只用于检索，未改写引用原文。
- 缺底本、疑字、图残、跨行残、粘连待核、kind=待核实、□/■：保留 `draft`，notes 写清原因。
- 空 notes 本轮仍为 0；麻衣识典 4 条原先 notes 未写明残/□，只补原因，不升。
- 未把理论/目录/案例/重复改成规则；择日/相法/紫微/风水/禄命去向是知识库，未伪造成已接入算法。
- 本会话未执行 `git commit` / `git push`；未改 product 仓；未碰 `/Users/sync/code`。

## 总量

| 项 | 数量 |
|---|---|
| Round4 结束后全局 draft | 2905 |
| Round4 结束后全局 source-reviewed | 59934 |
| 本轮升 `source-reviewed` | **0** |
| 本轮处理后全局 draft | **2905** |
| 本轮处理后全局 source-reviewed | **59934** |
| 奇门 nlc-layouts | 未打开升审（仍 1261 draft，ocr-draft 拦截） |
| 约言 nlc-recovery | 未打开升审（仍 162 draft，ocr-draft 拦截） |

0 升。2905 未变。不把未升的玉匣 180、秘本 86、紫微 48、麻衣 17+222、大六壬 812、奇门 1261、约言 162、小文件 16 算作已清空。

本轮对照电子本后，优先清单里 **没有**「可核电子本且 notes 无待核/疑/残/粘连」的条目。看起来像完整句的，要么 notes 仍写疑字，要么电子本下段才把句子写完，要么带 □。不凑数升。

## 分文件

### 1. `references/annotations/selection/yuqia-ji--shidian-NA09036.json`

| | 前（round4） | 后 |
|---|---|---|
| draft | 180 | **180** |
| source-reviewed | 2808 | 2808 |
| 本轮升 | **0** | |

`source_status` 全是 `reference-text`。对照 `sources/normalized/shidianguji/NA09036/text.md`。择日/符咒入知识库，不接入算法。`verified` 未设 true。

筛法：draft 且 kind≠待核实，源文无图像占位/□■、长度≥6。得到 29 条「看起来像完整格」。**0 条**以句号收束；29 条 notes 仍有残/疑/截/粘连。按硬规则全部不升。

**抽核（不升）：**

| paragraphId | 抽核要点 |
|---|---|
| `yuqia-ji:shidian-NA09036:P7655682801127849993` | L470「甲午乙未因申丁酉戍戌已玄庚子宰丑…」。因申/已玄/宰丑未唯一还原。 |
| `yuqia-ji:shidian-NA09036:P7655682801128570889` | L488「任子葵丑…聖膏」。疑字不改正文。 |
| `yuqia-ji:shidian-NA09036:P7655682842417135662` | L3445「天凹…所水和合以處世字此滅」。粘连/疑字。 |
| `yuqia-ji:shidian-NA09036:P7655682857755754542` | L5588「大安小起…臾目日中迤」。段末截断，不补起法。 |
| `yuqia-ji:shidian-NA09036:P7655682801098817586` | L303「羡士耳未…若人求福祭」。段未完。 |
| `yuqia-ji:shidian-NA09036:P7655682857633939483` | L5448「累火吞一道大吉」。形近 round3 已升符咒格，但 notes 仍标疑字，不跟着重升。 |

**为何留下 180（互斥：kind=待核实 → 残/截/未完 → 疑字）：**

| 原因 | 条数 |
|---|---:|
| kind=待核实 | 34 |
| 残字/残句/段残/截断（含过短残格、栏题残字） | 108 |
| 疑字/原文讹字 | 38 |
| **合计** | **180** |

与 round3 留下口径一致（当时过短 2 条 notes 同时写残，本轮归入残类）。无空 notes。

---

### 2. `references/annotations/san-shi/liuren-miben.json`

| | 前 | 后 |
|---|---|---|
| draft | 86 | **86** |
| source-reviewed | 2557 | 2557 |
| 本轮升 | **0** | |

`source_status` 为 `reference-text`。对照 `sources/fulltext/san-shi/liuren-miben/fulltext.md`。无 hold 关键词的只剩 3 条，均不是可核完整句。

**抽核（不升）：**

| paragraphId | 抽核要点 |
|---|---|
| `liuren-miben:L3453-L3453` | 中传岁「方来过去」方向含糊。信息不完整。 |
| `liuren-miben:L1392-L1392` | 句末「屠」缺，不补。 |
| `liuren-miben:L6015-L6018` | 尚未全书逐行异本校勘。inventory 标 doubtful。 |
| `liuren-miben:L3001-L3001` | 「水宿」疑水缩/水涸，不改正文。 |
| `liuren-miben:L3327-L3327` | 冲句电子本缺字，残缺不补。 |

**为何留下 86（互斥：kind=待核实 → 待核 → 粘连 → 疑 → 残）：**

| 原因 | 条数 |
|---|---:|
| kind=待核实 | 25 |
| 待核 | 46 |
| 疑字/存疑 | 6 |
| 信息不足/未展开 | 3 |
| 粘连（notes 无「待核」） | 2 |
| 残/缺字 | 2 |
| 待影印 | 1 |
| 未完成全书校勘 | 1 |
| **合计** | **86** |

`liuren-miben--shidian-SDZJ0628.json` 本轮未改（仍 61 draft）。不升运行规则。

---

### 3. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

| | 前 | 后 |
|---|---|---|
| draft | 48 | **48** |
| source-reviewed | 1022 | 1022 |
| 本轮升 | **0** | |

`source_status=reference-text`。对照 `sources/normalized/shidianguji/SDZJ0170/text.md`。Round4 已把误标「段末未完」而实际收束的 12 条升走。本轮 48 条电子本复核：残表、疑字、跨行截、图像占位仍在，**没有**新的误标完整段。紫微入知识库，不接入八术。

**抽核（不升）：**

| paragraphId | 抽核要点 |
|---|---|
| `P7356158877072703525` | 子宫残表，无庙旺标注。 |
| `P7356158869208383514` | 段中图像占位，不补字。 |
| `P7356158873473925171` | 纳音歌电子本已全，但丙戍屋上王、已卯等疑字不改正文。 |
| `P7356158890129653797` | 断句紊乱不臆补；娼婢条件为七杀单居福德。 |
| `P7356158895213150246` | 昌曲投河忧截于「一星轻」，不补后文。 |
| `P7356158877584441381` | 先𠢄終懶，孤例疑字。 |

**为何留下 48（互斥）：**

| 原因 | 条数 |
|---|---:|
| kind=待核实残表 | 12 |
| 疑字（含孤例字形 / 鿄 / ■） | 15 |
| 跨行残 / 段末截断 | 14 |
| 残表 / 残简（非待核实） | 4 |
| 图残 / 图像占位 | 2 |
| 断句紊乱不臆补 | 1 |
| **合计** | **48** |

---

### 4. 麻衣

#### 4a. `references/annotations/physiognomy/mayi-shenxiang.json`（主文本）

| | 前 | 后 |
|---|---|---|
| draft | 17 | **17** |
| source-reviewed | 1610 | 1610 |
| 本轮升 | **0** | |

对照 `sources/fulltext/physiognomy/mayi-shenxiang/fulltext.md`。16 条 kind=待核实（卷六现代白话附益）；1 条过短。

| paragraphId | 不升原因 |
|---|---|
| `mayi-shenxiang:L2891-L2891` | 电子本仅「又」一字 |
| `mayi-shenxiang:L4299-L4299` | 现代附益「看发相论尊贵」，不可作原典一线 |

#### 4b. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json`

| | 前 | 后 |
|---|---|---|
| draft | 222 | **222** |
| source-reviewed | 627 | 627 |
| 本轮升 | **0** | |

用户口径：只升无残无□。对照 `sources/normalized/shidianguji/NGJ89241199903149974518/text.md`。

筛完：源文无图/□■、notes 无残截、长度>4 的只剩 **2** 条，电子本都是跨行残句：

| paragraphId | 电子本 | 下段 | 处理 |
|---|---|---|---|
| `P7598367380087734312` | 「…如差偏不齐，則衣。」 | L100「虧，於此可見。」 | 补 notes，不升 |
| `P7598367453714055208` | 「…雖然生一子，却换。」 | L359「正此謂也。」 | 补 notes，不升 |

另 2 条 notes 未写 □，源文有 □，同样只补 notes：

| paragraphId | 原因 |
|---|---|
| `P7598367462934822952` | 「辞复□」缺字 |
| `P7598367464205221888` | 段末单独「□」 |

**为何留下 222（互斥：图 → □/■ → 过短残目 → 句截）：**

| 原因 | 条数 |
|---|---:|
| 图残/图像未转写 | 50 |
| □/■缺字 | 71 |
| 句截/段末未完/残句 | 81 |
| 过短/残字残目 | 20 |
| **合计** | **222** |

相法入知识库，不冒充已接入八术。

---

### 5. 小文件（空 notes 核对）

全局 draft 空 notes = **0**。下列文件本轮 0 升，原因已写。

| 文件 | draft | 不升原因 |
|---|---:|---|
| `fengshui/tianyu-jing--shidian-SK1592.json` | 4 | 跨行残：兩邊安 / 截于贵 / 截于惊动 / 两处阙 |
| `fengshui/dili-bianzheng--shidian-SDZJ0504.json` | 4 | kind=待核实；蒋序讹字过密；两卷题过短残句 |
| `xingming/xingxue-dacheng--shidian-SK1609.json` | 2 | kind=待核实；版面标记无字；源文仅「阙」 |
| `luming-nayin/yuzhao-shenying--shidian-SK1602.json` | 2 | kind=待核实；版面标记占位 |
| `bazi/sanming-tonghui--shidian-HY1521.json` | 2 | kind=待核实；河洛图残；「相芜」疑字 |
| `selection/xingli-kaoyuan--shidian-SK1618.json` | 1 | 版面标记占位，缺底本文字 |
| `luming-nayin/luoluzi-sanming--shidian-SK1605.json` | 1 | kind=待核实；版面标记占位 |
| **小计** | **16** | |

抽核：`tianyu-jing:shidian-SK1592:P7640236008973942794`（仅「两边安」）；`xingxue-dacheng:shidian-SK1609:P7640428574264541234`（仅「阙」）；`xingli-kaoyuan:shidian-SK1618:P7639153109960949787`（无转存文字）。

---

### 6. 本轮明确不做

- `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json`：1261 draft，ocr-draft 校验拦截。不重做升审。
- `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`：162 draft，同样 ocr-draft 拦截。不升。
- `references/annotations/san-shi/daliuren-daquan.json`：812 draft，kind=待核实 695 一律不升。其余 117 带待核/疑/残/粘连；过滤后仍是 round4 那 6 条信息不足（`L9187` `L9423` `L9443` `L9517` `L9749` `L10614`），不升、不改 JSON。

## 本轮保留 draft 的原因分类（已打开优先文件 + 复核不升的大六壬）

优先文件 569 条互斥（玉匣 180 + 秘本 86 + 紫微 48 + 麻衣主文本 17 + 麻衣识典 222 + 小文件 16）：

| 原因 | 条数 | 文件 |
|---|---:|---|
| kind=待核实 | 98 | 玉匣 34 + 秘本 25 + 紫微残表 12 + 麻衣主文本 16 + 地理辨正 4 + 星学 2 + 玉照 2 + 三命 2 + 珞琭子 1 |
| 残/截/未完/过短残格 | 108 | 玉匣 |
| 句截/段末未完 | 81 | 麻衣识典 |
| □/■缺字 | 71 | 麻衣识典 |
| 疑字/原文讹 | 59 | 玉匣 38 + 紫微 15 + 秘本 6 |
| 图残/图像未转写 | 52 | 麻衣识典 50 + 紫微 2 |
| 待核 | 46 | 秘本 |
| 过短/残目 | 21 | 麻衣识典 20 + 麻衣主文本 `L2891` |
| 跨行残/段末截断 | 18 | 紫微 14 + 天玉经 4 |
| 残表/残简（非待核实） | 4 | 紫微 |
| 信息不足/未展开 | 3 | 秘本 |
| 粘连 | 2 | 秘本 |
| 残/缺字 | 2 | 秘本 |
| 待影印 | 1 | 秘本 |
| 未完成全书校勘 | 1 | 秘本 |
| 断句紊乱 | 1 | 紫微 |
| 版面标记/缺底本 | 1 | 星历考原 `P7639153109960949787` |
| **优先文件小计** | **569** | |

98+108+81+71+59+52+46+21+18+4+3+2+2+1+1+1+1 = 569。

大六壬 812 本轮只复核不升：kind=待核实 695；其余 117 仍带待核/疑/残/粘连/信息不足（过滤后 6 条仍不升）。

未作为本轮主目标打开：奇门 1261 + 约言 162 + 秘本识典 61 + 皇极 40 = **1524**。

569 + 812 + 1524 = **2905**。对得上。不虚报清空。

本轮升 **0**。全局仍余 **2905**。

## 实际修改的 JSON

1. `references/annotations/physiognomy/mayi-shenxiang--shidian-NGJ89241199903149974518.json` — 4 条仍为 draft，只补残/□/跨行不升原因（`P7598367380087734312`、`P7598367453714055208`、`P7598367462934822952`、`P7598367464205221888`）

其余优先文件未改。`paragraphId` 无改动。`verified: true` 出现次数仍为 0。空 notes 仍为 0。

## 下一轮建议（不在本轮做）

1. 优先清单里可核且 notes 干净的已经没有了。再升必须先能还原残格/疑字/□，或先改奇门/约言源层 ocr-draft。
2. 大六壬 812 以 kind=待核实 695 为主；过滤后 6 条仍信息不足，不要为凑数升。
3. 紫微剩余 48、玉匣剩余 180、麻衣识典 222 仍是残表/疑字/段截/图像/□。
4. 麻衣主文本 16 条现代附益不得升作原典。
5. 择日/相法/紫微/风水已核条目只进知识库，不要在产品仓接线。

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
  "source_reviewed": 59934,
  "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
  "errors": []
}
```

对照 Round4 结束 `source_reviewed` 59934 / `draft` 2905：本轮 +0 / −0。校验器声明这只是结构与段落 ID 检查，不是语义证书，更不是人工 verified。

本会话未执行 `git commit` / `git push`。
