# 无法锚定的规则

定位不到原文或不支持结论的规则保持 `anchor: null`。无锚点是安全降级；错锚点不可接受。

共 462 条（P6 计数；P7 恢复 33 条误杀，另将 `LIURENMIBEN-020` 降级，并撤回误列的 `LZ`，未重扫全表）。P10：`qimen-dunjia-tongzhi` 24 条在「奇门四十格」有唯一整行，已重锚并从下表移除；`qimen-faqiao` 2 条仍不碰。

| book | rule_id | reason | quote 摘录 |
|---|---|---|---|
| `physiognomy/liuzhuang-xiangfa` | `LZ` | quote 是 source_base 元数据，P7 恢复名单误列，已撤回 | source_base: CTP《柳庄相法》Wiki 文本页抽取… |
| `san-shi/liuren-miben` | `LIURENMIBEN-020` | P7：CTP 出处声明（`>` 辑录行），非正文断辞 | > 清·金正音 辑录。CTP URN：ctp:wb348173… |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-009` | 对应度<0.15，引文不能支持结论 | 五阳皆阳丙为最，五阴皆阴癸为至。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-DR-02` | 对应度<0.15，引文不能支持结论 | 合有宜不宜，合多不为奇。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-014` | quote not locatable or previously unanchored | 命局之精（资源充足）、气（流通无阻）、神（光彩外显）三者饱满者为贵。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-022` | 对应度<0.15，引文不能支持结论 | 伤官见官果难辨，可见不可见。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-030` | 对应度<0.15，引文不能支持结论 | 任氏曰：众寡之说，强弱之意也，须分日主四柱两端而论也。 |
| `bazi/ditiansui-chanwei` | `DR-05` | 对应度<0.15，引文不能支持结论 | 夫妻因缘宿世来，喜神有意傍天财。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-DR-05` | 对应度<0.15，引文不能支持结论 | 官杀混杂来问我，有可有不可。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-038` | 对应度<0.15，引文不能支持结论 | 论夫论子要安样，气静平和妇道章，三奇二德虚好语，咸池驿马半推详。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-039` | 对应度<0.15，引文不能支持结论 | 论财论杀论精神，四柱和平易养成，气势攸长无削丧，杀关虽有不伤身。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-045` | 对应度<0.15，引文不能支持结论 | 五阳皆阳丙为最，五阴皆阴癸为至。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-047` | 对应度<0.15，引文不能支持结论 | 一出门来只见儿，吾儿成气构门闾：从儿不管身强弱，只要吾儿又得儿。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-048` | 对应度<0.15，引文不能支持结论 | 君不可抗也。贵乎损上以益下。 |
| `bazi/ditiansui-chanwei` | `DR-07` | 对应度<0.15，引文不能支持结论 | 五气不戾，性情中和；浊乱偏枯，性情乖逆。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-DR-07` | 对应度<0.15，引文不能支持结论 | 大忌四柱缺陷，五行偏枯。 |
| `bazi/ditiansui-chanwei` | `DITIANSUICHA-052` | 对应度<0.15，引文不能支持结论 | 造化起于元，亦止于贞。再肇贞元之会，胚胎嗣续之机。 |
| `bazi/mingli-yueyan` | `MLY-R001` | quote not locatable or previously unanchored | 命局先以日干对月令、透干、藏干、全局势力定格，再论扶抑。 |
| `bazi/mingli-yueyan` | `MLY-R002` | quote not locatable or previously unanchored | 月支本气透干可直接取格；本气不透或遭克，才转取藏干或别干势旺者。 |
| `bazi/mingli-yueyan` | `MLY-R003` | quote not locatable or previously unanchored | 禄刃比劫不独立取格，只作为日干助力。 |
| `bazi/mingli-yueyan` | `MLY-R004` | 对应度<0.15，引文不能支持结论 | 偏财赋/食神赋/伤官赋-卷二-命理约言-陈素庵(清) |
| `bazi/mingli-yueyan` | `MLY-R005` | quote not locatable or previously unanchored | - raw_file: sources/raw/bazi/mingli-yueyan/suanzhun_book_916.html |
| `bazi/mingli-yueyan` | `MLY-R006` | 对应度<0.15，引文不能支持结论 | 看正偏印法/看偏正财法-卷一-命理约言-陈素庵(清) |
| `bazi/mingli-yueyan` | `MLY-R007` | 对应度<0.15，引文不能支持结论 | 看食神法/看伤官法-卷一-命理约言-陈素庵(清) |
| `bazi/mingli-yueyan` | `MLY-R008` | 对应度<0.15，引文不能支持结论 | 看比劫禄刃法/拱夹法-卷一-命理约言-陈素庵(清) |
| `bazi/qiongtong-baojian` | `QIONGTONGBAO-QR` | 对应度<0.15，引文不能支持结论 | 木性腾上而无所止，气重则欲金任使，有金则有惟高惟敛之德。 |
| `bazi/qiongtong-baojian` | `QIONGTONGBAO-014` | 对应度<0.15，引文不能支持结论 | 炎炎真火，位镇南方，故火无不明之理，辉光不久。全要伏藏，故明无不灭之象。火以木为体。无木、则火不长焰。火以水为用，无水、则火太酷烈。故火多则不实，火烈则伤物。木 |
| `bazi/qiongtong-baojian` | `QR-02-08` | quote not locatable or previously unanchored | 冬丁寒弱，专用甲木生身、庚金劈甲、戊土制水；甲庚戊三透不悖者贵。 |
| `bazi/qiongtong-baojian` | `QIONGTONGBAO-034` | quote not locatable or previously unanchored | 04 论金（行论 + 庚辛金 × 四季） |
| `bazi/qiongtong-baojian` | `QR-04-00` | quote not locatable or previously unanchored | 金性沉重、主义、性刚；春金犹寒，宜火气以舒之；夏金尤柔，宜土厚以扶之；秋金当权，喜火炼以成器；冬金寒甚，喜火暖以解冻。 |
| `bazi/qiongtong-baojian` | `QR-05-00` | quote not locatable or previously unanchored | 水主智、性聪，至清而柔；春水泛滥，宜土堤之；夏水涸竭，宜金生之；秋水通源，喜水之归；冬水冻凝，喜火之暖。 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-003` | 对应度<0.15，引文不能支持结论 | 甲子金〔為寶物喜金木旺地進神喜福星平頭懸針破字〕 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-008` | quote not locatable or previously unanchored | 当令者旺、所生者相、生我者休、克我者囚、我克者死；命局以日干在月令的状态定基本旺衰。 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-014` | quote not locatable or previously unanchored | 子丑合土、寅亥合木、卯戌合火、辰酉合金、巳申合水、午未合（土火）。 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-018` | 对应度<0.15，引文不能支持结论 | 正月節   二月節   三月節 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-019` | 对应度<0.15，引文不能支持结论 | 子為墨池子在正北方屬水色象墨故有墨池之象凡命逢子年生者時喜見癸亥謂之水歸大海又謂之雙魚逰墨必為文章士矣 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-027` | 对应度<0.15，引文不能支持结论 | 時歸日祿生平不喜官星 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-033` | quote not locatable or previously unanchored | 神煞篇"正印"取法以日干查地支（甲见子、乙见亥等）；主印信文书之吉。 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-034` | 对应度<0.15，引文不能支持结论 | 論運者以月支為首分四時而提起五行消長 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-035` | 对应度<0.15，引文不能支持结论 | 〔屬毛頭星一名大耗〕 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-039` | quote not locatable or previously unanchored | 勾煞、绞煞取法以年支日支查（子见卯、丑见辰等）；主口舌是非、牵连纠缠。 |
| `bazi/sanming-tonghui` | `R-05` | quote not locatable or previously unanchored | 印为护身、食为养命、官为约束、财为资助；十神四类之本义。 |
| `bazi/sanming-tonghui` | `R-06` | 对应度<0.15，引文不能支持结论 | 年傷日干名為本主不和 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-055` | quote not locatable or previously unanchored | 财星旺而生官者，官星稳固；身、财、官三停为格高。 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-059` | 对应度<0.15，引文不能支持结论 | 〔濕木不生無{{SKchar\|3303}}火理固然也乙卯癸卯尤甚丅卯庶幾〕 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-R-07` | quote not locatable or previously unanchored | 甲乙肝胆、丙丁心小肠、戊己脾胃、庚辛肺大肠、壬癸肾膀胱；五行偏枯有相应脏腑病。 |
| `bazi/sanming-tonghui` | `R-08` | quote not locatable or previously unanchored | 卷八载六甲/六乙/六丙/六丁/六戊各12时辰共60条日时断语。核心原则：时柱为归宿，时辰与日干配合决定晚年格局倾向；日时断为古法断语索引，每条以日干+时支的组合 |
| `bazi/sanming-tonghui` | `SANMINGTONGH-101` | 对应度<0.15，引文不能支持结论 | 六甲年〔丁卯〕月〔乙未〕日〔戊寅〕時   六乙年〔己卯〕月〔甲戌〕日〔乙亥〕時六丙年〔庚寅〕月〔丁巳〕日〔丙午〕時   六丁年〔丙午〕月〔壬辰〕日〔丁未〕時六戊 |
| `bazi/shenfeng-tongkao` | `SF` | quote not locatable or previously unanchored | R01 先辨张楠批判对象 |
| `bazi/shenfeng-tongkao` | `SHENFENGTONG-SF` | quote not locatable or previously unanchored | R02 病药法是核心路由 |
| `bazi/shenfeng-tongkao` | `SHENFENGTONG-003` | quote not locatable or previously unanchored | R03 动静与盖头用于透藏和作用层级 |
| `bazi/shenfeng-tongkao` | `SHENFENGTONG-004` | quote not locatable or previously unanchored | R04 格局断语要与强弱任受同看 |
| `bazi/shenfeng-tongkao` | `SHENFENGTONG-005` | pack meta-rule, no original sentence | R05 高风险断语必须安全改写 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-006` | quote not locatable or previously unanchored | 当令者旺、所生者相、生我者休、克我者囚、我克者死。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-007` | 对应度<0.15，引文不能支持结论 | 立春念三丙火用，餘日甲木旺提纲。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-008` | 对应度<0.15，引文不能支持结论 | 假令月令有用神，得父母力。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-009` | quote not locatable or previously unanchored | 刑冲合害优先级：合 > 冲 > 刑 > 害（经验总论，非绝对规则）。 |
| `bazi/yuanhai-ziping` | `YR-02` | 对应度<0.15，引文不能支持结论 | 人稟天地，命属阴阳，生居覆载之内，尽在五行之中。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-012` | 对应度<0.15，引文不能支持结论 | 年根為本，月令為中。日生百刻，時旺時空。日主要強，月提得令。用物為財，表實為正。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-014` | 对应度<0.15，引文不能支持结论 | 杂气财官，刑冲则发。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-015` | quote not locatable or previously unanchored | 正官七煞同现为混杂，需去留得宜（去官留煞或去煞留官）。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-017` | 对应度<0.15，引文不能支持结论 | 假令月令有用神，得父母力。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-018` | quote not locatable or previously unanchored | 天干五合化气需化神当令、有根、不被冲克方真化。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-019` | 对应度<0.15，引文不能支持结论 | 假令月令有用神，得父母力。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-020` | quote not locatable or previously unanchored | 用神为命局所需之神；本书已有取用意识但框架尚不严格。 |
| `bazi/yuanhai-ziping` | `YR-03` | 对应度<0.15，引文不能支持结论 | 夫大运者，以天干曰『五运』，地支曰『六气』，故名『范气』。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-026` | quote not locatable or previously unanchored | 格局清纯有用为贵；格局破败无用为贱；身财两停为富；身弱财多为穷。 |
| `bazi/yuanhai-ziping` | `YR-04` | quote not locatable or previously unanchored | 神煞作事项辅证，不主格局；与十神/格局冲突时以格局为主。 |
| `bazi/yuanhai-ziping` | `YR-05` | quote not locatable or previously unanchored | 造化元钥赋文总论命理哲学；五行配合为人命之钥。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-YR-05` | quote not locatable or previously unanchored | 刑冲的补充辨析：冲喜用为凶、冲忌神为吉；刑入命未必凶。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-032` | quote not locatable or previously unanchored | 干支配脏腑（甲乙肝胆、丙丁心小肠、戊己脾胃、庚辛肺大肠、壬癸肾膀胱）；五行偏枯对应脏腑有体质倾向。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-033` | 对应度<0.15，引文不能支持结论 | 夫大运者，以天干曰『五运』，地支曰『六气』，故名『范气』。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-YR-04` | 对应度<0.15，引文不能支持结论 | 十惡大敗，格中不忌。若會財官，反成富貴。格局推詳，以殺為重。制煞為權，何愁損用。 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-037` | 对应度<0.15，引文不能支持结论 | 金玉赋》 |
| `bazi/yuanhai-ziping` | `YUANHAIZIPIN-038` | quote not locatable or previously unanchored | 年柱起官的古法；以年柱为起点取官。 |
| `bazi/ziping-zhenquan` | `ZPR-03` | 对应度<0.15，引文不能支持结论 | 用神專求月令，然以四柱配之，必有成敗。 |
| `bazi/ziping-zhenquan` | `ZPR-12` | 对应度<0.15，引文不能支持结论 | 論運與看命，無二法也。看命以四柱干支，配月令之喜忌。而取運則又以運之干支，配八字之喜忌。故運中每運行一字，即必以此一字，配命中八字而統觀之，爲喜爲忌，吉凶判然矣 |
| `bazi/ziping-zhenquan` | `ZPR-14` | 扩行后对应度仍<0.15 | 官以尅身，雖與【校：「與」原作「六」，據中州本改】七煞有別，終受彼制，何以切忌刑沖破害，尊之若是乎？豈知人生天地間【校：「間」字據中州本補】，必無矯焉自尊之理， |
| `bazi/ziping-zhenquan` | `ZPR-15` | 对应度<0.15，引文不能支持结论 | 煞以攻身，似非美物，而大貴之格，多存七煞。蓋控制得宜，煞爲我用，如大英雄大豪傑，似難駕馭，而處之有方，則驚天動地之功，忽焉而就。此王侯將相所以多存七煞也。 |
| `bazi/ziping-zhenquan` | `ZPR-16` | 对应度<0.15，引文不能支持结论 | 雜格者，月令無用，取外格而用之，其格甚多，故謂之雜。 |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-BSZZ` | quote not locatable or previously unanchored | R01 六爻必须先装卦 |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-003` | quote not locatable or previously unanchored | R02 先定用神，再看原忌仇 |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-004` | quote not locatable or previously unanchored | R03 世应定义主客边界 |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-005` | quote not locatable or previously unanchored | R04 飞伏神处理“用神不上卦” |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-006` | pack meta-rule, no original sentence | R05 与《增删卜易》并读 |
| `divination/bushi-zhengzong` | `BUSHIZHENGZO-007` | pack meta-rule, no original sentence | R06 高风险断语安全改写 |
| `divination/huangji-jingshi` | `HR-01` | quote not locatable or previously unanchored | 一元 = 12 会 = 360 运 = 4320 世 = 129600 年；为天地一开辟之大周期。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-HR-01` | quote not locatable or previously unanchored | 皇極經世書卷五上    宋 邵雍 撰 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-003` | quote not locatable or previously unanchored | 皇極經世書卷六下    宋 邵雍 撰觀物篇三十四  以運經世十 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-004` | quote not locatable or previously unanchored | 一元 12 会以 12 地支配；子开寅生午盛申退戌闭亥归；现今天地正处于"午会"中后期。 |
| `divination/huangji-jingshi` | `HR-02` | quote not locatable or previously unanchored | 以六十四卦配岁；卦气消息按月配中孚 / 复 / 临 / 泰……剥 / 坤；亦按经世配元会运世。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-HR-02` | quote not locatable or previously unanchored | 经世卦序以乾坤为始、咸恒为人事之序；与《周易》上下经卦序有结构相通。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-007` | quote not locatable or previously unanchored | 本书不涉个人卜筮取用神；元会运世为时间数理框架，非占断系统。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-011` | quote not locatable or previously unanchored | 六十四卦两两为偶（反对）；非反即对；卦序之理本于此。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-HR-05` | 对应度<0.15，引文不能支持结论 | 太極道之極也太𤣥道之𤣥也太素色之本也太一數之始也太初事之初也其成功則一也 |
| `divination/huangji-jingshi` | `HR-06` | 对应度<0.15，引文不能支持结论 | 剛少剛之用數是謂水火土石之化數日月星辰之變數一萬七千二十四謂之動數水火土石之化數一萬七千二十四謂之植數再唱和日月星辰水火土石之變化通數二萬八千九百八十一萬六千五 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-HR-09` | 对应度<0.15，引文不能支持结论 | 經辰之申二千一百五十七 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-020` | quote not locatable or previously unanchored | 本书数理框架虽含史观，但邵雍未明言"国运"预测；后世以此预言朝代兴衰多属附会。 |
| `divination/huangji-jingshi` | `HUANGJIJINGS-021` | quote not locatable or previously unanchored | 本书是宇宙史观数理，非个人命术；不可用本书直接推个人吉凶。 |
| `divination/huangjin-ce` | `HJC-R003` | 对应度<0.15，引文不能支持结论 | 世為己，應為人，大宜契合。動為始，變為終，最怕交爭。 |
| `divination/huangjin-ce` | `HJC-R006` | 对应度<0.15，引文不能支持结论 | 虎興而遇吉神，不害其為吉。龍動而逢凶曜，難掩其為凶。 |
| `divination/huangjin-ce` | `HJC-R007` | 对应度<0.15，引文不能支持结论 | 應乃太虛，逢空則雨晴難擬。世為大塊，受剋則天變非常。 |
| `divination/huangjin-ce` | `HJC-R008` | 对应度<0.15，引文不能支持结论 | 陰陽交錯，難期琴瑟之和鳴；內外互搖，定見家庭之撓括。 |
| `divination/huangjin-ce` | `HJC-R009` | 对应度<0.15，引文不能支持结论 | 要問吉凶，但看財福。 |
| `divination/huangjin-ce` | `HJC-R010` | 对应度<0.15，引文不能支持结论 | 兄如太過，反不剋財；身或兄臨，必難求望。 |
| `divination/huangjin-ce` | `HJC-R017` | 对应度<0.15，引文不能支持结论 | 人孰無常，疾病無常，事孰為大，死生為大。 |
| `divination/huozhu-lin` | `HZL` | 对应度<0.15，引文不能支持结论 | 旁爻持世，旺相得地； |
| `divination/huozhu-lin` | `HZL-R001` | 对应度<0.15，引文不能支持结论 | 阴阳男女，次策推排； |
| `divination/huozhu-lin` | `HZL-R002` | 对应度<0.15，引文不能支持结论 | 财官异路，可辨五乡； |
| `divination/huozhu-lin` | `HZL-R003` | 对应度<0.15，引文不能支持结论 | 独发易取，乱动难寻； |
| `divination/meihua-yishu` | `MEIHUAYISHU-003` | quote not locatable or previously unanchored | 乾兑属金、坤艮属土、震巽属木、坎属水、离属火。 |
| `divination/meihua-yishu` | `MR-03` | 对应度<0.15，引文不能支持结论 | 有客問曰：「今日動靜如何？ |
| `divination/meihua-yishu` | `MEIHUAYISHU-MR-07` | 对应度<0.15，引文不能支持结论 | 天下之事有吉凶，托占以明其機。 |
| `divination/zengshan-buyi` | `ZR` | quote not locatable or previously unanchored | 原文保存兑为泽初、上爻动而变天水讼的完整成卦实例，只用于核对 provider 的起卦结果。 |
| `divination/zengshan-buyi` | `ZR-02` | 对应度<0.15，引文不能支持结论 | 納天干地支總領： |
| `divination/zengshan-buyi` | `ZR-03` | 对应度<0.15，引文不能支持结论 | 卜筮被許多人斥為迷信行為。 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-012` | 对应度<0.15，引文不能支持结论 | 楚江李坦我平鑑定 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-013` | 对应度<0.15，引文不能支持结论 | 用財者﹐財爻旺相﹐卽許婚。 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-014` | 对应度<0.15，引文不能支持结论 | 楚江李坦我平鑑定 |
| `divination/zengshan-buyi` | `ZR-07` | 对应度<0.15，引文不能支持结论 | 楚江李坦我平鑑定 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-ZR-07` | 对应度<0.15，引文不能支持结论 | 楚江李坦我平鑑定 |
| `divination/zengshan-buyi` | `ZR-08` | 对应度<0.15，引文不能支持结论 | 楚江李坦我平鑑定 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-028` | quote not locatable or previously unanchored | 用神长生之地、帝旺之地、墓绝之地皆为应期取义点。 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-029` | 对应度<0.15，引文不能支持结论 | 官鬼雷霆霧電。官鬼乃父母之元神﹐動則生父﹐故主霧霆雷電。或應雷霆﹐不拘春夏秋冬﹐可執以爲雷霆霧電看是也。 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-031` | 短句无句读，无法扩成原文整行 | 隨鬼入墓章第三十 |
| `divination/zengshan-buyi` | `ZENGSHANBUYI-ZR-10` | 对应度<0.15，引文不能支持结论 | 父母爲雨雪霧霜﹐發則八方潤澤。 |
| `divination/zhouyi-zhezhong` | `ZZR` | 对应度<0.15，引文不能支持结论 | 乾坤剥復〔大過〕頤姤夬 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-ZZR-01` | quote not locatable or previously unanchored | 二爻居下卦中、五爻居上卦中；得中位者多吉，所谓"刚中"（阳爻居中）或"柔中"（阴爻居中）。 |
| `divination/zhouyi-zhezhong` | `ZZR-02` | quote not locatable or previously unanchored | 每卦象征一时；解卦先识卦时（屯之难、需之待、否之闭、泰之通）。 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-012` | quote not locatable or previously unanchored | 64 卦皆有错卦（六爻全反）；错卦之义为本卦之背面（乾错坤、屯错鼎）。 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-ZZR-04` | quote not locatable or previously unanchored | 形而上者谓之道、形而下者谓之器；易兼道器，不可偏执。 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-017` | quote not locatable or previously unanchored | 君子见几而作；知微之始者，可应万变。 |
| `divination/zhouyi-zhezhong` | `ZZR-05` | quote not locatable or previously unanchored | 64 卦相次有理；后卦由前卦之必然演化（屯生于乾坤、蒙次于屯）。 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-025` | quote not locatable or previously unanchored | 揲蓍得 9（老阳 / 重）、6（老阴 / 交）为动爻；7（少阳 / 单）、8（少阴 / 拆）为静爻。 |
| `divination/zhouyi-zhezhong` | `ZHOUYIZHEZHO-030` | quote not locatable or previously unanchored | 本书重宋学义理而旁取汉学象数；不取魏伯阳 / 京房等纳甲飞伏之纯象数。 |
| `fengshui/dili-bianzheng` | `DLBZ` | quote not locatable or previously unanchored | R01 经文与蒋注必须分层 |
| `fengshui/dili-bianzheng` | `DILIBIANZHEN-DLBZ` | quote not locatable or previously unanchored | R02 雌雄优先于简单阴阳 |
| `fengshui/dili-bianzheng` | `DILIBIANZHEN-003` | quote not locatable or previously unanchored | R03 理气问题需要工具，不让 LLM 手算 |
| `fengshui/dili-bianzheng` | `DILIBIANZHEN-004` | quote not locatable or previously unanchored | R04 与形势法冲突时并列 |
| `fengshui/dili-bianzheng` | `DILIBIANZHEN-005` | quote not locatable or previously unanchored | R05 辨伪段落用于冲突裁判 |
| `fengshui/dutian-baozhao-jing` | `DTR-01` | 对应度<0.15，引文不能支持结论 | 楊公妙應不多言.實實作家傳.人生禍福由天定.賢達能安命. |
| `fengshui/dutian-baozhao-jing` | `DTR-04` | 对应度<0.15，引文不能支持结论 | 子字出脈子字尋.莫教差錯丑與壬.莫是陽差與陰錯.勸君不必費心尋. |
| `fengshui/hanlong-jing` | `HANLONGJING-R-06` | quote not locatable or previously unanchored | 禄存九形：顿鼓、覆釜、鹤爪、肋扇、悬鹑、平洋、长蛇、兠鍪、落花；各形主作不同（神坛、关锁、罗星等）。 |
| `fengshui/hanlong-jing` | `HANLONGJING-R-07` | quote not locatable or previously unanchored | 文曲蛇行、撒网为淫邪；若无星峰为辅则散漫不结；男主酒色、女主内乱（古文措辞）。 |
| `fengshui/huangdi-zhaijing` | `HDZJ-R002` | 对应度<0.15，引文不能支持结论 | 夫宅者乃是隂陽之樞紐人倫之軌模非夫博物明賢而能悟斯道也就此五種其最要者唯有宅法而真秘術凡人所居無不在宅雖只大小不等隂陽有殊縱然客居一室之中亦有善惡大者大説小者小 |
| `fengshui/qingnang-aoyu` | `QNA-R002` | 对应度<0.15，引文不能支持结论 | 左為陽, 子癸至亥壬, 右為陰, 午丁至巳丙, |
| `fengshui/qingnang-aoyu` | `QNA-R005` | 短句无句读，无法扩成原文整行 | 向放水, 生旺有吉休囚否. |
| `fengshui/qingnang-aoyu` | `QNA-R008` | 对应度<0.15，引文不能支持结论 | 勸君再把星辰辨, 吉凶禍福如神現; |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-01` | 短句无句读，无法扩成原文整行 | 乾坤二卦為母， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-02` | 短句无句读，无法扩成原文整行 | 震巽離坤兌乾坎艮者， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-03` | 短句无句读，无法扩成原文整行 | 戴九履一， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-04` | 短句无句读，无法扩成原文整行 | 而在於陰， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-09` | 对应度<0.15，引文不能支持结论 | 以五星之正變審象也， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-10` | 短句无句读，无法扩成原文整行 | 謹歲時以扶地理之橐籥， |
| `fengshui/qingnang-jing` | `QINGNANGJING-R-11` | 短句无句读，无法扩成原文整行 | 各一物全具一天地之理， |
| `fengshui/rudi-yan-quanshu` | `RDY-R001` | 对应度<0.15，引文不能支持结论 | 一、是書自宋迄今，巨族大家抄寫成帙，秘之已久。或前後失次，或散軼事不全，愚不揣固陋，留心匯正，歷數寒暑，方成全集。至間有欠雅馴處，字字坦然明白，故不敢妄為刪易。 |
| `fengshui/rudi-yan-quanshu` | `RDY-R002` | 对应度<0.15，引文不能支持结论 | 入地眼全書龍法卷二 |
| `fengshui/rudi-yan-quanshu` | `RDY-R003` | 对应度<0.15，引文不能支持结论 | 入地眼全書龍法卷二 |
| `fengshui/rudi-yan-quanshu` | `RDY-R004` | 对应度<0.15，引文不能支持结论 | 入地眼全書水法卷六 |
| `fengshui/rudi-yan-quanshu` | `RDY-R006` | 对应度<0.15，引文不能支持结论 | 入地眼全書天星卷一 |
| `fengshui/rudi-yan-quanshu` | `RDY-R007` | 短句无句读，无法扩成原文整行 | 入地眼全書陽宅卷十 |
| `fengshui/shenshi-xuankong-xue` | `XK` | 对应度<0.15，引文不能支持结论 | 余以葬事，涉猎地理诸书，觉其说庞杂，有歧之又歧之慨！及读《沈氏玄空学》，江迂生太史《序》曰：“峦头征实，古今无伪书；理气课虚，古今多伪诀。”信哉斯言！然后知余向 |
| `fengshui/shenshi-xuankong-xue` | `SHENSHIXUANK-003` | 对应度<0.15，引文不能支持结论 | 向上有破屋并水，开巽方门，前有三叉水口，兑方有水至巽方门前聚消。 |
| `fengshui/shenshi-xuankong-xue` | `SHENSHIXUANK-004` | 对应度<0.15，引文不能支持结论 | 下诀：“一坎、二坤、三震、四巽、五中、六乾、七兑、八艮、九离。”一为壬子癸，二为未坤申，三为甲卯乙，四为辰巽巳，五为戊己，六为戌乾亥，七为庚酉辛，八为丑艮寅，九 |
| `fengshui/shenshi-xuankong-xue` | `SHENSHIXUANK-005` | quote not locatable or previously unanchored | 《沈氏玄空学》是近代玄空解释层，应与《地理辨正》《天玉经》《青囊》系原典分层读取。 |
| `fengshui/tianyu-jing` | `TYR-01` | 对应度<0.15，引文不能支持结论 | 江東一勢從來吉，八神四個一。 |
| `fengshui/tianyu-jing` | `TYR-02` | 对应度<0.15，引文不能支持结论 | 天卦江東掌上尋，知了值千金。 |
| `fengshui/tianyu-jing` | `TYR-08` | 对应度<0.15，引文不能支持结论 | 惟有挨星不最貴，泄漏天機秘。天機若然安在內，家活常富貴。天機若然安在外，家活漸退敗。五星配出九星名，天下任橫行。 |
| `fengshui/xuexin-fu` | `XXF` | 对应度<0.15，引文不能支持结论 | 城上星峰卓卓，真如插戟護垣；面前墩阜累累，喚作排衙唱喏。 |
| `fengshui/xuexin-fu` | `XUEXINFU-XXF` | 对应度<0.15，引文不能支持结论 | 類以聚；是以潛藏須細察，來止要詳明。 |
| `fengshui/xuexin-fu` | `XUEXINFU-004` | quote not locatable or previously unanchored | R04 水法重交鎖織結與避穿割箭射 |
| `fengshui/xuexin-fu` | `XUEXINFU-005` | quote not locatable or previously unanchored | R05 本書是形勢層，不處理羅盤理氣計算 |
| `fengshui/yangzhai-sanyao` | `YZS-R004` | 短句无句读，无法扩成原文整行 | 巽天五六祸生绝延 |
| `fengshui/yangzhai-sanyao` | `YZS-R005` | 短句无句读，无法扩成原文整行 | 西四宅   延年上大吉 |
| `fengshui/yangzhai-sanyao` | `YZS-R006` | 对应度<0.15，引文不能支持结论 | （生炁）  贪狼家道隆   五子更英雄   文艺多端立   精专百事通   （长房更大利） |
| `fengshui/yangzhai-sanyao` | `YZS-R007` | 对应度<0.15，引文不能支持结论 | 布八卦分二十四山、向，看系某主、某门、某 |
| `fengshui/yangzhai-shishu` | `YANGZHAISHIS-YZS-R001` | 对应度<0.15，引文不能支持结论 | 人之居處，宜以大地山河為主，其來脈氣勢最大，關 |
| `fengshui/yangzhai-shishu` | `YANGZHAISHIS-YZS-R004` | 对应度<0.15，引文不能支持结论 | 福元者何，即福德宮是也。古人隱祕此訣，謂之「伏位。」 |
| `fengshui/yangzhai-shishu` | `YANGZHAISHIS-YZS-R005` | 对应度<0.15，引文不能支持结论 | 東四位宅圖說并東四位生人用例 |
| `fengshui/yangzhai-shishu` | `YANGZHAISHIS-YZS-R007` | 对应度<0.15，引文不能支持结论 | 生者，生氣星，貪狼星也　　　，一木 |
| `fengshui/yangzhai-shishu` | `YZS-R009` | 对应度<0.15，引文不能支持结论 | 震坎方高大，皆為富貴之利宅。 |
| `fengshui/yangzhai-shishu` | `YZS-R010` | 对应度<0.15，引文不能支持结论 | 論開門修造門第六 |
| `fengshui/yangzhai-shishu` | `YZS-R011` | 对应度<0.15，引文不能支持结论 | 十墳，不與人家修一門。」故論開門修造門第六， |
| `fengshui/yangzhai-shishu` | `YZS-R014` | 对应度<0.15，引文不能支持结论 | 《宅法》多端，無一可略。宅內房屋，如龜頭雁尾，披孝之 |
| `fengshui/yangzhai-shishu` | `YZS-R015` | 对应度<0.15，引文不能支持结论 | ===論選擇第九 |
| `fengshui/yangzhai-shishu` | `YZS-R016` | 对应度<0.15，引文不能支持结论 | 逐日太陰過宮定局 |
| `fengshui/yangzhai-shishu` | `YZS-R017` | 对应度<0.15，引文不能支持结论 | 修宅造門，非甚有力之家，難以卒辦。縱有力者，非遲 |
| `fengshui/yangzhai-shishu` | `YZS-R018` | 对应度<0.15，引文不能支持结论 | 王子既輯《陽宅十書》成，客有質者曰：「亦有宅法吉 |
| `fengshui/yilong-jing` | `YILONGJING-R-01` | 对应度<0.15，引文不能支持结论 | 幹龍長遠去無窮。 |
| `fengshui/yilong-jing` | `YILONGJING-R-13` | quote not locatable or previously unanchored | 长震、中坎、少艮（男）；长巽、中离、少兑（女）。后世执河图三元九宫：长震四七、中离二五八、少兑三六九。 |
| `fengshui/yilong-jing` | `R-18` | 对应度<0.15，引文不能支持结论 | 幹頭未作枝先興，枝上未作幹先榮。 |
| `fengshui/zangfa-daozhang` | `ZFD-R005` | 对应度<0.15，引文不能支持结论 | 理法少差，天淵懸隔 |
| `fengshui/zangfa-daozhang` | `ZFD-R008` | 扩行后对应度仍<0.15 | 來龍急氣，脈直沖中，無乳氣穴粘右邊，側受倚其後，托左臂長而明堂寬展，如人之擔傘勢也。宜淺開金井，若太深必傷，宜培加客土，填實於塋，必主富貴綿遠。 |
| `fengshui/zangfa-daozhang` | `ZFD-R009` | 扩行后对应度仍<0.15 | 天地玄機，由人幹運，須憑目巧，總在心靈。 |
| `fengshui/zangfa-daozhang` | `ZFD-R010` | 扩行后对应度仍<0.15 | 脈甚急就龍虛粘曰離，有如懸筆之垂珠滴者，謂之脫煞穴、拋穴、接穴、大陽影光穴，懸棺長鬣封是也。如龍雄勢猛，卸落平洋，結成盤珠，鋪氈展席，遙對來脈，壘土浮□，高大為 |
| `fengshui/zangshu` | `ZANGSHU-R-01` | quote not locatable or previously unanchored | 葬地必须乘地中流行之生气，使遗骨与生气相合方能荫子孙；离生气则葬法不立。 |
| `luming-nayin/lantai-miaoxuan` | `LT` | quote not locatable or previously unanchored | M01 三命事实框架 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-LT` | quote not locatable or previously unanchored | R01 三命与六旬为底层框架 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-003` | quote not locatable or previously unanchored | R02 根基与格局必须同看 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-004` | quote not locatable or previously unanchored | R03 凶煞有制可反成光荣 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-005` | quote not locatable or previously unanchored | R04 纳音地支取象形成格名 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-006` | pack meta-rule, no original sentence | section_note: 專論惡煞、疾病，夭折、貧愚之類 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-007` | quote not locatable or previously unanchored | R06 得时/失时改变同一象格的解释 |
| `luming-nayin/lantai-miaoxuan` | `LANTAIMIAOXU-008` | quote not locatable or previously unanchored | R07 与子平体系冲突时分层并列 |
| `luming-nayin/li-xuzhong-mingshu` | `LIXUZHONGMIN-072` | quote not locatable or previously unanchored | 水智、木仁、火礼、土信、金义；十二位之全。 |
| `luming-nayin/luoluzi-sanming` | `LZ-04-01` | quote not locatable or previously unanchored | 五合正合贵命 |
| `luming-nayin/luoluzi-sanming` | `LZ-04-02` | quote not locatable or previously unanchored | 偏阴偏阳为疾 |
| `luming-nayin/luoluzi-sanming` | `LZ-06-01` | quote not locatable or previously unanchored | 夹禄正贵 |
| `luming-nayin/luoluzi-sanming` | `LZ-06-02` | quote not locatable or previously unanchored | 夹禄不实虚名 |
| `luming-nayin/luoluzi-sanming` | `LZ-07-02` | quote not locatable or previously unanchored | 天罗地网 |
| `luming-nayin/luoluzi-sanming` | `LZ-07-03` | quote not locatable or previously unanchored | 伏吟反吟 |
| `luming-nayin/luoluzi-sanming` | `LZ-07-05` | quote not locatable or previously unanchored | 勾绞元亡狂横 |
| `luming-nayin/luoluzi-sanming` | `LZ-07-06` | quote not locatable or previously unanchored | 宅墓丧吊 |
| `luming-nayin/luoluzi-sanming` | `LZ-08-01` | quote not locatable or previously unanchored | 阴男阳女出入元辰 |
| `luming-nayin/luoluzi-sanming` | `LZ-08-03` | quote not locatable or previously unanchored | 否泰交居小运起例 |
| `luming-nayin/luoluzi-sanming` | `LZ-08-05` | quote not locatable or previously unanchored | 祿馬不三台而八座 |
| `luming-nayin/luoluzi-sanming` | `LZ-08-06` | quote not locatable or previously unanchored | 父病推子禄、妻灾课夫年 |
| `luming-nayin/wuxing-jingji` | `WX-01-02` | quote not locatable or previously unanchored | 纳音胜真五行 |
| `luming-nayin/wuxing-jingji` | `WX-03-01` | 对应度<0.15，引文不能支持结论 | 亥子(水)寅卯(木)巳午(火)申酉(金)辰戍醜未(土) |
| `luming-nayin/wuxing-jingji` | `WX-04-01` | quote not locatable or previously unanchored | 五位起例 |
| `luming-nayin/wuxing-jingji` | `WX-04-02` | 短句无句读，无法扩成原文整行 | 釋日時貴格 |
| `luming-nayin/wuxing-jingji` | `WX-04-03` | 对应度<0.15，引文不能支持结论 | 甲子日丁卯时甲戌时 |
| `luming-nayin/wuxing-jingji` | `WX-04-04` | 短句无句读，无法扩成原文整行 | 立春正月节雨水正月中 |
| `luming-nayin/wuxing-jingji` | `WX-05-01` | 短句无句读，无法扩成原文整行 | 第十四卷論天乙貴神 |
| `luming-nayin/wuxing-jingji` | `WX-05-02` | 短句无句读，无法扩成原文整行 | 第十七卷並論祿馬 |
| `luming-nayin/wuxing-jingji` | `WX-05-05` | 对应度<0.15，引文不能支持结论 | 寅午戌人在戌巳酉醜人在醜申子辰人在辰亥卯未人在未 |
| `luming-nayin/wuxing-jingji` | `WX-06-02` | quote not locatable or previously unanchored | 中下贵之差 |
| `luming-nayin/wuxing-jingji` | `WX-07-01` | quote not locatable or previously unanchored | 劫煞亡神 |
| `luming-nayin/wuxing-jingji` | `WX-07-05` | 对应度<0.15，引文不能支持结论 | 相衝者十二支戰擊之神，大概為兇，然有為福之甚者，凡沖處要相生，如辛巳沖癸亥，即是金生水也，馀依此推之。如同類及相尅者最兇，如壬申金尅庚寅之木，己卯沖己酉之土，皆 |
| `luming-nayin/wuxing-jingji` | `WX-07-06` | quote not locatable or previously unanchored | 阳刃金煞 |
| `luming-nayin/wuxing-jingji` | `WX-10-01` | 短句无句读，无法扩成原文整行 | 乃是一歲奇九月之大運， |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-007` | quote not locatable or previously unanchored | 干支俱合相养则贵；乖违则凶。 |
| `luming-nayin/yuzhao-shenying` | `YZ-03` | quote not locatable or previously unanchored | 功曹（寅）传送（申）+庚甲，主商旅、公吏。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-010` | quote not locatable or previously unanchored | 六合(乙)+太陰(辛)+螣蛇(丁)+从魁(酉)等组合，主官事陰人之扰。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-017` | quote not locatable or previously unanchored | 庚辛申酉金旺多见，原文主军人、孤女、兵刃等象。 |
| `luming-nayin/yuzhao-shenying` | `YZ-04` | quote not locatable or previously unanchored | 智仁清、礼义浊、信从四时；五常对应水木清、火金浊、土因时。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-023` | quote not locatable or previously unanchored | 卯(三光户、陰贼)+子(神后)相刑，主无礼德。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-024` | quote not locatable or previously unanchored | 丑戌未三刑见者，主四肢病。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-025` | quote not locatable or previously unanchored | 卯(陰贼)+辰(天罡)相加，主狱刑或腰脚之患。 |
| `luming-nayin/yuzhao-shenying` | `YZ-07` | quote not locatable or previously unanchored | 兄弟干同辈，相生顺则和睦、相尅逆则交争。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-045` | quote not locatable or previously unanchored | 以胎元、月柱干支推父母年命；干同主父寿、音同主母寿。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-046` | quote not locatable or previously unanchored | 日柱大小定妻年龄、时柱变法定子嗣有无。 |
| `luming-nayin/yuzhao-shenying` | `YUZHAOSHENYI-047` | quote not locatable or previously unanchored | 命局夫旺则妻强，妻旺则夫强，按旺相之气。 |
| `physiognomy/liuzhuang-xiangfa` | `LIUZHUANGXIA-LZ` | quote not locatable or previously unanchored | R02 五官五岳六府是索引体系，不是结论体系 |
| `physiognomy/liuzhuang-xiangfa` | `LIUZHUANGXIA-003` | quote not locatable or previously unanchored | R03 气色与精神类条目不得医学化 |
| `physiognomy/liuzhuang-xiangfa` | `LIUZHUANGXIA-004` | quote not locatable or previously unanchored | R04 儿童、孕产、女性、婚姻条目全部高风险 |
| `physiognomy/liuzhuang-xiangfa` | `LIUZHUANGXIA-005` | quote not locatable or previously unanchored | R05 与《神相全编》互证时分层 |
| `physiognomy/mayi-shenxiang` | `MAYISHENXIAN-MR` | quote not locatable or previously unanchored | 五官、十二宫、十三部位可作为传统相法术语定位框架。 |
| `physiognomy/mayi-shenxiang` | `MAYISHENXIAN-003` | quote not locatable or previously unanchored | 金木水火土形相是传统象数分类，不是现代人格、能力或健康诊断。 |
| `physiognomy/mayi-shenxiang` | `MAYISHENXIAN-004` | 对应度<0.15，引文不能支持结论 | 夫手足者谓之四肢，以象四时，加之以首，谓之五体，以象五行。 |
| `physiognomy/mayi-shenxiang` | `MAYISHENXIAN-005` | 对应度<0.15，引文不能支持结论 | 议论争差识者稀　附于金锁号银匙 |
| `physiognomy/shenxiang-quanbian` | `SR-01` | 对应度<0.15，引文不能支持结论 | 一取威儀，「如虎下山，百獸自驚，如鷹升騰，狐兔自戰。」 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-01` | 对应度<0.15，引文不能支持结论 | 《擇交》在眼。 〈 眼惡者情多薄交之有害然露者無心不可不詳審也 〉 問「貴在眼。」 〈 未有 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-005` | 对应度<0.15，引文不能支持结论 | 第一天中對天嶽，左廂《內府》相隨續。高廣尺陽武庫 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-006` | quote not locatable or previously unanchored | 百岁面部流年图，童限 1-13 在两耳，14-30 在额上，31-50 在中庭，51-70 在下停，71-99 散布。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-009` | quote not locatable or previously unanchored | 上停（额至眉）主早年 / 中停（眉至鼻）主中年 / 下停（鼻至颏）主晚年；三停均匀为相之贵。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-02` | quote not locatable or previously unanchored | 额左颧鼻颏配五岳 / 耳目鼻口配四渎；五岳要朝拱、四渎要清通。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-013` | quote not locatable or previously unanchored | 五星六曜配面部部位；与七政命盘"五星六曜"同名异用，不可换算。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-014` | quote not locatable or previously unanchored | 六府（上中下二二二）+ 三才（天人地）+ 三停（上中下）共构面部立体框架。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-015` | 对应度<0.15，引文不能支持结论 | 下停長，終日區區促壽疆。上停長，下停短，衣食自然 |
| `physiognomy/shenxiang-quanbian` | `SR-03` | 对应度<0.15，引文不能支持结论 | ​ 欽定古今圖書集成博物彙編藝術典 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-03` | 对应度<0.15，引文不能支持结论 | 材，善御其德，又善治其器，善御其馬。小人反是，其氣 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-018` | 对应度<0.15，引文不能支持结论 | 太剛則折，隔山相聞，圓長不缺，斯乃貴人遠見風格。」 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-019` | 对应度<0.15，引文不能支持结论 | 一生清閑。骨格清雅，一生安寧。神清氣和，一生聰慧。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-021` | 对应度<0.15，引文不能支持结论 | 生逆毛主惡亡。此為惡死之相也。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-022` | 对应度<0.15，引文不能支持结论 | 訣曰：「眉高聳秀，威權祿厚。眉毛長垂，高壽無疑。眉毛潤澤，求官易得。眉交不分，早歲歸墳。眉如角弓，性善不雄。眉如初月，聰明超越。重重如絲，貪淫無守。彎彎如蛾，好 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-04` | 对应度<0.15，引文不能支持结论 | 針者，絕子，貧寒。」上有黑子者，多子。下有黑子者多女， |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-026` | 对应度<0.15，引文不能支持结论 | 音》欲清。《口德》欲端。《口脣》欲厚。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-027` | 对应度<0.15，引文不能支持结论 | 夭，廕下須教破且休。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-029` | 对应度<0.15，引文不能支持结论 | 《詩》曰：「齒密方為君子儒，分明小輩齒牙疏。色如白玉 |
| `physiognomy/shenxiang-quanbian` | `SR-05` | 对应度<0.15，引文不能支持结论 | 暴，太緩則遲，周旋不失其節，進退各中其度者，至貴」 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-05` | 对应度<0.15，引文不能支持结论 | 則心曲，故曰「觀其表則知其裡矣。」 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-034` | 对应度<0.15，引文不能支持结论 | 兼卑賤，背陷成坑亦主貧。若是時師依此訣，相中十 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-035` | 对应度<0.15，引文不能支持结论 | 前，此相之人終不貴。鼻大眼小金剋木，一世貧寒主 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-036` | 对应度<0.15，引文不能支持结论 | 「頭面耳鼻口腹」六者，反常而不得其正也。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-037` | 对应度<0.15，引文不能支持结论 | 方，耳雖小堅且圓，額雖小平且正，聲雖小宮且商，面 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-038` | 对应度<0.15，引文不能支持结论 | 來到底貧。鰥寡天羅赤色多，更看兩角旋成螺，語 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-039` | 对应度<0.15，引文不能支持结论 | 中，每與天地相流通。神流如夢如影響，目力觀兮如 |
| `physiognomy/shenxiang-quanbian` | `SR-07` | quote not locatable or previously unanchored | 神眼经专论目相精微；以"神 - 光 - 黑白分明"三层观目。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-07` | 对应度<0.15，引文不能支持结论 | 郎君面，男子郎君命不長。女子郎君好媱慾，僧道孤 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-043` | 对应度<0.15，引文不能支持结论 | 「塵蒙」而身無所資，玉潤而名高先唱。 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-08` | 对应度<0.15，引文不能支持结论 | 善盡美之人；兩眼雌雄，豈由仁由義」之子。色如常變 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-SR-09` | 对应度<0.15，引文不能支持结论 | 巧。鼠齒漏而多非，猴面長而不飽。黨結奸邪之輩，讎 |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-048` | 对应度<0.15，引文不能支持结论 | 吟，言祕密謹似珠金，若人收得得意集，此法須收拾， |
| `physiognomy/shenxiang-quanbian` | `SHENXIANGQUA-049` | 对应度<0.15，引文不能支持结论 | 似破菰兒，何知貪財并好色，龜背龜胸如何說？何知 |
| `san-shi/daliuren-daquan` | `DLR` | 对应度<0.15，引文不能支持结论 | 取课先从下贼呼，如无下贼上克初。初传之上名中次，中上加临是末居。三传既定天盘将，此是入式法第一。 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-DLR` | 对应度<0.15，引文不能支持结论 | 甲课寅兮乙课辰，丙戊课巳不须论。丁己课未庚申上，辛戌壬亥是其真。癸课原来丑宫坐，分明不用四正神。 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-003` | 对应度<0.15，引文不能支持结论 | 一 贼克法一下克上曰重审，一上克下曰元首 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-005` | 对应度<0.15，引文不能支持结论 | 渉害行来本家止，路逢多克为用取。孟深仲浅季当休，复等柔辰刚日宜。 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-007` | 对应度<0.15，引文不能支持结论 | 无遥无克昴星穷，阳仰阴俯酉位中论初传也。刚日先辰而后日，柔日先日而后辰论中末也。 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-010` | 对应度<0.15，引文不能支持结论 | 伏吟有克还为用，无克刚干柔取辰。迤逦刑之作中末，从兹《玉厯》职其真。若也自刑为发用，次传颠倒日辰并。次传更复自刑者，冲取末传不论刑。 |
| `san-shi/daliuren-daquan` | `DALIURENDAQU-011` | 对应度<0.15，引文不能支持结论 | 返吟有克亦为用，无克别有井栏名。若知六日该无克，丑未同干丁己辛。丑日登明未太乙，辰中日末识原因阳日用辰，阴日用日，辰上作中，日上作末。 |
| `san-shi/liuren-miben` | `LM` | 对应度<0.15，引文不能支持结论 | 凡占以正時為主，或為日之德合鬼墓，或為辰之破害刑衝，傳課未成，吉凶先露，故曰先鋒門。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-LM` | 对应度<0.15，引文不能支持结论 | 神後屬子，其數九，味咸，女虛危三宿三位。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-003` | 对应度<0.15，引文不能支持结论 | 甲子旬，子儀神，卯丁神，戌亥天中，壬日亥不空，醜奇神，酉閉口，未五亡神。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-004` | 对应度<0.15，引文不能支持结论 | 剛日先看日上神，更兼發用細詳明。柔日支上先須視，用神兼取兩邊迎。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-007` | 对应度<0.15，引文不能支持结论 | 類不逢空旺相乘，傳生支合事須成，見類日鬼空刑害，所乾不遂類中明。幹事，三傳上下相生，支神三六合乾合，所幹成。雖是見類，與今日為鬼，或刑害空亡，三傳見害，不成。傳 |
| `san-shi/liuren-miben` | `LIURENMIBEN-009` | 对应度<0.15，引文不能支持结论 | 日鬼加臨辰兩課，門中官事乃相榮。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-013` | 对应度<0.15，引文不能支持结论 | 傳進為進，傳退為退。進空宜退，退空宜進，觀其傳，吉則進，凶則退。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-015` | 对应度<0.15，引文不能支持结论 | 凡合與德入傳，百事皆吉，即會凶神，亦主凶中和合。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-016` | 对应度<0.15，引文不能支持结论 | > 原 CTP 标题附注：李批：亦可作注解入各類下 |
| `san-shi/liuren-miben` | `LIURENMIBEN-017` | 对应度<0.15，引文不能支持结论 | 天課占天人課人，地課卜宅地墳塋。罡天魁地人求貴，此訣教君最有靈。孟仲季中分順逆，地般落處見真情。仲於本位天盤取，孟季須知隔五尊。此是三才期應訣，鬼神無處可潛形。 |
| `san-shi/liuren-miben` | `LIURENMIBEN-018` | 对应度<0.15，引文不能支持结论 | 始入者，初起而犯上者也。凡四課中惟一下賊上者，名始入。若有一上克，複有下賊，舍克取賊發用，乃謂之重審。 |
| `san-shi/liuren-zhiyin` | `LR` | 对应度<0.15，引文不能支持结论 | 8. 以月將加占時之上 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-LR` | 对应度<0.15，引文不能支持结论 | 14. 賊克為初用之始，相因作中末之身。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-003` | 对应度<0.15，引文不能支持结论 | 17. 克多比用涉害， |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-005` | 对应度<0.15，引文不能支持结论 | 24. 若昴星當俯仰於酉上。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-006` | 对应度<0.15，引文不能支持结论 | 27. 若別責取干支之合神。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-007` | 对应度<0.15，引文不能支持结论 | 29. 伏返以刑衝為定 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-009` | 对应度<0.15，引文不能支持结论 | 32. 八專以逆順為真。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-010` | 对应度<0.15，引文不能支持结论 | 167. 用為發端之門，中為移易之府，末為歸計之宮。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-012` | 对应度<0.15，引文不能支持结论 | 227. 占天看雲龍風虎，察水火升降以辨陰晴。占地看玉藻金英，視神將生克以知吉凶。占宅占人看日辰而次詳課義，占獄占病視勾虎而解救同論。捕亡三奸之下可得，鬼神煩神 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-014` | 短句无句读，无法扩成原文整行 | 1574. 三合章第三十 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-017` | 对应度<0.15，引文不能支持结论 | 16. 克者動也，不克則不動。課中有幾克，即有幾事。又事之應期，亦在克中求，蓋克者，轉折也。元首主速，重審主遲；元首主喜，切防樂極生悲；重審主憂，亦詳自暗而明。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-018` | 对应度<0.15，引文不能支持结论 | 508. 辰來克日諸事難成，日往克辰所謀皆遂。 |
| `san-shi/liuren-zhiyin` | `LIURENZHIYIN-020` | 对应度<0.15，引文不能支持结论 | 174. 三傳生日百事宜，日生三傳財源耗。日克三傳求財可羨，三傳克日眾鬼難堪。初傳克末事成空，末克初傳事可成。傳見妻財利益多，傳見父母饒生意，傳見兄弟口舌生，傳 |
| `san-shi/qimen-faqiao` | `QM-P26` | qimen-faqiao excerpt only; no publisher scrape | 直使加地丁为守门 |
| `san-shi/qimen-faqiao` | `QM-P36` | qimen-faqiao excerpt only; no publisher scrape | 时干入墓，戊戌、壬辰、丙戌、癸未、丁丑、己丑也 |
| `san-shi/taiyi-shenshu` | `TR-06` | quote not locatable or previously unanchored | 九宫各主一州（一兾 / 二荆 / 三青 / 四徐 / 五豫 / 六雍 / 七梁 / 八兖 / 九雝） |
| `san-shi/taiyi-shenshu` | `TR-07` | quote not locatable or previously unanchored | 开 / 休 / 生为吉；伤 / 死 / 惊为凶；杜门闭、景门半吉 |
| `san-shi/taiyi-shenshu` | `TR-09` | 对应度<0.15，引文不能支持结论 | 經曰始擊將臨太乙宫謂之掩嵗計遇之王綱失序臣張君弱宜修徳以禳之盖掩襲刼殺之義若掩太乙在陽絶之地君凶隂絶之地臣誅掩主大將主人筭和吉不和凶參擊之勝 |
| `san-shi/taiyi-shenshu` | `TR-10` | 对应度<0.15，引文不能支持结论 | 推積年法      推君基太乙法 |
| `san-shi/taiyi-shenshu` | `TR-11` | quote not locatable or previously unanchored | 天皇占至尊 / 帝符占符瑞 / 天时占时气 / 太尊占至上 / 飞鸟以鸟象占 / 五行以五行配 / 八风以八方风占 |
| `san-shi/taiyi-shenshu` | `TR-12` | 短句无句读，无法扩成原文整行 | 〔與四神天乙地乙直符同用〕 |
| `san-shi/taiyi-shenshu` | `TR-14` | 对应度<0.15，引文不能支持结论 | 經曰助戰之法常須觀風雲之勢察飛鳥之情若太乙所在宫有風雲飛鳥䓁来衝格迫擊太乙者大敗之兆若迫擊大將宫者主敗若從主目上去擊客客敗若從客目上擊主主敗若從主人形上来客敗若 |
| `san-shi/taiyi-shenshu` | `TR-15` | quote not locatable or previously unanchored | 本 pack 仅作纲领；不展开具体应用 |
| `selection/donggong-zeri` | `DONGGONGZERI-DR` | 对应度<0.15，引文不能支持结论 | 小寒 小寒後三煞在東 |
| `selection/donggong-zeri` | `DONGGONGZERI-003` | 对应度<0.15，引文不能支持结论 | 紫檀天皇地皇星蓋照、宜婚姻入宅、起造安葬、 |
| `selection/donggong-zeri` | `DONGGONGZERI-006` | 对应度<0.15，引文不能支持结论 | 正、四、七、十，四孟之月： |
| `selection/donggong-zeri` | `DONGGONGZERI-008` | 对应度<0.15，引文不能支持结论 | 滿寅日：黃沙天富，是土瘟、但不宜動土，然有福星並黃羅 |
| `selection/donggong-zeri` | `DONGGONGZERI-009` | quote not locatable or previously unanchored | 本书属于民间通书系；遇到《协纪辨方书》《星历考原》对神煞、宜忌、起例的不同说法时，本书只能作为旁证或民间异说，不能覆盖官方系统。 |
| `selection/donggong-zeri` | `DONGGONGZERI-010` | 对应度<0.15，引文不能支持结论 | 建子日：火星甲子天赦日進財、惜被月建沖破用之主官司 |
| `selection/donggong-zeri` | `D2` | quote not locatable or previously unanchored | 状态 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-006` | 对应度<0.15，引文不能支持结论 | 宜霜降後立春前執日危日收日 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-007` | 对应度<0.15，引文不能支持结论 | 乾坤寳典曰天道者天之元陽順理之方也其地宜興舉衆務向之上吉○廣聖歴曰天道正月九月在南方二月在西南方三月七月在北方四月十二月在西方五月在西北方六月十月在東方八月在東 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-008` | 对应度<0.15，引文不能支持结论 | 起工通用吉日 己巳辛未甲戌乙亥戊寅己夘壬午甲申乙酉戊子庚寅乙未己亥壬寅癸夘丙午戊申己酉壬子乙夘己未庚申辛酉成開日 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-010` | 对应度<0.15，引文不能支持结论 | 忌土府月破平日收日閉日劫煞災煞月煞月刑月厭四廢土符地囊土王用事後 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-011` | 对应度<0.15，引文不能支持结论 | 按天德月德乃月建三合旺氣天德合月德合與旺氣作五合皆上吉之日故所宜應如此忌畋獵取魚者恐傷生氣也舊本天德止宜興土工營宮室繕城郭月德并宜上官宴樂天德合宜祭祀祈福覃恩肆 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-014` | quote not locatable or previously unanchored | 立券、交易、开市、纳财宜：天恩、天德、月德、成日、开日、满日；忌：破日、闭日、月破、四废、五墓。经络、酝酿另有专用吉日。 |
| `selection/xieji-bianfang-shu` | `XIEJIBIANFAN-015` | 对应度<0.15，引文不能支持结论 | 忌月建月破劫煞災煞月煞月刑月厭每月一日六日十五日十九日二十一日二十三日 |
| `selection/xingli-kaoyuan` | `KR-01` | quote not locatable or previously unanchored | 本书为康熙朝官方择日典籍考源；其规则定位是"神煞出处与起例口诀的官方源头"，不直接定具体某日吉凶。 |
| `selection/xingli-kaoyuan` | `KR-04` | 对应度<0.15，引文不能支持结论 | 立春艮雨水寅驚蟄甲春分卯 |
| `selection/xingli-kaoyuan` | `KR-09` | quote not locatable or previously unanchored | 金神七煞由年干推算，每年所占方位不同；为方位之大凶神，忌动土 / 修造。 |
| `selection/xingli-kaoyuan` | `KR-12` | quote not locatable or previously unanchored | 月建（该月建除之首）；月破（月建对冲日）；月厌（按月逆轮）；月害（六害关系）；为月凶神核心。 |
| `selection/xingli-kaoyuan` | `KR-13` | 对应度<0.15，引文不能支持结论 | 廣聖厯曰四廢者四時衰謝之辰也其日忌出軍征伐造舍迎親封建拜官納財開市○ |
| `selection/xingli-kaoyuan` | `KR-16` | quote not locatable or previously unanchored | 时神之首为贵登天门（贵人乘天乙之时）；其次为四大吉时；按日干起十二贵人时辰。 |
| `selection/xingli-kaoyuan` | `KR-17` | quote not locatable or previously unanchored | 卷六将"用事"系统化为六十事项（祭祀 / 嫁娶 / 起造 / 商事 / 安葬 / 出行 / 农事 / 医疗 / 沐浴 / 修缮 等）；每事项有官方"宜 / 忌" |
| `selection/yuqia-ji` | `JR-02` | 对应度<0.15，引文不能支持结论 | 真君見世人作福酬願，拜表上章，建齋設醮，或吉或凶，作福作禍。 |
| `selection/yuqia-ji` | `JR-04` | quote not locatable or previously unanchored | 二十八宿按七曜（日月火水木金土）周而复始配日；本书有"角木蛟亢金龙氐土貉…"长歌，逐宿配吉凶事项；与协纪辨方书卷五口径基本一致。 |
| `selection/yuqia-ji` | `JR-09` | 短句无句读，无法扩成原文整行 | 伏斷日             上兀下兀日 |
| `selection/yuqia-ji` | `JR-11` | 对应度<0.15，引文不能支持结论 | 人神所在日           先賢死葬日 |
| `selection/yuqia-ji` | `JR-13` | 对应度<0.15，引文不能支持结论 | 乙卯、丙辰、丁巳、戊午、已末五日，   在正東，忌甲卯乙。 |
| `selection/yuqia-ji` | `JR-15` | 对应度<0.15，引文不能支持结论 | 凡嫁娶男命與女命，三合、六合皆吉。 |
| `selection/yuqia-ji` | `JR-16` | 对应度<0.15，引文不能支持结论 | 天德是跟天道，月德是三合月旺，歲德是歲君天干，此三德之吉不與別吉相同，乃與三德相合者吉，與三德同。 |
| `selection/yuqia-ji` | `JR-17` | quote not locatable or previously unanchored | 民俗安葬宜鸣吠 / 鸣吠对 / 月恩 / 三合；忌重丧 / 复日 / 重日 / 月破 / 月厌 / 楊公忌 / 十恶大败。与协纪辨方书卷七安葬通例基本一致。 |
| `selection/yuqia-ji` | `JR-18` | quote not locatable or previously unanchored | 本书杂占篇收占梦、占耳鸣眼跳、占禽鸟、占灯花等民俗占断；以"梦兆 → 吉凶事项"或"身体征兆 → 吉凶事项"作映射。 |
| `selection/yuqia-ji` | `JR-19` | quote not locatable or previously unanchored | 民俗以猫瞳孔形状判时辰（子午圆 / 丑未亥扁 / 寅申巳枣核 等）；定寅时按节气月相调整。 |
| `selection/yuqia-ji` | `JR-20` | 对应度<0.15，引文不能支持结论 | 彭祖百忌日           楊公忌日 |
| `xingming/guotian-jing` | `GUOTIANJING-GR-01` | 短句无句读，无法扩成原文整行 | 子土宝瓶齐青位， |
| `xingming/guotian-jing` | `GUOTIANJING-003` | quote not locatable or previously unanchored | 28 宿各有度数（角 12、亢 9、氐 16…轸 17）；命躔哪一度即定度主。 |
| `xingming/guotian-jing` | `GUOTIANJING-004` | 对应度<0.15，引文不能支持结论 | 太阳行度、 |
| `xingming/guotian-jing` | `GUOTIANJING-005` | 对应度<0.15，引文不能支持结论 | 度：度主者，谓： |
| `xingming/guotian-jing` | `GUOTIANJING-006` | 对应度<0.15，引文不能支持结论 | 向：向者诸星向朝也，如日月向朝，如官福向朝，如田财向朝，如文魁向朝，如经纬向朝，如三元满用向朝，如一主专权向朝。向者有情凶星又怕向。 |
| `xingming/guotian-jing` | `GUOTIANJING-007` | 对应度<0.15，引文不能支持结论 | 昼夜百刻日永日短之图、 |
| `xingming/guotian-jing` | `GUOTIANJING-008` | quote not locatable or previously unanchored | 星辰强势位分入垣 / 升殿 / 庙旺 / 喜乐 4 等；外加贵格 / 贱格双向标签。 |
| `xingming/guotian-jing` | `GR-02` | 短句无句读，无法扩成原文整行 | 天干化曜星例、以年干横取 |
| `xingming/guotian-jing` | `GUOTIANJING-011` | 对应度<0.15，引文不能支持结论 | 天囚、若遇阑干贯索相并主牢狱之患 |
| `xingming/guotian-jing` | `GUOTIANJING-012` | 对应度<0.15，引文不能支持结论 | 科名、 |
| `xingming/guotian-jing` | `GUOTIANJING-013` | 对应度<0.15，引文不能支持结论 | 壬甲从干乙癸坤， |
| `xingming/guotian-jing` | `GUOTIANJING-014` | 短句无句读，无法扩成原文整行 | 斗标．注受．天乙、 |
| `xingming/guotian-jing` | `GUOTIANJING-015` | 对应度<0.15，引文不能支持结论 | 阳刃、 |
| `xingming/guotian-jing` | `GUOTIANJING-016` | 对应度<0.15，引文不能支持结论 | 五十一月临巳上， |
| `xingming/guotian-jing` | `GUOTIANJING-017` | 对应度<0.15，引文不能支持结论 | 牛头大忌，又谓之破碎。 |
| `xingming/guotian-jing` | `GUOTIANJING-018` | 对应度<0.15，引文不能支持结论 | 金空则鸣火空发， |
| `xingming/guotian-jing` | `GUOTIANJING-019` | 对应度<0.15，引文不能支持结论 | 巳酉丑人马在亥， |
| `xingming/guotian-jing` | `GUOTIANJING-020` | 对应度<0.15，引文不能支持结论 | 豹尾：同 上，戌未辰丑戌未辰丑戌未辰丑。 |
| `xingming/guotian-jing` | `GR-04` | 对应度<0.15，引文不能支持结论 | 先天心法、李?问答 |
| `xingming/guotian-jing` | `GUOTIANJING-GR-04` | 对应度<0.15，引文不能支持结论 | 后天口诀、李?问答 |
| `xingming/guotian-jing` | `GUOTIANJING-025` | 对应度<0.15，引文不能支持结论 | 至宝论、李?问答 |
| `xingming/guotian-jing` | `GUOTIANJING-026` | 对应度<0.15，引文不能支持结论 | 评人生禀赋分金论、李?问答 |
| `xingming/guotian-jing` | `GR-05` | 对应度<0.15，引文不能支持结论 | 即宫主、度主、身主是也。 |
| `xingming/guotian-jing` | `GUOTIANJING-031` | 对应度<0.15，引文不能支持结论 | 天地万物莫逃乎数，二气运行三辰流转，至于人物之休咎，莫不有不期然而然者，非人力所可为也。 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-XR` | quote not locatable or previously unanchored | M01 主曜身宫与经用 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-008` | 对应度<0.15，引文不能支持结论 | 日月五星各得其所富貴之原也如日午月未水居巳申金居辰酉火居夘戌木居寅亥土居子丑是也 |
| `xingming/xingming-suyuan` | `XR-02` | quote not locatable or previously unanchored | 01 度主为正 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-013` | quote not locatable or previously unanchored | 03 转生取用 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-014` | quote not locatable or previously unanchored | 04 飞廉守照 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-017` | 对应度<0.15，引文不能支持结论 | 〔炁月〕 乙〔水日〕 丙〔羅羅〕 丁〔計計〕 戊〔孛火〕 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-025` | quote not locatable or previously unanchored | 03 飞廉浮沉羊刃 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-027` | quote not locatable or previously unanchored | 05 闌干煞缢死 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-032` | quote not locatable or previously unanchored | 04 流年三方对照 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-042` | pack meta-rule, no original sentence | 03 不替代子平 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-043` | quote not locatable or previously unanchored | 04 旁证层接受相术 |
| `xingming/xingming-suyuan` | `XR-08` | 对应度<0.15，引文不能支持结论 | 老仙曰我之與世遇無他葢時變人輕不可與傳仙道惟汝淳愿質朴可傳憕曰仙道不願學也但星命之中願聞一二足矣 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-XR-08` | 对应度<0.15，引文不能支持结论 | 余在江湖二十餘年訪求訣命之士甚多考藝多無實學與果老所傳大不侔矣其中間有可取條目及彷彿格局不曽該載凡例者今續附于后以俟叅用焉 |
| `xingming/xingming-suyuan` | `XINGMINGSUYU-046` | quote not locatable or previously unanchored | 03 卷四后篇寿夭案例与具体死法 |
| `xingming/xingxue-dacheng` | `XXDC-R008` | 对应度<0.15，引文不能支持结论 | 一立身在何度何宫晝生人看命度主夜生人看身度主如上望前望後及下生者看身度主為亦如命度之法 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FZ` | pack meta-rule, no original sentence | 華山陳希夷先生飛星紫微斗數原旨 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-FZ` | 对应度<0.15，引文不能支持结论 | 觀測之道。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-003` | 对应度<0.15，引文不能支持结论 | 故先布出身命垣。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-004` | quote not locatable or previously unanchored | 本书将阴宅、阳宅、相理、命理互相参看；面相高低、痣、骨格等可作为地理/阴阳宅状态的观察线索，地理状态也可作为命盘旁证。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-005` | quote not locatable or previously unanchored | 流年吉凶星煞所到方位，书中常以阴阳宅、四邻住户、地主、土地变动、树木墙垣、塋葬起灵等事件相应；使用时应先确认命盘方位与实际空间方位。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-006` | 对应度<0.15，引文不能支持结论 | 歲破之方主破財破敗拆毀等事。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-008` | 对应度<0.15，引文不能支持结论 | 如法院警察局看守所律師之屬。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-010` | 对应度<0.15，引文不能支持结论 | 而其他一切對于占課身命顯然布明。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-011` | quote not locatable or previously unanchored | 本书把天气冷暖风雨阴晴与人事运限类比，且有按日时盘占风雨的案例；可作传统观测样例。 |
| `ziwei/feixing-ziwei-doushu-yuanzhi` | `FEIXINGZIWEI-012` | 对应度<0.15，引文不能支持结论 | 諸廟宇神煞表最靈不過。 |
| `ziwei/ziwei-doushu-quanshu` | `ZW` | 对应度<0.15，引文不能支持结论 | 紫微有倚靠年長之兄，天府同三人，天相同三四人，破軍同亦有三人，或各胞生，加羊陀火鈴空劫克害有則欠和。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW` | quote not locatable or previously unanchored | 01 14 主星核心断诀 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-01` | 对应度<0.15，引文不能支持结论 | 希夷先生曰：紫微為帝座，在諸宮能降福消災，解諸星之惡虛。能制火鈴為善，能降七殺為權。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-01` | 对应度<0.15，引文不能支持结论 | 紫微有倚靠年長之兄，天府同三人，天相同三四人，破軍同亦有三人，或各胞生，加羊陀火鈴空劫克害有則欠和。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-005` | pack meta-rule, no original sentence | 太阳庙旺（寅卯辰巳午）入命主贵气光明、为父星夫星；落陷（戌亥子）入命主辛劳;**女命**太阳庙旺与男命同贵，落陷则古书指婚迟（**强 reframe**：现代社 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-008` | 对应度<0.15，引文不能支持结论 | 財居空亡巴三覽四，文曲旺宮聞一知十。暗合廉貞為貪濫之曹吏。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-010` | pack meta-rule, no original sentence | 太阴庙旺（亥子丑酉）入命主富裕清秀、为母星妻星；落陷（巳午）入命主劳碌；**女命**太阴庙旺与男命同主富，落陷古书断为夫缘薄（**强 reframe**）。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-011` | 对应度<0.15，引文不能支持结论 | 答曰：廉貞屬火，北斗第五星也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-012` | 对应度<0.15，引文不能支持结论 | 北斗第二星也，為陰精之星，化氣為暗。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-015` | 对应度<0.15，引文不能支持结论 | 答曰：貪狼北斗解厄之神，第一星也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-017` | quote not locatable or previously unanchored | 02 辅星煞星合论 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-021` | 对应度<0.15，引文不能支持结论 | 苗而不秀科名陷於凶神，發不主財祿主躔於弱地。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-022` | 对应度<0.15，引文不能支持结论 | 命里逢空不飄流即主疾苦，馬頭帶劍非夭折則主刑傷。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-026` | quote not locatable or previously unanchored | 03 四化与三奇加会 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-03` | 对应度<0.15，引文不能支持结论 | 紫微廟旺遇左右昌曲魁鉞，軒勝位至封候伯，加羊陀火鈴平常，天府同權貴名利兩全，天相加內外權貴清正，破軍同鬧中安身。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-031` | 对应度<0.15，引文不能支持结论 | 若居廟旺，化祿化權，允為貴論。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-032` | quote not locatable or previously unanchored | 04 十二宫核心断法 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-04` | 对应度<0.15，引文不能支持结论 | 紫微土，南北斗化帝座，為官祿主。紫微面紫色或白青，腰背肥滿，為人忠厚老成，謙恭耿直，其威制七殺降火鈴。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-04` | 对应度<0.15，引文不能支持结论 | 紫微有倚靠年長之兄，天府同三人，天相同三四人，破軍同亦有三人，或各胞生，加羊陀火鈴空劫克害有則欠和。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-040` | 对应度<0.15，引文不能支持结论 | 順數命前六位是天傷，命後六位是天使，天傷安在奴僕宮，天使安在疾厄宮。身與歲限夾在傷使中間，謂之加夾地更加惡曜多凶。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-045` | 对应度<0.15，引文不能支持结论 | 生不逢時 命坐空亡逢廉貞是也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-05` | 对应度<0.15，引文不能支持结论 | 財蔭夾印 相守命武梁來夾是也，田宅宮亦然。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-05` | 对应度<0.15，引文不能支持结论 | 日月夾命 不坐空亡遇逢本宮有吉星是也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-048` | 对应度<0.15，引文不能支持结论 | 生不逢時 命坐空亡逢廉貞是也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-049` | 对应度<0.15，引文不能支持结论 | 風雲際會 身命雖弱二限逢祿馬是也。 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-06` | 对应度<0.15，引文不能支持结论 | 如宮分星纏全吉廟旺得地，無擎羊陀羅火鈴空劫者，主十年安靜，人財全美。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-057` | 对应度<0.15，引文不能支持结论 | 人生子命忌寅申  假如子年生人切忌寅申歲限，災晦至重，及忌子午歲限相衝。 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-07` | pack meta-rule, no original sentence | 古书男命主官禄财帛，女命主夫子家宅，断法不同；**强 reframe**：现代社会男女平权，不应套用古书男女命差异。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-07` | 对应度<0.15，引文不能支持结论 | 府相之星女命躔，必當子貴與夫賢。 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-066` | 对应度<0.15，引文不能支持结论 | 紫微 廟丑未午 旺寅申卯酉巳亥 平子 無陷 |
| `ziwei/ziwei-doushu-quanshu` | `ZW-09` | 对应度<0.15，引文不能支持结论 | 紫微 廟丑未午 旺寅申卯酉巳亥 平子 無陷 |
| `ziwei/ziwei-doushu-quanshu` | `ZIWEIDOUSHUQ-ZW-09` | 对应度<0.15，引文不能支持结论 | 生不逢時 命坐空亡逢廉貞是也。 |
