"""Candidate schema and gate for a cited DITIANSUICHA-051 favorite-element record.

This module validates author-entered adjudication records. It does not derive
yongshen, 喜神, strength, or effects from chart facts. Passing its structural
checks is necessary for a record, but is not evidence that the human reading
is correct or that DITIANSUICHA-051 itself is complete.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FULLTEXT = "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md"
COLLATION = "sources/normalized/bazi/ditiansui-chanwei/collation-notes.md"
CONTRACT_ID = "DITIANSUICHA-051-favorite-record-candidate-v1"

ELEMENTS = frozenset("木火土金水")
DISPOSITIONS = frozenset({"喜神", "忌神", "仇神", "闲神", "信息不足"})
RECORD_STATUSES = frozenset({"candidate", "adjudicated", "information_insufficient"})
REVIEW_STATES = frozenset({"applies", "not_applicable", "unresolved"})

# These identifiers are editorial review obligations grounded in this edition.
# They are not an ordered algorithm or a priority ranking.
REQUIRED_ROUTE_REVIEWS = {
    "month_command_and_revealed_use": ((2663, 2663),),
    "suppress_support_or_follow": ((2941, 2967),),
    "extreme_following": ((2942, 2947),),
    "root_and_strength": ((3203, 3221),),
    "favorite_and_hidden_use_branches": ((7313, 7319),),
    "favorite_avoidance_enemy_idle_roles": ((8979, 8999), (7369, 7375)),
    "selected_year_reselection": ((2967, 2967), (13402, 13405)),
}

FAVORITE_VERDICTS = frozenset({"明确喜行", "明确非喜行", "信息不足"})


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _in_domain(value: Any, domain: frozenset[str]) -> bool:
    return isinstance(value, str) and value in domain


def _anchors(record: Any, source_root: Path = ROOT) -> tuple[list[str], list[dict[str, Any]]]:
    """Return structural/source-text issues and normalized valid anchors."""
    issues: list[str] = []
    valid: list[dict[str, Any]] = []
    if not isinstance(record, list) or not record:
        return ["sourceAnchors must be a non-empty array"], valid

    for index, anchor in enumerate(record):
        prefix = f"sourceAnchors[{index}]"
        if not isinstance(anchor, dict):
            issues.append(f"{prefix} must be an object")
            continue
        file = anchor.get("file")
        line = anchor.get("line")
        cue = anchor.get("cue")
        source_role = anchor.get("sourceRole")
        if not isinstance(file, str) or file not in {FULLTEXT, COLLATION}:
            issues.append(f"{prefix}.file is not an allowed source in this candidate contract")
            continue
        if not _is_int(line) or line < 1:
            issues.append(f"{prefix}.line must be a positive integer")
            continue
        if not isinstance(cue, str) or not cue.strip():
            issues.append(f"{prefix}.cue must quote a non-empty source cue")
            continue
        if not isinstance(source_role, str) or source_role not in {"原注", "任氏曰", "正文", "原书案例", "影印校勘"}:
            issues.append(f"{prefix}.sourceRole must identify the commentary/source layer")
            continue

        source_path = source_root / file
        if not source_path.is_file():
            issues.append(f"{prefix}.file does not exist")
            continue
        lines = source_path.read_text(encoding="utf-8").splitlines()
        if line > len(lines) or cue not in lines[line - 1]:
            issues.append(f"{prefix}.cue does not occur at the cited line")
            continue
        valid.append({"file": file, "line": line, "cue": cue, "sourceRole": source_role})
    return issues, valid


def _anchor_in_route(anchor: dict[str, Any], route_id: str) -> bool:
    if anchor["file"] != FULLTEXT:
        return False
    return any(start <= anchor["line"] <= end for start, end in REQUIRED_ROUTE_REVIEWS[route_id])


def _valid_scope(scope: Any) -> bool:
    if not isinstance(scope, dict):
        return False
    if scope == {"layer": "本命"}:
        return True
    return (
        set(scope) == {"layer", "year"}
        and scope.get("layer") == "流年"
        and _is_int(scope.get("year"))
        and 1 <= scope["year"] <= 9999
    )


def validate_candidate_record(record: Any, *, source_root: Path = ROOT) -> dict[str, Any]:
    """Validate record shape, citations, route reviews, and year scoping.

    The returned ``structurallyAdjudicated`` flag means only that required
    fields and cited locations are present. Human source review remains needed.
    """
    errors: list[str] = []
    blockers: list[str] = []
    if not isinstance(record, dict):
        return {"valid": False, "structurallyAdjudicated": False,
                "errors": ["record must be an object"], "blockers": ["record_not_object"]}

    if record.get("contractId") != CONTRACT_ID:
        errors.append("contractId does not match this candidate contract")
    if not isinstance(record.get("recordId"), str) or not record["recordId"].strip():
        errors.append("recordId must be non-empty")
    if not isinstance(record.get("chartRef"), str) or not record["chartRef"].strip():
        errors.append("chartRef must identify the chart")
    if not _in_domain(record.get("recordStatus"), RECORD_STATUSES):
        errors.append("recordStatus must be candidate/adjudicated/information_insufficient")

    scope = record.get("scope")
    if not _valid_scope(scope):
        errors.append("scope must be exactly 本命 or 流年 with a selected integer year")
        scope = None

    element = record.get("element")
    if not _in_domain(element, ELEMENTS):
        errors.append("element must be one of 木火土金水")

    decision = record.get("decision")
    if not isinstance(decision, dict):
        errors.append("decision must be an object")
        decision = {}
    if not _in_domain(decision.get("disposition"), DISPOSITIONS):
        errors.append("decision.disposition must use the four source roles or 信息不足")
    if not _in_domain(decision.get("status"), RECORD_STATUSES):
        errors.append("decision.status must be candidate/adjudicated/information_insufficient")

    anchor_issues, valid_anchors = _anchors(record.get("sourceAnchors"), source_root)
    errors.extend(anchor_issues)
    anchors_by_line: dict[int, list[dict[str, Any]]] = {}
    for anchor in valid_anchors:
        anchors_by_line.setdefault(anchor["line"], []).append(anchor)

    route_reviews = record.get("routeReviews")
    if not isinstance(route_reviews, dict):
        errors.append("routeReviews must be an object")
        route_reviews = {}
    missing_routes = set(REQUIRED_ROUTE_REVIEWS) - set(route_reviews)
    extra_routes = set(route_reviews) - set(REQUIRED_ROUTE_REVIEWS)
    if missing_routes:
        blockers.append("route_reviews_missing:" + ",".join(sorted(missing_routes)))
    if extra_routes:
        errors.append("routeReviews has unsupported route IDs: " + ",".join(sorted(extra_routes)))
    unresolved_routes: list[str] = []
    for route_id in sorted(set(route_reviews) & set(REQUIRED_ROUTE_REVIEWS)):
        review = route_reviews[route_id]
        if not isinstance(review, dict):
            errors.append(f"routeReviews.{route_id} must be an object")
            continue
        state = review.get("state")
        if not _in_domain(state, REVIEW_STATES):
            errors.append(f"routeReviews.{route_id}.state is invalid")
            continue
        if state == "unresolved":
            unresolved_routes.append(route_id)
            blockers.append("route_unresolved:" + route_id)
        cited = review.get("sourceLines")
        if not isinstance(cited, list) or not cited or any(not _is_int(x) for x in cited):
            errors.append(f"routeReviews.{route_id}.sourceLines must list cited source lines")
            continue
        route_lines = {a["line"] for a in valid_anchors if _anchor_in_route(a, route_id)}
        if not set(cited) <= route_lines:
            errors.append(f"routeReviews.{route_id} cites lines without matching verified sourceAnchors")
        if not any(start <= line <= end for line in cited
                   for start, end in REQUIRED_ROUTE_REVIEWS[route_id]):
            errors.append(f"routeReviews.{route_id} cites outside its source range")
        if not isinstance(review.get("reason"), str) or not review["reason"].strip():
            errors.append(f"routeReviews.{route_id}.reason must explain applicability")
        if state != "unresolved" and not isinstance(review.get("evidenceRefs"), list):
            errors.append(f"routeReviews.{route_id}.evidenceRefs must be an array")
        if state != "unresolved" and not review.get("evidenceRefs"):
            blockers.append("route_evidence_missing:" + route_id)

    conflict = record.get("routeConflict")
    if not isinstance(conflict, dict):
        errors.append("routeConflict must be an object")
        conflict = {}
    conflict_state = conflict.get("status")
    if not isinstance(conflict_state, str) or conflict_state not in {"none", "resolved", "unresolved"}:
        errors.append("routeConflict.status must be none/resolved/unresolved")
    elif conflict_state == "unresolved":
        blockers.append("route_conflict_unresolved")
        if not isinstance(conflict.get("reason"), str) or not conflict["reason"].strip():
            errors.append("unresolved route conflict needs a reason")
        competing = conflict.get("competingRouteIds")
        if not isinstance(competing, list) or not competing:
            errors.append("unresolved route conflict must list the competing route IDs")
        elif any(not isinstance(route_id, str) or route_id not in REQUIRED_ROUTE_REVIEWS for route_id in competing):
            errors.append("routeConflict.competingRouteIds contains an unsupported route ID")
    elif not isinstance(conflict.get("reason"), str) or not conflict["reason"].strip():
        errors.append("resolved/no-conflict route decision needs a reason")
    elif conflict_state == "resolved" and not _in_domain(conflict.get("resolution"), frozenset({
        "applicability_exclusion", "convergent_routes", "source_priority", "case_specific_adjudication"
    })):
        errors.append("resolved route conflict needs a recognized resolution method")
    elif conflict_state == "none" and conflict.get("resolution") is not None and conflict.get("resolution") != "no_competing_applicable_route":
        errors.append("no-conflict record cannot claim a priority or conflict resolution")
    if isinstance(conflict_state, str) and conflict_state in {"none", "resolved"}:
        conflict_issues, conflict_anchors = _anchors(conflict.get("sourceAnchors"), source_root)
        errors.extend("routeConflict." + issue for issue in conflict_issues)
        if not conflict_anchors:
            blockers.append("route_conflict_reason_uncited")

    year_review = record.get("yearReview")
    if scope == {"layer": "本命"}:
        if year_review != {"status": "not_applicable"}:
            errors.append("natal record must mark yearReview not_applicable")
    elif isinstance(scope, dict) and scope.get("layer") == "流年":
        if not isinstance(year_review, dict):
            errors.append("selected-year record needs yearReview")
        else:
            year_state = year_review.get("status")
            if not isinstance(year_state, str) or year_state not in {"reassessed", "inherited_after_review", "unresolved"}:
                errors.append("yearReview.status is invalid")
            elif year_state == "unresolved":
                blockers.append("selected_year_review_unresolved")
            if year_review.get("selectedYear") != scope["year"]:
                errors.append("yearReview.selectedYear must match scope.year")
            if not isinstance(year_review.get("natalBaselineRef"), str) or not year_review["natalBaselineRef"].strip():
                errors.append("selected-year review needs natalBaselineRef")
            if isinstance(year_state, str) and year_state in {"reassessed", "inherited_after_review"}:
                if not isinstance(year_review.get("evidenceRefs"), list) or not year_review["evidenceRefs"]:
                    blockers.append("selected_year_evidence_missing")
                year_anchor_issues, year_anchors = _anchors(year_review.get("sourceAnchors"), source_root)
                errors.extend("yearReview." + issue for issue in year_anchor_issues)
                if not any(anchor["line"] in {2967, 13402, 13403, 13404, 13405}
                           for anchor in year_anchors):
                    blockers.append("selected_year_source_anchor_missing")

    if record.get("recordStatus") == "adjudicated":
        if decision.get("status") != "adjudicated":
            blockers.append("decision_not_adjudicated")
        if decision.get("disposition") == "信息不足":
            blockers.append("adjudicated_disposition_unknown")
        if unresolved_routes:
            blockers.append("adjudicated_record_has_unresolved_route")
        if conflict_state == "unresolved":
            blockers.append("adjudicated_record_has_unresolved_conflict")
        decision_issues, decision_anchors = _anchors(decision.get("sourceAnchors"), source_root)
        errors.extend("decision." + issue for issue in decision_issues)
        if not decision_anchors:
            blockers.append("decision_source_anchor_missing")
        for upstream in ("useSelection", "strengthReview", "rootReview", "followRouteReview", "yuanShenDepthReview"):
            review = record.get(upstream)
            if not isinstance(review, dict) or not isinstance(review.get("status"), str) or review.get("status") not in {"resolved", "not_applicable"}:
                blockers.append("upstream_review_incomplete:" + upstream)
            elif not review.get("evidenceRefs"):
                blockers.append("upstream_review_evidence_missing:" + upstream)
        if record.get("unresolvedItems"):
            blockers.append("unresolved_items_present")
    elif record.get("recordStatus") == "information_insufficient" and decision.get("disposition") != "信息不足":
        blockers.append("information_insufficient_record_has_non_unknown_disposition")

    unresolved_items = record.get("unresolvedItems")
    if not isinstance(unresolved_items, list) or any(not isinstance(x, str) or not x.strip() for x in unresolved_items):
        errors.append("unresolvedItems must be an array of non-empty strings")
    elif record.get("recordStatus") != "adjudicated" and not unresolved_items:
        blockers.append("unresolved_items_not_recorded")

    valid = not errors
    structurally_adjudicated = valid and record.get("recordStatus") == "adjudicated" and not blockers
    return {
        "valid": valid,
        "structurallyAdjudicated": structurally_adjudicated,
        "errors": sorted(set(errors)),
        "blockers": sorted(set(blockers)),
        "scope": scope,
    }


def favorite_element_verdict(
    record: Any,
    selected_year: int,
    element: str,
    *,
    source_root: Path = ROOT,
) -> dict[str, str]:
    """Return only a favorite-classification verdict, never a 051 effect."""
    unknown = {"favoriteElementVerdict": "信息不足", "effectVerdict": "信息不足"}
    if not _is_int(selected_year) or selected_year < 1 or selected_year > 9999 or not _in_domain(element, ELEMENTS):
        return unknown
    validation = validate_candidate_record(record, source_root=source_root)
    if (
        not validation["structurallyAdjudicated"]
        or validation.get("scope") != {"layer": "流年", "year": selected_year}
        or record.get("element") != element
    ):
        return unknown
    disposition = record["decision"]["disposition"]
    if disposition == "喜神":
        return {"favoriteElementVerdict": "明确喜行", "effectVerdict": "信息不足"}
    if disposition in {"忌神", "仇神", "闲神"}:
        return {"favoriteElementVerdict": "明确非喜行", "effectVerdict": "信息不足"}
    return unknown
