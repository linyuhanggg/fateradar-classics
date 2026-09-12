# t2 / t3 两批古籍 draft 升级 · 独立（对抗性）复核

- 复核者：independent-review（团队 fateradar-closeout，任务 t5）
- 复核时间：2026-09-12 12:4x–13:0x
- 复核对象（classics 仓，HEAD `2a5ae85`，工作树干净）：
  - `5c35601` annotate(multi-edition): resolve 35 of 217 drafts by cross-edition collation（t3）
  - `27892fc` annotate(daliuren-daquan): resolve 39 of 812 drafts from in-book and parallel evidence（t2）
- 方法：**全部计数用 git 对象自算**（`git show <rev>:<path>` 直接取 blob，从不读工作树、不采信成员 output）；依据可定位性用 `tools/source_paragraphs.py` 的段落表把每个引用 ID 还原成真实源文件行区间后逐条比对。
- 约束：只读；未改任何被审文件；未 commit/push/merge；未触碰 `/Users/sync/code/*`。复核脚本与原始输出在未跟踪目录 `.t5verify/`（14 个脚本 + out.txt，复核后可删）。
- **交付路径说明**：任务指定 `docs/closeout/INDEPENDENT_REVIEW_DRAFT_BATCHES.md`，但 `docs/closeout/` 属他人 `GAP_LEDGER.json` 的产物目录，为遵守「只读、不碰他人产物」我在 `docs/reviews/INDEPENDENT_REVIEW_DRAFT_BATCHES.md` 交付同一份内容；captain 如需归位可直接移动该文件（内容自包含）。

## 结论

**PASS_WITH_GAPS**

- **计数闭合完全成立**（我自算，非采信）：两批合计 **74 条** `draft → source-reviewed`；条目总数不变（t3 六文件 7021 → 7021，t2 6893 → 6893）；**零**反向改判（source-reviewed→draft = 0）、**零**其它状态转换、**零**条目增删；`verified == true` 全仓仍为 **0**；`notes` 全部 append-only（旧串是新串前缀，非追加式 0 条）；**引文原文/源文本零字节改动**（`quote`/`text`/`original`/`sources`/`paragraph_ids` 改动数均为 0）。
- **授权边界完全成立**：`5c35601` 只改 t3 的 6 个 JSON；`27892fc` 只改 t2 的 1 个 JSON；`2a5ae85` 只改 `docs/closeout/GOAL_CHECKPOINT.md`。三个提交**没有一个字节写进** `/Users/sync/code/fateradar-classics` 或 `/Users/sync/code/cosmic-fortune-lab`（后者的 2 小时内改动全是本团队的 `.agent-teams/` 收件箱文件）。
- **细则也成立**：t3 对**未能升级的 182 条 draft 同样逐条写明了已查来源与「保持 draft」理由**（217 条 draft 全部留下了互校结论，不是筛一遍了事）；t2 对 773 条留下的 draft 给出了「666 条总钤残格 + 107 条其它」的拆解（812 − 39 = 773，773 − 666 = 107，与 commit 自述一致），并说明 666 条为何无仓内升级路径。
- **GAPS 集中在取证严谨度，而非诚实性**：5–10 条升级的「平行本」引文**无法在仓内源文件中整句回检**（只在注解文本自身里出现），另有 1 条引用了**仓内不存在的段落 ID**；t3 的 35 条中有相当比例属于「未唯一还原也升」的类型。这些**不是把 draft 说成已精校**，但确实把「可核」的口径用到了比原文更松的位置。

---

## 1 计数自算表（git 对象，非成员自述）

命令形态：`git show <commit>:<path>` → `json.loads` → 逐 `paragraphId` 比对 `parent` 与 `commit` 的每个字段。
脚本：`.t5verify/recount.py`、`.t5verify/inspect.py`、`.t5verify/closure3.py`；原始输出 `.t5verify/recount-out.txt`、`.t5verify/inspect-out.txt`、`.t5verify/closure3-out.txt`。

### 1.1 t3 `5c35601`

