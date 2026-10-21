---
name: svg-defs
description: "SVG defs boilerplate: markers, gradients, masks, filters."
version: 1.0.0
---

# SVG Defs and Reusable Resources

## Before you draw

From `illustration-spec` bring the palette table (roles plus hex, one row per colour)
and the arrow semantics. In a spec, an arrow claims movement, transformation,
causation or sequence, never decoration or emphasis, so each marker in `<defs>` should
map to one declared meaning. Filters are the one place faithful rendering is not
assumed: `feGaussianBlur` has already broken headless capture here.

`<defs>` holds SVG resources that are not rendered on their own; they paint only when
referenced by `url(#id)` from an attribute (`fill`, `stroke`, `marker-end`, `clip-path`,
`mask`, `filter`). This skill is copy-paste boilerplate for the six resource types that
matter in explainers (markers, gradients, clip paths, masks, filters), plus
`foreignObject` and text elements.

> Scope note: support/availability claims come from the SVG APIs report (R4, accessed
> 2026-10-17) and the Phase 2 decisions in `parent-findings.md`. The markup itself is
> standard SVG boilerplate; details that go beyond what the reports quote carry an explicit
> **UNVERIFIED** tag.

## Quick Start

One `<defs>` block, five resource types, all referenced by id:

```html
<svg viewBox="0 0 400 240" width="100%" height="auto" role="img"
     aria-label="defs demo: arrowhead, gradients, clip, mask, filter">
  <defs>
    <!-- Arrowhead marker -->
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#111" />
    </marker>

    <!-- Gradients -->
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#3b82f6" />
      <stop offset="1" stop-color="#3b82f6" stop-opacity="0.1" />
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fbbf24" />
      <stop offset="1" stop-color="#fbbf24" stop-opacity="0" />
    </radialGradient>

    <!-- Hard-edge clip -->
    <clipPath id="plot-clip">
      <rect x="20" y="20" width="120" height="80" />
    </clipPath>

    <!-- Soft alpha mask: white shows, black hides -->
    <mask id="left-half">
      <rect x="0" y="0" width="200" height="240" fill="#fff" />
      <rect x="200" y="0" width="200" height="240" fill="#333" />
    </mask>

    <!-- Filter -->
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" />
    </filter>
  </defs>

  <!-- usage: reference each resource with url(#id) -->
  <rect x="20" y="20" width="120" height="80" fill="url(#glow)" clip-path="url(#plot-clip)" />
  <circle cx="140" cy="130" r="55" fill="url(#fade)" filter="url(#soft)" />
  <rect x="40" y="40" width="300" height="160" fill="#93c5fd" mask="url(#left-half)" />
  <line x1="40" y1="220" x2="340" y2="220" stroke="#111" stroke-width="2" marker-end="url(#arrow)" />
</svg>
```

## Markers and Arrowheads

A `<marker>` is a reusable arrowhead (or dot/tick) attached to path ends and waypoints:

```html
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="6" markerHeight="6" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#111" />
  </marker>
</defs>

<path d="M70,55 C120,10 120,100 170,55" fill="none" stroke="#111"
      stroke-width="2" marker-end="url(#arrow)" />
```

- `refX`/`refY` anchor the marker on the path point; `orient="auto"` rotates it with the
  path direction. Attach with `marker-end`, `marker-start`, or `marker-mid` (connector
  geometry lives in `svg-geometry`).
- **Hand-written: full support.**
- **SVG.js: full support**: `SVG.Marker` is documented, and markers `"can be added to
  every individual point of a line, polyline, polygon and path"`, with `start/mid/end`
  positioning and `orient()` (R4).
- **Two.js 0.8.24: missing**: the string `marker` occurs 0 times in the 543 KB published
  build; arrowheads exist only as drawn geometry via `Two.makeArrow` (R4).

## Gradients

```html
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#3b82f6" />
    <stop offset="1" stop-color="#3b82f6" stop-opacity="0.1" />
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fbbf24" />
    <stop offset="1" stop-color="#fbbf24" stop-opacity="0" />
  </radialGradient>
</defs>

<rect fill="url(#fade)" />
<circle fill="url(#glow)" />
```

- Stops go from `offset="0"` to `offset="1"`; `gradientUnits` and the coordinate-space
  rules (object bounding box vs user space) are standard SVG; **UNVERIFIED** against R4,
  which confirms only library support.
- **Hand-written: full support.**
- **SVG.js: full support**: `draw.gradient('linear'/'radial')`, `stop()`,
  `from/to/radius()`, then `fill(gradient)` (R4).
- **Two.js 0.8.24: supported**: `Two.LinearGradient` / `Two.RadialGradient` / `Two.Stop`,
  emitted into `<defs>`; the SVG renderer docs describe `"<defs /> to apply gradients,
  patterns, and bitmap imagery"` (R4).

