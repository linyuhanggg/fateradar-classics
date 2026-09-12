# B2 · 大六壬《總鈐》殘格 666 條 底本溯源報告

檢索日期：2026-09-12（DSH 子任務 session，research-only）
執行範圍：`/Users/yuhanglin/fateradar-goal-20260912/classics`（只讀）＋ 公開網路來源
寫入範圍：本檔一個（`docs/closeout/B2-DALIUREN-RESIDUE-SOURCE-HUNT.md`）

> **後續更正（2026-09-12，由 B4 實取該章後提出，`docs/closeout/B4-SHIDIAN-SK1599-ZONGQIAN-FETCH.md`）**
> 本報告對識典 SK1599「總鈐」章的結構描述「**10 個帶列結構的表（各 25 列）**」（見 §3 與 §6.7 等處）
> **不成立**。實際抓取該章後（HTTP 200、767,385 B）比對原始 payload：每個表是
> **25 行 × 每行 1 格**（`cellType:2, rows:1, cols:1`），`table.head` 為空 ——
> **源資料不保留任何列軸**，因此不存在可供逐格落位的列座標。可支持的軸是**十干**（一表一干）。
> 本報告其餘結論（影印在倉內、頁碼定位、666 條維持 draft、二級數字化本不能投票）**不受影響**，
> 且其核心觀察（殘格把「五甲」拆成「甲五」等）已由 B4 以逐格原文證實。
> 另：本報告給出的比值 0.97 經 B4 重算為字元盤比值 **0.9904**，但兩者是**不同線性化**
> （分干序列相似度僅 0.08–0.24），順序與格址**不可復原**。

---

## 0. 誠實聲明（先讀）

1. 本報告**沒有**把任何條目升為 `source-reviewed`，也**沒有**改動 `references/` 下任何檔案。
   本任務只做來源定位，寫入僅限本檔。
2. 本輪**最重要的結論是「影印底本其實已在倉內」**，與 `docs/closeout/GOAL_CHECKPOINT.md`
   及多條註解 notes 所寫的「倉內無《大六壬大全》影印」**直接衝突**。該斷言是錯的，見 §1.1。
3. 本報告區分三種證據強度，全篇遵守：
   - **[開啟]** = 我實際抓取到內容（HTTP 200 且讀到位元組）；
   - **[影像]** = 我實際下載了該頁影像檔並在本地對它做過處理／OCR；
   - **[僅搜尋片段]** = 只在搜尋結果裡看到標題／摘要，**未開啟**，不作為依據。
4. **我無法可靠讀出表格單格內容**：本 session 的模型無影像輸入能力，
   只能用 `tesseract` 對掃描件做 OCR。四庫全書刻本表格為孤立單字格，
   在 `chi_tra_vert` 下輸出為亂碼（§3.5 有實測輸出）。因此
   **「頁碼定位」成立，「單格取值校驗」不成立**。任何據此宣稱已還原某格的說法都是編造。

---

## 1. 委託內容與精確範圍（本地實測，非引用舊文件）

### 1.1 受影響語料

| 項 | 實測值 | 取法 |
|---|---|---|
| 註解檔 | `references/annotations/san-shi/daliuren-daquan.json` | — |
| 全檔條目 | 6893 條 | `len(entries)` |
| 其中 `review` 分布 | `source-reviewed` 6120 / `draft` 773 | — |
| **目標集合** | **666 條**（`review=draft` 且 `kind=待核实` 且內文含「残格」） | 見下重現指令 |
| 集合內同時含「总钤」 | **666 / 666**（全部） | — |
| 目標集合的行號跨度 | `L1010`–`L2468` | — |
| 落在 21 個「总钤…残格」分組內 | 664 條 | scopeNote 分組 |
| 落在分組外 | 2 條：`daliuren-daquan:L1010-L1010`、`daliuren-daquan:L1038-L1038` | 邊界條目 |
| 同檔其餘 draft | 107 條（`773 − 666`，非總鈐） | — |

重現指令（只讀）：

```bash
cd /Users/yuhanglin/fateradar-goal-20260912/classics
python3 - <<'EOF'
import json
d=json.load(open('references/annotations/san-shi/daliuren-daquan.json'))
S=[x for x in d['entries'] if x.get('review')=='draft'
   and '残格' in json.dumps(x,ensure_ascii=False)]
print(len(S))                      # -> 666
print(sum('总钤' in json.dumps(x,ensure_ascii=False) for x in S))   # -> 666
EOF
```

### 1.2 21 個分組與各組 draft 殘格數（依 scopeNote 的行區間實測）