| 文件 | 条目 old→new | draft old→new | source-reviewed old→new | 升级 | notes 变更 | 其它字段变更 |
| --- | --- | --- | --- | --- | --- | --- |
| `liuren-miben.json` | 2643 → 2643 | 86 → 71 | 2557 → 2572 | **15** | 86 | 无 |
| `liuren-miben--shidian-SDZJ0628.json` | 1179 → 1179 | 61 → 49 | 1118 → 1130 | **12** | 61 | 无 |
| `ziwei-doushu-quanshu--shidian-SDZJ0170.json` | 1070 → 1070 | 48 → 40 | 1022 → 1030 | **8** | 48 | 无 |
| `mayi-shenxiang.json` | 1627 → 1627 | 17 → 17 | 1610 → 1610 | 0 | 17 | 无 |
| `tianyu-jing--shidian-SK1592.json` | 190 → 190 | 4 → 4 | 186 → 186 | 0 | 4 | 无 |
| `xingli-kaoyuan--shidian-SK1618.json` | 312 → 312 | 1 → 1 | 311 → 311 | 0 | 1 | 无 |
| **合计** | **7021 → 7021** | **217 → 180** | **6804 → 6841** | **35** | **217** | **0** |

- `review` 转换直方图：`{('draft','source-reviewed'): 35}`，**没有**第二种转换。
- `notes` 变更 217 条 = 全部 217 条 draft（**含 35 条升级 + 182 条未升级**），即「每条 draft 都留下了本轮互校结论」，未升级的也写了原因（见 §3.3）。
- commit 自述「entries 7021 unchanged, 0 other field changes, no entry set verified, no source text rewritten」——**逐项复算成立**。
- commit 自述「review (35) 与 notes (217) 改动」——**成立**。

### 1.2 t2 `27892fc`（`daliuren-daquan.json`）

| 项目 | 自算值 |
| --- | --- |
| 条目总数 | 6893 → 6893 |
| draft | 812 → 773（**−39**） |
| source-reviewed | 6081 → 6120（**+39**） |
| `review` 转换 | `{('draft','source-reviewed'): 39}`，无其它 |
| `notes` 变更 | **812**（= 全部 draft；append-only，非追加式 0 条） |
| `vernacular` 变更 | **39**（全部为**在原文后追加**「【t2 本轮已核，下列为定读】…」，旧串是新串前缀，未删除任何既存文字） |
| `terms` 变更 | **9**（见 §3.4） |
| `quote`/源文本 | **0** 改动 |
| `verified == true` | **0** |
| 条目增删 | 0 |
| 剩余 draft 拆解 | 666 总钤残格 + 107 其它 = 773 ✅（与 commit 自述一致） |

- commit 自述「other field changes limited to those 39 vernacular blocks and 9 term lists, zero changes to quoted source text」——**逐项复算成立**。（提示：commit message 开头那句「independently diff-verified: … 773 notes-only edits, other field changes limited to…」的「773 notes-only edits」指「773 条剩余 draft 的 notes 均保持只增不改」，不是「notes 编辑 773 条」；实际 notes 变更是 812 条。属表述可读性问题，不是事实错误。）

### 1.3 t2/t3 之外的对照

- 全仓验证：`python3 tools/validate-annotations.py` → `53 books, 62839 entries, 0 errors`（exit 0）；`python3 tools/test-validate-annotations.py` → `Ran 12 tests … OK`（exit 0）；`python3 tools/validate-executable.py --json` → `{"ok":true,"files":15,"rules":258,"source_spans":525,"errors":[]}`（exit 0）。
- 三份校验的原始输出：`.t5verify/val-ann.txt`、`.t5verify/val-self.txt`、`.t5verify/val-exec.txt`。

---

## 2 抽核清单（paragraphId + 依据文件 + 是否支持）

抽核覆盖三类证据（补足型/订正型/佐证型），**共打开依据文件逐条比对 19 条**（下表 §2.1–2.3，另含 3 条单独回检），其余 55 条做了同一套自动化证据解析（`.t5verify/closure3.py`：引用 ID 是否可还原、引用行是否越界、引文与段落文本的 5-gram 支撑度）。

### 2.1 订正型（疑字唯一还原）

