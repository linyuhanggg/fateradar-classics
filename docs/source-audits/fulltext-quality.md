# 全库文字原料真实性核查

核查日期：2026-09-08。范围：54 个 `fulltext.md` 与 2 份补充文本。仅写本报告和 `references/source-quality.json`，未改原文、段落索引、注解或规则。命理约言影印恢复由另一工作包负责，本次不重复 OCR。

## 结论与口径

- **确认《命理约言》当前所谓 fulltext 只有导航与相关文章标题，没有实质正文。** 应保留为来源线索，并明确“正文恢复中”，不能继续按已整理古籍提供判断依据。
- 其余 **53 个主文件及 2 个补充文件均已看到实质文字**。这只证明有正文，不证明书卷齐全、各版一致、所有图像已在库，更不证明每字正确。
- 需要实际修复或分层的问题集中在：长段重复、跨书归属、现代附益分层以及图像/表格丢失。没有把少量网页页脚或短行视为整本缺文。
- 本轮**没有确认第二份整文件只有导航，也没有确认某一整份书完全 OCR 不可读**。皇极声韵表的方框不能仅凭数量定为乱码。

方法：先对全部56份文本做导航行、短行、重复长段、缺字符与图片占位筛选；再逐份读前/中/后部的分散段落，对疑点追加连续上下文。下面的行号是实际阅读证据。此为原料排雷与正文存在性核查，**不是逐页影印校勘，也不是全书逐字通读认证**。影印路径结合现存文件与既有 MANIFEST 核对，本次未重新通读全部 PDF/DjVu。

机器状态的含义：`text-present` = 已见实质正文；`navigation-only` = 当前无正文；`mixed` = 明确合刊/多作品或古今混合层；`unassessed` = 未完成真实性判断。图表缺失等具体问题写在 notes，不用状态伪装成完整性评分。

## 已确认问题与恢复路径

### 1. 命理约言：49个网页分节全部抓成导航

- 文件：`sources/fulltext/bazi/mingli-yueyan/fulltext.md`。
- L6–29 的“序”下面只有上一篇、下一篇、相关文章；L32–55“看命总法”仍只有标题；L1158–1180“卷四杂论”同样没有论说。
- 全文去掉文件说明、49个标题及 source/raw 元数据，再去掉导航词和文章标题后，没有剩余实质段落。10条带`...-`后缀的标题亦逐条确认是截断的相关文章标题，而非正文。
- 原料说明写“逐篇整理”为不实覆盖表述。不可依据当前行号生成该书算法或白话正文。
- 现存影印：`sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf`。这是《精选命理约言》选定扫描，不能未核目录便宣称覆盖所有异本。恢复工作另行进行。

### 2. 麻衣相法：长段重复；现代层已有标识，须继承

- 文件：`sources/fulltext/physiognomy/mayi-shenxiang/fulltext.md`。
- **L2300–2580 与 L2582–2981 重复281条非空行**：后一份增加 Markdown 标题和空行，正文仍相同。范围从“诗曰：贵人足厚…”到达摩相法结偈。不是只重复一个术语，也不能当第二次证据。
- 原文件 L1–15 和 L17–34 已明确：QX-01为现代前言，QX-12至14为现代附益。L4766“消化器官”等确在现代层，**不把这一点包装成新发现的伪造古文**；下游必须继承原有分层。
- 建议：原始文件保留，派生段落标重复及引用关系；现代层不得赋予古籍原文身份。
- 现存影印：`sources/facsimile/wikimedia-known/mayi-shenxiang/NLC416-12jh002690-44091 麻衣相法 第1卷.pdf`、`NLC416-12jh002690-44092 麻衣相法 第2卷.pdf`。网页六卷与影印两卷尚需建立目录对应，不直接宣称同版。

### 3. 奇门统宗：合卷层明记缺文，且与卷十大段重复