| # | 分組（scopeNote 原文） | 行區間 | 區間內 draft 殘格 |
|---:|---|---|---:|
| 1 | 总钤甲巳至甲戌残格 | L1040–L1118 | 35 |
| 2 | 总钤甲寅至乙申残格 | L1120–L1202 | 40 |
| 3 | 总钤乙辰至乙戌残格 | L1204–L1260 | 26 |
| 4 | 总钤乙寅至乙亥残格 | L1262–L1306 | 22 |
| 5 | 总钤丙巳至丙酉残格 | L1308–L1364 | 26 |
| 6 | 总钤丙卯至丙亥残格 | L1366–L1434 | 33 |
| 7 | 总钤丁巳至丁酉残格 | L1436–L1518 | 39 |
| 8 | 总钤丁卯至丁亥残格 | L1520–L1598 | 38 |
| 9 | 总钤戊巳至戊酉残格 | L1600–L1672 | 34 |
| 10 | 总钤戊卯至戊亥残格 | L1674–L1730 | 27 |
| 11 | 总钤己巳至己申残格 | L1732–L1790 | 29 |
| 12 | 总钤己辰至己酉残格 | L1792–L1828 | 17 |
| 13 | 总钤己卯至己亥残格 | L1830–L1900 | 34 |
| 14 | 总钤庚巳至庚酉残格 | L1902–L1966 | 30 |
| 15 | 总钤庚卯至庚亥残格 | L1968–L2026 | 28 |
| 16 | 总钤辛巳至辛酉残格 | L2028–L2118 | 43 |
| 17 | 总钤辛卯至辛亥残格 | L2120–L2202 | 40 |
| 18 | 总钤壬巳至壬酉残格 | L2204–L2266 | 29 |
| 19 | 总钤壬卯至壬亥残格 | L2268–L2336 | 33 |
| 20 | 总钤癸巳至癸酉残格 | L2338–L2390 | 24 |
| 21 | 总钤癸卯至癸亥残格 | L2392–L2468 | 37 |
| | **合計** | | **664**（＋區間外 2 = 666） |

### 1.3 受影響的「rule ID」

**沒有 executable rule ID 直接受影響。** 實測：

- `references/executable/daliuren-daquan.json`：22 條規則，逐條掃描後 **0 條** 含「总钤 / 總鈐」。
- `references/books/san-shi/daliuren-daquan/rules.yaml`：僅 3 處提到總鈐，全在四庫提要引文內
  （提要「首載《入手法》、《总钤》及貴神月將徳煞」），不是可執行規則 id。

因此本缺口的作用域是**註解段落，不是規則**。受影響識別碼即 666 個
`paragraphId`（形如 `daliuren-daquan:L1044-L1044`），完整清單可由 §1.1 指令匯出。

### 1.4 缺口性質（與前一輪描述一致的部分）

主文本 `sources/fulltext/san-shi/daliuren-daquan/fulltext.md` 的 L1040–L2468 是
《總鈐》表被壓平成單一文字流後的結果：表頭被抽進儲存格流，
只剩孤立地支與疑字（例：`甲五`、`甲四`、`六`、`甲`、`日` 各自成行），
列歸屬不可由該電子本自身復原。**這是真的**，本輪確認無誤。

---

## 2. LOCAL SEARCH RESULTS（本地檢索，逐項列出）

### 2.1 ★ 關鍵發現：四庫全書 0808 冊影印 **已在倉內**

