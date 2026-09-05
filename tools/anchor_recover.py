#!/usr/bin/env python3
"""Recover anchors for unanchored rules without inventing text.

High-confidence only:
  1. collapsed quote (plus simp/trad variants) is a unique/first substring of fulltext
  2. longest unique han-run of the quote (≥12) appears once in fulltext

On (2), quote is rewritten to the original line span (so V5 can pass).
statement is never rewritten. verified stays false.
Unrecovered rules stay anchor: null and are listed in tools/reports/unanchorable.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WS_RE = re.compile(r"\s+", re.UNICODE)
HAN_RE = re.compile(r"[㐀-鿿]")
MD_JUNK_RE = re.compile(r"\*\*|⚠️|（\*\*[^*]+\*\*：[^）]*）|\([^)]*强 reframe[^)]*\)")

PAIRS = (
    ("專", "专"), ("國", "国"), ("無", "无"), ("這", "这"), ("個", "个"), ("時", "时"),
    ("為", "为"), ("與", "与"), ("後", "后"), ("來", "来"), ("過", "过"), ("對", "对"),
    ("發", "发"), ("經", "经"), ("關", "关"), ("麼", "么"), ("說", "说"), ("義", "义"),
    ("書", "书"), ("門", "门"), ("開", "开"), ("體", "体"), ("餘", "余"), ("歲", "岁"),
    ("萬", "万"), ("學", "学"), ("當", "当"), ("從", "从"), ("還", "还"), ("氣", "气"),
    ("裏", "里"), ("裡", "里"), ("並", "并"), ("於", "于"), ("卻", "却"), ("論", "论"),
    ("殺", "杀"), ("財", "财"), ("傷", "伤"), ("順", "顺"), ("陽", "阳"), ("陰", "阴"),
    ("龍", "龙"), ("祿", "禄"), ("權", "权"), ("數", "数"), ("術", "术"), ("會", "会"),
    ("實", "实"), ("業", "业"), ("點", "点"), ("剋", "克"), ("儀", "仪"), ("宮", "宫"),
    ("禍", "祸"), ("賦", "赋"), ("觀", "观"), ("測", "测"), ("錄", "录"), ("華", "华"),
    ("陳", "陈"), ("飛", "飞"), ("鬥", "斗"), ("總", "总"), ("節", "节"), ("斷", "断"),
    ("決", "决"), ("貴", "贵"), ("窮", "穷"), ("寶", "宝"), ("鑑", "鉴"), ("鑒", "鉴"),
    ("淵", "渊"), ("詮", "诠"), ("虛", "虚"), ("強", "强"), ("調", "调"), ("變", "变"),
    ("遷", "迁"), ("僕", "仆"), ("親", "亲"), ("機", "机"), ("東", "东"), ("問", "问"),
    ("題", "题"), ("應", "应"), ("該", "该"), ("種", "种"), ("類", "类"), ("們", "们"),
    ("沒", "没"), ("讓", "让"), ("幹", "干"), ("眾", "众"), ("運", "运"), ("動", "动"),
    ("馬", "马"), ("鉞", "钺"), ("輔", "辅"), ("弼", "弼"), ("貪", "贪"), ("貞", "贞"),
    ("廟", "庙"), ("蓋", "盖"), ("華", "华"), ("殺", "杀"), ("孫", "孙"), ("葉", "叶"),
    ("條", "条"), ("處", "处"), ("號", "号"), ("電", "电"), ("雲", "云"), ("風", "风"),
    ("見", "见"), ("現", "现"), ("長", "长"), ("兩", "两"), ("內", "内"), ("外", "外"),
    ("稱", "称"), ("謂", "谓"), ("若", "若"), ("則", "则"), ("即", "即"), ("乃", "乃"),
    ("為", "为"), ("於", "于"), ("與", "与"), ("其", "其"), ("之", "之"), ("也", "也"),
    ("焉", "焉"), ("矣", "矣"), ("哉", "哉"), ("復", "复"), ("從", "从"), ("後", "后"),
    ("將", "将"), ("得", "得"), ("無", "无"), ("有", "有"), ("主", "主"), ("入", "入"),
    ("命", "命"), ("格", "格"), ("局", "局"), ("用", "用"), ("神", "神"), ("旺", "旺"),
    ("衰", "衰"), ("生", "生"), ("剋", "克"), ("克", "克"), ("洩", "泄"), ("泄", "泄"),
    ("秀", "秀"), ("氣", "气"), ("勢", "势"), ("貴", "贵"), ("賤", "贱"), ("富", "富"),
    ("貧", "贫"), ("吉", "吉"), ("凶", "凶"), ("禍", "祸"), ("福", "福"), ("災", "灾"),
    ("病", "病"), ("官", "官"), ("印", "印"), ("食", "食"), ("傷", "伤"), ("財", "财"),
    ("殺", "杀"), ("刃", "刃"), ("劫", "劫"), ("祿", "禄"), ("馬", "马"), ("空", "空"),
    ("亡", "亡"), ("刑", "刑"), ("沖", "冲"), ("冲", "冲"), ("合", "合"), ("害", "害"),
    ("會", "会"), ("聚", "聚"), ("破", "破"), ("狼", "狼"), ("廉", "廉"), ("府", "府"),
    ("相", "相"), ("梁", "梁"), ("同", "同"), ("曲", "曲"), ("機", "机"), ("陰", "阴"),
    ("陽", "阳"), ("微", "微"), ("紫", "紫"), ("星", "星"), ("斗", "斗"), ("數", "数"),
    ("全書", "全书"),
)
T2S = str.maketrans({a: b for a, b in PAIRS if len(a) == 1 and len(b) == 1})
S2T = str.maketrans({b: a for a, b in PAIRS if len(a) == 1 and len(b) == 1})
ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")


def collapse(text: str) -> str:
    return WS_RE.sub("", text or "")


def variants(text: str) -> list[str]:
    c = collapse(text)
    out = []
    for v in (c, c.translate(T2S), c.translate(S2T)):
        if v and v not in out:
            out.append(v)
    return out


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


def build_index(lines: list[str]) -> tuple[str, list[int]]:
    chunks: list[str] = []
    mapping: list[int] = []
    for i, line in enumerate(lines, 1):
        c = collapse(line)
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


def unique_span(hay: str, mapping: list[int], needle: str) -> tuple[int, int] | None:
    if not needle or hay.count(needle) != 1:
        return None
    return span_for(hay, mapping, needle)


def longest_unique_run(quote: str, hay: str) -> str | None:
    needle = collapse(quote)
    n = len(needle)
    if n < 12:
        return None
    max_l = min(n, 60)
    for length in range(max_l, 11, -1):
        found = None
        counts_multi = False
        step = 1 if length >= 24 else max(1, length // 6)
        for i in range(0, n - length + 1, step):
            sub = needle[i : i + length]
            if len(HAN_RE.findall(sub)) < 8:
                continue
            c = hay.count(sub)
            if c == 1:
                found = sub
                break
            if c > 1:
                counts_multi = True
        if found:
            return found
        if length <= 16 and not counts_multi:
            break
    return None


def yaml_quote(value: str) -> str:
    if any(ch in value for ch in ":#{}[]&*!|>%'\"\n") or value != value.strip():
        dumped = yaml.safe_dump(value, allow_unicode=True).strip()
        if dumped.endswith("\n..."):
            dumped = dumped[: -4].strip()
        return dumped
    return value


def patch_rule(text: str, rule_id: str, *, start: int, end: int, file_path: str, new_quote: str | None) -> str:
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
    new_anchor = [
        "  anchor:",
        f"    file: {file_path}",
        f"    start_line: {start}",
        f"    end_line: {end}",
    ]
    block[a0:a1] = new_anchor
    if new_quote is not None:
        q0 = next((k for k, line in enumerate(block) if re.match(r"  quote:", line)), None)
        if q0 is None:
            raise RuntimeError(f"no quote field: {rule_id}")
        q1 = q0 + 1
        if block[q0].strip() == "quote: >-" or block[q0].strip() == "quote: |" or block[q0].rstrip().endswith(">-"):
            while q1 < len(block) and (block[q1].startswith("    ") or block[q1].startswith("      ")):
                q1 += 1
        rendered = yaml_quote(new_quote)
        if "\n" in rendered:
            q_lines = ["  quote: >-"] + ["    " + ln for ln in new_quote.splitlines()]
        else:
            q_lines = [f"  quote: {rendered}"]
        block[q0:q1] = q_lines
    lines[start_i:end_i] = block
    return "\n".join(lines) + "\n"


def clean_quote(q: str) -> str:
    q = MD_JUNK_RE.sub("", q or "")
    q = q.replace("**", "")
    return q.strip()


def recover_one(quote: str, hays: list[tuple[str, list[int]]]) -> tuple[int, int, str] | None:
    """Return (start, end, method) or None. method in {exact, substr}."""
    cleaned = clean_quote(quote)
    for hay, mapping in hays:
        for v in variants(cleaned) + variants(quote):
            sp = unique_span(hay, mapping, v) or span_for(hay, mapping, v)
            if sp and v and len(HAN_RE.findall(v)) >= 6:
                # prefer unique; allow first-hit exact if quote is long
                if hay.count(v) == 1 or len(HAN_RE.findall(v)) >= 20:
                    return sp[0], sp[1], "exact"
        run = longest_unique_run(cleaned, hay) or longest_unique_run(quote, hay)
        if run:
            sp = unique_span(hay, mapping, run)
            if sp:
                return sp[0], sp[1], "substr"
    return None


def original_quote(lines: list[str], start: int, end: int) -> str:
    chunk = [lines[i - 1].strip() for i in range(start, end + 1) if 1 <= i <= len(lines)]
    text = "".join(chunk)
    text = re.sub(r"^#+\s*", "", text)
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", help="system/slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    recovered: list[dict] = []
    unanchorable: list[dict] = []
    already = 0
    skipped_no_ft = 0

    paths = sorted((ROOT / "references/books").glob("*/*/rules.yaml"))
    if args.book:
        paths = [ROOT / "references/books" / args.book / "rules.yaml"]

    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        key = path.parent.relative_to(ROOT / "references/books").as_posix()
        ft_rel = book.get("fulltext")
        if not isinstance(ft_rel, str):
            continue
        ft = ROOT / ft_rel
        if not ft.is_file():
            for rule in data.get("rules") or []:
                if isinstance(rule, dict) and not isinstance(rule.get("anchor"), dict):
                    skipped_no_ft += 1
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
        hays = [(hay, mapping)]
        hay_s = hay.translate(T2S)
        hay_t = hay.translate(S2T)
        if hay_s != hay:
            hays.append((hay_s, mapping))
        if hay_t != hay:
            hays.append((hay_t, mapping))

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
            hit = recover_one(quote, hays)
            if hit is None:
                unanchorable.append(
                    {
                        "book": key,
                        "art": art_of(book.get("system"), book.get("slug")),
                        "rule_id": rid,
                        "reason": "quote not locatable in fulltext",
                        "quote": quote[:120],
                    }
                )
                continue
            start, end, method = hit
            new_quote = None
            if method == "substr":
                new_quote = original_quote(lines, start, end)
                # keep it short enough to stay a real excerpt
                if len(new_quote) > 180:
                    # trim to the line that contained the unique run
                    new_quote = original_quote(lines, start, start)
                    end = start
            if method == "exact":
                # keep existing quote; it already sits in the window
                new_quote = None
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
    md_lines = [
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
        md_lines.append(f"| `{item['book']}` | `{item['rule_id']}` | {item['reason']} | {q} |")
    md_lines.append("")
    if not args.dry_run:
        (report_dir / "unanchorable.md").write_text("\n".join(md_lines), encoding="utf-8")
        (report_dir / "anchor-recover.json").write_text(
            json.dumps({"recovered": recovered, "unanchorable": len(unanchorable)}, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
    print(
        f"already={already} recovered={len(recovered)} unanchorable={len(unanchorable)} "
        f"no_ft={skipped_no_ft} dry_run={args.dry_run}"
    )
    by_m = defaultdict(int)
    for r in recovered:
        by_m[r["method"]] += 1
    print("methods", dict(by_m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
