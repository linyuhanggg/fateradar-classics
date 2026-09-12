# Draft 注解去向 · Round 4

日期：2026-09-12  
工作树：`/Users/yuhanglin/fateradar-goal-20260912/classics`  
分支：`dsh/full-library-classics`  
基线 SHA：`bdfd8ac`（round3：升 92，全局 draft 2921 / source-reviewed 59918）  
范围：优先六壬秘本主文本 88、紫微识典 SDZJ0170 60、大六壬剩余可核、麻衣主文本 19。**未重做奇门 nlc-layouts 升审。未重做约言 nlc-recovery 升审。未处理全部 draft，不虚报 2921 已清空。**

规则执行摘要：

- 能对照电子原文核实的，升 `source-reviewed`；`verified` 保持非 true（电子对照 ≠ 人工影印校勘）。
- 繁简/异体只用于检索，未改写引用原文。
- 缺底本、疑字、图残、跨行残、粘连待核、kind=待核实：保留 `draft`，notes 写清原因。
- 空 notes 本轮仍为 0，未新造空 notes。
- 未把理论/目录/案例/重复改成规则；择日/相法/紫微去向是知识库，未伪造成已接入算法。
- 本会话未执行 `git commit` / `git push`；未改 product 仓；未碰 `/Users/sync/code`。

## 总量

| 项 | 数量 |
|---|---|
| Round3 结束后全局 draft | 2921 |
| Round3 结束后全局 source-reviewed | 59918 |
| 本轮升 `source-reviewed` | **16**（六壬秘本 2 + 紫微识典 12 + 麻衣主文本 2） |
| 本轮处理后全局 draft | **2905** |
| 本轮处理后全局 source-reviewed | **59934** |
| 奇门 nlc-layouts | 未打开升审（仍 1261 draft，ocr-draft 拦截） |
| 约言 nlc-recovery | 未打开升审（仍 162 draft，ocr-draft 拦截） |

16 = 2 + 12 + 2。2905 = 2921 − 16。不把未升的大六壬 812、奇门 1261、约言 162、紫微剩余 48、麻衣剩余 17 算作已清空。

## 分文件

### 1. `references/annotations/san-shi/liuren-miben.json`

| | 前（round3） | 后 |
|---|---|---|
| draft | 88 | **86** |
| source-reviewed | 2555 | **2557** |
| 本轮升 | **2** | |

`source_status` 为 `reference-text`。对照 `sources/fulltext/san-shi/liuren-miben/fulltext.md`。邻行 L3019 / L3023、L3160 / L3164 已是 source-reviewed，本轮只升同样可核、notes 无待核/疑字/残/粘连的两句。`verified` 未设 true。不升运行规则。

**升 2 条：**

| paragraphId | 抽核要点 |
|---|---|
| `liuren-miben:L3021-L3021` | L3021「井欄射，《三元經》取馬發用，更捷。」只说取驿马，未给中末。不得用取马补全大全无克六日三传。 |
| `liuren-miben:L3162-L3162` | L3162「凡貴德臨身制鬼者，反吉。如乙丑乙巳，酉加巳發用，蛇制鬼例。」乙丑乙巳两日并列，不合并成一日。 |

**为何留下 86：**

| 原因（互斥） | 条数 |
|---|---:|
| 待核 | 39 |
| kind=待核实 | 25 |
| 疑字/存疑 | 6 |
| 粘连 | 6 |
| 残/缺字 | 5 |
| 信息不足/未展开 | 3 |
| 待影印 | 1 |
| 未完成全书校勘 | 1 |
| **合计** | **86** |

未升例（禁止凑数）：

- `L3001` 「水宿」疑水缩/水涸，不改正文
- `L3055` 「不腚顺」疑字改义
- `L3327` 冲句缺字，残缺不补
- `L6015-L6018` 尚未全书逐行异本校勘，inventory 标 doubtful

`liuren-miben--shidian-SDZJ0628.json` 本轮未改（仍 61 draft）。

---

### 2. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json`

| | 前 | 后 |
|---|---|---|
| draft | 60 | **48** |
| source-reviewed | 1010 | **1022** |
| 本轮升 | **12** | |

`source_status=reference-text`。对照 `sources/normalized/shidianguji/SDZJ0170/text.md`。Round2 把一批星曜专段标成「段末未完」。本轮按电子本段末复核：这 12 段实际以句号或完整韵句收束，白话先前截掉了已有的收束句。升审时补全白话、去掉误标，不改正文。紫微入知识库，不接入八术。`verified` 未设 true。

