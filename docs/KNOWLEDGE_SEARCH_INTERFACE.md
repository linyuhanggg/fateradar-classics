# 知识库检索接口（交给 Web）

风水、相法、择日、禄命纳音等 33 包**没有**对应八术页面。本接口只提供检索，不排盘、不断吉凶。

## 数据

古籍仓 `codex/grok-full-library`：

- 全量包：`references/inventory/library-inventory.json`
- 知识库索引：`references/inventory/knowledge-index.json`
- 段落：`references/inventory/paragraphs/{system}/{slug}.json`
- 原文：`sources/fulltext/{system}/{slug}/fulltext.md` 行号 = 段落 ID 中的 `Lxxxx`

## 字段

| 字段 | 含义 |
|---|---|
| slug | 资料包 |
| title | 书名 |
| system | catalog 系统 |
| art / art_label | 内容分类，不是已接入术数 |
| paragraph id | `{slug}:Lstart-Lend` |
| fulltext | 原文路径 |
| not_an_art_page | 恒为 true |

## 样例

《葬书》`zangshu:L0007-L0025` → `sources/fulltext/fengshui/zangshu/fulltext.md` 第 7–25 行。

《协纪辨方书》去向是 knowledge，不能在八字页当神煞引擎。

## 不要做

- 不要把这些段落送进 `buildBazi` / `buildZiwei` 等排盘函数
- 不要用关键词共现当规则命中
- 不要在本任务里改后台、billing 或大范围页面
