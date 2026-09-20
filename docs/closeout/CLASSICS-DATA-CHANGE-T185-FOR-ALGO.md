# 消费方数据版本 · t185 推翻 t177 的结论：游魂／归魂的正文**存在**（是我搜错了字）

日期：2026-09-21。基线提交：`6bd5991`（t184 后）。
**本轮规则与词表零改动 → 消费方 `CLASSICS_REV` 不变，仍为
`d5b84e2ffe7b1e4da0e18c8a2e45e5923394dbf3`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t177 对 `ZR-09`／`ZR-13`／`ZENGSHANBUYI-ZR-13` 三条写的处置是
「**本版没有可锚的正文**：该章只有标题」。**本轮证明那是错的。**

t177 用**简体**「游魂」去检索**繁体**正文，得 0 行，于是把「查无」当成了结论。
实际「遊魂」有 6 行、「歸魂」有 7 行；正文也不在章题下面，而排在**全书后段 L7720–L7730**。

**结论变了，但三条仍然不映射** —— 理由从「没有正文」变成
「**有正文，而且正文与 statement 不符，并附带一条原文自己的告诫**」。

这是同一类「**检索盲区伪造出查无**」的**第三次**（t182 域完备键、t183 紫微格局名、t177 本条），
本轮把它工具化了。

## 1. 找到了什么

t177 说「章题 L361 之后直接是下一章，所以该章无正文」——**章题确实空着**，
但该章正文排在全书后段：

| 行 | 原文 |
|---|---|
| L7720 | 遊魂卦爲各宮之第七卦，如乾宮中之火地晉，坤宮中之水天需。 |
| L7722 | 歸魂卦爲各宮之第八卦，如乾宮中之火天大有，坤宮中之水地比。 |
| **L7724** | 古以**遊魂行千里**，我行此事而欲久者，遊魂而不能久，**心無定向，遷改不常**。占身命無安家樂業之所，**占行人遊徧他鄕**。**占出行，行無定止**。占家宅，遷變不常，占墳塋，亡靈不能安妥。 |
| **L7726** | 野鶴曰：**須以用神爲主**，然後以此參之，**若捨用神執此而斷者，謬也**。 |
| **L7728** | 古以**歸魂不出疆**，諸事**拘泥不行**，與遊魂卦相反而斷之，可也。 |
| L7730 | 野鶴曰：亦須以用神爲主。 |

另有平行出处：**卜筮正宗 L407「归魂不出疆，」**（也在本仓语料里）。

## 2. 三条各自怎么办（措辞不符，不是「查无」）

| rule | t177 的说法 | **本轮核实** |
|---|---|---|
| `ZR-09` | 无正文 | **半截有据**：游魂「心無定向，遷改不常」「占出行，行無定止」✓ 对应「主漂泊、不定」；「占行人遊徧他鄕」✓ 对应「问行人宜参看」。**但归魂半截写「主回归、还原」，原文是「不出疆，諸事拘泥不行」——措辞不符。** |
| `ZR-13` | 无正文 | **相左**：「游魂卦不宜远行」vs 原文「古以遊魂**行千里**」「占出行，**行無定止**」。要把「行無定止」读成「不宜远行」，那是解释而非原文。 |
| `ZENGSHANBUYI-ZR-13` | 无正文 | **不符**：「临归魂——速归」vs「歸魂**不出疆**，諸事**拘泥不行**」——「拘泥不行」更像「事阻滞」而非「速归」。 |

### 2.1 最关键的一条：原文自己禁止这么断

三条**都漏了**原文的告诫：

> **L7726**：野鶴曰：須以**用神爲主**，然後以此參之，**若捨用神執此而斷者，謬也**。
> **L7730**：野鶴曰：亦須以用神爲主。

即原文**明确禁止**单凭游魂／归魂下断 —— 而这正是 `{liuyao_seq: 游魂}` 这类单条件谓词
会表达的意思。**故不能照 statement 直接映射**（这正是任务书「不编造」的反面情形：
原文写了，但写的是「不能这么断」）。

