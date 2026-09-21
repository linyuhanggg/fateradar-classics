# 消费方数据版本 · t212 谓词取值溯源分类：契约第一条第一次有了可读数字

日期：2026-09-21。基线提交：`c7037c3`（t211 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

贯穿契约第一条是「不编造、**可溯源**、原文没写就不写」。
既有的检查管的是「谓词**能不能跑通**」（art-keys／open-values／死引用／取值域／验证深度），
**没有一项在管「谓词里的取值是怎么来的」**。本轮补上这个度量。

## 1. 四类分类

对每个取值叶子问一句：**这个值在本条规则的 statement／quote 里吗？**

| 类 | 条数 | 占比 | 含义 |
|---|---:|---:|---|
| `literal` | **797** | 58.8% | 取值字面出现在本条 statement／quote 里（繁简折叠后） |
| `enumerated` | **477** | 35.2% | 本条在**同一键**上展开 ≥3 个取值——**值域枚举**，不是原文用词 |
| `canonical` | **44** | 3.2% | **既非字面、也非枚举、也非引擎态**——这一类**要人读**（共 **23 组**） |
| `engine-state` | **37** | 2.7% | 取值由引擎判定产出（键在工具里**显式列举**） |

合计 **1355** 个取值叶子（391 条带谓词的规则）。

`enumerated` 涉及的键：`gan` 76、`liuqin` 71、`dipan_gan` 48、`zhi` 38、`liuyao_tomb` 30、
`rizhu_strength` 27、`yueling` 22、`canggan` 20、`shishen` 19、`bamen` 14… ——
也就是说，**35% 的取值是我这套「枚举有限域」写法的产物**，而不是原文用词；
这正好把「谓词语言表达力」那条主线的**代价**量化出来了。

## 2. `canonical` 一类**不替人下结论**（我改过一次措辞）

它同时装着两种东西，报告里写明、并把 23 组**直接列出来给人看**：

- **真·名目对译**：原文俗称／异名 → 规范名
  （「财」→ 六亲规范名**妻财**、「七煞」→**七杀**、「官祿宮」→ 引擎宫名**事业**）；
- **本条只是没提这个值**：section 标题、就绪条件式 statement
  （如 `DALIURENDAQU-018`「三传及日干五行均由已验证事实层给出」）——
  值本身是规范名，但原文那句话里确实没写它。

我最初把这一类命名为「名目对译」，**读了样例才发现名不副实**（里面混着大量「本条没提」），
遂改成「既非字面／枚举／引擎态」并在输出里写明两类混合。
**报告不夸大自己的能力**——这也是为什么这一类的数量小（44）却仍需人读。

## 3. 产出

| 文件 | 内容 |
|---|---|
| `tools/value-provenance-report.py` | 分类工具；`--write` 落台账 |
| `tools/reports/value-provenance.json` | 四类计数 ＋ 枚举涉及的键 ＋ **23 组待读清单** |
| `tools/test-value-provenance.py` | 入 CI：分类完备、可复现、清单与计数对得上、**反例** |

测试钉的四件事：① 四类之和 **==** 取值叶子数（不许有值落不进任何一类）；
② 连跑两次一致；③ `canonical_pairs` 的计数之和 == `tally['canonical']`；
④ **反例**——繁简折叠要能命中「財」、枚举阈值是显式常量（3）、引擎态键是**显式列举**
而非运行时猜。**不钉具体数字**（它随施工变化；t187/t199 的同一教训），钉的是性质。

## 4. 未决清单（承接 t211）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **23 组「需人读」的取值** | **新增**：真·对译与「本条没提」混在一起，需人抽检（含 财→妻财、七煞→七杀、官祿→事业） |
| 2 | 梅花 1 条（`MHY-E-01`） | 本仓无梅花样盘，补样盘即可判 |
| 3 | 小六壬余 3 条 | 需产出输入类事实（时辰支、农历月日）与计数（吉类计数） |
| 4 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义（现居「接不上」之首） |
| 5 | `day.gan.element` 1 ／ `year.gan.doushu` 1 | 引擎未产出该键 |
| 6 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 7 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/value-provenance-report.py            # 四类计数 + 23 组待读
python3 tools/value-provenance-report.py --write    # 落台账
python3 tools/test-value-provenance.py              # 完备性 + 可复现 + 反例

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
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。
产品仓 `generated/*.json` 已同步覆盖（导出无变化）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变。

**给消费方的一条实用读数**：若你要审计「规则里的取值是不是原文说的」，现在有据可依——
`tools/reports/value-provenance.json` 给出**每一类的计数与待读清单**；
其中 **58.8% 是字面**、**35.2% 是枚举编码的产物**（不是原文用词，但也不是编造：
它们是有限值域的展开，写法与判据都在 `docs/PREDICATE-EXPRESSIVENESS-AUDIT.md` 里写明）。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。