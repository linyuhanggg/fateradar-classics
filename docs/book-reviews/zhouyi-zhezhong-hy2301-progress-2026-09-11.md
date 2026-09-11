# 御纂周易折中 · 识典 HY2301 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json`（新建）与本进度文档。未改源文 `sources/normalized/shidianguji/HY2301/**`。不碰主本 `zhouyi-zhezhong.json`、HY1521、SK1609、SDZJ0170、引擎、`chart.*`。禁止重做主本 0–899。

## WORK_PACKAGE_COMPLETE（CP1）

本包 CP1 索引 **0–299**（300 段）全部有实质处理：`source-reviewed` 300，`verified` 全 false。不是御纂周易折中全书完成，也不是人工 verified，也不是引擎包；索引 **300–680** 留给后续包。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-176`
- 分支：`codex/multica-ming-176`（基线只读权威树 `fateradar-classics-grok-full-library` @ `1fd3a37`）
- `sources/normalized/shidianguji/HY2301/paragraphs.json` SHA256 = `511d3e2a9a022444133ab985197a51f879d6d0f50d3e0f423243c9206a63c86c`（681 段，与 Issue 一致）
- `sources/normalized/shidianguji/HY2301/text.md` SHA256 = `3daa58177a204d86c55bbe4156fc645f408e03a6990a07a7ee45104c1d617fc1`
- 稳定 ID 与 `tools/source_paragraphs.py` / `references/source-editions.json` 中 `shidian-HY2301` 对齐
- `catalogComplete: false`；缺章不补造；网站章节名 ≠ 印本卷号核定
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 不 OCR、不抓站；不与主本折中段落 ID 混写

## 段落账本（300/300 · CP1）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 御制序 | 0–2 | `…P7675240779413241875`–`…P7477804283506720806` | 书名/序题与御制序宗旨 |
| 凡例 | 3–15 | `…P7675240779413274643`–`…P7477804283506802726` | 本义优先、程传/集说/案语体例与啟蒙附论安排 |
| 卷端 | 16–17 | `…P7571881320146681883`–`…P7571881320146698267` | 「御纂周易折中」「卷第九」目录标记 |
| 彖上传 | 18–35 | `…P7571881320146714651`–`…P7675240907662278675` | 本义·程传·集说·案语分层；含同人「曰」衍文提示 |
| 象下传 | 36–299 | `…P7554438476210176043`–`…P7675240944312877099` | 大象/小象原文与本义·程传·集说分层；止于鼎九三相关程传/案 |

- 起始：`zhouyi-zhezhong:shidian-HY2301:P7675240779413241875`
- 本批止：`zhouyi-zhezhong:shidian-HY2301:P7675240944312877099`（索引 299）
- **nextId**：`zhouyi-zhezhong:shidian-HY2301:P7675240944312893483`（索引 300）不在本包
- **remaining**：381（索引 300–680；全书 681 段）
- 全书末：`zhouyi-zhezhong:shidian-HY2301:P7510771359308382243` 留给后续包

### CP1 kind 分布

- `规则候选`：276
- `理论`：15（凡例等体例/读法）
- `序跋目录`：9（书名、序题、卷端、传题）

## 质量要点

- 禁止模板填白话；本义/程传/集说/案语分层，条件/救应/反转/未知分开
- 短标题与卷端仅作序跋目录；短象辞须连同后续分层读，不单句取象
- `verified` 全 false；非人工校勘
- 不与主本 `zhouyi-zhezhong.json` 混写；不替代主文本投票

### doubtful / unknown（本包）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `zhouyi-zhezhong:shidian-HY2301:P7499645407132909606` | 23 | 段内含电子源疑文提示；保留 unknown，不补造 |
| `zhouyi-zhezhong:shidian-HY2301:P7499645407132958758` | 26 | 本义「衍文」+程传「此三字義文」（同人曰）；保留 unknown，其余分层仍对读 |
| `zhouyi-zhezhong:shidian-HY2301:P7499645407132975142` | 27 | 段内含电子源疑文提示；保留 unknown，不补造 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/zhouyi-zhezhong--shidian-HY2301.json --json
```

结果：`ok=true`，`entries=300`，`source_reviewed=300`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包。识典网站章节名不当作印本卷号。
