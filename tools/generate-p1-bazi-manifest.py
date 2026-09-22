#!/usr/bin/env python3
"""Generate the product-facing P1 Bazi rule/Fact handoff.

The YAML files remain the rule source of truth.  This manifest only adds the
topic ownership, Fact scope contract, and fixed-fixture evidence that the
product needs when building Fact -> RuleEvaluation -> TopicEvaluation.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLASSICS_REV = "6321186f6aeebd0737537c45286153eedf49adb4"
SAMPLE = ROOT / "tools/reports/facts-sample.json"
PRODUCT_ROOT = Path("/Users/sync/code/cosmic-fortune-lab")

# A rule is listed once here and may be referenced by more than one topic.  A
# topic assignment is handoff metadata; it does not change rules.yaml.
RULE_META = {
    "DITIANSUICHA-003": {
        "primaryTopic": "overview",
        "secondaryTopics": ["personality", "health"],
        "requiredFacts": [{"key": "rizhu_strength", "scope": {"layer": "本命"}}],
        "fixtures": {"positive": "cov1_bazi_2", "negative": "caseA", "boundaryRemove": ["rizhu_strength"]},
        "role": "supporting",
        "extraCaveats": ["只表示中和/偏枯的传统结构证据，不是现实吉凶或健康诊断。"],
    },
    "DITIANSUICHA-004": {
        "primaryTopic": "personality",
        "secondaryTopics": [],
        "requiredFacts": [{"key": "rizhu_strength", "scope": {"layer": "本命"}}],
        "fixtures": {"positive": "cov1_bazi_2", "negative": "caseA", "boundaryRemove": ["rizhu_strength"]},
        "role": "method",
        "extraCaveats": ["这是方法论/取舍倾向证据，不能生成固定人格标签。"],
    },
    "DITIANSUICHA-DR-03": {
        "primaryTopic": "health",
        "secondaryTopics": ["overview", "personality"],
        "requiredFacts": [{"key": "rizhu_strength", "scope": {"layer": "本命"}}],
        "fixtures": {"positive": "cov1_bazi_2", "negative": "caseA", "boundaryRemove": ["rizhu_strength"]},
        "role": "supporting",
        "extraCaveats": ["健康主题只可显示传统平衡/作息关注点；不作疾病、风险概率或医疗建议。"],
    },
    "DITIANSUICHA-DR-06": {
        "primaryTopic": "career",
        "secondaryTopics": ["wealth", "overview"],
        "requiredFacts": [{"key": "rizhu_strength", "scope": {"layer": "本命"}}],
        "fixtures": {"positive": "cov1_bazi_1", "negative": "caseA", "boundaryRemove": ["rizhu_strength"]},
        "role": "structural",
        "extraCaveats": ["“从格”还需要无根、最旺之神和破格条件；本条谓词只表达极弱入口，不能单独判从财/从煞。"],
    },
    "SANMINGTONGH-015": {
        "primaryTopic": "overview",
        "secondaryTopics": ["relationship", "career"],
        "requiredFacts": [{"key": "zhi", "scope": {"layer": "本命", "pillar": ["year", "month", "day", "time"]}}],
        "fixtures": {"positive": "cov1_bazi_1", "negative": "caseA", "boundaryRemove": ["zhi"]},
        "role": "structural",
        "extraCaveats": ["三合组合是结构证据，不等于关系事件、职业结果或富贵结论；半合、成势和冲破仍待判断。", "产品评估时只传本命四柱。"],
    },
    "DITIANSUICHA-032": {
        "primaryTopic": "relationship",
        "secondaryTopics": ["overview"],
        "requiredFacts": [{"key": "zhi", "scope": {"layer": "本命", "pillar": ["year", "month", "day", "time"]}}],
        "fixtures": {"positive": "caseA", "negative": "caseB", "boundaryRemove": ["zhi"]},
        "role": "structural",
        "extraCaveats": ["子午相对只表示传统冲动/变化证据，不能写成分手、疾病或迁移事件。", "规则谓词未写 layer，产品必须只传本命四柱。"],
    },
    "SANMINGTONGH-097": {
        "primaryTopic": "personality",
        "secondaryTopics": ["overview"],
        "requiredFacts": [
            {"key": "gan", "scope": {"layer": "本命", "pillar": "day"}},
            {"key": "zhi", "scope": {"layer": "本命", "pillar": "day"}},
        ],
        "fixtures": {"positive": "caseA", "negative": "caseB", "boundaryRemove": ["gan"]},
        "role": "structural",
        "extraCaveats": ["八专日只说明日柱组合入口；身强、过旺、制化和月令仍是未表达条件。"],
    },
    "YUANHAIZIPIN-YR-03": {
        "primaryTopic": "overview",
        "secondaryTopics": ["career", "wealth"],
        "requiredFacts": [{"key": "dayun_liunian_relation_class", "scope": {"layer": "流年", "year": "selected"}}],
        "fixtures": {
            "positive": "caseFlowYear",
            "positiveYear": 2025,
            "negative": "caseFlowYear",
            "negativeYear": 2026,
            "boundary": "caseFlowYearUnknown",
            "boundaryYear": 2100,
        },
        "role": "structural",
        "extraCaveats": ["只记录相冲/相克/相刑的流年关系忌象候选，不等于现实凶事；必须先按当前选定年份过滤事实。", "制化、喜忌和命局作用尚未由本条表达，产品应保留后续 unknown。"],
        "applicableLayers": ["流年"],
        "unsupportedLayers": ["本命", "大运", "流月", "流日"],
    },
}

TOPIC_META = {
    "overview": {
        "status": "partial",
        "ruleIds": ["DITIANSUICHA-003", "DITIANSUICHA-DR-03", "DITIANSUICHA-DR-06", "SANMINGTONGH-015", "DITIANSUICHA-032", "SANMINGTONGH-097", "YUANHAIZIPIN-YR-03"],
        "requiredFactKeys": ["rizhu", "yueling", "zhi", "rizhu_strength", "geju", "yongshen", "canggan"],
        "blockers": ["本命结构事实可以进入证据层；格局成败、用神细节和岁运触发尚未形成每条规则的完整条件。"],
    },
    "personality": {
        "status": "partial",
        "ruleIds": ["DITIANSUICHA-003", "DITIANSUICHA-004", "DITIANSUICHA-DR-03", "SANMINGTONGH-097"],
        "requiredFactKeys": ["rizhu", "rizhu_strength", "shishen", "canggan"],
        "blockers": ["只交付稳定倾向证据；不交付绝对人格标签，需产品保留现实核对问题。"],
    },
    "career": {
        "status": "partial",
        "ruleIds": ["DITIANSUICHA-DR-06", "SANMINGTONGH-015", "YUANHAIZIPIN-YR-03"],
        "requiredFactKeys": ["rizhu_strength", "shishen", "geju", "yongshen", "yueling"],
        "blockers": ["职位/行业、完整格局成败、取用和岁运窗口不是当前三条规则的充分条件。"],
    },
    "wealth": {
        "status": "partial",
        "ruleIds": ["DITIANSUICHA-DR-06", "YUANHAIZIPIN-YR-03"],
        "requiredFactKeys": ["rizhu_strength", "shishen", "yongshen"],
        "blockers": ["当前只可交付‘极弱/从格入口’结构证据；财星位置、身财两停、比劫夺财和岁运尚未形成完整合同。"],
    },
    "relationship": {
        "status": "partial",
        "ruleIds": ["SANMINGTONGH-015", "DITIANSUICHA-032"],
        "requiredFactKeys": ["rizhu", "zhi", "shishen"],
        "blockers": ["配偶星/日支作用、性别条件和关系反馈没有完整 Fact 合同；冲合只能作为结构证据。"],
    },
    "health": {
        "status": "partial",
        "ruleIds": ["DITIANSUICHA-003", "DITIANSUICHA-DR-03"],
        "requiredFactKeys": ["rizhu_strength", "yueling", "gan_element"],
        "blockers": ["没有医疗、症状、作息等产品事实；古籍结构只能做传统养生关注点，不能做诊断或事件预测。"],
    },
}

BLOCKED = [
    {"ruleId": "DITIANSUICHA-DR-02", "status": "blocked", "reason": "V14 低对应度：固定锚点 L10521 只有“合有宜不宜”，没有三合/方局取值；当前谓词的具体组合不能从该 quote 追溯，退回等待更精确出处。"},
    {"ruleId": "DITIANSUICHA-012", "status": "blocked", "reason": "谓词只列十神/格局值，未表达声明中的月令、透干、司令和破格条件；固定样盘 24/24 满足，不能作为区分性规则。"},
    {"ruleId": "SANMINGTONGH-102", "status": "blocked", "reason": "声明含年柱、时柱、日坐、身强和比劫冲夺，谓词仅为无柱位 shishen OR；固定样盘 24/24 满足。"},
    {"ruleId": "YUANHAIZIPIN-023", "status": "blocked", "reason": "正财谓词无柱位/身能任财条件，且古代妻财语义不能直接转成现代伴侣或收入结论。"},
    {"ruleId": "YUANHAIZIPIN-024", "status": "blocked", "reason": "声明明确女命、夫宫和子星，但当前 FactKey 没有性别/夫宫/子星完整合同；现谓词命中不能判关系结果。"},
    {"ruleId": "SANMINGTONGH-069", "status": "blocked", "reason": "同类女命/正官夫星规则缺少性别和夫宫条件，保持 unknown。"},
    {"ruleId": "DITIANSUICHA-031", "status": "blocked", "reason": "当前固定样盘没有同时命中卯、酉的正例；需增加独立固定正例并确认本命层绑定后再进入 P1。"},
    {"ruleId": "SANMINGTONGH-R-02", "status": "blocked", "reason": "谓词表达月令藏干+透干，但固定锚点 L3218 为偏财长段，未支持该陈述；等待正确出处后再评估。"},
    {"ruleId": "YUANHAIZIPIN-008", "status": "blocked", "reason": "同样的月令藏干+透干谓词锚到‘假令月令有用神’，不足以支持完整陈述。"},
]


def load_eval_module():
    path = ROOT / "tools/eval-predicates.py"
    spec = importlib.util.spec_from_file_location("p1_eval_predicates", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_rule_index() -> dict[str, dict]:
    index: dict[str, dict] = {}
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        book = data.get("book") or {}
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or rule.get("rule_id") not in RULE_META:
                continue
            rid = rule["rule_id"]
            if rid in index:
                raise RuntimeError(f"ruleId 重复：{rid}")
            index[rid] = {
                "book": f"{book.get('system')}/{book.get('slug')}",
                "title": book.get("title"),
                **rule,
            }
    missing = sorted(set(RULE_META) - set(index))
    if missing:
        raise RuntimeError(f"manifest ruleId 不在 YAML：{missing}")
    return index


def leaves(node) -> list[dict]:
    if isinstance(node, list):
        out: list[dict] = []
        for child in node:
            out.extend(leaves(child))
        return out
    if not isinstance(node, dict):
        return []
    if isinstance(node.get("key"), str):
        return [node]
    out = []
    for key in ("any_of", "all_of", "none_of"):
        for child in node.get(key) or []:
            out.extend(leaves(child))
    return out


def fixture_result(module, rule: dict, facts: list[dict], case: str, remove: list[str] | None = None, year: int | None = None) -> dict:
    selected = [f for f in facts if f.get("key") not in set(remove or [])]
    if year is not None:
        selected = [f for f in selected if (f.get("scope") or {}).get("year") == year]
    evaluation = module.evaluate(rule, selected)
    result = {
        "case": case,
        "factCount": len(selected),
        "verdict": evaluation["verdict"],
        "confidence": evaluation.get("confidence"),
        "factCoverage": evaluation.get("fact_coverage"),
        "missingFactKeys": evaluation.get("missing_fact_keys", []),
    }
    if year is not None:
        result["year"] = year
    return result


def make_manifest(output: Path, export_file: Path | None) -> dict:
    module = load_eval_module()
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    bazi_cases = sample["bazi"]
    try:
        diff_numstat = subprocess.check_output(
            ["git", "-C", str(ROOT), "diff", "--numstat", "--", str(SAMPLE.relative_to(ROOT))],
            text=True,
        ).strip() or "无工作区 diff"
    except (OSError, subprocess.CalledProcessError):
        diff_numstat = "无法读取工作区 diff"
    shensha_fact_count = sum(
        1
        for case in bazi_cases.values()
        for fact in case.get("facts", [])
        if fact.get("key") == "shensha"
    )
    rules = load_rule_index()
    entries = []
    for rid, meta in RULE_META.items():
        rule = rules[rid]
        if rule.get("verified") is True:
            raise RuntimeError(f"禁止把 verified=true 带入 P1 manifest：{rid}")
        anchor = rule.get("anchor") or {}
        if not all(isinstance(anchor.get(k), (str, int)) for k in ("file", "start_line", "end_line")):
            raise RuntimeError(f"规则缺少完整 anchor：{rid}")
        fixture = meta["fixtures"]
        pos = fixture_result(module, rule, bazi_cases[fixture["positive"]]["facts"], fixture["positive"], year=fixture.get("positiveYear"))
        neg = fixture_result(module, rule, bazi_cases[fixture["negative"]]["facts"], fixture["negative"], year=fixture.get("negativeYear"))
        if "boundary" in fixture:
            boundary = fixture_result(module, rule, bazi_cases[fixture["boundary"]]["facts"], fixture["boundary"], year=fixture.get("boundaryYear"))
        else:
            boundary = fixture_result(module, rule, bazi_cases[fixture["positive"]]["facts"], fixture["positive"], fixture.get("boundaryRemove"), year=fixture.get("positiveYear"))
        expected = {"positive": "满足", "negative": "不满足", "boundary": "信息不足"}
        actual = {"positive": pos["verdict"], "negative": neg["verdict"], "boundary": boundary["verdict"]}
        if actual != expected:
            raise RuntimeError(f"固定样盘三态失败 {rid}: actual={actual} expected={expected}")
        required = []
        for item in meta["requiredFacts"]:
            required.append({"key": item["key"], "scope": item["scope"], "predicateScope": [p.get("scope", {}) for p in leaves(rule.get("applicable_to")) if p.get("key") == item["key"]]})
        export_info = {"artifact": "dist/rules/bazi.json", "classicsRev": CLASSICS_REV}
        if export_file and export_file.exists():
            export_info["generatedFile"] = str(export_file)
            export_info["sha256"] = hashlib.sha256(export_file.read_bytes()).hexdigest()
        entries.append({
            "ruleId": rid,
            "art": "bazi",
            "book": rule["book"],
            "primaryTopic": meta["primaryTopic"],
            "secondaryTopics": meta["secondaryTopics"],
            "status": "adopted_as_provisional_evidence",
            "role": meta["role"],
            "statement": rule["statement"],
            "quote": rule["quote"],
            "anchor": {"file": anchor["file"], "startLine": anchor["start_line"], "endLine": anchor["end_line"]},
            "applicableTo": rule.get("applicable_to") or [],
            "requiredFacts": required,
            "applicableLayers": meta.get("applicableLayers", ["本命"]),
            "unsupportedLayers": meta.get("unsupportedLayers", ["大运", "流年", "流月", "流日"]),
            "semantics": {
                "satisfied": "applicable_to 整体满足，且返回完整 matched Fact 见证集。",
                "notSatisfied": "所需 FactKey 存在，但 applicable_to 没有命中；不能解释为现实事件不发生。",
                "unknown": "任一所需 FactKey 缺失，或产品传入的时间层/柱位不在本 manifest 合同内；不能降级为 not_satisfied。",
            },
            "caveats": list(rule.get("caveats") or []) + meta["extraCaveats"],
            "exceptionsAndBreaks": list(rule.get("caveats") or []) + meta["extraCaveats"],
            "conflictNotes": ["不同古籍/流派对旺衰、格局与冲合解释可能冲突；产品保留来源与 unknown，不在本仓合并成分数。"],
            "verification": {
                "verified": False,
                "fixtureSource": "tools/reports/facts-sample.json",
                "positive": pos,
                "negative": neg,
                "boundary": boundary,
                "result": "三态固定样盘通过；这只证明求值和输入覆盖，不证明现实预测准确率。",
            },
            "export": export_info,
        })

    sample_hash = hashlib.sha256(SAMPLE.read_bytes()).hexdigest()
    product_script = PRODUCT_ROOT / "scripts/dump-facts.ts"
    product_fixture = PRODUCT_ROOT / "tests/fixtures/facts-sample.json"
    product_info = {
        "command": "bun scripts/dump-facts.ts /Users/sync/code/fateradar-classics",
        "repo": str(PRODUCT_ROOT),
        "repoHead": git_head(PRODUCT_ROOT),
        "script": str(product_script),
        "scriptSha256": hashlib.sha256(product_script.read_bytes()).hexdigest() if product_script.exists() else None,
        "productFixtureSha256": hashlib.sha256(product_fixture.read_bytes()).hexdigest() if product_fixture.exists() else None,
        "workingTreeInputs": "scripts/dump-facts.ts 和 tests/fixtures/facts-sample.json 在生成时均为未提交改动。",
    }
    return {
        "manifestVersion": "fateradar-p1-bazi-topic-handoff-v1",
        # Structural P1 rules are consumable, but the three semantic blockers
        # remain pending. A future contract must change this field explicitly;
        # the product importer refuses reserved semantic predicates otherwise.
        "semanticContractStatus": "pending",
        "generatedAt": datetime.date.today().isoformat(),
        "generatedBy": "tools/generate-p1-bazi-manifest.py",
        "art": "bazi",
        "ruleSchema": "fateradar-rules-v2",
        "predicateLanguage": "fateradar-rules-v3",
        "classicsRev": CLASSICS_REV,
        "sourceHeadAtAudit": git_head(ROOT),
        "classicsRevChanged": True,
        "factFixture": {
            "path": "tools/reports/facts-sample.json",
            "sha256": sample_hash,
            "caseCount": len(bazi_cases),
            "generator": product_info,
            "differenceFromClassicsHead": f"git diff --numstat: {diff_numstat}; 原因是按产品生成器重建事实快照，新增时间层/逐柱事实和覆盖样盘。",
        },
        "contract": {
            "pipeline": "Fact -> RuleEvaluation -> TopicEvaluation",
            "states": {"satisfied": "满足", "not_satisfied": "不满足", "unknown": "信息不足"},
            "unknownPolicy": "缺少事实、未实现时间层、性别/计数/关系合同不完整时保留 unknown；不写成 not_satisfied。",
            "verifiedPolicy": "本 manifest 的所有规则 verified=false；只有固定样盘、明确验收证据和人工出处核验完成后才可改变。",
            "layerPolicy": "各规则仅在其 applicableLayers 声明的层求值：当前 7 条本命规则仅适用于本命，YUANHAIZIPIN-YR-03 仅适用于流年。不得把本命规则复制到流年/流月/大运；未声明或缺少 scope 条件时保留 unknown。",
        },
        "topics": TOPIC_META,
        "rules": entries,
        "statusSummary": {
            "adopted": sorted(RULE_META),
            "blocked": BLOCKED,
            "rejectedRound50Drafts": ["SANMINGTONGH-051", "SANMINGTONGH-065", "SANMINGTONGH-066", "YUANHAIZIPIN-014", "WX-05-02"],
            "rejectedInvalidScope": [{"ruleId": "TAIWEIFU-004", "rejectedField": "scope.palace=伪宫名", "remainingBaseCondition": "ziwei_star=天马（旧条件保留但不进入本 P1 八字 manifest）"}],
        },
        "productFactGaps": [
            {"topic": "relationship", "gap": "性别/配偶星/夫宫与关系反馈的明确合同", "state": "部分可用", "action": "已增加 gender、spouse_star、spouse_palace_zhi 结构事实；关系反馈与古籍复合语义仍保持 unknown，未升级规则。"},
            {"topic": "all", "gap": "流年、流月、流日的逐柱干支/关系事实与层级绑定", "state": "部分可用", "action": "产品仓按时间层过滤事实；古籍仓不把本命规则复制为岁运结论。"},
            {"topic": "wealth", "gap": "财星位置、身财两停、比劫夺财与岁运触发", "state": "部分可用", "action": "已增加逐柱十神与 shishen_count，可供财星位置/计数取证；身财两停、比劫夺财与岁运触发仍阻塞。"},
            {"topic": "health", "gap": "作息、症状、体检等现实资料", "state": "产品边界", "action": "仅用于用户核对，不由古籍规则仓生成诊断。"},
            {"topic": "all", "gap": "多现/计数、跨柱同支关系", "state": "部分可用", "action": "已增加 shishen_count、natal_same_zhi、natal_relation；尚未把这些结构事实升级为古籍复合结论。"},
        ],
        "round50Audit": {
            "draftMap": "tools/reports/shensha-position-map.json",
            "draftStatus": "not_accepted",
            "fneInventory": "tools/reports/fne-residue-inventory.json",
            "scopePillarProof": {
                "result": "通过：生成器为 shensha 事实写入 scope.layer=本命 与 scope.pillar=year/month/day/time；固定样盘重建后与产品 fixture 字节一致。",
                "generator": "bun scripts/dump-facts.ts /Users/sync/code/fateradar-classics",
                "proofFile": "tools/reports/p1-bazi-20260921/shensha-scope-proof.json",
                "sampleSha256": sample_hash,
                "shenshaFactCount": shensha_fact_count,
                "semanticLimit": "柱位存在不证明神煞代理等价于建禄/专禄格局。",
            },
            "wx0502": "退回：只能写同柱禄神/驿马保守子集；跨柱同支未覆盖，且当前锚点仅卷名。",
            "ziweiPseudoPalace": {"ruleId": "TAIWEIFU-004", "result": "退回", "failureLog": "tools/reports/p1-bazi-20260921/round50-schema-before.json"},
            "ledger": {"command": "python3 tools/test-ledger-consistency.py", "result": "ALL LEDGER-CONSISTENCY OK; 464 条未映射均有 reason_class。"},
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--export-file")
    args = parser.parse_args(argv)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = make_manifest(output, Path(args.export_file) if args.export_file else None)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output} rules={len(manifest['rules'])} fixtureCases={manifest['factFixture']['caseCount']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
