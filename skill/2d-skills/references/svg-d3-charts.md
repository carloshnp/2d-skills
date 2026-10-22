---
name: svg-d3-charts
description: D3 7.9.0 data binding for SVG explainers and charts.
version: 1.1.0
---

# D3 SVG Charts

## Before you draw

From `illustration-spec` bring the encoding decision, not just the data: which quantity
is read off which channel (position on a common scale first, length second, never
angle, area or hue for the take-home number), whether small multiples share scales
(they must), and the palette roles. D3 will happily draw an encoding nobody can decode
accurately; that choice belongs in the spec, section 6. When the series is computed
from a model (a schedule, a phase diagram, a response curve), bring section 9b as well:
the chart is part of the mechanism and is checked with it.

D3 7.9.0 renders to real inline SVG DOM: every mark it draws is a node you can select,
style, transition and listen to. The core API has been **frozen since 2024-03-12** (no 7.10,
no 8.x as of 2026-10-17) and the relevant sub-modules have not changed since 2021-2022, so
code written against this skill stays stable.

> Scope note: the APIs and versions below come from the D3 status report (R2). Anything not
> covered by the source reports carries an explicit **UNVERIFIED** tag.

## Quick Start

```javascript
import * as d3 from "d3"; // npm i d3@7.9.0

const data = [
  { label: "A", value: 4 },
  { label: "B", value: 9 },
  { label: "C", value: 6 },
];

const width = 480;
const height = 220;
const margin = { top: 16, right: 16, bottom: 32, left: 40 };

// One fixed internal coordinate space; the browser scales it. See svg-interaction.
const svg = d3
  .select("#chart")
  .attr("viewBox", `0 0 ${width} ${height}`)
  .attr("role", "img")
  .attr("aria-label", "Bar chart of values");

const x = d3
  .scaleLinear()
  .domain([0, d3.max(data, (d) => d.value)])
  .range([margin.left, width - margin.right]);

const y = d3
  .scaleBand()
  .domain(data.map((d) => d.label))
  .range([margin.top, height - margin.bottom])
  .padding(0.2);

// Data join: create-or-update in a single call.
svg
  .selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", x(0))
  .attr("y", (d) => y(d.label))
  .attr("width", (d) => x(d.value) - x(0))
  .attr("height", y.bandwidth())
  .attr("fill", "steelblue");

// Axes
svg
  .append("g")
  .attr("transform", `translate(0,${height - margin.bottom})`)
  .call(d3.axisBottom(x).ticks(5));
```

## Versions and Setup

Latest release of `d3` is **7.9.0 (2024-03-12)**; it is still `latest` on 2026-10-17.
The modules this skill uses, and their last release, are:

| Module | Version | Released |
|---|---|---|
| d3-selection | 3.0.0 | 2021-06-07 |
| d3-scale | 4.0.2 | 2021-09-24 |
| d3-axis | 3.0.0 | 2021-06-09 |
| d3-transition | 3.0.1 | 2021-06-09 |
| d3-zoom | 3.0.0 | 2021-06-10 |
| d3-drag | 3.0.0 | 2021-06-09 |
| d3-shape | 3.2.0 | 2022-12-20 |

- 7.9.0's headline addition was **`d3.schemeObservable10`** (a categorical colour scheme).
- Post-7.9.0 commits to the core repo are documentation/link fixes only; no source changes.

```bash
npm i d3@7.9.0
```

```javascript
import * as d3 from "d3";
```

The community D3 skill loads a generic 7.x bundle rather than a pinned build:
`<script src="https://d3js.org/d3.v7.min.js"></script>`. For a reproducible, frozen pin,
install `d3@7.9.0` from npm and let your bundler resolve it.

**UNVERIFIED:** whether a CDN build pinned to exactly 7.9.0 is served at a stable URL was
not checked in any source report; prefer npm/bundler pinning.

## Selections and Joins

`join()` collapses the enter/update/exit dance into one call. Use a **key function** so
nodes keep identity across updates; without it D3 binds by index and transitions restart.

```javascript
function update(newData) {
  svg
    .selectAll("rect.bar")
    .data(newData, (d) => d.label) // key function
    .join(
      (enter) => enter.append("rect").attr("class", "bar"),
      (updateSel) => updateSel,
      (exit) => exit.remove(),
    )
    .attr("x", x(0))
    .attr("y", (d) => y(d.label))
    .attr("width", (d) => x(d.value) - x(0))
    .attr("height", y.bandwidth());
}
```

- `.data()` binds an array to the current selection.
- `.join(enter, update, exit)` returns the merged enter+update selection, so attributes
  applied after it hit both new and existing marks.
- Keep one render function that re-runs the join; never hand-manage `enter`/`exit` selections
  when `join()` will do.

## Scales and Axes

A scale maps data space to pixel space. `scaleLinear` is the workhorse for quantitative axes:

