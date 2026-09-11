# 地理辨正 · 识典 SDZJ0504 语义审读进度 · 2026-09-11

独占文件：`references/annotations/fengshui/dili-bianzheng--shidian-SDZJ0504.json` 与本进度文档。未改主本 `dili-bianzheng.json`（仅 2 段），不碰蒋注原经一线、引擎、`chart.*`、源文 `sources/normalized/shidianguji/SDZJ0504/**`。未把网站章节名当印本卷号。

## WORK_PACKAGE_COMPLETE（CP2）

本包 CP2 索引 **300–599**（最多 300 段）全部有实质处理：新增 `source-reviewed` 300，`verified` 全 false。CP1 索引 **0–299** 从只读快照原样继承，未改写。全文件 `entries=600`（含 CP1 既有 4 条 `draft`）。不是地理辨正全书完成，也不是人工 verified；索引 **600–992**（remaining **393**）留给后续包。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-160`
- 分支：`codex/multica-ming-160`（自只读权威树 `fateradar-classics-grok-full-library` @ `1fd3a37` 新建；未 checkout 覆盖 MING-128）
- CP1 继承：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-128/references/annotations/fengshui/dili-bianzheng--shidian-SDZJ0504.json`（entries=300，对象级与现文件 0–299 一致）
- `sources/normalized/shidianguji/SDZJ0504/paragraphs.json` SHA256 = `e024485bcbc368c7ec8a435873e9c818e9e4ce0b1aef60e190cd6908fe06ced6`（993 段，与派工一致）
- 网站章节名不等于印本卷号；识典补本不替代主本、不作独立投票证据
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 直解/章氏增补、蒋注、姜注与经文分层；疑字、缺图、〔此处为字形或图像〕占位不改正文

## 段落账本（本批 300/300 · CP2；累计 600/993）

| 区段 | 索引 | 起讫 paragraphId 尾 | 处理摘要 |
|---|---|---|---|
| 地理辨正卷四（中篇收束→下篇） | 300–372 | P…6646710311–P…0413661203 | 阳水阴山、山情水意、宾主、奇门比论；平洋曲水/中阳/内阳；下篇山龙龙虎飞与水局形法；蒋注/直解/姜注分层 |
| 地理辨正卷之五 | 373–414 | P…4548689935–P…6624189483 | 卷五辨伪/黄泉矛盾/公位与玉尺驳；姜垚总括歌及被否定板法；缺图占位不补字 |
| 心眼指要卷首 | 415–416 | P…3513535529–P…6896442422 | 附编起首题署/序目 |
| 心眼指要卷一 | 417–437 | P…6897261622–P…0530295858 | 八交/八极神枢等纲领，非八术接入 |
| 心眼指要卷二 | 438–553 | P…1019705383–P…0699895846 | 说卦往顺来逆、八大局/八阵、洛书理气、三字经排龙、乘生气、认脉生死、审理气与分目 |
| 心眼指要卷之三（至 CP2 止） | 554–599 | P…4686100516–P…8304939034 | 穴形窝钳乳突及图占位；残句/分目不补造 |

ID 前缀：`dili-bianzheng:shidian-SDZJ0504:`。

- 起始：`dili-bianzheng:shidian-SDZJ0504:P7549187526646710311`
- 本批止：`dili-bianzheng:shidian-SDZJ0504:P7579290848304939034`（索引 599）
- **nextId**：`dili-bianzheng:shidian-SDZJ0504:P7549187548170551335`（索引 600）不在本包
- 全书末：`dili-bianzheng:shidian-SDZJ0504:P7561132792207622153` 留给后续包
- **remaining**：393（索引 600–992；全书识典 993 段）

CP2 kind 分布（仅本批）：规则候选 139 · 术语 42 · 理论 34 · 序跋目录 33 · 待核实 29 · 评注或元数据 14 · 操作步骤 7 · 案例 2。

## 质量要点（节录）

- 阳水阴山配合：气运消长之阴阳，非干支板格、非左右到、非上下元固定配水
- 山情水意 / 宾主：用法得宜与气止水交分层，不把俗情意当算法
- 奇门比论：时师用错被否定；大五行配合在动静之间，不写成奇门排盘接入
- 黄泉/净阴净阳/三合长生等被驳条目不得反作认可算法
- 心眼指要分目与残句只标题义，未列细法不补猜
- 〔此处为字形或图像〕占位：`待核实`，不据异体提示补字
- 禁止模板填白话；条件/救应/反转/未知分开；`verified` 全 false

疑文/未决：缺图字形不补；残句不补造；口诀未列处不写已实现算法；风水进入可检索知识库 ≠ 八术接入 / 预测有效。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/fengshui/dili-bianzheng--shidian-SDZJ0504.json --json
```

结果：`ok=true`，`entries=600`，`source_reviewed=596`（CP1 既有 draft 4 + CP2 source-reviewed 300），`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包。
