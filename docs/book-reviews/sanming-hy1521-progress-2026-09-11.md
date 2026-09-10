# 三命通会识典 HY1521 语义注解进度 · 2026-09-11

独占文件：`references/annotations/bazi/sanming-tonghui--shidian-HY1521.json`。本会话只改本书注解与本进度文档。

## 源核

- worktree `sources/normalized/shidianguji/HY1521/text.md` SHA256 = `707ac9bc6796bdb679833fc280040485d95b36da6f7aca0b3e2adbb9e57d19d3`，与队列及原集成库一致。
- `load_source_paragraphs` / `paragraphs.json` 共 2340 段，首尾 ID 与 checkpoint 边界一致。
- 识典补本 `source_status=reference-text`，电子语义阅读可升 `source-reviewed`；`verified` 一律 false。不是影印校勘，不把补本当独立投票证据。
- 网站章节名与印本卷号可能不一致；正文卷题已见「卷之一」等，引用仍以正文为准。

## 队列

8 个 checkpoint，2340 段全部待语义阅读。现队列未再排除段落；1423 条转录校对门槛排除不适用于本补本这 2340 段，不能自行把未校影印升为校勘完成。

## Checkpoint 1（索引 0–299）

- 300 条已写入；校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=300`，`source_reviewed=298`，`errors=[]`。
- `verified` 全部 false。draft 2：`P7467786007220338740` 河洛图说碎行；`P7458198190622310419` 残句「人力相芜」。
- 覆盖：卷前/蒋国祥序/王谦序/河洛辩/总目，原造化、干支源流、纳音多算法、禄命身、六十甲子、神头禄与妙选六十、十干可为金木水火土、纳音与正五行、四季喜忌、徐大升过犹不及、卷一终；卷二河图洪範八干纳卦化属、十干阴阳生死、土两生与拟土歌否定、地支月提、天文地理取象、醉醒子、属相、人元司事两套日数、节气日刻、太阳躔次太阴纳甲、天月二德、旺相休囚死、寄生十二宫、遁月时、年月日时三主三限、定真论六亲。
- 条件/救应/反转已写入条目，未把未算条件当默认真。纳音多法、洪範与正五行、阳死阴生与四大长生、徐大升废纳音与罗青霄必用洪範均保留流派差异，不投票。
- 电子阅读不是影印校勘或预测有效证据。

## 进行中

Checkpoint 2 = 索引 300–599。
