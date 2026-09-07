#!/usr/bin/env python3
"""Export the reviewed Qiongtong month profiles; no second hand-maintained use-god table."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEMS = "甲乙丙丁戊己庚辛壬癸"
MONTHS = "寅卯辰巳午未申酉戌亥子丑"
PACK = "references/executable/qiongtong-baojian.json"
TEXT = "sources/fulltext/bazi/qiongtong-baojian/fulltext.md"


def validate_priority(priority: list, where: str) -> None:
    if not isinstance(priority, list) or any(not isinstance(group, list) or not group for group in priority):
        raise ValueError(f"{where}: priority 必须是有序的非空组数组（未知时整个数组可空）")
    flat = [gan for group in priority for gan in group]
    if any(gan not in STEMS for gan in flat) or len(flat) != len(set(flat)):
        raise ValueError(f"{where}: priority 有非法或重复天干")


def validate_condition(condition: dict, where: str) -> None:
    kind = condition.get("kind")
    if not isinstance(condition.get("label"), str) or not condition["label"].strip():
        raise ValueError(f"{where}: 条件缺 label")
    if kind in {"visible", "hidden", "absent"}:
        if condition.get("gan") not in STEMS:
            raise ValueError(f"{where}: 条件天干无效")
        if "excludeDay" in condition and type(condition["excludeDay"]) is not bool:
            raise ValueError(f"{where}: excludeDay 必须是布尔值")
        if kind == "visible" and "pillars" in condition and (
            not isinstance(condition["pillars"], list) or not condition["pillars"]
            or any(type(index) is not int or index not in range(4) for index in condition["pillars"])
        ):
            raise ValueError(f"{where}: 条件柱位无效")
        if kind == "absent" and condition.get("scope") not in {"visible", "all"}:
            raise ValueError(f"{where}: absent scope 无效")
    elif kind == "no-combine":
        if "".join(condition.get("pair", [])) not in {"甲己", "己甲", "乙庚", "庚乙", "丙辛", "辛丙", "丁壬", "壬丁", "戊癸", "癸戊"}:
            raise ValueError(f"{where}: 不是当前支持的五合对")
    elif kind == "term-phase":
        if condition.get("term") not in {"谷雨", "夏至", "秋分", "冬至"} or condition.get("phase") not in {"before", "after"}:
            raise ValueError(f"{where}: 精确中气条件无效")
    elif kind != "unknown" and kind != "branches":
        raise ValueError(f"{where}: 未实现的条件类型 {kind}")
    if kind == "branches" or (kind == "hidden" and "branches" in condition):
        branches = condition.get("branches")
        if not isinstance(branches, list) or not branches or any(z not in MONTHS for z in branches):
            raise ValueError(f"{where}: 条件地支无效")


def build_export(root: Path, revision: str) -> dict:
    payload = json.loads((root / PACK).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "fateradar-executable-v2" or payload.get("verified") is not False:
        raise ValueError("需要未经自动提升 verified 的 executable-v2 源数据")
    book = payload["book"]
    if book.get("slug") != "qiongtong-baojian" or book.get("fulltext") != TEXT:
        raise ValueError("调候导出只消费当前穷通底本")
    paragraphs = json.loads((root / "references/inventory/paragraphs/bazi/qiongtong-baojian.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in paragraphs["paragraphs"]}
    lines = (root / TEXT).read_text(encoding="utf-8").splitlines()
    profiles = []
    spans = {}
    seen = set()
    seen_ids = set()
    for rule in payload["rules"]:
        rid = rule["id"]
        config = rule.get("tiaohou")
        if not config:
            raise ValueError(f"{rid}: 缺少可消费的 tiaohou 配置")
        day, month = config["dayGan"], config["monthZhi"]
        if day not in STEMS or month not in MONTHS or (day, month) in seen or rid in seen_ids:
            raise ValueError(f"{rid}: 日干月令非法或重复")
        seen.add((day, month)); seen_ids.add(rid)
        if config["scope"] not in {"month", "season", "conditional", "unresolved"}:
            raise ValueError(f"{rid}: 来源范围无效")
        validate_priority(config["priority"], rid)
        if not isinstance(config.get("note"), str) or not config["note"].strip():
            raise ValueError(f"{rid}: 来源说明不能为空")
        rule_spans = []
        for source in rule["sources"]:
            pid = source["paragraph_id"]
            paragraph = by_id.get(pid)
            start, end = source["start_line"], source["end_line"]
            if not paragraph or not (type(start) is int and type(end) is int and 1 <= start <= end <= len(lines)):
                raise ValueError(f"{rid}: 来源 ID 或行范围错误")
            if not paragraph["start_line"] <= start <= end <= paragraph["end_line"]:
                raise ValueError(f"{rid}: 来源范围超出段落")
            if source["quote"] != "\n".join(lines[start - 1:end]):
                raise ValueError(f"{rid}: 原文 quote 不一致")
            sid = f"{pid}@{start}-{end}"
            spans[sid] = {"paragraphId": pid, "chapter": paragraph["heading"], "startLine": start,
                          "endLine": end, "quote": source["quote"]}
            rule_spans.append(sid)

        def resolve_sources(ids: list[str]) -> list[str]:
            if not ids or any(pid not in [spans[sid]["paragraphId"] for sid in rule_spans] for pid in ids):
                raise ValueError(f"{rid}: profile/check 引用了未声明的来源段落")
            return list(dict.fromkeys(sid for pid in ids for sid in rule_spans if spans[sid]["paragraphId"] == pid))

        checks = []
        check_ids = set()
        for check in config["checks"]:
            if check["id"] in check_ids:
                raise ValueError(f"{rid}: 重复条件 ID")
            check_ids.add(check["id"])
            if check["effect"] not in {"none", "replace", "add"} or check["role"] not in {"base", "alternative", "support"}:
                raise ValueError(f"{rid}: 条件效应或角色无效")
            if not check["conditions"]:
                raise ValueError(f"{rid}: source check 不能用空条件冒充已匹配")
            validate_priority(check["priority"], check["id"])
            for condition in check["conditions"]:
                validate_condition(condition, check["id"])
            checks.append({key: check[key] for key in ("id", "label", "role", "effect", "priority", "conditions", "explanation")}
                          | {"sourceIds": resolve_sources(check["sourceParagraphIds"])})
        profiles.append({"id": rid, **{key: config[key] for key in ("dayGan", "monthZhi", "scope", "priority", "note")},
                         "sourceIds": resolve_sources(config["sourceParagraphIds"]), "checks": checks})
    if seen != {(day, month) for day in STEMS for month in MONTHS}:
        raise ValueError("日干×月令必须覆盖完整120个入口；未定也应留有来源和状态")
    return {"version": 1, "sourceRevision": revision,
            "book": {"slug": book["slug"], "title": book["title"], "file": TEXT},
            "sources": spans, "profiles": profiles}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/tiaohou-profiles.json")
    args = parser.parse_args()
    dirty = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", PACK, TEXT], cwd=ROOT).returncode
    if dirty:
        raise SystemExit("穷通源数据或全文尚未提交，不能把工作区内容标记为 HEAD；先提交当前源内容。")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    data = build_export(ROOT, revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"profiles": len(data["profiles"]), "source_spans": len(data["sources"]),
                      "source_revision": revision, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
