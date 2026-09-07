#!/usr/bin/env python3
"""Build a real per-pack inventory and stable paragraph IDs.

Original fulltexts are not modified. Derived files go to references/inventory/.
Doubtful glyphs are flagged, never guessed into 原文.
"""
from __future__ import annotations

import hashlib
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
PREFACE_RE = re.compile(r"序|跋|提要|进表|進表|原序|自序")
CATALOG_RE = re.compile(r"目录|目錄|总目|總目")
CASE_RE = re.compile(r"命造|造曰|例一|例二|例三|附例")
PROCEDURE_RE = re.compile(r"起例|歌诀|歌訣|步法|起法")
META_RE = re.compile(r"^-\s*source_|东里山人按|東里山人按")

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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_heading(title: str) -> str:
    if PREFACE_RE.search(title):
        return "序跋目录"
    if CATALOG_RE.search(title):
        return "序跋目录"
    if CASE_RE.search(title):
        return "案例"
    if PROCEDURE_RE.search(title):
        return "操作步骤"
    return "理论"


def classify_paragraph(text: str, chapter_kind: str) -> str:
    if META_RE.search(text):
        return "评注或元数据"
    if chapter_kind == "序跋目录":
        return "序跋目录"
    if chapter_kind == "案例":
        return "案例"
    if chapter_kind == "操作步骤":
        return "操作步骤"
    if CASE_RE.search(text[:40]):
        return "案例"
    return chapter_kind or "理论"


def split_paragraphs(lines: list[str]) -> tuple[list[dict], list[dict]]:
    chapters: list[dict] = []
    paragraphs: list[dict] = []
    current_heading = "正文"
    current_kind = "理论"
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
                    "kind": "理论",
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


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    fac = facsimile_index()
    packs: list[dict] = []
    kind_counter: Counter[str] = Counter()
    para_total = 0
    doubtful_total = 0

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
        ft_sha = None
        if ft.exists():
            text = ft.read_text(encoding="utf-8")
            lines = text.splitlines()
            line_count = len(lines)
            char_count = len(re.sub(r"\s+", "", text))
            ft_sha = sha256_file(ft)
            chapters, paragraphs = split_paragraphs(lines)
            for p in paragraphs:
                p["id"] = f"{slug}:{p['id']}"
                kind_counter[p["kind"]] += 1
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
                        "fulltext_sha256": ft_sha,
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
                "fulltext_sha256": ft_sha,
                "line_count": line_count,
                "char_count": char_count,
                "chapter_count": len(chapters),
                "chapters": chapters,
                "paragraph_count": len(paragraphs),
                "doubtful_paragraphs": sum(1 for p in paragraphs if p["doubtful"]),
                "missing_markers": sum(1 for p in paragraphs if p["missing_marker"]),
                "pack_files": files,
                "legacy_rule_candidates": rules_n,
                "executable_rules": 0,
                "art": art,
                "art_label": art_label,
                "destination": destination,
                "purpose": purpose,
                "facsimile_status": facsimile_status,
                "facsimile_paths": fac_hits,
                "oversize_release": oversize,
                "verified_rules": 0,
                "plain_language": "none"
                if destination != "engine"
                else ("seed_chart_notes" if slug in {"ziping-zhenquan", "ziwei-doushu-quanshu"} else "pending_reuse_of_first_path"),
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
        "schema_version": "fateradar-library-inventory-v1",
        "note": "55 是资料包口径，不是 55 部独立完整古籍。全文以磁盘 fulltext.md 实数为准。",
        "counts": {
            "catalog_ready_packs": catalog.get("ready_count"),
            "disk_packs": len(packs),
            "fulltext_files": sum(1 for p in packs if p["fulltext_exists"]),
            "blocked_or_excluded": len(excluded),
            "paragraphs": para_total,
            "doubtful_paragraphs": doubtful_total,
            "legacy_rule_candidates": sum(p["legacy_rule_candidates"] for p in packs),
            "verified_rules": 0,
            "executable_rules_in_this_commit": 0,
            "paragraph_kinds": dict(kind_counter),
            "destinations": dict(Counter(p["destination"] for p in packs)),
        },
        "packs": packs,
        "blocked_or_excluded": excluded,
    }

    exe_total = 0
    exe_dir = ROOT / "references/executable"
    if exe_dir.is_dir():
        for path in sorted(exe_dir.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            rules = payload.get("rules") or []
            exe_total += len(rules)
            slug = (payload.get("book") or {}).get("slug")
            for p in packs:
                if p["slug"] == slug:
                    p["executable_rules"] = len(rules)
                    p["plain_language"] = p.get("plain_language") or "executable_rules_defined"
    summary["counts"]["executable_rules_in_this_commit"] = exe_total

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
        f"- 旧 rules.yaml 候选：{summary['counts']['legacy_rule_candidates']}（全部 verified=false，不作运行权威）",
        f"- 本轮接入可执行规则：{summary['counts']['executable_rules_in_this_commit']}（`references/executable/*.json` 实数；产品引擎实现等价条件）",
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
    lines += ["", "## 资料包", "", "| 系统 | slug | 书名 | 全文 | 段落 | 去向 | 影印 |", "|---|---|---|---:|---:|---|---|"]
    for p in packs:
        lines.append(
            "| {system} | {slug} | {title} | {ft} | {pc} | {dest} | {fac} |".format(
                system=p["system"],
                slug=p["slug"],
                title=p["title"].replace("|", "｜"),
                ft="是" if p["fulltext_exists"] else "否",
                pc=p["paragraph_count"],
                dest=p["destination"],
                fac=p["facsimile_status"],
            )
        )
    lines += ["", "## 排除项", ""]
    for item in excluded:
        lines.append(f"- `{item['system']}/{item['slug']}` 《{item['title']}》：不入库。")
    lines += [
        "",
        "## 段落种类（启发式，不是人工审读）",
        "",
        "目录、序跋不硬造解读。疑字只标记，不由模型补字。",
        "",
    ]
    for kind, n in sorted(kind_counter.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {kind}：{n}")
    lines += [
        "",
        "段落 ID 形如 `slug:L0123-L0125`，对应 `sources/fulltext/.../fulltext.md` 行号，明细在 `references/inventory/paragraphs/`。",
        "",
    ]
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