- 主文件：`sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`。
- L1017题“卷四～九”，L1019起太阴休门；L1033直接写“注缺。太阴会景门，及太阴会死门赋，均缺”。
- L1019–1059 与卷十下的 L1293–1333连续21条非空行相同；L1081–1125与L1355–1399连续23条相同；其后还存在18条、21条连续重复块。
- 现阶段只可确定当前转写存在缺文提示与重章。**未逐页对NLC前，不武断断言原书卷四至九全部不存在；同样不能用一个合卷标题证明六卷已齐。**
- 补充文件 `sources/fulltext/san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md` 的L1、L9–25已说明非canonical对照，亦重现同一太阴片段和缺文。它不是独立完整补本。
- 现存恢复锚：`sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf`；清单称十二卷选定扫描，须按卷页核明重章/缺句来源后再整理。

### 4. 合刊、辑录跨书内容需保留实际作品归属

- `sources/fulltext/fengshui/hanlong-jing/fulltext.md`：L128收尾题《撼龙经》，L130开始《疑龙经》，L229开始《葬法倒杖》。三者都有正文，但后两书不能因存放在hanlong文件夹而全归《撼龙经》。可在派生记录增加书内作品字段，不删除原合刊。
- 恢复锚：`sources/facsimile/wikisource/files/CADAL06054153 撼龍經·撼龍經~疑龍經.djvu`；葬法另有`CADAL06054154 撼龍經·葬法倒杖.djvu`，共享四库0808册亦在库。
- `sources/fulltext/physiognomy/shenxiang-quanbian/fulltext.md`：L19起《相儿经》，L55起《人相篇》，L112才进入《神相全编一》。既有source_risk已要求按作品筛分，应贯彻到段落归属。网页公版说明及AI标点声明（如L881、L883）也不能作原典理论。
- 当前无已确认同书影印恢复文件；`sources/facsimile/missing-recovery/MANIFEST.md` 明确没有把《神相水镜集全编》冒当本书。引用可回到既存维基文库卷631等来源，但本次没有取得新扫描。

### 5. 文字存在，但关键图表未被保存为可用内容

- **沈氏玄空学**：`sources/fulltext/fengshui/shenshi-xuankong-xue/fulltext.md` L1871“列表如下”，L1873随即“观此表”，中间无表；L2829–2832“更正蒋盘简式”只有图片/标题占位。现仓不含说明所称`sources/raw`目录，也未确认可直接恢复的同版影印。应从原来源重新取图/表或取得底本，而不是让模型猜盘。
- 该文件11个`image_only_or_section_title`并非11处正文必缺。例如L3711“阳宅秘断”是组标题，L3717起确有各宅正文，不能整章判空。
- **阳宅十书**：`sources/fulltext/fengshui/yangzhai-shishu/fulltext.md` 全部248处`[圖]`均无图片URL。L2912等符图以及L2985–3042的图列只有占位，现MD不能展示符形或图式。目录和十篇中的文字实际存在；不能因图书集成题“阳宅十书一至四”就推定只剩四篇。
- **神相全编**：L497“十三部位总要之图”之后直接接“十三部位总歌”，图像本身不在现文件。文字可读，不等于相图可供算法或用户核看。
- 这三书当前清单都没有已确认、在本仓的同版影印恢复路径。保留来源链接线索；不要写成已经恢复图像。

### 6. 数据清单还漏认了共享影印件

当前`library-inventory.json`只按slug目录识别时，会把滴天髓及多部共享四库/合刊的书标为`not_confirmed`。但`wikisource/files`实际有文件，且`wikisource/MANIFEST.md`明列覆盖书目。下面逐书表使用这些已存路径，**本次未改inventory**。恢复条件不能只看slug文件夹是否存在。

## 已排除的误报及仍须保持的边界

