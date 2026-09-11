# 三命通会识典 HY1521 语义注解进度 · 2026-09-11

独占文件：`references/annotations/bazi/sanming-tonghui--shidian-HY1521.json`。本会话只改本书注解与本进度文档。

## 源核

- worktree `sources/normalized/shidianguji/HY1521/text.md` SHA256 = `707ac9bc6796bdb679833fc280040485d95b36da6f7aca0b3e2adbb9e57d19d3`，与队列及原集成库一致。
- `load_source_paragraphs` / `paragraphs.json` 共 2340 段，首尾 ID 与 checkpoint 边界一致。
- 识典补本 `source_status=reference-text`，电子语义阅读可升 `source-reviewed`；`verified` 一律 false。不是影印校勘，不把补本当独立投票证据。
- 网站章节名与印本卷号可能不一致；正文卷题已见「卷之一」等，引用仍以正文为准。

## 队列

8 个 checkpoint，2340 段全部待语义阅读。现队列未再排除段落；1423 条转录校对门槛排除不适用于本补本这 2340 段，不能自行把未校影印升为校勘完成。

## Checkpoint 1（索引 0–299）

- 300 条已写入；校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=300`，`source_reviewed=298`，`errors=[]`。
- `verified` 全部 false。draft 2：`P7467786007220338740` 河洛图说碎行；`P7458198190622310419` 残句「人力相芜」。
- 覆盖：卷前/蒋国祥序/王谦序/河洛辩/总目，原造化、干支源流、纳音多算法、禄命身、六十甲子、神头禄与妙选六十、十干可为金木水火土、纳音与正五行、四季喜忌、徐大升过犹不及、卷一终；卷二河图洪範八干纳卦化属、十干阴阳生死、土两生与拟土歌否定、地支月提、天文地理取象、醉醒子、属相、人元司事两套日数、节气日刻、太阳躔次太阴纳甲、天月二德、旺相休囚死、寄生十二宫、遁月时、年月日时三主三限、定真论六亲。
- 条件/救应/反转已写入条目，未把未算条件当默认真。纳音多法、洪範与正五行、阳死阴生与四大长生、徐大升废纳音与罗青霄必用洪範均保留流派差异，不投票。
- 电子阅读不是影印校勘或预测有效证据。

## Checkpoint 2（索引 300–599）

- 300 条已写入；累计 entries=600。校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=600`，`source_reviewed=598`，`errors=[]`。
- `verified` 全部 false。本段无新增 draft。全书 draft 仍仅 CP1 两处：`P7467786007220338740` 河洛图说碎行；`P7458198190622310419` 残句「人力相芜」。
- 覆盖：胎元三百日与七月生贵人反例、安命宫月从子逆起时加月顺行逢卯、大运阳男阴女顺数未来节阴男阳女逆数过去节三日一岁否定约法一岁奇八月、行运用神喜忌基地厚薄、小运男丙寅顺女壬申逆与醉醒子从时生、太岁岁伤日轻日犯岁重真太岁征太岁岁运并临、进交退伏阎东叟壶中子广信集三套、十干合隔六偏枯紧慢、化气遇六遁三妒合一不能化转角进退坐下自化逐月横看、支元六合壬亥会次合禄合马合贵方向对翻、三合同刻与生旺库缺一不成局辰戌丑未全作土局、将星华盖咸池须纳音同类、六害方向酉见戌凶戌见酉无灾、三刑名目对调有吉反用主客刑入以煞止煞、冲击一七煞四庫喜冲四方全不论、卷二终、卷三十干禄四宫无禄金舆两取驿马先天计数十二马、禄马同乡孤孀、天乙阴阳昼夜三口径、三奇乙丙丁甲戊庚地三奇凿人间无据否定四奇、天月德合月空月厌旌钺三公、学堂词馆魁星多口径、秀气科名正印福聚祸聚德秀、劫煞亡神十六般分劫聚劫天煞地煞岁煞刑煞、羊刃飞刃真偏刃揽辔澄清阴干无刃、空亡天中轻重互换真空亡截路四大空亡、元辰阳前阴后徐子平七煞岁运、暗金的煞吟呻破碎白衣、灾煞白虎微不同、六厄勾绞孤辰寡宿连属不言、天罗地网龙蛇猪犬火水土才有、十恶大败四废天地转须中和、干支杂犯平头悬针曲脚聋哑、自缢水溺挂剑天火夭屠雷霆吞陷官符病符死符丧吊宅墓日刑流血剑锋戟锋浮沉破煞返本阴阳八专九醜孤鸾差错桃花红艳、福欲旺煞欲衰祸中生福、应天歌神煞不可拘定煞中包煞一位专旺对分散英灵、禄马宜合煞忌合、空亡凶煞吉禄马空亡减福、战斗力停为福偏颇为祸伏降互换相制、专论神煞则诬须先主本财官印食贵人禄马。
- 条件/救应/反转/未知已写入条目。化气妒合、三车恃势无恩名目对调、天乙冬夏与昼夜、金舆禄前与马前、学堂一位长生与柱带寅申巳亥、白虎与灾煞微不同、徐子平元辰与林开一偏、四废不及天地转太过有扶有制不在此论，均保留并置不投票。
- 图像占位不补字：`P7488273306552123419`、`P7488273311428919305`、`P7480921044170915867`、`P7480921051887616010`、`P7480921054824120330`。
- 电子阅读不是影印校勘或预测有效证据。

