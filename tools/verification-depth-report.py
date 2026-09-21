#!/usr/bin/env python3
"""「验证深度」报告：**我的谓词层有多少真的被样盘演示过**（t198）。

## 为什么要测这个

覆盖率只说明「写了谓词」；`--check-art-keys`／死引用扫描只说明「键存在」。
但没有东西回答：**这些谓词里，有多少在任何一张样盘上真的成立过？**

本报告对**口径内已映射**（带锚 + 有谓词）的规则逐条在**本术全部样盘**上求值，分四类：

    · 有满足样本   —— 至少一张样盘判「满足」（**正面演示过**）
    · 全不满足     —— 每张样盘都判「不满足」（条件在样盘里都不成立）
    · 全信息不足   —— 每张样盘都判「信息不足」（**键/取值缺失**）
    · 混合(无满足) —— 有的盘信息不足、有的盘不满足，但没有一张满足

**「全信息不足」应当为 0**：它与死引用扫描（`dead-reference-report.py`）互为独立校验——
若某条谓词的键真的在任何样盘里都没出现，两个工具都该报出来；两者都干净才说明事实层没漏。

## 怎么读「全不满足」

**不等于缺陷**。常见三类，报告里逐条归因：

    · `catalogue-by-value` —— 按取值逐条编排的目录式规则（如六十甲子纳音），
      每条要自己的日柱；要让 60 条都被演示就得 60 张盘。这类另有**结构性自证**
      （t170：复原的干支序列须等于规范六十甲子，无重无漏）。
    · `condition-specific` —— 条件本身很窄（如「日柱为庚辰…」这类枚举），
      样盘不够多自然演示不到。
    · `other` —— 其余，需逐条看。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("pr_vd", ROOT / "tools/predicate-report.py")
pr = importlib.util.module_from_spec(_spec)
sys.modules["pr_vd"] = pr
assert _spec.loader is not None
_spec.loader.exec_module(pr)

_spec2 = importlib.util.spec_from_file_location("ev_vd", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(_spec2)
sys.modules["ev_vd"] = ev
assert _spec2.loader is not None
_spec2.loader.exec_module(ev)

# 目录式编排的规则前缀（按取值逐条排的，逐条要自己的盘）
CATALOGUE_PREFIXES = ("LIXUZHONGMIN-", "SANMINGTONGH-R-", "LX-")

DUMP = ROOT / "tools/reports/facts-sample.json"


def classify(rule: dict, cases: dict) -> str:
    verdicts = [ev.evaluate(rule, c["facts"])["verdict"] for c in cases.values()]
    if "满足" in verdicts:
        return "有满足样本"
    if all(v == "不满足" for v in verdicts):
        return "全不满足"
    if all(v == "信息不足" for v in verdicts):
        return "全信息不足"
    return "混合(无满足)"


def why(rule_id: str) -> str:
    return "catalogue-by-value" if rule_id.startswith(CATALOGUE_PREFIXES) else "other-or-condition-specific"


def report() -> dict:
    dump = json.loads(DUMP.read_text(encoding="utf-8"))
    per: dict[str, Counter] = defaultdict(Counter)
    undemonstrated: list[dict] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        book = data.get("book") or {}
        art = pr.art_of(book.get("system"), book.get("slug"))
        if art not in ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng"):
            continue
        cases = dump.get(art) or {}
        if not cases:
            continue
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or not rule.get("applicable_to"):
                continue
            if not isinstance(rule.get("anchor"), dict):
                continue          # 只算口径内的已映射规则
            kind = classify(rule, cases)
            per[art][kind] += 1
            if kind != "有满足样本":
                undemonstrated.append(
                    {"art": art, "rule_id": rule["rule_id"], "kind": kind, "why": why(rule["rule_id"])}
                )
    total = Counter()
    for c in per.values():
        total.update(c)
    return {
        "report": "验证深度：口径内已映射规则在本术样盘上的三态分布",
        "generated_by": "t198",
        "method": "对每条『带锚 + 有谓词』的规则，在本术**全部**样盘上求值并归类；样盘取自 tools/reports/facts-sample.json。",
        "per_art": {a: dict(c) for a, c in per.items()},
        "total": dict(total),
        "mapped": sum(total.values()),
        "demonstrated": total["有满足样本"],
        "undemonstrated": sum(total.values()) - total["有满足样本"],
        "undemonstrated_by_why": dict(Counter(x["why"] for x in undemonstrated)),
        "entries": undemonstrated,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="验证深度报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = report()
    if args.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return 0
    print(f"口径内已映射 {r['mapped']} 条；**有满足样本** {r['demonstrated']} 条"
          f"（{r['demonstrated'] / r['mapped'] * 100:.0f}%）；未被任何样本满足 {r['undemonstrated']} 条")
    print("（「全信息不足」应恒为 0：它与死引用扫描互为独立校验）")
    print()
    print(f"{'art':8} {'已映射':>6} {'有满足':>6} {'全不满足':>8} {'全信息不足':>10} {'混合':>5}")
    for art in ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng"):
        c = r["per_art"].get(art) or {}
        n = sum(c.values())
        print(f"{art:8} {n:6} {c.get('有满足样本', 0):6} {c.get('全不满足', 0):8} {c.get('全信息不足', 0):10} {c.get('混合(无满足)', 0):5}")
    print(f"\n未被满足的归因: {r['undemonstrated_by_why']}")
    if r["total"].get("全信息不足"):
        print("⚠ 出现「全信息不足」——与死引用扫描不一致，需排查", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())