| 項 | 值 |
|---|---|
| 路徑 | `/Users/yuhanglin/fateradar-goal-20260912/classics/sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 大小 | 98,547,126 bytes（與 MANIFEST 宣稱一致） |
| sha256 | `38d40b5cb9beb1282ea33c794224cee148012c8c1fcba7b2f3952901f816f2db` |
| 檔案頭 | `AT&TFORM` / `DJVMDIRM` → 真 DJVU，非 LFS 指標 |
| 頁數 | 987（Commons API `pagecount`） |
| 掃描原生尺寸 | 1237 × 1864 px／頁 |
| 入庫提交 | `2da4bf9`（2026-09-04 01:37:49 +0800，"data: add Wikisource facsimiles and recovery manifest"），已是 HEAD 祖先 |
| 登記 | `sources/facsimile/wikisource/MANIFEST.md` 表 F07，逐書狀態表第 23 列「大六壬大全 → 共享 F07 → 已下載」 |

**sha256 與 `references/books/san-shi/daliuren-daquan/source-manifest.yaml` 中宣稱的
`Siku-Wenyuange-0808.djvu` sha256 完全相同**，但該 manifest 寫的路徑
（`sources/raw/san-shi/daliuren-daquan/Siku-Wenyuange-0808.djvu`）**不存在**。
即：檔案在，只是登記路徑寫錯，導致後續輪次誤判為「無影印」。

同一 manifest 的 `local_files` 還有兩類**實際不存在**的條目（我逐條 `test -e` 驗過，全部 MISSING）：

- `sources/raw/san-shi/daliuren-daquan/Siku-Wenyuange-0808.djvu` — MISSING
- `sources/raw/san-shi/daliuren-daquan/kanripo/KR3g0031_001.txt` … `_012.txt` — MISSING（12/12）
- `references/fulltext/san-shi/daliuren-daquan/fulltext.md` — MISSING（實檔在 `sources/fulltext/...`）
- `sources/raw/san-shi/daliuren-daquan/wikisource_raw.txt` — MISSING

→ 結論：manifest 的 Kanripo 與 0808 兩組路徑是**未落地的宣告**，
但 0808 影印以另一個路徑實際存在。`GOAL_CHECKPOINT.md` 的
「仓内无《大六壬大全》影印」與註解 notes 的「sources/facsimile 亦无大六壬大全影印」
**應予更正**。

### 2.2 本地逐項檢查清單

| 檢查位置 | 指令／方式 | 結果 |
|---|---|---|
| 倉內 `sources/facsimile/` 全樹 | 完整 `find`（含 `other/`、`wikisource/`、`wikimedia-known/`、`missing-recovery/`） | **只有** `文淵閣四庫全書 0808冊.djvu`（＋0809冊）涵蓋六壬大全；無獨立《六壬大全》檔 |
| `sources/facsimile/other/` 18 個書目子目 | 逐目錄列出 | 無六壬大全（僅 liuren-zhiyin = 六壬指南，不同書） |
| `sources/raw/` | `ls` | 只有 `divination/`；**無 `san-shi/`** |
| `references/fulltext/` | `ls` | **不存在** |
| git 索引 | `git ls-files \| grep -i "kanripo\|0808\|raw/"` | 只有 `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` 與 `sources/raw/divination/zengshan-buyi/...json` |
| git 歷史（是否曾入庫） | `git log --all --diff-filter=A -- '*Siku-Wenyuange*' '*KR3g0031*'` | **空**：這兩個路徑從未入庫 |
| 結案歸檔 `fateradar-closeout-20260912/classics/sources` | 完整樹 | 與主倉同構，無六壬大全影印 |
| 結案歸檔全樹 | `find … -iname "*壬*"` | **0 命中** |
| `/Users/yuhanglin` 名含 六壬/liuren/daliuren 的 pdf/djvu（depth ≤ 6） | `find` | **0 命中** |
| `/Users/yuhanglin` depth ≤ 5 的 pdf/djvu 總數 | `find` | 51 個，逐一以檔名核對，**無六壬大全** |
| 全機磁碟內容掃描 | 未完成 | 全 home 目錄 `find` 逾時被 kill；上列為 name-based 有界檢索，**不足以宣稱「全機絕對沒有」** |
| `sources/normalized/shidianguji/SK1599/` | 現存下載本 | 與註解 notes 一致：**無總鈐章節**（見 §3.4：這是下載不全，不是站上沒有） |
| `references/source-editions.json` 的 SK1599 `missingChapters` | 解析 | 內含 `{"chapterId":"1m1g2eil4og7e","expected":11,"actual":0}` — **正是總鈐章**，11 段全缺 |

---

## 3. PUBLIC SOURCE RESULTS

下列每一條都標明 **[開啟] / [影像] / [僅搜尋片段]**。

### 3.1 版本定位：受影響的書、版本、卷

- **書**：`六壬大全`（又名《大六壬大全》），十二卷，不著撰人，
  卷首題「懷慶府推官郭載騋校」（四庫提要語，倉內 `rules.yaml` 引文 **[開啟]**）。
- **本次要對的版本**：**欽定四庫全書（文淵閣）本《六壬大全》**，
  子部 術數類 占卜之屬，十二卷。
- **冊／卷**：**第 0808 冊**；《總鈐》在 **卷一**，位置在「九返吟法」之後、「神煞」之前。
- **電子主文本不是此本**：主文本來自維基文庫 `六壬大全/1…12`（另一版本編次），
  這正是殘格的來源（§3.3）。

### 3.2 四庫本兩種獨立掃描（頁碼已定位）

#### (A) 景印文淵閣四庫全書 第 0808 冊 — **倉內本，亦即 Commons 同檔**

- **[開啟]** Wikisource Index 頁面 wikitext：
  `https://zh.wikisource.org/w/api.php?action=query&prop=revisions&rvslots=main&titles=Index:文淵閣四庫全書 0808冊.djvu`
  原文分頁清單（逐字照錄關鍵行）：

  ```
  |Volume=第0808冊　子部 術數類 相宅相墓之屬、占卜之屬
  ==六壬大全==
  不著撰人
  <pagelist from=476 to=853 476=471 />
  ```
  → **《六壬大全》= 該冊掃描影像第 476–853 頁**（378 頁）；
  Wikisource 標籤頁碼 471–848（標籤 = 掃描序 − 5）。

- **[影像]** 我實際下載並處理過的頁（Commons 縮圖，HTTP 200，284–517 KB／頁）：
  476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491,
  492, 493, 500, 505, 510, 515, 520, 525, 530, 535, 540
  取法：
  `https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/文淵閣四庫全書_0808冊.djvu/page480-1280px-文淵閣四庫全書_0808冊.djvu.jpg`

- **[開啟]** Commons API 檔案資訊：
  `pagecount=987`、原生 `1237×1864`、`size=98547126`。