- 青囊奥语、青囊序、太微赋等是短篇，已实际读到歌诀/赋文，不因字少判无正文。太微赋仍按母书分出章节资料处理，不再数成另一部独立全本。
- 青囊经先列三卷经文，随后明确标“蒋大鸿注”；逐句短行不是OCR无正文。葬书先列后人敘与目录，再列内/外/杂篇；序中玄空术语不可直接归郭璞，但本书确有正文。
- 飞星紫微斗数原旨page-001至116标号连续，前后空页和末勘误表有记录，样读论说可读；不把短行或扉页空白认成整本坏OCR。原文件历史`reviewed_against_image`并非本次重新验过每页。
- 皇极经世书有历史叙事与观物论说。6475个□集中声韵表，另有■、○等表记号；本次未据影印区分空格记号与缺字，故不判“整书OCR失效”。表格须按图表建模，不当散文规则。恢复底本清单为Release里的四库0803册，工作树中无该超限原件，本次未下载。
- 太乙神数资料包当前正文实际是《太乙金镜式经》（L4–5、L40起），并已有〔缺〕标记。以实际题名引用；不能拿泛称证明另一部同名《太乙神数》已处理完整。

## 逐文件正文证据与现存影印定位

以下“有正文”均不等于完整本。每行列出本次读过的分散段落位置；长段或图表异常另见上文。影印路径表示现存恢复/核对锚点，未声明与当前网页转写每字相同。

