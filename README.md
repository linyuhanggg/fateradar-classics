# FateRadar Classics

FateRadar 古籍研究资料仓库。

这里保存的是此前整理出的 **55 套结构化古籍包**，以及目前仍能找回的 **54 本规范化全文、2 份补充文本和 1 份《奇门法窍》摘录**。它们用于重新研究排盘规则、检索、引用、核验和 AI 追问，不包含 FateRadar 产品代码或可执行的旧排盘引擎。

> 重要：部分 `rules.md`、`procedures.md` 和测试材料是在旧项目里派生出来的候选研究记录，其中会出现旧 Runtime、Provider 或 V5.1 术语。保留它们是为了追溯以前做过什么，**不代表 FateRadar 新算法会继承这些结论**。新算法必须回到来源、原文和独立测试重新确认。

## 这是什么

每套古籍包按用途拆成若干文件：

- `index.md`：书目、版本、来源和使用边界。
- `chapter-map.md` / `section-map.md`：章节与原文位置地图。
- `terms.md`：术语整理。
- `rules.md`：从古籍中抽取的候选规则。
- `procedures.md`：可操作步骤与使用条件。
- `quote-index.md`：短引、出处和定位。
- `validation.md`：覆盖情况、核验状态和已知问题。

这些文件是研究资料，不等于已经验证正确的命理算法。`ready` 只表示文件结构和引用检查曾经通过，不表示历史真伪、现实准确率或版权许可已经全部解决。

## 目录

```text
references/books/
  bazi/             八字，7 套
  divination/       六爻、梅花等，7 套
  fengshui/         风水，16 套
  luming-nayin/     禄命纳音，5 套
  physiognomy/      相法，4 套
  san-shi/          奇门、六壬、太乙，6 套
  selection/        择日，4 套
  xingming/         星命、七政相关，3 套
  ziwei/            紫微，3 套
references/catalog/ 55 套书目、来源、版本风险和发布边界
sources/fulltext/   54 本规范化 Markdown 全文及 2 份补充文本
sources/excerpts/   《奇门法窍》现存摘录
docs/               FateRadar 新排盘引擎调研文档
```

合计 55 套。完整名单见 [`references/catalog/D2_READY_REFERENCE_PACKS.md`](references/catalog/D2_READY_REFERENCE_PACKS.md)。

## 当前完成度

- 资料包结构：55 / 55 已建档，分为 9 类。
- 来源状态：17 / 55 仍标记为 `partial`，表示来源或覆盖并不完整。
- 旧项目曾抽取 1,328 条候选规则；其中只有 192 条曾完成“运行启用 + 古籍证据绑定”，且这些状态仍须在 FateRadar 新架构里重新复核。
- 规范化全文：54 / 55 已上传；《奇门法窍》目前只有摘录，没有找到完整全文。
- 补充材料：另有 2 份 Markdown 补充文本，已随全文上传。
- 原始扫描：当前没有找到以前保存的 PDF、DJVU、逐页图片、压缩包或 OCR 页面工程；仓库中登记的来源地址仍在，后续需要逐本重新恢复。
- 另有 4 个未纳入包：两项底本不稳，两项只有扫描线索但 OCR / 校勘未完成。

所以这里的 `D2 ready` 只表示结构和证据锚点检查通过，不等于“全文齐全”，更不等于“算法已经正确”。

## 原文与扫描件的状态

`sources/fulltext/` 保存的是当时用于蒸馏的规范化 Markdown 文本。它们可能混合网页录入、OCR、标点、校勘或现代整理内容，并不等于古籍原版扫描，也不保证逐字无误。

历史记录说明当时曾存在 raw 文本、PDF、逐页 OCR 和扫描材料，但原 Qoder 工程目录目前已经找不到。本机、iCloud、旧系统盘和已挂载磁盘的现有检索也没有找回相应的 PDF 或图片，因此当前仓库不能声称已经包含扫描原件。

详细文件口径见 [`sources/README.md`](sources/README.md)，来源地址见 [`references/catalog/D2_READY_REFERENCE_PACKS.yaml`](references/catalog/D2_READY_REFERENCE_PACKS.yaml)。

详细边界见 [`references/catalog/SOURCE_PROVENANCE_POLICY.md`](references/catalog/SOURCE_PROVENANCE_POLICY.md) 和 [`NOTICE.md`](NOTICE.md)。

## FateRadar 后续使用方式

开源排盘底座的完整选型、逐术结论和落地阶段见 [`docs/OPEN_SOURCE_CHART_ENGINE_RESEARCH.md`](docs/OPEN_SOURCE_CHART_ENGINE_RESEARCH.md)。

建议把本仓库当作“可追溯资料库”，不要直接当成排盘器：

1. 排盘由独立、轻量、可测试的确定性引擎完成。
2. 用户提出问题后，再按命盘事实和问题主题检索相关古籍包。
3. 只把少量命中的原文、出处、成立条件和冲突材料交给 AI。
4. AI 负责解释，不负责发明命盘事实，也不能把未核验规则说成定论。

## 快照来源

本仓库首次公开快照取自原 `mingli_web` 仓库 `main` 分支已经提交的古籍资料。没有复制该项目当前未提交内容，也没有复制其算法、后端、前端、账号、配置或运行数据。

## 许可

本仓库当前不提供覆盖全部内容的统一开源许可证。不同古籍、转录来源和派生整理可能适用不同权利条件。公开可见不等于允许任意复制、再授权或商业训练；使用前请逐项查看来源和 `NOTICE.md`。
