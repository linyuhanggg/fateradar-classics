# 消费方数据版本 · t169 人工复核台账化（目标项 2）

日期：2026-09-21。基线提交：`4e16db1`（t168 谓词语言 v3 交付后）。
**本轮无规则数据变化** → 消费方 `CLASSICS_REV` **不变，仍为 `51afcdf45eb73d15064052e73b650e638132e402`**。
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标项 1（谓词语言）在 t168 已交付。本轮做目标项 2（81 条人工复核）。
`tools/reports/needs-human-review.md` 与 unmapped 报告同病：**手写过程稿、无生成器、已累积失真**。
本轮把它变成可复算台账，并**实测结案了两个「需人决定」项**，同时查出
**189 条不可锚的根因**——它们**全部**是编者重述，原文里没有可指的句子。

## 1. 覆盖率：本轮不变（口径未改）

`python3 tools/predicate-report.py`

| art | anchored | with_pred | 覆盖 | 通配占比 |
|---|---:|---:|---:|---:|
| bazi | 449 | 151 | 33.6% | 10.6% |
| ziwei | 93 | 63 | 67.7% | 0.0% |
| qimen | 40 | 8 | 20.0% | 12.5% |
| liuren | 53 | 11 | 20.8% | 9.1% |
| liuyao | 69 | 21 | 30.4% | 14.3% |
| qizheng | 76 | 11 | 24.4% | 9.1% |

未映射 581 条、三道谓词门禁全 PASS、`coverage-report.py --fail-under 54` PASS。
与 t168 逐项一致：**本轮不动规则数据**，所以覆盖率与 CLASSICS_REV 都不动。

## 2. 旧件的三处失真（本轮抓出并量化）

| 失真 | 旧件写法 | 实测 |
|---|---|---|
| **id 写法不是 rule_id** | `shenfeng-tongkao` R01–R05、`lantai-miaoxuan` M01/R01–R07、`bushi-zhengzong` R01–R06 | 那些是 **statement 前缀**；按字面检索 **19 个 id 全部不存在**。真实 id 形如 `SF`/`SHENFENGTONG-SF`/`SHENFENGTONG-003`、`LT`/`LANTAIMIAOXU-LT`/`-003…008`、`BUSHIZHENGZO-BSZZ`/`-003…007` |
| **混用裸 id 与带前缀 id** | 「`GR-01` / `GR-03` 已改 procedure」 | 对裸 id 成立；但同书另有 `GUOTIANJING-GR-01`/`-GR-03` 是**两条不同规则**，前者 `procedure`、后者 `doctrine`。不写明前缀会让复核者改错条 |
| **规模数字失真** | 全文以「81 条」流传 | 81 是**行数**；实测 `anchor: null` 共 **189 条** |
| **前提已变** | 「`qimen-faqiao` QM-P26、QM-P36：仓库无 fulltext」 | 两条**已有** anchor，指向仓内自制选段 `sources/excerpts/qimen-faqiao-chaibu-v1.md`（非抓取现代整理本，旧件的著作权顾虑本身仍成立） |

## 3. 两个「需人决定」项：用测量结案

### 3.1 `book.script` 要不要按 fulltext 实际用字改正？→ 不需要，无一处不符

旧件：「需人决定：是否按 fulltext 实际用字改正 `book.script`，或接受 V11 残留。」

实测（`opencc` t2s/s2t 双向比对，判据：登记 `traditional` 却简体专用形更多即不符）：

> **55 本书，0 处不符。**

所以这个选项是**空的**：没有登记错的书可改。V11 的真实成因是**引文形态**——
未锚条目用现代概述，概述多为另一种字形，于是与 `book.script` 的字形统计不同向。
V11 现为 **111**（G1 要 < 50，**仍未达**），V14 为 **174**，warning 合计 285。

### 3.2 G10（紫微两盘 top-6 不同）→ 阻塞已消失

旧件：「G10 未达标……需要人决定：是否允许给 legacy 辅星补宫位，或把检索从『命中条数』改成『星带宫优先』。」

实测：产品仓 `tests/rules/predicate-matching.test.ts` 的「两盘 ruleId 集合不同」
对**六个 art（含 ziwei）全部通过**。即该阻塞已不存在，**不需要**改 `ziwei.ts`、
也**不需要**为凑差异补宫位（那正是「不许为两盘差异臆造宫位」要防的）。

## 4. 根本发现：189 条不可锚 **全部**是编者重述

实测 `anchor: null` 的 189 条，`quote_kind` 分布：

```
restatement  189
```

**一条不例外。** 也就是说这 189 条的 `quote` 本身就是现代概述，**原文里没有可指的句子**。
「不要硬锚」在这里不是政策限制，而是**逻辑后果**：没有可锚的对象。

这条同时**归并**了旧件分列的六类（无全文 / pack 元规则 / 原文多次出现 / 现代概括 / P7 名单 / V11）：
它们读起来像六种不同待办，实际只有**一个**决定——是否把这些重述换成真引文（**会改动 `quote`**）。

### 4.1 随之查出并修掉 `anchor_recover.py` 的一个真缺陷

t167 入库 31,525 源段后，`anchor_recover.py` 重跑的表观结果是「**可锚 25 条**」（method 全为 `exact`）。
按字面执行会**撞出 31 个 `validate-rules` 错误**：

