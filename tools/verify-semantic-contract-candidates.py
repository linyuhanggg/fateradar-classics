"""Audit-only check for the three unadopted Bazi semantic-contract candidates.

This script must stay read-only with respect to rules.yaml, manifests, and facts.
It proves the source anchors exist and that current fixtures contain shape facts
but no formal semantic outputs. It intentionally does not publish a rule.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "tools/reports/p1-bazi-20260922/semantic-contract-candidates.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"


def facts_for(case: dict, year: int | None = None) -> list[dict]:
    facts = case["facts"]
    if year is None:
        return facts
    return [f for f in facts if f.get("scope", {}).get("year") == year]


def rule_block(rule_id: str) -> str:
    text = (ROOT / "references/books/bazi/sanming-tonghui/rules.yaml").read_text()
    if rule_id == "DITIANSUICHA-051":
        text = (ROOT / "references/books/bazi/ditiansui-chanwei/rules.yaml").read_text()
    match = re.search(rf"(?ms)^- rule_id: {re.escape(rule_id)}\n(.*?)(?=^- rule_id:|\Z)", text)
    if not match:
        raise AssertionError(f"missing rule block: {rule_id}")
    return match.group(0)


def main() -> int:
    report = json.loads(REPORT.read_text())
    sample_bytes = FIXTURE.read_bytes()
    sample = json.loads(sample_bytes)["bazi"]
    checks: list[dict] = []

    assert report["status"] == "not_adopted"
    assert report["semanticContractStatus"] == "pending"
    expected_sha = report["fixture"]["sha256"]
    checks.append(
        {
            "check": "fixture_sha256",
            "expected": expected_sha,
            "actual": hashlib.sha256(sample_bytes).hexdigest(),
        }
    )
    assert checks[-1]["expected"] == checks[-1]["actual"]

    source_lines = {
        "SANMINGTONGH-010": (ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md").read_text().splitlines(),
        "SANMINGTONGH-011": (ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md").read_text().splitlines(),
        "DITIANSUICHA-051": (ROOT / "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md").read_text().splitlines(),
    }
    anchor_needles = {
        "SANMINGTONGH-010": (1081, "日犯歳君"),
        "SANMINGTONGH-011": (1084, "嵗運并臨"),
        "DITIANSUICHA-051": (13407, "喜神用神"),
    }
    for contract in report["contracts"]:
        rid = contract["ruleId"]
        assert contract["adoptableNow"] is False
        block = rule_block(rid)
        assert re.search(r"(?m)^\s+applicable_to:\s*\[\]\s*$", block)
        assert re.search(r"(?m)^\s+verified:\s*false\s*$", block)
        line_number, needle = anchor_needles[rid]
        line = source_lines[rid][line_number - 1]
        assert needle in line, (rid, line_number, line)
        missing_by_case = {}
        required = set(contract["candidateContract"]["requiredFacts"])
        for case_name, case in sample.items():
            present = {f["key"] for f in case["facts"]}
            missing_by_case[case_name] = sorted(required - present)
        checks.append(
            {
                "check": rid,
                "ruleMutation": "none",
                "sourceAnchor": {"line": line_number, "needle": needle},
                "missingRequiredFactsInCases": missing_by_case,
                "fixtureTriState": contract["currentEvidence"]["fixtures"],
            }
        )

    # Shape facts prove only the currently supported structural boundaries.
    binglin = facts_for(sample["caseFlowYearBinglin"], 1993)
    assert any(f["key"] == "suiyun_binglin" and f["value"] == "是" for f in binglin)
    assert any(f["key"] == "dayun_gan_zhi" and f["value"] == "癸酉" for f in binglin)
    unknown = facts_for(sample["caseFlowYearUnknown"], 2100)
    for key in ("suiyun_binglin", "dayun_liunian_relation_class"):
        assert any(f["key"] == key and f["value"] == "信息不足" for f in unknown)
    checks.append(
        {
            "check": "shape_fixture_boundaries",
            "caseFlowYearBinglin1993": "shape facts present; semantic outputs absent",
            "caseFlowYearUnknown2100": "explicit unknown facts present",
        }
    )

    result = {
        "schema": "fateradar-bazi-semantic-contract-candidate-audit-v1",
        "status": "pass",
        "candidateAdopted": False,
        "rulesChanged": False,
        "manifestChanged": False,
        "checks": checks,
        "conclusion": "三条候选均保留 blocked；当前只有结构形态或自由文本，缺正式语义键和满足/不满足样盘。",
    }
    out = ROOT / "tools/reports/p1-bazi-20260922/semantic-contract-candidate-audit.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