## clipPath

A clip path gives a **hard edge**, so content outside the shape is cut away:

```html
<defs>
  <clipPath id="plot-clip">
    <rect x="40" y="20" width="320" height="160" />
  </clipPath>
</defs>

<g clip-path="url(#plot-clip)">
  <!-- marks that must not spill past the plot area -->
</g>
```

- **Hand-written: full support.**
- **SVG.js: full support**: `draw.clip()`, `clipWith()`, `unclip()`, multiple children,
  and `clipper()` are documented (R4).
- **Two.js 0.8.24: partial**: the renderer creates `<clipPath clip-rule="nonzero">`
  elements for `Two.Path.clip` shapes, but there is no arbitrary clip-path container class
  (R4).

## Masks

A mask gives a **soft / alpha edge**: white shows, black hides, greys in between (standard
luminance masking; **UNVERIFIED** against R4, which confirms only support):

```html
<defs>
  <mask id="focus">
    <rect width="400" height="240" fill="#000" />
    <circle cx="200" cy="100" r="80" fill="#fff" />
  </mask>
</defs>

<g mask="url(#focus)"> <!-- everything outside the circle fades to hidden --> </g>
```

- **Hand-written: full support.**
- **SVG.js: full support**: `SVG.Mask` plus `maskWith()` and `unmask()` are documented
  (R4).
- **Two.js 0.8.24: missing and documented broken**: `Two.Path.mask` is `"currently not
  working because of SVG spec issues"` and the renderer never emits
  `createElement("mask")` (0 hits in the published build) (R4).

## Filters

```html
<defs>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" />
  </filter>
</defs>

<circle cx="140" cy="130" r="55" fill="#3b82f6" filter="url(#soft)" />
```

- Filter primitives (`feGaussianBlur`, `feColorMatrix`, …) and the filter-region
  attributes are standard SVG; **UNVERIFIED** against the reports; R4 confirms only
  whether `<filter>` elements are emitted/supported at all.
- **Hand-written: full support.**
- **SVG.js: partial in core**: there is no Filter element in core; filters are supported
  via the plugin `svg.filter.js` (listed on the official plugins page) (R4).
- **Two.js 0.8.24: missing**: `createElement("filter")` and the string `"filter"` have 0
  hits in the published build, and there is no Filter class in the docs (R4).

## foreignObject Embedding

`<foreignObject>` lets HTML live inside the SVG: widgets, wrapped prose, third-party
markup:

```html
<foreignObject x="40" y="40" width="240" height="90">
  <div xmlns="http://www.w3.org/1999/xhtml" style="font: 14px/1.4 system-ui">
    Wrapped <strong>HTML</strong> inside the figure.
  </div>
</foreignObject>
```

- The `xmlns` attribute on the child is standard practice for XML documents,
  **UNVERIFIED** against the reports (R4 confirms only that foreign objects "hold objects
  which are not from the svg namespace").
- **Hand-written: full support.**
- **SVG.js: full support**: `SVG.ForeignObject` is documented: `"A foreign object can
  hold objects which are not from the svg namespace."` (R4).
- **Two.js 0.8.24: missing**: 0 occurrences of `foreignObject` in the 543 KB published
  build and no docs entry (R4).
- Keep plain labels as `<text>` (below) rather than HTML: real SVG text stays searchable
  and selectable; see `svg-fundamentals` for the accessibility rules.

## Text Elements

```html
<text x="40" y="40" font-size="14" fill="#111">
  total <tspan font-weight="bold" fill="#3b82f6">42</tspan>
</text>
```

- `<tspan>` styles a run inside a `<text>`; `<textPath>` routes text along a path (standard
  SVG; **UNVERIFIED** against the reports).
- **Hand-written: full support.**
- **SVG.js: full support**: `SVG.Text`, `SVG.TextPath`, and `SVG.Tspan` are all in the
  documented element list (R4).
- **Two.js 0.8.24: present**: the docs index lists `Two.Text` (and `Two.Text.dashes.offset`
  for animated dashes); R4 did not matrix text, so its exact emitted markup is
  **UNVERIFIED**.
- Animating text splits? `SplitText does not support SVG <text>.` (R3); plan around it.

## Support Matrix

R4's feature matrix, condensed (Two.js **0.8.24**, SVG.js **3.2.8**, hand-written inline
SVG; all evidence accessed 2026-10-17):

