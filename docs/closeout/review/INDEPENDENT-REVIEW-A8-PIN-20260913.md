# 独立复核（A8 · 内容导出与版本钉）：候选 product `c300610`

- 任务：`t18`（fateradar-closeout，`reviewer-2`）。对象＝**`c300610f96bcb86ff55fbb56ee2fba002d67690f`**（`fix(A8): regenerate bazi-anchor to main, move CLASSICS_REV+CI ref to c45dfdb (three-way synced), harden generator (snapshot root + dirty-tree refusal); add pin audit (578/578 anchors 0 drift)`），9 文件 / +1030 −507。
- **先纠一处 SHA 口径**：任务书写「`c300610`（父 `20ac19b`；`20ac19b` 父 `cf0c1f7`）」，与实测不符。实测链为 `f030441`(A6, 已在 main) → `cf0c1f7`(A5) → **`c300610`(A8)** → `20ac19b`(A5b)：即 **`c300610` 的父是 `cf0c1f7`，`20ac19b` 是它的子**。因此正确的审查对象是 `git show c300610` ＝ `git diff cf0c1f7..c300610`（9 文件）；任务书里的 `git diff 20ac19b..c300610` 是**反向视图**（只 2 文件：撤掉 20ac19b 的改动）。**下面一律按 `diff cf0c1f7..c300610` 判。**
- 方法：全部只读 + 我自己建快照重跑；未 commit/push；未碰 `benchmarks/mingli-contest-2024/**`、contest-evidence 相关文件与 `/Users/sync/code/**`；探针/日志在 `/tmp/a6review`、`/tmp/a6review/*.py`，快照 `/tmp/classics-pin-c45dfdb4`，干净产品副本 `/tmp/prod-c3`。

---

## 1. 生成器改动是否只涉取源纪律 —— **成立**

我实读 `git diff cf0c1f7..c300610 -- scripts/export-bazi-source-rules.ts`（全文 56 行 diff，**只有 2 个 hunk**）：
1. `CLASSICS_ROOT = process.env["FATERADAR_CLASSICS_ROOT"]?.trim() || join(PRODUCT_ROOT, "..", "classics")`（新增覆盖 + 默认回落）；
2. `classicsRevision()` 改为不再 `try/catch` 吞错：`git rev-parse HEAD` 取不到即抛 `古籍仓 … 不是 git 仓库，无法固定 revision`（原实现 `catch { return "" }`）；
3. 新增 `git status --porcelain -- references/executable` 非空即抛（拒绝把带未提交改动的树写成 revision）。

**rules 组装 / fragments 过滤 / 输出结构未出现在 diff 里**（diff 只有上述声明与函数体，其余行全为上下文）→ 声称成立，**没有发现顺带改取源语义**。

**我加做的行为验证**（两个负例都实跑）：
- 脏树拒绝：把 `/tmp/classics-pin-c45dfdb4` 拷成 `/tmp/pin-dirty`，在 `references/executable/sanming-tonghui.json` 末尾加一个换行（`git status --porcelain` 显示 ` M`），再跑生成器 → **exit 1**，抛出「references/executable 有未提交改动，拒绝把 HEAD 写成产物 revision」；
- 非 git 目录：`FATERADAR_CLASSICS_ROOT=/tmp/notgit`（无 `.git`）→ **exit 1**（`fatal: not a git repository`），即「取不到 HEAD 即抛错」成立（旧实现会静默写成 `""`）。

## 2. 对同一 pin 可复现 —— **成立（逐字节相同）**

- 我按文档的快照法自建 pin 快照：`git clone --shared --no-checkout --branch main <classics> /tmp/classics-pin-c45dfdb4` → `git sparse-checkout set references/executable` → `git checkout --detach c45dfdb4`，结果 `git rev-parse HEAD = c45dfdb497a3ba802881a4191b976a6786a7f3d1`、`git status --porcelain -- references/executable` **干净**。
- 在干净产品副本（`git archive c300610` → `/tmp/prod-c3`，**不在真实工作树里生成，避免写坏产物**）跑：`PATH=~/.bun/bin:$PATH FATERADAR_CLASSICS_ROOT=/tmp/classics-pin-c45dfdb4 bun scripts/export-bazi-source-rules.ts` → exit 0，输出：
  ```
  bazi-anchor-rule-index: 183 条定义 -> …/bazi-anchor-rule-index.json
    按来源文件：{"guotian-jing.json":1,"qiongtong-baojian.json":120,"sanming-tonghui.json":20,"shenfeng-tongkao.json":2,"xingli-kaoyuan.json":1,"ziping-zhenquan.json":39}
    sourceRevision: c45dfdb
  ```
