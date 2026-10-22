---
name: svg-fundamentals
description: "Inline SVG: viewBox, scaling, groups, CSS, pointer coords."
version: 1.1.0
---

# SVG Fundamentals

## Before you draw

From `illustration-spec` bring the canvas contract: aspect ratio and its reason, the
unit scale, the final render size (which sets the minimum cap height in px), and the
text split (what is HTML prose, what is an in-SVG label). `viewBox` numbers are a
consequence of those decisions. Choosing them first is how a figure ends up with
labels that read fine at 1200 px and are illegible at 89 mm.

Also bring the view map (one `viewBox` per view, or one shared canvas when views are
tabs) and the detail level. `detail: full` is the default, so size the canvas for the
features the inventory lists, not for the first sketch.

## Quick Start

```html
<!-- HTML + inline-SVG hybrid: the SVG is part of the page DOM -->
<section class="figure">
  <svg viewBox="0 0 200 120" width="100%" height="auto"
       role="img" aria-label="demo figure">
    <g id="scene" transform="translate(10,10)">
      <rect class="box" x="0" y="0" width="40" height="30" rx="4" />
      <circle class="dot" cx="60" cy="15" r="8" />
      <text x="60" y="40" font-size="10">label</text>
    </g>
  </svg>
</section>
```

```css
/* Responsive scaling: width follows the column, viewBox never changes */
.figure svg { width: 100%; height: auto; display: block; }
/* CSS styling of inline-SVG shapes */
.box { fill: #3b82f6; stroke: #1e3a8a; stroke-width: 2; }
.dot { fill: #ef4444; }
.box:hover { fill: #2563eb; }
```

```javascript
// Pointer -> SVG user units: convert once at the event boundary
const svg = document.querySelector('.figure svg');
svg.addEventListener('pointerdown', (e) => {
  const pt = new DOMPoint(e.clientX, e.clientY);
  const loc = pt.matrixTransform(svg.getScreenCTM().inverse());
  // keep all simulation logic in viewBox units from here on
  console.log('svg coords', loc.x, loc.y);
});
```

## HTML + Inline SVG Hybrid Architecture

Inline SVG lives directly in the HTML document, so its elements are real DOM nodes: queryable, styleable with CSS, and readable by assistive tech. Text stays text (searchable and selectable) instead of being painted to a bitmap.

- Put short labels inside SVG `<text>`; give each figure `role="img"` plus `<title>`/`aria-label`, or `aria-hidden="true"` when adjacent prose already describes it.
- Canvas is a dead end for accessibility ("Canvas content is not exposed to accessibility tools as semantic HTML is.", MDN, accessed 2026-10-17); keep anything a reader may copy, search, or hear in inline SVG/HTML.
- Stay on inline SVG up to roughly 1,000 live elements; move dense marks to `<canvas>` above that (ApexCharts benchmark: ~1,000 marks → SVG; tens of thousands → canvas; auto-switch ~8,000 points); UNVERIFIED beyond the cited benchmark numbers.

## viewBox Coordinate Discipline

Pick one fixed internal coordinate space, declare it once in `viewBox`, and let the browser scale it. Never change the coordinate system at runtime.

- `viewBox="minX minY width height"` defines a rectangle in user space that is "mapped to the bounds of the viewport of an SVG element" (MDN, accessed 2026-10-17).
- Real-world evidence: Red Blob Games repeats `viewBox="-55,-55 110,110"` across grid diagrams so one diagram unit equals one grid cell, independent of rendered size (accessed 2026-10-17).
- Keep all simulation/model math in these user units; convert pointer input at the boundary (see below).

## Responsive Scaling

Width follows the container; the `viewBox` never changes.

- CSS: `svg { width: 100%; height: auto; }` (Distill GP figures use `svg.svelte-1gc1gg1{width:100%;height:auto}`, accessed 2026-10-17).
- The `viewBox` rectangle is mapped onto the viewport bounds, often with `preserveAspectRatio` (MDN, accessed 2026-10-17).

### Floors in CSS px, not units

