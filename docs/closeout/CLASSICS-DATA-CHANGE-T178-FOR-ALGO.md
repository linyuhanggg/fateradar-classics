# 消费方数据版本 · t178 六爻爻支入事实层（六合／六冲／三刑落地）

日期：2026-09-21。基线提交：`9e2d1df`（t177 后）。
**数据修订提交（请钉这个）：`da11267541a0fc500b96382e1d7b0bed004457d0`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

六爻的**基座事实**此前是空的：引擎会算纳甲地支，也从没把它当事实产出。
本轮补上 `yao_zhi`（本爻纳甲地支）与 `bian_yao_zhi`（变爻纳甲地支），
「子丑六合／子午六冲／寅巳申三刑」这类条件才第一次写得出来 —— 落地 **3 条**。

liuyao 谓词覆盖 **30.4% → 31.9%**（21→22）。**只 +1 的原因见 §4**：
三条里两条是 `anchor: null`，本来就不在「有锚且谓词为空」的分母内。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 27 | 67.5% | 14.8% | 6 |
| liuren | 11 (20.8%) | 11 (20.8%) | 12 | 22.6% | 8.3% | 5 |
| **liuyao** | 21 (30.4%) | 21 (30.4%) | **22** | **31.9%** | 13.6% | 5 → **6** |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **489**。4 大门禁全绿；**27** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS
（含 `--max-wildcard 15`）；`coverage-report --fail-under 54` PASS。
liuyao 本轮新映射**无一命中零区分度 hard 档**（hard 仍只有既有 3 条）。

## 2. 两个新事实

| key | 含义 | 取值域 | 来源（都已在排盘结果里） |
|---|---|---|---|
| `yao_zhi` | 本爻**纳甲地支**，`scope.yao ∈ 1–6` | 12 支 | `row.ganzhi[1]` |
| `bian_yao_zhi` | **变爻**纳甲地支，`scope.yao ∈ 1–6` | 12 支 | `row.changed?.[1]`（仅动爻有） |

- 都是**透传**，不新算排盘。
- 变爻支另立一键（而不是塞进 `yao_zhi`）：executable 层分别点名
  `liuyao.node.branch` 与 `liuyao.changed.branch`，两件事本来就不同。
- V16 的 `scope.yao` 允许键补入这两键；`ART_EMIT_KEYS[liuyao]` 同步补入。

实测样本：caseA 爻支 初→上 = `子寅辰午申戌`（无动爻、无变爻支）；
caseB = `子寅辰丑亥酉`，六爻皆动，变爻支 `丑亥酉丑亥酉`。

## 3. 三条落地与端到端验收

写法与 t175 同构：`{any_of: [{all_of: [{key: yao_zhi, value: X}, …]}, …]}`。
**仍然不加 `same`** —— 六合／六冲要的正是两支落在**不同爻**上
（同支两见是自刑，另一回事；`same` 会把它们绑到同一爻，反而错）。

| rule | 原文 | 组 |
|---|---|---|
| `ZR-07` | 子丑、寅亥、卯戌、辰酉、巳申、午未六合 | 6 对（`yao_zhi`） |
| `ZENGSHANBUYI-ZR-07` | 子午、丑未、寅申、卯酉、辰戌、巳亥六冲 | 6 对（`yao_zhi`） |
| `ZENGSHANBUYI-024` | 寅巳申、丑戌未、子卯三刑 | 3 组（`yao_zhi`） |

### 两个样本盘恰是标准的六冲卦／六合卦，互为对照

| 盘 | 爻支（初→上） | 六冲 | 六合 | 三刑 |
|---|---|---|---|---|
| caseA | 子 寅 辰 午 申 戌 | **满足** | 不满足 | 不满足 |
| caseB | 子 寅 辰 丑 亥 酉 | 不满足 | **满足** | 不满足 |

命中事实显示各对落在**不同爻位**，例如 caseA：
`子@1 午@4`、`寅@2 申@5`、`辰@3 戌@6` —— 三对冲全中，正是六冲卦的构成。

### 3.1 如实登记的一条边界

本式**不强制**「两支在不同爻」：v3 没有「两个子句须由不同事实满足」的语义
（t175 记的同值异位边界）。合成盘上「同一爻同时给子与午」仍会判成立。
**真实盘面一爻一支，故实际不受影响**：`yao_zhi` 每爻恰一条。
测试用合成盘把这条边界**显式记录下来**（不隐藏），待将来语言支持「异事实」再收紧。