- 与我重生成物比对：**md5 均为 `9b5c0c907f4964443a613bacbf832fa0`**，`diff` **0 行**（与 `git show c300610:src/lib/engine/generated/bazi-anchor-rule-index.json` 及工作树文件都一致）→ 「同一 pin 逐字段 0 差异」成立（强于逐字段：逐字节）。
- 「15/15 个 JSON 磁盘 md5 == `git show c45dfdb4:…` md5」→ 我逐个算：**15/15 全部相同**（bushi-zhengzong/daliuren-daquan/guotian-jing/liuren-zhiyin/meihua-yishu/qimen-dunjia-tongzhi/qiongtong-baojian/sanming-tonghui/shenfeng-tongkao/xingli-kaoyuan/xingxue-dacheng/yuxiaji-xiaoliuren/zengshan-buyi/ziping-zhenquan/ziwei-doushu-quanshu）。
- **我加做的一条对照（说明「必须固定快照」不是空话）**：classics **当前工作树**的 `references/executable` 有 **7 个文件与 pin 不同**（daliuren-daquan、qiongtong-baojian、sanming-tonghui、xingxue-dacheng、yuxiaji-xiaoliuren、ziping-zhenquan、ziwei-doushu-quanshu —— 后续 A7/t14 已提交的改动），其余 8 个相同。→ 若用工作树生成，产物会不同却仍写「HEAD」；该 dirty 检查能挡住**未提交**改动，但**已提交**的差异只能靠「固定快照」这条纪律挡住（文档已写明，属应知口径，不是缺陷）。

## 3. 三处同步 —— **成立（逐字相同）**

| 位置 | 值 |
| --- | --- |
| `src/lib/rules/source-link.ts` `CLASSICS_REV` | `c45dfdb497a3ba802881a4191b976a6786a7f3d1`（40 位） |
| `.github/workflows/ci.yml` classics `ref` | `c45dfdb497a3ba802881a4191b976a6786a7f3d1`（**逐字相同**） |
| `src/lib/engine/generated/bazi-anchor-rule-index.json` `sourceRevision` | `c45dfdb497a3ba802881a4191b976a6786a7f3d1`（逐字相同） |
| 同一提交另钉的 `tiaohou-profiles.json` `sourceRevision` | `c45dfdb497a3ba802881a4191b976a6786a7f3d1` |
| `docs/closeout/VERSION_MAP.json` `generated_pins.tiaohou` | `c45dfdb497a3ba802881a4191b976a6786a7f3d1` |

即「三处（连 tiaohou 实为四处）同步」成立，且都是**完整 40 位**（不是短 sha 与全 sha 混用）。其余 5 份产物仍钉各自旧 revision（liuyao `b8150a72…`、qizheng `3fbef8c5…`、qimen `5379881d…`、ziwei `3ca4a47d…`、liuren `a6c01820…`、reading-notes `a8edc922…`，= VERSION_MAP 的 `readingNotes` 值）——与账本「登记为 remaining、不冒充已解决」一致，**不作为缺陷**。

## 4. 锚点收口（补 captain 未做完的 liuyao 81 + qizheng 8）—— **0 漂移**

方法：对每份产物里每条 `fragments[]`，取 `{"file","startLine","endLine","quote"}`，用 `git show <产物自身 sourceRevision>:<file>` 与 `git show c45dfdb4:<file>` 各取同一 `startLine..endLine` 行区间，**空白归一（去所有空白）后比对**，并把 `quote` 分别在两处文本里做「包含」判定。结果：

```
liuyao-source-rules.json  (rev b8150a72…)  ：可读锚点 81/81 | 行区间漂移 0 | quote 不符 0 | 读不到文件 0
qizheng-source-rules.json (rev 3fbef8c5…)  ：可读锚点  8/8  | 行区间漂移 0 | quote 不符 0 | 读不到文件 0
```
用到的源文件：`sources/fulltext/divination/{bushi-zhengzong,zengshan-buyi}/fulltext.md`（六爻）、`sources/fulltext/xingming/xingxue-dacheng/fulltext.md`（七政）。

