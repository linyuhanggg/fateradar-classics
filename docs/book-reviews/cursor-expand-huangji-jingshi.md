# 《皇极经世书》电子本逐段审读（cursor 工作包）

状态：进行中。基线 `d47f77d` 的 corpus-3 初稿只做了结构铺满，大量条目复制古文或套“作用对象是元会运世”模板，声音表也被标成元会序号格，不能当语义验收。本包从独立分支按真实段落 ID 重审；`verified` 一律 false。

## 范围与独占文件

- 原文只读：`sources/fulltext/divination/huangji-jingshi/fulltext.md`（SHA256 `aeceef2a…`，与队列一致）
- 注解：`references/annotations/divination/huangji-jingshi.json`（8789 条，与 inventory ID 对齐）
- 账本：`docs/book-reviews/cursor-expand-huangji-jingshi-remaining.json`
- 未改原文、其他书注解、inventory、公共导出、算法、依赖、main

仓内无独立 `AGENTS.md`/`CLAUDE.md`；执行口径以 `docs/FATERADAR_FULL_LIBRARY_PLAN.md` 为准：目录序跋、重复、案例、理论、疑文各有去向；非八术材料进知识库，不造算法规则。

## 已完成章节（本轮累计）

| 章 | 段数 | 处理 |
|---|---:|---|
| 提要与卷首空白 | 2 | 馆臣提要重写，保留议者否定与“责成人事/非术数家”转折；空页保持 draft/unknown |
| 卷十一 观物51–56 | 7 | 天地四象、妄知妄言、四府、皇帝王伯、因革四命、饩羊/履霜 |
| 卷十二 观物57–62 | 6 | 受命等第、舜武桓狄、三变、十六位、体用数、以物观物 |
| 卷十三 外篇上 | 16 | 体四用三、数出于理/违理入术、未然之防、不诚不可以得道、历法≠历理 |
| 卷十四 外篇下 | 27 | 太极神数象器、以我观物情偏而暗、用兵条件、学际天人 |
| 附录索隐 | 3 | 张行成别书分层，截断不补字 |

关键限定已写入相应段，不再只当标语：易外别传、朱子推步之书、数出于理违理入术、不诚不可以得道、以物观物 / 不以我观物、有数而不见、名存实亡犹愈于俱亡。

## 未完成

卷一一至卷十共 8728 段：元会运世坐标格、以运经世史事纪、卷七至十声音唱和与年表混排。短表只标去向，但必须写出该格的章次、栏名与原文字面；史事要译出现代白话；声音表不得再标成元会序号格；□■○不补字。

## 验证

`python3 tools/validate-annotations.py --annotations references/annotations/divination/huangji-jingshi.json --json`：结构/ID 通过，8789 条，source-reviewed 8788，draft 1。该校验不是语义证书，也不是人校。
