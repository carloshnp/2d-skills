---
name: svg-interaction
description: "Direct SVG DOM interaction: steps, scrubbers, sliders."
version: 1.1.0
---

# SVG Interaction

## Before you draw

Interaction is a reading decision, not a feature. From `illustration-spec` bring the
reading task, the step list (one idea per step), and whether interaction is needed at
all: if a static figure answers the question, controls only add load. Every control
should trace to a requirement in the spec, and the step count should trace to the
mechanism's action points. When the figure is a mechanism, section 9b names the state
variable, its range, its datum, and its named states; the controls are bound to exactly
that.

Inline SVG gives you something canvas does not: every shape is a real DOM node with its own
events, text and accessibility. You do not project a pointer into a scene graph or run a
raycaster: you attach a listener to the node, or read the pointer in the figure's own
`viewBox` units. This skill covers the interaction layer for HTML + inline-SVG explainers:
a **step index** driving one `renderStep()`, Play/Pause/Prev/Next controls, a scrubber, and
range-slider parameters that update SVG attributes.

> Scope note: patterns below come from the explainer-architecture report (R5). The dedicated
> timeline-scrubber recipe was **not found in any shipped explainer** in that research, so the
> wiring here is explicitly authored from the documented primitives. Anything not covered by
> the source reports is tagged **UNVERIFIED**.

## Quick Start

A complete, GSAP-free stepper: one state index, one `renderStep()`, Play/Pause/Prev/Next, a
scrubber, and a radius slider that writes an SVG attribute.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>SVG stepper</title>
  </head>
  <body>
    <div class="controls">
      <button id="prev" aria-label="Previous step">◀ Prev</button>
      <button id="play" aria-label="Play or pause">Play</button>
      <button id="next" aria-label="Next step">Next ▶</button>
      <input id="scrub" type="range" min="0" max="3" step="1" value="0"
             aria-label="Step scrubber" />
      <span id="readout">Step 0/3</span>
    </div>

    <svg id="scene" viewBox="0 0 400 200" width="100%" role="img"
         aria-label="A dot moving along a line">
      <line x1="20" y1="100" x2="380" y2="100" stroke="#ddd" stroke-width="2" />
      <circle id="dot" cx="20" cy="100" r="8" fill="#3b82f6" />
    </svg>

    <label>radius
      <input id="radius" type="range" min="4" max="40" step="1" value="8" />
    </label>

    <script>
      // Fixed coordinate space = the viewBox above; 1 unit = 1 user unit.
      const STEPS = 4; // indices 0..3
      const positions = [20, 140, 260, 380];
      let step = 0;
      let playing = false;
      let timer = null;

      const dot = document.getElementById("dot");
      const scrub = document.getElementById("scrub");
      const readout = document.getElementById("readout");
      const playBtn = document.getElementById("play");
      const radius = document.getElementById("radius");

      // The ONLY function that writes to the DOM.
      function renderStep() {
        dot.setAttribute("cx", positions[step]);
        scrub.value = step; // keep the scrubber in sync
        readout.textContent = `Step ${step}/${STEPS - 1}`;
      }

      function go(n) {
        step = Math.max(0, Math.min(STEPS - 1, n)); // clamp
        renderStep();
      }

      // Controls only mutate the index.
      document.getElementById("prev").addEventListener("click", () => { stop(); go(step - 1); });
      document.getElementById("next").addEventListener("click", () => { stop(); go(step + 1); });
      scrub.addEventListener("input", () => { stop(); go(Number(scrub.value)); });

      // Play = a timer loop that calls the same next().
      function tick() { go(step >= STEPS - 1 ? 0 : step + 1); }
      function start() { playing = true; timer = setInterval(tick, 700); playBtn.textContent = "Pause"; }
      function stop() { playing = false; clearInterval(timer); timer = null; playBtn.textContent = "Play"; }
      playBtn.addEventListener("click", () => (playing ? stop() : start()));

      // Slider -> parameter -> SVG attribute (listen to "input", not "change").
      radius.addEventListener("input", () => dot.setAttribute("r", radius.value));

      renderStep();
    </script>
  </body>