## 4. 为什么只 +1：两条是 `anchor: null`

| rule | anchor | 是否进「有锚且谓词为空」的分母 |
|---|---|---|
| `ZENGSHANBUYI-024` | 有 | ✅ 进（故 liuyao +1） |
| `ZR-07` | **null** | ❌ 不进 |
| `ZENGSHANBUYI-ZR-07` | **null** | ❌ 不进 |

两条映射本身有效（规则有了谓词、产品检索可用），只是不在那个口径里。
**这不是算错**：`test-map-branch-groups.py` 已钉住「台账 12 条里 `anchor: null` 的恰好这 3 条」
（`SANMINGTONGH-018`、`ZR-07`、`ZENGSHANBUYI-ZR-07`）。

## 5. 查过但**不**映射的

- **`ZENGSHANBUYI-020` 化进神／化退神**：「化进神（**如**寅化卯）力增、化退神（**如**卯化寅）力减」
  —— 「如」标明这是**举例**，照它只写「寅→卯／卯→寅」会把通则窄化成一对
  （与 t168 撤回 `ZIWEIDOUSHUQ-ZW-04` 同一理由）。**不映射**。
  （该条若要忠实表达，需「同一爻的支与变爻支构成进／退神关系」——属关系判定，未产出。）
- **自刑**（同支两见）：见 §3.1 的语言边界。

## 6. 未决清单（承接 t169–t177，按可动性排序）

| # | 事项 | 卡在哪 | 谁能动 |
|---|---|---|---|
| 1 | **`QM-P26` 直使加地丁** | 形态与 t177 已映射三条同构，但再加一条 → 5/28 = **17.9%** > 15%（测试已钉算术） | **需授权** |
| 2 | **六爻其余**（用神旺衰／月建日辰／变爻关系） | 需新事实与关系判定；`bian_yao_zhi` 已就位，缺的是「同爻两支的关系」语义 | 引擎＋语言 |
| 3 | **神煞 30 条** | 需在 `shensha.ts` 新增约 20 个取法 | 引擎（工作量大、出错面大） |
| 4 | **梅花 21 条** | 本仓无梅花事实层；两处词表仍漂移 | 引擎＋词表 |
| 5 | **跨键取值相等**（如「庚临岁干」`QM-P27`） | `same` 只绑 scope 字段、不绑取值 | 语言或事实设计 |
| 6 | **同值异位／异事实**（自刑、六冲异爻） | 同上，t175 记；客户仍少 | 语言（先定语义） |
| 7 | 3 条无据 statement（t177 §4） | 本版无正文可锚 | **人判** |
| 8 | ziwei 11 条命名格局 | 需格局定义表（多为三方四正，关系未产出） | 定义＋事实 |
| 9 | `liuyao.structure`（executable 17 条） | 是**打包名**，无单一 FactKey 对应 | 古籍侧拆声明 |
| 10 | t169 遗留：189 条重述、V11 111 vs G1 <50、25 条既有结构恒真映射 | 各有专项记录 | 人判／混合 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮：爻支成组（含六冲卦／六合卦互斥断言与边界记录）
python3 tools/map-branch-groups.py --dry-run      # 幂等：已落实的会跳过
python3 tools/test-map-branch-groups.py           # 12 条台账 + 语义 + anchor 账

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 三态求值
python3 tools/eval-predicates.py --art liuyao --case caseA -v | grep -A2 "ZENGSHANBUYI-ZR-07"
python3 tools/eval-predicates.py --art liuyao --case caseB -v | grep -A2 "ZR-07"

# 导出与产品仓同步
python3 tools/export-rules.py
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`da11267541a0fc500b96382e1d7b0bed004457d0`**。
产品仓 `generated/liuyao.json` 已同步覆盖（22 条带谓词；`ZR-07`／`ZENGSHANBUYI-ZR-07`
因 `anchor: null` 不导出，属既有导出规则「无可用锚点即跳过」）。
两处 `fact-vocab.json` 共有键值域逐项一致（**41** 键）；`tsc --noEmit` exit 0；
相关测试文件全绿。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。