- **版式實測（像素分析，非猜測）**：每掃描頁 = **2 個版塊上下堆疊**，兩版塊間有水平空白帶
  （p478 實測空白帶在 y=882–949）。每版塊 = **1 葉**（含右半 = a 面、左半 = b 面）。
  逐項驗證（皆為 OCR 實測，見 §3.5 的 OCR 限制說明）：

  | 掃描頁 | 版塊 | OCR 實際看到的內容 | 對應 |
  |---|---|---|---|
  | 476 | 全頁 | 四庫提要（「欽定四庫全書…六壬大全…提要」） | 提要 |
  | 478 下 | 下版塊 | 「甲課寅兮乙課辰丙戊課己不須論丁巳課未庚申土」「取課先從下賊呼…」「中上加臨是末居三傳既定天盤將」「二比用法…陽日用陽隂用隂」「三渉害法…孟深仲淺季當休」 | **卷一 葉1a＋1b** |
  | 479 上 | 上版塊 | 「四課無尅號為遥」「昴星窮」 | 卷一 葉2 |
  | 479 下 | 下版塊 | 「迤邐刑之作中末」「從兹玉厯職其真」「若也自刑為發用」「冲取末傳不論刑」「九返吟法」「返吟有尅亦為用…丑未同干丁巳辛」＋**「總倫」＝總鈐標目** | **卷一 葉3（總鈐標目在卷末 b 面）** |
  | 480 | 上＋下版塊 | 大量孤立單字格（表格） | **卷一 葉4、葉5 ＝ 總鈐表** |
  | 481 | 上＋下版塊 | 大量孤立單字格（表格） | **卷一 葉6、葉7 ＝ 總鈐表** |
  | 482 上（右半） | 右半 | 孤立單字格（表格尾） | **卷一 葉8a ＝ 總鈐表末** |
  | 482 上（左半） | 左半 | **「歲君　甲見甲之類年中天子之象統攝諸位神煞」「太嵗　子年見子之類…七月以後見来年太嵗来年事」** | **卷一 葉8b ＝ 神煞起** |
  | 482 下 | 下版塊 | 「太歲神煞…病符後一不離宗…後四白虎是㐫神」＋十二支表 | 卷一 葉9 |
  | 483 | 上＋下版塊 | 「嵗後五位如子年見未」「嵗合即甲年見已」「金神」「病符嵗後一辰」「嵗虎嵗後四辰」「福星　子丑子子未未丑丑巳巳」 | 卷一 葉10、葉11 |

- **★ 結論（A）：《總鈐》表 = 文淵閣四庫全書《六壬大全》卷一 葉4a–8a，
  在 0808 冊 DJVU 中為掃描影像第 480–482 頁（Wikisource 標籤頁碼 475–477）。**

#### (B) CADAL／浙江大學圖書館掃描（Internet Archive 06054168.cn）— 另一套掃描、解析度更高

- **[開啟]** ctext 圖書館著錄頁 `https://ctext.org/library.pl?if=gb&res=6838`：
  「《欽定四庫全書》本。本書12卷，拆分成10冊。影印古籍　欽定四庫全書·子部七·術數類
  　原書來源：浙江大學圖書館。掃描者：CADAL。」
  列出「六壬大全卷一 → `library.pl?if=gb&file=75674&page=1`」與 IA 下載連結 `06054168.cn`。
- **[開啟]** `https://archive.org/metadata/06054168.cn`：
  `title=六壬大全·卷一`，`contributor=浙江大学图书馆`，含
  `06054168.cn.pdf`(3,458,657)、`_djvu.txt`、`_djvu.xml`、`_hocr.html`、
  `_page_numbers.json`、`_scandata.xml`。
- **[影像]** 下載 `06054168.cn.pdf`：`pdfinfo` → **Pages: 112**。
  原生嵌入影像實測 **2346×3179**（JPEG2000，600 ppi 級），**明顯優於 0808 冊的 1237×1864**。
- **[影像]** 以 `pdftoppm` 渲染 p1–p20、以 `pdfimages` 抽出原生 p10–p30 後 OCR：

  | CADAL PDF 頁 | OCR 實際看內容 | 對應 |
  |---:|---|---|
  | 10 | （殘，幾無字） | 提要末 |
  | 11 | 「甲課寅兮乙課辰丙戊課己不須論丁巳課未庚申土」 | 卷一 葉1a |
  | 12 | 「中工如忠是末居」「別責法」 | 葉1b |
  | 13 | 「四課無尅號為遥」 | 葉2a |
  | 14 | 「柔日支前三合取」「天上作初傳」 | 葉2b |
  | 15 | 「伏吟」「九返吟法」 | 葉3a |
  | 16 | 表格字樣（「甲…未…子…午…甲日」） | 葉3b（總鈐標目） |
  | 17–25 | 孤立單字格 | **葉4a–8a ＝ 總鈐表** |
  | 26 | **「歲君甲見甲…」「入占長部守之事占官有而盡之喜不宜受」** | **葉8b ＝ 神煞起** |
  | 27 | 「為符徐不離宗復二去慘餅兩客禾回白到」＝「病符後一不離宗…後四白虎是」 | 葉9（太嵗神煞） |

- **★ 結論（B）：同一部四庫本的 CADAL 掃描，《總鈐》= 第 1 冊 PDF 第 16–25 頁
  （表體 17–25）。** 這與 (A) 由葉碼獨立互證：兩套掃描分頁不同（0808 冊一頁兩葉，
  CADAL 一頁一半葉），但都指向 **卷一 葉4a–8a**。另：卷一 CADAL 為 p11–p112
  ＝ 102 頁 ＝ 102 半葉 ＝ **51 葉**，與 Kanripo 標記的卷一 51 葉完全吻合。

> 註：(A)、(B) 是**同一個版本的兩套掃描**（皆欽定四庫全書本），
> **不是文本層面的獨立見證**，不可互相當作校勘第二本。

### 3.3 殘格來源本：維基文庫 `六壬大全/1`（＝倉內電子主文本的實際出處）