```javascript
const x = d3.scaleLinear().domain([0, 100]).range([0, 480]);
x(50);          // 240: data -> pixel
x.invert(240);  // 50: pixel -> data (needed for pointer math)

const axis = d3.axisBottom(x).ticks(5).tickSizeOuter(0);
svg.append("g").attr("transform", "translate(0,200)").call(axis);
```

- Use `d3.axisBottom`/`d3.axisLeft` for x/y ticks; call the axis generator on a `<g>`.
- `x.invert()` converts a pointer coordinate back to a data value; pair it with the
  pointer-to-viewBox conversion from `svg-interaction`.
- The other scales (`scaleBand` for categories, `scaleTime`, `scaleLog`, …) live in the same
  `d3-scale` module and follow the same `domain`/`range` shape.
- Adopt the margin convention: one `margin` object, an inner plot rect, reused everywhere.

## Transitions

`d3-transition` interpolates attributes over time. Apply it *after* the join:

```javascript
svg
  .selectAll("rect.bar")
  .data(newData, (d) => d.label)
  .join("rect")
  .attr("class", "bar")
  .attr("y", (d) => y(d.label))
  .attr("height", y.bandwidth())
  .transition()
  .duration(300)
  .attr("width", (d) => x(d.value) - x(0));
```

- Starting a new `.transition()` on the same selection **interrupts** the previous one, which
  is exactly what you want for slider-driven updates (a fast input event should not queue up
  animations).
- Transition what changes (geometry, colour, opacity); keep the join structure identical so
  D3 can match nodes.

## Drag and Zoom Behaviors

`d3-zoom` and `d3-drag` attach gesture handlers to SVG elements and hand you coordinates in
user units; no manual hit-testing required.

```javascript
// Pan + wheel/pinch zoom on a group.
const g = svg.append("g");
const zoom = d3
  .zoom()
  .scaleExtent([1, 8])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });
svg.call(zoom);

// Drag individual handles.
d3.selectAll("circle.handle").call(
  d3
    .drag()
    .on("drag", function (event) {
      d3.select(this).attr("cx", event.x).attr("cy", event.y);
    })
    .on("end", () => {
      /* commit the new position to your model here */
    }),
);
```

- The zoom handler receives `event.transform`; apply it to a wrapping `<g>` so the whole
  figure pans/zooms together.
- Drag handlers receive the gesture state; the subject's coordinates are in the parent's
  user space, matching your `viewBox` units.
- Disable page scroll during touch gestures when a figure fills the viewport.

## Responsive SVG with ResizeObserver

Keep the `viewBox` **fixed** and let CSS scale the SVG (`width: 100%; height: auto`). Only
re-run layout logic that genuinely depends on the rendered size (label density, tick count).

```javascript
const wrap = document.querySelector("#chart-wrap");
const ro = new ResizeObserver(() => {
  // Re-render against the current container width; the viewBox never changes.
  render();
});
ro.observe(wrap);

// Fallback the community skill also uses:
window.addEventListener("resize", render);
```

Because the coordinate space is fixed, pointer conversions stay valid at any rendered size.
If you need to turn a click into a data value, use the `getScreenCTM().inverse()` recipe in
`svg-interaction` and then `x.invert(...)`.

## Charts Driven by a Model

Some charts have no data file: the series is computed from the same model that drives the
drawing (stroke schedule against crank angle, force against displacement, a phase diagram
against temperature). Then the generator is the model, and the chart is a mechanism.

```javascript
// one model, two views: the drawing and the chart call the same function
const PERIOD = 720;
const wrap = (t) => ((t % PERIOD) + PERIOD) % PERIOD;

// intervals that cross the period boundary become two marks with distinct keys
function bands(cyl) {
  return STROKES.flatMap(({ name, start, len }) => {
    const a = wrap(start + phaseOffset(cyl)), b = a + len;
    return b <= PERIOD
      ? [{ key: `${cyl}-${name}`, x0: a, x1: b, name }]
      : [{ key: `${cyl}-${name}`, x0: a, x1: PERIOD, name },
         { key: `${cyl}-${name}-b`, x0: 0, x1: b - PERIOD, name }];
  });
}

svg.selectAll("rect.band")
  .data(CYLS.flatMap(bands), (d) => d.key)      // the split suffix keeps identity
  .join("rect").attr("class", (d) => `band ${d.name}`)
  .attr("x", (d) => x(d.x0)).attr("width", (d) => x(d.x1) - x(d.x0));
```

- **Compute, do not transcribe.** Series typed in by hand drift from the drawing the first
  time the model changes; series computed from `phaseOffset` cannot.
- **Cyclic axes split at the wrap.** An interval from 630 to 810 on a 0 to 720 axis is two
  marks, 630 to 720 and 0 to 90. Drawn as one, it clips or vanishes. In one engine figure
  every stroke band was mapped into the period this way, with a `-b` key for the second
  half.
