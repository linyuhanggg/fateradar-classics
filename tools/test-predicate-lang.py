#!/usr/bin/env python3
"""tools/predicate_lang.py 的回归测试。

这个模块存在的唯一理由：**只按 `isinstance(x, list)` 判断的旧代码会把 v3 组读成「没有谓词」**，
于是覆盖率少算、未映射报告多算，而且没有任何报错。这里把该行为钉死。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from predicate_lang import has_predicates, iter_predicates, iter_usable_predicates, leaf_count  # noqa: E402

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}: {got!r}")


LEGACY = [{"key": "bamen", "value": "休门"}, {"key": "bashen", "value": "九天"}]
GROUP = {
    "any_of": [
        {"all_of": [{"key": "bamen", "value": "休门", "scope": {"gong": 9}}]},
        {"all_of": [{"key": "bamen", "value": "伤门", "scope": {"gong": 2}}]},
    ],
    "none_of": [{"key": "kongwang", "value": "*"}],
}
CO_LOCATION = {
    "all_of": [{"key": "ziwei_star", "value": "禄存"}, {"key": "ziwei_star", "value": "天马"}],
    "same": "palace",
}


def main() -> int:
    print("1. 旧平铺列表")
    check("  叶子数", leaf_count(LEGACY), 2)
    check("  有谓词", has_predicates(LEGACY), True)
    check("  空列表没有谓词", has_predicates([]), False)

    print("2. v3 组（旧代码在这里会读成「空」）")
    check("  叶子数", leaf_count(GROUP), 3)
    check("  有谓词（这正是旧 isinstance(list) 判断漏掉的）", has_predicates(GROUP), True)
    check("  嵌套 all_of 也被走到底", leaf_count(CO_LOCATION), 2)
    check("  none_of 里的叶子同样计入", [p["key"] for p in iter_predicates(GROUP)].count("kongwang"), 1)

    print("3. 无谓词形态")
    check("  None", has_predicates(None), False)
    check("  空 mapping", has_predicates({}), False)
    check("  same-only mapping（非法但不应崩）", leaf_count({"same": "palace"}), 0)

    print("4. 与真实规则库对账：v3 组必须被报告计入")
    yaml_path = ROOT / "references/books/san-shi/qimen-dunjia-tongzhi/rules.yaml"
    rules = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))["rules"]
    by_id = {r["rule_id"]: r for r in rules}
    qmp37 = by_id.get("QM-P37")
    if qmp37 is None:
        FAILED.append("QM-P37 不在 qimen-dunjia-tongzhi")
        print("  FAIL QM-P37 缺失")
    else:
        check("  QM-P37 用组形声明谓词", has_predicates(qmp37.get("applicable_to")), True)
        check("  QM-P37 叶子数（八组门+宫）", leaf_count(qmp37.get("applicable_to")), 8)
        # 覆盖率报告必须与之一致，否则就是又回到「组形隐形」的老毛病。
        import subprocess

        out = subprocess.run(
            [sys.executable, str(ROOT / "tools/predicate-report.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        payload = json.loads(out.stdout)
        check("  predicate-report 把组形规则计入 with_predicates（qimen ≥ 8）",
              payload["arts"]["qimen"]["with_predicates"] >= 8, True)

    print("5. iter_usable_predicates 过滤不完整叶子")
    check("  缺 value 的叶子不算可用", leaf_count([{"key": "bamen"}, {"key": "bamen", "value": "休门"}]), 1)

    print("6. 导出层不得静默丢掉组形（export-rules.py 的 predicates_of）")
    import importlib.util

    spec = importlib.util.spec_from_file_location("export_rules", ROOT / "tools/export-rules.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    check("  旧形导成 predicate 数组", mod.predicates_of({"applicable_to": LEGACY}), LEGACY)
    got = mod.predicates_of({"applicable_to": CO_LOCATION})
    check("  组形按原结构导出（不是 []）", got, CO_LOCATION)
    check("  topic_of 能穿透组形取标签", mod.topic_of({"applicable_to": CO_LOCATION}), "禄存 · 天马")

    dist = ROOT / "dist/rules/qimen.json"
    if dist.is_file():
        exported = {r["ruleId"]: r for r in json.loads(dist.read_text(encoding="utf-8"))}
        qm = exported.get("QM-P37") or {}
        ap = qm.get("applicableTo")
        check("  dist 里 QM-P37 的 applicableTo 不是空", bool(ap), True)
        check("  dist 里保留 any_of/all_of 结构", isinstance(ap, dict) and "any_of" in ap, True)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL PREDICATE-LANG OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())