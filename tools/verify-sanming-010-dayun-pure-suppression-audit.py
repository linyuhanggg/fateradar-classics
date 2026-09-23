#!/usr/bin/env python3
"""Verify the source boundary for SMTH-010's Dayun pure-suppression branch."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/SANMINGTONGH_010_DAYUN_PURE_SUPPRESSION_AUDIT_20260924.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_quoted_lines(path: str, expected_sha: str, clauses: list[dict]) -> None:
    source_path = ROOT / path
    raw = source_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_sha, path
    lines = raw.decode("utf-8").splitlines()
    for clause in clauses:
        assert clause["quote"] in lines[clause["line"] - 1], (path, clause)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"] == "fateradar-smth-010-dayun-pure-suppression-audit-v1"
    assert contract["status"] == "undetermined_no_executable_source_threshold"
    assert contract["ruleId"] == "SANMINGTONGH-010"
    assert contract["decision"]["dayunPureSuppression"] == "undetermined"
    assert contract["decision"]["candidateAdopted"] is False
    assert contract["decision"]["rulesChanged"] is False
    assert contract["decision"]["manifestChanged"] is False
    assert contract["decision"]["verified"] is False
    assert contract["scope"]["fullRuleEffect"] == "信息不足"

    primary = contract["primarySource"]
    verify_quoted_lines(primary["path"], primary["sha256"], primary["clauses"])
    for wood in contract["relatedWoodDefinitions"]:
        verify_quoted_lines(
            primary["path"],
            primary["sha256"],
            [{"line": wood["line"], "quote": wood["quote"]}],
        )

    for witness in contract["editorialWitnesses"]:
        verify_quoted_lines(
            witness["path"],
            witness["sha256"],
            [{"line": witness["line"], "quote": witness["quote"]}],
        )

    facsimile = contract["facsimile"]
    assert hashlib.sha256((ROOT / facsimile["path"]).read_bytes()).hexdigest() == facsimile["sha256"]
    prior = json.loads((ROOT / facsimile["priorReviewRecord"]).read_text(encoding="utf-8"))
    assert prior["facsimile"]["sha256"] == facsimile["sha256"]
    assert prior["facsimile"]["pdfPagesVisuallyReviewed"] == [121, 122, 125]

    fixture = contract["fixture"]
    fixture_bytes = FIXTURE.read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == fixture["sha256"]
    case = json.loads(fixture_bytes)["bazi"][fixture["caseId"]]
    assert case["label"] == fixture["label"]
    facts = case["facts"]

    # Check complete natal stems/branches and the selected-year facts used by
    # the existing local L1082 adjudicator; unscoped luck rows cannot fill the
    # 2018 Dayun scope.
    pillars = fixture["natalPillars"]
    for pillar, expected in pillars.items():
        for key in ("gan", "zhi"):
            matches = [
                fact for fact in facts
                if fact.get("key") == key
                and fact.get("scope") == {"layer": "本命", "pillar": pillar}
            ]
            assert len(matches) == 1 and matches[0]["value"] == expected[key], (pillar, key, matches)
    selected_day = [
        fact for fact in facts
        if fact.get("key") == "natal_day_gan"
        and fact.get("scope") == {"layer": "本命", "pillar": "day"}
    ]
    selected_year = [
        fact for fact in facts
        if fact.get("key") == "liunian_gan"
        and fact.get("scope") == {"layer": "流年", "year": fixture["selectedYear"]}
    ]
    selected_dayun = [
        fact for fact in facts
        if fact.get("key") == "dayun_gan_zhi"
        and fact.get("scope") == fixture["effectiveDayun"]["scope"]
    ]
    assert len(selected_day) == len(selected_year) == len(selected_dayun) == 1
    assert selected_day[0]["value"] == fixture["natalDayGan"]
    assert selected_year[0]["value"] == fixture["liunianGan"]
    assert selected_dayun[0]["value"] == fixture["effectiveDayun"]["value"]

    branch_audit = load_module(
        "smth_010_l1082_branch_audit",
        ROOT / "tools/verify-sanming-010-l1082-branch-audit.py",
    )
    observed = branch_audit.evaluate(facts, fixture["selectedYear"])
    assert observed == {
        "entry": "满足",
        "natalGengshenBranch": "不满足",
        "namedGuiWuBranch": "不满足",
        "effectiveSuppressionInput": "undetermined",
        "localAffinityInput": "ruled_out",
        "localL1082Tier": "信息不足",
        "full010Effect": "信息不足",
    }
    assert observed["effectiveSuppressionInput"] == fixture["sourceBranchProjection"]["dayunPureSuppression"]
    assert observed["full010Effect"] == fixture["sourceBranchProjection"]["full010Effect"]

    source_rules = yaml.safe_load(
        (ROOT / "references/books/bazi/sanming-tonghui/rules.yaml").read_text(encoding="utf-8")
    )["rules"]
    original = next(row for row in source_rules if row["rule_id"] == "SANMINGTONGH-010")
    assert original["applicable_to"] == [] and original["verified"] is False

    semantic_keys = {
        "rescue_condition", "transit_effect_semantics",
        "natal_rescue_evidence", "dayun_rescue_evidence",
    }
    assert not any(fact.get("key") in semantic_keys for fact in facts)

    print(
        "PASS SMTH-010 Dayun pure-suppression audit: source/witness/facsimile hashes; "
        "L1082 and same-book context clauses; split_only@2018 scope; undetermined branch; "
        "full 010 remains 信息不足; no rule or manifest promotion"
    )


if __name__ == "__main__":
    main()
