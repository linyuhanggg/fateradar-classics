/**
 * 独立 A/B 探针（reviewer / t8）。在 a6-head（HEAD 00e98fc）与 a6-wt（工作树 A6 修改）两棵树上各跑一次，
 * 输出同一份 JSON 结构，由外部脚本比对。只读：不写任何仓库文件。
 */
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";
import { buildZiwei } from "./src/lib/engine/ziwei";
import { buildZiweiFreeReading } from "./src/lib/engine/ziwei-free-reading";
import { palaceReadingOf } from "./src/lib/engine/ziwei-reading";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };

/* ---------------- 六爻 ---------------- */
const linesOf = (bits: number, movingMask: number): LiuyaoLines =>
  Array.from({ length: 6 }, (_, i) => ({
    yin: (bits >> i) & 1 ? 0 : 1, // 1 = 阳, 0 = 阴
    moving: Boolean((movingMask >> i) & 1),
  })) as unknown as LiuyaoLines;

const ganZhiPairs: [string, string][] = [
  ["甲子", "卯"],
  ["丙寅", "午"],
  ["戊辰", "酉"],
  ["庚午", "子"],
  ["壬申", "辰"],
];

type LiuyaoRow = {
  key: string;
  overviewCount: number;
  overviewIds: string[];
  overviewAnchored: number;
  overviewBogusOwnId: number;
  line: {
    lineIndex: number;
    count: number;
    anchored: number;
    dupIds: number;
    missingFromOverview: string[];
    hasMainPoint: boolean;
    bogusOwnId: number;
  }[];
};

const liuyaoRows: LiuyaoRow[] = [];
for (const [dayGanZhi, monthZhi] of ganZhiPairs) {
  for (let bits = 0; bits < 64; bits++) {
    for (const movingMask of [0, 1, 3, 8, 63]) {
      const key = `${dayGanZhi}/${monthZhi}/${bits}/${movingMask}`;
      let chart;
      try {
        chart = buildLiuyao({ lines: linesOf(bits, movingMask), dayGanZhi, monthZhi, useRelative: "世爻" } as never);
      } catch {
        continue;
      }
      const overview = buildLiuyaoFreeReading(chart);
      const ovIds = overview.points.map((p) => String(p.instanceId ?? p.id));
      const ovSet = new Set(ovIds);
      const ovAnchored = overview.points.filter((p) => p.source && p.sourceRevision).length;
      const bogus = (points: typeof overview.points) =>
        points.filter((p) => {
          const own = String(p.id ?? "");
          if (!/^liuyao-free-/.test(own)) return false;
          return (p.ruleIds ?? []).includes(own) || (p.paragraphIds ?? []).includes(own);
        }).length;
      const row: LiuyaoRow = {
        key,
        overviewCount: overview.points.length,
        overviewIds: ovIds,
        overviewAnchored: ovAnchored,
        overviewBogusOwnId: bogus(overview.points),
        line: [],
      };
      for (let li = 0; li < 6; li++) {
        const focus = buildLiuyaoFreeReading(chart, { lineIndex: li });
        const ids = focus.points.map((p) => String(p.instanceId ?? p.id));
        const idSet = new Set(ids);
        row.line.push({
          lineIndex: li,
          count: focus.points.length,
          anchored: focus.points.filter((p) => p.source && p.sourceRevision).length,
          dupIds: ids.length - idSet.size,
          missingFromOverview: [...ovSet].filter(
            (id) => id !== "liuyao:free:overview" && !idSet.has(id),
          ),
          hasMainPoint: idSet.has(`liuyao:free:main:${li + 1}`),
          bogusOwnId: bogus(focus.points),
        });
      }
      liuyaoRows.push(row);
    }
  }
}

/* ---------------- 紫微 ---------------- */
const subject = { ...subjectOf({ ...place, year: 1990, month: 1, day: 20, hour: 13, minute: 20 }), timeBasis: "clock" as const };
const viewDates = [
  "1990-01-20", "1995-06-01", "2000-03-15", "2005-09-09", "2010-12-31",
  "2015-07-07", "2020-02-29", "2024-06-01", "2028-11-11", "2035-04-04",
];
const palaces = ["命宫", "事业", "夫妻"];

type ZiweiCase = {
  date: string;
  palace: string;
  scopes: { name: string; available: boolean; ganzhi: string }[];
  requested: string | null;
  text: string;
  facts: string[];
  /** 正文点名的运限层名（"当前运限层X<ganzhi>" 的 X）；无＝未叠层 */
  textLayer: string | null;
  expectedOverlay: { scopeName: string; ganzhi: string; stars: string; mutagens: string[] } | null;
};
const ziweiCases: ZiweiCase[] = [];

