# 主文本、补充对照与影印恢复稿

主段落库53,640个既有ID不改。`references/source-editions.json`登记独立补充来源，`tools/source_paragraphs.py`在消费时合并，实际摘录路径随段落传递，不能用主书路径替代补充文本路径。

现有补充：六壬指南注解镜像卷三四、奇门演义卷四至九对照层。两者保留各自题名和来源说明，未自动充作canonical原典，也未自动进入运行规则。

命理约言NLC恢复稿采用`mingli-yueyan:nlc-recovery:P021:L002-L009`一类页内ID。P是PDF页，L是该页标题后相对行范围；全局start_line/end_line仍对应当前文件，以固定提交生成GitHub引用。前页拆列校正不会改下一页的ID，当前页校正后需重核该页的段落注解。未冻结OCR稿不是可随意引用的原典。

OCR片段保持`source_status=ocr-draft`。语义注解可存draft，但不能仅把review写成source-reviewed就升级；新校验器拒绝该组合，原书案例导出同样拒绝未校OCR。逐页校核记录由恢复任务继续补；仅status=source-reviewed且无未决项的具体页可转为page-reviewed，partial页可另列页内reviewedRanges；只有完整落在已核范围的正文段为passage-reviewed，范围外仍是草稿。spot-checked与未列页保持草稿。不会根据非空页数或单页抽检升级整稿。

产品书房显示补充来源名称，OCR另显“影印识别草稿·待校对”、PDF页码与使用范围。搜索命中不是规则满足；OCR草稿不会通过新规则来源导出进入已校依据。

验证：`python3 tools/test-source-editions.py`覆盖不同来源ID隔离、前页编辑不移动后页ID、OCR草稿不得升级；知识导出和前端查询测试覆盖补充来源路径及页码保留。

正式知识导出从当前Git HEAD的已提交源快照读取，而非边写边改的工作区。OCR校稿改变行数时，未提交变化不会混进标着旧revision的产物；源版本、文字和行号锚点因此一致。草稿状态仍可在已提交版本中保存，不会因此升级。

恢复正文注解单独存`references/annotations/{system}/{slug}--{edition}.json`，bookSlug仍是原资料包，段落ID包含edition与页标识。旧主注解文件不追加恢复ID，主段落统计与补充来源统计分列。

## 注解字段语义（下游消费须知）

- `review`：`draft` 或 `source-reviewed`。`source-reviewed` 只表示**已对照可核的电子文本或多版本平行本**，
  不表示逐段影印校勘、不表示人工 verified。`verified` 在本仓始终为 `false`。
- `notes`：append-only 的判读与依据记录。升级时写入所引平行段 ID；被复核推翻时**不删旧注**，
  另追加「【复核回退】」说明为什么回退。因此 notes 记录了完整的判读历史，也包含已被推翻的判断。
- `vernacular`：白话解释，不是原文；升级时在末尾追加「本轮已核，下列为定读」，不改动原文引文。
- `terms`：**定读术语索引，不是逐字原文**。当某个神煞/术语名在源文里是讹形或异体时，
  `terms` 会写还原后的定读名（如源行 `丑 天喜 驿心 信煞` 的「驿心」在 terms 里作「圣心」），
  并有本书起例或平行本依据写进 `notes`。下游导出、检索与 AI 上下文**不得**把 `terms` 当作原文引用；
  需要引用原文时请用 `sources/` 下的全文与注解所记的段落/行号。