| 资料 | 状态 | 文字文件及样读证据 | 现存影印／恢复定位 |
|---|---|---|---|
| 滴天髓阐微 | text-present | `sources/fulltext/bazi/ditiansui-chanwei/fulltext.md`<br>L578、L5889、L12131 | `sources/facsimile/wikisource/files/SSID-11335994 滴天髓闡微.pdf` |
| 命理约言 | navigation-only | `sources/fulltext/bazi/mingli-yueyan/fulltext.md`<br>L6–29、L1158–1180（导航） | `sources/facsimile/other/mingli-yueyan/NLC416-17jh002578-109774.pdf` |
| 穷通宝鉴 | text-present | `sources/fulltext/bazi/qiongtong-baojian/fulltext.md`<br>L99、L807、L1602 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 三命通会 | text-present | `sources/fulltext/bazi/sanming-tonghui/fulltext.md`<br>L923、L5206、L8971 | `sources/facsimile/other/sanming-tonghui/NLC416-13jh000156-94145.pdf` |
| 神峰通考 | text-present | `sources/fulltext/bazi/shenfeng-tongkao/fulltext.md`<br>L443、L2222、L4252 | `sources/facsimile/other/shenfeng-tongkao/NLC416-13jh001619-43305.pdf` |
| 渊海子平 | text-present | `sources/fulltext/bazi/yuanhai-ziping/fulltext.md`<br>L242、L1720、L4618 | `sources/facsimile/other/yuanhai-ziping/NLC416-15jh007754-99036.pdf` |
| 子平真诠 | text-present | `sources/fulltext/bazi/ziping-zhenquan/fulltext.md`<br>L165、L917、L1615 | `sources/facsimile/other/ziping-zhenquan/NLC416-11jh010455-35296.pdf` |
| 卜筮正宗 | text-present | `sources/fulltext/divination/bushi-zhengzong/fulltext.md`<br>L296、L2127、L3554 | `sources/facsimile/other/bushi-zhengzong/part-01.pdf`<br>`sources/facsimile/other/bushi-zhengzong/part-02.pdf`<br>同目录共6册（其余见MANIFEST） |
| 皇极经世书 | text-present | `sources/fulltext/divination/huangji-jingshi/fulltext.md`<br>L23828、L29564、L36917 | Release facsimiles-oversize-2026-09-04 / 0803.djvu（工作树无超限文件，本次未下载） |
| 黄金策 | text-present | `sources/fulltext/divination/huangjin-ce/fulltext.md`<br>L174、L904、L1592 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 火珠林 | text-present | `sources/fulltext/divination/huozhu-lin/fulltext.md`<br>L80、L560、L992 | Release facsimiles-oversize-2026-09-04 / GGZBCK421.pdf（工作树无超限文件，本次未下载） |
| 梅花易数 | text-present | `sources/fulltext/divination/meihua-yishu/fulltext.md`<br>L153、L1212、L2226 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 增删卜易 | text-present | `sources/fulltext/divination/zengshan-buyi/fulltext.md`<br>L926、L4638、L7181 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 御纂周易折中 | text-present | `sources/fulltext/divination/zhouyi-zhezhong/fulltext.md`<br>L851、L4792、L8994 | Release facsimiles-oversize-2026-09-04 / 0038.djvu（工作树无超限文件，本次未下载） |
| 地理辨正 | text-present | `sources/fulltext/fengshui/dili-bianzheng/fulltext.md`<br>L93、L1297、L1752 | `sources/facsimile/other/dili-bianzheng/part-01.pdf`<br>`sources/facsimile/other/dili-bianzheng/part-02.pdf`<br>同目录共6册（其余见MANIFEST） |
| 都天宝照经 | text-present | `sources/fulltext/fengshui/dutian-baozhao-jing/fulltext.md`<br>L24、L104、L186 | `sources/facsimile/other/dili-bianzheng/part-01.pdf`<br>`sources/facsimile/other/dili-bianzheng/part-02.pdf`<br>同目录共6册（其余见MANIFEST） |
| 撼龙经 | mixed | `sources/fulltext/fengshui/hanlong-jing/fulltext.md`<br>L29、L142、L289 | `sources/facsimile/wikisource/files/CADAL06054153 撼龍經·撼龍經~疑龍經.djvu`<br>`sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 黄帝宅经 | text-present | `sources/fulltext/fengshui/huangdi-zhaijing/fulltext.md`<br>L20、L44、L73 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu`<br>`sources/facsimile/wikisource/files/明刻本夷門廣牘24.djvu` |
| 青囊奥语 | text-present | `sources/fulltext/fengshui/qingnang-aoyu/fulltext.md`<br>L12、L18、L24 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 青囊经 | text-present | `sources/fulltext/fengshui/qingnang-jing/fulltext.md`<br>L11、L40、L427 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 青囊序 | text-present | `sources/fulltext/fengshui/qingnang-xu/fulltext.md`<br>L4、L10、L15 | `sources/facsimile/wikisource/files/CADAL06054155 青囊序.djvu`<br>`sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 入地眼全书 | text-present | `sources/fulltext/fengshui/rudi-yan-quanshu/fulltext.md`<br>L80、L540、L938 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 沈氏玄空学 | text-present | `sources/fulltext/fengshui/shenshi-xuankong-xue/fulltext.md`<br>L280、L1987、L3766 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 天玉经 | text-present | `sources/fulltext/fengshui/tianyu-jing/fulltext.md`<br>L49、L289、L694 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 雪心赋 | text-present | `sources/fulltext/fengshui/xuexin-fu/fulltext.md`<br>L32、L171、L299 | `sources/facsimile/other/xuexin-fu/NCL-06500.pdf` |
| 阳宅三要 | text-present | `sources/fulltext/fengshui/yangzhai-sanyao/fulltext.md`<br>L121、L826、L1404 | `sources/facsimile/other/yangzhai-sanyao/part-01.pdf`<br>`sources/facsimile/other/yangzhai-sanyao/part-02.pdf` |
| 阳宅十书 | text-present | `sources/fulltext/fengshui/yangzhai-shishu/fulltext.md`<br>L419、L1609、L2560 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 疑龙经 | text-present | `sources/fulltext/fengshui/yilong-jing/fulltext.md`<br>L62、L118、L214 | `sources/facsimile/wikisource/files/CADAL06054153 撼龍經·撼龍經~疑龍經.djvu`<br>`sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 葬法倒杖 | text-present | `sources/fulltext/fengshui/zangfa-daozhang/fulltext.md`<br>L37、L171、L258 | `sources/facsimile/wikisource/files/CADAL06054154 撼龍經·葬法倒杖.djvu`<br>`sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 葬书 | text-present | `sources/fulltext/fengshui/zangshu/fulltext.md`<br>L20、L99、L175 | `sources/facsimile/wikisource/files/CADAL06054152 葬書.djvu`<br>`sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 兰台妙选 | text-present | `sources/fulltext/luming-nayin/lantai-miaoxuan/fulltext.md`<br>L72、L354、L544 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 李虚中命书 | text-present | `sources/fulltext/luming-nayin/li-xuzhong-mingshu/fulltext.md`<br>L31、L128、L220 | `sources/facsimile/other/li-xuzhong-mingshu/CADAL06066015.djvu` |
| 珞琭子三命消息赋 | text-present | `sources/fulltext/luming-nayin/luoluzi-sanming/fulltext.md`<br>L101、L621、L1074 | `sources/facsimile/other/luoluzi-sanming/CADAL06054188.djvu` |
| 五行精纪 | text-present | `sources/fulltext/luming-nayin/wuxing-jingji/fulltext.md`<br>L1499、L6404、L10670 | `sources/facsimile/other/wuxing-jingji/part-01.pdf`<br>`sources/facsimile/other/wuxing-jingji/part-02.pdf`<br>同目录共6册（其余见MANIFEST） |
| 玉照神应真经 | text-present | `sources/fulltext/luming-nayin/yuzhao-shenying/fulltext.md`<br>L20、L73、L124 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0809冊.djvu` |
| 冰鉴 | text-present | `sources/fulltext/physiognomy/bingjian/fulltext.md`<br>L18、L64、L137 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 柳庄相法 | text-present | `sources/fulltext/physiognomy/liuzhuang-xiangfa/fulltext.md`<br>L63、L358、L874 | `sources/facsimile/other/liuzhuang-xiangfa/NLC416-13jh001257-42702.pdf` |
| 麻衣神相 | mixed | `sources/fulltext/physiognomy/mayi-shenxiang/fulltext.md`<br>L641、L3087、L4766 | `sources/facsimile/wikimedia-known/mayi-shenxiang/NLC416-12jh002690-44091 麻衣相法 第1卷.pdf`<br>`sources/facsimile/wikimedia-known/mayi-shenxiang/NLC416-12jh002690-44092 麻衣相法 第2卷.pdf` |
| 神相全编 | mixed | `sources/fulltext/physiognomy/shenxiang-quanbian/fulltext.md`<br>L408、L3036、L4986 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 大六壬大全 | text-present | `sources/fulltext/san-shi/daliuren-daquan/fulltext.md`<br>L3191、L9972、L17594 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu` |
| 大六壬秘本 | text-present | `sources/fulltext/san-shi/liuren-miben/fulltext.md`<br>L533、L3080、L5435 | Release facsimiles-oversize-2026-09-04 / NCL-06572-daliuren-miben.pdf（工作树无超限文件，本次未下载） |
| 六壬指南注解（张洪注本） | text-present | `sources/fulltext/san-shi/liuren-zhiyin/fulltext.md`<br>L259、L1459、L3155 | `sources/facsimile/other/liuren-zhiyin/NLC416-12jh005348-45347.pdf` |
| 奇门遁甲统宗大全 | text-present | `sources/fulltext/san-shi/qimen-dunjia-tongzhi/fulltext.md`<br>L242、L1135、L1861 | `sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf` |
| 太乙神数 | text-present | `sources/fulltext/san-shi/taiyi-shenshu/fulltext.md`<br>L114、L572、L1172 | Release facsimiles-oversize-2026-09-04 / 0810.djvu（工作树无超限文件，本次未下载） |
| 董公择日 | text-present | `sources/fulltext/selection/donggong-zeri/fulltext.md`<br>L82、L490、L876 | `sources/facsimile/wikimedia-known/donggong-zeri/NLC416-12jh005366-44510 董公選要覽.pdf` |
| 协纪辨方书 | text-present | `sources/fulltext/selection/xieji-bianfang-shu/fulltext.md`<br>L544、L4243、L11993 | `sources/facsimile/other/xieji-bianfang-shu/part-01.djvu`<br>`sources/facsimile/other/xieji-bianfang-shu/part-02.djvu`<br>同目录共26册（其余见MANIFEST） |
| 星历考原 | text-present | `sources/fulltext/selection/xingli-kaoyuan/fulltext.md`<br>L168、L862、L1554 | `sources/facsimile/other/xingli-kaoyuan/part-01.pdf`<br>`sources/facsimile/other/xingli-kaoyuan/part-02.pdf`<br>同目录共6册（其余见MANIFEST） |
| 玉匣记 | text-present | `sources/fulltext/selection/yuqia-ji/fulltext.md`<br>L503、L2215、L3965 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 果天经/果老星宗 | text-present | `sources/fulltext/xingming/guotian-jing/fulltext.md`<br>L1389、L4760、L8161 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 星命溯源 | text-present | `sources/fulltext/xingming/xingming-suyuan/fulltext.md`<br>L41、L306、L501 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0809冊.djvu` |
| 星学大成 | text-present | `sources/fulltext/xingming/xingxue-dacheng/fulltext.md`<br>L1106、L4656、L8408 | `sources/facsimile/wikisource/files/文淵閣四庫全書 0809冊.djvu` |
| 華山陳希夷先生飛星紫微斗數原旨 / 斗數觀測錄 | text-present | `sources/fulltext/ziwei/feixing-ziwei-doushu-yuanzhi/fulltext.md`<br>L364、L2355、L3961 | `sources/facsimile/wikimedia-known/feixing-ziwei-doushu-yuanzhi/NLC416-12jh004539-48693 華山陳希夷先生飛星紫微斗數原旨.pdf` |
| 太微赋 | text-present | `sources/fulltext/ziwei/taiwei-fu/fulltext.md`<br>L7、L37、L49 | 当前清单未确认同书影印；不等于世界范围不存在 |
| 紫微斗数全书 | text-present | `sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md`<br>L367、L2647、L4221 | 当前清单未确认同书影印；不等于世界范围不存在 |

### 两份补充文本

| 文件 | 已见实质文字 | 需要保持的边界／恢复锚 |
|---|---|---|
| `sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md` | L232天气歌、L1822断课总论、L3660神将说明均有正文 | L1–13明确是Golla注解对照，并将原卷三、四重编。不是canonical原典，也不是独立第二份证据。现存锚`sources/facsimile/other/liuren-zhiyin/NLC416-12jh005348-45347.pdf`，尚需卷次对照。 |
| `sources/fulltext/san-shi/qimen-dunjia-tongzhi/supplemental-taiyi-qimen-yanyi-vol4-9.md` | L9、L99、L171均为实际奇门断法文字 | L23明确缺句，且与主文件合卷层重叠。现存锚`sources/facsimile/other/qimen-dunjia-tongzhi/NLC416-12jh003951-48665.pdf`；不能据补充文件非空认定卷四至九已恢复。 |

## 后续加工要求

先恢复纯导航书与具体缺图/缺句；对已有实质正文按作品、经文/注释/现代附益分层，重复段建立引用关系。保持原文不动，修订进派生层；恢复影印后另做逐页目录、表图与文字对应。机器查询只消费这份真实性状态，不自动提升古籍`verified`或算法验证状态。

本报告未增加或修改任何原文、inventory、规则、案例或他人注解；只提交本报告与source-quality状态文件。全库语义加工完成度另由工程总报告统计，不能拿此处“有正文”替代。
