# 全库书目与覆盖清单

生成日期：2026-09-12。由 `tools/build-library-inventory.py` 从磁盘实数生成，不沿用 55 部完整古籍的说法。

## 口径

- catalog ready 资料包：55
- 磁盘 `references/books/*/*`：55
- 实际 `sources/fulltext/**/fulltext.md`：54
- catalog 另列排除项：4
- 稳定段落：53640（含疑文段 1261）
- 旧 rules.yaml 候选记录：1356（其中 declared verified=true：0；不作运行权威）
- 新规则定义记录：258，有规则白话 258（仅统计 `references/executable/*.json`；不据此认定运行接入或分支验证完成）
- 新规则 declared verified=true：0（只读已有标记，不自动提升）
- 独立盘面读法：14（`references/readings/chart-notes.json`；不换算成全文白话覆盖）

## 实际语义加工进度

- 已有段落注解：41900 / 53640
- 标记电子原文审读 source-reviewed：41036（不是人工影印核验）
- 有非空白话或处理说明的段落：41900（其中 source-reviewed：41036）
- 尚无注解：11740；尚无段落白话：11740
- 原文字面重复段：9220（仅忽略空白比较，same_text_as 不代表流派或理论等价）

上述是文件中实际存在的产物统计，不是全库完成率。模式分类只帮助找材料，未分类、只有规则标题或未审读白话都不能算完成。

## 去向

- 对应八术引擎：21
- 可检索知识库，未接入八术页面：33
- 版权排除：1
- 缺全文：0

## 影印可用性

- 已存影印／候选底本：34 个资料包，关联 75 个不同本地文件。合刊与四库同册可以关联多书，不重复保存或计为多个文件。
- 超限原件位于既有 Release：5 个资料包；未计入上述本地文件数。
- 当前未确认影印：16 个资料包；这不是世界范围不存在底本的结论。
- 文件存在不代表与电子本文字完全一致，也不证明同版、卷页齐全或已经逐页校勘。
- 共享底本关联依据：`sources/facsimile/wikisource/MANIFEST.md` F01–F08，以及 `sources/facsimile/other/MANIFEST.md` 的都天宝照经条目；不存在的文件不会算作 in_repo。

## 资料包

