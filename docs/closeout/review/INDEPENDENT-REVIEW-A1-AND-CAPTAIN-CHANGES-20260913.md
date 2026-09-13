# 独立复核（A1 可否判 pass ＋ captain 改动）· 2026-09-13

- 任务：`t22`（fateradar-closeout，`reviewer-2`）。只看实际文件与我自己的重算，不采信自报数字。
- 审查对象（我读的版本已按 md5 绑定；classics 工作树当时有他人未提交改动，我只读不改）：
  - `docs/closeout/review/a1-draft-disposition-20260913.json` — md5 `ad0982166d58f5e048f31df28b33647b`
  - `docs/closeout/evidence/a1-open-items-20260913.json` — md5 `fbbcb1b2971107b98b764b326f80b4e0`
  - `references/annotations/**`（79 文件）、`references/executable/*.json`（15 文件）、`docs/closeout/FULL-LIBRARY-DISPOSITION-20260912.md`、`docs/closeout/GAP_LEDGER.json`、`docs/closeout/DELIVERY_ACCEPTANCE.json#measured_baseline`
- 边界：未 commit/push；未改 `references/**`、`sources/**`、账本与任何交付物；未碰 `/Users/sync/code/**`。脚本与日志在 `/tmp/a6review/t22-*.py|log`。

---

## 1. A1 draft 分账 ↔ 注解集合是否一一对应 —— **成立（当前实测 2,826；任务书里的 2,835 是 t23 批次 1 之前的值）**

我自算（脚本直读 `references/annotations/**` 与分账台账，两边各自独立解析后做集合比对）：

```
注解：79 文件 / 62,839 条 = source-reviewed 60,013 + draft 2,826
      review 取值只有两类；同一 paragraphId 出现多次的 draft = 0
分账：draft_total 2826 / entries 2826 / 唯一 paragraphId 2826
      分账有、注解无 = 0 ；注解有、分账无 = 0 ；交集 2826
分类（我自算）：ledger-metadata 1531 / entry-review-pending 1287 / archived-out-of-scope 7 / source-transcription-pending 1 = 2826
      disposition_definitions 里定义的 processed-not-landed = 0 条（与 t7「已处理未入库实测 0」一致）
```

**判定：成立** —— 就是任务书描述的那种「一一对应、0 多余、0 缺失」，但**当前分子是 2,826 不是 2,835**：t23 批次 1（已提交 `8b8dab3`）把 9 条 draft 提升为 source-reviewed（台账 `batches.t23_batch1.promoted_to_source_reviewed = 9`），所以

```
target(2,835 = 60,004+2,835)  →  current(2,826 = 60,013+2,826)：draft −9、source-reviewed +9
分类侧同样平移：entry-review-pending 1,296 → 1,287（其余三类不变）
```
你给的四个分类数（1,531／1,296／7／1）与我实测的差恰好是这 9 条，**口径一致、没有对不上**。

## 2. A1 两项具名条目（682 = 666 + 16）—— **成立**

**666（《總鈐》残格）**
- 条数 666/666；**paragraphId 唯一 666/666**；四栏（`what_is_missing`／`attempts`／`product_handling`／`locator`）**空值 0**；`locator` 子栏（`line_range`／`terms`／`content_lead`）空值 0；`class` 全为 `precise-undecided-not-blocking`（682/682）。
- **抽查 7 条**（首 3 + 中 2 + 末 2：L1010/L1038/L1044/L1756/L1758/L2466/L2468）与 `references/annotations/san-shi/daliuren-daquan.json` 逐条对：
  - 每条 paragraphId **都真在注解里**（该文件 6,893 条），`review = draft`、`kind = 待核实`；
  - `locator.content_lead`（如「十二月辰：天煞、天空、死神…」「残格「巳未酉」」）**逐字出现在对应注解的 vernacular 里**；
  - `locator.terms`（8/8、1/1、3/3、2/2、2/2…）**全部**在注解文本里命中。
  → 不是「字段非空凑数」，locator 真能落到注解条目上。
  - **路径纠正**：任务书写 `references/annotations/daliuren/daliuren-daquan.json`，实际路径是 **`references/annotations/san-shi/daliuren-daquan.json`**。