**升 12 条（抽核 8）：**

| paragraphId | 抽核要点 |
|---|---|
| `P7356158877957783589` | 廉贞。电子本收束「主残疾」，不是六甲句残。入庙武贵 / 巳亥弃祖 / 干支格分层。 |
| `P7356158878339366922` | 天府。「先大後小，有始無終」是收束，不是「先」字截断。甲庚安命亥卯未辰酉不贵。 |
| `P7356158878712676362` | 太阴诗。收束「空門出入得從容」，先前误标空字截断。寅上吉拱仍不丰。 |
| `P7356158878779752498` | 贪狼入限。收束「一命入泉郷」。原文四庫不改。无吉曜则入泉乡，不是段残。 |
| `P7356158879702548530` | 破军诗。「不見傷残的夀夭，只冝僧道度平生」是本段收束句，不是残文。 |
| `P7356158880394559497` | 文曲。收束「旺有暗痣，𨺻有班痕」。原文己酉丑，不改巳。 |
| `P7356158881128792115` | 禄存。收束「限倒其年入墓中」。禄马交驰怕劫空太岁恶星冲。 |
| `P7356158881367785523` | 陀罗。收束「弃祖入赘…僧道吉」，先前误标「入」字截断。 |

其余本轮所升：`P7356158878339596298`（太阴专段，六丁次之已在电子本）、`P7356158878985289765`（七杀，辰宫六庚人吉；𨿽按虽通读）、`P7356158878985519141`（破军专段，丙戊辰戌丑未紫微同垣）、`P7356158881367621683`（擎羊，不守祖业至否则僧道）。

**只补 notes、不升：**

| paragraphId | 原因 |
|---|---|
| `P7356158877584441381` | 先𠢄終懶，𠢄 孤例疑字 |
| `P7356158878779768882` | 石中𨼆玉，𨼆 孤例疑字 |
| `P7356158873473925171` | 纳音歌电子本已全；丙戍屋上王、已卯等疑字不改 |
| `P7356158882164506650` | 𠙚 不补字 |
| `P7356158894672052274` | 段截于「日子月」 |
| `P7356158872928895013` | 跨行残「就 / 從酉宫起紫㣲」 |
| `P7356158869376106523` | 奏書事士疑博士 |

**为何留下 48：**

| 原因（互斥） | 条数 |
|---|---:|
| kind=待核实残表 | 12 |
| 疑字（含孤例字形 / 鿄 / ■） | 14 |
| 跨行残 / 段末截断 | 13 |
| 残表 / 残简 / 后半残（非待核实） | 6 |
| 图残 / 图像占位 | 2 |
| 断句紊乱不臆补 | 1 |
| **合计** | **48** |

未升例：`P7356158877072703525` 子宫残表；`P7356158869208383514` 段中图像占位；`P7356158890129653797` 断句紊乱不臆补。

---

### 3. `references/annotations/san-shi/daliuren-daquan.json`

| | 前 | 后 |
|---|---|---|
| draft | 812 | **812** |
| source-reviewed | 6081 | 6081 |
| 本轮升 | **0** | |

用户口径：剩余 812 中 kind≠待核实 且 notes 无「待核 / 疑 / 残 / 粘连」才考虑升。kind=待核实 695 一律不升。过滤后只剩 **6** 条，全部仍有缺口，**不升、不改 JSON**。

| paragraphId | 不升原因 |
|---|---|
| `L9187` | 「于亥日」缺天干、「午加加申」衍加；计数未复算 |
| `L9423` | 「先克」未定义计时顺序，信息不足 |
| `L9443` | 未给出下贼是否同样取天盘孟仲，信息不足 |
| `L9517` | 将名重出待影印核 |
| `L9749` | 「先举」待与订讹对读，信息不完整 |
| `L10614` | 心镜寅时 / 本行午时异文并行 |

**为何留下 812：** 与 round3 相同。kind=待核实 695；其余 117 仍带待核 / 疑字 / 残 / 粘连 / 信息不足 / 待影印。未升例：`L0098` 井栏粘连待文渊阁；`L9691`「宙」疑寅。

---

### 4. `references/annotations/physiognomy/mayi-shenxiang.json`

| | 前 | 后 |
|---|---|---|
| draft | 19 | **17** |
| source-reviewed | 1608 | **1610** |
| 本轮升 | **2** | |

