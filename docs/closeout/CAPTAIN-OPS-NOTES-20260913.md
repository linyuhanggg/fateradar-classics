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
