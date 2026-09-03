# 原始资料层说明

这个目录放的是新算法开发要用的上游资料，包括从旧工程找回的规范化全文，以及按来源重新下载的影印原件。它们不是旧算法的蒸馏结果。

## 已恢复

- `fulltext/`：54 个非空 `fulltext.md`，总计 13,978,151 bytes。
- `fulltext/` 内另有 2 份补充 Markdown，分别属于六壬指引与奇门遁甲统宗材料。
- `excerpts/qimen-faqiao-chaibu-v1.md`：《奇门法窍》现存核验摘录。它不是全书。
- `facsimile/`：75 个 PDF / DjVu 影印文件，共 1,170,138,206 bytes，覆盖 34 / 55 套；每批都有来源和书目映射清单。
- 超过 GitHub 普通仓库单文件限制的 4 套影印原件，共 545,553,071 bytes，放在 [GitHub Release](https://github.com/linyuhanggg/fateradar-classics/releases/tag/facsimiles-oversize-2026-09-04)。

规范化全文来自旧工程最后一份与 catalog 对齐的 stage 快照。复制到本仓库后保持内容不变，并已逐文件比较源目录与目标目录。影印件则是从各 manifest 登记的公开来源重新下载，并核对文件长度和格式。

## 没有找回的旧工程原件

下列历史原件目前没有在本机、iCloud、旧系统盘和已挂载磁盘的现有检索中找到：

- PDF / DJVU 影印本；
- JPG / PNG / TIFF 等逐页扫描图；
- ZIP / 7z / RAR / TAR 等原始压缩包；
- `sources/raw/` 网页快照；
- 逐页 OCR、人工 review 和原始 manifest 工程。

因此，本仓库不能冒充“旧工程原封不动的扫描全集”。现在已经做的是：能从公开来源确认的影印本重新下载并公开；没找到或无法确认同书的项目在各 manifest 里直接标明，不拿近名书、现代整理本或误匹配文件凑数。

资料层按下面四层继续整理：

```text
raw/          原始网页或下载文件
facsimile/    PDF、DJVU、逐页扫描图
normalized/   统一编码但不改写正文的文本
distilled/    章节、术语、规则、引用和核验材料
```

当前影印件分在：

```text
facsimile/wikimedia-known/   直接确认的 Commons 单本
facsimile/other/             CText 等旧锚点对应的替代影印本
facsimile/wikisource/        维基文库 / Commons 底本
facsimile/missing-recovery/  未找到、超限或误匹配的恢复记录
```

《大六壬秘本》的 154,825,545-byte 扫描已经确认来源，但来源站首次请求返回限流，暂未上传；原文件直链保留在 `facsimile/other/MANIFEST.md`。

以 catalog 的 55 套为全集，当前互斥状态是：普通 Git 影印件 34 套、Release 影印件 4 套、待传 1 套、未找到可确认影印本 14 套、仅摘录或 section pack 2 套，合计正好 55 套。

## 开发使用边界

新 FateRadar 可以把这里的全文用于搜索、对照和重新抽取候选规则，但不能直接把旧 `rules.md`、`procedures.md` 或旧 Runtime 结果当作新算法。每条进入新排盘引擎的规则，都需要重新定位原文、确定版本与流派，并用固定课例验证。

这些文本来自多种网页、OCR 和整理版本。文件可见不代表内容已经完成版本学核对；引用或再利用时请同时保留书名、来源地址和版本说明。