- **[開啟]** `https://zh.wikisource.org/w/api.php?...titles=六壬大全/1`
  → rev **854569**，2017-04-16T03:58:04Z，23,920 bytes。
- 該頁 offset 8610 起即為總鈐，逐字照錄開頭：

  ```
  总钤

  甲　　巳	甲　　午	甲　　未	甲　　申

  申

  亥

  寅	午　戌　　申　子

  寅　　　辰
  ```

  → 與倉內 `sources/fulltext/.../fulltext.md` L1040 起的內容**逐字相同**，
  確認 **666 殘格的電子來源就是這個被壓平的版本**，而非四庫本本身。
- 該頁**自稱四庫本**，但倉內 `conflict-notes.md` C-001 已記錄其卷次與文淵閣轉寫不符；
  本輪不改此結論。

### 3.4 ★ 真正的結構化見證：識典古籍 SK1599「總鈐」章（**已開啟，且可機讀**）

- **[開啟]** `https://www.shidianguji.com/zh/book/SK1599/chapter/1m1g2eil4og7e`
  HTTP 200，732,875 bytes，`<title>總鈐-六壬大全全文原文及譯文-識典古籍</title>`。
- 頁面內嵌 SSR 資料含該書卷一完整章目與 **該章 11 個段落**，逐字照錄關鍵欄位：

  ```json
  {"chapterId":"1m1g2eil4og7e","chapterName":[{"content":"總鈐"}],
   "startPageNum":13,"endPageNumWithoutSubchapter":23,"paragraphCount":11,
   "hasMainContent":true,"chapterOrder":15}
  {"chapterId":"1m1g2eil4osui","chapterName":[{"content":"神煞"}],"startPageNum":24, ...}
  ```
  → 總鈐章 **存在且 `hasMainContent: true`**，跨網站頁碼 **13–23（11 頁）**，
  下一章「神煞」自第 24 頁起 —— 與四庫本的「總鈐在神煞之前、且是長表」完全吻合。

- 更關鍵：其段落內容是 **帶列結構的表資料**，不是被壓平的文字流。
  我解析出的結構（逐字照錄第一列樣本）：

  ```json
  {"lineType":12,"table":{"head":"","rows":[
    {"cells":[{"paraList":[{"lines":[{"lineNum":95,"lineType":1,"content":"申甲"}]}],
               "cellType":2,"rows":1,"cols":1}]}, ...]}}
  ```

  11 段 = 表目 1 段（`content="總鈐"`，dataSize 146）＋ **10 個表**（dataSize 4297–4729），
  每個表 25 列，**一表對一干**（甲/乙/丙/丁/戊/己/庚/辛/壬/癸），
  列樣本如 `申甲`、`酉。甲`、`六甲日`、`五甲子巳、戌、辰。寅未子`、`四乙寅未子、酉未。`。

- **與倉內殘格的量化比對（我實測）**：

  | 量 | 值 |
  |---|---:|
  | 倉內 L1040–L2468 干支字元數 | 1975（unique 22） |
  | 識典 10 表抽出的干支字元數 | 1914（unique 23） |
  | 比值 | **0.97** |

  → 同一張表，**字元盤幾乎一致**；而識典版把倉內被拆散的疑字復原成完整串：
  倉內 `辰　甲五` / `申 辰 甲 四` / 獨立的 `六`、`甲`、`日`
  ↔ 識典 `五甲子巳、戌、辰。寅未子` / `四甲戌申、午、` / `六甲日`。

- **這是本輪找到的最可行還原路徑**：`references/source-editions.json` 早已把
  SK1599 登記為 `reference-text` 補本，並在 `missingChapters` 記下
  `1m1g2eil4og7e expected=11 actual=0`。**該章從未被下載**，
  因此註解 notes 中「识典SK1599补本无总钤章节」是**下載不全的誤推**，不是站上沒有。

### 3.5 兩個「空白見證」：同版電子轉寫都跳過了這張表

#### (a) Kanripo KR3g0031（文淵閣轉寫）

- **[開啟]** `https://raw.githubusercontent.com/kanripo/KR3g0031/master/{Readme.org,KR3g0031_000..012.txt}`
  （12 卷全文＋提要）。檔頭照錄：`#+PROPERTY: BASEEDITION WYG`、`#+PROPERTY: JUAN 卷一`。
- 修訂已釘死：`KR3g0031_001.txt` 最後變更 commit
  **`320cbc13a9048aa0f028d996ab32f8bf7b362ef7`**（2016-02-05），
  與倉內 manifest 宣稱釘的 commit **完全相同**。
- 提要（`KR3g0031_000.txt` L40）**[開啟]**：「法是書總集諸書遺文首載入手法**總鈐**及…」
  —— 四庫館臣自己把「總鈐」列為本書開篇要件。
- 卷一（`KR3g0031_001.txt`）逐行標記 **[開啟]**，總鈐段落**逐字照錄**：

  ```
  　　總鈐¶
  <pb:KR3g0031_WYG_001-4a>¶
  ¶
  <pb:KR3g0031_WYG_001-5a>¶
  ¶
  <pb:KR3g0031_WYG_001-6a>¶
  ¶
  <pb:KR3g0031_WYG_001-7a>¶
  ¶
  <pb:KR3g0031_WYG_001-8a>¶
  　¶   （×8）
  <pb:KR3g0031_WYG_001-8b>¶
  　　神煞¶
  ```

  → **轉寫者沒有抄這張表**（表體全空）。但頁葉標記給了關鍵定位：
  **總鈐 = 卷一 葉4a–8a（標目在 3b 末），神煞自 8b 起。**
  同檔卷一葉碼上限 51，與 (B) CADAL 卷一 102 半葉完全吻合。