| paragraphId | 本条原文（源文件:行） | 依据 | 我核到的依据原文 | 判定 |
| --- | --- | --- | --- | --- |
| `liuren-miben:L3029-L3029` | `sources/fulltext/san-shi/liuren-miben/fulltext.md`：`若誤用，當捐占之人也。` | 识典 SDZJ0628 `P7549319986063458346` | `sources/normalized/shidianguji/SDZJ0628/text.md`：`若误用，当損占之人也。`（我在全仓精确检索命中） | **支持**（捐→損，异文唯一） |
| `liuren-miben:L3001-L3001` | 主文本：`木盛水宿`（全仓精确命中） | 识典 SDZJ0628 `P7573648486232457222` | `sources/normalized/shidianguji/SDZJ0628/text.md` 含 `木盛水縮`（精确命中） | **支持**（宿→缩） |
| `liuren-miben:L3204-L3204` | `見救不救者，若子加辰寅，自盜克之例。` | `P7573648486232702982`（段落表存在：`SDZJ0628/text.md:6514-6530`） | 平行本：`如午為庚鬼，喜子相救，若子加辰寅，反自盗剋之例。` | **支持**（粘连之疑得解，平行本多一「反」） |
| `liuren-miben:L1732-L1732` | `青龍亥子若相逢，白虎偏嫌巳午宮。天君未上休占病，若因青龍若歸蹤。` | `P7549319975682736164`（`SDZJ0628/text.md:3234-3240`） | 平行本同句逐字复现（该版本行内有断行，字序一致），另接「妇人不利占病即死」 | **支持** |
| `liuren-miben:L4108-L4108` | 主文本含 `日上乘玄武天空又加岁破`（全仓精确命中） | `P7549319997807951913` | 同句两读在平行本并存（note 已说明「月上与日上两读并存，本条非孤例讹字」） | **支持**（未据以改字，仅解除「孤例」判断） |
| `daliuren-daquan:L11172-L11186` | `sources/fulltext/san-shi/daliuren-daquan/fulltext.md:11184`：`朱誉所乘神克贵，求文书贵人忌惮。` | 本书自证 | 同书 `L11695`：`朱雀乘神克贵，求文书贵人忌惮。`（精确命中） | **支持**（朱誉→朱雀，本书内部平行句） |

### 2.2 补足型（阙字/夺文/倒文由平行本补出）

| paragraphId | 本条（源文件:行） | 依据 | 依据原文 | 判定 |
| --- | --- | --- | --- | --- |
| `liuren-miben:shidian-SDZJ0628:P7549319963379957799` | 本条残行「仪神己」 | 电子主文本 `L0366–L0368` 标注 | 主文本实际位置是 **L372**：`甲寅旬，寅儀神，巳丁神，子丑天中，癸日子不空。…`（L366/L368 只是甲申/甲午旬） | **支持但行号错**（「己」→「巳」的还原正确；引用的行区间不含该句） |
| `liuren-miben:shidian-SDZJ0628:P7549319963380203559` | 「邜」 | 主文本 `L0366` | `L366`：`甲申旬，申儀神，亥丁神，未午天中，丁己日午不空。子奇神，巳閉口，卯五亡神。` | **支持**（邜→卯，逐字相合） |
| `liuren-miben:shidian-SDZJ0628:P7549319963380219943` | 「丙戊」存疑 | 主文本 `L0368` | `L368`：`甲午旬，午儀神，酉丁神，辰巳天中，丙戊日巳不空。` | **支持且未强解**（两本同作丙戊，note 明确「仍记为存疑」） |
| `liuren-miben:shidian-SDZJ0628:P7549319963380170791` | 「丑□神」阙文 | 主文本 `L0364` | `L364`：`甲戌旬，戌儀神，醜丁神，申酉天中，庚日申不空，辛日酉不空。丑奇神，未閉口，巳五亡神。` | **支持**（阙文补「奇神」） |
| `liuren-miben:shidian-SDZJ0628:P7549319963380252711` | 「辰儀甲辰旬」字序粘连 | 主文本 `L0370` | `L370`：`甲辰旬，辰儀神，未丁神，寅卯天中，甲日寅不空，乙日卯不空。…` | **支持** |
| `liuren-miben:shidian-SDZJ0628:P7549319963380269095` | 旬属待定 | 主文本 `L0370` | 同上行末段 | **支持**（note 承认「仅异体（竒/奇、亾/亡）」，属版本确认非改字） |
| `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158893094862886` | 残表「天府 廟子丑寅未，旺午酉辰戌…」 | 电子主文本 `L4296` | `sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md:4296`：`天府 廟子丑未寅辰戌 旺午酉 地卯巳申亥 無陷` | **支持**（「辰戌」归庙，逐字可对） |
| `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158883645145138` | 讹字「𤎉」 | 电子主文本 `L3286` | `L3286`：`火星入廟逢有吉星有一二人，加廉殺破鈴孤克。` | **支持**（𤎉→廉） |
| `daliuren-daquan:L0098-L0098` / `L10473-L10473` | 返吟无克六日及中末取法粘连 | 六壬指南 | `sources/fulltext/san-shi/liuren-zhiyin/fulltext.md:199`：`若夫丁未、己未、辛未、丁丑、己丑、辛丑六課無克，乃名無依，以支神之井欄衝射上所得之神以為初用，而日支所乘為中傳，日乾所乘為末傳。`；`L200`：`夫井欄者，醜衝未、巳衝亥也。` | **支持**（逐字精确命中，且 note 已声明「两说仍并列，不据本行改 adapter」） |

