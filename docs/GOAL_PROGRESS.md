# 完整目标施工账本

目标保持 active：执行 `docs/FATERADAR_FULL_LIBRARY_PLAN.md`，直到全库加工、八术核心算法、免费内容和产品联动全部完成并通过总验收。当前仍在施工；局部检查绿色不能当作总验收，也没有无法推进的阻塞。

两仓均为 `codex/full-library-completion`：古籍 `/Users/yuhanglin/.codex/worktrees/fateradar-classics-grok-full-library`；产品 `/Users/yuhanglin/.codex/worktrees/fateradar-product-grok-full-library`。原接手基准古籍2396e4c、产品8f1ca84。原main及他人admin/billing/.claude不改。本目标尚未合main或部署。

## 最新接续点：2026-09-08 17:05

此段优先于下方旧接续记录。完整目标仍active；本命与六爻新增批次有固定提交验证，但全库/八术完整目标尚未总验收，没有合main或部署。

- 当前固定清单1497b01取源ffed8d1：55资料包、54主文件、53640主段，14163已注解、39477未注解；5补充版3516段。主段ID与范围逐项比旧索引全同，没有重切编号。229来源规则记录/433引文范围是定义数量，不能说全都执行。17inventory测试过，固定源注解校验19books/23files/15712entries、15333 source-reviewed、0error；其中379为draft元数据。
- 全知识产品4a22d99固定源5379881：57156段，15333 source-reviewed。新增雪心18、葬法13、都天101、疑龙96全部逐段对当前电子源；都天根重写33处、疑龙78段。疑龙本仓合刊对照出外无拦、阳宅怕穴小、中央过等较明读法，同时合刊变星篇末自记缺文；保留异版，不覆原字、不计独立支持。此前三份Grok任务均已收齐；新《入地眼全书》126段草稿运行中，session17086，目录/tmp/fateradar-grok-rudi-20260908，尚未验读/入库。新提示词加了现代白话、非简体重述、古文收束不当元数据及相邻条件要求。临时原JSON/草稿在/tmp/fateradar-grok-{zangfa,dutian,yilong}-20260908；Grok疑龙session01a08018-0784-73b0-b2a1-3cd25fe5d700。绝不输出wrapper.thought。疑龙5379881已提交，50知识/reading测试过。
- 源案例references/cases/source-cases.json已更新固定5379881：2201次出现、2184组件输入可复算、149重复输入关系、69异表期望争议、verified全false；原书叙述应验与可复算字段分开。产品奇门fixture仍固定7bdd1b5/1106条，来源引用均在已提交历史内。
- 奇门18局总表5178ac2完整：1080输入（18局×6旬×10时）、1106出现；67条含103异表争议字段。根83bbfd1比较4284一致字段，4字段为阴五丁酉两处九八→按同书一般法八八、阴八丙申两处三三→按法一三，原expected/clear保持。6ce1c93同版方法和圆图支持时干法；具名差异断言与六丁/六丙一般法检查，1136相关测试通过，不能算1106完整盘全一致。b29a176已补10时附格可辨部分；当前classics_audit继续原纸卷4–9的圆图和逐时附断，未全完。P97己丑“但非伏吟”纠正了尚未提交稿的错拼“但非入墓”，不能建免墓规则。
- 本命格局：正官f26146f、财052f258、印379a2a7、食伤5aec9f4、七杀7bd9511、禄劫/阳刃11af74a已生产。禄刃19原例+17真实日期，相关252项与36原文锚核过。fe8009b共享五合：日主严格更近参与排他而不合去，同距既定顺序保留。root60b7dea公共execution接所有family、luren优先、monthKind、真实entryFacts；夏主月劫己藏伤制时杀不再留在局部食伤；脱脱年壬＋月辰藏癸不造辰藏壬；原源与变用后财/官名称分开。
- 免费/病药/报告/追问：ecae2ba补实际作用者位置与空病药的未成/未知理由，bazi-evidence E01消费真实entryFacts，实际execution源范围各有自己的version/anchor，ID不是伪造算法规则。263cc42再修yongshen只认展示字“成格”的漏接：采用公共execution.verdict，月比“配合成立”也正确进入格局取用。Ego实测1981-07-08 14:00男上海clock（辛酉乙未丁亥丁未）修前错退扶抑水土金，修后总览/喜忌格局取用土金，显示真实月藏己食、年辛财，扶抑/调候分列。
- 六爻producer至5f65fd8/古籍ffed8d1，共19规则：逐爻日月空破墓绝进退飞伏；45829d8端位三合、4371be6主卦实际三位置候选；1f1cd26寅巳申论刑不论生；25b3897日冲回克解除、不能把月冲或自身旬空一并删除；5f65fd8内外反吟/伏吟与恒豫具体合护、已旺且活动确认戌才自冲辰墓。49分析行为、7文件110相关测试/tsc/lint/19真源出口过。root394524d/c64bd43/bcf1ff1/e88e38e把threeHarmony/punishments/backControls/reversals完整转交模型；31chat测试过。静变只作卦形、不造活动节点，组合不重复加力。不存在全面应期或事项终断完成的宣称。
- 固定审查worktree/private/tmp/fateradar-review-20260908-1610：83bbfd1旧全测5fail已真实修；8259cbf 71files/1984pass；60b7dea 73files/2028pass，typecheck/lint:ci/Nodebuild均过。固定263cc42全测73files/2033项、tsc/lint:ci/Nodebuild均已通过；日志/private/tmp/fateradar-263cc42-{tests,typecheck,lint,build}.log。日志按提交分文件，不把并行工作区当已验。review worktree有node_modules软链，无.env复制。原golden不刷新。
- 预览仍Ego空间7、5188服务session14995，原5186用户tab不动。8月印例pmts5rsg070ff保留存储；最新月比合成档案pmtsfqxm801pm当前在tab7AAB7B8FE3B15670F8B90CCE0DD5E0D8。按钮click可能无效，DOM表单requestSubmit确实保存并导航；新建而未覆旧档案。六爻tabAE76363261D505E35162C8D7A3FC2127仍2000-04-20父母例。书房tab452402...当前都天乾流已读回白话/原文/固定行号，另一个书房tab仍增删枯根。只做语义/DOM交互读回；Screenshot帮助和CDP两次失败，不宣称视觉截图已验。
- Web消息仍未发送：工具仅list/read/wait，无create/send；原生CUA getApp(Codex)明确禁止com.openai.codex，不能绕过。已读computer-use技能，已向用户说明具体阻塞。docs/ART_READING_FIELD_MAP.md、GEJU_EXECUTION_DELIVERY.md、LIUYAO_ENGINE_WEB_DELIVERY.md已更新具体接口和样例，不冒双方已沟通。继续其余独立工作。
- 最近已推送：产品固定8259cbf、古籍8ca2150；后面的263cc42/1497b01与其祖先待本批核后推自己的completion分支。根当前仅有doc措辞小修和GOAL_PROGRESS未提交；不要包含agent的liuren/qimen工作稿。