for (const date of viewDates) {
  const chart = buildZiwei(subject, date, 12);
  const scopes = (chart.transit?.scopes ?? []).map((s) => ({
    name: s.name,
    available: s.available,
    ganzhi: s.ganzhi,
  }));
  for (const palace of palaces) {
    const pr = palaceReadingOf(chart, palace);
    const overlays = pr.transitOverlays;
    const requests: (string | null)[] = [
      null,
      "__bogus__",
      ...scopes.map((s) => s.name),
    ];
    for (const requested of requests) {
      const focus: { palace: string; scope?: string } = { palace };
      if (requested && requested !== "__bogus__") focus.scope = requested;
      const free = buildZiweiFreeReading(chart, focus);
      const text = free.paragraphs.join("");
      const m = /当前运限层(.+?)([\u4e00-\u9fa5]{2})叠在本宫/.exec(text);
      const expected =
        requested && requested !== "__bogus__"
          ? (overlays.find((o) => o.scopeName === requested && o.available) ?? null)
          : null;
      ziweiCases.push({
        date,
        palace,
        scopes,
        requested,
        text,
        facts: [...(free.points[0]?.usedFacts ?? [])],
        textLayer: m ? m[1]! : null,
        expectedOverlay: expected
          ? {
              scopeName: expected.scopeName,
              ganzhi: expected.ganzhi,
              stars: expected.stars,
              mutagens: [...expected.mutagens],
            }
          : null,
      });
    }
  }
}

console.log(
  JSON.stringify(
    {
      tree: process.cwd(),
      liuyao: {
        charts: liuyaoRows.length,
        sample: liuyaoRows.slice(0, 3),
        stats: {
          overviewCounts: [...new Set(liuyaoRows.map((r) => r.overviewCount))].sort((a, b) => a - b),
          lineCounts: [...new Set(liuyaoRows.flatMap((r) => r.line.map((l) => l.count)))].sort((a, b) => a - b),
          overviewAnchoredZero: liuyaoRows.filter((r) => r.overviewAnchored === 0).length,
          lineAnchoredZero: liuyaoRows.reduce((n, r) => n + r.line.filter((l) => l.anchored === 0).length, 0),
          lineCases: liuyaoRows.length * 6,
          lineMissingOverviewPoints: liuyaoRows.reduce(
            (n, r) => n + r.line.filter((l) => l.missingFromOverview.length > 0).length,
            0,
          ),
          dupIdCases: liuyaoRows.reduce((n, r) => n + r.line.filter((l) => l.dupIds > 0).length, 0),
          missingMainPoint: liuyaoRows.reduce((n, r) => n + r.line.filter((l) => !l.hasMainPoint).length, 0),
          bogusOwnIdOverview: liuyaoRows.filter((r) => r.overviewBogusOwnId > 0).length,
          bogusOwnIdLine: liuyaoRows.reduce((n, r) => n + r.line.filter((l) => l.bogusOwnId > 0).length, 0),
        },
      },
      ziwei: {
        cases: ziweiCases.length,
        sample: ziweiCases
          .filter((c) => c.date === "2024-06-01" && c.palace === "命宫")
          .map((c) => ({
            requested: c.requested,
            textLayer: c.textLayer,
            expected: c.expectedOverlay?.scopeName ?? null,
            factLine: c.facts.filter((f) => f.startsWith("运限") || f.startsWith("流曜")),
            transitSentence: (/(当前运限层[^。]*。|本次按本命层解读[^。]*。|所选运限层[^。]*。)/.exec(c.text) ?? [""])[0],
          })),
        mismatches: ziweiCases
          .filter((c) => {
            if (!c.expectedOverlay) return false;
            const o = c.expectedOverlay;
            const stars = o.stars || "无";
            const mutagens = o.mutagens.join("、") || "无";
            const textOk = c.text.includes(
              `当前运限层${o.scopeName}${o.ganzhi}叠在本宫：流曜${stars}，四化${mutagens}。`,
            );
            const factsOk =
              c.facts.includes(`运限层=${o.scopeName}`) &&
              c.facts.includes(`流曜=${stars}`) &&
              c.facts.includes(`运限四化=${mutagens}`);
            return !(c.textLayer === o.scopeName && textOk && factsOk);
          })
          .map((c) => ({
            date: c.date,
            palace: c.palace,
            requested: c.requested,
            textLayer: c.textLayer,
            expected: c.expectedOverlay!.scopeName,
            expectedStars: c.expectedOverlay!.stars || "无",
            facts: c.facts.filter((f) => f.startsWith("运限") || f.startsWith("流曜")),
          })),
        crossLayer: ziweiCases
          .filter((c) => {
            if (!c.expectedOverlay || !c.textLayer) return false;
            return c.textLayer !== c.expectedOverlay.scopeName;
          })
          .length,
        noScopeMentionsTransit: ziweiCases.filter(
          (c) => c.requested === null && c.text.includes("当前运限层"),
        ).length,
        bogusScopeHandled: ziweiCases.filter(
          (c) => c.requested === "__bogus__" && c.text.includes("信息不足"),
        ).length,
        bogusScopeCases: ziweiCases.filter((c) => c.requested === "__bogus__").length,
        factLayerLabel: [
          ...new Set(
            ziweiCases
              .filter((c) => c.requested && c.requested !== "__bogus__")
              .flatMap((c) => c.facts.filter((f) => f.startsWith("运限层=") || f.startsWith("运限叠宫="))),
          ),
        ].sort(),
      },
    },
    null,
    1,
  ),
);
