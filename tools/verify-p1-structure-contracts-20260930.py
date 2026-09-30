"""Verify the 2026-09-30 delegated Bazi structure contracts.

Read-only except for REPORT. No product imports, network, chart engine, or
inferred hidden stems: tables and tri-states come from the pinned adjudication.
The content-policy regex snapshot is the sole copied product component.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "docs/closeout/P1_BAZI_STRUCTURE_CONTRACTS_20260930.json"
REPORT = ROOT / "tools/reports/p1-bazi-20260930/structure-contract-verification.json"
DOCUMENT = "docs/closeout/P1_STRUCTURE_CONTRACT_ADJUDICATION_20260930.md"
ADJUDICATION_COMMIT = "48077232269ded4da1bcee2058603b7f80f9fd79"
SOURCE_COMMIT = "672aabc0a5fcba04cb1d5fc1d712233dca03d95a"
SOURCE_TREE = "f296230d0f095eb57a5002e8394913c21f0d2025"
FIXTURE_PATH = "tools/reports/p1-bazi-20260930/structure-contract-fixture.json"
PILLARS = ("year", "month", "day", "time")
NAMES = dict(zip(PILLARS, ("年柱", "月柱", "日柱", "时柱")))
STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STATES = ("satisfied", "not_satisfied", "unknown")
# 裁决书第 10 节：逐项固定，不从合同反推允许的编号。
IDENTITY_FIELDS = ("category", "ruleId", "semanticContractId", "sourceRuleId", "relatedNonL1RuleIds", "displayOrder")
IDENTITY_TABLE = (
    ("sanhe", "SANMINGTONGH-015-L1-STRUCT", "SMTH-015-SANHE-20260930", "SANMINGTONGH-015", [], 1),
    ("ziwu", "SMTH-CHONGJI-ZIWU-L1-STRUCT", "SMTH-CHONGJI-ZIWU-20260930", None, ["DITIANSUICHA-032"], 2),
    ("maoyou", "SMTH-CHONGJI-MAOYOU-L1-STRUCT", "SMTH-CHONGJI-MAOYOU-20260930", None, ["DITIANSUICHA-031"], 3),
    ("jia_chen_wu", "ZPR-P1-01-L1-STRUCT", "ZPR-P1-01-TOUWU-20260930", "ZPR-P1-01", [], 4),
)
RULE_IDS = tuple(row[1] for row in IDENTITY_TABLE)
# 裁决书第 3–7 节：独立复算只用这张表，不执行合同给定的谓词。
TRIADS = ("申子辰", "巳酉丑", "寅午戌", "亥卯未")
STRUCTURES = {
    "sanhe": {"kind": "branch_triad_complete", "pillars": list(PILLARS), "groups": [
        {"branches": list("申子辰"), "variant": "water"},
        {"branches": list("巳酉丑"), "variant": "other", "foldElement": "金"},
        {"branches": list("寅午戌"), "variant": "other", "foldElement": "火"},
        {"branches": list("亥卯未"), "variant": "other", "foldElement": "木"}]},
    "ziwu": {"kind": "branch_pair_present", "pillars": list(PILLARS), "branches": list("子午")},
    "maoyou": {"kind": "branch_pair_present", "pillars": list(PILLARS), "branches": list("卯酉")},
    "jia_chen_wu": {"kind": "month_hidden_stem_exposed", "dayStem": "甲", "monthBranch": "辰", "hiddenStem": "戊", "exposedAt": ["year", "month", "time"]},
}
SOURCES = {k: f"sources/fulltext/bazi/{book}/fulltext.md" for k, book in (
    ("sanming", "sanming-tonghui"), ("ditiansui", "ditiansui-chanwei"), ("ziping", "ziping-zhenquan"))}
RULE_META = (
    ("bazi/sanming-tonghui", "論支元三合", "《三命通会·论支元三合》", ["015-1", "015-2", "015-3", "015-4"], 4),
    ("bazi/sanming-tonghui", "論衝擊", "《三命通会·论冲击》", ["5-1", "5-2"], 5),
    ("bazi/sanming-tonghui", "論衝擊", "《三命通会·论冲击》", ["6-1", "6-2"], 6),
    ("bazi/ziping-zhenquan", "論雜氣如何取用", "《子平真诠》论杂气一篇", ["P1-01-1", "P1-01-2"], 7),
)
# Roles cannot be promoted by editing a contract. Lines are pinned independently.
ANCHOR_TABLE = {
    "smth-sanhe-list": ("sanming", 1216, "statement"),
    "smth-sanhe-water": ("sanming", 1217, "statement"),
    "smth-sanhe-collation": ("sanming", 1218, "support"),
    "smth-sanhe-effect": ("sanming", 1218, "not_authorized"),
    "smth-chongji-heading": ("sanming", 1282, "support"),
    "smth-chongji-definition": ("sanming", 1283, "statement"),
    "smth-chongji-sha": ("sanming", 1283, "not_authorized"),
    "smth-chongji-effect": ("sanming", 1284, "not_authorized"),
    "dts-four-names": ("ditiansui", 97, "fold_other_book"),
    "dts-maoyou-name": ("ditiansui", 101, "fold_other_book"),
    "dts-ziwu-name": ("ditiansui", 102, "fold_other_book"),
    "dts-example-premise": ("ditiansui", 98, "not_authorized"),
    "dts-ziwu-effect": ("ditiansui", 99, "not_authorized"),
    "dts-maoyou-effect": ("ditiansui", 100, "not_authorized"),
    "dts-jiji-effect": ("ditiansui", 103, "not_authorized"),
    "zpr-chen-hidden": ("ziping", 542, "statement"),
    "zpr-clear-premise": ("ziping", 542, "support"),
    "zpr-jia-chen-wu": ("ziping", 544, "statement"),
    "zpr-emotion-effect": ("ziping", 548, "not_authorized"),
}

# Snapshot: /Users/sync/code/cosmic-fortune-lab/src/lib/reading/synthesis/content-policy.ts
# Copied 2026-09-30. /u needs no Python flag; /g is irrelevant to first-hit checks.
# JS /u (without /i) still uses ASCII word boundaries and ASCII digits. Do NOT
# use re.ASCII globally: that would also change \s, whose JS meaning is Unicode.
DEV_RECORD_PATTERNS = (
    ("规则编号", r"\b[A-Z]{3,}(?:-[A-Z0-9]+)+\b"),
    ("枚举值", r"\b(?:not_satisfied|satisfied|unknown|provisional|accepted_semantic_contract|product_neutral_fallback)\b"),
    ("字段名", r"\b[a-z]+(?:_[a-z]+)+\b"),
    ("版本号", r"[a-z]+-\d{8}-v\d+"),
    ("事实编号", r"\b[a-z]+:[^\s:<>]{1,6}:[^\s，。<>]{1,6}"),
    ("代码类名", r"\b(?:RuleEvaluation|FactKey|ruleId|factIds|tierLabel|topicEvaluation)\b"),
    ("F/L 代码", r"(?<![A-Za-z0-9])(?:F\d+|L[123])(?![A-Za-z0-9])"),
    ("出处行号", r"第 \d+(?:–\d+)? 行|查看原文第|\bL\d{4}\b|\[part=\d+"),
    ("文本版本", r"文本版本：|\b[0-9a-f]{40}\b"),
    ("内部说法", r"兜底|非算法判定|求值|锚点|窄入口|窄规则|例型|交接规则|已交接|待交接|未交接|入口证据|未交付|口径声明|映射到|算法判定|语义合同|结构入口|三态|规则状态|当前实现|现行实现|不得把|实现假设|本模块|电子文本|电子源|尚未影印校勘|不冒称|不伪装满足|fulltext|\.md\b"),
)
SCORE_PATTERNS = (
    ("百分比", r"\d+(?:\.\d+)?\s*%"),
    ("分值", r"(?<![\dA-Za-z])[+-]\d+(?:\.\d+)?(?![\d年月日岁])"),
    ("计分说法", r"约占|分值|计分|加权|占比|帮身力量"),
)
JARGON_PATTERNS = (
    ("吉凶字", r"偏?凶|偏吉|[·：]\s*吉(?![一-鿿])"),
    ("引擎用词", r"候选|未执行|配合未|取用|判为|当令|本气|用神|喜神|忌神|仇神|闲神|得令|得地|得势|微燥|微寒|偏燥|偏寒|寒暖调匀|透干|藏支|根浅|根微|根深|旺相|休囚|气候估计|估计"),
)
RED_LINE_PATTERNS = (
    ("绝对词", r"注定|必然|一定会|必定"),
    ("事件预言", r"(?:\d{4}年|今年|明年|后年|某年|你将|你会|将会|必会)[^。！？\n]{0,24}(?:离婚|死亡|去世|丧命|患[上有]?[^。！？\n]{0,8}(?:病|癌|症))"),
    ("疾病诊断", r"(?:你|命主|本人)[^。！？\n]{0,10}(?:患有|患上|得了|罹患|确诊|有)[^。！？\n]{0,8}(?:病|癌|症)"),
    ("百分比", r"\d+(?:\.\d+)?\s*[%％]|百分之[零一二三四五六七八九十百\d.]+"),
)
JS_BOUNDARY = r"(?:(?<![A-Za-z0-9_])(?=[A-Za-z0-9_])|(?<=[A-Za-z0-9_])(?![A-Za-z0-9_]))"
JS_SPACE = r"\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"


def js_pattern(pattern: str) -> re.Pattern:
    """Translate only the escapes used by this frozen snapshot, incl. classes."""
    pattern = pattern.replace(r"\b", JS_BOUNDARY)
    result, inside, i = [], False, 0
    while i < len(pattern):
        char = pattern[i]
        if char == "\\" and i + 1 < len(pattern):
            escape = pattern[i + 1]
            if escape in "ds":
                body = "0-9" if escape == "d" else JS_SPACE
                result.append(body if inside else "[" + body + "]")
            else:
                result.append(pattern[i:i + 2])
            i += 2
            continue
        if char == "[":
            inside = True
        elif char == "]":
            inside = False
        result.append(char)
        i += 1
    return re.compile("".join(result))


CONTENT_PATTERNS = [(name, js_pattern(pattern)) for name, pattern in
                    (*DEV_RECORD_PATTERNS, *SCORE_PATTERNS, *JARGON_PATTERNS, *RED_LINE_PATTERNS)]


def content_policy_hits(text: str) -> list[dict]:
    return [{"name": name, "match": hit[0]} for name, pattern in CONTENT_PATTERNS
            if (hit := pattern.search(text))]


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode().strip()


def fact_index(facts: list[dict]) -> dict:
    index = {(key, p): set() for p in PILLARS for key in ("gan", "zhi", "canggan")}
    for fact in facts:
        scope = fact.get("scope", {})
        key = (fact.get("key"), scope.get("pillar"))
        if scope.get("layer") == "本命" and key in index:
            index[key].add(fact["value"])
    return index


def unknown_evidence(index: dict, keys: list[tuple[str, str]]) -> dict:
    ordered = sorted(set(keys), key=lambda kp: (PILLARS.index(kp[1]), ("gan", "zhi", "canggan").index(kp[0])))
    missing, conflicts = [], []
    for key, pillar in ordered:
        values = index[key, pillar]
        if not values:
            missing.append({"key": key, "pillar": pillar})
        elif key != "canggan" and len(values) > 1:
            order = STEMS if key == "gan" else BRANCHES
            conflicts.append({"key": key, "pillar": pillar, "values": sorted(values, key=order.index)})
    affected = {item["pillar"] for item in missing + conflicts}
    return {"state": "unknown", "unknownPillars": [p for p in PILLARS if p in affected],
            **({"missingKeys": missing} if missing else {}),
            **({"conflicts": conflicts} if conflicts else {})}


def evaluate_structure(category: str, index: dict) -> dict:
    if category in ("sanhe", "ziwu", "maoyou"):
        keys = [("zhi", p) for p in PILLARS]
        diagnostic = unknown_evidence(index, keys)
        if diagnostic.get("conflicts"):
            return diagnostic
        known = {p: next(iter(index["zhi", p])) for p in PILLARS if index["zhi", p]}
        groups = TRIADS if category == "sanhe" else ("子午" if category == "ziwu" else "卯酉",)
        for group in groups:
            if set(group) <= set(known.values()):
                return {"state": "satisfied", "positions": {b: [p for p in PILLARS if known.get(p) == b] for b in group}}
        k = len(diagnostic.get("missingKeys", []))
        if any(1 <= len(group) - len(set(group) & set(known.values())) <= k for group in groups):
            return diagnostic
        return {"state": "not_satisfied"}

    # P1-01-2: premise missing/conflicts precede negative and positive results.
    keys = [("gan", p) for p in PILLARS] + [("zhi", "month"), ("canggan", "month")]
    diagnostic = unknown_evidence(index, keys)
    premises = [("gan", "day"), ("zhi", "month"), ("canggan", "month")]
    if diagnostic.get("conflicts") or any(not index[k] for k in premises):
        return diagnostic
    if index["gan", "day"] != {"甲"} or index["zhi", "month"] != {"辰"} or "戊" not in index["canggan", "month"]:
        return {"state": "not_satisfied"}
    exposed = [p for p in ("year", "month", "time") if index["gan", p] == {"戊"}]
    if exposed:
        return {"state": "satisfied", "positions": {"戊": exposed}}
    if diagnostic.get("missingKeys"):
        return diagnostic
    return {"state": "not_satisfied"}


def join_positions(positions: list[str]) -> str:
    words = [NAMES[p] for p in PILLARS if p in positions]
    if not words:
        raise ValueError("cannot render empty positions")
    return words[0] if len(words) == 1 else "、".join(words[:-1]) + "和" + words[-1]


def render(rule: dict, positions: dict) -> dict:
    copy = rule["copy"]
    substitutions = {f"pos:{char}": join_positions(ps) for char, ps in positions.items()}
    if rule["category"] == "sanhe":
        i = next(i for i, group in enumerate(TRIADS) if set(group) == set(positions))
        copy = copy["water" if i == 0 else "other"]
        for n, char in enumerate(TRIADS[i], 1):
            substitutions[f"b{n}"] = char
            substitutions[f"pos:b{n}"] = join_positions(positions[char])
        if i:
            substitutions["element"] = ("金", "火", "木")[i - 1]
    return {slot: re.sub(r"\{([^{}]+)\}", lambda m: substitutions[m[1]], template)
            for slot, template in copy.items()}


def evaluate_chart(facts: list[dict], contracts: dict) -> dict:
    """Return all four exported verdicts, plus displayed strings without label."""
    index = fact_index(facts)
    rules = {r["category"]: r for r in contracts["rules"]}
    results, display, statements, rendered = {}, [], [], {}
    for category, rid, sid, _, _, _ in IDENTITY_TABLE:
        value = evaluate_structure(category, index)
        displayed = value["state"] == "satisfied" and len(display) < 2
        row = {"ruleId": rid, "semanticContractId": sid, **value, "displayed": displayed,
               "verificationMethod": "delegated_adjudication", "sourceCommit": SOURCE_COMMIT,
               "adjudicationCommit": ADJUDICATION_COMMIT}
        if not displayed:
            row["notDisplayedReason"] = "display_cap" if value["state"] == "satisfied" else value["state"]
        if value["state"] == "satisfied":
            rendered[rid] = render(rules[category], value["positions"])
        if displayed:
            display.append(rid)
            statements.append(rendered[rid]["statement"])
        results[rid] = row
    return {"results": results, "display": display, "statements": statements, "rendered": rendered}


class VerificationError(Exception):
    def __init__(self, name, detail, checks):
        super().__init__(f"{name}: {detail}")
        self.checks = checks


def verify(contracts: dict, *, fixture_bytes: bytes | None = None) -> dict:
    """Check a JSON object without mutating it; byte override enables memory tests."""
    checks = []

    def check(name, ok, detail=None):
        checks.append({"check": name, "ok": bool(ok), **({"detail": detail} if detail is not None else {})})
        if not ok:
            raise VerificationError(name, detail, checks)

    check("schema", contracts.get("schema") == "fateradar-bazi-structure-contracts-v1")
    check("contract-version", contracts.get("contractVersion") == "p1-bazi-structure-contracts-20260930-v1")
    check("purpose", contracts.get("art") == "bazi" and contracts.get("contractPurpose") == "structure_statement")
    check("method", contracts.get("verificationMethod") == "delegated_adjudication")
    check("status", contracts.get("status") in ("pending_product_fixture", "accepted") and type(contracts.get("verified")) is bool)
    fixture_meta = contracts.get("fixture")
    check("fixture-required-for-acceptance", fixture_meta is not None or
          (contracts["status"] == "pending_product_fixture" and contracts["verified"] is False))
    check("status-verified-consistent", (contracts["status"] == "accepted") == contracts["verified"])
    components = contracts.get("verificationComponents", [])
    check("verification-components", len(components) == 4 and "双实现一致" in components[3])
    adj = contracts["adjudication"]
    check("adjudication-pin", adj["id"] == "p1-structure-adjudication-20260930" and adj["document"] == DOCUMENT and adj["commit"] == ADJUDICATION_COMMIT)
    check("adjudicator", "claude-opus-5-5" in adj["adjudicator"] and "无人工复核" in adj["adjudicator"])
    check("user-instruction", all(s in adj["userInstruction"] for s in (
        "原文解释交给你来拍板，不需要人类接入，然后你继续开发", "2026-09-30", "不再询问")))
    pinned_document = git_bytes("show", f"{ADJUDICATION_COMMIT}:{DOCUMENT}")
    check("adjudication-unchanged", (ROOT / DOCUMENT).read_bytes() == pinned_document)
    document = pinned_document.decode()
    pin = contracts["sourcePin"]
    check("source-pin:declaration", pin == {"path": "sources/fulltext", "gitTree": SOURCE_TREE,
          "remoteRef": "refs/heads/main", "remoteCommit": SOURCE_COMMIT})
    for ref in ("HEAD", SOURCE_COMMIT):
        check(f"source-pin:{ref}", git("rev-parse", f"{ref}:sources/fulltext") == SOURCE_TREE)
    check("sources", contracts["sources"] == SOURCES)
    source_lines = {}
    for name, path in SOURCES.items():
        raw = (ROOT / path).read_bytes()
        check(f"source-worktree:{name}", raw == git_bytes("show", f"{SOURCE_COMMIT}:{path}"))
        source_lines[name] = raw.decode().splitlines()
    # Detect edits to any tracked source/rules file without consulting another checkout.
    changed = git("diff", "--name-only", SOURCE_COMMIT, "--", "sources", "references").splitlines()
    check("protected-files-unchanged", not [p for p in changed if p.startswith("sources/") or p.endswith("/rules.yaml")], changed)

    anchors_list = contracts["anchors"]
    anchors = {a["id"]: a for a in anchors_list}
    check("anchor-inventory", len(anchors_list) == len(anchors) and set(anchors) == set(ANCHOR_TABLE))
    for aid, (source, line, role) in ANCHOR_TABLE.items():
        a = anchors[aid]
        if source == "sanming" and 1282 <= line <= 1284 and a["role"] == "statement":
            check(f"chongji-statement-range:{aid}", 1282 <= a["startLine"] <= a["endLine"] <= 1283)
        check(f"anchor-pin:{aid}", (a["source"], a["startLine"], a["endLine"], a["role"]) == (source, line, line, role))
        check(f"anchor-quote:{aid}", bool(a["quote"]) and a["quote"] in source_lines[source][line - 1], a["quote"])
    check("chongji-definition-only", anchors["smth-chongji-definition"]["quote"] == "地支取七位為衝猶天干取七位為煞之義如子午對衝子至午七數")

    rules = contracts["rules"]
    check("identity-count", len(rules) == 4)
    for rule, identity, meta in zip(rules, IDENTITY_TABLE, RULE_META):
        rid = identity[1]
        check(f"identity:{rid}", tuple(rule.get(f) for f in IDENTITY_FIELDS) == identity)
        check(f"structure:{rid}", rule["structure"] == STRUCTURES[rule["category"]])
        check(f"rule-meta:{rid}", (rule["book"], rule["chapter"], rule["pageCitation"], rule["rulings"]) == meta[:4])
        check(f"rule-scope:{rid}", (rule["topic"], rule["layer"], rule["contractPurpose"]) == ("overview", "本命", "structure_statement"))
        check(f"page-citation:{rid}", not content_policy_hits(rule["pageCitation"]) and not any(w in rule["pageCitation"] for w in ("取用", "透干")))
        for field, roles in (("statementAnchors", {"statement"}), ("foldAnchors", {"support", "statement", "fold_other_book"}), ("notAuthorizedAnchors", {"not_authorized"})):
            refs = rule[field]
            check(f"anchor-roles:{rid}:{field}", bool(refs) and len(set(refs)) == len(refs) and all(ref in anchors and anchors[ref]["role"] in roles for ref in refs))
        expected_source = "ziping" if rule["category"] == "jia_chen_wu" else "sanming"
        check(f"statement-single-book:{rid}", all(anchors[ref]["source"] == expected_source for ref in rule["statementAnchors"]))
        section = document.split(f"## {meta[4]}.", 1)[1].split(f"## {meta[4] + 1}.", 1)[0].split("### 显示句", 1)[1]
        copies = rule["copy"].values() if rule["category"] == "sanhe" else [rule["copy"]]
        for copy in copies:
            check(f"copy-slots:{rid}", set(copy) == {"statement", "fold"})
            for slot, template in copy.items():
                check(f"content-template:{rid}:{slot}", not content_policy_hits(template), content_policy_hits(template))
                original = re.sub(r"\{pos:[^{}]+\}", "{柱}", template)
                for token, value in (("b1", "巳"), ("b2", "酉"), ("b3", "丑"), ("element", "金")):
                    original = original.replace("{" + token + "}", value)
                check(f"copy-adjudication:{rid}:{slot}", f"「{original}」" in section)

    # Entire YAML bytes (stronger than only applicable_to / verified) must match
    # the baseline; IDs are then checked in their actual book, not the L1 book.
    for book, ids in (
        ("sanming-tonghui", ["SANMINGTONGH-015"]),
        ("ditiansui-chanwei", ["DITIANSUICHA-032", "DITIANSUICHA-031"]),
        ("ziping-zhenquan", ["ZPR-P1-01"]),
    ):
        path = f"references/books/bazi/{book}/rules.yaml"
        raw = (ROOT / path).read_bytes()
        base = git_bytes("show", f"{SOURCE_COMMIT}:{path}")
        check(f"rules-yaml-unchanged:{book}", raw == base)
        current = {r["rule_id"]: r for r in yaml.safe_load(raw)["rules"]}
        baseline = {r["rule_id"]: r for r in yaml.safe_load(base)["rules"]}
        for rid in ids:
            check(f"source-rule-exists:{rid}", rid in current and rid in baseline)
            for field in ("applicable_to", "verified"):
                check(f"source-rule-field:{rid}:{field}", field in current[rid] and current[rid][field] == baseline[rid][field])

    display = contracts["displayPolicy"]
    for key, value in {"placement": "overview_natal_after_reasons_before_advice", "countsAsReason": False,
                       "label": "古籍依据：", "maxStatements": 2, "order": [i[0] for i in IDENTITY_TABLE],
                       "onePerCategory": True, "onlyState": "satisfied", "notDisplayedReason": "display_cap",
                       "positionOrder": list(PILLARS), "positionNames": NAMES}.items():
        check(f"display-policy:{key}", display.get(key) == value)
    vocab = contracts["factVocabulary"]
    check("fact-vocabulary", vocab["pillars"] == list(PILLARS) and
          {k: v["cardinality"] for k, v in vocab["keys"].items()} == {"gan": "single", "zhi": "single", "canggan": "multiple"})
    check("tri-state-vocabulary", contracts["triState"]["states"] == list(STATES))
    check("export-policy", contracts["exportPolicy"]["everyRuleEveryChart"] is True and
          set(contracts["exportPolicy"]["fields"]) == {"ruleId", "semanticContractId", "state", "positions", "unknownPillars", "missingKeys", "conflicts", "displayed", "notDisplayedReason", "verificationMethod", "sourceCommit", "adjudicationCommit"})
    check("excluded", [(x["ruleId"], x["ruling"]) for x in contracts["excluded"]] == [("ZPR-P1-03", "not_l1_eligible")])
    check("deferred", [(x["ruleId"], x["ruling"]) for x in contracts["deferred"]] == [("ZPR-P1-04", "deferred"), ("ZPR-P1-06", "deferred")])
    check("fixture-format", contracts["fixtureFormat"]["path"] == FIXTURE_PATH)

    def validate_facts(facts, context):
        check(f"facts-list:{context}", isinstance(facts, list))
        for i, f in enumerate(facts):
            check(f"fact-shape:{context}:{i}", isinstance(f, dict) and isinstance(f.get("scope"), dict) and isinstance(f.get("key"), str) and "value" in f)
            if f["key"] not in ("gan", "zhi", "canggan") or f["scope"].get("layer") != "本命":
                continue
            check(f"fact-domain:{context}:{i}", f["scope"].get("pillar") in PILLARS and
                  isinstance(f["value"], str) and len(f["value"]) == 1 and
                  f["value"] in (BRANCHES if f["key"] == "zhi" else STEMS))

    def gate_rendered(got, context):
        for rid, copies in got["rendered"].items():
            for slot, text in copies.items():
                check(f"content-rendered:{context}:{rid}:{slot}", not content_policy_hits(text), content_policy_hits(text))
                check(f"render-resolved:{context}:{rid}:{slot}", "{" not in text and "}" not in text)

    synthetic = contracts["syntheticCases"]
    check("synthetic-case-ids", bool(synthetic) and len({s["id"] for s in synthetic}) == len(synthetic))
    synthetic_results = {}
    for case in synthetic:
        cid = case["id"]
        validate_facts(case["facts"], cid)
        got = evaluate_chart(case["facts"], contracts)
        check(f"synthetic-states:{cid}", {rid: r["state"] for rid, r in got["results"].items()} == case["expected"], case["expected"])
        check(f"synthetic-display:{cid}", got["display"] == case["expectedDisplay"])
        check(f"synthetic-positions:{cid}", {rid: r["positions"] for rid, r in got["results"].items() if "positions" in r} == case["expectedPositions"])
        check(f"synthetic-statements:{cid}", got["statements"] == case["expectedStatements"])
        gate_rendered(got, cid)
        synthetic_results[cid] = got
    for rule in rules:
        rid = rule["ruleId"]
        check(f"rule-fixture-states:{rid}", set(rule["fixtures"]) == set(STATES))
        for state in STATES:
            expected_ids = [case["id"] for case in synthetic if case["expected"][rid] == state]
            check(f"rule-fixtures:{rid}:{state}", bool(expected_ids) and rule["fixtures"][state] == expected_ids)

    cohorts, coverage, product_rows = {}, {}, 0
    fixture_sha, product_fixture = None, "pending"
    if fixture_meta is not None:
        check("fixture-path", fixture_meta.get("path") == FIXTURE_PATH)
        raw = fixture_bytes if fixture_bytes is not None else (ROOT / FIXTURE_PATH).read_bytes()
        fixture_sha = hashlib.sha256(raw).hexdigest()
        check("fixture-sha256", fixture_meta.get("sha256") == fixture_sha)
        fixture = json.loads(raw)
        rows = fixture["rows"]
        check("fixture-rows", isinstance(rows, list) and bool(rows))
        seen, all_charts, covered_charts = set(), set(), set()
        cohort_charts, cohort_covered = {}, {}
        core = {"state", "positions", "unknownPillars", "missingKeys", "conflicts", "displayed", "notDisplayedReason"}
        metadata = {"ruleId", "semanticContractId", "verificationMethod", "sourceCommit", "adjudicationCommit"}
        for row in rows:
            cid, cohort = row["id"], row["cohort"]
            check("fixture-row-identity", isinstance(cid, str) and bool(cid) and cohort in ("coverage388", "named", "time_removed"))
            check(f"fixture-unique-row:{cohort}:{cid}", (cohort, cid) not in seen)
            seen.add((cohort, cid))
            all_charts.add(cid)
            cohort_charts.setdefault(cohort, set()).add(cid)
            cohort_covered.setdefault(cohort, set())
            validate_facts(row["facts"], f"product:{cohort}:{cid}")
            got = evaluate_chart(row["facts"], contracts)
            check(f"product-rules:{cid}", set(row["product"]) == set(RULE_IDS))
            for rid, value in got["results"].items():
                actual = row["product"][rid]
                check(f"product-fields:{cid}:{rid}", isinstance(actual, dict) and set(actual) <= core | metadata)
                check(f"product-verdict:{cid}:{rid}", {k: v for k, v in value.items() if k in core} == {k: v for k, v in actual.items() if k in core}, {"python": value, "product": actual} if {k: v for k, v in value.items() if k in core} != {k: v for k, v in actual.items() if k in core} else None)
                check(f"product-displayed-boolean:{cid}:{rid}", type(actual.get("displayed")) is bool)
                check(f"product-provenance:{cid}:{rid}", all(actual[k] == value[k] for k in metadata if k in actual))
            check(f"product-display:{cid}", row["productDisplay"] == got["display"])
            if "productStatements" in row:
                check(f"product-statements:{cid}", row["productStatements"] == got["statements"])
            gate_rendered(got, f"product:{cid}")
            stats = cohorts.setdefault(cohort, {"rows": 0, "uniqueCharts": 0, "atLeastOneStatementCharts": 0,
                "satisfiedStatements": 0, "displayedStatements": 0, "rowsWithProductStatements": 0,
                "ruleStates": {rid: dict.fromkeys(STATES, 0) for rid in RULE_IDS}})
            stats["rows"] += 1
            stats["rowsWithProductStatements"] += int("productStatements" in row)
            stats["displayedStatements"] += len(got["display"])
            for rid, value in got["results"].items():
                stats["ruleStates"][rid][value["state"]] += 1
                stats["satisfiedStatements"] += int(value["state"] == "satisfied")
            if got["display"]:
                cohort_covered[cohort].add(cid)
                covered_charts.add(cid)
        for cohort, stats in cohorts.items():
            stats["uniqueCharts"] = len(cohort_charts[cohort])
            stats["atLeastOneStatementCharts"] = len(cohort_covered[cohort])
        coverage = {"uniqueCharts": len(all_charts), "atLeastOneStatementCharts": len(covered_charts),
                    "deduplicationKey": "id"}
        product_rows, product_fixture = len(rows), "verified"

    return {"result": "PASS", "contractVersion": contracts["contractVersion"], "status": contracts["status"],
            "verified": contracts["verified"], "verificationMethod": contracts["verificationMethod"],
            "sourceCommit": SOURCE_COMMIT, "sourceTree": SOURCE_TREE, "adjudicationCommit": ADJUDICATION_COMMIT,
            "productFixture": product_fixture, "fixtureSha256": fixture_sha, "productRows": product_rows,
            "cohorts": cohorts, "coverage": coverage, "syntheticCases": len(synthetic), "anchors": len(anchors),
            "checks": len(checks), "syntheticResults": synthetic_results,
            "limitations": ["Python 只复算输入 facts，不重排出生时间；合成样盘不等于产品端到端验收。",
                            "productStatements 为可选字段；仅在提供时逐字比对，报告列明提供行数。"]}


def dry_run_fixture(path: Path) -> dict:
    """Pre-acceptance check of a product fixture against the pending contract.

    The declared fixture path and digest are filled in memory only, so the
    product side can compare its fixture before the orchestrator commits it
    here. Nothing is written; the committed contract and report stay as is.
    """
    raw = path.read_bytes()
    trial = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    trial["fixture"] = {**(trial.get("fixture") or {}), "path": FIXTURE_PATH,
                        "sha256": hashlib.sha256(raw).hexdigest()}
    return verify(trial, fixture_bytes=raw)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixture", type=Path,
                        help="dry run: check an external product fixture; writes no report")
    args = parser.parse_args(argv)
    errors = (VerificationError, OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.CalledProcessError)
    if args.fixture is not None:
        try:
            report = dry_run_fixture(args.fixture)
        except errors as exc:
            print(f"FAIL: {exc}", file=sys.stderr)
            if isinstance(exc, VerificationError):
                print(json.dumps(exc.checks[-1], ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        print(json.dumps({k: report[k] for k in ("result", "productRows", "cohorts", "coverage", "checks")},
                         ensure_ascii=False, indent=2))
        return 0
    try:
        report = verify(json.loads(CONTRACTS.read_text(encoding="utf-8")))
    except errors as exc:
        report = {"result": "FAIL", "error": str(exc)}
        if isinstance(exc, VerificationError):
            report["checks"] = len(exc.checks)
            report["failedCheck"] = exc.checks[-1]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["result"] == "FAIL":
        print(f"FAIL: {report['error']}", file=sys.stderr)
        return 1
    print(f"PASS: {report['checks']} checks, {report['syntheticCases']} synthetic cases, productFixture={report['productFixture']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
