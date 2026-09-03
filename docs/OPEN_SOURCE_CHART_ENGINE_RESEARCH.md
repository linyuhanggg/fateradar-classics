# FateRadar 开源排盘引擎调研

> 调研日期：2026-09-04。仓库活跃度、版本和许可证可能变化；真正接入时必须锁定提交，并再次核对该提交的许可证。

## 一句话结论

**FateRadar 不继承 mingli_web 的旧算法；新排盘采用“成熟开源库只负责历法和天文底座，FateRadar 按古籍原包重新实现各术数规则”的路线。八字先做，紫微可直接借 iztro 排盘底座，七政借 Astronomy Engine 天文底座，六爻、奇门、大六壬自研。**

这里的“自研”不是重写公历、农历、节气和行星位置。那些是成熟、重复的基础计算。我们要重写的是术数口径、流派规则、输出合同和测试。

## 目标架构：排盘和 AI 追问彻底分开

```text
出生/起局资料
    ↓
校时层：时区、历史夏令时、经度、真太阳时策略
    ↓
确定性排盘层：浏览器和 Node 共用同一份 TypeScript 内核
    ↓
立即显示结构化命盘 JSON
    ↓（后台保存和复核，不挡首屏）
chart_id + engine_version + school + time_policy

用户提出问题
    ↓
服务器根据术数、盘面事实和问题检索古籍原包
    ↓
只取少量相关原文和规则，附书名、篇章、定位
    ↓
AI 边生成边显示回答
```

排盘阶段不调用大模型，不读取整套古籍，不进入慢队列。古籍也不打进浏览器包。AI 只能读取排盘层已经确认的事实，不能重新算四柱、宫位或星曜。

前端和服务器不能各用一套算法。推荐发布同一个 TypeScript 包：浏览器先计算并显示，服务器用同版本包复核和保存。两边结果不一致时，阻止深读并报告版本差异，但不能让后台复核挡住基础盘首次显示。

## 校时层必须单独建设

现有候选库没有一个能完整包办 FateRadar 的真太阳时需求。新项目需要独立的校时模块，输入至少包括：

- 当地民用年月日时分；
- IANA 时区，例如 `Asia/Shanghai`；
- 出生地经纬度；
- 是否采用真太阳时，以及采用它的术数和流派；
- 历史夏令时处理结果；
- 原始时间、校正后时间和校正明细。

基本流程是：民用时间先按当地时区和历史夏令时换成标准时刻，再做经度差修正和均时差修正，最后把明确的“排盘用时刻”交给术数引擎。真太阳时不能写成全局强制开关：八字、紫微、奇门等不同流派可能采用不同时间口径，必须随 `time_policy` 保存。

地理编码只负责把地名变成经纬度；它不是排盘算法。找不到精确地点时，应让用户确认城市或坐标，不能让 AI 猜。

## 基础库结论

### 1. tyme4ts：新历法主底座

- 语言和运行环境：TypeScript，提供 ESM、CommonJS 和类型声明，可用于浏览器与 Node。
- 许可证：MIT，可用于商业项目，但必须保留版权和许可证声明。
- 能力：公历、农历、干支、节气、八字等；官方文档说明节气算法来自寿星天文历，并提供八字子时流派扩展方式。
- 测试和维护：仓库包含八字、节气、公历时间、农历等多类测试；2026 年仍有发布和提交记录。接入前仍要跑 FateRadar 自己的边界课例，不能把库内测试当成产品验收。
- 缺口：不负责地点查询，也不能替代完整的真太阳时策略；古籍流派、神煞取舍、格局和断法仍属于 FateRadar。
- 结论：**采用，但只把它当历法、四柱和运限计算底座；对外合同由 FateRadar 自己定义。**

