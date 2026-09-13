import { buildZiwei } from "./src/lib/engine/ziwei";
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { liuyaoAnalysisPoints } from "./src/lib/engine/liuyao-reading";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };
const subject = {
  ...subjectOf({ ...place, year: 1990, month: 1, day: 20, hour: 13, minute: 20 }),
  timeBasis: "clock" as const,
};

/* (a) 不可用层的精确 scope 表 */
const scopesFor = (date: string) =>
  (buildZiwei(subject, date, 12).transit?.scopes ?? []).map((s) => `${s.name}:${s.available ? "available" : "UNAVAILABLE"}`);
const ziwei = {
  "1920-01-15": scopesFor("1920-01-15"),
  "1960-07-15": scopesFor("1960-07-15"),
  "2024-06-01": scopesFor("2024-06-01"),
};

/* (b) 六爻 instanceId 后缀碰撞：`:main:N` 是否为某些 targetId 的后缀 */
const lines = (bits: number, movingMask: number): LiuyaoLines =>
  Array.from({ length: 6 }, (_, i) => ({
    yin: (bits >> i) & 1 ? 0 : 1,
    moving: Boolean((movingMask >> i) & 1),
  })) as unknown as LiuyaoLines;

const collisions: unknown[] = [];
let charts = 0;
for (const [dayGanZhi, monthZhi] of [
  ["甲子", "卯"],
  ["丙寅", "午"],
  ["戊辰", "酉"],
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
      for (let li = 1; li <= 6; li++) {
        const matched = ids.filter((id) => id.endsWith(`:main:${li}`));
        for (const id of matched) {
          // 该 id 的 targetId 是否为 `main:${li}` 本身？（instanceId = liuyao:<check>:<topic>:<targetId>）
          const targetPart = id.slice(id.indexOf(":") + 1);
          if (!/(^|:)([a-z-]+:)?main:\d+$/.test(targetPart) || targetPart.includes("→")) continue;
          if (!targetPart.endsWith(`main:${li}`) || targetPart === `main:${li}`) continue;
          collisions.push({ key: `${dayGanZhi}/${monthZhi}/${bits}/${movingMask}`, line: li, instanceId: id });
        }
      }
    }
  }
}
console.log(
  JSON.stringify(
    { tree: process.cwd(), ziwei, liuyao: { charts, collisionCount: collisions.length, sample: collisions.slice(0, 8) } },
    null,
    1,
  ),
);
