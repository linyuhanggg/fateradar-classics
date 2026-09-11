# corpus-3 工作包进度 2026-09-10

lane: `codex/grok-fast-corpus-3-20260910`  
worktree: `/Users/yuhanglin/.codex/worktrees/fateradar-grok-fast-corpus-3`  
权威方案只读；未改 GOAL_PROGRESS / inventory / 主本五行精纪 / 大六壬大全；未 push；未停 dispatcher。

## 问题

队列 16 个 job（P0→P1→P2）要求按真实段落 ID 做电子语义审读：作用对象、前提、否定、例外、反转、救应与未知。补本不得当主本独立投票。`verified` 一律 false。validator 只做结构/ID 检查，不是语义证书。

## 原文锚点（SHA 均与队列一致）

| job | SHA256 前缀 | IDs | 关键原文 |
|---|---|---|---|
| yuqia P0 小六壬 | `d75c0737` | 19 | 月上起日、日上起时；大安身不动 |
| wuxing-jingji 补本 | `29ee1245` | 493 | 背禄逐马「逐非追」 |
| xingxue-dacheng SK1609 | `0d0f3106` | 398 | 提要驳乔庙；冲能致吉；有验有不验 |
| li-xuzhong SK1601 | `6eee34bd` | 76 | 元和称载作伪；空亡有用 |
| sanming-tonghui SK1610 | `9833d244` | 322 | 只取正官正印等馆臣层 |
| yuanhai NGJ | `94cbf77c` | 1988 | 有病方为贵 |
| bushi-zhengzong HY0057 | `8483ae06` | 627 | 卜筮正宗补本 |
| minghai HY1442 | `e33a3582` | 1058 | 余星救驾；禄主五条并得用；被土制之下元膀胱。`runtimeEvidenceAllowed=false` |
| zangshu SK1588 | `43570473` | 30 | 郭璞未著葬书；力小图大不可泥 |
| qingnang-xu SK1590 | `4727bfe7` | 40 | 阳山阳向荒唐；退神宜退亦同旺 |
| yuqia DZ1480 | `9375baaa` | 154 | 五福通日不问值隔 |
| shenxiang SDZJ0174 | `00e07f58` | 748 | 尽系于相非也 / 不系于相亦非也；水星来救护 |
| xuexin-fu SDZJ0175 | `329cd1bb` | 326 | 以龙为先；指鹿为马 |
| yuqia 主本其余 | `d75c0737` | 1760 | 小小祈福半吉 / 上章拜表大凶 |
| shenshi-xuankong-xue | `030a5ddd` | 1191 | 峦头无伪书、理气多伪诀；三元三合须参用骑墙可哂 |
| huangji-jingshi | `aeceef2a` | 8789 | 易外别传；朱子推步之书；数出于理违理入术；不诚不可以得道 |

## 实际变更（独占 annotation 文件）

已完成全部 15 个 owned 文件。玉匣记主本先 19 后 1760 追加，未覆盖小六壬。命海/李虚中/皇极等长段 `subsections` 覆盖父段起迄。图像/空段保持 `draft`。

## 测试命令与结果

均在本 worktree 运行：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations <file> --json`

| 文件 | ok | entries | source-reviewed | draft |
|---|---|---|---|---|
| minghai HY1442 | true | 1058 | 1054 | 4 |
| shenxiang SDZJ0174 | true | 748 | 748 | 0 |
| yuqia-ji.json（19+1760） | true | 1779 | 1779 | 0 |
| shenshi-xuankong-xue | true | 1191 | 1180 | 11 |
| huangji-jingshi | true | 8789 | 8788 | 1 |

先前已验证并提交：yuqia 19、wuxing-jingji 493、xingxue-dacheng 398、li-xuzhong 76、sanming 322、yuanhai 1988、bushi 627、zangshu 30、qingnang-xu 40、yuqia DZ1480 154、xuexin-fu 326。

validator 注释原文：`Structural and source-ID checks only; not a semantic or human review certificate.`  
未跑全库 export；未做 typecheck（本包无 TS 变更）。未编造浏览器验收。

## 未决项

- `verified=false`：电子语义审读 ≠ 影印校勘 ≠ 人工 verified ≠ 预测有效。
- 命海全编仅研究参考，不得写入运行时证据链。
- 补本不能当主本独立投票；网站章节名 ≠ 印本卷号。
- 皇极经世约 6333 条短表仅标去向，不是独立吉凶断。
- 1423 OCR-threshold 段落不在本包。
- 未 push；未 SIGTERM dispatcher。

## Commits（本地）

- `b5f0632` yuqia-ji 小六壬 19
- `f70f145` wuxing-jingji 补本 493
- `3daffc5` xingxue-dacheng SK1609 398
- `7694e4b` li-xuzhong SK1601 76
- `1a53569` sanming-tonghui SK1610 322
- `14efec4` yuanhai NGJ 1988
- `3aad45b` bushi-zhengzong HY0057 627
- `a8baa4e` minghai HY1442 1058
- `edee5bd` zangshu SK1588 30
- `a12041e` qingnang-xu SK1590 40
- `4ec7aea` yuqia DZ1480 154
- `3bd1c88` shenxiang SDZJ0174 748
- `975334e` xuexin-fu SDZJ0175 326
- `1f8ea33` yuqia remaining 1760
- `78e1cfe` shenshi-xuankong-xue 1191
- `b0ec83d` huangji-jingshi 8789
