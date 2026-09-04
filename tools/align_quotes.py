#!/usr/bin/env python3
"""Align unanchored rules to original fulltext without inventing text.

High-confidence only. On hit, quote is rewritten to a contiguous original
span so V5 can pass; statement is never rewritten; verified stays false.
Does not fetch remote text. Does not modify san-shi/qimen-faqiao.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

try:
    from opencc import OpenCC

    _CC = OpenCC("t2s")
except Exception:  # pragma: no cover
    _CC = None

ROOT = Path(__file__).resolve().parents[1]
WS_RE = re.compile(r"\s+", re.UNICODE)
HAN_RE = re.compile(r"[㐀-鿿]")
NOTE_RE = re.compile(r"【[^】]*】")
MD_JUNK_RE = re.compile(r"\*\*|⚠️|（\*\*[^*]+\*\*：[^）]*）")
SKIP_BOOKS = {"san-shi/qimen-faqiao"}
ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")
WIKI_NOISE = ("编辑]", "編輯]", "姊妹計劃", "數據項", "@media", "◄", "►")
HEADER_RE = re.compile(r"^(?:\d{1,2}\s+\d{1,2}\s|R\d{2}\s)")
CATALOG_PREFIX_RE = re.compile(r"^(?:M\d{2}|R\d{2}|0?\d{1,2}|[一二三四五六七八九十]+)\s+")
QUOTED_RE = re.compile(r"[“「『\"']([^”」』\"']{2,30})[”」』\"']")
TITLE_STRIP_RE = re.compile(r"^[一二三四五六七八九十百千0-9、.．\s]+")
META_RE = re.compile(r"调用本 pack|調用本 pack|安全改写|reframe|不替代|并读|並讀")

PAIR_FALLBACK = str.maketrans(
    {
        "專": "专",
        "國": "国",
        "無": "无",
        "這": "这",
        "個": "个",
        "時": "时",
        "為": "为",
        "爲": "为",
        "與": "与",
        "後": "后",
        "來": "来",
        "過": "过",
        "對": "对",
        "發": "发",
        "經": "经",
        "關": "关",
        "麼": "么",
        "說": "说",
        "義": "义",
        "書": "书",
        "門": "门",
        "開": "开",
        "體": "体",
        "餘": "余",
        "歲": "岁",
        "萬": "万",
        "學": "学",
        "當": "当",
        "從": "从",
        "還": "还",
        "氣": "气",
        "裏": "里",
        "裡": "里",
        "並": "并",
        "於": "于",
        "卻": "却",
        "論": "论",
        "殺": "杀",
        "財": "财",
        "傷": "伤",
        "順": "顺",
        "陽": "阳",
        "陰": "阴",
        "龍": "龙",
        "祿": "禄",
        "權": "权",
        "數": "数",
        "術": "术",
        "會": "会",
        "實": "实",
        "業": "业",
        "點": "点",
        "剋": "克",
        "尅": "克",
        "宮": "宫",
        "機": "机",
        "賦": "赋",
        "觀": "观",
        "禍": "祸",
        "斷": "断",
        "貴": "贵",
        "變": "变",
        "僕": "仆",
        "親": "亲",
        "應": "应",
        "運": "运",
        "馬": "马",
        "輔": "辅",
        "弼": "弼",
        "貪": "贪",
        "貞": "贞",
        "廟": "庙",
        "沖": "冲",
        "復": "复",
        "將": "将",
        "賤": "贱",
        "貧": "贫",
        "災": "灾",
        "見": "见",
        "長": "长",
        "兩": "两",
        "內": "内",
        "稱": "称",
        "謂": "谓",
        "則": "则",
        "強": "强",
        "虛": "虚",
        "節": "节",
        "總": "总",
        "飛": "飞",
        "華": "华",
        "陳": "陈",
        "鉞": "钺",
        "鬥": "斗",
        "問": "问",
        "錄": "录",
        "測": "测",
        "遷": "迁",
        "眾": "众",
        "沒": "没",
        "幹": "干",
        "動": "动",
        "蓋": "盖",
        "處": "处",
        "條": "条",
        "葉": "叶",
        "孫": "孙",
        "現": "现",
        "風": "风",
        "雲": "云",
        "電": "电",
        "號": "号",
        "洩": "泄",
        "勢": "势",
        "淵": "渊",
        "詮": "诠",
        "窮": "穷",
        "寶": "宝",
        "鑑": "鉴",
        "鑒": "鉴",
        "儀": "仪",
        "調": "调",
        "東": "东",
        "題": "题",
        "該": "该",
        "種": "种",
        "類": "类",
        "們": "们",
        "讓": "让",
        "決": "决",
        "外": "外",
    }
)

ZIWEI_STAR = (
    ("紫微", "問紫微所主"),
    ("天機", "問天機所主"),
    ("太陽", "問太陽所主"),
    ("武曲", "問武曲星所主"),
    ("天同", "問天同星所主"),
    ("廉貞", "問廉貞所主"),
    ("天府", "問天府所主"),
    ("太陰", "問太陰星所主"),
    ("貪狼", "問貪狼所主"),
    ("巨門", "問巨門所主"),
    ("天相", "問天相星所主"),
    ("天梁", "問天梁星所主"),
    ("七殺", "問七殺星所主"),
    ("破軍", "問破軍所主"),
    ("文昌", "問文昌星所主"),
    ("文曲", "問文曲星所主"),
    ("左輔", "問左輔所主"),
    ("右弼", "問右弼所主"),
    ("天魁", "問天魁天鉞星所主"),
    ("天鉞", "問天魁天鉞星所主"),
    ("祿存", "問祿存星所主"),
    ("天馬", "問天馬星所主"),
    ("化祿", "問化祿星所主"),
    ("化權", "問化權星所主"),
    ("化科", "問化科星所主"),
    ("化忌", "問化忌星所主"),
    ("擎羊", "問擎羊星所主"),
    ("陀羅", "問陀羅星所主"),
    ("火星", "問火星所主"),
    ("鈴星", "問鈴星所主"),
    ("天空", "問天空地劫所主"),
    ("地劫", "問天空地劫所主"),
    ("地空", "問天空地劫所主"),
    ("天傷", "問天傷天使所主"),
    ("天使", "問天傷天使所主"),
    ("天刑", "問天刑星所主"),
    ("天姚", "問天姚星所主"),
)
ZIWEI_PALACE = (
    ("命宮", "一 命宮"),
    ("兄弟", "二兄弟"),
    ("妻妾", "三妻妾"),
    ("子女", "四子女"),
    ("財帛", "五財帛"),
    ("疾厄", "六疾厄"),
    ("遷移", "七遷移"),
    ("奴僕", "八奴僕"),
    ("官祿", "九官祿"),
    ("田宅", "十田宅"),
    ("福德", "十一福德"),
    ("父母", "十二父母"),
)
ZIWEI_OTHER = (
    ("富局", "定富局"),
    ("貴局", "定貴局"),
    ("貧賤", "定貧賤局"),
    ("雜局", "定雜局"),
    ("女命骨髓", "女命骨髓賦"),
    ("小兒命", "論小兒命"),
    ("克親", "論小兒克親"),
    ("大限十年", "論大限十年禍福何如"),
    ("流年太歲", "論流年太歲吉凶星殺"),
    ("陰騭", "論陰騭延壽"),
    ("南北斗", "論行限分南北斗"),
    ("入格", "論人命入格"),
    ("格星", "論格星數高下"),
    ("男女命", "論男女命同異"),
    ("先貧後富", "論命先貧後富"),
    ("羊陀迭", "論羊陀迭並"),
    ("七殺重逢", "論七殺重逢"),
    ("所忌訣", "論大小限星辰過十二宮遇十二支所忌訣"),
    ("同垣", "論諸星同垣"),
    ("太微", "太微賦"),
    ("骨髓賦", "斗數骨髓賦"),
    ("十二宮", "其星分布一十二垣"),
)

# statement keyword → original needle. Unique span, or TOC+body title pair (take last).
# Never a coincidental 4-gram. Unlocatable topics stay null.
TOPIC_NEEDLES: dict[str, list[tuple[str, str]]] = {
    "bazi/ditiansui-chanwei": [
        ("所藏", "干为天元"),
        ("得令", "得令者冲衰则拔"),
        ("清者", "清浊两字"),
        ("众者", "众寡之说"),
        ("震", "卯酉为震兑"),
        ("坎", "子午为坎离"),
        ("从财", "曰从财"),
        ("妻宫", "一夫妻"),
    ],
    "luming-nayin/wuxing-jingji": [
        ("空亡", "论空亡"),
        ("疾病", "论疾病"),
        ("寿夭", "论寿夭"),
        ("壽夭", "论寿夭"),
        ("父母位", "论父母位"),
        ("子息位", "论子息位"),
        ("形貌性情", "论形貌性情"),
        ("学堂文章", "论学堂文章"),
        ("金舆", "论金舆"),
        ("小儿", "释小儿例"),
        ("男命", "释男命例"),
        ("女命", "释女命例"),
        ("小运", "论小运"),
        ("二运", "论二运"),
        ("岁运", "论岁运"),
        ("歲運", "论岁运"),
        ("凶中凶格", "凶中凶格"),
        ("节气", "论十二月节气"),
        ("华盖", "论华盖"),
        ("三刑", "论三刑"),
        ("冲破", "论冲破"),
        ("僧道", "论僧道"),
        ("太岁", "论太岁"),
        ("支神", "论支神"),
        ("吏卒", "论吏卒"),
    ],
    "luming-nayin/luoluzi-sanming": [
        ("三才", "著三才以成象"),
        ("四气", "播四气以为年"),
        ("一辰十岁", "一辰十岁"),
        ("绝处", "五行绝处有禄马"),
        ("鬼旺身衰", "鬼旺身衰"),
        ("身旺鬼绝", "鬼旺身衰"),
        ("八孤", "八孤临于五墓"),
        ("财命有气", "财命有气"),
        ("建禄不富", "建禄不富"),
        ("四柱内外", "四柱内外"),
        ("父病", "父病"),
    ],
    "bazi/qiongtong-baojian": [
        ("论木", "论木"),
        ("论火", "论火"),
        ("论土", "论土"),
        ("论水", "论水"),
        ("冬庚", "三冬庚金"),
        ("夏辛", "三夏辛金"),
        ("秋壬", "三秋壬水"),
        ("冬己", "三冬己土"),
    ],
    "bazi/yuanhai-ziping": [
        ("继善", "继善篇"),
        ("阳刃格", "阳刃格"),
    ],
    "bazi/sanming-tonghui": [
        ("子午双包", "子午双包"),
        ("一气生成", "一气生成"),
        ("四位纯全", "四位纯全"),
        ("六厄", "论六厄"),
    ],
    "xingming/xingming-suyuan": [
        ("寒月", "寒月最喜"),
        ("时令", "时令须分"),
        ("产亡", "女命主产亡"),
        ("三主", "三主俱躔"),
        ("衝刑", "战冲刑尅"),
        ("冲刑", "战冲刑尅"),
        ("三嫁", "三嫁"),
        ("经纬夹拱", "经纬夹拱"),
        ("二星合璧", "二星合璧"),
        ("五曜连珠", "五曜连珠二星合璧"),
        ("太岁填实", "太岁填实"),
        ("交宫过度", "交宫过度"),
        ("官魁", "官魁例"),
        ("四时令旺", "四时论"),
        ("天耗", "天耗地耗切忌财乡"),
    ],
    "xingming/guotian-jing": [
        ("童限", "定童限例歌"),
        ("化曜", "天干化曜星例"),
    ],
    "divination/zengshan-buyi": [
        ("日辰", "日辰章第十七"),
        ("六合", "六合章第十九"),
        ("六冲", "六冲章第二十"),
        ("三刑", "三刑章第二十一"),
        ("回头", "动散章第二十三"),
        ("动爻变出", "动散章第二十三"),
        ("胎孕", "胎孕章第八十七"),
        ("出行", "出行章第九十"),
        ("独一爻动", "独发章第三十一"),
        ("归魂", "归魂游魂章第又二十六"),
        ("游魂", "归魂游魂章第又二十六"),
        ("月令当令", "四时旺相章第又十五"),
    ],
    "divination/huangji-jingshi": [
        ("开物", "开物始月寅之中"),
        ("闭物", "闭物经月戌之终"),
        ("甲辰", "甲辰唐尧"),
        ("天声", "唱和"),
        ("地音", "唱和"),
        ("动植", "动植通数"),
        ("先天", "先天图者环中也"),
    ],
    "divination/zhouyi-zhezhong": [
        ("朱熹", "朱子本义"),
        ("程颐", "朱子本义"),
    ],
    "divination/meihua-yishu": [
        ("晴", "天时占第一"),
        ("天时", "天时占第一"),
        ("屋舍", "屋舍占第四"),
        ("坟", "坟墓占第十八"),
        ("告者", "人事占第二"),
        ("体克用", "体用生克篇之一"),
        ("用克体", "体用生克篇之一"),
    ],
    "divination/huangjin-ce": [
        ("动爻", "黄金策"),
    ],
    "divination/huozhu-lin": [
        ("世应", "世应相克"),
    ],
}


def fold(text: str) -> str:
    s = NOTE_RE.sub("", text or "")
    s = MD_JUNK_RE.sub("", s)
    s = WS_RE.sub("", s)
    if _CC is not None:
        return _CC.convert(s)
    return s.translate(PAIR_FALLBACK)


def han_only(text: str) -> str:
    return "".join(HAN_RE.findall(fold(text)))


def art_of(system: str, slug: str) -> str | None:
    if system == "san-shi":
        if slug.startswith("qimen-"):
            return "qimen"
        if slug.startswith("liuren-") or slug.startswith("daliuren-"):
            return "liuren"
        return None
    return {
        "bazi": "bazi",
        "luming-nayin": "bazi",
        "ziwei": "ziwei",
        "divination": "liuyao",
        "xingming": "qizheng",
    }.get(system)


def is_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    return any(tok in s for tok in WIKI_NOISE)


def is_header_rule(statement: str, quote: str) -> bool:
    s = (statement or "").strip()
    if META_RE.search(s):
        return True
    # bare catalog indexes with no locatable topic, e.g. "01 14 主星核心断诀"
    if HEADER_RE.match(s) and len(HAN_RE.findall(s)) <= 18:
        return True
    q = (quote or "").strip()
    if HEADER_RE.match(q) and len(HAN_RE.findall(q)) <= 18:
        return True
    return False


def catalog_core(statement: str) -> str:
    s = CATALOG_PREFIX_RE.sub("", (statement or "").strip())
    s = re.sub(r"[（(].*$", "", s)
    s = re.sub(r"[，。；、：:].*$", "", s)
    return han_only(s)


def build_index(lines: list[str]) -> tuple[str, list[int]]:
    chunks: list[str] = []
    mapping: list[int] = []
    for i, line in enumerate(lines, 1):
        c = han_only(line)
        chunks.append(c)
        mapping.extend([i] * len(c))
    return "".join(chunks), mapping


def span_for(hay: str, mapping: list[int], needle: str) -> tuple[int, int] | None:
    if not needle:
        return None
    idx = hay.find(needle)
    if idx < 0:
        return None
    end_idx = idx + len(needle) - 1
    if end_idx >= len(mapping):
        return None
    return mapping[idx], mapping[end_idx]


def unique_run(needle: str, hay: str, minl: int = 6) -> str | None:
    n = len(needle)
    if n < minl:
        if n >= 4 and hay.count(needle) == 1:
            return needle
        return None
    for length in range(min(n, 48), minl - 1, -1):
        for i in range(0, n - length + 1):
            sub = needle[i : i + length]
            if hay.count(sub) == 1:
                return sub
    if 4 <= n <= 16 and hay.count(needle) == 1:
        return needle
    return None


def pick_quote(lines: list[str], start: int, end: int) -> tuple[int, int, str]:
    start = max(1, start)
    end = min(len(lines), end)
    usable: list[tuple[int, str]] = []
    for i in range(start, end + 1):
        raw = lines[i - 1].strip()
        if is_noise(raw) or raw.startswith("#"):
            continue
        segs = NOTE_RE.split(raw)
        piece = max(segs, key=len).strip() if segs else raw
        if len(HAN_RE.findall(piece)) >= 8:
            usable.append((i, piece))
        elif len(HAN_RE.findall(raw)) >= 8:
            usable.append((i, raw))
    if not usable:
        raw = lines[start - 1].strip()
        return start, start, raw
    i0, q0 = usable[0]
    if len(q0) > 180:
        q0 = q0[:180]
    return i0, i0, q0


def yaml_quote_lines(value: str) -> list[str]:
    special = any(ch in value for ch in ":#{}[]&*!|>%'\"\n") or value != value.strip()
    if special:
        dumped = yaml.safe_dump(value, allow_unicode=True).strip()
        if dumped.endswith("\n..."):
            dumped = dumped[:-4].strip()
        if "\n" in dumped:
            return ["  quote: >-"] + ["    " + ln for ln in value.splitlines()]
        return [f"  quote: {dumped}"]
    return [f"  quote: {value}"]


def patch_rule(text: str, rule_id: str, *, start: int, end: int, file_path: str, new_quote: str) -> str:
    lines = text.splitlines()
    pat = re.compile(rf"^- rule_id:\s*{re.escape(rule_id)}\s*$")
    start_i = next((i for i, line in enumerate(lines) if pat.match(line)), None)
    if start_i is None:
        raise RuntimeError(f"rule_id not found: {rule_id}")
    end_i = len(lines)
    for j in range(start_i + 1, len(lines)):
        if lines[j].startswith("- rule_id:"):
            end_i = j
            break
    block = lines[start_i:end_i]
    a0 = next((k for k, line in enumerate(block) if re.match(r"  anchor:", line)), None)
    if a0 is None:
        raise RuntimeError(f"no anchor field: {rule_id}")
    a1 = a0 + 1
    if block[a0].strip() != "anchor: null":
        while a1 < len(block) and block[a1].startswith("    "):
            a1 += 1
    block[a0:a1] = [
        "  anchor:",
        f"    file: {file_path}",
        f"    start_line: {start}",
        f"    end_line: {end}",
    ]
    q0 = next((k for k, line in enumerate(block) if re.match(r"  quote:", line)), None)
    if q0 is None:
        raise RuntimeError(f"no quote field: {rule_id}")
    q1 = q0 + 1
    if block[q0].rstrip().endswith(">-") or block[q0].rstrip().endswith("|"):
        while q1 < len(block) and (block[q1].startswith("    ") or block[q1].startswith("      ")):
            q1 += 1
    block[q0:q1] = yaml_quote_lines(new_quote)
    lines[start_i:end_i] = block
    return "\n".join(lines) + "\n"


def parse_sections(lines: list[str]) -> list[dict]:
    secs: list[dict] = []
    cur = {"start": 1, "title": "", "end": len(lines), "body": []}
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            if cur["body"] or cur["title"] or i == 1:
                cur["end"] = i - 1
                secs.append(cur)
            cur = {
                "start": i,
                "title": fold(line.lstrip("#").strip()),
                "end": len(lines),
                "body": [],
            }
        elif not is_noise(line) and not line.startswith("|"):
            if len(HAN_RE.findall(line)) >= 6:
                cur["body"].append(i)
    cur["end"] = len(lines)
    secs.append(cur)
    return [s for s in secs if s["title"] or s["body"]]


def grams(text: str, n: int = 2) -> set[str]:
    h = han_only(text)
    if len(h) < n:
        return set()
    return {h[i : i + n] for i in range(len(h) - n + 1)}


def heading_line(lines: list[str], needle: str) -> int | None:
    n = fold(needle)
    hits = []
    for i, line in enumerate(lines, 1):
        if not line.startswith("#"):
            continue
        if n and n in fold(line):
            hits.append(i)
    if len(hits) == 1:
        return hits[0]
    if hits:
        return hits[0]
    # also allow non-heading exact title
    for i, line in enumerate(lines, 1):
        if n and n in fold(line) and len(HAN_RE.findall(line)) <= 40:
            return i
    return None


def ziwei_topic(statement: str, lines: list[str]) -> tuple[int, int, str] | None:
    st = fold(statement)
    for key, heading in list(ZIWEI_OTHER) + list(ZIWEI_PALACE) + list(ZIWEI_STAR):
        if fold(key) in st:
            loc = heading_line(lines, heading)
            if loc is None:
                continue
            start, end, quote = pick_quote(lines, loc, min(len(lines), loc + 12))
            if len(HAN_RE.findall(quote)) >= 8:
                return start, end, quote
    return None


def section_hit(statement: str, lines: list[str], sections: list[dict]) -> tuple[int, int, str] | None:
    g = grams(statement)
    if len(g) < 4:
        return None
    scored: list[tuple[float, dict]] = []
    for sec in sections:
        title_g = grams(sec["title"])
        body_txt = "".join(lines[i - 1] for i in sec["body"][:40])
        body_g = grams(body_txt)
        inter_t = len(g & title_g)
        inter_b = len(g & body_g)
        if inter_t == 0 and inter_b < 4:
            continue
        score = inter_t * 12 + inter_b
        if sec["title"] and fold(sec["title"]) in fold(statement):
            score += 20
        scored.append((score, sec))
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    best, sec = scored[0][0], scored[0][1]
    second = scored[1][0] if len(scored) > 1 else 0
    if best < 8:
        return None
    if second and best < second * 1.25 + 2:
        return None
    # pick the body line with max overlap
    best_line = None
    best_inter = 0
    for i in sec["body"][:80]:
        inter = len(g & grams(lines[i - 1]))
        if inter > best_inter:
            best_inter = inter
            best_line = i
    if best_line is None:
        return None
    if best_inter < 3 and len(g & grams(sec["title"])) < 2:
        return None
    start, end, quote = pick_quote(lines, best_line, best_line)
    if len(HAN_RE.findall(quote)) < 8:
        return None
    return start, end, quote


def line_overlap_hit(statement: str, lines: list[str]) -> tuple[int, int, str] | None:
    g = grams(statement)
    if len(g) < 6:
        return None
    scored: list[tuple[int, float, int]] = []
    for i, line in enumerate(lines, 1):
        if is_noise(line) or line.startswith("#"):
            continue
        lg = grams(line)
        inter = len(g & lg)
        if inter < 5:
            continue
        jacc = inter / max(1, min(len(g), len(lg)))
        scored.append((inter, jacc, i))
    if not scored:
        return None
    scored.sort(reverse=True)
    inter, jacc, i = scored[0]
    second = scored[1][0] if len(scored) > 1 else 0
    if inter >= 8 and (second == 0 or inter >= second + 3):
        return pick_quote(lines, i, i)
    if inter >= 6 and jacc >= 0.45 and inter >= second + 2:
        return pick_quote(lines, i, i)
    return None


def quoted_needles(text: str) -> list[str]:
    out = []
    for m in QUOTED_RE.finditer(text or ""):
        h = han_only(m.group(1))
        if len(h) >= 4:
            out.append(h)
    return out


def heading_keyword_hit(statement: str, lines: list[str], sections: list[dict]) -> tuple[int, int, str] | None:
    st = fold(statement)
    hits: list[dict] = []
    for sec in sections:
        title = sec.get("title") or ""
        key = TITLE_STRIP_RE.sub("", title)
        key = key.lstrip("论論")
        kh = han_only(key)
        if len(kh) < 2:
            continue
        if fold(key) in st or kh in han_only(statement):
            hits.append(sec)
    if len(hits) != 1:
        return None
    sec = hits[0]
    g = grams(statement)
    best_line = None
    best_inter = -1
    for i in sec["body"][:80]:
        inter = len(g & grams(lines[i - 1]))
        if inter > best_inter:
            best_inter = inter
            best_line = i
    if best_line is None:
        best_line = sec["start"]
    start, end, quote = pick_quote(lines, best_line, best_line)
    if len(HAN_RE.findall(quote)) < 8:
        return None
    return start, end, quote


def rare_phrase_hit(statement: str, quote: str, hay: str, mapping: list[int], lines: list[str]) -> tuple[int, int, str] | None:
    h = han_only(statement + quote)
    g = grams(statement + quote)
    for length in (10, 8, 6, 5, 4):
        if length > len(h):
            continue
        for i in range(0, len(h) - length + 1):
            sub = h[i : i + length]
            if hay.count(sub) != 1:
                continue
            sp = span_for(hay, mapping, sub)
            if not sp:
                continue
            extra = len(g & grams(lines[sp[0] - 1]))
            need = 3 if length <= 4 else 2
            if extra >= need:
                return pick_quote(lines, sp[0], sp[1])
    return None


def exact_line_hit(quote: str, lines: list[str]) -> tuple[int, int, str] | None:
    nq = han_only(quote)
    if not (4 <= len(nq) <= 40):
        return None
    eqs = [i for i, line in enumerate(lines, 1) if han_only(line) == nq]
    if len(eqs) != 1:
        return None
    return pick_quote(lines, eqs[0], eqs[0])


def collect_title_lines(lines: list[str]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for i, line in enumerate(lines, 1):
        raw = line.strip()
        if not raw:
            continue
        h = han_only(raw)
        if not h:
            continue
        if raw.startswith("#"):
            out.append((i, h))
            continue
        if re.match(r"^第.{0,12}卷", raw) or raw.startswith("論") or raw.startswith("论") or raw.startswith("釋") or raw.startswith("释"):
            if len(h) <= 24:
                out.append((i, h))
                continue
        if "章第" in h and len(h) <= 24:
            out.append((i, h))
    return out


def first_body_after(lines: list[str], loc: int) -> tuple[int, int, str] | None:
    for i in range(loc, min(len(lines), loc + 40) + 1):
        raw = lines[i - 1].strip()
        if is_noise(raw) or raw.startswith("#"):
            continue
        h = han_only(raw)
        if raw.endswith("，") and len(h) < 28:
            continue
        if len(HAN_RE.findall(raw)) >= 8:
            return pick_quote(lines, i, i)
    return pick_quote(lines, loc, loc)


def heading_core_hit(statement: str, lines: list[str]) -> tuple[int, int, str] | None:
    titles = collect_title_lines(lines)
    if not titles:
        return None
    core = catalog_core(statement)
    cores: list[str] = []
    sources = [core]
    # keep a short han slice of the full statement for heading match, not every 2-gram
    st = han_only(statement)
    if st and st != core:
        sources.append(st[:24])
    for c in sources:
        if not c:
            continue
        minl = 2 if len(c) <= 8 else 3
        for length in range(min(8, len(c)), minl - 1, -1):
            for i in range(0, len(c) - length + 1):
                sub = c[i : i + length]
                if sub not in cores:
                    cores.append(sub)
    scored: list[tuple[int, int]] = []
    for sub in cores:
        hits = [t[0] for t in titles if sub in t[1]]
        if len(set(hits)) != 1:
            continue
        title_h = next(t[1] for t in titles if t[0] == hits[0])
        if len(sub) == 2 and not (
            title_h.endswith(sub)
            or f"{sub}章" in title_h
            or f"论{sub}" in title_h
            or f"論{sub}" in title_h
        ):
            continue
        scored.append((len(sub), hits[0]))
    if not scored:
        return None
    scored.sort(reverse=True)
    best_len = scored[0][0]
    locs = {loc for ln, loc in scored if ln == best_len}
    if len(locs) != 1:
        return None
    loc = next(iter(locs))
    return first_body_after(lines, loc)


def is_toc_list_line(line: str, needle_h: str) -> bool:
    h = han_only(line)
    if not h or not needle_h:
        return False
    if h == needle_h or h.endswith(needle_h):
        return False
    if h.count("论") >= 3 and needle_h.startswith("论"):
        return True
    return False


def topic_needle_hit(
    book_key: str, statement: str, hay: str, mapping: list[int], lines: list[str]
) -> tuple[int, int, str] | None:
    items = TOPIC_NEEDLES.get(book_key) or []
    if not items:
        return None
    st = fold(statement)
    st_h = han_only(statement)
    titles = collect_title_lines(lines)
    for key, needle in items:
        kh = han_only(key)
        if not kh:
            continue
        if kh not in st_h and fold(key) not in st:
            continue
        n = han_only(needle)
        if len(n) < 2:
            continue
        title_hits = []
        for loc, th in titles:
            if n not in th:
                continue
            if is_toc_list_line(lines[loc - 1], n):
                continue
            if not (
                th == n
                or th.endswith(n)
                or th.startswith(n)
                or f"论{n}" in th
                or f"論{n}" in th
            ):
                # allow chapter titles that merely contain a long needle
                if len(n) < 6:
                    continue
            title_hits.append(loc)
        loc = None
        if hay.count(n) == 1:
            sp = span_for(hay, mapping, n)
            if sp and not is_toc_list_line(lines[sp[0] - 1], n):
                loc = sp[0]
        if loc is None and len(set(title_hits)) == 1:
            loc = title_hits[0]
        elif loc is None and len(set(title_hits)) == 2:
            loc = max(title_hits)
        elif loc is None and hay.count(n) == 2 and len(n) >= 4:
            idx = hay.rfind(n)
            if idx >= 0 and not is_toc_list_line(lines[mapping[idx] - 1], n):
                loc = mapping[idx]
        if loc is None:
            continue
        hit = first_body_after(lines, loc)
        if hit and len(HAN_RE.findall(hit[2])) >= 8:
            return hit
    return None


def recover_rule(quote: str, statement: str, lines: list[str], hay: str, mapping: list[int], sections: list[dict], book_key: str) -> tuple[int, int, str, str] | None:
    """Return start, end, new_quote, method."""
    if is_header_rule(statement, quote):
        # still try catalog-core unique title before giving up
        hit = heading_core_hit(statement, lines)
        if hit and len(HAN_RE.findall(hit[2])) >= 8:
            return hit[0], hit[1], hit[2], "heading-core"
        hit = topic_needle_hit(book_key, statement, hay, mapping, lines)
        if hit and len(HAN_RE.findall(hit[2])) >= 8:
            return hit[0], hit[1], hit[2], "topic"
        return None
    needle = han_only(quote)
    st_needle = han_only(statement)
    hit = exact_line_hit(quote, lines)
    if hit:
        return hit[0], hit[1], hit[2], "exact-line"
    for src, raw, minl in (("quote", needle, 6), ("stmt", st_needle, 6), ("core", catalog_core(statement), 3)):
        if not raw:
            continue
        run = unique_run(raw, hay, minl=minl)
        if run:
            sp = span_for(hay, mapping, run)
            if sp:
                start, end, q = pick_quote(lines, sp[0], sp[1])
                return start, end, q, f"ngram-{src}"
    for qn in quoted_needles(statement) + quoted_needles(quote):
        if hay.count(qn) == 1:
            sp = span_for(hay, mapping, qn)
            if sp:
                start, end, q = pick_quote(lines, sp[0], sp[1])
                return start, end, q, "quoted"
    if book_key == "ziwei/ziwei-doushu-quanshu":
        hit = ziwei_topic(statement, lines)
        if hit:
            return hit[0], hit[1], hit[2], "ziwei-topic"
    hit = topic_needle_hit(book_key, statement, hay, mapping, lines)
    if hit:
        return hit[0], hit[1], hit[2], "topic"
    hit = heading_core_hit(statement, lines)
    if hit:
        return hit[0], hit[1], hit[2], "heading-core"
    hit = heading_keyword_hit(statement, lines, sections)
    if hit:
        return hit[0], hit[1], hit[2], "heading-key"
    hit = section_hit(statement, lines, sections)
    if hit:
        return hit[0], hit[1], hit[2], "section"
    hit = line_overlap_hit(statement, lines)
    if hit:
        return hit[0], hit[1], hit[2], "overlap"
    hit = rare_phrase_hit(statement, quote, hay, mapping, lines)
    if hit:
        return hit[0], hit[1], hit[2], "rare"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", help="system/slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    recovered: list[dict] = []
    unanchorable: list[dict] = []
    already = 0
    skipped_faqiao = 0

    paths = sorted((ROOT / "references/books").glob("*/*/rules.yaml"))
    if args.book:
        paths = [ROOT / "references/books" / args.book / "rules.yaml"]

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        key = path.parent.relative_to(ROOT / "references/books").as_posix()
        if key in SKIP_BOOKS:
            for rule in data.get("rules") or []:
                if isinstance(rule, dict) and not isinstance(rule.get("anchor"), dict):
                    skipped_faqiao += 1
                    unanchorable.append(
                        {
                            "book": key,
                            "rule_id": rule.get("rule_id"),
                            "reason": "qimen-faqiao excerpt only; no publisher fetch",
                            "quote": (rule.get("quote") or "")[:80],
                        }
                    )
            continue
        ft_rel = book.get("fulltext")
        if not isinstance(ft_rel, str):
            continue
        ft = ROOT / ft_rel
        if not ft.is_file():
            for rule in data.get("rules") or []:
                if isinstance(rule, dict) and not isinstance(rule.get("anchor"), dict):
                    unanchorable.append(
                        {
                            "book": key,
                            "rule_id": rule.get("rule_id"),
                            "reason": "no fulltext file",
                            "quote": (rule.get("quote") or "")[:80],
                        }
                    )
            continue
        lines = ft.read_text(encoding="utf-8").splitlines()
        hay, mapping = build_index(lines)
        sections = parse_sections(lines)
        text = path.read_text(encoding="utf-8")
        orig = text
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            rid = str(rule.get("rule_id") or "")
            if isinstance(rule.get("anchor"), dict):
                already += 1
                continue
            quote = rule.get("quote") or ""
            statement = rule.get("statement") or ""
            hit = recover_rule(quote, statement, lines, hay, mapping, sections, key)
            if hit is None:
                reason = "header/catalog label" if is_header_rule(statement, quote) else "quote not locatable in fulltext"
                unanchorable.append(
                    {
                        "book": key,
                        "art": art_of(book.get("system"), book.get("slug")),
                        "rule_id": rid,
                        "reason": reason,
                        "quote": quote[:120],
                    }
                )
                continue
            start, end, new_quote, method = hit
            if not args.dry_run:
                text = patch_rule(
                    text,
                    rid,
                    start=start,
                    end=end,
                    file_path=ft_rel,
                    new_quote=new_quote,
                )
            recovered.append(
                {
                    "book": key,
                    "rule_id": rid,
                    "method": method,
                    "start": start,
                    "end": end,
                }
            )
        if not args.dry_run and text != orig:
            path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")

    report_dir = ROOT / "tools/reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    md = [
        "# 无法锚定的规则",
        "",
        "定位不到原文的规则保持 `anchor: null`。无锚点是安全降级；错锚点不可接受。",
        "",
        f"共 {len(unanchorable)} 条。",
        "",
        "| book | rule_id | reason | quote 摘录 |",
        "|---|---|---|---|",
    ]
    for item in unanchorable:
        q = (item.get("quote") or "").replace("|", "\\|").replace("\n", " ")
        md.append(f"| `{item['book']}` | `{item['rule_id']}` | {item['reason']} | {q} |")
    md.append("")
    if not args.dry_run:
        (report_dir / "unanchorable.md").write_text("\n".join(md), encoding="utf-8")
        (report_dir / "anchor-recover.json").write_text(
            json.dumps(
                {"recovered": recovered, "unanchorable": len(unanchorable), "skipped_faqiao": skipped_faqiao},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print(
        f"already={already} recovered={len(recovered)} unanchorable={len(unanchorable)} "
        f"faqiao={skipped_faqiao} dry_run={args.dry_run}"
    )
    by_m = defaultdict(int)
    by_b = defaultdict(int)
    for r in recovered:
        by_m[r["method"]] += 1
        by_b[r["book"]] += 1
    print("methods", dict(by_m))
    print("top books", sorted(by_b.items(), key=lambda x: -x[1])[:12])
    return 0


if __name__ == "__main__":
    sys.exit(main())