**「影印在仓」这一更正**
- `sources/facsimile/other/daliuren-daquan/liuren-daquan-juan1-siku-archive-06054168.pdf` **存在**，3,458,657 字节；
- **112 页**（`/Type /Page` 计数 112、PDF `/Count 112` 双证），与条目所述「112 页」**一致**；
- sha256 = `7790f774ec92e5c1fe7bf728d7e9daf0706bf8388987ff65e4cc543b49c2df5f`，与条目所述「sha256 7790f774…」**一致**；
- 三个转录/版式件**都在仓**：`sources/normalized/san-shi/daliuren-daquan/zongqian-layout-016-025.md`、`zongqian-cells-016-020.md`、`zongqian-cells-021-025.md`（注：在 `sources/normalized/…` 而非 `sources/facsimile/…`）。
→ 「旧记『缺影印件』已推翻」这条更正是**真的**。

**16 套未确认影印底本**
- 我**全量 16 套**（不止抽 4 套）按两条路在 `sources/facsimile/**`（80 件影印文件）里搜：**slug 命中 0、书名命中 0，16/16 全是 0**；且条目自报 `facsimile_hits: []` 与我实测一致。
- 16 套为：qiongtong-baojian、huangjin-ce、meihua-yishu、zengshan-buyi、qingnang-jing、rudi-yan-quanshu、shenshi-xuankong-xue、yangzhai-shishu、lantai-miaoxuan、bingjian、shenxiang-quanbian、qimen-faqiao、yuqia-ji、guotian-jing、taiwei-fu、ziwei-doushu-quanshu。
- 台账算式自洽：`已存影印 34 + Release 影印 5 + 尚未确认 16 = 55（catalog ready）`（我另核 §1 表体 **55 行**、逐书注解条目相加 **62,839**，与注解总数一致）。

## 3. captain 改动的独立复核

### 3.1 `FULL-LIBRARY-DISPOSITION-20260912.md` §0 的逐书救应 —— **成立（我 15/15 逐书复现）**

我从 `references/executable/*.json` 的 `rules[].rescue` 逐文件重算：

```
全库：self 117 ／ none 106 ／ unimplemented 30 ／ 交叉引用 5（= ZPR-E-03×2、ZPR-E-05×1、ZPR-E-08×2）＝ 258
```
与 §0「117／106／30／5，共 258」**完全一致**。§0 说「与 §1 不符的只有 2 行」，我逐书对：
- `qiongtong-baojian`（120 条）：我算 **self 66／unimpl 10／none 44** = §0 的更正值 ✓（§1 原记 66/11/43 已过期 ✓）
- `sanming-tonghui`（20 条）：我算 **self 5／unimpl 6／none 9** = §0 的更正值 ✓（§1 原记 4/7/9 已过期 ✓）
- §0 列出的其余 **13 个文件逐书数**（bushi-zhengzong 2/0/0、daliuren-daquan 13/1/8、guotian-jing 0/0/1、liuren-zhiyin 1/0/0、meihua-yishu 0/0/1、qimen-dunjia-tongzhi 0/0/6、shenfeng-tongkao 0/0/2、xingli-kaoyuan 0/0/1、xingxue-dacheng 0/3/3、yuxiaji-xiaoliuren 0/1/5、zengshan-buyi 19/0/0、ziping-zhenquan 11/6/17〔另交叉 5〕、ziwei-doushu-quanshu 0/3/9）**我 13/13 全对**。
- §1 的合计行（第 84 行）仍写 `116/32/105/5`，§1 表体救应四列相加我算 **258** → 说明合计行确为旧快照，§0 的更正必要且正确。

### 3.2 `GAP_LEDGER.json` 的过期登记 —— **成立；但「current」列本身又过期了 9 条**