## 当前存活分工（替代下方旧角色记录）

- classics_audit：只负责奇门原纸卷4–9恢复/图式/附断、对应annotations/page-reviews/source-cases候选/书评。root拥有registry/exporters及产品qimen算法。还有大量原附格图文，不能改称不存在。
- bazi_audit：六爻本批已完成，已转大六壬。发现壬癸GUIREN昼夜两支写反：当前卯巳，原大全L17771夜卯、L17739昼巳/夜卯、L4832正月壬子辰时亥将加时贵加戌倒行支持昼巳。正在修liuren.ts＋源例/真实日期/原字符化测试，四课三传地支未改；拟generalPlacement={dayStem,dayTime,daylightRule:fixed-06-18,localTime,selectedBranch,earthBranch,forward,source?}。root接chat/免费位置投影。6/18保持现口径，未据未定流派改5/17。
- other_arts_audit：禄刃11af74a后进入岁运，已授权拥有bazi/types、geju-strength、各producer上下文、geju.ts、yunsui.ts、bazi/index与bazi.ts岁运输入传递。原四柱gans/zhis仍四项，新增context.externalPillars；actorId natal:year/month/day/time与dayun/liunian分层。当前所取财/印与来源family分开，不重置原出生主格；先明文官的运支植根、运干合官/混杀和干支不同效应，再继续各族。返回助力/牵制/交织/未定及before/after条件，不换成新分数。root已明确批准无需逐个常规文件再询问。
- root：共同projection/free/yongshen/bingyao/readings/chat/UI、通用出口和全库其它古籍。岁运将由root接模型/页面，同张图选岁运后同步解释；当前静态xi评分仍在，但agent正实现替换，别并行再写它。继续剩39477主段与各未完算法，不缩成当前完成子集。

## 历史接续点：2026-09-08 12:45

