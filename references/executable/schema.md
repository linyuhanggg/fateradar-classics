# 规则定义与电子文本来源字段

进入运行系统的规则必须能连接：原文段落 → 适用条件 → 本盘事实 → 计算结果 → 白话 → 页面位置。

本文件只约定字段。旧 `rules.yaml` 仍是候选，不能当运行权威。

当前版本：`fateradar-executable-v2`。这些 JSON 是规则定义与证据包；是否可执行、哪些分支已实现，由产品实现和测试另行证明，不能按 JSON 条目数宣称算法完成。

## 结果

`verdict` 只能是：

- `满足`
- `不满足`
- `信息不足`

缺少条件不能默认成立。缺少必需输入属于“信息不足”，不是“不满足”；没有独立反例的观察/来源条目明确标明没有不满足分支，不能为了凑三态虚构反例。未实现救应不能写成没有救应。不同流派分条记录，不投票。

## 字段

| 字段 | 含义 |
|---|---|
| id | 稳定 ID |
| art | 术数 |
| theme | 主题 |
| school | 流派；空则只标书名 |
| paragraph_ids | `sources` 中真实段落库 ID，按来源顺序去重；不能用任意行范围造 ID |
| sources | 一条或多条准确来源摘录，字段见下表 |
| quote | 各来源摘录以 `\n[…]\n` 连接的展示文本；保留省略符，不能另行改写 |
| page | 页面栏目 |
| required_facts | 本盘必须提供的位置化事实 |
| when | 适用范围 |
| satisfy_when | 满足 |
| fail_when | 不满足 |
| unknown_when | 信息不足 |
| rescue | `self`（本条自身即救应条款）、`unimplemented`（原文有救应条款、引擎尚未实现）、`none`（原文没有救应条款，本条无可实现）、或真实救应规则 ID |
| vernacular | 白话模板，必须能填入本盘位置 |
| implementation_assumption | 原文未明说、实现需要的假设 |
| named_gaps | 可选。具名登记：影响判断而原文未界定／读法待定／口径待定的条件，逐条写进条款并附可复算计数与逐字证据行（见下节） |
| verified | 当前全部 false；电子文本匹配、模型审查和测试不能代替人工影印核验 |

事实使用柱、宫、星、爻、课、传等位置，不用整段关键词共现。

## 具名登记（`named_gaps`）

「原文未界定」「读法待定」「引擎给信息不足属口径」这类条件必须**写在条款内**，不能只留在过程稿或审计报告里。
每条登记都要能被独立复核，字段如下：

| 字段 | 含义 |
|---|---|
| kind | `source-term`（术语／读法）或 `verdict-scope`（判定口径） |
| term / topic | 登记对象；`source-term` 用 `term`，`verdict-scope` 用 `topic` |
| status | `source-term`：`criterion-stated`（原文给出取法）／`partially-stated`（给出部分判据）／`source-undefined`（原文未给判据）／`reading-undetermined`（读法待定）；`verdict-scope`：`named-scope-decision` |
| claim_checked | 本次要核的原判（写清出处），便于第三方复核是否被推翻 |
| finding / decision | 复核结论；`verdict-scope` 写口径决定 |
| occurrences / lines_with_term | 该术语在本书全文的出现处数与行数；`verdict-scope` 同义字段为 `cue_occurrences` / `cue_lines`（cue＝口径所本的原文说法） |
| evidence | 原文证据行：`paragraph_id` + `start_line`／`end_line` + `quote`（quote 必须是这些行的逐字片段，且至少一条含登记词） |
| readings | `reading-undetermined` 必填，至少两条读法并列，**不替原文择一** |
| not_claimed | `verdict-scope` 必填：不得由本登记推出的结论 |
| effect | 本登记对判定语义的影响；须写明保留了哪条 `rescue` 标签、是否影响满足分支 |

校验器对这些字段要**重算**：`occurrences`／`lines_with_term`（及 `cue_*`）必须与当前全文逐字相符，
证据行必须落在真实段落内且是原文逐字片段，含登记词。原文一变，登记即校验失败，须重新核对——
登记不能靠自报数字成立。

登记本身**不改变** `satisfy_when`／`fail_when`／`unknown_when` 三态语义，也不提升 `verified`：
`source-undefined` 不等于「可以不给判据」，`criterion-stated` 也不等于「已经实现」。

## 来源摘录

| 字段 | 含义 |
|---|---|
| paragraph_id | 对应 `references/inventory/paragraphs/{system}/{slug}.json` 内确实存在的 ID |
| start_line / end_line | 在该段落内部截取的原文行范围，均为从 1 开始、含边界 |
| quote | 原文件上述行逐字连接的文本；保留原有繁简、校注、转折和否定，不猜改疑字 |

跨段摘录使用多个 `sources`。段落标识和摘录范围各司其职：例如原文 L1116 属于 `ziping-zhenquan:L1111-L1116`，不能把 `L1116-L1116` 当作一个已建档段落。不同位置的原文不能只挂在一个范围下面。原文件版本由内容发布提交标识；段落 ID 仅对该原文版本成立。

来源中出现吉凶、成格或破格措辞，表示电子原文如此，不表示本盘算法已经满足相应条件。代码未计算的力量、气候或救应条件仍须输出信息不足。ZPR-E-06 当前明确没有可启用的“满足”分支，不能因原书例文存在就自动成立。

## 校验边界

`python3 tools/validate-executable.py` 校验本目录全部 JSON 的字段、唯一 ID、真实段落引用、原文行范围、逐字引文、摘要拼接、救应依赖和 `named_gaps` 具名登记（计数重算＋证据逐字比对）。它不验证古籍预测、规则语义是否完整或产品执行是否正确。

`python3 tools/test-validate-executable.py` 用独立小文本验证跨段成功，以及外键悬空、超范围、篡改引文、遗漏来源、无效救应、具名登记计数不符／证据伪造等失败分支。两条命令均进入 `.github/workflows/validate-rules.yml`；旧 YAML 和 reading-notes 校验继续保留。

逐条来源调整记录见 `SOURCE_REVIEW.md`。
