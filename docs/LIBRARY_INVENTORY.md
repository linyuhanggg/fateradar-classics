# 全库书目与覆盖清单

生成日期：2026-09-08。由 `tools/build-library-inventory.py` 从磁盘实数生成，不沿用 55 部完整古籍的说法。

## 口径

- catalog ready 资料包：55
- 磁盘 `references/books/*/*`：55
- 实际 `sources/fulltext/**/fulltext.md`：54
- catalog 另列排除项：4
- 稳定段落：53640（含疑文段 1261）
- 旧 rules.yaml 候选：1356（全部 verified=false，不作运行权威）
- 本轮接入可执行规则：33（`references/executable/*.json` 实数；产品引擎实现等价条件）

## 去向

- 对应八术引擎：21
- 可检索知识库，未接入八术页面：33
- 版权排除：1
- 缺全文：0

## 资料包

| 系统 | slug | 书名 | 全文 | 段落 | 去向 | 影印 |
|---|---|---|---:|---:|---|---|
| bazi | ditiansui-chanwei | 滴天髓阐微 | 是 | 5681 | engine | not_confirmed |
| bazi | mingli-yueyan | 命理约言 | 是 | 540 | engine | in_repo |
| bazi | qiongtong-baojian | 穷通宝鉴 | 是 | 605 | engine | not_confirmed |
| bazi | sanming-tonghui | 三命通会 | 是 | 970 | engine | in_repo |
| bazi | shenfeng-tongkao | 神峰通考 | 是 | 15 | engine | in_repo |
| bazi | yuanhai-ziping | 渊海子平 | 是 | 2409 | engine | in_repo |
| bazi | ziping-zhenquan | 子平真诠 | 是 | 556 | engine | in_repo |
| divination | bushi-zhengzong | 卜筮正宗 | 是 | 9 | engine | in_repo |
| divination | huangji-jingshi | 皇极经世书 | 是 | 8789 | knowledge | oversize_release |
| divination | huangjin-ce | 黄金策 | 是 | 849 | knowledge | not_confirmed |
| divination | huozhu-lin | 火珠林 | 是 | 314 | engine | oversize_release |
| divination | meihua-yishu | 梅花易数 | 是 | 623 | engine | not_confirmed |
| divination | zengshan-buyi | 增删卜易 | 是 | 3125 | engine | not_confirmed |
| divination | zhouyi-zhezhong | 御纂周易折中 | 是 | 1622 | knowledge | oversize_release |
| fengshui | dili-bianzheng | 地理辨正 | 是 | 2 | knowledge | in_repo |
| fengshui | dutian-baozhao-jing | 都天宝照经 | 是 | 101 | knowledge | not_confirmed |
| fengshui | hanlong-jing | 撼龙经 | 是 | 6 | knowledge | not_confirmed |
| fengshui | huangdi-zhaijing | 黄帝宅经 | 是 | 11 | knowledge | not_confirmed |
| fengshui | qingnang-aoyu | 青囊奥语 | 是 | 3 | knowledge | not_confirmed |
| fengshui | qingnang-jing | 青囊经 | 是 | 24 | knowledge | not_confirmed |
| fengshui | qingnang-xu | 青囊序 | 是 | 1 | knowledge | not_confirmed |
| fengshui | rudi-yan-quanshu | 入地眼全书 | 是 | 126 | knowledge | not_confirmed |
| fengshui | shenshi-xuankong-xue | 沈氏玄空学 | 是 | 1191 | knowledge | not_confirmed |
| fengshui | tianyu-jing | 天玉经 | 是 | 224 | knowledge | not_confirmed |
| fengshui | xuexin-fu | 雪心赋 | 是 | 18 | knowledge | in_repo |
| fengshui | yangzhai-sanyao | 阳宅三要 | 是 | 2 | knowledge | in_repo |
| fengshui | yangzhai-shishu | 阳宅十书 | 是 | 9 | knowledge | not_confirmed |
| fengshui | yilong-jing | 疑龙经 | 是 | 96 | knowledge | not_confirmed |
| fengshui | zangfa-daozhang | 葬法倒杖 | 是 | 13 | knowledge | not_confirmed |
| fengshui | zangshu | 葬书 | 是 | 17 | knowledge | not_confirmed |
| luming-nayin | lantai-miaoxuan | 兰台妙选 | 是 | 7 | knowledge | not_confirmed |
| luming-nayin | li-xuzhong-mingshu | 李虚中命书 | 是 | 8 | knowledge | in_repo |
| luming-nayin | luoluzi-sanming | 珞琭子三命消息赋 | 是 | 156 | knowledge | in_repo |
| luming-nayin | wuxing-jingji | 五行精纪 | 是 | 4294 | knowledge | in_repo |
| luming-nayin | yuzhao-shenying | 玉照神应真经 | 是 | 2 | knowledge | not_confirmed |
| physiognomy | bingjian | 冰鉴 | 是 | 26 | knowledge | not_confirmed |
| physiognomy | liuzhuang-xiangfa | 柳庄相法 | 是 | 2 | knowledge | in_repo |
| physiognomy | mayi-shenxiang | 麻衣神相 | 是 | 1627 | knowledge | in_repo |
| physiognomy | shenxiang-quanbian | 神相全编 | 是 | 345 | knowledge | not_confirmed |
| san-shi | daliuren-daquan | 大六壬大全 | 是 | 6893 | engine | not_confirmed |
| san-shi | liuren-miben | 大六壬秘本 | 是 | 2643 | engine | oversize_release |
| san-shi | liuren-zhiyin | 六壬指南注解（张洪注本） | 是 | 13 | engine | in_repo |
| san-shi | qimen-dunjia-tongzhi | 奇门遁甲统宗大全 | 是 | 739 | engine | in_repo |
| san-shi | qimen-faqiao | 奇门法窍（V5.1 核验摘录） | 否 | 0 | excluded_copyright | not_confirmed |
| san-shi | taiyi-shenshu | 太乙神数 | 是 | 209 | knowledge | oversize_release |
| selection | donggong-zeri | 董公择日 | 是 | 198 | knowledge | in_repo |
| selection | xieji-bianfang-shu | 协纪辨方书 | 是 | 2399 | knowledge | in_repo |
| selection | xingli-kaoyuan | 星历考原 | 是 | 315 | knowledge | in_repo |
| selection | yuqia-ji | 玉匣记 | 是 | 1779 | knowledge | not_confirmed |
| xingming | guotian-jing | 果天经/果老星宗 | 是 | 247 | engine | not_confirmed |
| xingming | xingming-suyuan | 星命溯源 | 是 | 75 | engine | not_confirmed |
| xingming | xingxue-dacheng | 星学大成 | 是 | 1392 | engine | not_confirmed |
| ziwei | feixing-ziwei-doushu-yuanzhi | 華山陳希夷先生飛星紫微斗數原旨 / 斗數觀測錄 | 是 | 336 | engine | in_repo |
| ziwei | taiwei-fu | 太微赋 | 是 | 3 | engine | not_confirmed |
| ziwei | ziwei-doushu-quanshu | 紫微斗数全书 | 是 | 1981 | engine | not_confirmed |

## 排除项

- `ziwei/doushu-guanjian` 《斗数管见》：不入库。
- `xingming/qizheng-siyu-tianjing` 《七政四余天经》：不入库。
- `xingming/qizheng-quanshu-dacheng` 《七政全書大成》：不入库。
- `xingming/minghai-quanbian` 《新刻星平總會命海全編》：不入库。

## 段落种类（启发式，不是人工审读）

目录、序跋不硬造解读。疑字只标记，不由模型补字。

- 理论：53107
- 序跋目录：314
- 评注或元数据：146
- 操作步骤：66
- 案例：7

段落 ID 形如 `slug:L0123-L0125`，对应 `sources/fulltext/.../fulltext.md` 行号，明细在 `references/inventory/paragraphs/`。

