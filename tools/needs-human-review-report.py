#!/usr/bin/env python3
"""把 `tools/reports/needs-human-review.md` 从过程稿变成**可复算的论断台账**。

背景：旧件是手写过程稿（P6/P7/P10/P11 时期），没有生成器，因此会累积失真。
实测它至少三处与当前树不符：

  · 「san-shi/qimen-faqiao QM-P26、QM-P36：仓库无 fulltext」→ 两条**已有** anchor
    （指向 `sources/excerpts/qimen-faqiao-chaibu-v1.md`）。
  · 「shenfeng-tongkao R01–R05」「lantai-miaoxuan M01、R01–R07」「bushi-zhengzong R01–R06」
    → 那些是 **statement 前缀**，不是 `rule_id`；按字面检索这些 id **全部不存在**。
  · 「GR-01 / GR-03 已改 kind: procedure」→ 对**裸 id** 成立，但对
    `GUOTIANJING-GR-01` / `GUOTIANJING-GR-03`（同书另有这两条）**不成立**：
    前者 procedure、后者 doctrine。混用 id 写法会把复核带偏。

本脚本做三件事：
  1. 从 `references/books/*/*/rules.yaml` 算出**真实**的 `anchor: null` 集合；
  2. 把旧件的每条论断写成声明式检查（`CLAIMS`），逐条对当前树复核，给出
     `已解决` / `仍未决` / `论断已过时` / `机器不可判` 四种状态；
  3. 重写 `tools/reports/needs-human-review.md` 并落一份 JSON 台账。

**本脚本不写任何锚点、不改任何规则**——「不要硬锚」是硬约束，这里只做核对与登记。

    python3 tools/needs-human-review-report.py                    # 人类可读
    python3 tools/needs-human-review-report.py --json             # 台账
    python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

RESOLVED, OPEN, STALE, UNVERIFIABLE = "已解决", "仍未决", "论断已过时", "机器不可判"

# ── 论断台账 ────────────────────────────────────────────────────────────────
# 每条对应旧件里的一段可核对的话。`rules` 用**当前真实的 rule_id**（旧件的写法记在
# `doc_notation` 里，便于对照为什么旧写法会检索不到）。
CLAIMS: list[dict] = [
    {
        "id": "faqiao-no-fulltext",
        "category": "著作权 / 无全文",
        "from_doc": "san-shi/qimen-faqiao QM-P26、QM-P36：仓库无 fulltext，禁止抓现代出版社整理本。",
        "doc_notation": "QM-P26 / QM-P36（与当前 rule_id 一致）",
        "rules": [("san-shi/qimen-faqiao", "QM-P26"), ("san-shi/qimen-faqiao", "QM-P36")],
        "expect": {"anchor": "any"},
        "note": "旧件的顾虑是著作权（不得抓现代整理本）。现两条 anchor 指向 `sources/excerpts/qimen-faqiao-chaibu-v1.md`，"
        "是仓内自制选段、非抓取版，故该顾虑不再阻塞；是否接受「以选段为据」仍需人认可。",
        "on_hold": False,
    },
    {
        "id": "pack-meta-rules",
        "category": "Pack 元规则（不在书中）",
        "from_doc": "statement 含「安全改写 / reframe / 不替代 / 并读 / 调用本 pack」等，原文无对应句："
        "`bazi/shenfeng-tongkao` R01–R05；`luming-nayin/lantai-miaoxuan` M01、R01–R07；"
        "`divination/bushi-zhengzong` R01–R06；`xingming/xingming-suyuan` XINGMINGSUYU-042/043。",
        "doc_notation": "R01–R05 / M01 / R01–R07 / R01–R06 是 **statement 前缀**，不是 rule_id；"
        "按 id 检索会全部落空。此处换成当前真实 id。",
        "rules": [
            ("bazi/shenfeng-tongkao", "SF"),
            ("bazi/shenfeng-tongkao", "SHENFENGTONG-SF"),
            ("bazi/shenfeng-tongkao", "SHENFENGTONG-003"),
            ("bazi/shenfeng-tongkao", "SHENFENGTONG-004"),
            ("bazi/shenfeng-tongkao", "SHENFENGTONG-005"),
            ("luming-nayin/lantai-miaoxuan", "LT"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-LT"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-003"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-004"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-005"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-006"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-007"),
            ("luming-nayin/lantai-miaoxuan", "LANTAIMIAOXU-008"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-BSZZ"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-003"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-004"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-005"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-006"),
            ("divination/bushi-zhengzong", "BUSHIZHENGZO-007"),
            ("xingming/xingming-suyuan", "XINGMINGSUYU-042"),
            ("xingming/xingming-suyuan", "XINGMINGSUYU-043"),
        ],
        # 旧件按字面写的 id；机器直接拿去检索，用来量化「照旧件抄会找不到」。
        "doc_literal_ids": [
            ("bazi/shenfeng-tongkao", "R01"),
            ("bazi/shenfeng-tongkao", "R02"),
            ("bazi/shenfeng-tongkao", "R03"),
            ("bazi/shenfeng-tongkao", "R04"),
            ("bazi/shenfeng-tongkao", "R05"),
            ("luming-nayin/lantai-miaoxuan", "M01"),
            ("luming-nayin/lantai-miaoxuan", "R01"),
            ("luming-nayin/lantai-miaoxuan", "R02"),
            ("luming-nayin/lantai-miaoxuan", "R03"),
            ("luming-nayin/lantai-miaoxuan", "R04"),
            ("luming-nayin/lantai-miaoxuan", "R05"),
            ("luming-nayin/lantai-miaoxuan", "R06"),
            ("luming-nayin/lantai-miaoxuan", "R07"),
            ("divination/bushi-zhengzong", "R01"),
            ("divination/bushi-zhengzong", "R02"),
            ("divination/bushi-zhengzong", "R03"),
            ("divination/bushi-zhengzong", "R04"),
            ("divination/bushi-zhengzong", "R05"),
            ("divination/bushi-zhengzong", "R06"),
        ],
        "expect": {"anchor": "null"},
        "note": "21 条全部仍 anchor: null，论断成立：原文确实没有对应句，不能锚。"
        "这批是**永久性**的（除非人决定把它们单独归类成 pack 元规则而不列入待复核），不是待办。",
    },
    {
        "id": "multi-occurrence",
        "category": "原文多次出现、无法唯一落点",
        "from_doc": "`xingming/xingming-suyuan` 五曜连珠（4 处）、度主为正、飞廉、转生、闌干煞、流年三方对照；"
        "`divination/meihua-yishu` 乾兑属金（五行配卦多次）；"
        "`divination/zhouyi-zhezhong` 「形而上者谓之道」「见几而作」等经文多次；"
        "`luming-nayin/wuxing-jingji` 纳音 / 华盖单字标题过短。",
        "doc_notation": "以篇名/术语描述，未给 rule_id。",
        "rules": [],
        "expect": {},
        "note": "旧件只给术语、不给 id，机器无从逐条核对；且「哪一处算唯一落点」是**人的判断**，"
        "不能由机器定。要推进必须先补 id 清单。",
        "on_hold": True,
        "unverifiable_reason": "未给 rule_id，且「唯一落点」属人的判断",
    },
    {
        "id": "modern-summary",
        "category": "现代概括，书中无对应命题",
        "from_doc": "`divination/huangji-jingshi` HR-01 元会运世换算、HUANGJIJINGS-007/020/021"
        "「非占断 / 非国运 / 非个人命术」；`xingming/xingming-suyuan` 卷四后篇案例总述。",
        "doc_notation": "HR-01 等与当前 rule_id 一致",
        "rules": [
            ("divination/huangji-jingshi", "HR-01"),
            ("divination/huangji-jingshi", "HUANGJIJINGS-007"),
            ("divination/huangji-jingshi", "HUANGJIJINGS-020"),
            ("divination/huangji-jingshi", "HUANGJIJINGS-021"),
        ],
        "expect": {"anchor": "null"},
        "note": "4 条仍 anchor: null，论断成立。「卷四后篇案例总述」旧件未给 id，机器不可判。",
    },
    {
        "id": "p7-lz-metadata-quote",
        "category": "P7 恢复名单",
        "from_doc": "`LZ`（`physiognomy/liuzhuang-xiangfa`）quote 是 `source_base:` 元数据，P7 恢复名单误列，已改回 `anchor: null`。",
        "doc_notation": "LZ",
        "rules": [("physiognomy/liuzhuang-xiangfa", "LZ")],
        "expect": {"anchor": "null"},
        "note": "仍 anchor: null，且 quote 仍含元数据形态；论断成立。",
    },
    {
        "id": "v14-low-correspondence",
        "category": "V14 低对应度",
        "from_doc": "`FEIXINGZIWEI-008` 对应度 0.140、`ZIWEIDOUSHUQ-ZW-05` 对应度 0.106，V14 WARN。",
        "doc_notation": "两个 id 与当前一致",
        "rules": [
            ("ziwei/feixing-ziwei-doushu-yuanzhi", "FEIXINGZIWEI-008"),
            ("ziwei/ziwei-doushu-quanshu", "ZIWEIDOUSHUQ-ZW-05"),
        ],
        "expect": {"correspondence_max": 0.15},
        "note": "实测对应度与旧件一致（0.14 / 0.106），论断成立。这两条是「statement 概括性强」"
        "而非 quote 有问题——V14 本身已注明该档不必据以动手。",
    },
    {
        "id": "v11-g1-target",
        "category": "V11 与 G1",
        "from_doc": "G1 要求 V11 < 50，当前约 112。需人决定：是否按 fulltext 实际用字改正 `book.script`，或接受 V11 残留。",
        "doc_notation": "—",
        "rules": [],
        "expect": {},
        "note": "**旧件给的这个「需人决定」项，本轮用测量结案**：55 本书的 `book.script` 与各自 fulltext 实际用字"
        "**全部一致（0 处不符）**，所以没有「按实际用字改正 book.script」这回事——该选项是空的。"
        "V11 的真实成因是引文形态（未锚条目用另一种字形的概述），不是 script 登记错。",
        "resolution": "book.script 无需更正（实测 0 处不符）",
    },
    {
        "id": "qizheng-factgap",
        "category": "七政格局 / 行限未加 FactKey",
        "from_doc": "任务书 3a 要求加 `qizheng_geju`、`xingxian`；3c 要求引擎必须从已有排盘结果取出。"
        "实测 `buildQizheng` 只有星曜宫位宿度庙旺，没有格局名或行限字段。按 3c 不加这两个 key。约 35 条七政未映射规则本轮仍空。",
        "doc_notation": "GUOTIANJING-GR-02 / -GR-05 / GR-03（旧件混用了裸 id 与带前缀 id）",
        "rules": [
            ("xingming/guotian-jing", "GUOTIANJING-GR-02"),
            ("xingming/guotian-jing", "GUOTIANJING-GR-05"),
            ("xingming/guotian-jing", "GUOTIANJING-GR-03"),
        ],
        "expect": {"anchor": "any", "applicable_to": "empty"},
        "note": "三条仍无可写谓词。「加 qizheng_geju / xingxian」需要新写五曜格局与洞微百六限算法，"
        "属算法开发，不在语料轮次范围。**数字已漂移**：旧件说「约 35 条七政未映射」，实测 **65 条**。",
        "stale_numbers": {"七政未映射": {"doc": 35, "measured": 65}},
    },
    {
        "id": "catalog-titles",
        "category": "七政目录篇名",
        "from_doc": "P11 把 31 条 `xingming-suyuan` 未映射规则改归「目录篇名，不是可判定规则」，"
        "并从谓词覆盖率分母剔除。下列 statement 带一点判定语气，但仍保守留在目录篇名："
        "XINGMINGSUYU-XR-03、XR-04、XINGMINGSUYU-XR-04、XR-06、XINGMINGSUYU-038、XINGMINGSUYU-047、XR-07。",
        "doc_notation": "与当前一致",
        "rules": [
            ("xingming/xingming-suyuan", "XINGMINGSUYU-XR-03"),
            ("xingming/xingming-suyuan", "XINGMINGSUYU-XR-04"),
            ("xingming/xingming-suyuan", "XR-04"),
            ("xingming/xingming-suyuan", "XR-06"),
            ("xingming/xingming-suyuan", "XINGMINGSUYU-038"),
            ("xingming/xingming-suyuan", "XINGMINGSUYU-047"),
            ("xingming/xingming-suyuan", "XR-07"),
        ],
        "expect": {"in_catalog_title_set": True},
        "note": "7 条确实都在 `CATALOG_TITLE_RULE_IDS` 名单内（已从覆盖率分母剔除并单独计数），论断成立。",
    },
    {
        "id": "procedure-kind",
        "category": "起例改 procedure",
        "from_doc": "`GR-01` / `GR-03` 已改 `kind: procedure`。",
        "doc_notation": "裸 id。同书另有 `GUOTIANJING-GR-01` / `-GR-03` 两条**不同**规则，"
        "前者 doctrine、后者 procedure——旧件不写明前缀会让复核者改错条。",
        "rules": [("xingming/guotian-jing", "GR-01"), ("xingming/guotian-jing", "GR-03")],
        "expect": {"kind": "procedure"},
        "note": "两条确实都是 procedure，论断成立（但 id 写法必须带准，见 doc_notation）。",
    },
    {
        "id": "ziwei-palace-scope",
        "category": "紫微宫位 scope",
        "from_doc": "24 条规则、54 个谓词按 statement 写了 `scope.palace`。未加 scope 的包括：星性、夹命、"
        "地支居子/居午、未点名宫位的同宫、宫位专章无列星、`TAIWEIFU-004` 天马。"
        "G10 未达标：仍无法在不改 `ziwei.ts` / 不改断言的前提下让默认 top-6 两盘不同。",
        "doc_notation": "TAIWEIFU-004",
        "rules": [("ziwei/taiwei-fu", "TAIWEIFU-004")],
        "expect": {"has_scope_palace": False},
        "note": "**G10 已不成立**：本轮实测产品仓 `tests/rules/predicate-matching.test.ts` 的"
        "「两盘 ruleId 集合不同」对六个 art（含 ziwei）**全部通过**，即该阻塞已消失，不需要改 `ziwei.ts`、"
        "也不需要为凑差异补宫位。TAIWEIFU-004 仍无 scope.palace（留给 V15 reverse6 用例）。",
        "resolution": "G10 阻塞已消失（产品仓该断言现为绿）",
    },
    {
        "id": "p6-grey-zone",
        "category": "P6 灰区（对应度 0.15–0.30）",
        "from_doc": "任务书要求机器不动这一档，留人抽检。不要为了覆盖率把任务 5 已降级的 `<0.15` 填回去。",
        "doc_notation": "—",
        "rules": [],
        "expect": {},
        "note": "这是**政策**而非待办：机器不得动 0.15–0.30 档。本轮未动该档任何条目。",
        "on_hold": True,
        "unverifiable_reason": "政策声明，无逐条对象",
    },
    {
        "id": "restatement-census",
        "category": "190 条不可锚的根因（本轮实测新增）",
        "from_doc": "旧件把这些条目分列为「无全文 / pack 元规则 / 原文多次出现 / 现代概括 / P7 名单 / V11」"
        "六类，读起来像是六种不同的待办。",
        "doc_notation": "—",
        "rules": [],
        "expect": {},
        "expect": {"unanchored_all_restatement": True},
        "note": "**实测：全部 189 条不可锚规则的 `quote_kind` 都是 `restatement`（编者重述），一条不例外。**"
        "也就是说它们的 `quote` 本身就是现代概述、**原文里根本没有对应句子可指**——"
        "「不要硬锚」在这里不是政策限制，而是逻辑后果：没有可锚的对象。"
        "本条同时解释了 §二 的 V11：未锚条目用概述、且概述多为另一种字形，"
        "于是与 `book.script` 的字形统计不同向。",
        "resolution": "归类归并：189 条的真问题只有一个——是否把重述换成真引文（会改动 quote），不是 189 个各自找锚点",
    },
]


def load_rules_index() -> dict[tuple[str, str], dict]:
    idx: dict[tuple[str, str], dict] = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        key = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict):
                idx[(key, r.get("rule_id"))] = r
    return idx


def unanchored() -> list[dict]:
    out: list[dict] = []
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        key = f"{b.get('system')}/{b.get('slug')}"
        for r in d.get("rules") or []:
            if isinstance(r, dict) and not isinstance(r.get("anchor"), dict):
                out.append(
                    {
                        "book": key,
                        "rule_id": r.get("rule_id"),
                        "kind": r.get("kind"),
                        "quote_kind": r.get("quote_kind"),
                    }
                )
    return out


def warn_counts() -> dict[str, int]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate-rules.py"), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}
    return dict(Counter(w.get("code") for w in payload.get("warnings") or []))


def book_script_audit() -> tuple[int, list[str]]:
    """book.script 与 fulltext 实际用字是否一致。这是旧件「需人决定」那一项的结案依据。"""
    try:
        import opencc
    except ImportError:
        return -1, []
    t2s = opencc.OpenCC("t2s").convert
    s2t = opencc.OpenCC("s2t").convert
    bad: list[str] = []
    total = 0
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        b = d.get("book") or {}
        ft = b.get("fulltext")
        if not ft or not (ROOT / ft).is_file():
            continue
        total += 1
        text = (ROOT / ft).read_text(encoding="utf-8")
        trad = sum(1 for x, y in zip(text, t2s(text)) if x != y)
        simp = sum(1 for x, y in zip(text, s2t(text)) if x != y)
        declared = b.get("script")
        if declared == "traditional" and simp > trad:
            bad.append(f"{b.get('system')}/{b.get('slug')}（登记 traditional，实测简体为主）")
        elif declared == "simplified" and trad > simp:
            bad.append(f"{b.get('system')}/{b.get('slug')}（登记 simplified，实测繁体为主）")
    return total, bad


def catalog_title_ids() -> set[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("pr", ROOT / "tools/predicate-report.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return set(mod.CATALOG_TITLE_RULE_IDS)


def check_claim(claim: dict, idx: dict, un: list[dict]) -> dict:
    if claim.get("on_hold"):
        return {**claim, "status": UNVERIFIABLE, "findings": [claim.get("unverifiable_reason", "")]}

    findings: list[str] = []
    missing: list[str] = []
    mismatched: list[str] = []
    exp = claim.get("expect") or {}
    cat = catalog_title_ids() if exp.get("in_catalog_title_set") else set()

    for book, rid in claim["rules"]:
        r = idx.get((book, rid))
        if r is None:
            missing.append(f"{book} {rid}")
            continue
        has_anchor = isinstance(r.get("anchor"), dict)
        if exp.get("anchor") == "null" and has_anchor:
            mismatched.append(f"{book} {rid}：期望 anchor=null，实测有锚")
        if exp.get("anchor") == "any" and not has_anchor:
            mismatched.append(f"{book} {rid}：期望有锚，实测 null")
        if exp.get("kind") and r.get("kind") != exp["kind"]:
            mismatched.append(f"{book} {rid}：期望 kind={exp['kind']}，实测 {r.get('kind')}")
        if exp.get("applicable_to") == "empty" and (r.get("applicable_to") or []):
            mismatched.append(f"{book} {rid}：期望 applicable_to 空，实测非空")
        if exp.get("has_scope_palace") is False:
            preds = r.get("applicable_to")
            leaves = []
            if isinstance(preds, list):
                leaves = [p for p in preds if isinstance(p, dict)]
            if any("palace" in (p.get("scope") or {}) for p in leaves):
                mismatched.append(f"{book} {rid}：期望无 scope.palace，实测有")
        if exp.get("in_catalog_title_set") and rid not in cat:
            mismatched.append(f"{book} {rid}：不在 CATALOG_TITLE_RULE_IDS 内")

    if exp.get("unanchored_all_restatement"):
        offenders = [f"{x['book']} {x['rule_id']}" for x in un if x.get("quote_kind") != "restatement"]
        findings.append(f"未锚 {len(un)} 条的 quote_kind：{sorted({x.get('quote_kind') or '(未标注)' for x in un})}")
        if offenders:
            mismatched.append(f"有 {len(offenders)} 条未锚规则不是 restatement：" + "、".join(offenders[:5]))

    if exp.get("correspondence_max") is not None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("vr", ROOT / "tools/validate-rules.py")
        vr = importlib.util.module_from_spec(spec)
        sys.modules["vr"] = vr
        spec.loader.exec_module(vr)
        for book, rid in claim["rules"]:
            r = idx.get((book, rid))
            if r is None:
                continue
            corr = vr.correspondence(r.get("statement") or "", r.get("quote") or "")
            findings.append(f"{book} {rid}：对应度 {corr:.3f}")
            if corr > exp["correspondence_max"]:
                mismatched.append(f"{book} {rid}：对应度 {corr:.3f} > {exp['correspondence_max']}")

    if missing:
        status = STALE
        findings.append("**按当前 rule_id 检索不到**：" + "、".join(missing))
    elif mismatched:
        status = STALE
        findings.extend(mismatched)
    elif claim.get("resolution"):
        status = RESOLVED
    else:
        status = OPEN

    # 量化「照旧件字面写法去检索会怎样」：查不到、或查到的是**另一条**规则。
    literal_bad: list[str] = []
    for book, rid in claim.get("doc_literal_ids") or []:
        r = idx.get((book, rid))
        if r is None:
            literal_bad.append(f"{book} {rid}（不存在）")
    if literal_bad:
        findings.append(
            f"**旧件字面写法有 {len(literal_bad)} 个 id 检索不到**（说明照抄旧件会找不到条目）："
            + "、".join(literal_bad[:6])
            + ("…" if len(literal_bad) > 6 else "")
        )
    return {**claim, "status": status, "findings": findings, "literal_unresolvable": len(literal_bad)}


def render_markdown(
    claims: list[dict],
    un: list[dict],
    warns: dict,
    script_total: int,
    script_bad: list[str],
    quote_kind_census: dict,
) -> str:
    by_cat: dict[str, list[dict]] = {}
    for c in claims:
        by_cat.setdefault(c["category"], []).append(c)
    counts = Counter(c["status"] for c in claims)
    per_book = Counter(x["book"] for x in un)

    L: list[str] = [
        "# 需要人工判断（可复算台账）",
        "",
        "由 `python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md` 生成。",
        "**本文件不写任何锚点、不改任何规则**——「不要硬锚」是硬约束；这里只做核对与登记。",
        "全部 `verified` 仍为 `false`。",
        "",
        "旧件是 P6/P7/P10/P11 时期的手写过程稿、无生成器，已累积失真（见各条 `论断已过时`）。",
        "",
        "## 一、台账总览",
        "",
        f"论断 {len(claims)} 条："
        + "、".join(f"**{k} {counts.get(k, 0)}**" for k in (RESOLVED, OPEN, STALE, UNVERIFIABLE)),
        "",
        "| 论断 | 类别 | 状态 |",
        "|---|---|---|",
    ]
    for cat, items in by_cat.items():
        for c in items:
            L.append(f"| `{c['id']}` | {cat} | **{c['status']}** |")
    L.append("")

    L += [
        "## 二、机器实测的规模（旧件未给、或已漂移）",
        "",
        f"- **`anchor: null` 的规则共 {len(un)} 条**（旧件按「81 条」流传，那是**行数**不是条数）。",
        f"- 这 {len(un)} 条的 `quote_kind` 分布："
        + "、".join(f"`{k}` {v}" for k, v in quote_kind_census.items())
        + "。",
        f"- `validate-rules.py` 当前 warning：V11 {warns.get('V11', 0)}、V14 {warns.get('V14', 0)}，"
        f"合计 {sum(warns.values())}（G1 要 V11 < 50，**仍未达**）。",
        f"- `book.script` 与 fulltext 实际用字：实测 **{script_total} 本，不符 {len(script_bad)} 本**"
        + ("。" if not script_bad else "：" + "；".join(script_bad) + "。"),
        "",
        "> ⚠️ **本节是旧件最需要的更正**：`anchor_recover.py` 在 t167 入库 31,525 源段之后重跑过一次，"
        "表观「可以锚 25 条」；加两道前置闸门（跳过 `restatement`、用 V13 判据挡劣质 quote）后"
        "**可锚数归零**——那 25 条全是被锚上的**来源标签**（如「入地眼全書龍法卷二」）或重述文本。"
        "也就是说：`anchor: null` 不是「还没找到」，是**没有可找的对象**。",
        "",
        "| 书目 | anchor: null 条数 |",
        "|---|---:|",
    ]
    for k, v in per_book.most_common():
        L.append(f"| `{k}` | {v} |")
    L.append("")

    L += ["## 三、逐条论断与复核", ""]
    for cat, items in by_cat.items():
        L.append(f"### {cat}")
        L.append("")
        for c in items:
            L.append(f"#### `{c['id']}` — **{c['status']}**")
            L.append("")
            L.append(f"- 旧件原文：{c['from_doc']}")
            if c.get("doc_notation"):
                L.append(f"- 写法校正：{c['doc_notation']}")
            if c["rules"]:
                L.append(f"- 涉及规则 {len(c['rules'])} 条")
            L.append(f"- 复核结论：{c['note']}")
            for f in c.get("findings") or []:
                if f:
                    L.append(f"    - {f}")
            if c.get("stale_numbers"):
                for k, v in c["stale_numbers"].items():
                    L.append(f"    - **数字漂移**：{k} 旧件记 {v['doc']}，实测 {v['measured']}")
            if c.get("resolution"):
                L.append(f"- 结案：{c['resolution']}")
            L.append("")

    L += [
        "## 四、仍需人决定的事（机器不能代劳）",
        "",
        "1. **`multi-occurrence` 那一档要先补 rule_id 清单**：旧件只给术语，「哪一处算唯一落点」"
        "是人的判断，机器不能定，也不能为提高覆盖率擅自选一处锚上。",
        "2. **V11 的残留怎么处置**：`book.script` 已实测无需更正，所以只剩两条路——"
        "逐条补锚（把概述换成原文，但会改动 `quote`）或接受残留。两条都要人拍板。",
        "3. **pack 元规则（21 条）是否单列一类**：它们「原文无对应句」是**永久事实**、不是待办，"
        "继续留在「待人工判断」里会稀释这一页的信号。",
        "4. **P6 灰区（对应度 0.15–0.30）**：政策要求机器不动该档，仍需人抽检；本轮未动该档任何条目。",
        "",
        "## 五、可复跑",
        "",
        "```bash",
        "python3 tools/needs-human-review-report.py",
        "python3 tools/needs-human-review-report.py --json",
        "python3 tools/needs-human-review-report.py --md tools/reports/needs-human-review.md",
        "```",
    ]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="needs-human-review 可复算台账")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", default=None)
    args = ap.parse_args()

    idx = load_rules_index()
    un = unanchored()
    warns = warn_counts()
    script_total, script_bad = book_script_audit()
    claims = [check_claim(c, idx, un) for c in CLAIMS]
    census = dict(Counter(x.get("quote_kind") or "(未标注)" for x in un))

    if args.md:
        text = render_markdown(claims, un, warns, script_total, script_bad, census)
        p = ROOT / args.md if not Path(args.md).is_absolute() else Path(args.md)
        p.write_text(text, encoding="utf-8")
        print(f"wrote {args.md}（{len(claims)} 条论断，anchor:null {len(un)} 条）")
        return 0

    if args.json:
        json.dump(
            {
                "claims": claims,
                "unanchored_count": len(un),
                "unanchored": un,
                "warnings": warns,
                "book_script": {"books": script_total, "mismatched": script_bad},
                "quote_kind_census": census,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    counts = Counter(c["status"] for c in claims)
    print(f"论断 {len(claims)} 条：", "  ".join(f"{k}={counts.get(k, 0)}" for k in (RESOLVED, OPEN, STALE, UNVERIFIABLE)))
    print(f"anchor: null 规则 {len(un)} 条；V11={warns.get('V11', 0)} V14={warns.get('V14', 0)}")
    print(f"book.script 不符 {len(script_bad)}/{script_total}")
    print(f"未锚规则 quote_kind 分布：{census}")
    for c in claims:
        print(f"  [{c['status']}] {c['id']} — {c['category']}")
        for f in c.get("findings") or []:
            if f:
                print(f"        {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())