Stroke and text floors are met on screen, so convert at the smallest viewport the spec
names: `px per unit = rendered SVG width / viewBox width`. In one build a 1600x820 canvas
rendered at about 0.78 px per unit at 1280x720, so 1.25-unit annotation strokes drew under
1 CSS px; they were raised to 1.5 units, and labels to 18.5 units (about 14 px). Measure
the scale from `svg.getBoundingClientRect().width`, not from the window size, and assert
the label floor in px in the audit (see `svg-verify`).

- A full-page figure (`100vw x 100vh`, no scrollbar) gets its scale from the tighter of
  the two axes; check the floor at the narrowest aspect the spec allows.
- Raising every class by the same factor keeps the 2:1 outline-to-annotation ratio; raising
  only the thin lines breaks it.

## Groups and Transforms

- `<g>` is an empty container for organising elements; transforms on a group apply to all children.
- Use `transform="translate(x,y)"`, `scale(...)`, `rotate(deg, cx, cy)` to position sub-scenes without editing every coordinate.
- Nest groups to build a scene graph (axes, plot, legend) that can be moved as a unit.

## CSS Styling of SVG Shapes

Inline SVG elements accept both presentation attributes and CSS:

- `fill`, `stroke`, `stroke-width`, `opacity`, `font-size` work as CSS properties on SVG elements.
- Prefer classes (`.box { fill: ... }`) over inline styles for theming and `:hover`/`:focus` states.
- `transform` on SVG elements via CSS is supported in modern browsers (UNVERIFIED against the reports); prefer the SVG `transform` attribute for maximum compatibility.

## Pointer-to-SVG Conversion

The canonical recipe: build a point from `clientX/clientY`, then multiply by the inverse screen CTM.

- Modern entry point: `new DOMPoint(x, y).matrixTransform(svg.getScreenCTM().inverse())` (MDN `getScreenCTM`/`createSVGPoint`/`matrixTransform`; SitePoint recipe `pt.matrixTransform(svg.getScreenCTM().inverse())`, accessed 2026-10-17).
- Legacy equivalent: `const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; const loc = pt.matrixTransform(svg.getScreenCTM().inverse());`
- `getScreenCTM()` "represents the matrix that transforms the current element's coordinate system to the coordinate system of the SVG viewport" (MDN, accessed 2026-10-17).
- Shipped explainers use exactly this: Distill's GP bundle contains `r.matrixTransform(t.getScreenCTM().inverse())` (accessed 2026-10-17).
- Agent rule: never mix CSS pixel coordinates with user units; do the single `getScreenCTM().inverse()` conversion at the event boundary and keep all simulation logic in `viewBox` units.

## Common Patterns

- **Single render function:** keep a state index and one `renderStep(state)` that touches the DOM; controls only mutate the index (TensorFlow Playground routes everything through `oneStep()`; scrollama uses `data-step`, accessed 2026-10-17).
- **Slider-driven params:** bind `input` events, recompute the model, then write SVG attributes (`d`, `cx/cy`, `transform`, `opacity`, `stroke-width`); never rebuild the markup string.
- **Accessibility:** `role="img"` + `<title>`/`aria-label`, or `aria-hidden="true"` for decorative SVGs (Red Blob Games `aria-label="start location blob"`; Transformer Explainer `role="img" aria-label`, accessed 2026-10-17).

## Math in HTML, SVG text rules (MUSTs, verified breakage)
- Never use the MathJax `tex-svg.js` output: its `<svg>` sizes itself in `ex`
  units, which some Chromium builds ignore, collapsing the graphic to full container
  width (a small inline root rendered 6-8x oversized in testing). Use `tex-chtml.js`;
  raw TeX stays readable if the CDN fails.
- Inside SVG `<text>`, prefer `<tspan dy>` subscripts whenever headless captures
  matter: Unicode subscripts (U+2080+) render as tofu in headless Chromium
  (desktop browsers usually handle them, so this is a verification constraint,
  not a typographic one). Check inline math size in a capture
  (`mjx-container { font-size: 100%; }` is a sane default, not a law).

## See Also

- `svg-geometry` - Paths, Beziers, markers, connectors, dash arrays
- `svg-interaction` - Step state, sliders, scrubbers: the control layer on top of the DOM
- `svg-defs` - Reusable `<defs>` boilerplate: markers, gradients, masks, filters, text