#!/usr/bin/env python3
"""Export annotated original-book cases without inventing civil birth dates."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from source_paragraphs import load_source_paragraphs

ROOT = Path(__file__).resolve().parents[1]
GANS = "甲乙丙丁戊己庚辛壬癸"
ZHIS = "子丑寅卯辰巳午未申酉戌亥"


def valid_pillars(pillars: object) -> bool:
    return isinstance(pillars, list) and len(pillars) == 4 and all(
        isinstance(pair, str) and len(pair) == 2 and pair[0] in GANS and pair[1] in ZHIS
        and GANS.index(pair[0]) % 2 == ZHIS.index(pair[1]) % 2 for pair in pillars
    )


def case_input(case: dict) -> tuple[dict, tuple | None, str]:
    basis = case.get("inputBasis", "four-pillars")
    if basis == "four-pillars":
        pillars = case.get("pillars", [])
        valid = valid_pillars(pillars)
        fields = {"pillars": pillars, "inputBasis": basis,
                  "scope": ["十神关系", "四柱组合条件"],
                  "unavailable": ["公历生日", "交节后天数", "出生地与时制", "起运"]}
        signature = (basis, *pillars) if valid else None
        repeated = "samePillarsAs"
    elif basis == "meihua-numbers":
        numbers = case.get("numbers", {})
        month, day = numbers.get("lunarMonth"), numbers.get("lunarDay")
        valid = numbers.get("yearBranch") in list(ZHIS) and numbers.get("hourBranch") in list(ZHIS) and type(month) is int and 1 <= month <= 12 and type(day) is int and 1 <= day <= 30
        fields = {"numbers": numbers, "inputBasis": basis,
                  "scope": ["数字起卦", "上下互变", "动爻"],
                  "unavailable": ["绝对公历年份", "节气月令与体用旺衰", "现实应验的独立记录"]}
        signature = (basis, numbers["yearBranch"], month, day, numbers["hourBranch"]) if valid else None
        repeated = "sameNumbersAs"
    else:
        raise ValueError(f"Unsupported case input basis: {basis}")
    if case.get("canRecompute") is True and not valid:
        raise ValueError("Incomplete or invalid case input marked recomputable")
    fields["canRecompute"] = bool(case.get("canRecompute") and valid)
    if not fields["canRecompute"]:
        fields["scope"] = []
    if "expected" in case:
        fields["expected"] = case["expected"]  # Only the explicitly recorded expectation.
    return fields, signature, repeated


def collect_cases(root: Path) -> dict:
    sources = load_source_paragraphs(root)
    locations = {key: (row["source_file"], row["start_line"], row["end_line"]) for key, row in sources.items()}
    cases, by_input = [], {}
    for p in sorted((root / "references/annotations").glob("*/*.json")):
        data = json.loads(p.read_text())
        for entry in data["entries"]:
            if entry["review"] != "source-reviewed":
                continue
            records = ([entry["case"]] if entry.get("case") else []) + entry.get("cases", [])
            pid = entry["paragraphId"]
            if pid not in locations:
                raise ValueError(f"Unknown case source: {pid}")
            if records and sources[pid].get("source_status") == "ocr-draft":
                raise ValueError(f"OCR draft cannot supply reviewed source cases: {pid}")
            for index, case in enumerate(records):
                fields, signature, repeated = case_input(case)
                fulltext, start, end = locations[pid]
                case_id = pid if len(records) == 1 else f"{pid}:case-{index + 1}"
                row = {"id": case_id, "bookSlug": data["bookSlug"], "name": case["name"],
                       "kind": "source_case", **fields,
                       "reading": entry["vernacular"], "notes": entry["notes"],
                       "source": {"paragraphId": pid, "file": fulltext, "startLine": start, "endLine": end},
                       "verified": False}
                # Repeated mathematical inputs are not extra independent validation cases.
                if signature is not None and row["canRecompute"]:
                    if signature in by_input:
                        row[repeated] = by_input[signature]
                    else:
                        by_input[signature] = case_id
                cases.append(row)
    return {"version": 1, "note": "原书记载与现代独立验盘分开；四柱合法不代表公历可还原。", "cases": cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "references/cases/source-cases.json")
    args = parser.parse_args()
    data = collect_cases(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cases": len(data["cases"]), "recomputable": sum(c["canRecompute"] for c in data["cases"]),
                      "repeated_inputs": sum("samePillarsAs" in c or "sameNumbersAs" in c for c in data["cases"]), "verified": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
