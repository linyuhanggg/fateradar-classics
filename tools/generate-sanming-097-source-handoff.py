#!/usr/bin/env python3
"""Build the pinned, source-only SANMINGTONGH-097 correction candidate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REV = "1fe030d93c7cf8f95ea89b7df669aa7080a7eb2b"
SOURCE_PATH = "references/books/bazi/sanming-tonghui/rules.yaml"
FULLTEXT_PATH = "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
BASE_PATH = "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V7.json"
BASE_SHA = "f3d689cf0c24ca61685548ee4246461701bf1436191d3580c461a3c6e068f306"
FIXTURE_PATH = "tools/reports/facts-sample.json"
FIXTURE_SHA = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"
OUTPUT = ROOT / "docs/closeout/SANMINGTONGH_097_SOURCE_HANDOFF_20260924.json"
RULE_ID = "SANMINGTONGH-097"
DAY_PAIRS = ["甲寅", "乙卯", "己未", "丁未", "庚申", "辛酉", "戊戌", "癸丑"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pinned_file(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{SOURCE_REV}:{path}"], cwd=ROOT)


def evaluator():
    spec = importlib.util.spec_from_file_location("handoff_predicates", ROOT / "tools/eval-predicates.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build() -> dict:
    source_bytes = pinned_file(SOURCE_PATH)
    assert (ROOT / SOURCE_PATH).read_bytes() == source_bytes, "source worktree differs from pinned commit"
    fulltext_bytes = pinned_file(FULLTEXT_PATH)
    base_bytes = (ROOT / BASE_PATH).read_bytes()
    fixture_bytes = (ROOT / FIXTURE_PATH).read_bytes()
    assert sha(base_bytes) == BASE_SHA, "historical V7 manifest changed"
    assert sha(fixture_bytes) == FIXTURE_SHA, "50-case fixture changed"

    source = next(r for r in yaml.safe_load(source_bytes)["rules"] if r["rule_id"] == RULE_ID)
    old = next(r for r in json.loads(base_bytes)["rules"] if r["ruleId"] == RULE_ID)
    cases = json.loads(fixture_bytes)["bazi"]
    assert len(cases) == 50
    assert source["verified"] is False and old["verification"]["verified"] is False
    assert source["quote"] == "八專乃甲寅乙卯己未丁未庚申辛酉戊戌癸丑是也"
    assert source["anchor"] == {"file": FULLTEXT_PATH, "start_line": 1761, "end_line": 1761}
    assert source["quote"] in fulltext_bytes.decode().splitlines()[1760]
    assert source["applicable_to"] == {
        "any_of": [
            {"all_of": [
                {"key": "gan", "value": pair[0], "scope": {"layer": "本命", "pillar": "day"}},
                {"key": "zhi", "value": pair[1], "scope": {"layer": "本命", "pillar": "day"}},
            ]}
            for pair in DAY_PAIRS
        ]
    }
    assert old["primaryTopic"] == "personality" and "overview" in old["secondaryTopics"]

    ev = evaluator()
    old_eval_rule = {"applicable_to": old["applicableTo"]}
    old_counts = Counter(ev.evaluate(old_eval_rule, case["facts"])["verdict"] for case in cases.values())
    new_counts = Counter(ev.evaluate(source, case["facts"])["verdict"] for case in cases.values())
    assert old_counts == {"满足": 12, "不满足": 38}
    assert new_counts == {"满足": 10, "不满足": 40}

    positive = cases["cov1_bazi_3"]["facts"]
    negative = cases["caseA"]["facts"]
    missing_day_zhi = [
        f for f in positive
        if not (f.get("key") == "zhi" and f.get("scope") == {"layer": "本命", "pillar": "day"})
    ]
    example_states = {
        "positive": {"case": "cov1_bazi_3", "verdict": ev.evaluate(source, positive)["verdict"]},
        "negative": {"case": "caseA", "verdict": ev.evaluate(source, negative)["verdict"]},
        "missingNatalDayBranch": {
            "projectionOf": "cov1_bazi_3",
            "removed": {"key": "zhi", "scope": {"layer": "本命", "pillar": "day"}},
            "verdict": ev.evaluate(source, missing_day_zhi)["verdict"],
        },
    }
    assert [entry["verdict"] for entry in example_states.values()] == ["满足", "不满足", "信息不足"]

    return {
        "handoffVersion": "fateradar-p1-bazi-097-source-correction-v1",
        "status": "candidate_not_full_manifest_not_product_importable",
        "sourceRevision": SOURCE_REV,
        "baseManifest": {"path": BASE_PATH, "sha256": BASE_SHA, "version": "v7"},
        "factFixture": {"path": FIXTURE_PATH, "sha256": FIXTURE_SHA, "caseCount": 50},
        "sourceFiles": {
            "rulesYaml": {"path": SOURCE_PATH, "sha256": sha(source_bytes)},
            "fulltext": {"path": FULLTEXT_PATH, "sha256": sha(fulltext_bytes)},
        },
        "rule": {
            "ruleId": RULE_ID,
            "book": "bazi/sanming-tonghui",
            "role": "structural_day_pair_membership_only",
            "statement": source["statement"],
            "quote": source["quote"],
            "anchor": source["anchor"],
            "applicableTo": source["applicable_to"],
            "requiredFacts": [
                {"key": "gan", "scope": {"layer": "本命", "pillar": "day"}},
                {"key": "zhi", "scope": {"layer": "本命", "pillar": "day"}},
            ],
            "caveats": source["caveats"],
            "verified": False,
            "oldV7RealChartStates": dict(old_counts),
            "candidateRealChartStates": dict(new_counts),
            "examples": example_states,
        },
        "proposedTopicDisposition": {
            "overview": "neutral structural evidence only",
            "personality": "remove unsupported attribution; requires a separate effect contract",
        },
        "productState": "V8 retains old 097 and forces its consumer result to unknown; no import or topic change yet",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify committed candidate bytes")
    args = parser.parse_args()
    encoded = (json.dumps(build(), ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        assert OUTPUT.read_bytes() == encoded, "source handoff differs from pinned inputs"
        print(f"PASS source correction candidate sha256={sha(encoded)}")
    else:
        OUTPUT.write_bytes(encoded)
        print(f"Wrote {OUTPUT.relative_to(ROOT)} sha256={sha(encoded)}")


if __name__ == "__main__":
    main()