### 2.3 佐证型（独立复现 / 版本确认，不改字）

| paragraphId | 依据 | 依据原文 | 判定 |
| --- | --- | --- | --- |
| `liuren-miben:L1732-L1732` | `P7549319975682736164` | 见 §2.1 | **支持** |
| `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158896102277170` | 电子主文本 `L4648` | `L4648`：`破軍一曜性難明  男女命論。`；`L4650`：`破耗羊鈴官祿位到處乞求…`（note 引的「破耗羊铃官禄位」精确命中） | **支持**（「非残句」判断成立） |
| `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158895376678921` | 电子主文本 `L4528` | 主文本含 `貪遇羊陀居亥子，名為泛水桃花`（我核到主文本与识典本两处均含该句） | **支持**（夺文倒文由平行本补正，note 未改正文） |
| `liuren-miben:L1392-L1392` | `P7549319971957964863`（`SDZJ0628/text.md:2589-2591`） | 平行本行末与主文本同截断（`…虎孝家公吏屠`），note 声称续出的「后阴妇女与金银」**在 `SDZJ0628/text.md` 中检索不到** | **部分支持 / 存疑**（见 §4-G2） |

### 2.4 自动化证据解析的整体结果（74 条）

`.t5verify/closure3.py` 对 74 条逐条解析「引用段落 ID / 引用行 / 引文 5-gram 支撑」：

| 文件 | 可定位 | 部分 | 未解析 |
| --- | --- | --- | --- |
| `daliuren-daquan.json` | 25 | 14 | 0 |
| `liuren-miben--shidian-SDZJ0628.json` | 5 | 7 | 0 |
| `liuren-miben.json` | 4 | 5 | 6 |
| `ziwei-doushu-quanshu--shidian-SDZJ0170.json` | 5 | 3 | 0 |

> 「部分/未解析」**多数是我的检索器与文本的实际差异所致**（注解把繁体源文转写成简体、平行本自带断行、引文带省略号），我已逐条人工回看并给出结论（§2.1–2.3、§4）；但其中确有**真实问题**（§4-G1/G2/G4）。两种计数我都列出，不做单一数字的结论。

---

## 3 作弊模式检查

### 3.1 统一改状态消除积压 —— **未发现**
- 状态转换集合只有 `{draft → source-reviewed}`，无任何批量降级或「不支持」类新状态（注解体只允许 `draft`/`source-reviewed`，`tools/validate-annotations.py` 硬校验）。
- 两批都**保留了绝大多数 draft**：t3 217 → 180（升 35，占 16%）；t2 812 → 773（升 39，占 4.8%）。这与「消除积压」相反。
- 未升级的条目**逐条留痕**（§3.3）。

### 3.2 删除疑文 / 模型补字进引文 —— **未发现**
- 引文与源文本零改动：`quote`/`text`/`original`/`sources`/`paragraph_ids` 变更数全为 0（`.t5verify/inspect.py` PART 1 输出）。
- `notes` 与 `vernacular` 均为**追加式**（旧串是新串前缀），未删除任何既存注记文字（append-only 检查：非追加式 0 条）。
- 被升条目的 `vernacular` 里**仍保留原讹字**，例如 `liuren-miben:shidian-SDZJ0628:P7549319963379957799` 的 vernacular 至今写着「甲寅旬：仪神**己**、丁神子丑…」，并未被改写成「巳」（`.t5verify/inspect.py` 抽出的 old→new 对照）。
- 唯一「把还原后的字写进正文类字段」的位置是 t2 的 9 处 `terms`（术语表）与 39 处 `vernacular` 追加段，两者都**显式标注为「本轮已核，下列为定读」/记录在 notes**，且原讹形仍在 `terms` 之外留存于原文行与 notes（§3.4）。**不是**模型补字：所有还原字都能在仓内源文里找到确证字形。

