# captain 运行札记（2026-09-13）

> 记录执行机制层面的实测结论，供后续轮次避免误判与重复动作。不是验收证据，也不改变任何验收状态。

## 1. 成员活跃度的正确探针

**现象**：`team.json` 里 4 名成员长期显示 `status: idle`，而任务仍是 `in_progress`、工作树又长时间无新文件 —— 极易误判为「成员停了」。

**有效探针**：看各成员**自己的会话文件是否在增长**：

```bash
ls -la ~/.dsh/sessions/--Users-sync-code-fateradar-classics--/<member-subagent-id>/session.jsonl.zstd
```

2026-09-13 10:26 实测：

| 成员 | session.jsonl.zstd | 最后写入 |
|---|---|---|
| algo-impl | 1.95 MB | 10:26 |
| reviewer | 1.16 MB | 10:24 |
| classics-audit | 320 KB | 10:24 |
| page-acceptance | 272 KB | 10:25 |

→ **当时四名成员都在活跃执行**。`team.json.status` 只是持久状态字段（成员 turn 之间的常驻值），**不能**当作 live 判据。

**据此调整的 captain 节奏**：
- 只在「成员会话文件连续多轮不再增长」时才判定停滞并补发消息；
- 成员活跃期间反复补发「继续」会把 inbox 塞满，让成员把回合耗在重读指令上，反而降低吞吐；
- 成员执行期间，captain 应做**不与成员文件冲突**的工作：账本维护、main 集成、独立复核、交付报告骨架。

## 2. 工具使用札记（避免丢工作）

- 本环境的**持久 bash 会偶发超时/重置**，尤其是「heredoc + 多命令 + 中文参数」组合；`git commit -m` 传中文参数会被 shell 吞掉多字节字符（会用 `-F <消息文件>` 或纯 ASCII 消息）。
- `git commit` 在本仓偶发长时间挂起，用 `timeout 60 git -c gc.auto=0 commit ...` 稳定通过（怀疑触发 `gc --auto`）。
- 因此**重要写入一律用文件编辑工具或脚本文件**，不用 heredoc 直写；提交后用 `git log -1` 回读确认落地。


## 3. captain 自造的重跑事故（2026-09-13 round 30）—— 我违反了要求成员遵守的同一条纪律

**事件**：我在工作树直接跑 `python3 tools/export-source-cases.py`（11:02:24），而该生成器取 **HEAD 归档**作为 candidates 输入；
当时 HEAD 的 `qimen-component-candidates.json` 仍是旧措辞 → 产物「混血」：字段名已是「值符落宫数／值使落宫数」，但**说明文字 3,076 处回到「原宫」**。
更严重的是：**这次重跑覆盖了 classics-audit 手工改好、尚未提交的 `source-cases.json`**（该改动已不可恢复）。

**根因（比表象更深，已定位）**：案例 `reading`/`notes` 文本**不是来自 candidates**，而是来自**上游**：
`references/annotations/**`、`inventory/supplemental/**`、`nlc-layout-page-reviews.json`、`collation-notes.md`
（大概率还有 `sources/normalized/san-shi/qimen-dunjia-tongzhi/*.md` 的 table_reading/notes）。
**只要上游还是旧措辞，每次重跑都会把「原宫」带回来**——手工改 `source-cases.json` 属治标。

**已采取的处置**：captain 裁定**统一上游措辞**（只改描述 starPalaceRaw/doorPalaceRaw 这批数字的措辞；凡是「原宫」作为**概念**本身的表述——如口径句「仅 376 条与原宫一致」——必须原样保留），
改完再重跑导出器并自检 `值符落宫数=1918 / 值符原宫数=0 / 原宫 仅概念性表述`；`source-cases.json` 由 captain 提交。

**教训（写给后续轮次的我自己）**：
- 「重跑/重生成前先固定输入快照」这条纪律**对 captain 同样适用**；我此前用它要求成员，自己却直接在工作树上跑了生成器。
- **提交顺序会影响再生结果**：生成器读 HEAD 归档时，必须先提交上游输入、再重跑生成器；否则产物是「新生成器 × 旧输入」的混血。
- **绝不要在多人在途写作的工作树上跑会覆盖产物的生成器**——它会静默吃掉别人未提交的手工修正。重跑前先 `git status` 看清在途编辑，必要时等对方提交或改用快照目录。
