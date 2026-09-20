# 消费方数据版本 · t183 紫微格局「有据定义表」：未提供定义表 12 → 4

日期：2026-09-21。基线提交：`c52de9f`（t182 后）。
**本轮规则与词表零改动 → 消费方 `CLASSICS_REV` 不变，仍为
`da11267541a0fc500b96382e1d7b0bed004457d0`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

executable 层有 11 条记录以 `{definition: 格局名}` 为 `when`，长期只能报「未提供定义表」。
本轮回答「这些名字**在我们自己的语料里到底有没有定义**」——答案是 **8 条有、3 条没有**，
并把有定义的按原文展开接进求值器：

**未提供定义表 12 → 4**；其中 `君臣庆会`（ZWD-E-04）**已经可判**（本样本盘判**不满足**）。

## 1. 先更正我自己差点写错的一个结论

第一遍检索的结论是「**8 个名字全文 0 次**」。**那是错的。**

语料是**繁体**，而 executable 记录里的名字是**简体**：
`月朗天门` vs `月朗天門`、`贪火相逢` vs `貪火相逢`。
按简体名去繁体正文里搜，当然搜不到 —— 于是把**其实有定义**的名字误判成「查无」。

改用仓库既有的 `fold_han`（opencc t2s）把两边都折后再查，真结果完全相反：

| 名字 | 检索结论 | 依据 |
|---|---|---|
| **日月夹财** | 有据定义 | L1572「日月夾財 武守命日月來夾是也，財帛宮亦然」 |
| **君臣庆会** | 有据定义 | L1595「君臣慶會 紫微左右同守命是也」 |
| **日出扶桑** | 有据定义 | L1587「日出扶桑 日在卯守命是也，守官祿宮亦然」 |
| **月朗天门** | 有据定义（**别名体例**） | L1589「月落亥宮 月在亥守命是也，**又名月朗天門**」 |
| **月生沧海** | 有据定义 | L1591「月生滄海 月在子宮守田宅是也」 |
| **金灿光辉** | 有据定义 | L1580「金燦光輝 太陽單守，命在午宮是也」 |
| **武曲守垣** | 有据定义 | L1619「武曲守垣 武守命卯宮是也，余不是」 |
| **贪火相逢** | 有据定义 | L1617「貪火相逢 謂二星守命同居廟旺是也」 |
| 辅弼夹帝 | 无构成定义 | 只在赋文断语里（「輔弼夾帝為上品」） |
| 禄马同宫 | 无构成定义 | 只在**别门**（五行精纪／星学大成）散文歌诀里 |
| 魁命钺身 | 无构成定义 | 全文 **0 次** |
| month-chong／month-xing | 非语料名 | 引擎关系 id，不属「从原文找定义」的范畴 |

**8 条有据定义的原文，就是紫微斗数全书 L1572–1622 的格局术语表**，
体例为「名稱 構成…是也。」；别名体例是「…又名 X」。

> 这一条与 t182 是同一类教训：**检索盲区会伪造出「查无」**。
> t182 漏的是「域完备键上的单值」，本轮漏的是「繁简不折」。两次都是
> **先把「查无」当成结论，而不是当成待验证的断言**。

## 2. 交付物

| 文件 | 作用 |
|---|---|
| `references/definitions/ziwei-geju.json` | **有据定义表**：8 条逐条带 文件+行号+逐字引文+展开谓词+所需事实+缺什么；3 条无定义的带检索证据 |
| `tools/executable-definition-gaps.py` | 可得性登记册生成器（繁简折半检索，自检三态归属） |
| `tools/reports/executable-definition-gaps.json` | 登记册快照（13 条：8 有据／2 只有断语／1 查无／2 非语料名） |
| `tools/test-definition-table.py` | 引文逐字、展开求值、三态边界（已入 CI） |
| `tools/eval-executable.py` | 接入定义表（`{definition: X}` 不再一律报「无定义表」） |

### 2.1 定义表的引文是**逐处校验**的

`test-definition-table.py` 对每一处 `source`/`evidence` 都验「quote 是不是那一行的逐字片段、
文件是否存在」。它当场抓到我自己的两个错：

1. 我把登记册里**被截断的**引文（带 `…`）粘进了定义表 —— 那不是逐字片段；
2. `wuxing-jingji` 的全文路径写错（应是 `sourcing/fulltext/luming-nayin/…`，我写成了 `bazi-jixiang/…`）。

## 3. 求值结果与三态边界