</html>
```

## Step State: One Index, One renderStep()

Make a single integer the source of truth. One function, `renderStep()`, is the only thing
that touches the DOM, and every control merely changes the index and calls it.

```javascript
let step = 0;

function renderStep() {
  // read `step`, write attributes / text
}

function go(n) { step = clamp(n, 0, TOTAL - 1); renderStep(); }
```

This is the pattern shipped by the reference explainers:

- **TensorFlow Playground** routes everything through one `oneStep()`; the step button is
  wired as `d3.select("#next-step-button").on("click", …oneStep())`, with a `#iter-number`
  readout for the current index.
- **Distill's t-SNE** article pairs a `<button class="play-pause">` with a
  `#tray-steps-display` step counter.
- **Scrollama** stores step identity in markup (`<div class="step" data-step="a">`) and fires
  `onStepEnter`, i.e. step identity, not imperative drawing, drives rendering. The
  `data-step` attribute is optional bookkeeping but useful for linking clicks to indices.

Why one render path: Play, Prev/Next and the scrubber all funnel through `renderStep()`, so
they can never drift out of sync. Add a step by extending the data, not by adding a second
drawing routine.

## Play/Pause/Prev/Next + Scrubber

Bind the scrubber directly to `step` and call `renderStep()`; no separate render path.

```javascript
const scrub = document.getElementById("scrub");
scrub.max = TOTAL - 1;

scrub.addEventListener("input", () => { stop(); go(Number(scrub.value)); });

function next() { go(step + 1); }
function prev() { go(step - 1); }
```

Keep Play on a loop that calls the *same* `next()`:

```javascript
function tick() { go(step >= TOTAL - 1 ? 0 : step + 1); }

function start() { playing = true; timer = setInterval(tick, 700); }
function stop()  { playing = false; clearInterval(timer); timer = null; }
```

`requestAnimationFrame` (driving an elapsed-time accumulator) is the other valid loop; a
plain timer is enough for discrete steps.

> **Authored pattern.** The research deliberately recorded that a *dedicated timeline
> scrubber* (a range input over step indices) was **not found** in any shipped explainer it
> opened. The nearest verified substitutes were an integer `type="range"` used as a state
> selector (Transformer Explainer) and a step counter (Distill t-SNE). So this scrubber
> wiring is authored from those primitives; treat it as a starting point, not a quote.

Accessibility details worth keeping: give each button an `aria-label`, mark decorative SVGs
`aria-hidden="true"`, and give the figure `role="img"` with a descriptive label.

## Range-Slider Parametric Updates

A range slider writes a parameter; a handler recomputes the model; the result is pushed into
SVG **attributes** (`d`, `cx`/`cy`, `transform`, `opacity`, `stroke-width`); never by
rebuilding the markup string.

```javascript
const noise = document.getElementById("noise");

noise.addEventListener("input", () => {       // "input", not "change", tracks continuously
  const p = Number(noise.value);
  const geometry = compute(p);                 // pure: f(params) -> geometry
  group.setAttribute("transform", `translate(${geometry.x},${geometry.y})`);
  dot.setAttribute("cx", geometry.cx);
  dot.setAttribute("opacity", geometry.alpha);
});
```

Rules that keep this safe and smooth:

- Listen to `input` so the SVG updates while the thumb is dragged.
- Keep the model pure (`f(params) -> geometry`) and write attributes only as the last step.
- Clamp in HTML (`min`/`max`/`step`) so the JS needs no validation.
- This is the shape used by Distill's Gaussian-process figures (`updateSlider()` →
  `resample()` → redraw), TensorFlow Playground's hyperparameter sliders, Setosa's Markov
  chain probabilities, and Transformer Explainer's temperature/top-k controls.

## Controls Bound to the State Variable

