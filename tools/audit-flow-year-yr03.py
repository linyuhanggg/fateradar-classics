"""Audit the conservative YUANHAIZIPIN-YR-03 flow-year relation rule."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("flow_eval", ROOT / "tools/eval-predicates.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sample_path = ROOT / "tools/reports/facts-sample.json"
sample = json.loads(sample_path.read_text())["bazi"]
probe = {
    "rule_id": "YUANHAIZIPIN-YR-03",
    "applicable_to": {
        "any_of": [
            {"key": "dayun_liunian_relation_class", "value": value, "scope": {"layer": "流年"}}
            for value in ("相冲", "相克", "相刑")
        ]
    },
}
rows = []
for case, year, expected in [
    ("caseFlowYear", 2025, "满足"),
    ("caseFlowYear", 2026, "不满足"),
    ("caseFlowYearUnknown", 2100, "信息不足"),
]:
    facts = [f for f in sample[case]["facts"] if f.get("scope", {}).get("year") == year]
    actual = module.evaluate(probe, facts)["verdict"]
    rows.append(
        {
            "case": case,
            "year": year,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
            "facts": [f for f in facts if f["key"] == "dayun_liunian_relation_class"],
        }
    )
report = {
    "command": "python3 tools/audit-flow-year-yr03.py",
    "fixtureSha256": hashlib.sha256(sample_path.read_bytes()).hexdigest(),
    "ruleId": "YUANHAIZIPIN-YR-03",
    "ruleAdopted": True,
    "scopePolicy": "先按选定 scope.year 过滤，再执行流年层谓词",
    "passed": all(r["passed"] for r in rows),
    "cases": rows,
}
out = ROOT / "tools/reports/p1-bazi-20260922/flow-year-yr03.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report["passed"] else 1)
