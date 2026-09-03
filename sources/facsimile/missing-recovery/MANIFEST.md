# 定向影印恢复记录

检索日期：2026-09-04。检索范围仅限 Wikimedia Commons、Internet Archive、Google
Books 公版入口、Harvard/NLC/CADAL 公开入口；未使用现代付费版，也未批量抓取
CText。结果是“有限检索”，未找到不代表世界范围内不存在其他底本。

## 已排除的误匹配

### 四库全书 0703 册

- 检索候选：`文淵閣四庫全書_0703冊.djvu`
- 来源：Wikimedia Commons 文件页：<https://commons.wikimedia.org/wiki/File:%E6%96%87%E6%B7%B5%E9%96%A3%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8_0703%E5%86%8A.djvu>
- 核对结果：该册实际收录《戒子通录》《知言》《明本释》《少仪外传》《丽泽论说集录》《曾子全书》《子思子全书》《迩言》《木钟集》，不含《入地眼全书》。因此本地候选文件已排除，不进入公开语料库。

## 找到候选但本轮不下载

### 入地眼全书相关四库册

- `文淵閣四庫全書_0731冊.djvu`：Wikimedia Commons，111,426,434 bytes，超过 100 MB；直链：<https://upload.wikimedia.org/wikipedia/commons/a/ab/%E6%96%87%E6%B7%B5%E9%96%A3%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8_0731%E5%86%8A.djvu>
- `文淵閣四庫全書_0710冊.djvu`：Wikimedia Commons，107,964,924 bytes，超过 100 MB；直链：<https://upload.wikimedia.org/wikipedia/commons/d/d3/%E6%96%87%E6%B7%B5%E9%96%A3%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8_0710%E5%86%8A.djvu>

这两册尚未确认是否包含《入地眼全书》正文，因此仅登记，不视为已恢复。

## 本轮未找到可直接恢复的明确同书扫描

下列 14 本在允许范围内未找到“明确同书且单文件小于 100 MB”的可下载影印件；仓库中仍只有对应蒸馏包和来源锚点：

- 穷通宝鉴：Commons 无明确同书文件；Internet Archive 结果为现代套装，不采用。
- 黄金策：Commons 结果均为无关文件；未找到合适扫描。
- 梅花易数：Commons 仅返回《梅花心易掌中指南》等近名书，不视为同书；未下载。
- 增删卜易：Commons 无明确同书文件；未找到合适扫描。
- 青囊经：Commons 无明确同书文件；未找到合适扫描。
- 入地眼全书：0703 册已经核对为误匹配；0731、0710 两册尚未确认包含正文，因此不能计为已经恢复。
- 阳宅十书：Commons 搜索未返回明确同书文件；未找到合适扫描。
- 冰鉴：Commons 结果为青铜器图片或无关资料；未找到古籍扫描。
- 神相全编：Commons 返回《神相水镜集全编》，题名和书系不同，未作为同书下载。
- 玉匣记：Commons 结果为残本图片但非可确认完整底本；未下载。
- 果老星宗：Internet Archive 有 `guolaoxingzong` 等条目，但本轮未确认版本/文件许可及完整度，未下载。
- 紫微斗数全书：Internet Archive 有现代整理/今注条目，不采用；Commons 未找到明确文件。
- 兰台妙选：Commons 无明确同书文件；未找到合适扫描。
- 沈氏玄空学：Commons 结果为《沈氏日旦》等无关文件；Internet Archive 未找到合适扫描。

## 备注

- 本轮没有接受新的影印底本；唯一下载候选经目录核对后确认为误匹配，已排除。
- “未找到”是本轮有限检索结论，不是对馆藏世界范围的否定。
- `太微赋` 是《紫微斗数全书》的分出 section pack，恢复时应优先定位该书的同一影印底本，不应把现代单篇网页当作原始扫描。

## 仅摘录或 section pack

- 奇门法窍：目前只有 `sources/excerpts/qimen-faqiao-chaibu-v1.md` 的卷六核验摘录，没有全书或影印件。
- 太微赋：是从《紫微斗数全书》分出的 section pack，有独立结构化包和规范化文本，但没有独立影印本；应随母书底本定位。