A step index is one shape of state. A mechanism usually has a continuous one (crank
angle, time, a parameter) with named states inside it. Either way the control is a view
of the spec's state variable, never a second source of truth.

```javascript
// shell owns the state; panels only render it
const STATE = { min: 0, max: 719, step: 1, initial: 90 };          // from spec 9b
const q = new URLSearchParams(location.search);
let theta = clampWrap(Number(q.get("angle") ?? STATE.initial));
let tab = q.get("tab") ?? "A";

const slider = document.getElementById("crankAngle");              // min/max/step from STATE
slider.addEventListener("input", () => { theta = Number(slider.value); render(); });
document.addEventListener("keydown", (e) => {
  const d = { ArrowRight: 1, ArrowLeft: -1, PageUp: 90, PageDown: -90 }[e.key];
  if (d) { theta = clampWrap(theta + d); render(); e.preventDefault(); }
});
function clampWrap(t) { return ((t % 720) + 720) % 720; }           // cyclic: wrap, not clamp
function render() {
  slider.value = theta;
  readout.textContent = `${theta} deg, ${phaseName(theta)}`;       // units and named state
  PANELS[tab].render({ theta });
}
```

- **Range, step, and default come from 9b.** A slider whose `max` is 360 on a 720-degree
  cycle silently hides half the mechanism.
- **Cyclic state wraps, bounded state clamps.** Arrow keys past 719 return to 0.
- **Step by the mechanism's natural interval too.** Fine steps for inspection (1 degree)
  and a coarse key for the named interval (90 degrees, one firing apart in a V8), so a
  reader can walk the named states without dragging.
- **The readout shows the state in the spec's units and the named phase**, so a screenshot
  records which state it shows.
- **State lives in the shell, not in a view.** Switching tabs re-renders the new view from
  the same state; a view that keeps its own copy will disagree after the first switch.
- **Every state is reachable by URL** (`?tab=C&angle=90`). The harness, the reviewer, and
  a bug report all name states the same way. `svg-verify` relies on it.

## Per-Node Listeners

Because the marks are DOM nodes, attach listeners directly to them. There is no hit-test pass
and no raycaster.

```javascript
scene.querySelectorAll(".node").forEach((node) => {
  node.addEventListener("pointerenter", () => node.classList.add("is-hover"));
  node.addEventListener("pointerleave", () => node.classList.remove("is-hover"));
  node.addEventListener("click", () => go(Number(node.dataset.step)));
});
```

If a handler needs the pointer position in `viewBox` units (drag handles, seek-to-click),
convert once at the event boundary using the screen CTM:

```javascript
function toSvgPoint(svg, event) {
  const pt = new DOMPoint(event.clientX, event.clientY);
  return pt.matrixTransform(svg.getScreenCTM().inverse());
}
```

Never mix CSS pixel coordinates with user units; convert at the boundary and keep all
simulation logic in `viewBox` units. (`createSVGPoint()` is the older equivalent; prefer
`DOMPoint` for new code.)

A drag handle built from pointer events:

```javascript
let dragging = false;

dot.addEventListener("pointerdown", (e) => { dragging = true; e.preventDefault(); });
dot.addEventListener("pointermove", (e) => {
  if (!dragging) return;
  const p = toSvgPoint(scene, e);
  dot.setAttribute("cx", p.x);
  dot.setAttribute("cy", p.y);
});
dot.addEventListener("pointerup", () => { dragging = false; });
```

**UNVERIFIED:** `setPointerCapture()`/`releasePointerCapture()` on SVG elements, and
`pointercancel` handling, are standard Pointer Events features but were not covered by the
source reports; add them if you need robust capture and cancellation.

## Contrast with Canvas Hit-Testing

Inline SVG and canvas live on opposite sides of a trade-off:

| | Inline SVG | Canvas |
|---|---|---|
| Interaction | Native per-node `addEventListener` | Manual hit-testing (project pointer, then test geometry) |
| Text | Real `<text>`: searchable, selectable, readable by AT | Painted pixels; needs a parallel DOM overlay |
| Setup | No raycaster, no scene-graph pick pass | A picking layer or a raycaster-style test |

