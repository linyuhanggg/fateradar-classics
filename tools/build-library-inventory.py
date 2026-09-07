#!/usr/bin/env python3
"""Build a real per-pack inventory and stable paragraph IDs.

Original fulltexts are not modified. Derived files go to references/inventory/.
Doubtful glyphs are flagged, never guessed into 原文.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references/catalog/catalog.json"
BOOKS = ROOT / "references/books"
FULLTEXT = ROOT / "sources/fulltext"
FACSIMILE = ROOT / "sources/facsimile"
OUT_DIR = ROOT / "references/inventory"
DOC_OUT = ROOT / "docs/LIBRARY_INVENTORY.md"

DOUBTFUL_RE = re.compile(r"[�□囗■△�]")
MISSING_RE = re.compile(r"缺页|缺葉|阙文|闕文|此页残|此頁殘")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
PREFACE_RE = re.compile(r"序跋|前言|後記|后记|提要|进表|進表|原序|自序|序$|跋$")
CATALOG_RE = re.compile(r"目录|目錄|总目|總目")
CASE_RE = re.compile(r"命造|造曰|例一|例二|例三|附例")
PROCEDURE_RE = re.compile(r"起例|歌诀|歌訣|步法|起法")
PROCEDURE_BODY_RE = re.compile(
    r"取[课課]先[从從]|先取神[遥遙]克|"
    r"(?:正月|子[时時])[^\n。！？]{0,5}起[^\n。！？]{0,10}[顺順逆]|"
    r"[顺順逆][数數行][^\n。！？]{0,15}(?:位|[宫宮]|[支辰])"
)
THEORY_HEADING_RE = re.compile(r"(?:^|[、\s])(?:论|論).+")
META_RE = re.compile(r"^-\s*source_|东里山人按|東里山人按")
STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
PILLAR_RE = re.compile(rf"[{STEMS}][{BRANCHES}]")
PILLAR_RUN_RE = re.compile(rf"[{STEMS}][{BRANCHES}](?:[\s、，,·]*[{STEMS}][{BRANCHES}]){{3,}}")
ANNOTATION_KINDS = {"理论", "术语", "规则候选", "操作步骤", "案例", "序跋目录", "评注或元数据", "重复", "待核实", "待分类"}

OVERSIZE = {
    "huangji-jingshi": "Release facsimiles-oversize-2026-09-04 / 0803.djvu",
    "huozhu-lin": "Release facsimiles-oversize-2026-09-04 / GGZBCK421.pdf",
    "zhouyi-zhezhong": "Release facsimiles-oversize-2026-09-04 / 0038.djvu",
    "taiyi-shenshu": "Release facsimiles-oversize-2026-09-04 / 0810.djvu",
    "liuren-miben": "Release facsimiles-oversize-2026-09-04 / NCL-06572-daliuren-miben.pdf",
}

SLUG_ART = {
    "qimen-dunjia-tongzhi": ("qimen", "奇门", "engine"),
    "qimen-faqiao": ("qimen", "奇门", "excluded_copyright"),
    "daliuren-daquan": ("liuren", "六壬", "engine"),
    "liuren-miben": ("liuren", "六壬", "engine"),
    "liuren-zhiyin": ("liuren", "六壬", "engine"),
    "taiyi-shenshu": ("taiyi", "太乙", "knowledge"),
    "zengshan-buyi": ("liuyao", "六爻", "engine"),
    "huozhu-lin": ("liuyao", "六爻", "engine"),
    "bushi-zhengzong": ("liuyao", "六爻", "engine"),
    "meihua-yishu": ("meihua", "梅花", "engine"),
    "huangji-jingshi": ("huangji", "皇极", "knowledge"),
    "huangjin-ce": ("divination", "占卜通论", "knowledge"),
    "zhouyi-zhezhong": ("yijing", "周易", "knowledge"),
    "guotian-jing": ("qizheng", "七政四余", "engine"),
    "xingming-suyuan": ("qizheng", "七政四余", "engine"),
    "xingxue-dacheng": ("qizheng", "七政四余", "engine"),
}

SYSTEM_ART = {
    "bazi": ("bazi", "八字", "engine"),
    "ziwei": ("ziwei", "紫微", "engine"),
    "fengshui": ("fengshui", "风水", "knowledge"),
    "physiognomy": ("xiangfa", "相法", "knowledge"),
    "selection": ("selection", "择日", "knowledge"),
    "luming-nayin": ("nayin", "禄命纳音", "knowledge"),
    "xingming": ("qizheng", "七政四余", "engine"),
}


def four_pillar_sequences(text: str) -> list[list[str]]:
    """Only flag explicit four-pillar examples; longer calendar/luck lists stay lists."""
    found = []
    for match in PILLAR_RUN_RE.finditer(text):
        pillars = PILLAR_RE.findall(match.group())
        if len(pillars) != 4:
            continue
        if any(STEMS.index(p[0]) % 2 != BRANCHES.index(p[1]) % 2 for p in pillars):
            continue
        before = text[max(0, match.start() - 50):match.start()]
        after = text[match.end():match.end() + 30].strip()
        context = re.search(r"命|造|生於|生于|例如|譬如|如$", before + after)
        bare_with_comment = not before.strip() and after.startswith(("（", "("))
        if context or bare_with_comment:
            found.append(pillars)
    return found


def classify_heading(title: str) -> str:
    if PREFACE_RE.search(title):
        return "序跋目录"
    if CATALOG_RE.search(title):
        return "序跋目录"
    if CASE_RE.search(title):
        return "案例"
    if PROCEDURE_RE.search(title):
        return "操作步骤"
    if THEORY_HEADING_RE.search(title):
        return "理论"
    return "待分类"


def classify_paragraph(text: str, chapter_kind: str) -> str:
    if META_RE.search(text):
        return "评注或元数据"
    if four_pillar_sequences(text) or CASE_RE.search(text[:40]):
        return "案例"
    if PROCEDURE_BODY_RE.search(text):
        return "操作步骤"
    if chapter_kind == "序跋目录":
        return "序跋目录"
    if chapter_kind == "案例":
        return "案例"
    if chapter_kind == "操作步骤":
        return "操作步骤"
    return chapter_kind or "待分类"


def split_paragraphs(lines: list[str]) -> tuple[list[dict], list[dict]]:
    chapters: list[dict] = []
    paragraphs: list[dict] = []
    current_heading = "正文"
    current_kind = "待分类"
    current_start = 1
    buf: list[tuple[int, str]] = []

    def flush_chapter(end: int) -> None:
        nonlocal current_start
        if not chapters or chapters[-1]["title"] != current_heading:
            chapters.append(
                {
                    "title": current_heading,
                    "kind": current_kind,
                    "start_line": current_start,
                    "end_line": end,
                }
            )
        else:
            chapters[-1]["end_line"] = end

    def flush_para() -> None:
        if not buf:
            return
        start, end = buf[0][0], buf[-1][0]
        text = "\n".join(t for _, t in buf).strip()
        if not text:
            buf.clear()
            return
        kind = classify_paragraph(text, current_kind)
        paragraphs.append(
            {
                "id": f"L{start:04d}-L{end:04d}",
                "start_line": start,
                "end_line": end,
                "heading": current_heading,
                "kind": kind,
                "classification_method": "unclassified" if kind == "待分类" else "pattern",
                **({"four_pillar_sequences": four_pillar_sequences(text)} if kind == "案例" and four_pillar_sequences(text) else {}),
                "char_count": len(re.sub(r"\s+", "", text)),
                "doubtful": bool(DOUBTFUL_RE.search(text)),
                "missing_marker": bool(MISSING_RE.search(text)),
            }
        )
        buf.clear()

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        m = HEADING_RE.match(line)
        if m:
            flush_para()
            if chapters:
                chapters[-1]["end_line"] = i - 1
            current_heading = m.group(2).strip()
            current_kind = classify_heading(current_heading)
            current_start = i
            chapters.append(
                {
                    "title": current_heading,
                    "kind": current_kind,
                    "start_line": i,
                    "end_line": i,
                }
            )
            continue
        if not line.strip():
            flush_para()
            continue
        buf.append((i, line))
    flush_para()
    if chapters:
        chapters[-1]["end_line"] = len(lines)
    else:
        flush_chapter(len(lines))
        if not chapters:
            chapters.append(
                {
                    "title": "正文",
                    "kind": "待分类",
                    "start_line": 1,
                    "end_line": len(lines),
                }
            )
    return chapters, paragraphs


def facsimile_index() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    if not FACSIMILE.exists():
        return found
    for path in FACSIMILE.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".pdf", ".djvu", ".jpg", ".png", ".tif", ".tiff"}:
            if path.name in {"MANIFEST.md", "README.md"}:
                continue
            if path.suffix.lower() not in {".pdf", ".djvu"}:
                continue
        rel = str(path.relative_to(ROOT))
        for part in path.parts:
            found.setdefault(part, []).append(rel)
    return found


def art_of(system: str, slug: str) -> tuple[str, str, str]:
    if slug in SLUG_ART:
        return SLUG_ART[slug]
    return SYSTEM_ART.get(system, (system, system, "knowledge"))


def pack_files(pack: Path) -> dict[str, bool]:
    names = [
        "index.md",
        "chapter-map.md",
        "terms.md",
        "rules.yaml",
        "rules.md",
        "procedures.md",
        "quote-index.md",
        "validation.md",
    ]
    return {name: (pack / name).exists() for name in names}


def count_rule_ids(path: Path) -> int:
    if not path.exists():
        return 0
    return len(re.findall(r"^- rule_id:", path.read_text(encoding="utf-8"), re.M))


def apply_annotations(system: str, slug: str, paragraphs: list[dict]) -> None:
    """Bind existing semantic notes; source-reviewed is electronic review, not human verification."""
    path = ROOT / "references/annotations" / system / f"{slug}.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("bookSlug") != slug or not isinstance(data.get("entries"), list):
        raise ValueError(f"{path}: bookSlug/entries 与资料包不符")
    indexed = {p["id"]: p for p in paragraphs}
    seen = set()
    for entry in data["entries"]:
        pid = entry.get("paragraphId")
        if pid not in indexed:
            raise ValueError(f"{path}: paragraphId 不在原段落库中: {pid}")
        if pid in seen:
            raise ValueError(f"{path}: 重复 paragraphId: {pid}")
        seen.add(pid)
        if entry.get("kind") not in ANNOTATION_KINDS:
            raise ValueError(f"{path}: {pid} kind 不在约定分类中")
        if entry.get("review") not in {"source-reviewed", "draft"}:
            raise ValueError(f"{path}: {pid} review 应为 source-reviewed 或 draft")
        if not isinstance(entry.get("vernacular"), str) or not entry["vernacular"].strip():
            raise ValueError(f"{path}: {pid} vernacular 需要实际白话或处理说明，草稿也不能只留空串")
        if not all(isinstance(entry.get(key), list) for key in ("terms", "notes")):
            raise ValueError(f"{path}: {pid} terms/notes 应为数组")
        paragraph = indexed[pid]
        paragraph["automatic_kind"] = paragraph["kind"]
        paragraph["kind"] = entry["kind"]
        paragraph["classification_method"] = "annotation"
        paragraph["annotation_file"] = str(path.relative_to(ROOT))
        paragraph["annotation_review"] = entry["review"]
        paragraph["has_vernacular"] = bool(entry["vernacular"].strip())


def paragraph_progress(paragraphs: list[dict]) -> dict[str, int]:
    annotated = [p for p in paragraphs if p.get("classification_method") == "annotation"]
    reviewed = [p for p in annotated if p.get("annotation_review") == "source-reviewed"]
    vernacular = sum(bool(p.get("has_vernacular")) for p in annotated)
    return {
        "annotated_paragraphs": len(annotated),
        "source_reviewed_paragraphs": len(reviewed),
        "vernacular_paragraphs": vernacular,
        "source_reviewed_vernacular_paragraphs": sum(bool(p.get("has_vernacular")) for p in reviewed),
        "unannotated_paragraphs": len(paragraphs) - len(annotated),
        "paragraphs_without_vernacular": len(paragraphs) - vernacular,
        "literal_duplicate_paragraphs": sum("same_text_as" in p for p in paragraphs),
    }


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    fac = facsimile_index()
    packs: list[dict] = []
    kind_counter: Counter[str] = Counter()
    method_counter: Counter[str] = Counter()
    progress_counter: Counter[str] = Counter()
    first_text_occurrence: dict[str, str] = {}
    para_total = 0
    doubtful_total = 0

    rule_stats: dict[tuple[str, str], Counter] = {}
    for path in sorted((ROOT / "references/executable").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        book = payload.get("book") or {}
        rules = payload.get("rules") or []
        key = (book.get("system"), book.get("slug"))
        stats = rule_stats.setdefault(key, Counter())
        stats["rule_definitions"] += len(rules)
        stats["rule_definitions_with_vernacular"] += sum(
            isinstance(rule.get("vernacular"), str) and bool(rule["vernacular"].strip()) for rule in rules
        )
        stats["verified_rule_flags"] += sum(rule.get("verified") is True for rule in rules)

    notes_path = ROOT / "references/readings/chart-notes.json"
    notes = json.loads(notes_path.read_text(encoding="utf-8")).get("notes", []) if notes_path.exists() else []
    notes_by_file = Counter(
        note.get("source", {}).get("anchor", {}).get("file") for note in notes
        if note.get("source", {}).get("anchor", {}).get("file")
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    para_root = OUT_DIR / "paragraphs"
    para_root.mkdir(parents=True, exist_ok=True)

    catalog_by_slug = {
        f"{p['system']}/{p['slug']}": p for p in catalog.get("ready_reference_packs", [])
    }

    disk_packs = sorted(p for p in BOOKS.glob("*/*") if p.is_dir())
    for pack in disk_packs:
        system, slug = pack.parts[-2], pack.parts[-1]
        key = f"{system}/{slug}"
        cat = catalog_by_slug.get(key, {})
        art, art_label, destination = art_of(system, slug)
        ft = FULLTEXT / system / slug / "fulltext.md"
        files = pack_files(pack)
        rules_n = count_rule_ids(pack / "rules.yaml")
        fac_hits = fac.get(slug, [])
        oversize = OVERSIZE.get(slug)
        facsimile_status = (
            "oversize_release"
            if oversize
            else "in_repo"
            if fac_hits
            else "not_confirmed"
        )
        chapters: list[dict] = []
        paragraphs: list[dict] = []
        line_count = 0
        char_count = 0
        if ft.exists():
            text = ft.read_text(encoding="utf-8")
            lines = text.splitlines()
            line_count = len(lines)
            char_count = len(re.sub(r"\s+", "", text))
            chapters, paragraphs = split_paragraphs(lines)
            for p in paragraphs:
                p["id"] = f"{slug}:{p['id']}"
                normalized = re.sub(r"\s+", "", "\n".join(lines[p["start_line"] - 1:p["end_line"]]))
                previous = first_text_occurrence.setdefault(normalized, p["id"])
                if previous != p["id"]:
                    p["same_text_as"] = previous
            apply_annotations(system, slug, paragraphs)
            for p in paragraphs:
                kind_counter[p["kind"]] += 1
                method_counter[p["classification_method"]] += 1
                para_total += 1
                if p["doubtful"]:
                    doubtful_total += 1
            para_path = para_root / system
            para_path.mkdir(parents=True, exist_ok=True)
            (para_path / f"{slug}.json").write_text(
                json.dumps(
                    {
                        "pack": key,
                        "fulltext": str(ft.relative_to(ROOT)),
                        "classification_note": "pattern 是文本模式初筛；annotation 来源另见注解文件；source-reviewed 不等同人工影印核验。same_text_as 仅表示忽略空白后的原文字面相同。",
                        "paragraphs": paragraphs,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        elif destination == "excluded_copyright":
            destination = "excluded_copyright"
        else:
            destination = destination if destination != "engine" else "missing_fulltext"

        purpose = {
            "engine": "接入对应术数引擎与免费解释，不把资料包数当成已完成规则数。",
            "knowledge": "当前页面没有对应输入，进入可检索知识库，不冒充已接入八术。",
            "excluded_copyright": "明确排除：不抓取、不补全文、不接入运行规则。",
            "missing_fulltext": "缺全文，只保留书目与缺失记录。",
        }[destination if destination in {"engine", "knowledge", "excluded_copyright", "missing_fulltext"} else "knowledge"]
        progress = paragraph_progress(paragraphs)
        progress_counter.update(progress)
        stats = rule_stats.get((system, slug), Counter())
        legacy_verified = len(re.findall(r"^\s+verified:\s*true(?:\s|$)", (pack / "rules.yaml").read_text(encoding="utf-8"), re.M)) if files["rules.yaml"] else 0

        packs.append(
            {
                "system": system,
                "slug": slug,
                "title": cat.get("title") or pack.name,
                "source_anchor_url": cat.get("source_anchor_url"),
                "source_risk": cat.get("source_risk"),
                "catalog_fulltext_path_legacy": cat.get("local_fulltext_path"),
                "actual_fulltext_path": str(ft.relative_to(ROOT)) if ft.exists() else None,
                "fulltext_exists": ft.exists(),
                "line_count": line_count,
                "char_count": char_count,
                "chapter_count": len(chapters),
                "chapters": chapters,
                "paragraph_count": len(paragraphs),
                "doubtful_paragraphs": sum(1 for p in paragraphs if p["doubtful"]),
                "missing_markers": sum(1 for p in paragraphs if p["missing_marker"]),
                "pack_files": files,
                "legacy_rule_candidates": rules_n,
                "legacy_verified_rule_flags": legacy_verified,
                "rule_definitions": stats["rule_definitions"],
                "rule_definitions_with_vernacular": stats["rule_definitions_with_vernacular"],
                "verified_rule_flags": stats["verified_rule_flags"],
                "reading_notes": notes_by_file[str(ft.relative_to(ROOT))],
                **progress,
                "art": art,
                "art_label": art_label,
                "destination": destination,
                "purpose": purpose,
                "facsimile_status": facsimile_status,
                "facsimile_paths": fac_hits,
                "oversize_release": oversize,
            }
        )

    excluded = []
    for item in catalog.get("blocked_or_excluded", []):
        excluded.append(
            {
                "system": item.get("system"),
                "slug": item.get("slug"),
                "title": item.get("title"),
                "destination": "blocked_or_excluded",
                "reason": item.get("reason"),
                "purpose": "遵守已有排除，不以全量取消边界。",
            }
        )

    summary = {
        "generated_on": date.today().isoformat(),
        "schema_version": "fateradar-library-inventory-v2",
        "note": "资料包、基础段落索引、语义注解、白话和规则定义分开统计；规则 JSON 条数不证明引擎已经接入，source-reviewed 不等同人工影印核验。全文以磁盘 fulltext.md 实数为准。",
        "counts": {
            "catalog_ready_packs": len(catalog.get("ready_reference_packs", [])),
            "disk_packs": len(packs),
            "fulltext_files": sum(1 for p in packs if p["fulltext_exists"]),
            "blocked_or_excluded": len(excluded),
            "paragraphs": para_total,
            "doubtful_paragraphs": doubtful_total,
            "legacy_rule_candidates": sum(p["legacy_rule_candidates"] for p in packs),
            "rule_definitions": sum(stats["rule_definitions"] for stats in rule_stats.values()),
            "rule_definitions_with_vernacular": sum(stats["rule_definitions_with_vernacular"] for stats in rule_stats.values()),
            "verified_rule_flags": sum(stats["verified_rule_flags"] for stats in rule_stats.values()),
            "legacy_verified_rule_flags": sum(p["legacy_verified_rule_flags"] for p in packs),
            "reading_notes": len(notes),
            **progress_counter,
            "paragraph_kinds": dict(kind_counter),
            "classification_methods": dict(method_counter),
            "destinations": dict(Counter(p["destination"] for p in packs)),
        },
        "packs": packs,
        "blocked_or_excluded": excluded,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "library-inventory.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    dest = summary["counts"]["destinations"]
    lines = [
        "# 全库书目与覆盖清单",
        "",
        f"生成日期：{summary['generated_on']}。由 `tools/build-library-inventory.py` 从磁盘实数生成，不沿用 55 部完整古籍的说法。",
        "",
        "## 口径",
        "",
        f"- catalog ready 资料包：{summary['counts']['catalog_ready_packs']}",
        f"- 磁盘 `references/books/*/*`：{summary['counts']['disk_packs']}",
        f"- 实际 `sources/fulltext/**/fulltext.md`：{summary['counts']['fulltext_files']}",
        f"- catalog 另列排除项：{summary['counts']['blocked_or_excluded']}",
        f"- 稳定段落：{summary['counts']['paragraphs']}（含疑文段 {summary['counts']['doubtful_paragraphs']}）",
        f"- 旧 rules.yaml 候选记录：{summary['counts']['legacy_rule_candidates']}（其中 declared verified=true：{summary['counts']['legacy_verified_rule_flags']}；不作运行权威）",
        f"- 新规则定义记录：{summary['counts']['rule_definitions']}，有规则白话 {summary['counts']['rule_definitions_with_vernacular']}（仅统计 `references/executable/*.json`；不据此认定运行接入或分支验证完成）",
        f"- 新规则 declared verified=true：{summary['counts']['verified_rule_flags']}（只读已有标记，不自动提升）",
        f"- 独立盘面读法：{summary['counts']['reading_notes']}（`references/readings/chart-notes.json`；不换算成全文白话覆盖）",
        "",
        "## 实际语义加工进度",
        "",
        f"- 已有段落注解：{progress_counter['annotated_paragraphs']} / {para_total}",
        f"- 标记电子原文审读 source-reviewed：{progress_counter['source_reviewed_paragraphs']}（不是人工影印核验）",
        f"- 有非空白话或处理说明的段落：{progress_counter['vernacular_paragraphs']}（其中 source-reviewed：{progress_counter['source_reviewed_vernacular_paragraphs']}）",
        f"- 尚无注解：{progress_counter['unannotated_paragraphs']}；尚无段落白话：{progress_counter['paragraphs_without_vernacular']}",
        f"- 原文字面重复段：{progress_counter['literal_duplicate_paragraphs']}（仅忽略空白比较，same_text_as 不代表流派或理论等价）",
        "",
        "上述是文件中实际存在的产物统计，不是全库完成率。模式分类只帮助找材料，未分类、只有规则标题或未审读白话都不能算完成。",
        "",
        "## 去向",
        "",
    ]
    for key, label in [
        ("engine", "对应八术引擎"),
        ("knowledge", "可检索知识库，未接入八术页面"),
        ("excluded_copyright", "版权排除"),
        ("missing_fulltext", "缺全文"),
    ]:
        lines.append(f"- {label}：{dest.get(key, 0)}")
    lines += ["", "## 资料包", "", "| 系统 | slug | 书名 | 全文 | 段落 | 注解 | 段落白话 | 规则定义 | 去向 | 影印 |", "|---|---|---|---:|---:|---:|---:|---:|---|---|"]
    for p in packs:
        lines.append(
            "| {system} | {slug} | {title} | {ft} | {pc} | {annotations} | {vernacular} | {rules} | {dest} | {fac} |".format(
                system=p["system"],
                slug=p["slug"],
                title=p["title"].replace("|", "｜"),
                ft="是" if p["fulltext_exists"] else "否",
                pc=p["paragraph_count"],
                annotations=p["annotated_paragraphs"],
                vernacular=p["vernacular_paragraphs"],
                rules=p["rule_definitions"],
                dest=p["destination"],
                fac=p["facsimile_status"],
            )
        )
    lines += ["", "## 排除项", ""]
    for item in excluded:
        lines.append(f"- `{item['system']}/{item['slug']}` 《{item['title']}》：不入库。")
    lines += [
        "",
        "## 段落分类来源",
        "",
        f"- pattern 文本模式初筛：{method_counter['pattern']}；annotation 实际语义注解：{method_counter['annotation']}；unclassified 待分类：{method_counter['unclassified']}",
        "- 四柱案例从正文命造或带评语的四组干支识别；起例、先取后取与月起顺逆等操作从正文识别。模式结果仍可能需修订，不当作人工审读。",
        "- 目录、序跋不硬造解读；无分类依据时保留待分类。疑字只标记，不由模型补字。",
        "",
    ]
    for kind, n in sorted(kind_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {kind}：{n}")
    lines += [
        "",
        "段落 ID 形如 `slug:L0123-L0125`，对应 `sources/fulltext/.../fulltext.md` 行号，明细在 `references/inventory/paragraphs/`。",
        "",
        "## 注解输入约定",
        "",
        "读取 `references/annotations/{system}/{slug}.json`：顶层 `bookSlug`、`entries`；每项 `paragraphId` 必须对应已有确切段落，`kind` 为分类，`vernacular` 为非空中文白话或处理说明，`terms`、`notes` 为数组，`review` 为 `source-reviewed` 或 `draft`。草稿也需要实际说明；同一文件同一段落只一项注解；错误或重复 ID 会中止生成，避免虚增进度。",
        "",
        "分类支持：理论、术语、规则候选、操作步骤、案例、序跋目录、评注或元数据、重复、待核实、待分类。source-reviewed 表示这条注解已对照电子原文，不替代 human verified，也不证明算法可执行。",
        "",
    ]
    DOC_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOC_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "packs": len(packs),
                "fulltext": summary["counts"]["fulltext_files"],
                "paragraphs": para_total,
                "out": str((OUT_DIR / "library-inventory.json").relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
