# 消费方数据版本 · t177 关闭 30 条机械残留 · 更正 t173 提法 · 值符三条落地

日期：2026-09-21。基线提交：`4049c83`（t176 后）。
**数据修订提交（请钉这个）：`2c04b536063e2480db5a548d869430dcde618286`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

本轮三件事，含一次**自己纠正自己**与一次**被自己过时算术挡住的机会**：

1. 把 `classify()` 机械判为「本可表达」的 **30 条**逐条复核，**27 条维持不映射**（落台账＋测试）；
2. **更正 t173 我写错的一条提法**：那 3 条无据 statement **在本版无处可改锚**；
3. **值符三条落地**（`QM-P01/P02/P31`）——t173 曾按 15% 通配闸门记为
   「gate-blocked」，本轮复核发现 **t175/t176 加谓词后分母变大，4/27 = 14.8% ≤ 15%，闸门已不再挡**。
   qimen **60.0% → 67.5%**（24→27），未映射 **493 → 490**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 |
|---|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% |
| **qimen** | 7 (17.5%) | 24 (60.0%) | **27** | **67.5%** | 4.2% → **14.8%** |
| liuren | 11 (20.8%) | 11 (20.8%) | 12 | 22.6% | 8.3% |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 | 30.4% | 14.3% |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% |

未映射 **490**。4 大门禁全绿；**27** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS
（含 `--max-wildcard 15`，实测 4/27 = 14.8%）；`coverage-report --fail-under 54` PASS；
qimen 本轮新映射**无一命中零区分度 hard 档**（hard 仍只有既有 `QM-P17`）。

## 2. 值符三条：为什么现在可以映射，以及 `*` 在这里的语义

原文条件问的是**值符所在之宫**，不是值符星名：

| rule | 原文 | 谓词 |
|---|---|---|
| `QM-P01` 龙回首 | 甲值符加地盘丙奇 | `{all_of: [{key: zhifu, value: "*"}, {key: dipan_gan, value: 丙}], same: gong}` |
| `QM-P02` 鸟跌穴 | 丙奇加地盘甲值符 | `{all_of: [{key: tianpan_gan, value: 丙}, {key: zhifu, value: "*"}], same: gong}` |
| `QM-P31` 伏宫 | 庚临值符 | `{all_of: [{key: tianpan_gan, value: 庚}, {key: zhifu, value: "*"}], same: gong}` |

- `zhifu` 事实自 t173 起带 `scope.gong`（值符星落宫），所以 `same: gong` 能把
  「值符宫」与「该宫的天／地盘干」绑到**同一宫**。
- 这里 `value: "*"` 的语义是**存在性**（该键须有事实、取值不限）：值符星名随盘而变，
  静态写不出具体值。**不是凑数**——写在 `map-qimen-stems.py` 的注释里。
- `甲` 不出现在天地盘（甲寄六仪），所以「甲值符」只能靠 `zhifu` 这个键指认，这正是本式。

### 2.1 语义验收（样本盘上三条都不成立，故另造盘）

样本 caseA/caseB 上三条**均不满足**（故不会被零区分度工具误判）。另造「值符在 2 宫、
该宫地盘干为丙、天盘干为庚」的盘：

| 断言 | 结果 |
|---|---|
| 值符宫地盘干为丙 → 龙回首 | **满足**（命中 `zhifu@2` + `dipan_gan 丙@2`） |
| 值符宫天盘干为庚 → 伏宫 | **满足** |
| 鸟跌穴要**天盘丙在值符宫**（本例丙在 3 宫） | **不满足**（`same: gong` 生效） |
| 值符宫地盘干为戊（非丙） | **不满足** |

## 3. 30 条「机械判为可表达」的残留：27 条维持不映射

`predicate-gap-report.py` 的 `classify()` 判据是「statement 里能否复原出该 art 的 FactKey 取值」。
它把 30 条标成 `single-pair`／`multi-pair-same-key`／`multi-key`（＝「现有语言本可表达」）。

复核结论：**3 条（值符类）确实可映射、已落地；其余 27 条维持不映射**，理由归 15 类：

| 理由类别 | 条数 | 含义 |
|---|---:|---|
| `zero-discrimination` | 5 | 该取值在**每一盘**都成立（如六爻每盘都有全部六亲）→ 恒真零筛选 |
| `equation-table` | 3 | 取象表／类象映射，不是盘面条件 |
| `derivation-method` | 3 | 取法（**怎么取**），不是「**何时适用**」 |
| `ungrounded` | 3 | statement 断言的概念在本版锚定原文里不存在（§4） |
| `needs-gender` | 2 | 需性别事实（本仓无 gender key） |
| `needs-geju` | 2 | 需格局名事实（未产出） |
| 其余 9 类各 1 | 9 | 需大运干支／跨键取值相等／计数／关系／仅可部分表达／原文自陈不作硬输入／元规则／收窄（t168 已撤同款）／收窄… |

台账 `tools/reports/expressible-residue.json`，由 `test-expressible-residue.py` 钉住：
台账条目必须**仍未被映射**（被映射即须从台账移除，不是改台账迁就）且**仍是机械命中**。
**本轮正是这套机制在起作用**：三条值符被映射后，测试要求把它们移出台账。

### 3.1 这条负结论本身有信息量

