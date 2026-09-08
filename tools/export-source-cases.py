#!/usr/bin/env python3
"""Export annotated original-book cases without inventing civil birth dates."""
from __future__ import annotations
import argparse
import io
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path
from source_paragraphs import load_source_paragraphs

ROOT = Path(__file__).resolve().parents[1]
GANS = "甲乙丙丁戊己庚辛壬癸"
ZHIS = "子丑寅卯辰巳午未申酉戌亥"
ZIWEI_COMPONENTS = {
    "soul-body": ({"lunarMonth", "hourBranch"}, {"soulBranch", "bodyBranch"}, "命身宫位置"),
    "purple-star": ({"fiveElementsClass", "lunarDay"}, {"ziweiBranch"}, "紫微星位置"),
    "chang-qu": ({"hourBranch"}, {"wenChangBranch", "wenQuBranch"}, "文昌文曲位置"),
    "zuo-you": ({"lunarMonth"}, {"zuoFuBranch", "youBiBranch"}, "左辅右弼位置"),
    "lu-yang-tuo": ({"yearStem"}, {"luCunBranch", "qingYangBranch", "tuoLuoBranch"}, "禄存羊陀位置"),
    "transit-lu-yang-tuo": ({"transitYearStem", "transitYearBranch"}, {"luCunBranch", "qingYangBranch", "tuoLuoBranch"}, "流年禄存羊陀位置"),
    "mutagens": ({"yearStem"}, {"禄", "权", "科", "忌"}, "年干四化星名"),
    "kong-jie": ({"hourBranch"}, {"sourceTianKongBranch", "diJieBranch"}, "原书天空与地劫位置"),
    "tian-fu": ({"ziweiBranch"}, {"tianFuBranch"}, "紫府相对位置"),
}


def ziwei_component_input(case: dict) -> tuple[bool, str]:
    component = case.get("component")
    if component not in ZIWEI_COMPONENTS:
        raise ValueError(f"Unsupported Ziwei component: {component}")
    required, expected_keys, label = ZIWEI_COMPONENTS[component]
    given, expected = case.get("input", {}), case.get("expected", {})
    if not isinstance(given, dict) or not isinstance(expected, dict):
        return False, label
    valid = set(given) == required and bool(expected) and set(expected) <= expected_keys
    for field, value in given.items():
        if field == "lunarMonth":
            valid &= type(value) is int and 1 <= value <= 12
        elif field == "lunarDay":
            valid &= type(value) is int and 1 <= value <= 30
        elif field in {"hourBranch", "transitYearBranch", "ziweiBranch"}:
            valid &= value in list(ZHIS)
        elif field in {"yearStem", "transitYearStem"}:
            valid &= value in list(GANS)
        elif field == "fiveElementsClass":
            valid &= value in {"水二局", "木三局", "金四局", "土五局", "火六局"}
    if component == "mutagens":
        valid &= all(isinstance(value, str) and bool(value.strip()) for value in expected.values())
    else:
        valid &= all(value in list(ZHIS) for value in expected.values())
    return bool(valid), label


def valid_pillars(pillars: object) -> bool:
    return isinstance(pillars, list) and len(pillars) == 4 and all(
        isinstance(pair, str) and len(pair) == 2 and pair[0] in GANS and pair[1] in ZHIS
        and GANS.index(pair[0]) % 2 == ZHIS.index(pair[1]) % 2 for pair in pillars
    )


