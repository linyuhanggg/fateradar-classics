# 消费方数据版本 · t207 谓词语言表达力审计（回答目标里那条判断）

日期：2026-09-21。基线提交：`224512a`（t206 后）。
**本轮无规则/谓词数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`275ac4c7bd84528431d41db930d4bd09cc3b9b22`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标里写着「**不是缺事实，是谓词语言的表达力不够**」。本轮把这句话**逐类核对**了一遍：
按 37 轮施工中**实际遇到**的条件形状归类，每类附证据与需求规模。

结论：**这句话现在只对一小部分成立**。四类方向里，
**复合条件／嵌套**语言原生支持、**多事实联合**（跨键相等）已用枚举配对解决、
**时序**在适用条件侧几乎没有需求；**真正的语言缺口只剩「计数」**（约 2–3 条）。
其余大头是**引擎未产出派生判定**与**契约上永久留空的通论/体例**——都不是语言问题。

产出：`docs/PREDICATE-EXPRESSIVENESS-AUDIT.md` ＋ 台账 ＋ 测试（入 CI）。

## 1. 为什么不用关键词扫（先做了一次，自己推翻）

先扫了 465 条未映射规则：按「时序」类关键词得 **29 条**命中。
**逐条读过之后**：多数是**历法描述**（「丑之终、寅之始」解释立节）或
**应期/断法**（「破而后立」「出月不破」「动爻主发动、变爻主后势」）——
**不是适用条件**。关键词扫会把需求**夸大**，故改为按形状归类。

> 这与 t202 的教训同源：**先读，再归类**。

## 2. 八类形状

| # | 形状 | 状态 | 需求 |
|---|---|---|---|
| 1 | 复合条件／嵌套 | **原生支持**（v3 组形；t188 起实际用了嵌套 `same`） | 已消化 |
| 2 | **跨键取值相等** | **已解决**：枚举有限域＋分支内配对（t188/189/194/195/197/204） | 已消化 |
| 3 | 全称／排除（「全无直接克」） | **已解决**：`none_of` ＋ 正句保键在场（t200） | 已消化 |
| 4 | 或位穷举（域覆盖） | 写得出，但**恒真风险**（t182 登记册 **64** 条） | 已登记供过滤 |
| 5 | **计数**（独发／独静／两现） | **缺** | **约 2–3 条** |
| 6 | 时序（先…后…） | 适用条件侧**几无需求** | ≈0 |
| 7 | 跨键关系（生克冲合） | 可写但**会爆炸**（≈千级分支/条） | 约 7–9 条 |
| 8 | 派生判定（元神/忌神、变体用、七政格局） | **引擎侧** | 数十条（引擎投入） |

**第 2 类的通用解法**（本仓最主要的表达力成果）：**枚举有限域 ＋ 分支内配对**——
地盘干只取 9 值、爻位只取 6、藏干只取 10 干，把等式逐值配成支，
支内用 `same` 绑定同一位置。**不用通配、不加新原语、不动闸门。**

## 3. 机器钉住的部分

`tools/test-expressiveness-audit.py`（入 CI）钉四件事：

1. 台账结构完整（每类有 id／name／status／evidence／demand）；
2. **计数类候选（`ZENGSHANBUYI-007`／`ZENGSHANBUYI-021`）仍未映射** ——
   一旦有人把计数语义做出来并映射它们，**断言会红**，提醒同步更新审计；
3. 「已消化」三类的证据工具/台账仍在（防审计变成无凭据的散文）；
4. `status` 取值合法（防手写错值）。

## 4. 未决清单（承接 t206）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **计数语义**（独发／独静／用神两现） | **本轮定性：唯一有真实需求的语言缺口**，约 2–3 条；要做需另立设计文档 |
| 2 | `TAIWEIFU-010`「魁钺同行」的所指 | 三种读法待人裁定（t206） |
| 3 | `liuyao.structure` 17 条（可执行层） | 两仓无定义，需人给定义 |
| 4 | `yongshen.zhi` 2 条（可执行层） | 跨键配对，映射表表达不了 |
| 5 | 跨键关系 7–9 条 | **建议**改由引擎产出判定名（而非谓词硬枚举千级分支） |
| 6 | 派生判定数十条（元神/忌神、七政格局、神煞三套） | 引擎投入 |
| 7 | `ZENGSHANBUYI-025` 反吟／伏吟 | ~1.6 万盘遍历未见该结构 |
| 8 | `QM-P30`「三奇」两读／`QM-P26` 无取值子句 | 原文两读／口径待裁 |
| 9 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 10 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/test-expressiveness-audit.py
python3 -c "import json; d=json.load(open('tools/reports/expressiveness-audit.json'))
[print(c['status'].ljust(28), c['name']) for c in d['classes']]"
sed -n '1,40p' docs/PREDICATE-EXPRESSIVENESS-AUDIT.md

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/domain-check.py
python3 tools/verification-depth-report.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

**无规则/谓词数据变化**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `275ac4c7bd84528431d41db930d4bd09cc3b9b22`；产品仓无需重新导出。
六术覆盖率不变；验证深度仍为 **380/381（100%）**。

**给消费方的一条实用说明**（审计里最有用的那半）：

- 本仓的谓词**已经能表达**：复合/嵌套、跨键取值相等、全称排除、或位穷举；
- **不能表达**：计数（有且仅有 N 个）——所以「独发／独静」这类规则不会出现命中；
- **不建议**消费方期待「生克冲合」这类**跨键关系**条件：谓词层若要写就得枚举千级分支，
  本仓选择**不写**，改由引擎产出具名判定（如六爻的月建强度/活动那样）。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。