**处置**：仍保持 `applicable_to: []`，但理由已更新为
「有正文、正文与 statement 不符、且附『须以用神为主』的告诫」。
正确出路是**人判**：改写 statement 以贴合 L7720–L7730，或让谓词必须同时体现「用神为主」
（后者需要「用神」事实，本仓未产出）。机器不擅自改 `statement`。

## 3. 工具化：把「查无」降级为待验证的断言

新增 `tools/han_search.py` —— **唯一检索入口**：

- 同时按**原字面**与**折半后**（`fold_han`／opencc t2s）检索；
- **两种口径的命中数都报出来**；两口径不一致 → `diverges=True`，
  并提示「**不得直接下查无结论**」。

```
$ python3 tools/han_search.py 游魂 归魂 月朗天门 贪火相逢
「游魂」: 原字面 64 行；折半 91 行
「归魂」: 原字面 28 行；折半 44 行
「月朗天门」: 原字面 0 行；折半 3 行  ⚠ 两口径不一致——不得直接下「查无」结论
「贪火相逢」: 原字面 0 行；折半 1 行  ⚠ 两口径不一致——不得直接下「查无」结论
```

（顺带修掉一个自己刚犯的性能问题：逐行调 opencc 让一次检索要 18 秒——
整档折一次并缓存后 5 秒。这正是 t183 记过的同一处置。）

`tools/test-han-search.py`（已入 CI）钉住：
diverges 判定、t177 错案**可复现地被纠正**（折半后能在曾删卜易搜到、含 L7720–L7730 段内行）、
以及台账更正里的 7 处引文**逐字落在所引行**。

## 4. 台账更正

`tools/reports/ungrounded-claims.json` 新增 `t185_correction`：7 处逐字引文、
三条各自的措辞比对、`decisive_caveat`（用神告诫）、以及处置说明。
原 `t177_correction` 保留不删（留下纠错链）。

## 5. 未决清单（承接 t179／t182／t184）

| # | 事项 | 变化 |
|---|---|---|
| ★ | **3 条无据 statement** | t177 列的是「本版无正文」（等于说无解）；**现更正为「有正文、措辞不符、须以用神为主」**——变成**可解**的人判项：改写 statement 或补用神事实 |
| 1 | 奇门「X临Y」块 | 8 条（qimen 70%→~90%），三选一需授权／跨仓协调（t184） |
| 2 | 紫微命名格局 4 条记录 | 只差宫地支一笔 passthrough（t183） |
| 3 | 其余 | 沿用 t179：需授权（闸门判据、引擎投入、`daxian`）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：折半检索与纠错
python3 tools/han_search.py 游魂 归魂 月朗天门 贪火相逢
python3 tools/test-han-search.py                 # diverges 判定 + t177 错案 + 台账引文逐字

# 三条的正文（人工复核用）
sed -n '7720p;7722p;7724p;7726p;7728p;7730p' sources/fulltext/divination/zengshan-buyi/fulltext.md
sed -n '407p' sources/fulltext/divination/bushi-zhengzong/fulltext.md

# 三条仍未映射（结论没变，理由变了）
python3 -c "
import yaml,glob
for f in glob.glob('references/books/divination/*/rules.yaml'):
    for r in yaml.safe_load(open(f))['rules']:
        if r.get('rule_id') in ('ZR-09','ZR-13','ZENGSHANBUYI-ZR-13'):
            print(r['rule_id'], r.get('applicable_to'))"

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

**规则与词表零改动**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `d5b84e2ffe7b1e4da0e18c8a2e45e5923394dbf3`；产品仓无需重新导出。
六术覆盖率不变：bazi 49.4%／ziwei 67.7%／qimen **70.0%**／liuren 22.6%／liuyao 31.9%／qizheng 24.4%。

**给消费方的一条提醒**：`tools/reports/ungrounded-claims.json` 里
`t177_correction` 已被 `t185_correction` 更正 —— 若你有流程在读它，请以最新一条为准。
（该文件记录的是「statement 断言的概念在锚定原文里找不到」的情形，
本轮结论是：这三条**找得到**，只是措辞与原文不符、且原文禁止单凭此断。）

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。