def liuyao_component_input(case: dict) -> bool:
    given, expected = case.get("input", {}), case.get("expected", {})
    if not isinstance(given, dict) or not isinstance(expected, dict):
        return False
    lines = given.get("linesBottomUp", [])
    valid = (set(given) <= {"linesBottomUp", "monthBranch", "dayGanzhi"}
             and isinstance(lines, list) and len(lines) == 6
             and all(line in {"⚊", "⚋", "○", "ㄨ"} for line in lines))
    if "monthBranch" in given:
        valid &= given["monthBranch"] in list(ZHIS)
    if "dayGanzhi" in given:
        pair = given["dayGanzhi"]
        valid &= (isinstance(pair, str) and len(pair) == 2 and pair[0] in GANS and pair[1] in ZHIS
                  and GANS.index(pair[0]) % 2 == ZHIS.index(pair[1]) % 2)
    valid &= (isinstance(expected.get("mainGua"), str) and bool(expected["mainGua"])
              and type(expected.get("shi")) is int and 1 <= expected["shi"] <= 6
              and type(expected.get("ying")) is int and 1 <= expected["ying"] <= 6)
    fields = ["mainLines"]
    if any(line in {"○", "ㄨ"} for line in lines):
        valid &= isinstance(expected.get("changedGua"), str) and bool(expected["changedGua"])
        fields.append("changedLines")
    else:
        valid &= "changedGua" not in expected and "changedLines" not in expected
    for field in fields:
        rows = expected.get(field)
        if not isinstance(rows, list) or len(rows) != 6:
            return False
        valid &= all(isinstance(row, dict) and type(row.get("position")) is int for row in rows)
        if not valid:
            return False
        valid &= sorted(row["position"] for row in rows) == list(range(1, 7))
        valid &= all(row.get("kinship") in {"父母", "兄弟", "子孙", "子孫", "妻财", "妻財", "官鬼"}
                     and row.get("branch") in list(ZHIS) and row.get("element") in list("木火土金水")
                     for row in rows)
    return bool(valid)


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
    elif basis == "meihua-hexagram":
        given = case.get("input", {})
        moving = given.get("moving")
        names = {"乾", "兑", "離", "离", "震", "巽", "坎", "艮", "坤", "兌"}
        valid = given.get("upper") in names and given.get("lower") in names and type(moving) is int and 1 <= moving <= 6
        fields = {"input": given, "inputBasis": basis,
                  "scope": ["已给主卦", "动爻变卦"],
                  "unavailable": ["起卦日期与原始取数", "未明说的取互对象", "节气月令与体用旺衰", "现实应验的独立记录"]}
        signature = (basis, given["upper"], given["lower"], moving) if valid else None
        repeated = "sameHexagramInputAs"
    elif basis == "ziwei-component":
        valid, label = ziwei_component_input(case)
        expectation_status = case.get("expectationStatus", "clear")
        if expectation_status not in {"clear", "source-conflict"}:
            raise ValueError(f"Unsupported source expectation status: {expectation_status}")
        fields = {"component": case["component"], "input": case.get("input", {}), "inputBasis": basis,
                  "expectationStatus": expectation_status,
                  "scope": [label], "unavailable": ["完整公历或农历生日", "完整命盘", "未给字段的安星结果", "现实命运的独立记录"]}
        signature = (basis, case["component"], json.dumps(fields["input"], ensure_ascii=False, sort_keys=True)) if valid else None
        repeated = "sameComponentInputAs"
    elif basis == "liuyao-line-symbols":
        valid = liuyao_component_input(case)
        given = case.get("input", {})
        fields = {"input": given, "inputBasis": basis,
                  "scope": ["原卦阴阳与动爻", "主卦纳支五行六亲与世应"],
                  "unavailable": list(dict.fromkeys(case.get("unavailable", []) + ["绝对公历年份", "现代独立应验记录"]))}
        if any(line in {"○", "ㄨ"} for line in given.get("linesBottomUp", [])):
            fields["scope"].append("变卦纳支五行与本宫六亲")
        # This export compares diagram components. A different stated day does
        # not make the same six line symbols an independent placement case.
        signature = (basis, *given["linesBottomUp"]) if valid else None
        repeated = "sameComponentInputAs"
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
    cases, by_input, reviewed_entries = [], {}, {}
    for p in sorted((root / "references/annotations").glob("*/*.json")):
        data = json.loads(p.read_text())
        for entry in data["entries"]:
            if entry["review"] != "source-reviewed":
                continue
            reviewed_entries[entry["paragraphId"]] = entry
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
    # Component examples often appear inside operation tables. Keep their original
    # explicit inputs instead of fabricating a full birthday to fit four-pillars.
    for path in sorted((root / "references/cases").glob("*-component-candidates.json")):
        data = json.loads(path.read_text())
        seen = set()
        for case in data["cases"]:
            fragments = case.get("sources") or ([case["source"]] if case.get("source") else [])
            if not fragments:
                raise ValueError(f"Component case requires a reviewed source: {case['id']}")
            for source in fragments:
                pid = source["paragraphId"]
                if pid not in reviewed_entries or pid not in locations:
                    raise ValueError(f"Component case requires a reviewed source: {pid}")
                if not pid.startswith(data["bookSlug"] + ":"):
                    raise ValueError(f"Component case book mismatch: {pid}")
                if sources[pid].get("source_status") == "ocr-draft":
                    raise ValueError(f"OCR draft cannot supply reviewed source cases: {pid}")
                if (source["file"], source["startLine"], source["endLine"]) != locations[pid]:
                    raise ValueError(f"Component case source range mismatch: {pid}")
                if "quote" in source:
                    raw = (root / source["file"]).read_text().splitlines()
                    text = "\n".join(raw[source["startLine"]-1:source["endLine"]])
                    if not source["quote"] or source["quote"] not in text:
                        raise ValueError(f"Component case quote mismatch: {pid}")
            if case["id"] in seen or case.get("verified") is True:
                raise ValueError(f"Duplicate or automatically verified component case: {case['id']}")
            seen.add(case["id"])
            fields, signature, repeated = case_input(case)
            source = fragments[0]
            entry = reviewed_entries[source["paragraphId"]]
            case_id = f"{data['bookSlug']}:{case['id']}"
            row = {"id": case_id, "bookSlug": data["bookSlug"], "name": case["name"], "kind": "source_component_case", **fields,
                   "reading": entry["vernacular"], "notes": list(dict.fromkeys(entry["notes"] + case.get("notes", []))),
                   "source": source, "verified": False}
            if case.get("sources"):
                row["sources"] = fragments
            for field in ("question", "sourceReading", "reportedOutcome", "relatedCaseIds"):
                if field in case:
                    row[field] = case[field]
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
    parser.add_argument("--book", help="Only export cases from this book slug")
    args = parser.parse_args()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    paths = ["references/inventory", "references/annotations", "references/cases", "references/source-editions.json", "sources/fulltext", "sources/normalized"]
    present = [path for path in paths if subprocess.check_output(["git", "ls-tree", revision, "--", path], cwd=ROOT)]
    archive = subprocess.check_output(["git", "archive", "--format=tar", revision, "--", *present], cwd=ROOT)
    with tempfile.TemporaryDirectory(prefix="fateradar-source-cases-") as folder:
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(folder, filter="data")
        data = collect_cases(Path(folder))
    data["sourceRevision"] = revision
    if args.book:
        data["cases"] = [case for case in data["cases"] if case["bookSlug"] == args.book]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"source_revision": revision, "cases": len(data["cases"]), "recomputable": sum(c["canRecompute"] for c in data["cases"]),
                      "expected_unresolved": sum(c.get("expectationStatus") == "source-conflict" for c in data["cases"]),
                      "repeated_inputs": sum(any(field in c for field in ("samePillarsAs", "sameNumbersAs", "sameHexagramInputAs", "sameComponentInputAs")) for c in data["cases"]), "verified": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
