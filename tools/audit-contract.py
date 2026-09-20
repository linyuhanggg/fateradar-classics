#!/usr/bin/env python3
"""贯穿契约的跨提交审计：**证明这十几轮只动了 `applicable_to`**。

任务书的贯穿契约是「不编造、可溯源、原文没写就不写」，并且明确「不做」四件事
（不虚构反例凑三态／不把未实现救应写成没有救应／不硬锚／不生成让 verified 变 true 的自我认定）。
本脚本把其中**可机器验证**的部分钉成一条命令：

1. **受保护字段零改动**：以某基线的每个 `rules.yaml` 为准，逐规则比对
   `statement` / `quote` / `anchor` / `verified` / `verified_by` / `verified_at` /
   `caveats` / `school` / `kind` / `rule_id` 与 `book` 块 —— 要求**逐字相同**。
2. **规则集合零变动**：不新增、不删除规则。
3. **`verified: true` 全库为 0**（电子锚定不能自动提升核验）。
4. **可溯源**：每一条 `applicable_to` 变动都必须能在**判定台账**里找到出处；
   台账的谓词还要与**当前文件**一致（不是自报）。
   台账有三种形态，各配适配器：
   - `map-*.json` 的 `applicable_to_yaml`（直接比对）
   - `nayin-ganzhi-map.json` 的 `gan`/`zhi`（按固定模板重建后比对）
   - `predicate-decisions/*.json` 的 `decision == "mapped"`（t168 逐条判定台账，
     扣除 `captain-audit.json` 里复核撤回的条目）

    python3 tools/audit-contract.py                      # 默认对 t168 之前的基线
    python3 tools/audit-contract.py --base <ref> --json
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
# t168 之前的基线（谓词施工起点）。此后所有 applicable_to 变动都应能在这里被审计出来。
DEFAULT_BASE = "cd41f5b"
PROTECTED = (
    "statement",
    "quote",
    "anchor",
    "verified",
    "verified_by",
    "verified_at",
    "caveats",
    "school",
    "kind",
    "rule_id",
)
REVERTED = {"DITIANSUICHA-DR-07", "TAIWEIFU-021", "ZIWEIDOUSHUQ-ZW-04", "ZR-04", "HZL-R001"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def load_rules(rel: str, *, ref: str | None = None) -> dict:
    """`rel` 必须是**工作区相对路径**。

    ⚠ 初版这里传了绝对路径（`ROOT / f`），于是 `git show <ref>:/abs/path` 取不到内容、
    基线被当成空文件，审计结果全盘失真（报「55 份 book 块都变了、新增 1356 条规则」）。
    本函数因此只接受相对路径，并在取不到内容时**直接报错**而不是静默返回空。
    """
    if ref:
        text = git("show", f"{ref}:{rel}")
        if not text.strip():
            raise SystemExit(f"git show {ref}:{rel} 无内容——基线引用或路径不对")
    else:
        text = (ROOT / rel).read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}


def rules_yaml_files(ref: str) -> list[str]:
    out = git("ls-tree", "-r", "--name-only", ref, "--", "references/books").split()
    return [f for f in out if f.endswith("/rules.yaml")]


def nayin_predicate(gan: str, zhi: str) -> dict:
    """t170 李虚中六十甲子：固定模板。"""
    return {
        "all_of": [
            {"key": "gan", "value": gan},
            {"key": "zhi", "value": zhi},
        ],
        "same": "pillar",
    }


def load_trace() -> dict[str, list[tuple[str, dict | None]]]:
    """rule_id → [(来源, 期望谓词|None)]。期望为 None 表示该台账不携带谓词字符串。"""
    trace: dict[str, list[tuple[str, dict | None]]] = {}
    for f in sorted(glob.glob(str(ROOT / "tools/reports/*map*.json"))):
        name = Path(f).name
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for x in (data if isinstance(data, list) else data.get("entries") or []):
            if not isinstance(x, dict) or not x.get("rule_id"):
                continue
            y = x.get("applicable_to_yaml")
            if isinstance(y, str):
                trace.setdefault(x["rule_id"], []).append((name, yaml.safe_load(y)))
            elif x.get("gan") and x.get("zhi"):
                trace.setdefault(x["rule_id"], []).append((name, nayin_predicate(x["gan"], x["zhi"])))
    # v3 升级时的**语义变动**登记（形态：entries[*].rule_id，携带 before/after 而非谓词字符串）
    mig = ROOT / "tools/reports/v3-language-migrations.json"
    if mig.is_file():
        for x in json.loads(mig.read_text(encoding="utf-8")).get("entries") or []:
            if isinstance(x, dict) and x.get("rule_id"):
                trace.setdefault(x["rule_id"], []).append((mig.name, None))
    for f in sorted(glob.glob(str(ROOT / "tools/reports/predicate-decisions/*.json"))):
        if "captain-audit" in Path(f).name:
            continue
        data = json.loads(Path(f).read_text(encoding="utf-8"))
        for x in data.get("decisions") or []:
            if x.get("decision") == "mapped" and x.get("rule_id") not in REVERTED:
                trace.setdefault(x["rule_id"], []).append((Path(f).name, None))
    return trace


def main() -> int:
    ap = argparse.ArgumentParser(description="贯穿契约的跨提交审计")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    # 基线引用必须**先验证**：`git ls-tree <坏引用>` 返回空，于是「没有文件 → 没有违规」
    # → 审计静默通过。这是比误报更危险的失效模式（一条永不说坏的审计＝没有审计），
    # 所以这里显式挡掉，并由 test-audit-contract.py 的反例 C 钉住。
    if subprocess.run(["git", "rev-parse", "--verify", f"{args.base}^{{commit}}"], cwd=ROOT,
                      capture_output=True, text=True).returncode != 0:
        raise SystemExit(f"基线引用不存在：{args.base}")
    files = rules_yaml_files(args.base)
    if not files:
        raise SystemExit(f"基线 {args.base} 下取不到任何 rules.yaml——基线引用或路径不对")
    viol: list[str] = []
    changed: dict[str, str] = {}
    added: list[str] = []
    removed: list[str] = []
    total_rules = 0
    for f in files:
        p = ROOT / f
        if not p.is_file():
            viol.append(f"{f}: 文件已删除")
            continue
        old = load_rules(f, ref=args.base)
        new = load_rules(f)
        if old.get("book") != new.get("book"):
            viol.append(f"{f}: book 块变了")
        om = {r["rule_id"]: r for r in old.get("rules") or [] if isinstance(r, dict)}
        nm = {r["rule_id"]: r for r in new.get("rules") or [] if isinstance(r, dict)}
        total_rules += len(nm)
        for rid in om:
            if rid not in nm:
                removed.append(rid)
                continue
            for k in PROTECTED:
                if om[rid].get(k) != nm[rid].get(k):
                    viol.append(f"{f}: {rid}.{k} 变了")
            if om[rid].get("applicable_to") != nm[rid].get("applicable_to"):
                changed[rid] = f
        added.extend(rid for rid in nm if rid not in om)

    trace = load_trace()
    untraced = sorted(r for r in changed if r not in trace)
    # 先把当前树的「规则 → applicable_to」建一次索引：初版把它写在双层循环里
    # （每条台账 × 每个文件都重新解析一次 YAML），审计一次要几分钟，
    # 直接被 test-audit-contract.py 的超时抓到。
    live_map: dict[str, object] = {}
    for f in files:
        for r in load_rules(f).get("rules") or []:
            if isinstance(r, dict):
                live_map.setdefault(r["rule_id"], r.get("applicable_to"))
    mismatched: list[str] = []
    for rid, entries in trace.items():
        if rid not in changed:
            continue
        live = live_map.get(rid)
        for src, expect in entries:
            if expect is not None and expect != live:
                mismatched.append(f"{rid}（{src}）台账谓词与当前文件不一致")

    verified_true = 0
    for f in git("ls-files", "--", "references/books").split():
        if f.endswith("/rules.yaml"):
            verified_true += len(re.findall(r"(?m)^\s*verified:\s*true", (ROOT / f).read_text(encoding="utf-8")))

    report = {
        "base": args.base,
        "files": len(files),
        "rules": total_rules,
        "protected_violations": viol,
        "rules_added": added,
        "rules_removed": removed,
        "applicable_to_changed": len(changed),
        "untraced_changes": untraced,
        "ledger_mismatches": mismatched,
        "verified_true_lines": verified_true,
    }
    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"基线 {args.base} → HEAD：{len(files)} 份 rules.yaml，{total_rules} 条规则")
        print(f"  受保护字段违规        : {len(viol)}")
        for v in viol[:10]:
            print(f"      {v}")
        print(f"  新增／删除规则        : {len(added)} / {len(removed)}")
        print(f"  applicable_to 净变动  : {len(changed)}")
        print(f"  其中无台账出处        : {len(untraced)} {untraced[:8]}")
        print(f"  台账谓词与文件不一致  : {len(mismatched)} {mismatched[:5]}")
        print(f"  verified: true 行数   : {verified_true}")

    bad = bool(viol or added or removed or untraced or mismatched or verified_true)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())