MDN states plainly that "Canvas content is not exposed to accessibility tools as semantic
HTML is," and that you should generally avoid canvas in an accessible site. SVG text, by
contrast, is "searchable, selectable, and accessible by screen readers." So for anything a
reader may need to copy, search or hear, prefer SVG nodes.

**Node ceiling.** Stay on inline SVG up to roughly **1,000 live interactive elements**; the
cited benchmark measures SVG and canvas as "neck and neck" at 1,000 points with SVG still
fully interactive. Between ~1,000 and ~8,000, measure on your target device. Above that,
either move the dense marks to `<canvas>` or keep SVG for chrome/labels and put only the
dense layer in canvas (the hybrid pattern used by TensorFlow Playground and Red Blob Games).
One `<path>` counts as one node, so lines and areas scale far beyond 1,000 data values.

## Cyclic Mechanisms: Phase Datum and Pose Order

When the animation angle drives a thermodynamic or mechanical cycle, reference phase zero to the mechanism's datum, not to the drawing's angle zero. A crank pin at screen-angle zero rarely coincides with any cylinder's top dead center: each bank's TDC is the pin angle parallel to that bank's axis, so define phase as angle-minus-TDC modulo the period, per bank. Stroke labels derived from raw angle drift by that offset, and the error reads as inverted physics, e.g. a power stroke showing the piston rising halfway through. After wiring, assert at every phase boundary that the driven body sits at its geometric extremum (TDC/BDC), and that boundary-tied events (spark, valve lift) fire at the correct offset from the true datum.

For static steppers, pick representative mid-stroke poses whose consecutive order reads direction-correct: the exhaust pose must sit visibly above (more risen than) the power pose, or stepping forward looks like the motion runs backward. Boundary poses that step the wrong way across a transition are worse than slightly inexact mid-stroke poses.

## Common Patterns

- **Index as truth.** `let step = 0` + `renderStep()` + controls that only call `go(n)`.
  Persist the index in a `data-step` attribute if markup needs to reference it.
- **Tooltip.** Toggle a `<g>`'s visibility on `pointerenter`/`pointerleave`, positioning it
  with `toSvgPoint()`; do not rebuild the tooltip markup per frame.
- **Highlight.** Add/remove a class (`.is-hover`) and let CSS own stroke/fill/opacity so the
  interaction layer stays out of styling.
- **Keyboard.** Add `keydown` handlers for `ArrowLeft`/`ArrowRight`/`Space` mapped to
  `prev()`/`next()`/Play-Pause so the stepper is usable without a pointer.
- **Attribute-only writes.** Mutate `d`, `cx`/`cy`, `r`, `transform`, `opacity`,
  `stroke-width`; never reassign `innerHTML`.
- **Shared state across views.** One state object in the shell, read from the URL on load,
  rendered into whichever tab is active; controls write it, views only read it.

## Field notes (defaults, not laws)
- The Quick Start stepper is ONE working implementation. Keep its invariants
  (single state index, one render function, controls only mutate the index)
  and redesign the surface freely: per-tab steppers, scroll-driven progress,
  keyboard-first, or something better. Same purpose, better form, wins.
- Full-scene steps: exclusive reveal with opacity 0 for inactive scenes.
  Progressive builds: cumulative reveal with dimmed context. The composition
  decides, not this file.

## See Also

- `svg-fundamentals` - Inline SVG authoring, `viewBox`, scaling, groups, CSS, pointer coords.
- `svg-geometry` - Paths, Beziers, markers, connectors and dash arrays to draw with.
- `svg-d3-charts` - D3 7.9.0 joins, scales, axes and transitions for SVG figures.
- `svg-animation` - Timeline-driven SVG animation with a scrubbed playhead.
- `svg-defs` - Reusable `<defs>` boilerplate plus the SVG.js imperative section.
