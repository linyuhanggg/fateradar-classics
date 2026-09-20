#!/usr/bin/env python3
"""tools/eval-executable.py 的语义与不变量测试。

钉住两件事：
  A. **三态语义**（缺输入不得降级成「不满足」；命名定义不得伪装成三态中的任何一个）；
  B. **对照表不许引用不存在的事实**：`FIELD_MAP` 里映射到的 FactKey 必须在
     `fact-vocab.json` 里存在，且属于该 art 引擎实际产出的键（`ART_EMIT_KEYS`）。
     后者正是本轮修过的那类缺陷（声明了引擎不产出的事实却照样算数）。

另钉 executable 层自身的不变量：全库 `verified=true` 为 0。
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/eval-executable.py"

spec = importlib.util.spec_from_file_location("ee", TOOL)
ee = importlib.util.module_from_spec(spec)
sys.modules["ee"] = ee
assert spec.loader is not None
spec.loader.exec_module(ee)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def fact(key, value, **scope):
    return {"key": key, "value": value, "scope": scope, "derivedFrom": ["test"]}


def main() -> int:
    print("A. 三态语义")
    chart = [fact("gan", "甲", layer="本命", pillar="day"), fact("zhi", "寅", layer="本命", pillar="month"),
             fact("keti", "伏吟课", layer="本命"), fact("sanchuan", "初传", layer="本命")]
    present = ee.facts_present(chart)

    check("  equals 命中 → 满足", ee.eval_when({"equals": {"day.gan": "甲"}}, chart, present)[0], "满足")
    check(
        "  equals 不符（字段可判）→ 不满足",
        ee.eval_when({"equals": {"day.gan": "乙"}}, chart, present)[0],
        "不满足",
    )
    check("  all 两真 → 满足",
          ee.eval_when({"all": [{"equals": {"day.gan": "甲"}}, {"equals": {"month.zhi": "寅"}}]}, chart, present)[0], "满足")
    check("  all 一假 → 不满足",
          ee.eval_when({"all": [{"equals": {"day.gan": "甲"}}, {"equals": {"month.zhi": "申"}}]}, chart, present)[0], "不满足")
    check(
        "  all 一真一「接不上」→ 信息不足（不得降级成不满足）",
        ee.eval_when({"all": [{"equals": {"day.gan": "甲"}}, {"exists": "zhifu.palace"}]}, chart, present)[0],
        "信息不足",
    )
    check("  exists 命中 → 满足", ee.eval_when({"exists": "three.chuan"}, chart, present)[0], "满足")
    # `exists` 在字段对应 key **整个缺席** 时只能给「信息不足」：
    # 事实袋里没有这个 key，无法区分「本盘不成立」与「引擎没产出」。
    # 这条口径与谓词层一致，且正是 executable 层 named_gaps 关心的「未知分支必须成立」。
    check(
        "  exists 的 key 整个缺席 → 信息不足（不得当成不满足）",
        ee.eval_when({"exists": "three.chuan"}, [fact("gan", "甲")], {"gan"})[0],
        "信息不足",
    )
    check(
        "  exists 的 key 在场但本盘无匹配 → 仍为满足（exists 只问存在性，不问取值）",
        ee.eval_when({"exists": "three.chuan"}, [fact("sanchuan", "初传")], {"sanchuan"})[0],
        "满足",
    )
    check(
        "  exists 接不上 FactKey → 信息不足",
        ee.eval_when({"exists": "liuyao.structure"}, chart, present)[0],
        "信息不足",
    )
    check("  in 命中 → 满足", ee.eval_when({"in": {"ke.style": ["伏吟课", "返吟课"]}}, chart, present)[0], "满足")
    check(
        "  简写 {字段: [值]} → 满足",
        ee.eval_when({"geju.name": ["正官格"]}, [fact("geju", "正官格", layer="本命")], {"geju"})[0],
        "满足",
    )
    check(
        "  命名定义 → 未提供定义表（不是三态中的任何一个）",
        ee.eval_when({"definition": "辅弼夹帝"}, chart, present)[0],
        "未提供定义表",
    )
    check(
        "  命名定义也不得被当成满足",
        ee.eval_when({"scope": "natal-structure", "definition": "禄马同宫"}, chart, present)[0] == "满足",
        False,
    )
    check(
        "  skyStemIn 接到 tianpan_gan：命中 → 满足",
        ee.eval_when(
            {"skyStemIn": ["乙", "丙", "丁"], "locationBasis": "actual-sky-stem-palace"},
            [fact("tianpan_gan", "丙", layer="本命", gong=3)],
            {"tianpan_gan"},
        )[0],
        "满足",
    )
    check(
        "  skyStemIn 无天盘干事实 → 信息不足",
        ee.eval_when({"skyStemIn": ["乙"], "locationBasis": "actual-sky-stem-palace"}, chart, present)[0],
        "信息不足",
    )

    print("B. 对照表不得引用不存在／不产出的事实")
    vocab = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
    keys = set(vocab["keys"])
    pr_spec = importlib.util.spec_from_file_location("pr2", ROOT / "tools/predicate-report.py")
    prm = importlib.util.module_from_spec(pr_spec)
    assert pr_spec.loader is not None
    pr_spec.loader.exec_module(prm)
    emitted = set().union(*prm.ART_EMIT_KEYS.values())
    bad = [
        f"{name}→{key}"
        for name, (key, _scope, _basis) in ee.FIELD_MAP.items()
        if key is not None and (key not in keys or key not in emitted)
    ]
    check("  FIELD_MAP 的 FactKey 全部存在且被某引擎产出", bad, [])
    check(
        "  前缀映射同理（tenGodFacts.* → shishen）",
        ee.lookup_field("tenGodFacts.正官.layer")[0] in keys and ee.lookup_field("tenGodFacts.正官.layer")[0] in emitted,
        True,
    )
    unmapped = [n for n, (k, _s, _b) in ee.FIELD_MAP.items() if k is None]
    check("  接不上的字段必须写明依据（不得空口）", all(ee.FIELD_MAP[n][2] for n in unmapped), True)

    print("C. 全库运行与 executable 层不变量")
    p = subprocess.run([sys.executable, str(TOOL), "--all", "--json"], cwd=ROOT, capture_output=True, text=True)
    check("  exit", p.returncode, 0)
    data = json.loads(p.stdout)
    check("  包数 15", data["packages"], 15)
    check("  记录数 258", data["records"], 258)
    tally = data["tally"]
    check("  三态 + 未提供定义表 合计 == 记录数", sum(tally.values()), 258)
    check("  verified=true 为 0（全库不变量）", sum(1 for r in data["results"] if r["verified"] is True), 0)
    check("  每条都带出处段落 ID", all(r["source"].get("paragraph_ids") for r in data["results"] if r["source"]), True)
    check(
        "  rescue=unimplemented 条数与报告一致（30）",
        sum(1 for r in data["results"] if r["rescue_unimplemented"]),
        30,
    )
    check(
        "  带 named_gaps 条数与报告一致（31）",
        sum(1 for r in data["results"] if r["has_named_gaps"]),
        31,
    )

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL EXECUTABLE EVAL OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())