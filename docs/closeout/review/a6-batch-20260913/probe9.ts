/** t8 追加：盘级规则点是否在逐爻焦点里全数回来（ZSB-E-09/E-14/E-16/E-17）+ 锚点分布。 */
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";

const linesOf = (bits: number, movingMask: number): LiuyaoLines =>
  Array.from({ length: 6 }, (_, i) => ({
    yin: (bits >> i) & 1 ? 0 : 1,
    moving: Boolean((movingMask >> i) & 1),
  })) as unknown as LiuyaoLines;

const WATCH = ["ZSB-E-09", "ZSB-E-14", "ZSB-E-16", "ZSB-E-17"];
const triggered: Record<string, number> = Object.fromEntries(WATCH.map((w) => [w, 0]));
let charts = 0;
let lineCases = 0;
const violations: unknown[] = [];
let summaryIsOnlyUnanchored = 0;
let lineCasesWithUnanchoredNotSummary = 0;

for (const [dayGanZhi, monthZhi] of [
  ["甲子", "卯"],
  ["丙寅", "午"],
  ["戊辰", "酉"],
  ["庚午", "子"],
  ["壬申", "辰"],
] as [string, string][]) {
  for (let bits = 0; bits < 64; bits++) {
    for (const movingMask of [0, 1, 3, 8, 63]) {
      let chart;
      try {
        chart = buildLiuyao({ lines: linesOf(bits, movingMask), dayGanZhi, monthZhi, useRelative: "世爻" } as never);
      } catch {
        continue;
      }
      charts++;
      const ov = buildLiuyaoFreeReading(chart);
      const ovIds = ov.points.map((p) => String(p.instanceId ?? p.id));
      const ovSet = new Set(ovIds);
      for (const w of WATCH) if (ovIds.some((id) => id.includes(w))) triggered[w]!++;
      for (let li = 0; li < 6; li++) {
        lineCases++;
        const focus = buildLiuyaoFreeReading(chart, { lineIndex: li });
        const ids = new Set(focus.points.map((p) => String(p.instanceId ?? p.id)));
        const missing = [...ovSet].filter((id) => id !== "liuyao:free:overview" && !ids.has(id));
        if (missing.length) violations.push({ chart: `${dayGanZhi}/${monthZhi}/${bits}/${movingMask}`, li, missing: missing.slice(0, 4) });
        const unanchored = focus.points.filter((p) => !(p.source && p.sourceRevision)).map((p) => String(p.id));
        if (unanchored.length === 1 && unanchored[0] === `liuyao-free-${"line"}`) summaryIsOnlyUnanchored++;
        else if (unanchored.some((id) => !/^liuyao-free-(line|overview)$/.test(String(id)))) lineCasesWithUnanchoredNotSummary++;
      }
    }
  }
}

console.log(JSON.stringify({ tree: process.cwd(), charts, lineCases, triggered, violationCases: violations.length, sample: violations.slice(0, 5), summaryIsOnlyUnanchored, lineCasesWithUnanchoredNotSummary }, null, 1));
