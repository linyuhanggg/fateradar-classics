# FateRadar Classics

FateRadar 古籍研究资料仓库。

这里保存的是此前整理出的 **55 套结构化古籍包**。它们用于重新研究排盘后的检索、引用、规则核验和 AI 追问，不包含 FateRadar 产品代码，也不包含已经放弃的旧排盘算法。

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
```

合计 55 套。完整名单见 [`references/catalog/D2_READY_REFERENCE_PACKS.md`](references/catalog/D2_READY_REFERENCE_PACKS.md)。

## 为什么不放完整古籍全文

古籍原典可能已经进入公版，但现代网页转录、OCR、标点、校勘、注释和排版不一定可以再次公开分发。原项目没有完成 55 份全文的逐本转载许可核验，因此本仓库只发布结构化研究包、短引和来源元数据，不发布 `fulltext` 全文。

详细边界见 [`references/catalog/SOURCE_PROVENANCE_POLICY.md`](references/catalog/SOURCE_PROVENANCE_POLICY.md) 和 [`NOTICE.md`](NOTICE.md)。

## FateRadar 后续使用方式

建议把本仓库当作“可追溯资料库”，不要直接当成排盘器：

1. 排盘由独立、轻量、可测试的确定性引擎完成。
2. 用户提出问题后，再按命盘事实和问题主题检索相关古籍包。
3. 只把少量命中的原文、出处、成立条件和冲突材料交给 AI。
4. AI 负责解释，不负责发明命盘事实，也不能把未核验规则说成定论。

## 快照来源

本仓库首次公开快照取自原 `mingli_web` 仓库 `main` 分支已经提交的古籍资料。没有复制该项目当前未提交内容，也没有复制其算法、后端、前端、账号、配置或运行数据。

## 许可

本仓库当前不提供覆盖全部内容的统一开源许可证。不同古籍、转录来源和派生整理可能适用不同权利条件。公开可见不等于允许任意复制、再授权或商业训练；使用前请逐项查看来源和 `NOTICE.md`。