- 原文真实性、来源外键、缺失正文和补充版本协议已修。55资料包、54主文本、主索引53640段；导航与正文、正文与盘表、重复与独立支持分别统计。固定快照190cbab包含4份补充/对照来源3137段，总知识56777段，14105条source-reviewed注解；其中大量盘表、导航、目录，不是14105条理论或算法。主索引13196有注解，40444尚无注解。
- 当前源案例快照190cbab：1095次出现，1078具备所列组件复算输入，123重复输入关系，2项紫微原表期望冲突，全部verified=false。记录见references/cases/source-cases.json。模型自审、测试通过不升人工verified，不刷新原golden。
- 《子平真诠》556、《穷通宝鉴》605、《梅花易数》623、《紫微斗数全书》1981以及青囊奥语/序、太微赋、葬书、冰鉴、黄帝宅经当前电子文本已逐段整理。根新完成青囊经24段b7647e0，经文与蒋注/再录/资料分层，五星表L460–464缺接明确标记，不声称影印全校。紫微85待核项含真实版本/取法差异，不能强行清零。
- 《命理约言》旧抓取540条全为导航/元数据，0正文，原文件保持。新增韦千里四卷选本NLC185页恢复版；781段全处理，406实质正文均逐页校读。614 source-reviewed、167封面/恢复元数据draft。选本不冒称原十卷；影印状态按page-reviewed/passage-reviewed/ocr-draft逐段分开。2张神峰完整四柱例已导出。
- 《滴天髓阐微》最终1bfa0f7：63章5681/5681段全审，977正文/注＋4704盘表，517原书完整四柱出现、508组不同输入；真实疑文具体保留，不声称516页影印全校。PDF416–417校正合局两处整盘错位并保留旧电子表/ID，JSON记录位于sources/normalized/bazi/ditiansui-chanwei/collated-case-corrections.json。PDF176余气混墓库、177土极似金、258缺“无”、264戊辰、278偏正印绶、284无子等方向性问题已记校勘。
- 《增删卜易》最终4628d5d：3125/3125（1409直接语义+1523图行字段+193严格重复互链），另版295/295。31处被否定/限制的旧说已将转折写进vernacular，不能只依赖隐藏notes知道作者反对。卷一目录后只见标题，但最终逐段核对确认31章263正文段全部错置书末L6504–7730，未发现整章缺漏。193段同段同字重复，其余70段有拆合/显示包装或注记差异。因此已纠正“整卷未采入”的错误判断。维基31分章另版295段全审，保留固定rev/来源/范围/站点注记和重复互链，不全算新文字或独立支持；不用现代增订代替原书。

## 核心算法与真实消费

- 调候120日干×月令入口、136条件由穷通来源化，59旧基础列表有差异，已记docs/TIAOHOU_SOURCE_AUDIT.md。组内并看/先后/替代、缺壬缺辛等条件真正改变输出。喜忌不按旧寒暖总分改写候选；1990-01-01 13:20上海钟表时丙子月，调候壬先戊后，对应水土。寒暖估计仍为现代粗略层，不能冒充完整原文气候判断。
- 正官、财格、印格真实执行分别已落f26146f、052f258、379a2a7。力量/通根/日主承载、透藏、合绊/受制、具体控制与救应按源内路线执行；实现假设明列，不声称古书给出数值。正官宣参国/范太傅可达；财格13原例有9条成立+1失败、3具体未决；印格14原例11成立、3具体未决。各模块原文与真实日期边界见对应执行审读文档。
- 共享geju-strength保留阳长生/禄旺growthRoot与实际藏根分开；非日主干一人一合、近合优先，隔日无阻可合的原例支持来自辛亥庚子甲辰乙亥；不任意将年月隔三位合掉。印的阻挡克官路径与删除整个食伤分开。
- 产品5f85c5b：`geju.execution`只投影实际结果、不重算，统一正官/财/印的verdict、summary、supports、issues、unresolved、assumptions、sources。喜忌采用真实supports，病药采用局部实际救应；整格未决不列已采用者，局部有救仍可解释。藏官始终标藏干。geju-reading/free-reading/bingyao/yongshen/bazi-evidence统一消费。原先恒未知模板已修，不把旧字段的观察范围冒作新执行完整性。
- 原黄金012壬寅癸丑壬辰乙巳（2023-02-03 10上海）独立纠错为月劫格：子平L542–548杂气透癸劫，壬刃在子不在丑。只加具名纠错，原tests/golden/bazi.json不改。旧丙寅辛丑壬辰乙巳应杂气印，撤掉伪正官负例，换实际1987-03-01 12丁卯壬寅己酉庚午。
- 紫微178原组件出现，176无争议期望与iztro一致，木三局同日两种原表保留冲突；缺木五日/金三十日不填。只比较原例给的最小组件，不伪造生日。11个本命组合E02–E12在同一raw.palaces执行，逐项位置/亮度/状态/多片段来源可查；金舆扶驾、财荫夹印在严格原文读法与现行安星位置下不可达，已有3600合法盘扫描和位置推导，不造星曜正例。
- 产品5238e85：紫微追问接实际combinations及原文，生年四化E01接本盘行；命盘事实只传本命，不混入机器当前流年。通用概念另列；不是模型已实测。传统职业探索编辑器刻意不接命盘，保留该边界。
- 六爻产品76d4013：`buildLiuyaoStructure(lines)`只按六符装卦，buildLiuyao再附真实占日/月建。增删10图全部纳支/六亲/世应/变图一致；复占未重述日期不借前卦日期。古籍95f02e4出口支持多sources逐段核对、sourceReading/reportedOutcome分列，原称应验不进数学期望。
- 梅花主本体贯穿本互变，互两体分别对本体；结构relations/interactions进入页面/事实/追问，已撤下无依据加分吉凶与休囚死直接判凶。无节气月令不补土。
- 小六壬/七政现代实现说明与古籍分开；奇门/六壬先前实际修正保留，见产品SCHOOL_DIVERGENCE与既有审读记录。其复杂组合与时间层完整性仍需继续审查，不能因旧单测通过宣布八术全完。