- **A state cursor is a derived mark.** The vertical line at the current angle is drawn
  from the same state the drawing uses, never from its own copy.
- **Invariants go in 9b and get swept.** For a schedule: each row's segments cover the
  period exactly once with no gap or overlap; the cursor's value equals the drawing's
  state; no band or label leaves the plot rect at any state.

## Choosing a Library

R2's per-library verdicts, for LLM-generated interactive explainers:

| Library | Version | Inline SVG DOM | Default renderer | Prefer when |
|---|---|---|---|---|
| D3 | 7.9.0 (2024-03-12) | Yes (native) | SVG | Bespoke marks, transitions, brushing, custom choreography |
| Observable Plot | 0.6.17 (2025-02-14) | Yes | SVG | A one-liner figure; lowest hallucination surface |
| Apache ECharts | 6.1.0 (2026-05-19) | Yes, opt-in | canvas | Rich built-in components (tooltip, legend, dataZoom) |
| Vega-Lite | 6.5.0 (2026-10-08) | Yes, configurable | contested | A declarative JSON spec; grammar fills in scales/axes |

**Observable Plot: one-liner SVG figures.** Returns a *detached* DOM element (an SVG or an
HTML `<figure>`) that you append yourself:

```javascript
import * as Plot from "@observablehq/plot";

const figure = Plot.plot({
  marks: [Plot.barY(data, { x: "label", y: "value" })],
});
document.querySelector("#chart-wrap").append(figure);
```

**ECharts: richest components, SVG is opt-in and the bundle is large (~60 MB unpacked).**
Canvas is the recommended default, and some effects fall back to canvas:

```javascript
import * as echarts from "echarts";
const chart = echarts.init(document.getElementById("chart"), null, { renderer: "svg" });
chart.setOption({ xAxis: { type: "category", data: ["A", "B", "C"] }, yAxis: {}, series: [{ type: "bar", data: [4, 9, 6] }] });
```

With tree-shakable imports you must import the SVG renderer yourself. **UNVERIFIED:** the
exact import path for the tree-shakable SVG renderer was not quoted in the source reports.

**Vega-Lite: declarative, but set the renderer explicitly.** vega-embed's README calls `svg`
the default while Vega core documents `canvas` as the default, so do not rely on the default:

```javascript
import embed from "vega-embed"; // vega-embed 7.3.0 (vega-lite 6.5.0, vega 6.4.0)

embed("#chart", spec, { renderer: "svg" }); // infer: "svg" -> guaranteed SVG DOM
```

Vega-Lite also ships a `vl2svg` CLI for server-side SVG export. Its interactivity runs through
Vega *signals*, which is more indirect than D3 or ECharts.

## Common Patterns

- **One render function.** `let state = {...}; function render(){ /* re-join + re-scale */ }`.
  Every interaction mutates `state` and calls `render()`. This is the backbone of
  `svg-interaction`'s `renderStep()`.
- **Join + axis together.** Rebuild ticks inside the same `render()` so the axis can never
  disagree with the marks, and use `d3.max` on the *current* data for the domain.
- **Hover/focus via per-node listeners.** D3 selections are DOM nodes, so you can attach
  native `pointerenter`/`pointerleave`/`click` handlers after the join instead of adding a
  raycaster. See `svg-interaction`.
- **Debounce expensive re-renders.** Wrap the ResizeObserver callback in a
  `requestAnimationFrame` guard so a drag-resize does not re-layout on every pixel.
- **Accessibility is free.** Give the root SVG `role="img"` and an `aria-label`, and expose
  data as `<text>` so labels stay searchable and selectable.
- **Model-driven series.** Generate from the model the drawing uses, split cyclic intervals
  at the wrap with distinct keys, and sweep the chart's invariants with the mechanism.

## Field notes (defaults, not laws)
- MUST: mark ONLY sourced numbers, and state the schematic-vs-measured
  convention in the caption with the source. Never invent curve points to
  fill a series: a hedged fabrication still propagates.
- DEFAULT: log time axis with Catmull-Rom smoothing through anchors; verify
  dot-on-curve coincidence numerically (`--dump-dom`), not by eye. Other
  honest presentations (step plots, annotated points without curves) are fine.

## See Also

- `svg-fundamentals` - Inline SVG authoring, `viewBox`, scaling, groups, CSS, pointer coords.
- `svg-geometry` - Paths, Beziers, markers, connectors and dash arrays for chart marks.
- `svg-interaction` - Direct SVG DOM interaction: step state, Play/Pause/Prev/Next, scrubbers.
- `svg-animation` - Timeline-driven SVG animation and the DrawSVG/MorphSVG plugins.
- `svg-defs` - Reusable `<defs>` boilerplate plus the SVG.js imperative section as a D3 alternative.
