# 《命海全编》识典 HY1442 电子语义扩写账本

独占文件：`references/annotations/xingming/minghai-quanbian--shidian-HY1442.json`。  
原文只读：`sources/normalized/shidianguji/HY1442/text.md`（SHA256 `e33a35825af5591d554c067ea901b72d512ae19cea6314ba503cdda67e65c7d8`）。  
段落账本：`docs/book-reviews/cursor-expand-minghai-quanbian-remaining.json`。

本仓未见独立 `AGENTS.md` / `CLAUDE.md`；已按 `docs/FATERADAR_FULL_LIBRARY_PLAN.md` 执行：目录序跋、重复、案例、理论、疑文各有去向；非八术材料入知识库，不造算法规则；`verified` 保持 false；不改原文、他人注解、inventory、公共导出、算法、依赖或 main。

## 基线核验

`d47f77d18bae74240986d04ce830ec094436ce39` 是 corpus-3 交包初稿，不是语义验收。

| 项 | 结果 |
|---|---|
| 源文段落 | 1058，与注解 ID 集合、顺序完全一致 |
| 复制古文（`原文：`） | 1049 |
| 通用模板（作用对象须按本句已写…） | 1048 |
| 可考虑保留的实质白话 | 5（目录、半截序、水星生制、两条题署） |
| 图像/无字 draft | 4 |
| 几乎一律标成规则候选 | 1050，分类不可信 |

已有条目只有对照原文后实质正确才保留。需要重写的，按段写现代白话和成立前提，不改 label 冒充审读。

## 网站章节（不等于印本卷号）

1. 卷一（首卷）53
2. 卷之一 223
3. 二卷 229
4. 卷之三 55
5. 卷之四 36
6. 卷六 238
7. 卷之六 75
8. 卷八 148
9. 卷十 1

## 处理原则

- 星平杂纂：七政垣局与子平用神分条，不混成一条算法。
- 禄主五条须并得用；见七强不自动发福。
- 否定、例外、转折、救应与前后文同一审读单元。
- 疑文保留原字与 `unknown`，不发明字句。
- 研究参考，`runtimeEvidenceAllowed=false`。
- `source-reviewed` 只表示对照电子原文；不是影印校勘、人工 verified 或预测有效。

## 进度

- 已完成网站卷一（首卷）53/53：目录序跋补全；三才赋形与生制分开写前提；禄主五条并得用；岁殿岁驾、学堂正印、驿马见财不见子、三方昼夜、九事分档、八煞残图 unknown、诸杀不可执一、小儿关有关无故均对照原文重写。
- 网站卷之一已完成 183/223：十二要法与琴堂要例之后，又据原文重写子女宫不得力、四恶阑干、帝座、十二宫吊宫飞星、月格诸贵、子平细法与乙卷终、弦望月相。中间一批 40 段（金星羊刃、太乙抱蟾至限路）仍是账本空洞，下一轮先补，不把本章标成 done。
- 其余 822 段仍在按章重写。全文件 substantively 处理完毕且必要 validator 通过前，不写 `WORK_PACKAGE_COMPLETE`。

`validate-annotations.py` 对本文件：1058 entries，0 errors（结构/ID only）。
