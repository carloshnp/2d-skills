---
name: svg-geometry
description: "SVG geometry: paths, Beziers, markers, connectors, dashes."
version: 1.0.0
---

# SVG Geometry

## Before you draw

Geometry here serves a composition decided earlier. From `illustration-spec` bring the
annotation budget (maximum labels and leaders), the line weight scale in px with its
2:1 outline-to-annotation ratio, and the projection (orthographic, isometric at 30/30,
or flat). Without those, paths and connectors get placed by eye and no two panels share
a grammar.

## Quick Start

```html
<svg viewBox="0 0 240 120" width="100%" height="auto" role="img" aria-label="connector demo">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#111" />
    </marker>
  </defs>
  <!-- two boxes -->
  <rect x="10"  y="40" width="60" height="30" fill="#dbeafe" stroke="#3b82f6" />
  <rect x="170" y="40" width="60" height="30" fill="#dbeafe" stroke="#3b82f6" />
  <!-- cubic Bezier connector with arrowhead and dash array -->
  <path d="M70,55 C120,10 120,100 170,55" fill="none"
        stroke="#111" stroke-width="2" stroke-dasharray="6 4"
        marker-end="url(#arrow)" />
</svg>
```

## Paths (M, L, C, Q, Z)

SVG `<path>` data uses single-letter commands (absolute by default; lowercase = relative):

- `M x,y`: move pen to a point (start a new sub-path).
- `L x,y`: straight line to a point.
- `H x` / `V y`: horizontal / vertical line (UNVERIFIED against the reports; standard SVG).
- `C x1,y1 x2,y2 x,y`: cubic Bezier.
- `Q x1,y1 x,y`: quadratic Bezier.
- `Z` (or `z`): close the current sub-path back to its start.

Example polyline-ish path: `d="M10,10 L70,10 L70,55"`.

## Cubic and Quadratic Beziers

- **Cubic** `C x1,y1 x2,y2 x,y`: two control points plus the end point; good for S-shaped connectors.
- **Quadratic** `Q x1,y1 x,y`: one control point; simpler, fewer parameters.
- Smooth variants `S`/`T` (UNVERIFIED against the reports; standard SVG) reuse the reflected previous control point.

## Markers and Arrowheads

- Define a marker in `<defs>` and attach with `marker-end="url(#id)"` (also `marker-start`, `marker-mid`).
- Key attributes: `viewBox`, `refX`/`refY` (anchor), `markerWidth`/`markerHeight`, `orient="auto"` so the arrow rotates with the path.
- SVG.js supports markers as a first-class element: `SVG.Marker` is documented, and markers "can be added to every individual point of a line, polyline, polygon and path", including `start/mid/end` and `orient()` (R4, accessed 2026-10-17).
- Two.js (0.8.24) does NOT emit markers; its arrowheads are drawn geometry via `Two.makeArrow` (R4, accessed 2026-10-17); use hand-written SVG when arrowheads are required.

## Connectors Between Boxes

1. Compute anchor points on each box (e.g. right edge mid-point of box A, left edge mid-point of box B).
2. Use a cubic Bezier whose control points sit horizontally (or vertically) out from the anchors to create a smooth curve.
3. Attach `marker-end` for an arrowhead and a `stroke-dasharray` for styling.

```javascript
// Coordinate mapping helper: linear scale (like d3.scaleLinear)
function scaleLinear(value, inMin, inMax, outMin, outMax) {
  return outMin + ((value - inMin) / (inMax - inMin)) * (outMax - outMin);
}
// anchor of box A's right edge
const ax = boxA.x + boxA.w;
const ay = boxA.y + boxA.h / 2;
const bx = boxB.x;
const by = boxB.y + boxB.h / 2;
const cx1 = ax + (bx - ax) * 0.4;
const cx2 = bx - (bx - ax) * 0.4;
const d = `M${ax},${ay} C${cx1},${ay} ${cx2},${by} ${bx},${by}`;
path.setAttribute('d', d);
```

## Dash Arrays

- `stroke-dasharray="6 4"` paints 6 units of stroke then 4 units of gap, repeating.
- `stroke-dashoffset` shifts the pattern; animating it creates a marching-ants / draw-on effect.
- DrawSVG (GSAP, free since 3.13) animates `stroke-dashoffset`/`stroke-dasharray` for stroke reveal; requires a visible stroke and prefers single-segment `<path>`s (R3, accessed 2026-10-17).
- Static dash arrays are trivial in hand-written SVG; SMIL/CSS animation of dashoffset is UNVERIFIED against the reports.

## Coordinate Mapping Helpers

- Linear scale function (above) maps data values to SVG user units.
- D3 provides `d3.scaleLinear().domain([a,b]).range([c,d])` (R2: d3-scale 4.0.2, stable since 2021); Observable Plot and ECharts also emit real inline SVG (R2).
- Keep a single source of truth: model values -> scale -> SVG attributes, never hand-pick pixels.

## Common Patterns

- **Box-and-arrow diagram:** rects + cubic Bezier connectors + `marker-end` arrowheads.
- **Dashed connector:** `stroke-dasharray` + `stroke-dashoffset` for emphasis or "in progress".
- **Annotated path:** use `marker-mid` for waypoints along a line.

## Field notes (defaults, not laws)
- When annotation columns threaten to overflow the viewBox, prefer stacking
  (scores / weights / output top to bottom) over squeezing side-by-side, or
  shrink the figure, or split the panel. The principle is budget the
  annotation space up front; the arrangement is yours.
- Zone swapping (`#pipe.swap #compZone { opacity: 0; }`) is one fix for two
  groups sharing one zone across steps; redesigning the layout so zones
  don't collide is equally valid.

## See Also

- `svg-fundamentals` - viewBox, scaling, groups, CSS, pointer conversion
- `svg-defs` - Markers, gradients, masks and filters that attach to these paths
- `svg-animation` - GSAP timelines and DrawSVG stroke animation for these paths