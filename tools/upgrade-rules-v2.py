#!/usr/bin/env python3
"""Upgrade existing v1 rules.yaml + terms.yaml to fateradar-rules-v2.

Format only: do not invent doctrine, do not rename rule_id, do not set verified.
Unmappable applicable_to strings become [].
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_TERMS = Path("/Users/sync/code/cosmic-fortune-lab/src/lib/rules/terms.ts")
SCHEMA_V2 = "fateradar-rules-v2"
VOCAB_SCHEMA = "fateradar-vocab-v1"
ANY = "*"

SCRIPT_PAIRS = (
    ("專", "专"),
    ("國", "国"),
    ("無", "无"),
    ("這", "这"),
    ("個", "个"),
    ("時", "时"),
    ("為", "为"),
    ("與", "与"),
    ("後", "后"),
    ("來", "来"),
    ("過", "过"),
    ("對", "对"),
    ("發", "发"),
    ("經", "经"),
    ("關", "关"),
    ("麼", "么"),
    ("說", "说"),
    ("義", "义"),
    ("書", "书"),
    ("門", "门"),
    ("開", "开"),
    ("體", "体"),
    ("餘", "余"),
    ("歲", "岁"),
    ("萬", "万"),
    ("學", "学"),
    ("當", "当"),
    ("從", "从"),
    ("還", "还"),
    ("氣", "气"),
    ("裏", "里"),
    ("並", "并"),
    ("於", "于"),
    ("卻", "却"),
    ("論", "论"),
    ("殺", "杀"),
    ("財", "财"),
    ("傷", "伤"),
    ("順", "顺"),
    ("陽", "阳"),
    ("陰", "阴"),
    ("龍", "龙"),
    ("祿", "禄"),
    ("權", "权"),
    ("數", "数"),
    ("術", "术"),
    ("會", "会"),
    ("實", "实"),
    ("業", "业"),
    ("點", "点"),
)

KEY_ALIASES: dict[str, tuple[str, str]] = {
    "月令": ("yueling", ANY),
    "提纲": ("yueling", ANY),
    "月建": ("yueling", ANY),
    "空亡": ("kongwang", ANY),
    "旬空": ("kongwang", ANY),
    "世爻": ("shiyao", ANY),
    "应爻": ("yingyao", ANY),
    "世应": ("shiyao", ANY),
    "七政": ("xingyao", ANY),
    "四余": ("xingyao", ANY),
    "日主": ("rizhu", ANY),
    "大限": ("daxian", ANY),
}

SHISHEN_ALIAS = {
    "偏官": "七杀",
    "七煞": "七杀",
    "七杀": "七杀",
}

TERM_RE = re.compile(
    r'\{\s*canonical:\s*"([^"]+)",\s*kind:\s*"([^"]+)",\s*aliases:\s*\[([^\]]*)\]\s*\}'
)


class FlowMap(dict):
    pass


class RulesDumper(yaml.SafeDumper):
    pass


def _represent_none(dumper, _data):
    return dumper.represent_scalar("tag:yaml.org,2002:null", "null")


def _represent_flow(dumper, data):
    return dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=True)


RulesDumper.add_representer(type(None), _represent_none)
RulesDumper.add_representer(FlowMap, _represent_flow)
RulesDumper.ignore_aliases = lambda *_: True  # type: ignore[method-assign]


def detect_script(text: str) -> str:
    trad = simp = 0
    for t_ch, s_ch in SCRIPT_PAIRS:
        trad += (text or "").count(t_ch)
        simp += (text or "").count(s_ch)
    if trad == 0 and simp == 0:
        return "traditional"
    return "traditional" if trad >= simp else "simplified"


def load_vocab() -> tuple[set[str], dict[str, list[str]], dict[str, list[str]]]:
    data = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
    keys = set(data["keys"])
    values = {k: list(v) for k, v in data["values"].items()}
    closed_index: dict[str, list[str]] = {}
    for key, vals in values.items():
        if not vals:
            continue
        for val in vals:
            closed_index.setdefault(val, []).append(key)
    return keys, values, closed_index


def map_tag(tag: str, closed_index: dict[str, list[str]], values: dict[str, list[str]]) -> list[dict]:
    tag = (tag or "").strip()
    if not tag:
        return []
    if tag in KEY_ALIASES:
        key, value = KEY_ALIASES[tag]
        return [FlowMap({"key": key, "value": value})]
    if tag in SHISHEN_ALIAS:
        return [FlowMap({"key": "shishen", "value": SHISHEN_ALIAS[tag]})]
    if tag == "天乙":
        return [FlowMap({"key": "shensha", "value": "天乙贵人"})]
    if tag == "仆役":
        return [FlowMap({"key": "ziwei_palace", "value": "交友"})]
    if tag == "官禄":
        return [FlowMap({"key": "ziwei_palace", "value": "事业"})]
    if tag == "日主偏旺":
        return [FlowMap({"key": "rizhu_strength", "value": v}) for v in ("中强", "偏强", "极强")]
    if tag == "日主偏弱":
        return [FlowMap({"key": "rizhu_strength", "value": v}) for v in ("中弱", "偏弱", "极弱")]
    if tag == "财星显":
        return [
            FlowMap({"key": "shishen", "value": "正财"}),
            FlowMap({"key": "shishen", "value": "偏财"}),
        ]
    hits = closed_index.get(tag) or []
    if len(hits) == 1:
        return [FlowMap({"key": hits[0], "value": tag})]
    if tag in values.get("ziwei_palace", []) and "ziwei_palace" in hits:
        return [FlowMap({"key": "ziwei_palace", "value": tag})]
    return []


def convert_applicable(raw, closed_index, values) -> list:
    if not isinstance(raw, list):
        return []
    out: list = []
    seen: set[tuple[str, str]] = set()
    for item in raw:
        if isinstance(item, dict) and isinstance(item.get("key"), str) and isinstance(item.get("value"), str):
            pred = FlowMap({"key": item["key"], "value": item["value"]})
            if isinstance(item.get("scope"), dict) and item["scope"]:
                pred["scope"] = item["scope"]
            key = (pred["key"], pred["value"])
            if key not in seen:
                seen.add(key)
                out.append(pred)
            continue
        if not isinstance(item, str):
            continue
        for pred in map_tag(item, closed_index, values):
            key = (pred["key"], pred["value"])
            if key not in seen:
                seen.add(key)
                out.append(pred)
    return out


def upgrade_book(path: Path, closed_index, values) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    book = dict(data.get("book") or {})
    fulltext_rel = book.get("fulltext")
    script = book.get("script")
    if script not in {"traditional", "simplified"}:
        ft = ROOT / fulltext_rel if isinstance(fulltext_rel, str) else None
        sample = ""
        if ft and ft.is_file():
            sample = ft.read_text(encoding="utf-8")[:80000]
        script = detect_script(sample)
    book_out = {
        "slug": book.get("slug"),
        "system": book.get("system"),
        "title": book.get("title"),
        "script": script,
        "fulltext": book.get("fulltext"),
        "fulltext_sha256": book.get("fulltext_sha256"),
    }
    rules_out = []
    for rule in data.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        kind = rule.get("kind") if rule.get("kind") in {"doctrine", "procedure"} else "doctrine"
        rules_out.append(
            {
                "rule_id": rule.get("rule_id"),
                "kind": kind,
                "statement": rule.get("statement"),
                "anchor": rule.get("anchor"),
                "quote": rule.get("quote"),
                "applicable_to": convert_applicable(rule.get("applicable_to"), closed_index, values),
                "caveats": list(rule.get("caveats") or []),
                "school": rule.get("school"),
                "verified": bool(rule.get("verified")),
                "verified_by": rule.get("verified_by"),
                "verified_at": rule.get("verified_at"),
            }
        )
    out = {"schema_version": SCHEMA_V2, "book": book_out, "rules": rules_out}
    text = yaml.dump(
        out,
        Dumper=RulesDumper,
        allow_unicode=True,
        sort_keys=False,
        width=10000,
        default_flow_style=False,
    )
    path.write_text(text, encoding="utf-8")


def product_terms() -> list[dict]:
    if not PRODUCT_TERMS.is_file():
        return []
    text = PRODUCT_TERMS.read_text(encoding="utf-8")
    out = []
    for m in TERM_RE.finditer(text):
        aliases = re.findall(r'"([^"]+)"', m.group(3))
        out.append({"canonical": m.group(1), "kind": m.group(2), "aliases": aliases})
    return out


def assign_fact_key(term: dict, values: dict[str, list[str]]) -> str | None:
    canonical = term.get("canonical") or ""
    kind = term.get("kind") or ""
    aliases = term.get("aliases") or []
    labels = [canonical, *aliases]

    if canonical in KEY_ALIASES:
        return KEY_ALIASES[canonical][0]
    if any(x in SHISHEN_ALIAS or x in values.get("shishen", []) for x in labels):
        return "shishen"
    if kind == "palace" and canonical in values.get("ziwei_palace", []):
        return "ziwei_palace"
    if kind == "door" and canonical in values.get("bamen", []):
        return "bamen"
    if canonical in values.get("sihua", []):
        return "sihua"
    if canonical in values.get("sanchuan", []):
        return "sanchuan"
    if kind == "ke" and canonical.endswith("课"):
        return "keti"
    if kind == "cycle" and canonical == "大限":
        return "daxian"
    if canonical in {"偏旺", "偏弱"}:
        return "rizhu_strength"
    if canonical == "空亡" or "空亡" in aliases:
        return "kongwang"
    if kind == "shensha":
        return "shensha"
    if kind == "god":
        if canonical in values.get("bashen", []):
            return "bashen"
        if canonical in values.get("tianjiang", []):
            return "tianjiang"
        if canonical in values.get("liushen", []):
            return "liushen"
        if canonical in values.get("jiuxing", []):
            return "jiuxing"
        return None
    if kind == "star":
        if canonical in values.get("sihua", []):
            return "sihua"
        if canonical in values.get("xingyao", []) and canonical not in {
            "太阳",
            "太阴",
            "火星",
        }:
            return "xingyao"
        return "ziwei_star"
    if kind == "element" and canonical in values.get("yongshen", []):
        return "yongshen"
    return None


def upgrade_terms(values: dict[str, list[str]]) -> None:
    path = ROOT / "references/vocab/terms.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    existing = list(data.get("terms") or [])
    by_canon = {t.get("canonical"): t for t in existing if isinstance(t, dict)}
    for src in product_terms():
        cur = by_canon.get(src["canonical"])
        if cur is None:
            cur = {"canonical": src["canonical"], "kind": src["kind"], "aliases": list(src["aliases"])}
            existing.append(cur)
            by_canon[src["canonical"]] = cur
        if not cur.get("kind"):
            cur["kind"] = src["kind"]
        aliases = list(cur.get("aliases") or [])
        for alias in src["aliases"]:
            if alias not in aliases:
                aliases.append(alias)
        cur["aliases"] = aliases
        fact_key = assign_fact_key(cur, values)
        if fact_key:
            cur["fact_key"] = fact_key
    # leftover existing terms
    for term in existing:
        if term.get("fact_key"):
            continue
        fact_key = assign_fact_key(term, values)
        if fact_key:
            term["fact_key"] = fact_key
    if "七杀" not in by_canon:
        existing.append(
            {
                "canonical": "七杀",
                "kind": "element",
                "fact_key": "shishen",
                "aliases": ["偏官", "七煞"],
            }
        )
    def emit(value) -> str:
        text = "" if value is None else str(value)
        if text == "" or text[:1] in "-?*&!%@`'\",{}[]|>" or text in {
            "true",
            "false",
            "null",
            "yes",
            "no",
            "on",
            "off",
        } or any(ch in text for ch in ":#"):
            return json.dumps(text, ensure_ascii=False)
        return text

    lines = [f"schema_version: {VOCAB_SCHEMA}", "terms:"]
    for term in existing:
        lines.append(f"- canonical: {emit(term['canonical'])}")
        if term.get("kind"):
            lines.append(f"  kind: {emit(term['kind'])}")
        if term.get("fact_key"):
            lines.append(f"  fact_key: {emit(term['fact_key'])}")
        aliases = term.get("aliases") or []
        if aliases:
            lines.append("  aliases:")
            for alias in aliases:
                lines.append(f"  - {emit(alias)}")
        else:
            lines.append("  aliases: []")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    _keys, values, closed_index = load_vocab()
    files = sorted((ROOT / "references/books").glob("*/*/rules.yaml"))
    for path in files:
        upgrade_book(path, closed_index, values)
        print(f"upgraded {path.relative_to(ROOT)}")
    upgrade_terms(values)
    print(f"books={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