对照 `sources/fulltext/physiognomy/mayi-shenxiang/fulltext.md`。邻条 L2794 / L2796 / L2798、L2802 已是 source-reviewed。本轮只升完整标题行。相法入知识库，不冒充已接入八术。`verified` 未设 true。

**升 2 条：**

| paragraphId | 抽核要点 |
|---|---|
| `mayi-shenxiang:L2792-L2792` | L2792「目光有三脱：」标题，细则在邻条，不能单凭标题判人 |
| `mayi-shenxiang:L2800-L2800` | L2800「神色有三疑。」标题，细则在邻条 |

**留下 17：**

| 原因 | 条数 |
|---|---:|
| kind=待核实（卷六现代白话附益，不可作原典一线） | 16 |
| 过短标记（`L2891` 仅「又」） | 1 |
| **合计** | **17** |

未升例：`L2891` 电子本仅「又」一字；`L4299` 现代附益「看发相论尊贵」。

`mayi-shenxiang--shidian-NGJ89241199903149974518.json` 本轮未改（仍 222 draft）。

---

### 5. 本轮明确不做

- `references/annotations/san-shi/qimen-dunjia-tongzhi--nlc-layouts.json`：1261 draft，ocr-draft 校验拦截。Round1–3 已说明。本轮不重做升审。
- `references/annotations/bazi/mingli-yueyan--nlc-recovery.json`：162 draft，同样 ocr-draft 拦截。本轮不升。

## 本轮保留 draft 的原因分类（仅已打开文件）

| 原因 | 条数 | 文件 |
|---|---:|---|
| kind=待核实 | 748 | 大六壬 695 + 秘本 25 + 紫微残表 12 + 麻衣现代附益 16 |
| 待核 | 39 | 秘本 |
| 疑字/疑读 | 20 | 秘本 6 + 紫微 14 |
| 跨行残/段末截断 | 13 | 紫微 |
| 残/缺字/残简 | 11 | 秘本 5 + 紫微 6 |
| 粘连 | 6 | 秘本 |
| 信息不足/未展开 | 3 | 秘本 |
| 图残/图像占位 | 2 | 紫微 |
| 待影印 | 1 | 秘本 |
| 未完成全书校勘 | 1 | 秘本 |
| 断句紊乱 | 1 | 紫微 |
| 过短标记 | 1 | 麻衣 `L2891` |

打开文件剩余：秘本 86 + 紫微 48 + 大六壬 812 + 麻衣 17 = **963**。  
全局 2905 − 963 = **1942** 是未作为本轮主目标打开的文件（奇门 1261 + 约言 162 + 玉匣 180 + 麻衣识典 222 + 秘本识典 61 + 皇极 40 + round1/2 小文件保留等）。

本轮升 16。全局仍余 **2905**。不虚报清空。

## 实际修改的 JSON

1. `references/annotations/san-shi/liuren-miben.json` — 2 条 review→source-reviewed
2. `references/annotations/ziwei/ziwei-doushu-quanshu--shidian-SDZJ0170.json` — 12 条升审；7 条保留条更正 notes（误标段末未完 → 疑字/跨行/段截）
3. `references/annotations/physiognomy/mayi-shenxiang.json` — 2 条标题升审；`L2891` 补过短不升

`daliuren-daquan.json` 未改。`paragraphId` 无改动。`verified: true` 出现次数仍为 0。

## 下一轮建议（不在本轮做）

1. 大六壬剩下 812 以 kind=待核实 695 为主，须先能对照电子本还原残格/疑字，禁止批量标不支持。过滤后 6 条仍信息不足，不要为凑数升。
2. 紫微识典剩余 48 仍是残表/疑字/段截/图像，不要整文件升。
3. 奇门 nlc-layouts 1261、约言 162 仍被 ocr-draft 拦截；升审必须先改源层。
4. 麻衣主文本剩下 16 条是现代附益，kind=待核实，不得升作原典。
5. 择日/相法/紫微已核条目只进知识库，不要在产品仓接线。

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

对照 Round3 结束 `source_reviewed` 59918 / `draft` 2921：本轮 +16 source-reviewed、−16 draft，与六壬秘本 2 + 紫微 12 + 麻衣 2 一致。校验器声明这只是结构与段落 ID 检查，不是语义证书，更不是人工 verified。

本会话未执行 `git commit` / `git push`。