| 系统 | slug | 书名 | 文字文件 | 段落 | 注解 | 段落白话 | 规则定义 | 去向 | 影印 |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| bazi | ditiansui-chanwei | 滴天髓阐微 | 是 | 5681 | 5681 | 5681 | 0 | engine | 已存影印／候选底本 |
| bazi | mingli-yueyan | 命理约言 | 是 | 540 | 540 | 540 | 0 | engine | 已存影印／候选底本 |
| bazi | qiongtong-baojian | 穷通宝鉴 | 是 | 605 | 605 | 605 | 120 | engine | 尚未确认影印 |
| bazi | sanming-tonghui | 三命通会 | 是 | 970 | 970 | 970 | 20 | engine | 已存影印／候选底本 |
| bazi | shenfeng-tongkao | 神峰通考 | 是 | 15 | 15 | 15 | 2 | engine | 已存影印／候选底本 |
| bazi | yuanhai-ziping | 渊海子平 | 是 | 2409 | 2409 | 2409 | 0 | engine | 已存影印／候选底本 |
| bazi | ziping-zhenquan | 子平真诠 | 是 | 556 | 556 | 556 | 39 | engine | 已存影印／候选底本 |
| divination | bushi-zhengzong | 卜筮正宗 | 是 | 9 | 9 | 9 | 2 | engine | 已存影印／候选底本 |
| divination | huangji-jingshi | 皇极经世书 | 是 | 8789 | 0 | 0 | 0 | knowledge | Release 影印／候选底本 |
| divination | huangjin-ce | 黄金策 | 是 | 849 | 849 | 849 | 0 | knowledge | 尚未确认影印 |
| divination | huozhu-lin | 火珠林 | 是 | 314 | 314 | 314 | 0 | engine | Release 影印／候选底本 |
| divination | meihua-yishu | 梅花易数 | 是 | 623 | 623 | 623 | 1 | engine | 尚未确认影印 |
| divination | zengshan-buyi | 增删卜易 | 是 | 3125 | 3125 | 3125 | 19 | engine | 尚未确认影印 |
| divination | zhouyi-zhezhong | 御纂周易折中 | 是 | 1622 | 1622 | 1622 | 0 | knowledge | Release 影印／候选底本 |
| fengshui | dili-bianzheng | 地理辨正 | 是 | 2 | 2 | 2 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | dutian-baozhao-jing | 都天宝照经 | 是 | 101 | 101 | 101 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | hanlong-jing | 撼龙经 | 是 | 6 | 6 | 6 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | huangdi-zhaijing | 黄帝宅经 | 是 | 11 | 11 | 11 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | qingnang-aoyu | 青囊奥语 | 是 | 3 | 3 | 3 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | qingnang-jing | 青囊经 | 是 | 24 | 24 | 24 | 0 | knowledge | 尚未确认影印 |
| fengshui | qingnang-xu | 青囊序 | 是 | 1 | 1 | 1 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | rudi-yan-quanshu | 入地眼全书 | 是 | 126 | 126 | 126 | 0 | knowledge | 尚未确认影印 |
| fengshui | shenshi-xuankong-xue | 沈氏玄空学 | 是 | 1191 | 0 | 0 | 0 | knowledge | 尚未确认影印 |
| fengshui | tianyu-jing | 天玉经 | 是 | 224 | 224 | 224 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | xuexin-fu | 雪心赋 | 是 | 18 | 18 | 18 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | yangzhai-sanyao | 阳宅三要 | 是 | 2 | 2 | 2 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | yangzhai-shishu | 阳宅十书 | 是 | 9 | 9 | 9 | 0 | knowledge | 尚未确认影印 |
| fengshui | yilong-jing | 疑龙经 | 是 | 96 | 96 | 96 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | zangfa-daozhang | 葬法倒杖 | 是 | 13 | 13 | 13 | 0 | knowledge | 已存影印／候选底本 |
| fengshui | zangshu | 葬书 | 是 | 17 | 17 | 17 | 0 | knowledge | 已存影印／候选底本 |
| luming-nayin | lantai-miaoxuan | 兰台妙选 | 是 | 7 | 7 | 7 | 0 | knowledge | 尚未确认影印 |
| luming-nayin | li-xuzhong-mingshu | 李虚中命书 | 是 | 8 | 8 | 8 | 0 | knowledge | 已存影印／候选底本 |
| luming-nayin | luoluzi-sanming | 珞琭子三命消息赋 | 是 | 156 | 156 | 156 | 0 | knowledge | 已存影印／候选底本 |
| luming-nayin | wuxing-jingji | 五行精纪 | 是 | 4294 | 4294 | 4294 | 0 | knowledge | 已存影印／候选底本 |
| luming-nayin | yuzhao-shenying | 玉照神应真经 | 是 | 2 | 2 | 2 | 0 | knowledge | 已存影印／候选底本 |
| physiognomy | bingjian | 冰鉴 | 是 | 26 | 26 | 26 | 0 | knowledge | 尚未确认影印 |
| physiognomy | liuzhuang-xiangfa | 柳庄相法 | 是 | 2 | 2 | 2 | 0 | knowledge | 已存影印／候选底本 |
| physiognomy | mayi-shenxiang | 麻衣神相 | 是 | 1627 | 1627 | 1627 | 0 | knowledge | 已存影印／候选底本 |
| physiognomy | shenxiang-quanbian | 神相全编 | 是 | 345 | 345 | 345 | 0 | knowledge | 尚未确认影印 |
| san-shi | daliuren-daquan | 大六壬大全 | 是 | 6893 | 6893 | 6893 | 22 | engine | 已存影印／候选底本 |
| san-shi | liuren-miben | 大六壬秘本 | 是 | 2643 | 2643 | 2643 | 0 | engine | Release 影印／候选底本 |
| san-shi | liuren-zhiyin | 六壬指南注解（张洪注本） | 是 | 13 | 13 | 13 | 1 | engine | 已存影印／候选底本 |
| san-shi | qimen-dunjia-tongzhi | 奇门遁甲统宗大全 | 是 | 739 | 739 | 739 | 6 | engine | 已存影印／候选底本 |
| san-shi | qimen-faqiao | 奇门法窍（V5.1 核验摘录） | 否 | 0 | 0 | 0 | 0 | excluded_copyright | 尚未确认影印 |
| san-shi | taiyi-shenshu | 太乙神数 | 是 | 209 | 209 | 209 | 0 | knowledge | Release 影印／候选底本 |
| selection | donggong-zeri | 董公择日 | 是 | 198 | 198 | 198 | 0 | knowledge | 已存影印／候选底本 |
| selection | xieji-bianfang-shu | 协纪辨方书 | 是 | 2399 | 2399 | 2399 | 0 | knowledge | 已存影印／候选底本 |
| selection | xingli-kaoyuan | 星历考原 | 是 | 315 | 315 | 315 | 1 | knowledge | 已存影印／候选底本 |
| selection | yuqia-ji | 玉匣记 | 是 | 1779 | 19 | 19 | 6 | knowledge | 尚未确认影印 |
| xingming | guotian-jing | 果天经/果老星宗 | 是 | 247 | 247 | 247 | 1 | engine | 尚未确认影印 |
| xingming | xingming-suyuan | 星命溯源 | 是 | 75 | 75 | 75 | 0 | engine | 已存影印／候选底本 |
| xingming | xingxue-dacheng | 星学大成 | 是 | 1392 | 1392 | 1392 | 6 | engine | 已存影印／候选底本 |
| ziwei | feixing-ziwei-doushu-yuanzhi | 華山陳希夷先生飛星紫微斗數原旨 / 斗數觀測錄 | 是 | 336 | 336 | 336 | 0 | engine | 已存影印／候选底本 |
| ziwei | taiwei-fu | 太微赋 | 是 | 3 | 3 | 3 | 0 | engine | 尚未确认影印 |
| ziwei | ziwei-doushu-quanshu | 紫微斗数全书 | 是 | 1981 | 1981 | 1981 | 12 | engine | 尚未确认影印 |

