# corpus-1 古籍接力 · 2026-09-10

独占交付记录。电子语义审读 ≠ 影印校勘，≠ 人工 verified，≠ 术数预测有效。`verified` 一律 false。识典补本不计独立投票。

## 问题

P0《大六壬秘本》识典 SDZJ0628 1179 段待语义标注。网站章节名与印本卷号不一致；卷四/五/七/八百章歌题记重出；金氏旁注与正文分层；残表、图像占位、乾隆题记夹在口诀中。

## 原文锚点（checkpoint 1）

- 文件：`sources/normalized/shidianguji/SDZJ0628/text.md`
- SHA256：`eda976a95ca7b31142c67a1f3368e2a1047839426a4e3b61f6f2e0a0e0b0f304`（与队列一致）
- 段 0–299：`liuren-miben:shidian-SDZJ0628:P7549318767957573695` … `P7549319971295641663`
- 关键条件/否定/救应：
  - 二日一轮旺相，否定「四季分五行之用」（约 L1669 山阴道士 / 苗公密宝）
  - 课式活法：每月三十日三周、每旬十日一遍；甲乙日像春序是日干当令，不是日历春（约 L1681）
  - 乾卦逢火即软、遇水即坚；散而不全
  - 空亡不可便为空；初空末实、末空实事作虚；天上变通、地下旬空（百章歌）
  - 破传初/中/末层次不同，不能凡破皆无成
  - 四课三传实则昌，重冲重破亦无妨；金氏改空仍旁注实
  - 白虎乘墓加支有伏尸；天鬼春酉夏午秋卯冬子；天鼠正月在子逆行
  - 占产克辰伤母克干儿；传财入空否定日上见财自排；先贵后空 / 先空后贵反转

## 实际变更

- 新增 `references/annotations/san-shi/liuren-miben--shidian-SDZJ0628.json`：300 条，覆盖 CP1 全部 ID。
  - source-reviewed 281，draft 19（旬煞残表、宿度残表、将名切断、过短残句）
  - 重复 32：卷五天乙/朱雀、卷六卦气、卷七十干表、卷七终/乾隆题记/百章歌起首重出
  - 长段用 subsections：十二天将混段、太常/白虎、百章歌 270/277
- 未改主本 `liuren-miben.json`，未改证据仓，未提升 verified。

## 测试命令/结果

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/san-shi/liuren-miben--shidian-SDZJ0628.json --json
```

实际结果：`{"ok": true, "books": 1, "files": 1, "entries": 300, "source_reviewed": 281, "errors": []}`。校验器只做结构与 ID，不是语义证书。

## 未决项

- P0 CP2–4：段 300–1178 未读。
- P1/P2 其余 12 个 job 未开始。
- 1423 条 OCR-draft 门槛不在本队列，不消除。
- 残表、金氏旁注、一云别说保持并存；疑字不改正文。

## commit

CP1 提交后回填哈希。
