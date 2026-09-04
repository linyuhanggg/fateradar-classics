#!/usr/bin/env python3
"""Compile validated rules.yaml into product-shaped JSON.

Doctrine → dist/rules/<art>.json (runtime).
Procedure → dist/procedures/<art>.json (tests only).
Rules without a usable anchor are skipped — that is the pipeline gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "fateradar-rules-v2"
ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")

SYSTEM_TO_ART = {
    "bazi": "bazi",
    "luming-nayin": "bazi",
    "ziwei": "ziwei",
    "divination": "liuyao",
    "xingming": "qizheng",
}

SAN_SHI_PREFIX = (
    ("qimen-", "qimen"),
    ("liuren-", "liuren"),
    ("daliuren-", "liuren"),
)


def art_of(system: str, slug: str) -> str | None:
    if system == "san-shi":
        for prefix, art in SAN_SHI_PREFIX:
            if slug.startswith(prefix):
                return art
        return None
    if system in {"fengshui", "physiognomy", "selection"}:
        return None
    return SYSTEM_TO_ART.get(system)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def topic_of(rule: dict) -> str:
    labels: list[str] = []
    for pred in rule.get("applicable_to") or []:
        if not isinstance(pred, dict):
            continue
        value = pred.get("value")
        key = pred.get("key")
        if isinstance(value, str) and value and value != "*":
            labels.append(value)
        elif isinstance(key, str) and key:
            labels.append(key)
        if len(labels) >= 3:
            break
    return " · ".join(labels) if labels else "通则"


def chapter_of(rule: dict) -> str:
    anchor = rule.get("anchor") or {}
    start = anchor.get("start_line")
    end = anchor.get("end_line")
    if isinstance(start, int) and isinstance(end, int):
        return f"L{start}-L{end}"
    return ""


def verification_of(rule: dict) -> str:
    return "verified" if rule.get("verified") is True else "provisional"


def predicates_of(rule: dict) -> list[dict]:
    out: list[dict] = []
    for pred in rule.get("applicable_to") or []:
        if not isinstance(pred, dict):
            continue
        key = pred.get("key")
        value = pred.get("value")
        if not isinstance(key, str) or not isinstance(value, str):
            continue
        item: dict = {"key": key, "value": value}
        scope = pred.get("scope")
        if isinstance(scope, dict) and scope:
            item["scope"] = scope
        out.append(item)
    return out


def convert(rule: dict, *, art: str, title: str, slug_path: str) -> dict:
    anchor = rule["anchor"]
    return {
        "ruleId": rule["rule_id"],
        "art": art,
        "topic": topic_of(rule),
        "statement": rule["statement"],
        "source": {"book": title, "chapter": chapter_of(rule)},
        "quote": rule["quote"],
        "applicableTo": predicates_of(rule),
        "caveats": list(rule.get("caveats") or []),
        "verification": verification_of(rule),
        "bookSlug": slug_path,
        "anchor": {
            "file": anchor["file"],
            "startLine": anchor["start_line"],
            "endLine": anchor["end_line"],
        },
    }


def usable_anchor(rule: dict) -> bool:
    anchor = rule.get("anchor")
    if not isinstance(anchor, dict):
        return False
    return (
        isinstance(anchor.get("file"), str)
        and isinstance(anchor.get("start_line"), int)
        and isinstance(anchor.get("end_line"), int)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export anchored rules to dist/{rules,procedures}/<art>.json")
    parser.add_argument("--out-rules", default="dist/rules")
    parser.add_argument("--out-procedures", default="dist/procedures")
    args = parser.parse_args(argv)

    rules_dir = ROOT / args.out_rules
    proc_dir = ROOT / args.out_procedures
    rules_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)

    doctrine: dict[str, list[dict]] = defaultdict(list)
    procedure: dict[str, list[dict]] = defaultdict(list)
    seen = 0
    skipped_no_anchor = 0
    skipped_art = 0
    anchored_exportable = 0

    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
            print(f"skip invalid {path}", file=sys.stderr)
            continue
        book = data.get("book") or {}
        system = book.get("system")
        slug = book.get("slug")
        title = book.get("title")
        art = art_of(system, slug)
        slug_path = f"{system}/{slug}"
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            seen += 1
            if art is None:
                skipped_art += 1
                continue
            if not usable_anchor(rule):
                skipped_no_anchor += 1
                continue
            anchored_exportable += 1
            item = convert(rule, art=art, title=title, slug_path=slug_path)
            if rule.get("kind") == "procedure":
                procedure[art].append(item)
            else:
                doctrine[art].append(item)

    exported = 0
    for art in ARTS:
        d_items = doctrine.get(art, [])
        p_items = procedure.get(art, [])
        (rules_dir / f"{art}.json").write_text(
            json.dumps(d_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (proc_dir / f"{art}.json").write_text(
            json.dumps(p_items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        exported += len(d_items) + len(p_items)
        print(f"{art}: doctrine={len(d_items)} procedure={len(p_items)}")

    print(
        f"exported={exported} anchored_exportable={anchored_exportable} "
        f"scanned={seen} skipped_no_anchor={skipped_no_anchor} skipped_other_system={skipped_art}"
    )
    if exported != anchored_exportable:
        print("FAIL export count != anchored exportable count", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