- **V15 25 条**：条目自报 `quote_kind: restatement`（编者重述，不是引文），
  其 `quote` 往往是**来源标签**——例如「入地眼全書龍法卷二」、
  「看正偏印法/看正偏财法-卷一-命理约言-陳素庵(清)」。这类字符串碰巧与 fulltext 某行标题相同，
  就被当成「可锚」锚上了。**这正是「不要硬锚」要防的事。**
- **V13 6 条**：`quote` 是卷首署名／标题行（如「皇極經世書卷五上    宋 邵雍 撰」），本就不能当断辞。

修法：给 `anchor_recover.py` 补两道**前置闸门**——跳过 `quote_kind: restatement`；
用 `validate-rules.py` 的 `v13_bad_quote`（单一实现，不另写一份判据）挡掉劣质 quote。

加闸门后重跑：

```
already=1167 recovered=0 unanchorable=189 no_ft=0
```

**可锚数归零**。这是**正确结果**，不是失败：`anchor: null` 不是「还没找到」，是**没有可找的对象**。
`git status -- references/books/` 为空——修好之后工具不再改动任何规则。

> 方法学注记：这里的顺序很重要——先用**门禁**判死，再改**工具**，不改门禁。
> 若当时选择「改 quote_kind 或放宽 V15/V13 让这批过闸」，就会把来源标签变成合法引文。

## 5. 台账（本轮的交付物）

`tools/needs-human-review-report.py` → 重写 `tools/reports/needs-human-review.md`，13 条论断四态：

| 状态 | 条数 | 论断 |
|---|---:|---|
| **已解决** | 3 | `v11-g1-target`（book.script 无需更正）、`ziwei-palace-scope`（G10 阻塞消失）、`restatement-census`（189 条全 restatement） |
| **仍未决** | 8 | `faqiao-no-fulltext`、`pack-meta-rules`、`modern-summary`、`p7-lz-metadata-quote`、`v14-low-correspondence`、`qizheng-factgap`、`catalog-titles`、`procedure-kind` |
| **论断已过时** | 0 | （失真的 id 已在台账里换成真实 id，故按当前 id 复核不再报过时；失真本身记在 `doc_notation` 与 §2） |
| **机器不可判** | 2 | `multi-occurrence`（旧件只给术语、未给 id，且「哪一处算唯一落点」是人的判断）、`p6-grey-zone`（政策声明，无逐条对象） |

台账的机械检查（不是自报数字）：

- `pack-meta-rules`：**19 个旧件字面 id 检索不到**，由工具量化；
- `v14-low-correspondence`：对应度实测 `FEIXINGZIWEI-008` 0.140、`ZIWEIDOUSHUQ-ZW-05` 0.106，与旧件一致；
- `catalog-titles`：7 条确实都在 `CATALOG_TITLE_RULE_IDS` 内（已从覆盖率分母剔除）；
- `procedure-kind`：`GR-01`/`GR-03` 确实都是 `procedure`；
- `restatement-census`：断言未锚 189 条 `quote_kind` 只有 `restatement` 一种；
- `qizheng-factgap`：三条仍写不出谓词；**数字已漂移**——旧件「约 35 条七政未映射」，实测 **65 条**。

**本脚本不写任何锚点、不改任何规则**——「不要硬锚」是硬约束，工具只做核对与登记。

## 6. 仍需人决定（机器不能代劳）

1. **是否统一换成真引文**：这是 189 条重述的**唯一**决定，且会改动 `quote`（当前不变量禁止本轮动）。
   不换 = 接受 `quote_kind: restatement` 与 V11 残留；换 = 需逐条找原文并重写 `quote`。
2. **V11 残留怎么处置**：`book.script` 已实测无需更正，所以只剩「逐条补锚（改 `quote`）」或「接受残留」两条路。
3. **pack 元规则（21 条）是否单列一类**：它们「原文无对应句」是**永久事实**、不是待办，
   继续留在「待人工判断」会稀释这一页的信号。
4. **`multi-occurrence` 要先补 rule_id 清单**：旧件只给术语，机器无从逐条核对。
5. **P6 灰区（对应度 0.15–0.30）**：政策要求机器不动该档；本轮未动该档任何条目。

## 7. 可复跑

```bash
cd /Users/sync/code/fateradar-classics

python3 tools/needs-human-review-report.py            # 四态总览
python3 tools/needs-human-review-report.py --json      # 台账（含未锚全表、warning 读数、census）
python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md

python3 tools/anchor_recover.py --dry-run              # 必须是 recovered=0
python3 tools/test-needs-human-review-report.py        # 22 项，已入 CI

# 闸门（本轮全绿）
python3 tools/validate-rules.py                        # OK 55 file(s), 285 warning(s)
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
```

## 8. 给 cosmic 的版本钉

**本轮未改任何规则数据**（`anchor_recover.py` 加闸门后 recovered=0，`git status -- references/books/` 为空），
因此 `CLASSICS_REV` **不变**，仍为 `51afcdf45eb73d15064052e73b650e638132e402`。
产品仓无需重新导出。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0；电子文本匹配、模型审查与测试都不能代替人工影印核验。