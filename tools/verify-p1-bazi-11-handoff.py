#!/usr/bin/env python3
"""Verify the locked 11-rule P1 handoff against its source and real fixtures."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json"
PRODUCT_FIXTURE = Path("/Users/sync/code/cosmic-fortune-lab/tests/fixtures/facts-sample.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    spec = importlib.util.spec_from_file_location("p1_manifest_generator", ROOT / "tools/generate-p1-bazi-manifest.py")
    require(spec is not None and spec.loader is not None, "cannot load manifest generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    regenerated = module.make_manifest(MANIFEST, None)
    actual_bytes = MANIFEST.read_bytes()
    expected_bytes = (json.dumps(regenerated, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    require(actual_bytes == expected_bytes, "manifest differs from reproducible generator output")
    manifest = json.loads(actual_bytes)
    require(manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v2", "wrong handoff version")
    require(manifest["semanticContractStatus"] == "pending", "semantic blockers were upgraded")
    require(len(manifest["rules"]) == 11, "handoff must contain 11 distinct rules")
    require(len({rule["ruleId"] for rule in manifest["rules"]}) == 11, "duplicate rule ID")
    require(all(rule["verification"]["verified"] is False for rule in manifest["rules"]), "verified was upgraded")
    require(manifest["carryoverTenSemanticSha256"] == module.TEN_RULE_SEMANTIC_SHA256, "old ten changed meaning")
    require(module.carryover_semantic_sha(manifest["rules"]) == module.TEN_RULE_SEMANTIC_SHA256, "old ten changed meaning")

    local_fixture = (ROOT / manifest["factFixture"]["path"]).read_bytes()
    require(hashlib.sha256(local_fixture).hexdigest() == module.FIXTURE_SHA256, "fixture hash drift")
    if PRODUCT_FIXTURE.exists():
        require(local_fixture == PRODUCT_FIXTURE.read_bytes(), "product and classics fixture differ")

    entry = next(rule for rule in manifest["rules"] if rule["ruleId"] == "ZPR-P1-03")
    require(entry["primaryTopic"] == "overview" and entry["secondaryTopics"] == [], "classification escaped overview")
    require(entry["role"] == "source_classification", "wrong semantic role")
    require(all("ZPR-P1-03" not in topic["ruleIds"] for name, topic in manifest["topics"].items() if name != "overview"), "classification escaped overview")
    require(entry["candidateOutput"] == {
        "entryId": "ZPR-P1-01", "entry": "甲辰月透戊偏财", "category": "财",
        "direction": "顺用", "status": "候选", "scope": {"layer": "本命"}, "emitOn": "满足",
    }, "candidate output exceeds source classification")
    require({name: entry["verification"][name]["verdict"] for name in ("positive", "negative", "boundary", "coexistingEntry")} == {
        "positive": "满足", "negative": "不满足", "boundary": "信息不足", "coexistingEntry": "满足",
    }, "real-case results changed")
    require(entry["verification"]["boundary"]["missingFactKeys"] == ["gan"], "missing pillar was treated as false")
    require([item["anchor"]["startLine"] for item in entry["candidateSources"]] == [328, 544, 548], "three-source chain incomplete")
    for item in entry["candidateSources"]:
        anchor = item["anchor"]
        source_line = (ROOT / anchor["file"]).read_text(encoding="utf-8").splitlines()[anchor["startLine"] - 1]
        require(item["quote"] in source_line, f"quote drift at L{anchor['startLine']}")
    require("ZPR-E-02" not in {rule["ruleId"] for rule in manifest["rules"]}, "E-02 was imported")

    print(f"PASS 11-rule handoff; sha256={hashlib.sha256(actual_bytes).hexdigest()}; oldTen={module.TEN_RULE_SEMANTIC_SHA256}")


if __name__ == "__main__":
    main()