## 排除项

- `ziwei/doushu-guanjian` 《斗数管见》：不入库。
- `xingming/qizheng-siyu-tianjing` 《七政四余天经》：不入库。
- `xingming/qizheng-quanshu-dacheng` 《七政全書大成》：不入库。
- `xingming/minghai-quanbian` 《新刻星平總會命海全編》：不入库。

## 段落分类来源

- pattern 文本模式初筛：915；annotation 实际语义注解：41900；unclassified 待分类：10825
- 四柱案例从正文命造或带评语的四组干支识别；起例、先取后取与月起顺逆等操作从正文识别。模式结果仍可能需修订，不当作人工审读。
- 目录、序跋不硬造解读；无分类依据时保留待分类。疑字只标记，不由模型补字。

- 理论：11830
- 待分类：10825
- 规则候选：10744
- 评注或元数据：7136
- 案例：4116
- 术语：3404
- 序跋目录：2363
- 操作步骤：1841
- 待核实：911
- 重复：470

段落 ID 形如 `slug:L0123-L0125`，对应 `sources/fulltext/.../fulltext.md` 行号，明细在 `references/inventory/paragraphs/`。

## 注解输入约定

读取 `references/annotations/{system}/{slug}.json`：顶层 `bookSlug`、`entries`；每项 `paragraphId` 必须对应已有确切段落，`kind` 为分类，`vernacular` 为非空中文白话或处理说明，`terms`、`notes` 为数组，`review` 为 `source-reviewed` 或 `draft`。草稿也需要实际说明；同一文件同一段落只一项注解；错误或重复 ID 会中止生成，避免虚增进度。

分类支持：理论、术语、规则候选、操作步骤、案例、序跋目录、评注或元数据、重复、待核实、待分类。source-reviewed 表示这条注解已对照电子原文，不替代 human verified，也不证明算法可执行。