| | 之前 | **之后** |
|---|---:|---:|
| 未提供定义表 | 12 | **4** |
| 信息不足 | 36 | **43** |
| 不满足 | 143 | **145** |
| 满足 | 67 | 66 |

三态分得很清楚：

- **查得到且事实齐备 → 按原文展开求值**：`君臣庆会`（ZWD-E-04）本盘 **不满足**
  （原文「紫微左右同守命是也」→ 紫微／左辅／右弼须**同在命宫**；本盘未同在）。
- **查得到但缺事实 → 信息不足**，理由写明「已据原文登记（file Lline），缺 …」：
  7 条。其中 **4 条只差「宫地支」**（日出扶桑／月朗天门／月生沧海／武曲守垣），
  另 1 条差「宫地支＋單守」（金灿光辉）、1 条差「星曜亮度」（贪火相逢）、1 条差「夹关系」（日月夹财）。
- **语料确实没有构成定义 → 仍报「未提供定义表」**，并附检索证据：3 条（＋1 条 interference）。

`scope` 匹配也顺带从只认 `pillar`/`value` 泛化为**按字段同名比**——紫微定义需要 `scope.palace`。

## 4. 如实说明：两个我**没有**动的东西

1. **宫地支（`palaces.earthlyBranch`）没有产出。** 引擎已算（`p.earthlyBranch`），
   事实层未产出，是一笔现成的 passthrough；但它的受益面是 **4 条 executable 记录 ＋ 0 条规则谓词**，
   按我 t179 立下的「按客户数量决定是否立键」标准（`sanchuan_zhi` 1 个客户即已否决），
   **本轮不立**，先如实登记。它离「值得做」只差一件事：宫支若能配合三方四正/夹邻关系层，
   受益面会明显变大。
2. **`liuyao.structure`（17 条）保持未定义。** 它在**两个仓**里都只被使用、**从未被定义**
   （归档的早期 worktree 亦然）；且其使用者所需的 `liuyao.node.element`（爻五行）、
   `liuyao.node.state`（爻旺衰／空墓）引擎未产出 —— **今天连「如实定义它」都构造不出来**。
   按「原文没写就不写」，不猜。

## 5. 未决清单（承接 t179／t181／t182）

t179 那张决策表仍有效（唯 t182 已把需人判 ⑥ 由 25 更正为 **64**）。本轮新增一条：

| # | 事项 | 卡在哪 |
|---|---|---|
| ★ | **宫地支 passthrough** | 技术上一行即可（引擎已算）；**它的价值取决于是否同时上关系层**（三方四正／夹邻），单上只值 4 条 executable 记录 |
| 2 | 星曜亮度（`s.brightness`） | 同上量过：提亮度的未映射规则仅 4 条且多为汇总体例（t180 已否决一次） |
| 3 | `liuyao.structure` 定义 | 需知道它指哪些事实的人给出定义；且 `node.element`／`node.state` 未产出 |
| 4 | 其余 | 三项需授权、三项需人判 —— 沿用 t179 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：有据定义表与求值
python3 tools/executable-definition-gaps.py        # 繁简折半检索生成登记册（约 8 秒）
python3 tools/test-definition-table.py             # 引文逐字 + 展开求值 + 三态边界
python3 tools/eval-executable.py --all | head -4    # 未提供定义表应为 4

# 单条记录的三态与理由（入参盘面状态 → 结论 + 置信度 + 出处）
python3 tools/eval-executable.py --all --json | python3 -c "
import json,sys
for r in json.load(sys.stdin)['results']:
    if r['id'] in ('ZWD-E-04','ZWD-E-11','ZWD-E-09'):
        print(r['id'], r['verdict'], '|', r['notes'][0][:110])"

# 其余闸门（本轮全绿）
python3 tools/audit-contract.py
python3 tools/test-ledger-consistency.py
python3 tools/test-tautology-register.py
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
```

## 7. 给 cosmic 的版本钉

**规则与词表零改动**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `da11267541a0fc500b96382e1d7b0bed004457d0`；产品仓无需重新导出。
六术覆盖率不变：bazi 49.4%／ziwei 67.7%／qimen 67.5%／liuren 22.6%／liuyao 31.9%／qizheng 24.4%。

**新增给消费方的一个可选产物**：`references/definitions/ziwei-geju.json`。
产品侧若愿意消费它，就能把这 11 条 ziwei 格局记录的三态理由从「未提供定义表」
升级为「按原文展开/缺某事实」，并附锚点行 —— 不需要产品改引擎事实层。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0；
本轮的「有据定义」只表示**定义能在原文里找到并逐字核对**，
不等于该原文经过人工影印核验。