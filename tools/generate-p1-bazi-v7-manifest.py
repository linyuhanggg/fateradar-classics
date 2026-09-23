#!/usr/bin/env python3
"""Create a V7 candidate handoff that adds explicit 辛日寅月 scope to P1-06."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json"
BASE_SHA = "39e53a6c5c3693334209d80eb2f9e9002339fff2117b64f1988d6f2a02f344a6"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V7.json"
FIXTURE_PATH = ROOT / "tools/reports/facts-sample.json"
FIXTURE_SHA = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"
EVALUATOR_PATH = ROOT / "tools/eval-predicates.py"
EVALUATOR_SHA = "9e22790a852e424cf90e6cef4c04450af31f853943e71b621938ed5ee720f910"
RULE_ID = "ZPR-P1-06"
FACT_KEY = "natal_yin_simple_hidden_exposure_pattern"
DAY_SCOPE = {"layer": "本命", "pillar": "day"}
MONTH_SCOPE = {"layer": "本命", "pillar": "month"}
SOURCE_REV = "4434c43e7c729c1547f49897bb227870b8d402a0"
AUDIT_HEAD = "6c0d7b9454d34029c8855cf07f686839b9f4174c"
PREDICATE_DOC = "docs/PREDICATE-LANGUAGE-V3.md"
PREDICATE_DOC_SHA = "95641647798655f175fc2b2627208d0a3df188a91767ff653719d93e9d4c0bc9"

PREDICATES = [
    {"key": "gan", "value": "辛", "scope": DAY_SCOPE},
    {"key": "zhi", "value": "寅", "scope": MONTH_SCOPE},
    {"key": "yueling", "value": "寅", "scope": MONTH_SCOPE},
    {"key": FACT_KEY, "value": "甲丙", "scope": MONTH_SCOPE},
]

PROBES = {
    "positive": ("caseP1_ZPR_month_xin_jia_bing_1954", "满足"),
    "secondPositive": ("caseP1_ZPR_month_xin_jia_bing_1984", "满足"),
    "negative": ("caseP1_ZPR_month_xin_no_jia_1979", "不满足"),
    "nonYinMonthBranchNegative": ("cov1_bazi_4", "不满足"),
    "nonYinMonthOrderNegative": ("cov3_bazi_6", "不满足"),
    "tripleExposureUnknown": ("caseP1_ZPR_month_xin_jia_bing_wu_1984", "信息不足"),
    "meetingUnknown": ("caseP1_ZPR_month_xin_jia_bing_meeting_1994", "信息不足"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def evaluation(evaluator, entry: dict, facts: list[dict], case_id: str) -> dict:
    result = evaluator.evaluate(
        {"rule_id": RULE_ID, "applicable_to": entry["applicableTo"], "verified": False}, facts
    )
    return {
        "case": case_id,
        "factCount": len(facts),
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "factCoverage": result["fact_coverage"],
        "missingFactKeys": result.get("missing_fact_keys", []),
    }


def remove_scope_key(facts: list[dict], key: str, scope: dict) -> list[dict]:
    return [fact for fact in facts if not (fact.get("key") == key and fact.get("scope") == scope)]


def scoped_values(facts: list[dict], key: str, scope: dict) -> set[str]:
    return {
        str(fact.get("value"))
        for fact in facts
        if fact.get("key") == key and fact.get("scope") == scope
    }


def make_manifest() -> dict:
    base_bytes = BASE_PATH.read_bytes()
    assert sha256(base_bytes) == BASE_SHA, "locked V6 changed"
    assert sha256(FIXTURE_PATH.read_bytes()) == FIXTURE_SHA, "shared fixture changed"
    assert sha256(EVALUATOR_PATH.read_bytes()) == EVALUATOR_SHA, "predicate evaluator changed"
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v6"
    assert base["semanticContractStatus"] == "pending"
    assert len(base["rules"]) == 15

    predicate_doc = subprocess.check_output(
        ["git", "show", f"{SOURCE_REV}:{PREDICATE_DOC}"], cwd=ROOT
    )
    assert sha256(predicate_doc) == PREDICATE_DOC_SHA
    predicate_text = predicate_doc.decode("utf-8")
    assert "| { all_of: [clause, ...] }" in predicate_text
    assert "`scope` 允许字段" in predicate_text and "`pillar`" in predicate_text

    fixture_bytes = FIXTURE_PATH.read_bytes()
    fixture = json.loads(fixture_bytes)["bazi"]
    assert len(fixture) == 50
    evaluator = load_module(EVALUATOR_PATH, "p1_v7_predicate_evaluator")

    for case_id, month in (("cov1_bazi_4", "丑"), ("cov3_bazi_6", "辰")):
        facts = fixture[case_id]["facts"]
        assert scoped_values(facts, "gan", DAY_SCOPE) == {"辛"}
        assert scoped_values(facts, "zhi", MONTH_SCOPE) == {month}
        assert scoped_values(facts, "yueling", MONTH_SCOPE) == {month}
        assert not scoped_values(facts, FACT_KEY, MONTH_SCOPE)
    for case_id in (PROBES["positive"][0], PROBES["tripleExposureUnknown"][0],
                    PROBES["meetingUnknown"][0]):
        facts = fixture[case_id]["facts"]
        assert scoped_values(facts, "gan", DAY_SCOPE) == {"辛"}
        assert scoped_values(facts, "zhi", MONTH_SCOPE) == {"寅"}
        assert scoped_values(facts, "yueling", MONTH_SCOPE) == {"寅"}
    for case_id in (PROBES["tripleExposureUnknown"][0], PROBES["meetingUnknown"][0]):
        assert not scoped_values(fixture[case_id]["facts"], FACT_KEY, MONTH_SCOPE)

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v7"
    manifest["generatedAt"] = "2026-09-24"
    manifest["generatedBy"] = "tools/generate-p1-bazi-v7-manifest.py"
    manifest["sourceHeadAtAudit"] = AUDIT_HEAD
    manifest["previousHandoff"] = {
        "path": str(BASE_PATH.relative_to(ROOT)),
        "sha256": BASE_SHA,
        "ruleCount": 15,
    }
    manifest["handoffStatus"] = "candidate_pending_product_import"
    manifest["scopeCorrection"] = {
        "ruleId": RULE_ID,
        "sourceAnchor": {
            "file": "sources/fulltext/bazi/ziping-zhenquan/fulltext.md",
            "startLine": 435,
            "endLine": 435,
            "quote": "如辛生寅月，透丙化官，而又透甲，格成正財，正官乃其兼格也；",
        },
        "predicateSchema": {
            "version": "fateradar-rules-v3",
            "document": PREDICATE_DOC,
            "documentRev": SOURCE_REV,
            "documentSha256": PREDICATE_DOC_SHA,
        },
        "priorV6Counts": {"满足": 2, "不满足": 44, "信息不足": 4},
        "candidateV7Counts": {"满足": 2, "不满足": 46, "信息不足": 2},
        "reason": (
            "V6 只核本命日干和寅月专属派生结构键；cov1_bazi_4 与 cov3_bazi_6 的本命月支、"
            "月令已知为丑、辰，但派生键缺席，故旧谓词给信息不足。V7 将 L435 明示的寅月"
            "适用域以现有 zhi/yueling 事实显式列入 all_of。"
        ),
        "preserved": [
            "V6 文件与 SHA-256 不变。",
            "共享 fixture 不变。",
            "ZPR-E-02 的整体语义、rescue 标签与 verified=false 不变。",
            "不新增格局作用、成败、救应、吉凶或流年效果推断。",
            "Classic rules.yaml 与 dist/rules/bazi.json 不由本候选改写。",
        ],
    }
    entry = manifest["rules"][-1]
    assert entry["ruleId"] == RULE_ID
    entry["applicableTo"] = {"all_of": copy.deepcopy(PREDICATES)}
    entry["requiredFacts"] = [
        {"key": "gan", "scope": DAY_SCOPE, "predicateScope": [DAY_SCOPE]},
        {"key": "zhi", "scope": MONTH_SCOPE, "predicateScope": [MONTH_SCOPE]},
        {"key": "yueling", "scope": MONTH_SCOPE, "predicateScope": [MONTH_SCOPE]},
        {"key": FACT_KEY, "scope": MONTH_SCOPE, "predicateScope": [MONTH_SCOPE]},
    ]
    entry["factSlicePolicy"] = (
        "只消费本命日干、本命月支、本命月令与完整寅月清楚暴露形态；月支和月令须均为寅。"
        "流年干、其它层事实和旧格局标签不参与。"
    )
    entry["semantics"]["notSatisfied"] = (
        "本命所需事实完整且自洽时，任一适用条件已知不成立（包括月支或月令明确非寅）即不满足；"
        "只否定辛日寅月甲丙清楚例型。"
    )
    entry["semantics"]["unknown"] = (
        "月支、月令、日干或结构键缺失/冲突时保留信息不足；三透戊、寅午戌全会仍因结构键缺席而未知。"
    )
    new_scope_caveat = (
        "V7 在 V6 谓词上显式增加 zhi=寅@本命月柱 与 yueling=寅@本命月柱；"
        "月支、月令为丑/辰的已知盘只判本窄例型不满足，不补推其其它格局入口。"
    )
    entry["caveats"] = [*entry["caveats"], new_scope_caveat]
    entry["exceptionsAndBreaks"] = list(entry["caveats"])
    entry["conflictNotes"] = [
        *entry["conflictNotes"],
        "V7 两张新增不满足盘的本命月支与月令均一致且已知为丑/辰；单键同 scope 多值冲突仍按谓词语言返回信息不足。",
    ]

    results = {}
    for label, (case_id, expected) in PROBES.items():
        result = evaluation(evaluator, entry, fixture[case_id]["facts"], case_id)
        assert result["verdict"] == expected, (label, result)
        results[label] = result

    positive = fixture[PROBES["positive"][0]]["facts"]
    mutation_cases = {
        "missingStructuralFact": remove_scope_key(positive, FACT_KEY, MONTH_SCOPE),
        "missingMonthBranch": remove_scope_key(positive, "zhi", MONTH_SCOPE),
        "missingMonthOrder": remove_scope_key(positive, "yueling", MONTH_SCOPE),
        "conflictingStructuralFact": [*positive, {"key": FACT_KEY, "value": "丙", "scope": MONTH_SCOPE}],
        "conflictingMonthBranch": [*positive, {"key": "zhi", "value": "丑", "scope": MONTH_SCOPE}],
        "conflictingMonthOrder": [*positive, {"key": "yueling", "value": "丑", "scope": MONTH_SCOPE}],
        "foreignLayerGuard": [
            *remove_scope_key(positive, FACT_KEY, MONTH_SCOPE),
            {"key": FACT_KEY, "value": "甲丙", "scope": {"layer": "流年", "year": 2018}},
        ],
    }
    for label, facts in mutation_cases.items():
        result = evaluation(evaluator, entry, facts, label)
        assert result["verdict"] == "信息不足", (label, result)
        results[label] = result

    states = Counter(
        evaluator.evaluate(
            {"rule_id": RULE_ID, "applicable_to": entry["applicableTo"], "verified": False},
            case["facts"],
        )["verdict"]
        for case in fixture.values()
    )
    state_counts = {state: states[state] for state in ("满足", "不满足", "信息不足")}
    assert state_counts == {"满足": 2, "不满足": 46, "信息不足": 2}
    entry["verification"].update(results)
    entry["verification"]["allRealChartStates"] = state_counts
    entry["verification"]["result"] = (
        "50 张固定真日期盘按 V7 谓词得到满足 2、不满足 46、信息不足 2；"
        "两张已知非寅月盘明确落入本窄例型之外，三透与全会两例仍未知。"
        "只验证局部来源入口的输入三态，不证明完整作用或现实准确率。"
    )
    manifest["exportState"] = {
        "candidateOnly": True,
        "sourceRuleYamlChanged": False,
        "classicsDistChanged": False,
        "note": (
            "本 V7 是供独立审核的 handoff predicate 候选。规则项原有 export 元数据仍指向 V6"
            "固定基线；本文件不声称该 predicate 已写入 Classic rules.yaml 或 dist。"
        ),
    }
    assert manifest["semanticContractStatus"] == "pending"
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    manifest = make_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    digest = sha256(args.output.read_bytes())
    print(f"wrote {args.output} rules=15 sha256={digest}")


if __name__ == "__main__":
    main()