#### (b) 維基文庫 `六壬大全 (四庫全書本)/卷01`

- **[開啟]** rev **763659**，2016-10-24T18:36:15Z，24,184 bytes。
- 總鈐段落**逐字照錄**（`<子部,術數類,占卜之屬,六壬大全,卷一>` 是該頁的版心行）：

  ```
  　　{{SK anchor|總鈐}}

  <子部,術數類,占卜之屬,六壬大全,卷一>   （×4）

  <子部,術數類,占卜之屬,六壬大全,卷一>   （×4）

  　　{{SK anchor|神煞}}
  ```

  → 同樣**空白**，但留下 **8 個版心行 = 8 個半葉純表頁**，
  是「此處確為整頁表格」的第二個獨立電子見證。

### 3.6 清刊本：已定位（國圖藏，清光緒十二年掃葉山房刻本）

- **[開啟]** 中國國家圖書館「中華古籍資源庫」著錄頁
  `http://read.nlc.cn/allSearch/searchDetail?searchType=1002&showType=1&indexName=data_892&fid=GBZX0301010256`
  逐字照錄著錄項：

  ```
  大六壬大全 十三卷
  责任者：不著撰人
  版本项：清光緒十二年（1886）掃葉山房刻本  13冊；1函
  现有藏本附注：天津圖書館藏
  ```

- **[開啟]** Commons 上有該 13 冊的公有領域 PDF（上傳者標示來源 Tianjin Library）：
  `File:NLC892-GBZX0301010256-249407 大六壬大全 十三卷 第1冊.pdf`
  （19,841,112 bytes，49 頁，`LicenseShortName: Public domain`；
  13 冊檔案齊全，編號 …-249407 / 249467 / 249468 / 249469 / 249470 / 249471 /
  249526 / 249527 / 249528 / 249529 / 249530 / 249531 / 249602）。
  目錄可查：
  `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=大六壬大全 NLC892&srnamespace=6`
- **[影像]** 我下載第 1 冊 PDF（HTTP 200），`pdftoppm -r 150` 渲染全 49 頁並逐頁 OCR。
  實測：

  | 第1冊 PDF 頁 | OCR 實際看內容 | 判斷 |
  |---:|---|---|
  | 3–10 | 序（「六壬…三式…」「大六壬大全…郭和青先生訂／入手」） | 序＋目／凡例 |
  | 11 | 「十干寄宫」 | 卷一 起例 |
  | 12 | 「先辰而後」「別責法」「四課不全三課備」 | 卷一 九宗 |
  | 13–17 | 孤立單字格；p16 出現「**總**」字樣 | **總鈐表區（推測）** |
  | 18 | **「六頻年中天子之伯生謂話位油徐入占長部守之事占官有而盡之喜不宜受」** = 「歲君…統攝諸位神煞／入占尊長部官之事占官有面君之喜不宜受剋」 | **神煞起** |
  | 19 | 「歲後五…子年見未」「歲合印甲年見已」 | 歲神煞 |

  → 清刻本**同樣有《總鈐》表**，且位置同樣在「神煞」之前；
  依 p18 = 神煞起回推，總鈐表體落在 **第 1 冊 PDF 第 14–17 頁**。

- **★ 判定：PARTIAL。** 版本已確定（清光緒十二年掃葉山房刻本、十三卷、
  國圖藏／天津圖書館藏本、13 冊 1 函），頁區已收窄到第 1 冊 p14–17，
  但**我未能逐頁確認總鈐標目行與表格起訖**（該 PDF 原生解析度僅 639×1114，
  OCR 在表格頁全數失效），因此**不寫死頁碼**。

### 3.7 只搜到、未開啟、不採用的來源（誠實列出）

- `https://www.zhycw.com/art/n867c10p15.aspx` — **[僅搜尋片段]**
- `https://m.guoxuedashi.com/guji/214991i/` — **[僅搜尋片段]**
- `https://www.360doc.cn/article/5006336_79391370.html` — **[僅搜尋片段]**
- `https://www.bilibili.com/video/BV1c7mEB6Edg/` — **[僅搜尋片段]**（現代分享，非底本）
- `https://vstudy.ruc.edu.cn/...`、`https://www.dl-library.net.cn/...` — **[僅搜尋片段]**
- `https://sonchu.vn/thu-vien/06054170cn` — **[僅搜尋片段]**（轉載同一 CADAL 掃描）
- 未使用任何付費、登入或需繞過限制的來源；未下載任何需付費版本。

### 3.8 OCR 能力上限（實測，必須記錄）

四庫刻本表格為孤立單字格；本 session 只有 `tesseract`（`chi_tra_vert`）。
對 0808 冊 p480（自適應二值化＋3× 放大，`--psm 6`）的**實際輸出**：

