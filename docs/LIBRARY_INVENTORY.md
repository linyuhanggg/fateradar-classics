# 全库书目与覆盖清单

生成日期：2026-09-08。由 `tools/build-library-inventory.py` 从磁盘实数生成，不沿用 55 部完整古籍的说法。

## 口径

- catalog ready 资料包：55
- 磁盘 `references/books/*/*`：55
- 实际 `sources/fulltext/**/fulltext.md`：54
- catalog 另列排除项：4
- 稳定段落：53640（含疑文段 1261）
- 旧 rules.yaml 候选记录：1356（其中 declared verified=true：0；不作运行权威）
- 新规则定义记录：82，有规则白话 82（仅统计 `references/executable/*.json`；不据此认定运行接入或分支验证完成）
- 新规则 declared verified=true：0（只读已有标记，不自动提升）
- 独立盘面读法：11（`references/readings/chart-notes.json`；不换算成全文白话覆盖）

## 实际语义加工进度

- 已有段落注解：617 / 53640
- 标记电子原文审读 source-reviewed：617（不是人工影印核验）
- 有非空白话或处理说明的段落：617（其中 source-reviewed：617）
- 尚无注解：53023；尚无段落白话：53023
- 原文字面重复段：9220（仅忽略空白比较，same_text_as 不代表流派或理论等价）

上述是文件中实际存在的产物统计，不是全库完成率。模式分类只帮助找材料，未分类、只有规则标题或未审读白话都不能算完成。

## 去向

- 对应八术引擎：21
- 可检索知识库，未接入八术页面：33
- 版权排除：1
- 缺全文：0

## 资料包

| 系统 | slug | 书名 | 全文 | 段落 | 注解 | 段落白话 | 规则定义 | 去向 | 影印 |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| bazi | ditiansui-chanwei | 滴天髓阐微 | 是 | 5681 | 0 | 0 | 0 | engine | not_confirmed |
| bazi | mingli-yueyan | 命理约言 | 是 | 540 | 0 | 0 | 0 | engine | in_repo |
| bazi | qiongtong-baojian | 穷通宝鉴 | 是 | 605 | 0 | 0 | 1 | engine | not_confirmed |
| bazi | sanming-tonghui | 三命通会 | 是 | 970 | 0 | 0 | 20 | engine | in_repo |
| bazi | shenfeng-tongkao | 神峰通考 | 是 | 15 | 0 | 0 | 2 | engine | in_repo |
| bazi | yuanhai-ziping | 渊海子平 | 是 | 2409 | 0 | 0 | 0 | engine | in_repo |
| bazi | ziping-zhenquan | 子平真诠 | 是 | 556 | 556 | 556 | 39 | engine | in_repo |
| divination | bushi-zhengzong | 卜筮正宗 | 是 | 9 | 0 | 0 | 0 | engine | in_repo |
| divination | huangji-jingshi | 皇极经世书 | 是 | 8789 | 0 | 0 | 0 | knowledge | oversize_release |
| divination | huangjin-ce | 黄金策 | 是 | 849 | 0 | 0 | 0 | knowledge | not_confirmed |
| divination | huozhu-lin | 火珠林 | 是 | 314 | 0 | 0 | 0 | engine | oversize_release |
| divination | meihua-yishu | 梅花易数 | 是 | 623 | 0 | 0 | 1 | engine | not_confirmed |
| divination | zengshan-buyi | 增删卜易 | 是 | 3125 | 0 | 0 | 2 | engine | not_confirmed |
| divination | zhouyi-zhezhong | 御纂周易折中 | 是 | 1622 | 0 | 0 | 0 | knowledge | oversize_release |
| fengshui | dili-bianzheng | 地理辨正 | 是 | 2 | 0 | 0 | 0 | knowledge | in_repo |
| fengshui | dutian-baozhao-jing | 都天宝照经 | 是 | 101 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | hanlong-jing | 撼龙经 | 是 | 6 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | huangdi-zhaijing | 黄帝宅经 | 是 | 11 | 11 | 11 | 0 | knowledge | not_confirmed |
| fengshui | qingnang-aoyu | 青囊奥语 | 是 | 3 | 3 | 3 | 0 | knowledge | not_confirmed |
| fengshui | qingnang-jing | 青囊经 | 是 | 24 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | qingnang-xu | 青囊序 | 是 | 1 | 1 | 1 | 0 | knowledge | not_confirmed |
| fengshui | rudi-yan-quanshu | 入地眼全书 | 是 | 126 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | shenshi-xuankong-xue | 沈氏玄空学 | 是 | 1191 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | tianyu-jing | 天玉经 | 是 | 224 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | xuexin-fu | 雪心赋 | 是 | 18 | 0 | 0 | 0 | knowledge | in_repo |
| fengshui | yangzhai-sanyao | 阳宅三要 | 是 | 2 | 0 | 0 | 0 | knowledge | in_repo |
| fengshui | yangzhai-shishu | 阳宅十书 | 是 | 9 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | yilong-jing | 疑龙经 | 是 | 96 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | zangfa-daozhang | 葬法倒杖 | 是 | 13 | 0 | 0 | 0 | knowledge | not_confirmed |
| fengshui | zangshu | 葬书 | 是 | 17 | 17 | 17 | 0 | knowledge | not_confirmed |
| luming-nayin | lantai-miaoxuan | 兰台妙选 | 是 | 7 | 0 | 0 | 0 | knowledge | not_confirmed |
| luming-nayin | li-xuzhong-mingshu | 李虚中命书 | 是 | 8 | 0 | 0 | 0 | knowledge | in_repo |
| luming-nayin | luoluzi-sanming | 珞琭子三命消息赋 | 是 | 156 | 0 | 0 | 0 | knowledge | in_repo |
| luming-nayin | wuxing-jingji | 五行精纪 | 是 | 4294 | 0 | 0 | 0 | knowledge | in_repo |
| luming-nayin | yuzhao-shenying | 玉照神应真经 | 是 | 2 | 0 | 0 | 0 | knowledge | not_confirmed |
| physiognomy | bingjian | 冰鉴 | 是 | 26 | 26 | 26 | 0 | knowledge | not_confirmed |
| physiognomy | liuzhuang-xiangfa | 柳庄相法 | 是 | 2 | 0 | 0 | 0 | knowledge | in_repo |
| physiognomy | mayi-shenxiang | 麻衣神相 | 是 | 1627 | 0 | 0 | 0 | knowledge | in_repo |
| physiognomy | shenxiang-quanbian | 神相全编 | 是 | 345 | 0 | 0 | 0 | knowledge | not_confirmed |
| san-shi | daliuren-daquan | 大六壬大全 | 是 | 6893 | 0 | 0 | 9 | engine | not_confirmed |
| san-shi | liuren-miben | 大六壬秘本 | 是 | 2643 | 0 | 0 | 0 | engine | oversize_release |
| san-shi | liuren-zhiyin | 六壬指南注解（张洪注本） | 是 | 13 | 0 | 0 | 0 | engine | in_repo |
| san-shi | qimen-dunjia-tongzhi | 奇门遁甲统宗大全 | 是 | 739 | 0 | 0 | 2 | engine | in_repo |
| san-shi | qimen-faqiao | 奇门法窍（V5.1 核验摘录） | 否 | 0 | 0 | 0 | 0 | excluded_copyright | not_confirmed |
| san-shi | taiyi-shenshu | 太乙神数 | 是 | 209 | 0 | 0 | 0 | knowledge | oversize_release |
| selection | donggong-zeri | 董公择日 | 是 | 198 | 0 | 0 | 0 | knowledge | in_repo |
| selection | xieji-bianfang-shu | 协纪辨方书 | 是 | 2399 | 0 | 0 | 0 | knowledge | in_repo |
| selection | xingli-kaoyuan | 星历考原 | 是 | 315 | 0 | 0 | 1 | knowledge | in_repo |
| selection | yuqia-ji | 玉匣记 | 是 | 1779 | 0 | 0 | 0 | knowledge | not_confirmed |
| xingming | guotian-jing | 果天经/果老星宗 | 是 | 247 | 0 | 0 | 1 | engine | not_confirmed |
| xingming | xingming-suyuan | 星命溯源 | 是 | 75 | 0 | 0 | 0 | engine | not_confirmed |
| xingming | xingxue-dacheng | 星学大成 | 是 | 1392 | 0 | 0 | 3 | engine | not_confirmed |
| ziwei | feixing-ziwei-doushu-yuanzhi | 華山陳希夷先生飛星紫微斗數原旨 / 斗數觀測錄 | 是 | 336 | 0 | 0 | 0 | engine | in_repo |
| ziwei | taiwei-fu | 太微赋 | 是 | 3 | 3 | 3 | 0 | engine | not_confirmed |
| ziwei | ziwei-doushu-quanshu | 紫微斗数全书 | 是 | 1981 | 0 | 0 | 1 | engine | not_confirmed |

