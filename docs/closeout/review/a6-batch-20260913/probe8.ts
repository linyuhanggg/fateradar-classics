import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";

const lines = (symbols: string): LiuyaoLines =>
  [...symbols].map((symbol) => ({
    yin: symbol === "阳" || symbol === "○" ? 1 : 0,
    moving: symbol === "○" || symbol === "ㄨ",
  })) as unknown as LiuyaoLines;

const chart = buildLiuyao({
  lines: lines("○阴阴阴阴阴"),
  dayGanZhi: "甲子",
  monthZhi: "卯",
  useRelative: "世爻",
} as never);

const summarize = (points: readonly { instanceId?: string; id?: string; source?: unknown; sourceRevision?: string }[]) => ({
  count: points.length,
  anchored: points.filter((p) => p.source && p.sourceRevision).length,
  ids: points.map((p) => String(p.instanceId ?? p.id)),
});

const overview = buildLiuyaoFreeReading(chart);
const out: Record<string, unknown> = { overview: summarize(overview.points) };
for (let i = 0; i < 6; i++) out[`line${i}`] = summarize(buildLiuyaoFreeReading(chart, { lineIndex: i }).points);
out["missing"] = summarize(buildLiuyaoFreeReading(chart, { lineIndex: 9 }).points);
console.log(JSON.stringify({ tree: process.cwd(), out }, null, 1));
