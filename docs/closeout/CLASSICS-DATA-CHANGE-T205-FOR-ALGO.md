# 消费方数据版本 · t205 可执行层字段接上真实 FactKey（满足 67→72、信息不足 40→34）

日期：2026-09-21。基线提交：`62027d2`（t204 后）。
**数据修订提交（请钉这个）：`0a0e27d3f068d8eee9a0c80285c7406a07a2c304`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标第 3 条要守的是 `fateradar-executable-v2`：三态 · rescue · named_gaps ·
implementation_assumption · `verified=false`。本轮去碰它的痛点——
**`FIELD_MAP` 里有一批字段标着「引擎未产出」，其实好几项是引擎早就算过的**，
只是没产成事实、也没接上 key，于是挂在这些字段上的记录只能报「信息不足」。

补上之后：**满足 67 → 72**、**信息不足 40 → 34**、接不上 FactKey 的字段引用 **30 → 21**。
谓词口径与覆盖率**完全不变**（六术同前）。

## 1. 可执行层三态

| | 前 | 后 |
|---|---:|---:|
| 满足 | 67 | **72** |
| 不满足 | 147 | 148 |
| **信息不足** | **40** | **34** |
| 未提供定义表 | 4 | 4 |

其余不变：`rescue=unimplemented` 30、带 `named_gaps` 31、**`verified=true` 0**，
`validate-executable.py` 仍 OK（15 包 / 258 条 / 579 来源跨度 / 42 具名缺口）。

## 2. 补上的四枚事实（仍是「已有判定搬进事实层」）

| 新键 | 取值 | 来自 | 接了哪个字段 |
|---|---|---|---|
| `liuren_ke` | 四课各课的**上神**（地支） | `selection.courses[].top` | `four.ke` |
| `liuren_shehai` | **`depth`／`mengzhong`** | `selection.shehaiMethod` | `shehai.method` |
| `qizheng_ascendant` | 十二宫名（与 `gongwei` 同值域） | 引擎 `Math.floor(asc/30)%12` | `ascendant.sign` |
| `positions`（代理） | 逐爻在场 | 按逐爻分名接（见下） | `positions` |

三处值得写清的设计选择：

1. **`liuren_ke` 与既有 `sanchuan`（三传）同形** —— 三传是三枚事实、四课就是四枚，
   不另造一套形状。
2. **`liuren_shehai` 沿用引擎原值 `depth`／`mengzhong`，不译成中文。**
   因为 executable 的记录就是按这两个字面值比对的（`{equals: {shehai.method: "depth"}}`）——
   **译成中文会让这两条记录从「信息不足」掉进「不满足」**（更糟）。这是刻意的偏离：
   事实层一般是中文名，此处以「能对齐下游比对值」为准。
3. **`positions` 是总名，按逐爻分名接**：`FIELD_MAP` 旧注自己写着
   「引擎产出的是 `shiyao`/`yingyao`/`dongyao` 分名」——那就照分名接：
   `positions`→`yao_zhi`（逐爻必有，作**在场代理**）、`.activity`→`liuyao_activity`（t193 产出）、
   `.moving`→`dongyao`（无动爻时缺席，故**不**作在场代理）。
   `.moving`／`.activity` 影响的是**输入完备度**（置信度），不是三态判定。

另：`ascendant.sign` 此前在 `FIELD_MAP` 里**根本没有条目**（落进「未知字段」桶），本轮补上。

## 3. 没有做的那一件（并说明理由）

`liuyao.structure`（**17 条**，仍是最大一块）**没有接**：

- 它在**两个仓都没有定义**；
- 其使用者还需要 `liuyao.node.element`／`node.state`；
- `liuyao_seq`（卦体分类：本宫／游魂／归魂）看似相关，但把 `structure` 认作它就是**猜**。

按 t183 的判断**不猜所指**——要接它，得先有人给出定义。

剩余接不上的字段引用 **21**：`liuyao.structure` 17、`yongshen.zhi` 2、
`day.gan.element` 1、`year.gan.doushu` 1。
（其中 `yongshen.zhi`＝「用神所在之爻的支」，本质是**跨键配对**，
不是单一 FactKey 能表达的——executable 层的映射表没有 join 能力，故留空。）

## 4. 未决清单（承接 t204）

| # | 事项 | 状态 |
|---|---|---|
| 1 | `liuyao.structure` 17 条 | **未接**：两仓无定义、需人给定义（`node.element` 亦未产出） |
| 2 | `yongshen.zhi` 2 条 | 需跨键配对，executable 的映射表表达不了 |
| 3 | 余 38 条未被样盘演示 | 37 目录式（结构性自证）＋ 1 条 `TAIWEIFU-010` |
| 4 | 六爻用神×关系、八字化气/有根 7–9 条 | 需五行**关系**判定 |
| 5 | 八字神煞 30 条 | t201 改判：横跨三套神煞体系，不是可做的块 |
| 6 | `ZENGSHANBUYI-025`／`QM-P30`／`QM-P26` | 罕见结构／原文两读／口径待裁 |
| 7 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 8 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付（可执行层三态与接不上的字段）
python3 tools/eval-executable.py --all
python3 tools/validate-executable.py

# 新事实确实进盘
python3 -c "
import json; d=json.load(open('tools/reports/facts-sample.json'))
print('liuren 四课上神:', [f['value'] for f in d['liuren']['caseA']['facts'] if f['key']=='liuren_ke'])
print('涉害取法:', [f['value'] for f in d['liuren']['caseA']['facts'] if f['key']=='liuren_shehai'])
print('七政上升:', [f['value'] for f in d['qizheng']['caseA']['facts'] if f['key']=='qizheng_ascendant'])"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
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

`CLASSICS_REV` = **`0a0e27d3f068d8eee9a0c80285c7406a07a2c304`**。
产品仓 `generated/*.json` 已同步覆盖；`tc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变
（bazi 49.9%／ziwei 67.7%／qimen 90.0%／liuren 35.9%／liuyao 40.6%／qizheng 24.4%）。

**给消费方的两条提醒**：

1. `liuren_shehai` 的取值是**英文枚举** `depth`／`mengzhong`（引擎原值）——
   因为 executable 层就是按这两个字面值比对的。别以为是漏译。
2. 可执行层的「信息不足」已从 40 降到 **34**：这 34 条引用的是**引擎确实不产出**的字段
   （最大一块是 `liuyao.structure`，两仓无定义）。它们**不是**「条件不成立」，
   按本仓口径也不得降级成「不满足」。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。