| Defs feature | Two.js 0.8.24 (SVG output) | SVG.js 3.2.8 | Hand-written inline SVG |
|---|---|---|---|
| Markers / `marker-end` | ❌ missing (`marker`: 0 build hits; arrows via `Two.makeArrow`) | ✅ `SVG.Marker`, start/mid/end, `orient()` | ✅ |
| linear/radial gradients | ✅ `Two.LinearGradient` / `Two.RadialGradient` / `Two.Stop` | ✅ `gradient()`, `stop()`, `from/to/radius()`, `fill()` | ✅ |
| `clipPath` | 🟡 emits `<clipPath>` for `Path.clip` shapes only | ✅ `clip()`, `clipWith()`, `unclip()`, `clipper()` | ✅ |
| `<mask>` | ❌ broken (`Two.Path.mask` "currently not working") | ✅ `SVG.Mask`, `maskWith()`, `unmask()` | ✅ |
| `<filter>` | ❌ missing (0 build hits) | 🟡 plugin `svg.filter.js` only | ✅ |
| `foreignObject` | ❌ missing (0 build hits) | ✅ `SVG.ForeignObject` | ✅ |

Reading: **hand-written SVG is the ceiling**; everything is available. SVG.js is the
full-fidelity imperative option (its only trade is that it edits real SVG DOM directly).
Two.js drops markers, `foreignObject`, `<mask>`, and filters from its SVG output entirely.

## Choosing an Authoring Path

Phase 2 decision (parent-findings, 2026-10-17): **hand-written inline SVG + GSAP +
D3/Plot, with SVG.js as the imperative option.** No Two.js skill was planned precisely
because its reduced SVG surface defeats the purpose of going SVG-first.

- Need arrowheads, masks, filters, or HTML-in-SVG from a generator? Check the matrix above
  first: Two.js cannot emit them, so author those figures by hand or via SVG.js.
- `snap.svg` is effectively dead (0.5.1 published 2017-02-06; last commit 2022-03-13); do
  not reach for it (R4).

## SVG.js Boilerplate (Imperative Option)

```javascript
import { SVG } from "@svgdotjs/svg.js"; // npm i @svgdotjs/svg.js, 3.2.8 (2026-08-04)

const draw = SVG().addTo("body").size(400, 240);

const rect = draw.rect(100, 100).attr({ fill: "#f06" }); // factory pattern from the docs
rect.animate().fill("#f03").move(100, 100);               // chained animation, docs example

const adopt = SVG("#myRectId");   // wrap an existing node
const frag = SVG("<circle>");     // create from a fragment
```

Defs-relevant API, all method/class names verified in R4:

| Need | SVG.js |
|---|---|
| Defs container | `SVG.Defs` (container element) |
| Gradients | `draw.gradient('linear'/'radial')`, `stop()`, `from/to/radius()`, `fill(gradient)` |
| Clip | `draw.clip()`, `clipWith()`, `unclip()`, `clipper()` |
| Mask | `SVG.Mask`, `maskWith()`, `unmask()` |
| Marker | `SVG.Marker`, `orient()`, start/mid/end positioning |
| foreignObject | `SVG.ForeignObject` |
| Text | `SVG.Text`, `SVG.TextPath`, `SVG.Tspan` |
| Filters | plugin `svg.filter.js` (not in core) |
| Also available | `SVG.Pattern`, `SVG.Use`, `SVG.Style` |

**UNVERIFIED:** argument lists for the methods above, where not quoted verbatim; R4
verified the names and the `SVG()`/`rect()`/`animate()` examples shown, not every
signature.

Version note: npm `latest` is **3.2.8 (published 2026-08-04)**; the GitHub Releases page
still shows **3.2.6 (2026-07-17)** as "Latest"; trust npm for the newest publish (R4).

## Common Patterns

- **One `<defs>` per figure**, at the top of the SVG, referenced with `url(#id)`.
- **Prefix ids** (`#myfig-arrow`) when several SVGs share a page: colliding ids make every
  reference resolve to the first match (standard SVG; **UNVERIFIED** against R4).
- **Arrowheads** are a marker + `orient="auto"`; the connector curve that carries them is
  in `svg-geometry`.
- **Pick the resource by edge quality:** gradient = painted fill, `clipPath` = hard cut,
  `mask` = soft/alpha fade.
- **Generator check first:** before drawing a defs-heavy figure through Two.js, consult the
  support matrix; its SVG output silently lacks markers, masks, filters, and
  `foreignObject`.
- **Keep labels as `<text>`**; reserve `foreignObject` for HTML widgets that SVG cannot
  express (forms, KaTeX); see `svg-fundamentals`.

## See Also

- `svg-fundamentals` - Inline SVG authoring, `viewBox`, scaling, groups, CSS, pointer coords.
- `svg-geometry` - Paths, Beziers, connectors and dash arrays that carry these markers.
- `svg-interaction` - Direct SVG DOM interaction: steps, scrubbers, sliders.
- `svg-d3-charts` - D3 7.9.0 joins, scales, axes and transitions for SVG figures.
- `svg-animation` - GSAP 3.15 paused timelines, DrawSVG stroke animation, easeReverse.