## 网页、检索、报告和验证

- 书房数据按54书服务端分包，固定git archive导出，各包sourceRevision一致；客户端不带全库。本轮再更新到190cbab，14,105 source-reviewed注解可检索；Ego核增删“枯根”的31处转折修正文案及31章错置而非缺失的来源说明已显示。Ego实际查命理约言“看格局”，恢复正文、白话、PDF页数与原文行号已出现。已修旧“正文仍在恢复”笼统提示，并将导航说明和正文白话分开标题。
- 通用14读法使用独立内容版本；PointsPanel/梅花详情/紫微总览实际显示来源。新来源不串用旧CLASSICS_REV。
- 八字默认格局先解释正官/财/印是什么意思，再说本盘位置。Ego空间7表单新建合成验收档案pmts5rsg070ff：1990-08-15 13:00男上海黄浦钟表时，庚午甲申壬子丁未；格局显示印多用财/时丁，喜忌显示格局取用喜火，来源链接9aa577c正确落行。免费阅读无需登录或AI。工程词汇仍需随全模块完备继续磨平，不能用正文长度代替质量。
- 生时比较已有独立/birth-time页面，时间区间、日界、太阳时与事件精度均保留，支持/矛盾可比，不宣称找回真实时辰。输入变化清空旧结果，不写假档案。尚无独立标注集，不能说排序准确率。
- 最近已完成的代码批次全产品64文件769项通过；当前工人正新增食伤/六爻文件，不能把旧结果冒充其工作区已验。typecheck、lint:ci、改动源码ESLint通过，默认/Node生产构建通过。默认正文微调后33项再通过，知识刷新后16查询测试+7出口测试通过。日志/tmp/fateradar-current-{all-tests,lint,build,node-build}.log。原书图通过只证明原图组件一致。
- 古籍当前注解校验14books14272entries、0errors（含167draft）；源码案例14测试通过。未做真实收费模型调用或生产部署。
- Ego只用空间7，5188服务session14995；原5186用户预览保留。当前书房/八字/紫微/梅花/生时页留待完整目标验收。不要重建同任务空间；只有完成整个目标后才处理最终交接。

## 存活分工与接续动作

