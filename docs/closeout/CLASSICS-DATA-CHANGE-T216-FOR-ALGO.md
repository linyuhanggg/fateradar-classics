# 消费方数据版本 · t216 消费方表全量扫描（无新增缺口）＋ `liuyao.structure` 定义提议

日期：2026-09-21。基线提交：`a3dc491`（t215 后）。
**本轮无规则/谓词数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`c5bba9be08c4080107a5a001a6e0b886ae34a558`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两件事：把 t215 那类「**暗中退化**」系统性扫干净（结论：**没有第二个会退化的表**，
且把它变成回归测试）；以及给长期阻塞的 `liuyao.structure`（17 条记录）**一份有据的定义提议**——
读过 17 条使用者的原文条件之后，它的所指不再是「完全未知」，而是**两种可辨的读法**，
留给人工裁定，**本轮不落地**。

## 1. 消费方表全量扫描

t215 查出 21 个键缺消费方标签、**瞒了十轮**。本轮按同一类风险系统扫：字符串键的表
（若写成 `Record<FactKey, …>`，tsc 会拦；问题只出在 `Record<string, …>`）。

| 表 | 键是什么 | 结论 |
|---|---|---|
| `chart-emphasis.ts` `FORTUNE_TEXT` | 吉／凶／平／主 | 与事实键无关 |
| `admin-policy.ts` `VERIFICATION_LABEL` | 验证状态 | **已经把 `provisional` 显示为「待核验」**——本仓规则的 verification 在产品侧本来就不冒充「已验证」 |
| `rules/terms.ts` | 同义词→规范名 | 缺条目只是不做归一，**不退化** |

**没有第二个会退化的表** —— 即 t215 的修复是完整的。

### 并把这一类变成回归

新增 `tests/engine/fact-label-coverage.test.ts`（产品侧，已入测试集）：

1. `fact-vocab.json` 里**每个键**都必须在 `LABELS` 里；
2. `LABELS` 里不得有词表之外的可疑键（历史遗留的 4 个展示层标签显式列出，防拼写漂移）；
3. 检查本身**非空跑**（确实读到了词表与标签表）。

> 它之所以能红：`LABELS` 是 `Record<string, string>` 而**不是** `Record<FactKey, string>`，
> 所以漏登记 tsc 拦不住——**这正是它潜伏十轮的原因**。

## 2. `liuyao.structure`：从「两仓无定义」到**有据的提议**

t183 判定：该名在两个仓都只被使用、从未定义；按「原文没写就不写」**不猜所指** →
17 条记录长期只能报「信息不足」。本轮换了个动作：**把 17 条使用者的 `when`／`satisfy_when` 逐条读过**。

**新证据**：

- 17 条**全部**是 `when: {exists: "liuyao.structure"}`；
- `satisfy_when` 描述的全是**逐爻结构分析**：节点临月／同月五行未破、旺相静爻被日冲、
  真实动位的变爻对本位形成生克冲合、同元素进退支对、伏用得日月飞或动生、
  日支／动爻支／变爻支落墓绝位、三支在真实三位置齐全……
  → 都以「**本卦的逐爻结构层已就位**」为前提。

**提议**（不是裁定）：

| | |
|---|---|
| 所指 | `liuyao.structure` ＝「本卦的逐爻结构事实齐备」 |
| 代理键 | `yao_zhi`（逐爻必有；任何构建成功的六爻盘都有六枚）——与 t205 给 `positions` 的处理同理 |
| 若落地 | 17 条记录从「未提供定义表／信息不足」变为**可判** |

**同时写明反证**：这 17 条的 `satisfy_when` 所描述的分析，**引擎自己已有实现**
（`liuyao-analysis.ts` 的 `ruleChecks` 按 ZSB-E-01…E-19 编排）→ 「structure」**也可能**指
「引擎已算完那一层」，而不只是「事实层有键」。

**两种读法留给人工裁定；本轮不改 `FIELD_MAP`。**
另记一项前置：`liuyao.node.element`（爻五行）仍未产出（谓词侧 0 客户，故未加）。

台账 `tools/reports/liuyao-structure-proposal.json`；
测试 `tools/test-structure-proposal.py`（入 CI）钉四件事：
**提议未落地**（`FIELD_MAP` 里该字段仍接不上）、17 条齐全、每条都有 satisfy_when、
代理键真实存在且**每张六爻盘恰好六枚**。

## 3. 可执行层跨盘汇总（现状）

| | 条数 |
|---|---:|
| 至少一张盘可判 | 229 |
| 任何盘都判不了 | **29** |
| ├ 引用接不上 FactKey 的字段 | 22 |
| ├ 语料无构成定义 | 4 |
| └ 事实键在任何样盘都不在场 | 3 |

（22 里最大一块仍是 `liuyao.structure` 的 17 条 —— 正是本轮提议要解的那一块。）

## 4. 未决清单（承接 t215）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **`liuyao.structure` 的读法裁定** | **本轮给出提议与反证**：①逐爻结构在场（代理键 `yao_zhi`）②引擎已算完结构分析层。待人裁定后可立即落地（①即刻可判 17 条） |
| 2 | `liuyao.node.element`（爻五行） | 落地上项的**前置**：引擎有 `element`，事实层无键；谓词侧 0 客户故未加 |
| 3 | 新增 FactKey 必须登记消费方标签 | 已有**回归测试**（`fact-label-coverage.test.ts`），不再靠偶然发现 |
| 4 | 梅花余项／易理余项 | 断法表（恒真）不写；`-016` 变卦所指有歧义；`-007` 卦主口径多歧；`-026` 需计数与爻辞层 |
| 5 | 撤回谓词 5 条所需事实 | 限类型／制化、星属南斗北斗、大限序列与武贪格 |
| 6 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 7 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/test-structure-proposal.py            # 提议未落地 + 17 条齐全 + 代理键逐爻必有
python3 -c "
import json;d=json.load(open('tools/reports/liuyao-structure-proposal.json'))
print(d['status']); print('提议代理键:', d['proposed_mapping']['fact_key']); print('反证:', d['caveat'][:80])"
python3 tools/eval-executable.py --all --across | sed -n '5,12p'

# 消费方标签回归（产品仓）
cd /Users/sync/code/cosmic-fortune-lab
FATERADAR_CLASSICS=/Users/sync/code/fateradar-classics npx vitest run tests/engine/fact-label-coverage.test.ts

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
cd /Users/sync/code/fateradar-classics
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/domain-check.py
python3 tools/verification-depth-report.py
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`c5bba9be08c4080107a5a001a6e0b886ae34a558`。
产品仓 `generated/*.json` 无需重新导出；`tsc --noEmit` exit 0；
产品侧 **3574 passed / 0 failed**（新增 3 项：`fact-label-coverage`）。

**给消费方的两条说明**：

1. 新增回归测试 `tests/engine/fact-label-coverage.test.ts`：
   以后**任何**新增 FactKey 若没在 `LABELS` 登记，会立刻测试红，而不是像 t184–t215 那样
   悄悄退化成「盘面：值」。
2. `liuyao.structure` 的裁定若选「逐爻结构在场」，则 17 条 executable 记录会同时变为可判——
   届时 `FIELD_MAP` 会多一条映射（`liuyao.structure → yao_zhi`），本仓会在交付文档里写明。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。