**该机械判据在散文式古籍上精度很低**：术名本身（「六爻」同时是爻位取值）、
同义值域（`dongyao`/`shiyao`/`yingyao` 共享爻位、`bamen`/`zhishi` 共享八门）都会假命中。
这解释了此前看似矛盾的现象：t168 测得「真需要 AND 的只有 7 条」而未映射有 599 条 ——
因为**机械可复原 ≠ 原文真写了盘面条件**。

## 4. 更正 t173：那 3 条**在本版无处可改锚**

t173 对 `ZR-09`／`ZR-13`／`ZENGSHANBUYI-ZR-13` 写的处置是
「改锚到真正讲归魂／游魂的原文，或把 statement 标为编者综述」。**前半句是错的**：

- 全文确有「**歸魂遊魂章第又二十六**」**章题两处**（L188 目录、L361 正文标题）；
- 但 **L361 之后紧接着就是下一章「月破章第二十七」——该章没有正文**；
- 断语用词全文出现次数：**漂泊 0、飄泊 0、回歸 0、回归 0、還原 0、还原 0**；
- 全文「歸魂」7 行（L65/L67/L188/L361/L573/L7722…）**都是结构定义与取法**
  （如「歸魂卦爲各宮之第八卦，如乾宮中之火天大有」、「歸魂卦世在三爻」），
  不是「主回归／主漂泊」这类**断语**。

**结论**：这三条的判定内容在本版没有可锚正文 —— 既不能改锚（无处可锚），
也不该照 statement 写谓词。正确处置是把 statement 标为**编者综述**或**换版本重做**，属人判。
机器不擅自改 `statement`／`quote`／`anchor`。已写入 `ungrounded-claims.json` 的 `t177_correction`。

> 记这一笔是因为**我上一轮给了一个做不到的选项**。发现方式是把「改锚」当成待验证的断言去查：
> 查章题 → 章题在但正文空 → 再查断语用词 → 0 次命中。

## 5. 明确**不做**的决定：同值异位语言扩展

t175 记过一个 v3 边界：**「同一取值出现在两个不同位置」写不出来**
（`all_of` 两句相同的 `{zhi: 辰}` 会被**同一个事实**同时满足 → 假阳），当时以「自刑」举例。

本轮按 重复／叠／重见／俱全／双／全见 等线索在全部未映射规则里搜，
真正需要该语义的**只有 1 条**（`YUZHAOSHENYI-026` 自刑+下尅上；其余命中项是格局名、
神煞取法、宫名「双鱼」等假命中）。**为 1 条客户改语言属过度设计**，故**不实现**，只登记边界。

## 6. 顺带修掉一个与 t168 同类的缺陷

给 `test-map-qimen-stems.py` 加通配计数时，我第一版写成「只看平铺列表」，于是
**v3 组里的通配数不到**（数成 1，实际 4）——正是 t168 修过的「组形隐形」那一类。
已改为走共享的 `predicate_lang.iter_usable_predicates`。

## 7. 未决清单（承接 t169–t176，按可动性排序）

| # | 事项 | 卡在哪 | 谁能动 |
|---|---|---|---|
| 1 | **六爻爻支事实** | 需引擎新事实；一加即可复用 t175 成组写法映射 `ZR-07` 六合／`ZENGSHANBUYI-ZR-07` 六冲 | 引擎 |
| 2 | **`QM-P26` 直使加地丁** | 形态与已映射三条同构，但再加一条 → 5/28 = **17.9%** > 15%，**闸门会红**（测试已钉住这条算术） | **需授权** |
| 3 | **神煞 30 条** | 需在 `shensha.ts` 新增约 20 个取法 | 引擎（工作量大、出错面大） |
| 4 | **梅花 21 条** | 本仓无梅花事实层；两处词表仍漂移 | 引擎＋词表 |
| 5 | **跨键取值相等**（如「庚临岁干」`QM-P27`） | `same` 只绑 scope 字段、不绑取值 | 语言或事实设计 |
| 6 | 3 条无据 statement（§4） | 本版无正文可锚 | **人判** |
| 7 | ziwei 11 条命名格局 | 需格局定义表（多为三方四正，关系未产出） | 定义＋事实 |
| 8 | `liuyao.structure`（executable 17 条） | 是**打包名**，无单一 FactKey 对应 | 古籍侧拆声明 |
| 9 | t169 遗留 | 189 条重述是否换真引文、V11 111 vs G1 <50 | 人判 |
| 10 | 25 条既有结构恒真映射、`fold_han` 异体字、`daxian`/`liunian_taisui` | 各有专项记录 | 混合 |

## 8. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 值符三条（形态 + same: gong 绑定 + 语义）
python3 tools/map-qimen-stems.py --dry-run
python3 tools/map-qimen-stems.py                 # 幂等
python3 tools/test-map-qimen-stems.py            # 含闸门算术断言

# 残留台账
python3 tools/test-expressible-residue.py

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 三态求值
python3 tools/eval-predicates.py --art qimen --case caseA -v | grep -A2 "QM-P01"
python3 tools/eval-predicates.py --art qimen --discrimination
python3 tools/export-rules.py
```

## 9. 给 cosmic 的版本钉

`CLASSICS_REV` = **`2c04b536063e2480db5a548d869430dcde618286`**。
产品仓 `generated/qimen.json` 已同步覆盖（27 条带谓词），`QM-P01` 导出形为
`{"all_of":[{"key":"zhifu","value":"*"},{"key":"dipan_gan","value":"丙"}],"same":"gong"}`；
`tsc --noEmit` exit 0；相关 6 个测试文件 **78 项全绿**。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。