```
名 評 M 衝 雯 當 由 友 各 w 0 上 CC 人 _ 漲 喀 條 必 衝 吾 字 划 于 _ 必 六 二 人 四條 站 生生 MW LU M 族 六 光 + 必 *。
```

對 CADAL 高清頁 im-007（`--psm 6/11/12`）同樣為亂碼。

→ **表格單格內容無法由本 session 的機器 OCR 可靠還原。**
凡是「已把某格讀出來」的結論，本報告一律不給。
要真正還原，需要：(i) 具視覺能力的模型直接讀已定位的頁；或
(ii) 人工過錄；或 (iii) 依專案規則正式導入識典 SK1599 的結構化表資料。

---

## 4. 逐項判定

判定定義（本報告專用）：

- **LOCATED**：底本／卷／葉／頁全部確定，**且所需內容已在該頁被讀出並可引**。
- **PARTIAL**：底本與頁碼確定，但**所需單格內容未經讀出／校驗**。
- **NOT LOCATED**：底本或頁碼未能確定。

| 集合 | 條數 | 位置（底本/卷/葉/頁） | 單格取值校驗 | 判定 |
|---|---:|---|---|---|
| 大六壬《總鈐》殘格 666 條 | **666** | **LOCATED** | **NOT LOCATED** | **PARTIAL（666／666）** |
| 其中落 21 分組內 | 664 | LOCATED（同上） | NOT LOCATED | PARTIAL |
| 其中區間外 2 條（`L1010`、`L1038`） | 2 | LOCATED（同上） | NOT LOCATED | PARTIAL |

**合計：LOCATED 0 ／ PARTIAL 666 ／ NOT LOCATED 0。**

> 「LOCATED 0」不是壞消息：前一輪的瓶頸是**找不到正確版本的頁**，
> 這一輪把頁找到了（卷一 葉4a–8a；0808 冊影像 480–482；CADAL 第1冊 16–25；
> 清刻本第1冊約 14–17）。但依本任務的誠實規則，
> **「找到頁」不等於「讀出格」**，故不計為 LOCATED。

### 4.1 可直接引用的最強引用（全部為我實際開啟／實際處理）

1. **底本（倉內，sha256 已驗）**
   `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu`
   = 景印文淵閣四庫全書 第0808冊；《六壬大全》占該冊掃描影像第 476–853 頁。
   依 Wikisource Index 分頁清單：`<pagelist from=476 to=853 476=471 />`。
2. **總鈐頁（景印本）**：**掃描影像第 480–482 頁**（標籤頁碼 475–477），
   對應 **卷一 葉4a–8a**；標目在葉3b 末（影像第 479 頁下版塊，OCR 見「總倫」）；
   神煞起於葉8b（影像第 482 頁上版塊左半，OCR 見「歲君　甲見甲之類…」「太嵗　子年見子之類…」）。
   影像直鏈（我實抓 HTTP 200）：
   `https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/文淵閣四庫全書_0808冊.djvu/page480-1280px-文淵閣四庫全書_0808冊.djvu.jpg`
3. **葉碼見證（Kanripo，commit 已釘）**
   `https://raw.githubusercontent.com/kanripo/KR3g0031/master/KR3g0031_001.txt`
   @ `320cbc13a9048aa0f028d996ab32f8bf7b362ef7`；`　　總鈐` 之後為 `<pb:KR3g0031_WYG_001-4a>`
   … `<pb:KR3g0031_WYG_001-8a>` 空行，`<pb:KR3g0031_WYG_001-8b>` 接 `　　神煞`。
4. **空白見證（維基文庫四庫本）**
   `https://zh.wikisource.org/wiki/六壬大全_(四庫全書本)/卷01` @ rev 763659；
   總鈐後為 8 個 `<子部,術數類,占卜之屬,六壬大全,卷一>` 版心行，再入 `{{SK anchor|神煞}}`。
5. **殘格來源本（維基文庫另一版本）**
   `https://zh.wikisource.org/wiki/六壬大全/1` @ rev 854569（2017-04-16），
   offset 8610 起「总钤／甲　　巳　甲　　午…」。
6. **第二套四庫掃描（CADAL／浙大）**
   `https://archive.org/download/06054168.cn/06054168.cn.pdf`（112 頁，原生 2346×3179）；
   總鈐 = 第 1 冊第 **16–25** 頁。
7. **結構化表資料（最可行還原路徑）**
   `https://www.shidianguji.com/zh/book/SK1599/chapter/1m1g2eil4og7e`
   —— 總鈐章 11 段＝1 段標目＋**10 個帶列結構的表**（各 25 列），
   網站頁碼 13–23，下一章神煞 p24。
8. **清刊本（獨立版本）**
   國圖著錄 `fid=GBZX0301010256`：**清光緒十二年（1886）掃葉山房刻本，十三卷，13 冊 1 函，天津圖書館藏**；
   Commons 公有領域 PDF：`File:NLC892-GBZX0301010256-249407 大六壬大全 十三卷 第1冊.pdf`
   （19,841,112 bytes／49 頁）；總鈐表區在第 1 冊 PDF p14–17（**待人眼確認**）。

---

## 5. 可升級 vs. 必須留 draft

### 5.1 可以升級的

**本輪：0 條。** 我沒有把任何一條 666 讀出來並校驗，因此**不建議把任何一條**
由 `draft` 升為 `source-reviewed`。