官方来源：[Tyme 官方说明](https://6tail.cn/tyme.html) · [tyme4ts 仓库](https://github.com/6tail/tyme4ts) · [package.json](https://github.com/6tail/tyme4ts/blob/master/package.json)

### 2. lunar-javascript：仅作旧实现对拍

- 语言和运行环境：JavaScript，无第三方依赖，可直接用于普通网页和 Node。
- 许可证：MIT，可商用并保留许可证。
- 能力：公农历转换、节气、干支、八字、十神、大运等，仓库有八字、节气和大运测试。
- 维护风险：作者已明确说明 Lunar 后续不再增加新特性，只修 bug，并推荐新项目使用 Tyme。
- 结论：**不作为 FateRadar 新底座。只在迁移和边界差分测试中对拍。**

官方来源：[lunar-javascript 仓库](https://github.com/6tail/lunar-javascript) · [官方维护说明](https://6tail.cn/calendar/overview.html) · [测试目录](https://github.com/6tail/lunar-javascript/tree/master/__tests__)

### 3. sxtwl_cpp：离线历法对拍，不进首屏运行时

- 语言和运行环境：C++，通过 SWIG 暴露 Python、Java、Lua 等接口；官方没有直接的浏览器/Node TypeScript 包。
- 许可证：BSD-3-Clause，可商用并遵守版权、声明和不得借作者名义背书等条件。
- 能力：基于寿星天文历，提供公农历、干支、节气及节气儒略日等能力。
- 测试和维护风险：仓库以示例、跨平台构建和旧 CI 为主，没有像 tyme4ts、iztro 那样清晰的领域单测目录；原生构建也会增加 Web 部署、冷启动和跨平台成本。
- 结论：**不作为浏览器或 Node 主运行时。用于开发期、离线任务和节气边界的第二来源对拍。**

官方来源：[sxtwl_cpp 仓库](https://github.com/yuangu/sxtwl_cpp) · [Python 接口示例](https://github.com/yuangu/sxtwl_cpp/blob/master/python/README.md) · [BSD-3-Clause 许可证](https://github.com/yuangu/sxtwl_cpp/blob/master/LICENSE)

### 4. iztro：紫微排盘底座

- 语言和运行环境：TypeScript/JavaScript，提供 Node 包、类型声明和浏览器构建。
- 许可证：MIT，可商用并保留许可证。
- 能力：十二宫、星曜、四化、大限、小限、流年、流月、流日、流时；支持通行版本和中州派等配置。
- 测试和维护：仓库有 Jest、覆盖率工作流和分模块测试；截至调研日仍持续维护。接入时必须锁版本，不能自动漂移升级。
- 缺口：官方排盘接口主要接收日期和时辰序号，不负责出生地、IANA 时区或完整真太阳时。流派配置是全局状态，服务端并发使用时要先验证隔离方式，不能让不同用户的流派互相污染。
- 结论：**采用为紫微固定盘底座，外面包 FateRadar 适配器；古籍规则、证据和解读自研。**

官方来源：[iztro 仓库](https://github.com/SylarLong/iztro) · [排盘接口](https://docs.iztro.com/en_US/posts/astrolabe) · [配置和插件](https://docs.iztro.com/posts/config-n-plugin) · [MIT 许可证](https://github.com/SylarLong/iztro/blob/main/LICENSE)

### 5. Astronomy Engine：七政四余天文底座

- 语言和运行环境：项目提供 JavaScript/TypeScript、Python、C 等版本；JavaScript 版同时支持浏览器和 Node。
- 许可证：MIT，可商用并保留许可证。
- 能力：太阳、月亮和主要行星的位置，黄道/赤道坐标转换，以及按观测者经纬度计算的相关天文量。
- 测试和维护：项目官方说明其计算会与 NOVAS、JPL Horizons 等来源做单元验证，并把误差目标写为 ±1 角分。这是上游项目声明，不是 FateRadar 已完成的精度验收；七政接入后仍需用独立星历和古籍课例验证。
- 缺口：它不是七政四余排盘库，不会替我们决定二十八宿距星、罗计孛紫、宫制、庙旺或古法流派。
- 结论：**采用为日月五星天文底座；七政四余的传统规则和盘面合同自研。**

官方来源：[Astronomy Engine 仓库](https://github.com/cosinekitty/astronomy) · [JavaScript/TypeScript 文档](https://github.com/cosinekitty/astronomy/blob/master/source/js/README.md) · [MIT 许可证](https://github.com/cosinekitty/astronomy/blob/master/LICENSE)

### 6. Swiss Ephemeris：当前排除

- 语言和运行环境：核心为 C，通常用于服务器或原生绑定，不是轻量浏览器优先方案。
- 许可证：官方实行 AGPL 与商业许可证双轨。若免费采用 AGPL，网络服务的整体开源义务可能与 FateRadar 商业计划冲突；另一条路是购买商业授权。
- 能力：专业级日月行星、节点和星历计算，适合对精度要求更高的后续七政服务。
- 结论：**当前排除。只有在七政验收证明 Astronomy Engine 精度或能力不足，并完成商业许可采购后，才考虑服务器端替换。**

官方来源：[Swiss Ephemeris 官方说明](https://www.astro.com/swisseph/) · [官方许可章节](https://www.astro.com/swisseph-download/doc/swisseph.pdf) · [官方商业许可说明](https://www.astro.com/faq/fq_swe_prog_e.htm)

## 分术数推荐

### 八字

**方案：tyme4ts 历法底座 + FateRadar 自研八字领域层。**

第一期只做确定性事实：校时、四柱、藏干、十神、纳音、旬空、大运顺逆、起运时间、大运、流年。格局、旺衰、用神和神煞属于古籍与流派层，不能从旧算法搬过来，也不能让 AI 现场发明。

`lunar-javascript` 和 `sxtwl_cpp` 只用来找差异。若三者不同，应回到古籍口径、节气时刻和时间政策裁决，不按多数票决定。

### 紫微

**方案：iztro 固定盘 + FateRadar 校时、适配器、古籍规则和证据层。**

先固定采用的流派、闰月处理、早晚子时、年界和运限边界，再冻结 iztro 版本。FateRadar 只接收自己的输入合同并输出自己的结构化 JSON，不能让前端页面直接依赖 iztro 内部对象。

### 七政四余

**方案：Astronomy Engine 天文位置 + FateRadar 自研传统星命层。**

经纬度、UTC 换算和观测时刻是必填事实。二十八宿边界、罗喉计都、月孛、紫气、命身宫和宫度体系应分别标注算法来源与精度层级。初期不采用 Swiss Ephemeris；只有实测不达标时再评估付费授权。

### 六爻

**方案：自研纯 TypeScript 小内核。**

六十四卦、京房八宫、纳甲、六亲、六神、世应、旬空和动变规则规模不大，适合直接按古籍原包实现。Python 项目 [`bopo/najia`](https://github.com/bopo/najia) 为 MIT 且有测试，可作开发期对拍；但其代码长期少更新、不能直接运行于浏览器，因此不作为生产依赖。

### 奇门

**方案：自研，并显式区分拆补、置闰、茅山、转盘和飞盘等口径。**

可用于对拍的公开项目包括：

- [`3meta`](https://github.com/3metaJun/3meta)：TypeScript、MIT，有分模块测试，但项目历史较短；
- [`qfdk/qimen`](https://github.com/qfdk/qimen)：Node/JavaScript，项目较老且有少量排盘测试，但侧重茅山派转盘；仓库许可证与 `package.json` 的许可证标记不一致，未澄清前不复制代码；
- [`qimen-dunjia`](https://github.com/arc119226/qimen_dunjia)：JavaScript、MIT、浏览器/Node 可用且有 CI，但项目较新，并依赖已进入维护期的 lunar-javascript。

结论：**三者都只对拍，不直接采用为 FateRadar 真值。**

### 大六壬

**方案：自研 TypeScript 内核。**

[`kinliuren`](https://github.com/kentang2017/kinliuren) 为 MIT/Python，覆盖天地盘、四课、三传、天将和部分神煞，可作结构和样例对拍。但其接口要求调用方先提供节气、农历月、日干支和时干支，仓库也没有清晰的自动测试目录。因此**不作为生产依赖，只作对拍材料**。

## 采用、对拍、排除清单

| 类别 | 项目 | 用途 |
| --- | --- | --- |
| 采用 | tyme4ts | 历法、节气、四柱和运限基础 |
| 采用 | iztro | 紫微固定盘底座 |
| 采用 | Astronomy Engine | 七政日月五星天文位置 |
| 仅对拍 | lunar-javascript | 八字和历法旧实现差分 |
| 仅对拍 | sxtwl_cpp | 节气、干支、历法第二来源 |
| 仅对拍 | bopo/najia | 六爻纳甲差分 |
| 仅对拍 | 3meta、qfdk/qimen、qimen-dunjia | 奇门多实现差分 |
| 仅对拍 | kinliuren | 大六壬结构和课例差分 |
| 排除 | Swiss Ephemeris 免费版 | AGPL 与商业闭源计划冲突 |
| 排除 | 无明确许可证的聚合命理仓库 | 公开可见不等于允许复制和商用 |
| 排除 | mingli_web 旧算法及其 Runtime 制品 | 架构臃肿、口径难审计；本项目明确不继承 |

## 测试原则

上游库通过自己的测试，不等于 FateRadar 的术数口径正确。新引擎至少要建立以下固定样本：

1. 节气交接前后、立春前后、23 点换日和早晚子时；
2. 历史夏令时、跨时区、经度校正和真太阳时跨时辰；
3. 农历闰月、紫微闰月处理和流派切换；
4. 八字起运、大运顺逆和边界年龄；
5. 每个术数从古籍原包提取的完整课例；
6. 同一输入在浏览器和 Node 产生完全相同的结构化结果；
7. 与两个独立实现出现差异时，记录差异和最终采用的古籍口径。

性能必须实测，不能引用上游宣传。首期目标建议定义为：基础八字排盘不发网络请求即可显示；记录浏览器端 P50/P95、包体积和低性能设备耗时。七政等较重模块按页面懒加载，不能拖慢首页和八字页面。

## 落地阶段

### 阶段 0：冻结合同

- 明确 FateRadar 是新项目，不继承旧算法；
- 定义统一输入、校时结果、盘面 JSON、流派和版本字段；
- 从古籍原包整理八字金标课例和来源定位；
- 锁定第三方库提交与许可证副本。

### 阶段 1：校时和历法底座

- 完成时区、历史夏令时、经度和均时差模块；
- 接入 tyme4ts 适配器；
- 用 lunar-javascript、sxtwl_cpp 和固定课例做一次边界差分；
- 差异裁决后冻结 FateRadar 时间政策。

### 阶段 2：八字秒排盘样板

- 自研八字领域层，不搬旧代码；
- 浏览器和 Node 共用一份 TypeScript 包；
- 首屏只展示确定性事实；
- 服务器后台保存相同版本的 `chart_id`；
- 古籍检索和 AI 追问另走流式接口。

### 阶段 3：紫微

- 用适配器封装 iztro；
- 冻结流派、时间和闰月政策；
- 古籍原包负责新增规则与证据，不改 iztro 内部代码。

### 阶段 4：七政四余

- 接入 Astronomy Engine；
- 建立独立星历对照和边界样本；
- 自研传统宫度、星曜和古法规则；
- 只有实测证明确有需要，才采购并评估 Swiss Ephemeris。

### 阶段 5：六爻、奇门、大六壬

- 按古籍原包逐术实现；
- 每次只上线一个明确流派；
- 开源项目只作为差分来源，不把多个项目拼成无法解释的混合算法。

## 最终验收口径

新排盘引擎完成，不是“页面能显示一个盘”，而是同时满足：

- 旧算法零继承；
- 浏览器和服务器共用同一版本内核；
- 时间、流派和第三方版本可追溯；
- 古籍原包能定位每条自研规则；
- 边界课例和跨实现差分已有明确裁决；
- 基础排盘不依赖 AI、古籍全文加载或后台队列；
- AI 只解释已冻结的盘面事实，并能展示古籍出处。