**合上 captain 的 489**（bazi-anchor 362、liuren 82、ziwei 21、reading-notes 12、qimen 12）→ **578/578 全量覆盖、0 漂移**。我另核了 578 的构成（自算每份产物的锚点数）：`bazi-anchor 362 + liuren 82 + liuyao 81 + qimen 12 + qizheng 8 + reading-notes 12 + ziwei 21 = 578`（`tiaohou-profiles.json` 无 fragments，计 0）→ **数字自洽**。

## 5. 同级收口的正确性 —— **成立；但有一处明细变化要如实说明**

| 声称 | 我的独立结果 | 判定 |
| --- | --- | --- |
| `tiaohou-profiles.json`「除 revision 外逐字节相同」 | `git diff cf0c1f7..c300610 -- src/lib/engine/generated/tiaohou-profiles.json` **只有 1 行变化**：`"sourceRevision": "83c654b9638d9b75f8c26cbb9ea5f3825b077d15"` → `"c45dfdb497a3ba802881a4191b976a6786a7f3d1"`（diff 共 12 行，其余为上下文） | **成立** |
| `VERSION_MAP.generated_pins.tiaohou` 与之一致 | VERSION_MAP 同提交改的就是这一行（`83c654b9…` → `c45dfdb4…`），与产物一致 | **成立** |
| `art-verdict-consumer-points.*` 重跑后「probed 52 / appeared 50 / notProbed 4」与改前相同 | 我逐 id 比对 before(`cf0c1f7`)/after(`c300610`) 的 `fixture_probe`：`probed 52 → 52`、`appeared 50 → 50`、`notProbed = [ZSB-E-15, ZSB-E-17, ZSB-E-18, ZSB-E-19]` 不变；**逐 id 的 `appeared`/`probed` 布尔值零翻转**（0 个 id 翻） | **成立（汇总层与逐 id 布尔层都成立）** |
| （我加做）该文件是否「内容相同」 | **不是**：`fixture_probe.byId` 的 56 条里有 **37 条内容变化**，集中在 `via` 与 `otherIds` 的选择/顺序（例：`DLD-E-01` 的 `via` 由 `BIRTH_DLD_E_02` 变 `BIRTH_DLD_E_20_FAIL`；`DLD-E-09` 的 `otherIds` 由 `["BIRTH_DLD_E_20_SAT"]` 变 `[]`），另有 `generated_at` 更新。原因可解释：本候选把 `bazi-anchor-rule-index` 重钉到 `c45dfdb4`（规则内容变了），probe 的「经由哪条点出现」随之变化 | **成立但须写明**：笼统说「重跑结果与改前完全相同」不准确，应写成「probed/appeared/notProbed 与逐 id 布尔值不变；byId 的 via/otherIds 明细会随 anchor 重钉而变」 |

---

## 6. 结论

五件事：① 生成器 diff 只有取源纪律三处（并有脏树/非 git 两个负例实测）→ **成立**；② 同 pin 重生成**逐字节相同**（md5 9b5c0c90…）+ 15/15 JSON md5 相符 → **成立**；③ `CLASSICS_REV` = CI ref = 产物 `sourceRevision` = tiaohou pin = VERSION_MAP **逐字相同**（均 40 位）→ **成立**；④ 我补核的 liuyao 81 + qizheng 8 **0 漂移**，合 489 → **578/578 全量 0 漂移，构成自洽** → **成立**；⑤ tiaohou「仅 revision」与 VERSION_MAP 一致**成立**，consumer-points 的 `probed/appeared/notProbed` **成立**（但 byId 明细 37 条变化，须按上面口径描述）。

**没有发现必修项**。两条非阻断建议：**(a)** 把 `art-verdict-consumer-points` 的口径写成「汇总计数与逐 id 布尔不变；byId 的 via/otherIds 会随 anchor 重钉变化」，避免下次复核把明细差异误判为回归；**(b)** 生成器文档已在注释里写明「输入必须固定成快照」，建议把「已提交但非 pin 的工作树也会生成不同产物」这句话一并写进 `docs/implementation/A8-CONTENT-REVISION-PIN-AUDIT.md`（dirty 检查只覆盖未提交改动）。另建议顺手修正任务书里的 SHA 父子关系（`c300610` 的父是 `cf0c1f7`）。

**末句判定：可合 main**（A8 候选 `c300610` 内无必修项；两条建议为非阻断登记项）。
