# 可执行规则字段

进入运行系统的规则必须能连接：原文段落 → 适用条件 → 本盘事实 → 计算结果 → 白话 → 页面位置。

本文件只约定字段。旧 `rules.yaml` 仍是候选，不能当运行权威。

## 结果

`verdict` 只能是：

- `满足`
- `不满足`
- `信息不足`

缺少条件不能默认成立。未实现救应不能写成没有救应。不同流派分条记录，不投票。

## 字段

| 字段 | 含义 |
|---|---|
| id | 稳定 ID |
| art | 术数 |
| theme | 主题 |
| school | 流派；空则只标书名 |
| paragraph_id | 段落库 ID |
| quote | 原文摘录，须含转折/否定/例外所在范围 |
| page | 页面栏目 |
| required_facts | 本盘必须提供的位置化事实 |
| when | 适用范围 |
| satisfy_when | 满足 |
| fail_when | 不满足 |
| unknown_when | 信息不足 |
| rescue | `unimplemented` 或具体救应规则 ID |
| vernacular | 白话模板，必须能填入本盘位置 |
| implementation_assumption | 原文未明说、实现需要的假设 |
| verified | 仅人工影印校勘后为 true；模型不得改 |

事实使用柱、宫、星、爻、课、传等位置，不用整段关键词共现。
