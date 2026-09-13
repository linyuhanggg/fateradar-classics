import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { liuyaoAnalysisPoints } from "./src/lib/engine/liuyao-reading";

const lines = (bits: number, movingMask: number): LiuyaoLines =>
  Array.from({ length: 6 }, (_, i) => ({
    yin: (bits >> i) & 1 ? 0 : 1,
    moving: Boolean((movingMask >> i) & 1),
  })) as unknown as LiuyaoLines;

/** instanceId = liuyao:<checkId>:<topic>:<targetId>；targetId 自身可能含冒号。 */
const targetIdOf = (instanceId: string) => instanceId.split(":").slice(3).join(":");

const falsePositive: unknown[] = [];
const targetIdShapes = new Map<string, number>();
let charts = 0;
for (const [dayGanZhi, monthZhi] of [
  ["甲子", "卯"],
  ["丙寅", "午"],
  ["戊辰", "酉"],
  ["庚午", "子"],
] as [string, string][]) {
  for (let bits = 0; bits < 64; bits++) {
    for (const movingMask of [0, 1, 3, 8, 63]) {
      let chart;
      try {
        chart = buildLiuyao({ lines: lines(bits, movingMask), dayGanZhi, monthZhi, useRelative: "世爻" } as never);
      } catch {
        continue;
      }
      charts++;
      const ids = liuyaoAnalysisPoints(chart.analysis).map((p) => String(p.instanceId ?? ""));
      for (const id of ids) {
        const t = targetIdOf(id);
        const shape = /^main:\d+$/.test(t) ? "main:<n>" : t.replace(/:main:\d+$/, ":main:<n>");
        targetIdShapes.set(shape, (targetIdShapes.get(shape) ?? 0) + 1);
      }
      for (let li = 1; li <= 6; li++) {
        for (const id of ids) {
          if (!id.endsWith(`:main:${li}`)) continue;
          const t = targetIdOf(id);
          if (t === `main:${li}`) continue;
          falsePositive.push({ chart: `${dayGanZhi}/${monthZhi}/${bits}/${movingMask}`, line: li, instanceId: id, targetId: t });
        }
      }
    }
  }
}
console.log(
  JSON.stringify(
    {
      tree: process.cwd(),
      charts,
      falsePositiveCount: falsePositive.length,
      sample: falsePositive.slice(0, 10),
      targetIdShapes: [...targetIdShapes.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12),
    },
    null,
    1,
  ),
);