## Checkpoint 3（索引 600–899）· 完成

- 累计 entries=900。Multica 继承旧 owner 未提交 600–639（hash `7d51ed2`）后，本轮写完 640–899（含上轮 640–689 与本轮 690–899）。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=900`，`source_reviewed=898`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：六庚/六辛/壬癸日通论与十二月支 → 五行时地分野木火土金水 → 论甲乙丙丁戊己庚辛壬癸用神 → 纳音取用专条 → 卷四终 → 卷五印食官财名义、正官诸格、偏官/时上一贵/年煞/官煞混杂去留。
- 条件/救应/反转/未知已写入；正五行与纳音并置不投票；图像占位与残讹不补字；命例≠golden。
- worktree 已安全 `git worktree move` 至 `fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## Checkpoint 4（索引 900–1199）· 完成

- 累计 entries=1200。本轮写完 900–1199（300 段），未重做 0–899。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=1200`，`source_reviewed=1198`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：卷五杂气收束 → 伤官/伤尽 → 食神 → 飞天禄马/倒冲/合禄/专印合禄 → 阳刃/败财/比肩 → 建禄 → 卷五终 → 卷六井栏斜叉、壬骑龙背、子遥巳禄、丑遥巳禄、刑合、冲合禄马、破官、飞财、六阴朝阳、六乙鼠贵、日禄归时、拱禄拱贵、趋艮趋乾、二德、金神、禄元会等。
- 条件/救应/反转/未知已写入；图像占位与残讹不补字；命例≠golden。
- worktree：`fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## Checkpoint 5（索引 1200–1499）· 完成

- 累计 entries=1500。本轮写完 1200–1499（300 段），未重做 0–1199。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=1500`，`source_reviewed=1498`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：卷六收束（贵人帝座等）→ 卷七女命/小儿关煞等 → 卷八日时断起手（六甲日时诸断等）。
- 条件/救应/反转/未知已写入；图像占位与残讹不补字；命例≠golden。
- worktree：`fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## Checkpoint 6（索引 1500–1799）· 完成

- 累计 entries=1800。本轮写完 1500–1799（300 段），未重做 0–1499。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=1800`，`source_reviewed=1798`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：卷八日时断续（乙/丙/丁/戊日时诸断）→ 卷九起（六己日时断至己丑日壬申等）。
- 条件/救应/反转/未知已写入；图像占位与残讹不补字；命例≠golden。
- worktree：`fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## Checkpoint 7（索引 1800–2099）· 完成

- 累计 entries=2100。本轮写完 1800–2099（300 段），未重做 0–1799。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=2100`，`source_reviewed=2098`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：卷九日时断续（己/庚/辛/壬日时诸断等）。
- 条件/救应/反转/未知已写入；图像占位与残讹不补字；命例≠golden。
- worktree：`fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## Checkpoint 8（索引 2100–2339）· 完成 · 全书注解收尾

- 累计 entries=2340 / 2340。本轮写完 2100–2339（240 段），未重做 0–2099；未回改 CP5 质量账本条目。
- 校验：`PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py --annotations references/annotations/bazi/sanming-tonghui--shidian-HY1521.json --json` → `ok=true`，`entries=2340`，`source_reviewed=2338`，`errors=[]`。
- `verified` 全部 false。全书 draft 仍仅 CP1 两处：`P7467786007220338740`、`P7458198190622310419`。
- 本段覆盖：卷九癸日时断收束 → 卷十/看命口诀 → 卷十一/十二诸赋论收束（止于 `P7490505784620105791`）。
- 条件/救应/反转/未知已写入；图像占位与残讹不补字；命例≠golden。
- remaining **0**；nextId 无（全书段落注解覆盖完成）。
- worktree：`fateradar-multica-ming-98`；分支 `codex/multica-ming-98`。

## 状态

识典 HY1521《三命通会》段落注解已全覆盖，待协调验收/派下包。人工 `verified` 未伪造。
