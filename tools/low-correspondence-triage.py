#!/usr/bin/env python3
"""低对应度分诊：把「对应度极低」的规则分成三类，并给出证据（t202）。

## 为什么不能只看对应度

`correspondence(statement, quote)` 是**汉字集合的召回率**（见 `validate-rules.py`）。
它对两类完全正常的情形会误报：

- quote 是**表格／取法条**（如「寅午戌人在戌…」），statement 是「华盖主孤高僧道」——
  主题相关，但字面零重叠；
- quote 只是 statement 所概括的**其中一句**（长综述 + 短引文）。

而它真正该报的是：**anchor 指向了不相干的段落**（例如 `SANMINGTONGH-018`「子午丑未…相冲」
的 quote 却是「正月節 二月節 三月節」）。

## 分诊办法

对每条低对应度规则，把 statement 的**内容字集合**分别与三处比对：

  1. **锚点邻域**（anchor 行 ±30 行）——命中高 → 引文就在附近，**判据误报**（`metric-artifact`）；
  2. **同一文件其它位置**——命中高 → anchor 落点偏了，**给出正确位置**（`anchor-elsewhere`）；
  3. **全库其它文件**——命中高 → 该命题的正文在别处，**给出候选文件与行**（`anchor-elsewhere`）；
  4. 三处都低 → statement 很可能是**现代概括／元数据／包级声明**，不是书里的句子
     （`not-source-text`）。

## ⚠ 实读验证：**这三类都不能当结论用**

t202 我按单字版跑出「`GUOTIANJING-007` anchor 疑应移到 L7891（覆盖 0.52）」，
**读过去发现那一处讲的是「入庙乘旺乐宫」，与 statement 的「童限」毫无关系**——
单字集合在中文里几乎必然重叠（星/宫/之…），0.52 是巧合。
改用**二元组**后仍有 9 条被判「同文件另有更匹配的窗口」，逐条读过去多半也是
**韵语引文 vs 白话归纳**造成的结构性低重叠，不是锚点错位。

**结论**：字符串方法（单字／二元组）**判不了锚点对不对**。
本工具因此只作为**分诊线索 + 读单**：它列出「对应度极低」的规则及其锚点、引文、statement，
供**人眼扫读**；三类标签请当线索看，不要当判定。

**本工具只产出「提议」，不改任何受保护字段**（`statement`/`quote`/`anchor` 一律不动，
由 `audit-contract.py` 把关）。人要改的是 anchor，不是让机器去硬锚。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("vr_lc", ROOT / "tools/validate-rules.py")
vr = importlib.util.module_from_spec(_spec)
sys.modules["vr_lc"] = vr
assert _spec.loader is not None
_spec.loader.exec_module(vr)

CJK = re.compile(r"[\u4e00-\u9fff]")
WINDOW = 30
THRESHOLD = 0.05
# 「判据误报」的判定线：邻域内容字覆盖率
NEAR_HIT = 0.30


def content_chars(text: str) -> set[str]:
    return set(CJK.findall(vr.fold_han(text or "")))


def content_bigrams(text: str) -> set[str]:
    """**内容二元组**。单字集合在中文里几乎必然重叠（星/宫/之…），
    于是「字面覆盖」会把毫不相干的段落判成相关——t202 实读验证过这一点
    （`GUOTIANJING-007` 被 L7891 的 0.52 命中，读过去却是「入庙乘旺乐宫」，
    与 statement 的「童限」毫无关系）。二元组能滤掉这类巧合。"""
    han = "".join(CJK.findall(vr.fold_han(text or "")))
    return {han[i : i + 2] for i in range(len(han) - 1)}


def load_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def coverage(chars: set[str], text: str) -> float:
    """内容**二元组**覆盖率（单字版会因常用字而误判，故用二元组）。"""
    if not chars:
        return 1.0
    return len(chars & content_bigrams(text)) / len(chars)


def best_in_file(chars: set[str], lines: list[str], exclude: tuple[int, int] | None = None) -> tuple[float, int]:
    """文件内最佳窗口命中（可排除给定行区间）。返回 (覆盖率, 起始行号)。"""
    best = (0.0, 0)
    for start in range(0, max(1, len(lines)), WINDOW):
        if exclude and exclude[0] - WINDOW <= start <= exclude[1]:
            continue
        cov = coverage(chars, "\n".join(lines[start : start + WINDOW]))
        if cov > best[0]:
            best = (cov, start + 1)
    return best


def triage(threshold: float = THRESHOLD) -> list[dict]:
    # 预读全部全文（缓存折叠所需原文，避免逐行重复 IO）
    fulltext: dict[str, list[str]] = {}
    out: list[dict] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        book = data.get("book") or {}
        book_id = f"{book.get('system')}/{book.get('slug')}"
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            stmt, quote = rule.get("statement") or "", rule.get("quote") or ""
            anchor = rule.get("anchor") or {}
            if not stmt or not quote or not anchor.get("file"):
                continue
            corr = vr.correspondence(stmt, quote)
            if corr >= threshold:
                continue
            chars = content_bigrams(stmt)
            rel = str(anchor["file"])
            fpath = ROOT / rel
            if rel not in fulltext:
                fulltext[rel] = load_lines(fpath)
            lines = fulltext[rel]
            start = int(anchor.get("start_line") or 1)
            end = int(anchor.get("end_line") or start)
            near = coverage(chars, "\n".join(lines[max(0, start - 1 - WINDOW) : end + WINDOW]))
            elsewhere_cov, elsewhere_line = best_in_file(chars, lines, exclude=(start, end))
            # 标签**只是线索**（见文件头：实读已证不可当判定）。
            kind = (
                "near-anchor"
                if near >= NEAR_HIT
                else ("higher-overlap-window-found" if max(elsewhere_cov, near) >= NEAR_HIT else "no-overlap-anywhere")
            )
            entry = {
                "book": book_id,
                "rule_id": rule.get("rule_id"),
                "correspondence": round(corr, 3),
                "anchor": {"file": rel, "start_line": start, "end_line": end},
                "near_coverage": round(near, 3),
                "same_file_best": {"coverage": round(elsewhere_cov, 3), "start_line": elsewhere_line},
                "kind": kind,
                "statement_head": stmt[:60],
                "quote_head": quote[:60],
            }
            entry["proposal"] = (
                "**请人眼读一遍**：statement 是不是现代归纳/包级声明？引文主题与它是否同一件事？"
                "字符串指标（单字/二元组）判不了这一层——t202 已用实读证过。"
            )
            out.append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="低对应度分诊（只提议，不改受保护字段）")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true", help="写入 tools/reports/low-correspondence-triage.json")
    args = ap.parse_args()
    rows = triage(args.threshold)
    kinds = Counter(r["kind"] for r in rows)
    payload = {
        "report": "低对应度分诊",
        "generated_by": "t202",
        "method": (
            "correspondence() 是汉字集合召回率，对「表格型引文」与「长综述+短引文」会误报。"
            "本报告用**内容二元组**做覆盖（单字会因常用字而误判，t202 实读验证过）。"
            "本报告以 statement 的内容字分别比锚点邻域(±30 行)、同文件其它窗口、其它文件，"
            "分三类并给出证据；**只提议，不改 statement/quote/anchor**。"
        ),
        "threshold": args.threshold,
        "counts": dict(kinds),
        "entries": rows,
    }
    if args.write:
        out = ROOT / "tools/reports/low-correspondence-triage.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"写入 {out.relative_to(ROOT)}：{len(rows)} 条")
    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return 0
    print(f"对应度 < {args.threshold} 的规则：{len(rows)} 条")
    for k, v in kinds.most_common():
        print(f"   {v:4}  {k}")
    print()
    print("（标签只是线索；读单如下，供人眼扫读）")
    for r in rows:
        print(f"  [{r['kind']:26}] {r['rule_id']:20} stmt={r['statement_head'][:36]!r}")
        print(f"      quote={r['quote_head'][:40]!r}  @{r['anchor']['file'].split('/')[-2]}:L{r['anchor']['start_line']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())