### 5.2 必須維持 `draft` 的

**全部 666 條**，直到下列任一路徑完成並留有可核記錄：

- **路徑 A（首選，最快）**：把 `識典 SK1599 / chapter/1m1g2eil4og7e` 的
  10 個結構化表正式導入，依專案規則補 `sources/normalized/shidianguji/SK1599/`
  的 `text.md` / `paragraphs.json`，並把 `references/source-editions.json`
  的 `missingChapters` 中 `1m1g2eil4og7e expected=11 actual=0` 更正為已取；
  然後按段比對，逐條寫入平行段 ID 與判讀。**此路徑不需新影印，且已有字元盤 0.97 的實證。**
- **路徑 B**：由具視覺能力的模型或人工，直接讀已定位的
  **0808 冊影像 480–482**（或 CADAL 第 1 冊 p16–25），逐格過錄後再升級。
- **路徑 C**：以清光緒十二年掃葉山房刻本（國圖／天津圖書館藏本，Commons PDF）
  作第二版本，先確認其總鈐表起訖頁，再作版本互校。

### 5.3 明確不得做的事

- 不得因為本報告「找到了頁碼」就把 666 條標成 `source-reviewed`。
  `docs/SOURCE_EDITIONS.md` 已定明：`source-reviewed` 只表示
  「已對照可核的電子文本或多版本平行本」，**且補充來源不能作為投票證據**。
- 不得把 §3.4 的識典字串直接當「原典引文」寫進 `terms`（`terms` 是定讀索引，不是原文）。
- 不得宣稱 0808 冊與 CADAL 是兩本（同一版本的兩套掃描，非獨立文本見證）。

---

## 6. 未解阻塞與需據實登記的缺口

1. **單格未讀出（阻塞全部 666 條）**：定位完成，取值未完成。
   阻塞原因具體且可複現：本 session 無影像輸入能力、只有 `tesseract`，
   而四庫刻本表格為孤立單字格，OCR 實測輸出為亂碼（§3.8）。
2. **manifest 路徑失準（新發現的真缺口，影響後續所有輪次）**：
   `references/books/san-shi/daliuren-daquan/source-manifest.yaml` 的 `local_files`
   中至少 14 條路徑實際不存在（Kanripo 13 檔＋`Siku-Wenyuange-0808.djvu`＋
   `references/fulltext/...`＋`wikisource_raw.txt`）。
   同一 manifest 卻宣稱「文淵閣影印已取得」「影印已經本地化」。
   這正是「無影印」誤判的根因。**建議另開一條修正任務**（本任務寫入範圍不含該檔）。
3. **`GOAL_CHECKPOINT.md` 與註解 notes 的錯誤斷言需更正**：
   「仓内无《大六壬大全》影印」（GOAL_CHECKPOINT 第 66 行）與
   666 條 notes 中的「sources/facsimile 亦无大六壬大全影印」皆與 §2.1 實測不符。
4. **識典 SK1599 總鈐章未取**（`expected=11 actual=0`）：這是唯一「只需下載即可關閉」的缺口。
5. **全機磁碟內容掃描未完成**：全 home 目錄 `find` 逾時被 kill（§2.2 末列）。
   已做的 name-based 有界檢索未發現其他六壬大全底本，
   但**不能據此宣稱全機絕對沒有**。此為方法學限制，非已解結論。
6. **清刊本總鈐頁碼未定死**：清光緒十二年掃葉山房刻本第 1 冊僅收窄到 p14–17，
   標目行與表體起訖未確認（掃描原生僅 639×1114）。
7. **兩條區間外條目**：`daliuren-daquan:L1010-L1010`、`daliuren-daquan:L1038-L1038`
   含「残格／总钤」但落在 scopeNote 21 分組之外，登記缺口時勿漏計。

---

## 7. 一頁速查

| 問題 | 答案 |
|---|---|
| 需要對哪本書、哪個版本、哪一卷 | 《六壬大全》十二卷；**欽定四庫全書（文淵閣）本**；**卷一** |
| 影印在哪 | 倉內 `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu`（sha256 已驗） |
| 該冊哪一頁 | 掃描影像 **480–482**（Wikisource 標籤頁碼 475–477）＝ **卷一 葉4a–8a** |
| 第二套四庫掃描 | CADAL／浙大 06054168.cn 第1冊 PDF **16–25** 頁（原生 2346×3179） |
| 獨立清刊本 | **清光緒十二年（1886）掃葉山房刻本，十三卷，13冊1函，天津圖書館藏**；Commons 公有領域 PDF；總鈐約第 1 冊 p14–17 |
| 為何 Kanripo／維基四庫本查不到表 | 兩者都把這張純表跳過（Kanripo 留 4a–8a 空行；維基留 8 個版心行）→ 表確實存在，只是沒被轉寫 |
| 最可行還原路徑 | 識典 SK1599 `chapter/1m1g2eil4og7e` 的 **10 個結構化表**（已登記為 missing，11 段全未取） |
| 666 條判定 | **PARTIAL 666／LOCATED 0／NOT LOCATED 0** |
| 可升級條數 | **0** |
| 受影響 rule ID | **無**（executable 22 條規則皆不含總鈐；作用域是段落） |