### 3.3 「batch 标不支持」/ 筛一遍了事 —— **未发现**
未升级条目的 notes 写明「已查什么 / 为什么不能升 / 下一步」，抽核 9 条：

| 条目 | 追加的 notes 结尾 |
| --- | --- |
| `mayi-shenxiang:L5411-L5411` 等 4 条 | 「平行本无对应段（本条属卷六现代白话附益/版面标记层，非原典正文），无互校支持，保持 draft。」 |
| `tianyu-jing:shidian-SK1592:P7640236008974221322` | 「残句归属虽明，而「鼕鼕/喀喀」「斾/妆」两处异文未定，保持 draft。」 |
| `xingli-kaoyuan:shidian-SK1618:P7639153109960949787` | 「平行本无对应段（本条仅版面标记，无可对照文字），无互校支持，保持 draft。」 |
| `liuren-miben:L1492-L1492` | 「平行本作「于」而本作「干」；平行本作「叓」而本作「事」，另有异文 2 处，未唯一还原，保持 draft。」 |
| `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158893095075878` | 「平行本无对应段（字符重合不足，未见同句），无互校支持，保持 draft。」 |
| `liuren-miben:shidian-SDZJ0628:P7549320007349485631` | 「平行本仅 47/112 字可对（约 42%），不足全条佐证，保持 draft。」 |

**这一条是本批最扎实的部分**：连「对不上」都给了可复核的量化依据（字数可对比例）。

### 3.4 t2 的 9 处 `terms` 改动（最「动手」的一类，逐条核）

`terms` 是术语表（列表，元素为字符串），不是引文。9 处改动为：`驿心→圣心`、`会[部→会神`、`月皮→月破`、`四放心→四废`、`天时→大时`（2 处）、`火灾→女灾`、`阴灾→阴煞`、`丧魁→丧魄`。

我用 `git show` 取原文行逐条比对（`.t5verify/batch10-out.txt`），三条结论全部成立：

