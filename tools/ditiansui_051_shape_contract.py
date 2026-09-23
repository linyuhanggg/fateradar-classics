"""Conditional source-example matcher for DITIANSUICHA-051.

This evaluates *membership in the 37 cited examples*, not luck, strength,
effective yongshen, or the complete doctrine. An upstream decision about the
favored luck element is mandatory and remains unavailable in the shared facts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "tools/reports/p1-bazi-20260922/ditiansui-051-shape-examples.json"
SHAPES = {"gaitou", "jiejiao"}
ELEMENTS = set("木火土金水")
GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")
GAN_ORDER = "甲乙丙丁戊己庚辛壬癸"
ZHI_ORDER = "子丑寅卯辰巳午未申酉戌亥"


def _is_ganzhi(pillar: Any) -> bool:
    return (
        isinstance(pillar, str)
        and len(pillar) == 2
        and pillar[0] in GAN
        and pillar[1] in ZHI
        and GAN_ORDER.index(pillar[0]) % 2 == ZHI_ORDER.index(pillar[1]) % 2
    )


def _result(verdict: str, reason: str, year: int, shape: str, *,
            pillar: str | None = None, element: str | None = None,
            source_line: int | None = None, evidence_mode: str | None = None) -> dict[str, Any]:
    return {
        "contractId": "DITIANSUICHA-051-listed-shape-v1",
        "verdict": verdict,
        "reason": reason,
        "scope": {"layer": "大运", "year": year, "shape": shape},
        "luckPillar": pillar,
        "favoriteElement": element,
        "sourceLine": source_line,
        "evidenceMode": evidence_mode,
        "effectVerdict": "信息不足",
    }


def evaluate_shape(
    facts: list[dict[str, Any]], year: int, shape: str,
    favorite_decision: dict[str, Any] | None,
) -> dict[str, Any]:
    """Evaluate one shape at one selected year's effective luck pillar.

    ``不满足`` means only that the fully specified element/pillar pair is not
    enumerated for *this shape*. It is never a negative effect judgment.
    """
    if shape not in SHAPES or not isinstance(year, int) or isinstance(year, bool):
        raise ValueError("shape must be gaitou/jiejiao and year an integer")

    pillars = [
        fact.get("value") for fact in facts
        if fact.get("key") == "dayun_gan_zhi"
        and fact.get("scope") == {"layer": "大运", "year": year}
    ]
    if not pillars or any(not _is_ganzhi(p) for p in pillars) or len(set(pillars)) != 1:
        return _result("信息不足", "selected_year_luck_pillar_missing_or_conflicting", year, shape)
    pillar = next(iter(pillars))

    if not isinstance(favorite_decision, dict) or favorite_decision.get("status") != "adjudicated":
        return _result("信息不足", "favorite_luck_element_not_adjudicated", year, shape, pillar=pillar)
    element = favorite_decision.get("favoriteElement")
    mode = favorite_decision.get("evidenceMode")
    if (
        not isinstance(element, str) or element not in ELEMENTS
        or favorite_decision.get("scope") != {"layer": "大运", "year": year}
        or mode not in {"source_adjudicated", "counterfactual"}
        or not favorite_decision.get("sourceRef")
        or not favorite_decision.get("route")
    ):
        return _result("信息不足", "favorite_luck_element_decision_invalid_or_wrong_scope", year, shape, pillar=pillar)

    rows = json.loads(TABLE.read_text())["rows"]
    matches = [row for row in rows if row["favoriteElement"] == element
               and row["luckPillar"] == pillar and row["shape"] == shape]
    if len(matches) > 1:
        raise ValueError("duplicate source-example rows")
    if matches:
        return _result("满足", "listed_source_example", year, shape, pillar=pillar,
                       element=element, source_line=matches[0]["sourceLine"], evidence_mode=mode)
    return _result("不满足", "pair_not_listed_for_shape", year, shape, pillar=pillar,
                   element=element, evidence_mode=mode)