## 排除项

- `ziwei/doushu-guanjian` 《斗数管见》：不入库。
- `xingming/qizheng-siyu-tianjing` 《七政四余天经》：不入库。
- `xingming/qizheng-quanshu-dacheng` 《七政全書大成》：不入库。
- `xingming/minghai-quanbian` 《新刻星平總會命海全編》：不入库。

## 段落分类来源

- pattern 文本模式初筛：3210；annotation 实际语义注解：617；unclassified 待分类：49813
- 四柱案例从正文命造或带评语的四组干支识别；起例、先取后取与月起顺逆等操作从正文识别。模式结果仍可能需修订，不当作人工审读。
- 目录、序跋不硬造解读；无分类依据时保留待分类。疑字只标记，不由模型补字。

- 待分类：49813
- 理论：2423
- 操作步骤：402
- 序跋目录：368
- 案例：316
- 评注或元数据：156
- 规则候选：148
- 术语：13
- 重复：1

段落 ID 形如 `slug:L0123-L0125`，对应 `sources/fulltext/.../fulltext.md` 行号，明细在 `references/inventory/paragraphs/`。

## 注解输入约定

读取 `references/annotations/{system}/{slug}.json`：顶层 `bookSlug`、`entries`；每项 `paragraphId` 必须对应已有确切段落，`kind` 为分类，`vernacular` 为非空中文白话或处理说明，`terms`、`notes` 为数组，`review` 为 `source-reviewed` 或 `draft`。草稿也需要实际说明；同一文件同一段落只一项注解；错误或重复 ID 会中止生成，避免虚增进度。

分类支持：理论、术语、规则候选、操作步骤、案例、序跋目录、评注或元数据、重复、待核实、待分类。source-reviewed 表示这条注解已对照电子原文，不替代 human verified，也不证明算法可执行。