- classics_audit已完成滴天髓，正在奇门统宗主本739段与yanyi-vol4-9补充94段，独占san-shi该两份annotations和书评。已核补本91正文全与主本重复，其余3是元数据。根初查入墓L315乙坤/1634乙乾/1543丙丁乾有取法差异，等其上下文审读后再做规则；根拥有executable及产品集成。
- bazi_audit已完成增删，正在产品liuyao.ts/新liuyao-*模块和源例测试、文档，及古籍executable/zengshan-buyi.json。拟新增chart.analysis(use候选/逐爻日月状态/interaction/ruleChecks)，所有位置关系由结构计算；source按sourceRevision/book/chapter/fragments/primaryFragmentIndex/verified:false与紫微一致。当前删除过宽合作谈判/择时/迁移强选用神；复杂日冲旺衰须原文真分支，不以旧tier硬判。根负责chat/evidence与前端消费；tools/export-source-cases.py仍由根维护。
- other_arts_audit正在食神/伤官真实执行，负责新模块、geju.ts必要挂接、原例/真实输入测试、文档；shared strength变更需协调。summary用白话，方法/档位进assumptions。不改根消费者。
- 根独占geju-execution.ts、free/yongshen/bingyao/geju-reading/report/chat消费者及全库出口/知识接入；等食伤模块完成扩共同输出。继续其它七术深层算法与全量正文处理，不能缩成当前已完成子集。
- 产品82c2adb、古籍5bd1485已推送completion分支；当前另有整书最终、source-case和190cbab知识快照与产品Web字段文档d91bca9，需本接续点再推送。只推自己分支，不merge main/改他人任务。
- Web协调现有产品任务“后端开发”ID01a07cb3-e237-7a13-a66b-320bf1075b26，host remote-ssh-discovered:macmini-fate。工具只有list/read/wait，无create_thread/send_message_to_thread，尚未发送；不得说已沟通。具体字段文档已在产品，后续若用原生Codex UI需按技能操作；browser仍只ego。

## 尚不能总验收

尚有四万余主文本段落未审读；不能靠模式分类/待处理清单宣布完成。原书尚未解决的真实路线、其他格局、整体旺衰与局部力量口径、岁运静态喜忌评分、其他术数复合规则和时间层、全部主要栏目联动仍在范围内。各模块具体未决见执行文档。交付证明文字来源、计算实现与页面一致性，不证明传统术数的现实预测有效性。目标没有完成；继续推进。

## 接续补充：13:12，依赖中的改动不要误提交成完整版本

- 已推送产品35f105b、古籍5c3ca9e，知识固定190cbab，source-reviewed14105、原书case1095/可复算1078/重复123/原表期望冲突2。Ego已实查增删“枯根”默认白话带野鹤反驳，不再把旧说当最终断法；31章齐备但错置的来源说明也已显示。
- 根新增雪心赋18/18完整审读bbadd60（尚未重导到产品），正文否定与例外写入白话，现代网页尾注和典故不当古籍规则/真实案例。青囊经24/24先前已在b7647e0及190cbab知识版本里。
- 根工作区已接shishang进geju.execution，family扩食神/伤官；checks/effects/monthSupport/balance/transformation/notes进details，adopted仅最终满足才出。geju-reading已补食神/伤官白话。与21原书源例合测27项通过；财多带印只取丁、罗例月亥甲年透取正财而来源伤官、夏例主月劫仍未知，不借局部成立生成全局喜用。
- 根工作区bazi-evidence另把execution.sources的实际专章引用加入sources，ID形如execution:ziping-zhenquan:1046-1051。它是原文范围ID，不是新增算法规则或虚构段落ID；只使用带anchor/revision/quote/bookSlug的真实Source，每条有自己的sourceRevision和URL，不与总论E02/E03版本混同。没有paragraphId的范围不伪造fragments。chat.server输出说明改为“依据ID”。报告/对话相关48项通过，完整新批次尚未验。
- 根已把应爻接到chat.ts enum、chatSource直接读chart.analysis.use.requested，及chart.liuyao下拉与主爻高亮。原有useConsultationState持久键保持，原流程没有use的URL参数，不另造一个不消费的参数。新增应爻传输/服务端复算测试通过。六爻完整新analysis尚未进board/sources，这仍由根在producer交付后完成。
- 以上根消费者文件尚未提交，依赖other_arts_audit正在写的shishang.ts/geju.ts及bazi_audit的liuyao.ts/liuyao-analysis.ts；不要先提交造成HEAD缺producer。根拥有geju-execution/geju-reading/bazi-evidence/chat/chat.server/chart.liuyao/tests-chat和geju-execution-consumers；两agent不改这些消费者。
- other_arts_audit的shishang接口已稳定，仍在原例外的真实边界与白话校正，源例21首轮通过。夏例待后续月劫主格模块衔接，不是可以永久排除的未决。bazi_audit的7条行为测试曾通过，正在空破墓绝、进退、飞伏等规则闭合；interactions.scope=structural-relation，只表名义关系，生效情况在node.state.movement/supportPaths/ruleChecks，不能拿每条边当已经有力。
- classics_audit正在奇门：本地NLC PDF15–16目录显示原卷4–9是阴阳18局图，网页标卷4–9的91正文不是那些排局图。主文本739＋补充94分别在审；补充91正文全与主本重复。真实原局图的恢复/组件案例很有价值，尚未建入registry，不能继续说已补齐纸本卷4–9。