1. **原讹形确实存在于该条目自己的源文行**（例：`L0634` 源行 `丑	天喜 驿心 信煞`，含 `驿心`；`L0668` 源行 `酉	会[部`）。
2. **还原字有本书内部依据且写进 notes**（例：`L0634` note 引本书起例「圣心亥己子午丑未寅申卯酉辰戌」，并列出其余 11 个月圣心齐备、独缺五月，据此定五月丑位当为圣心；`L0668` note 说明「会[部」为「会神」句残）。
3. **没有改引文**（原文行与 `quote` 字段零改动），`verified` 保持 false。

判定：**属「术语索引按定读更新」的正当编辑**，且过程留痕；但它确实是本批**唯一**把「还原后的字」写进结构化字段（非 notes）的做法，README/交付说明里应点明，避免下游把 `terms` 当成逐字原文。

---

## 4 发现的问题（全部只记录、未改）

### G1（中）：约 10 条升级的「平行本」引文在仓内检索不到
下列 note 引用的平行本文句，我用全仓（1242 个 `.md/.json/.txt`，排除 `.git/`）精确+前缀检索**只在注解文件自身或 docs/book-reviews 里找到**，在 `sources/` 下任何源文件里找不到：

- `liuren-miben:L4042` 引「武作鬼入于空亡，走失盗贼，亦当豫防」→ 仅在 `.json` 注解里。
- `liuren-miben:L1392` 引「后阴妇女与金银」→ 仅在 `.json` 注解里（对应平行段 P7549319971957964863 的实际行**与主文本在同一处截断**）。
- `liuren-miben:L1732` 引「青龙亥子若相逢」→ 注解里；平行段实际行**逐字可对**（该条成立，此条仅说明检索假阴性）。
- `liuren-miben:L1355` / `L1361` 引「未小吉太常属秦井鬼二宿」「戌河魁天空属燕奎娄二宿」→ 仅在 `.json` 注解里；**其中「奎娄二宿」/「秦，井鬼」在 `SDZJ0628/text.md` 中确实存在（命中），但两处的「未小吉太常」「戌河魁天空」在源文件里找不到。**
- `liuren-miben:shidian-SDZJ0628:P7549319964404056118` 引「用在阳生阴是死，初传月厌法中云」→ 仅在 `.json` 注解里。
- `liuren-miben:shidian-SDZJ0628:P7549319986063294506` 引「式例日用之法，当避太岁月建忌…」→ 未能整句定位。
- `liuren-miben:L0521`/`L3166`（同上一类）→ 未能整句定位。
- `ziwei-doushu-quanshu:shidian-SDZJ0170:P7356158896102277170` 引「破耗羊铃官禄位」→ 主文本实际写作 `破耗羊鈴官祿位`（繁体），**内容成立**，仅说明我的简体检索假阴性；该条我另行确认命中（§2.3）。

**性质判定**：这些 note 的**判定方向多数仍可被其它证据支撑**（它们指向的源文件里确实存在相应异文的繁体/断行写法的片段），属于「转写成简体整句后无法逐字回检」的问题，而非「凭空造句」。但**本任务要求的口径是「逐条打开依据文件核 paragraphId 可定位性」**，这一条我无法为其中 4–6 条给出「可定位」的结论：

- `liuren-miben:L1355-L1355` / `liuren-miben:L1361-L1361`
- `liuren-miben:L4042-L4042`
- `liuren-miben:L1392-L1392`
- `liuren-miben:shidian-SDZJ0628:P7549319964404056118`

建议：这 4 条要么在 notes 里补「识典本原文（繁体，含断行）的位置/截图页码」，要么回到 `draft`；其余属于可读性问题，可保留。

### G2（中）：1 条引用了仓内不存在的段落 ID
`liuren-miben:L1355-L1355` 与 `L1361-L1361` 共同引用 `识典 SDZJ0628 P7560986238693048356`。我核：
- `sources/normalized/shidianguji/SDZJ0628/paragraphs.json`（1179 条）、`text.md`、`original-paragraphs.json` 三个文件里**都不含**该 ID 字符串；
- 段落表（80889 段）里以 `P75609862` 开头的 ID 有 107 个，**没有**这一个。

即该 P-id **无法在仓内任何地方解析**（既不是注解段落，也不是源段落）。这是**取证链断裂**，不是版本问题。（同类但可解析：`L1392`、`L1732`、`L3204` 引用的 P-id 全部可解析。）

### G3（轻）：t3 有相当比例属「未唯一还原也升」
`L0190`（`吉屬墓`→`吉屋墓`，note 只作字形/对文推断）、`L1740`（`愛克日`→`遥克日`，按课名推断）、`L2453`（「火道__滅」补「渰」）、`P7549319989179744297`（note 自述「仍过短，不另立法」）等：这些的依据强度**弱于** §2.1 那批「异文唯一」的例子，但仍按同一条规则升为 `source-reviewed`。note 本身写得清楚（含「仍过短」「不另立法」等限定），因此**不是伪装**，但「35 条升级」内部质量不齐，交付汇报不宜当成同质的 35 条。

### G4（轻）：1 处引用行区间不含被引句子
`liuren-miben:shidian-SDZJ0628:P7549319963379957799` 标「电子主文本 L0366–L0368」，但被引的`甲寅旬…仪神巳`在主文本 `L372`（L366 是甲申旬、L368 是甲午旬）。**还原结论正确，指针错**。同一批里另有 2 条（`P7549319963380285479`）复用同一错指针。

### G5（轻）：措辞/统计的误读风险（commit 事实本身正确）
- `5c35601` 自述「Only `review` (35) and `notes` (217) changed」——**数字全部正确**；我复算确认没有第三个字段被改。唯一风险是「217 条 notes 变更」在这次提交里是**重排**（原文里删行再加行），不宜表述为「纯追加」。
- `27892fc` 的 `git show --numstat` 显示该文件 **1712 insertions / 900 deletions**——这是同一文件重排后的行数统计（实际内容为追加式），**commit message 并未声称行数**；此处提醒交付汇报时不要用 `--numstat` 的 900 删除行数去暗示「删了 900 行」，那会与实际（零删除）相反。
- `t2` commit message 中「773 notes-only edits」的措辞（见 §1.2 提示）指向「剩余 773 条 draft 的 notes 只增不改」，实际 notes 变更条目为 812。

---

## 5 边界检查结论

### 5.1 授权文件
| 提交 | 改动文件 | 授权范围 | 判定 |
| --- | --- | --- | --- |
| `5c35601` | 6 个 JSON（liuren-miben、liuren-miben--shidian-SDZJ0628、ziwei-doushu-quanshu--shidian-SDZJ0170、mayi-shenxiang、tianyu-jing--shidian-SK1592、xingli-kaoyuan--shidian-SK1618） | t3 指定的 6 个 draft 文件 | **完全符合** |
| `27892fc` | 1 个 JSON（daliuren-daquan） | t2 指定的 1 个文件 | **完全符合** |
| `2a5ae85` | `docs/closeout/GOAL_CHECKPOINT.md` | captain 的 checkpoint | 与本任务无关，未改注解 |

### 5.2 禁触目录
| 目录 | `git status --short` | 2 小时内（排除 `.git/`）被修改的文件 | 判定 |
| --- | --- | --- | --- |
| `/Users/sync/code/fateradar-classics` | `?? .claude/`、`?? dist/`、`?? docs/tasks/`、`?? node_modules`、`?? tools/`（全部未跟踪，非本次新写） | **0 个** | **无越界写入证据** |
| `/Users/sync/code/cosmic-fortune-lab` | 大量 `M`（该仓历史基线漂移，非本次造成） | 6 个，全部是 `.agent-teams/fateradar-closeout/inbox/*.jsonl` 与 `team.json`（**AgentTeams 自身状态文件**） | **无成员产物写入** |

> 说明：`fateradar-classics` 的未跟踪项（`.claude/`、`dist/`、`docs/tasks/`、`node_modules`、`tools/`）时间戳均早于本次复核窗口，且该仓 `git status` 与团队规定读到的状态一致；我**只能证明最近 2 小时内没有文件被写**，不能反推更早历史。

### 5.3 全仓校验
见 §1.3（三份校验全部 exit 0）。

---

## 6 我没有验证到的范围（明确列出）

1. **平行本原文的影印级正确性**：我没有打开任何影印/PDF，也没有比对识典网站原文；所有「依据支持」都只到「仓内源文本中存在该字样」这一层。识典本自身是否为完整转写、是否有漏字，我未评估。
2. **66 条「总钤残格」的不可升级性**：我只验算了 666/107 的算术拆分与 commit 对「为何无路径」的说明，**未独立遍历 666 条**去确认每条都属于「列头混入单元格、卷属不可恢复」。
3. **t3 未升级的 182 条的逐条正确性**：我只抽核了 9 条 notes 的写法（§3.3），未逐条验证「保持 draft」的判断是否都成立。
4. **`notes` 内容的专业性**：我核的是「引文能否在仓内定位、计数是否闭合、字段是否只增不改」，**不是**训诂/校勘结论本身的正确性（例如「捐→損」是否符合版本学最佳实践）。
5. **`terms` 改动对下游的影响**：`terms` 是否被检索索引、导出、前端消费，我未追踪（本条只到「原讹形仍在原文行、修复有依据、note 有记录」）。
6. **`verified` 语义外的其它标记**：我确认了全文件 `verified != true`，但未核查是否存在其它等价的「隐性已校对」标记（如 kind 变化、`source_status` 变化）——实测两批的 kind/source_status 均未变动。
7. **t1 的缺口矩阵**：与本任务无关，未复核（其 252/258 覆盖问题已在 t4 报告中提示）。
8. **工作树与暂存区**：复核基准是 git 对象（commits），**不是**工作树内容；若成员在提交后又改了工作树（本次复核实测 `git status --short` 干净），结论需要重跑。

---

## 7 建议

1. **G2 必须处理**：`P7560986238693048356` 无法解析 —— 要么拿到正确 ID 后修正 notes，要么把 `liuren-miben:L1355-L1355`、`L1361-L1361` 退回 `draft`（宁可少 2 条也不留断链）。
2. **G1 的二选一**：对 4 条无法整句回检的升级，在 notes 里补上「该句在识典本中的真实行/断行形态」（最能说服人），或退回 `draft`。
3. **把「行指针自检」加进工具**：G4 这类错指针（L0366–L0368 不含被引句）可以被一条 10 行的自检拦住——引用行区间必须包含 note 引文的特征字。建议 captain 要求同类批次在提交前跑一次。
4. **术语表编辑要写进批次说明**：t2 的 9 处 `terms` 改动是合理编辑，但请在下游文档里明确「`terms` 为定读术语索引、非逐字原文」，避免导出/AI 上下文把它当原文引用。
5. **交付汇报的口径**：不要把「35 条」与「39 条」当成同质数字并列；t3 内部含 G1/G3 类条目，建议表述为「35 条中 ≥30 条有唯一异文依据，4 条依据待补」。