- `staleness_20260913` 登记的字段我逐条核对**属实**：`counts.source_reviewed` 文件内 59,934（文件里确为 59,934）、`counts.draft` 2,905、`counts.merged_main: false`（两分支成果均已是 origin/main 祖先 → 被证伪）、两个 baseline SHA 过期、`rules[].level` 落后（以 product 矩阵为准）、`page_consumers.other_arts` 已就地作废（`other_arts_stale: true` + 更正时间/人已写）。
- **需要再刷一次**：该块里写的「current」值 `source_reviewed 60,004`／`draft 2,835` 是 t23 批次 1 之前的数；现测 **60,013／2,826**（差 9，原因同 §1）。`DELIVERY_ACCEPTANCE.json#measured_baseline` 里同样是 60,004／2,835（`measured_at 2026-09-13T04:10Z`）。→ 两个文件要么刷新数字，要么加「截至时间」以免下次复核再踩。

### 3.3 `named_gaps` 计数 —— **成立**

我从 `references/executable/*.json` 重算：**42 条** = `source-term` **11** + `unimplemented-reason` **30** + `verdict-scope` **1** ✓；30 条的 `reason_class` = **implementation-gap 22 ／ evidence-undecided 8** ✓。30 条 ID 我逐条打印，分别是：
`DLD-E-09`（8 条 evidence-undecided 之一）、`QTB-M-02-04/02-07/06-07/06-11/06-12/07-12/08-04/08-11/09-12/10-09`、`SMTH-E-04`、`SMTH-E-06/07/08/09/10`、`XXDC-E-04/05/06`、`YXJ-E-04`、`ZPR-E-02/33/36/37/38/39`、`ZWD-E-02/09/10`（共 30）。
（`evidence-undecided` 8 条 = DLD-E-09、SMTH-E-06/07/08/09/10、XXDC-E-05、YXJ-E-04。）

---

## 4. A1 可否判 `pass` —— **可以判 pass**

A1 的 `pass_definition`：「每包去向可定位且 draft 余量逐项登记为可定位状态（**不要求清零**）＋未确认底本/残本逐项有证据条目」。逐条对照我的独立结果：

| pass 条件 | 我的独立结果 | 判定 |
| --- | --- | --- |
| 每包（55）去向可定位 | §1 表体 **55 行**；逐书注解条目相加 62,839 ＝ 注解总数；可执行规则 258 条全书对齐；无「待处理」笼统项（四类分类各有定义，`processed-not-landed` 实测 0） | **满足** |
| draft 余量逐项登记为可定位状态（不要求清零） | 台账 2,826 行 ↔ 注解 2,826 条 draft **一一对应**（0 多余/0 缺失），每条带 `file/bookSlug/paragraphId/kind/source_status/disposition/action` | **满足**（余量 1,287 条实质待审是**余量**，按定义不要求清零） |
| 未确认底本/残本逐项有证据条目 | 682 条：666 残格（唯一 locator＋四栏非空，抽样 7 条与注解逐条对得上）＋16 套未确认底本（16/16 双路搜索 0 命中）；影印在仓的更正经我实测（112 页、sha256 相符） | **满足** |

**我判 pass 的依据**：三条都能在仓内被独立复算，且我这次的复算与台账/报告逐项一致（除下文 3 条登记项）；deadline 类的「余量」被 pass_definition 明确排除在清零要求之外。

**附 3 条必须登记的项（均非阻断，但不得静默）**：
1. **数字口径刷新**：`a1-draft-disposition` 已是 2,826/1,287，而 `FULL-LIBRARY-DISPOSITION §1 合计行`（60,004／2,835）、`GAP_LEDGER.staleness_20260913` 的 current 列、`DELIVERY_ACCEPTANCE#measured_baseline`（60,004／2,835）仍是 t23 批次 1 之前的数 → 建议刷新为 60,013／2,826，或统一加「截至时间」。
2. **14 vs 16 的裁定**：条目文件自己写明「计划文档与账本 A1 写 14 套、磁盘实数 16 套，差 2 套未查明（不猜），请 captain 裁定」——这条应落到账本 A1 的 remaining/裁定栏，否则「未确认底本」总数有两个互相矛盾的数。
3. **路径纠正**：任务书与部分引用写 `references/annotations/daliuren/daliuren-daquan.json`，实际是 `references/annotations/san-shi/daliuren-daquan.json`（`references/**` 我未改，仅登记）。

**末句判定：A1 可以判 `pass`**（pass_definition 三条我均独立复算通过），前置＝落地上述 3 条登记项（口径刷新、14/16 裁定、路径纠正）。
