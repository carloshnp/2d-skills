---
name: svg-animation
description: GSAP 3.15 paused timelines for step-through explainers.
---

# SVG Animation with GSAP

## Before you draw

This skill times a sequence; it does not decide what the sequence is worth. From
`illustration-spec` bring three things: the step list (one idea per step), the answer
to the enabling test (why the reader cannot infer the transition from statics), and
the per-step labels. Statics are the default for causal processes; animation has to
earn its place. Without a step list, a timeline is only motion.

GSAP **3.15.0** (released 2026-04-13) is the current version, and every bonus plugin —
DrawSVG, MorphSVG, MotionPath, SplitText — has been **100% free since 3.13 (April 2025)**.
The timeline scrubbing primitives needed for a step-through explainer (`seek()`, `time()`,
`progress()`, `tweenTo()`, `tweenFromTo()`, labels, `nextLabel()`/`previousLabel()`) are
stable and unchanged through 3.15.

> Scope note: APIs and versions below come from the GSAP status report (R3, accessed
> 2026-10-17). The control wiring in the Quick Start is an **illustrative pattern
> constructed from documented primitives** (R3 §3) — neither GSAP's docs nor the official
> `greensock/gsap-skills` repo ships a Prev/Next + scrubber UI. Anything outside the source
> reports is tagged **UNVERIFIED**.

## Quick Start

A paused timeline whose steps are marked with labels, driven by Play/Pause, Prev/Next and a
range-input scrubber. Install with `npm i gsap@3.15.0`.

```html
<div class="controls">
  <button id="prev" aria-label="Previous step">◀ Prev</button>
  <button id="playpause" aria-label="Play or pause">Play</button>
  <button id="next" aria-label="Next step">Next ▶</button>
  <input id="scrub" type="range" min="0" max="1000" value="0" step="1" aria-label="Timeline scrubber">
</div>

<svg viewBox="0 0 200 200" width="200" height="200">
  <!-- step targets; give stroked shapes a real stroke so DrawSVG works -->
  <circle id="dot" cx="20" cy="100" r="6" fill="none" stroke="#3b82f6" stroke-width="3"/>
  <path id="trace" d="M20,100 L180,100" fill="none" stroke="#111" stroke-width="2"/>
</svg>
```

```js
import { gsap } from "gsap";
import { DrawSVGPlugin } from "gsap/DrawSVGPlugin";
gsap.registerPlugin(DrawSVGPlugin);
// Pinned CDN equivalent (verified): import { gsap } from "https://cdn.jsdelivr.net/npm/gsap@3.15.0/index.js";

// 1) Build a PAUSED timeline whose steps are marked with labels.
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.5, ease: "power2.inOut" }
});

tl.addLabel("step1")
  .to("#trace", { drawSVG: "0% 100%" }, "step1")      // draw the line
  .set("#dot",   { attr: { cx: 180 } }, "step1")        // discrete SVG attribute step

  .addLabel("step2")                                    // waits at end of step1 by default
  .to("#dot",    { attr: { cy: 40 }, duration: 0.4 })   // move up via attribute tween

  .addLabel("step3")
  .to("#dot",    { attr: { r: 12 }, duration: 0.4 });   // grow

// 2) Play / Pause (toggles in place; play() resumes from the current playhead).
const btn = document.getElementById("playpause");
btn.addEventListener("click", () => {
  if (tl.paused()) { tl.play(); btn.textContent = "Pause"; }
  else            { tl.pause(); btn.textContent = "Play"; }
});

// 3) Prev / Next: snap to the neighbouring LABEL with a short tween (tweenTo = scrubbed seek).
const nextLabel = () => tl.nextLabel(tl.time());
const prevLabel = () => tl.previousLabel(tl.time());

document.getElementById("next").addEventListener("click", () => {
  const lbl = nextLabel();
  if (lbl) tl.pause().tweenTo(lbl, { duration: 0.4, ease: "power2.out" });
});

document.getElementById("prev").addEventListener("click", () => {
  // nudge time slightly so previousLabel() doesn't return the current label
  const lbl = tl.previousLabel(Math.max(0, tl.time() - 0.001));
  tl.pause().tweenTo(lbl ?? 0, { duration: 0.4, ease: "power2.out" });
});

// 4) Range input drives the playhead; timeline keeps the slider in sync on update.
const scrub = document.getElementById("scrub");
scrub.max = tl.duration() || 1000;         // if you prefer 0..1, use progress() instead
scrub.addEventListener("input", () => {
  tl.pause();
  tl.time(Number(scrub.value));            // time() seeks without changing paused/reversed state
  btn.textContent = "Play";
});
tl.eventCallback("onUpdate", () => { scrub.value = tl.time(); });
```

## Paused Timelines and Labels

Build the whole explainer as **one timeline, created paused**, and treat labels as the step
names the UI navigates by.

```javascript
const tl = gsap.timeline({
  paused: true, // documented: "paused: true — create paused; call .play() to start."
  defaults: { duration: 0.5, ease: "power2.inOut" },
});

tl.addLabel("intro")
  .to("#trace", { drawSVG: "0% 100%" }, "intro")
  .addLabel("middle")
  .to("#dot", { attr: { cx: 180 }, duration: 0.4 });
```

- `addLabel()` places a named marker; tween positions (`"intro"` above) target the same
  label so tweens and step boundaries stay aligned.
- `seek()` accepts a label as well as a time: `"Jumps to a specific time (or label) without
  affecting whether or not the instance is paused or reversed."`
- `addPause()` is documented alongside `addLabel()` and inserts a pause point in the
  timeline. **UNVERIFIED:** its exact arguments/behaviour were not quoted in R3.
- Timeline `defaults` cascade to every child tween — including `easeReverse` (see below).

## Play / Pause

Play/Pause toggles in place; `play()` resumes from the current playhead rather than
restarting.

```javascript
document.getElementById("playpause").addEventListener("click", () => {
  if (tl.paused()) tl.play();
  else tl.pause();
});
```

- `tl.paused()` is the boolean getter used above.
- Also documented and stable: `.play(from)`, `.restart()`, `.reverse()`, `.timeScale()`.
- GSAP's own summary: `"paused: true — create paused; call .play() to start."`

## Prev / Next Step Buttons

Step navigation = find the neighbouring **label**, then scrub to it with `tweenTo()` instead
of hard-cutting with `seek()`.

```javascript
document.getElementById("next").addEventListener("click", () => {
  const lbl = tl.nextLabel(tl.time());
  if (lbl) tl.pause().tweenTo(lbl, { duration: 0.4, ease: "power2.out" });
});

document.getElementById("prev").addEventListener("click", () => {
  // nudge time slightly so previousLabel() doesn't return the current label
  const lbl = tl.previousLabel(Math.max(0, tl.time() - 0.001));
  tl.pause().tweenTo(lbl ?? 0, { duration: 0.4, ease: "power2.out" });
});
```

- `nextLabel()` / `previousLabel()` / `currentLabel()` are the documented label navigators:
  `"Get the currentLabel() or find labels at various positions in the timeline using
  nextLabel() and previousLabel()."`
- `tweenTo()` is a *scrubbed* jump: `tweenFromTo() ... "essentially scrubs the playhead from
  a particular time or label to another time or label and then stops."` The same applies to
  `tweenTo()` — it eases the playhead there and stops, so Prev/Next never "plays through"
  the intermediate steps abruptly.
- The 0.001-second nudge keeps `previousLabel()` from returning the label you are already
  on; `tweenTo(0)` (or `seek(0)`) is the fallback at the very first step.

## Range-Input Scrubber

GSAP's docs explicitly sanction a slider on the playhead:
`"You could even attach a slider to one of these to give the user the ability to drag
forward or backward through the timeline."`

```javascript
const scrub = document.getElementById("scrub");
scrub.max = tl.duration() || 1000; // absolute seconds; use progress() for a 0..1 slider

scrub.addEventListener("input", () => {
  tl.pause();                       // a playing timeline would fight the drag
  tl.time(Number(scrub.value));     // seek without changing paused/reversed state
});

tl.eventCallback("onUpdate", () => { scrub.value = tl.time(); }); // timeline -> slider sync
```

Rules that keep it consistent:

- The timeline is the single source of truth: the slider seeks it, `onUpdate` writes the
  slider back, so the two can never drift.
- Pause before seeking so an in-flight `play()` does not override the drag.
- Use `time()` (seconds) when steps map to absolute durations; use `progress()` when you
  want a normalized control — `"0 is at the beginning, 0.5 is halfway complete, and 1 is
  complete."`

## Choosing a Scrub Primitive

All of these are documented and stable (R3 §1.4, unchanged through 3.15):

| Primitive | Behavior | Use it for |
|---|---|---|
| `seek(timeOrLabel)` | Hard jump to a time or label; paused/reversed state untouched | Instant jumps, initial state |
| `time(t)` / `totalTime(t)` | Set the playhead in seconds | Range slider in seconds |
| `progress(p)` / `totalProgress(p)` | Set the playhead as 0–1 | Normalized slider |
| `tweenTo(label)` | Eased scrub to a target, then stops | Prev/Next buttons |
| `tweenFromTo(a, b)` | `"scrubs the playhead ... and then stops"` between two points | Guided transitions |
| `play()` / `pause()` / `reverse()` / `timeScale()` | Playback control | Play/Pause button |

Docs summary: `"Tween the time(), totalTime(), progress(), or totalProgress() to fast-forward
or rewind the timeline."` The scroll-driven analogue is ScrollTrigger `scrub` (below).

## DrawSVG Stroke Animation

DrawSVG reveals or hides a stroke by animating `stroke-dashoffset` / `stroke-dasharray`:
`"Reveals or hides the stroke of SVG elements by animating stroke-dashoffset /
stroke-dasharray."` It has been free since 3.13 and was unchanged in 2025–2026.

```javascript
import { DrawSVGPlugin } from "gsap/DrawSVGPlugin";
gsap.registerPlugin(DrawSVGPlugin);

// setup: the element must already HAVE a stroke
// <path id="trace" d="M20,100 L180,100" fill="none" stroke="#111" stroke-width="2"/>

tl.to("#trace", { drawSVG: "0% 100%", duration: 0.5 }, "step1"); // draw on during the step
```

Requirements and caveats (all from R3 / the official `gsap-plugins` skill):

- **The stroke must exist first:** `"In order to animate the stroke, you must first actually
  apply one using either CSS or SVG attributes"` — set `stroke` and `stroke-width`.
- The value describes the visible segment: `"Think of the drawSVG value as describing the
  stroked portion of the overall SVG element"` and you can `"animate outward from the center
  of the stroke (or any position/segment)"`. The Quick Start uses `"0% 100%"`.
- **Fill is never touched:** `"DrawSVGPlugin does not animate the fill of the SVG at all."`
- **Prefer single-segment paths:** `"Prefer single-segment <path> elements"` — the docs ship
  a helper `"that automatically splits a multi-segment <path> into a <path> for each
  segment"`.
- **`<use>` contents are immutable** (R3's caveat list) — animate the referenced original,
  not the instance.
- **iOS Safari `<rect>` strokes:** `"As of December 2014, iOS Safari has a bug that causes
  it to render <rect> strokes incorrectly in some cases"` — prefer `<path>` on that target.
- The `"live"` measurement mode and the `getLength()` / `getPosition()` helpers remain
  stable (no 2025–2026 change found).

## Discrete Attribute Steps

Explainers often need hard, discrete changes (`cx`, `r`, `stroke-dashoffset`) rather than
interpolation. The `attr` pattern is *not* shipped by `greensock/gsap-skills` — author it
yourself:

```javascript
// hard step: zero-duration .set(), nothing interpolates mid-step
tl.set("#dot", { attr: { cx: 180 } }, "step1");

// small animated transition where you DO want movement
tl.to("#dot", { attr: { cy: 40 }, duration: 0.4 }, "step2");
```

- `attr` tweens SVG attributes directly — no markup-string rebuilding.
- For a *discrete-step* explainer prefer `.set(...)` / zero-duration tweens at label
  boundaries; save `attr` tweens for the motion you actually want the reader to see.

## easeReverse (GSAP 3.15)

3.15's one new feature is adaptive directional easing, tailor-made for scrubbing UIs:

- `"easeReverse is a new tween property that lets you define a different ease for when the
  playhead moves backwards."`
- It is tween-level and nests cleanly: `"easeReverse is a tween-level property, which works
  perfectly in timelines, no matter how deeply nested your tweens are."`
- It can live in timeline defaults: `"set easeReverse in your timeline defaults and it'll
  cascade down to the child tweens"` (docs wording per R3: `"You can also set easeReverse in
  your timeline defaults"`).
- `yoyoEase` is deprecated and auto-replaced: `"As of version 3.15.0, GSAP internally
  replaces yoyoEase with easeReverse (it's fully backwards-compatible)."`

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: {
    duration: 0.5,
    ease: "power2.inOut",
    easeReverse: "power2.inOut", // documented: set it in timeline defaults
  },
});

tl.to("#dot", { attr: { r: 12 }, ease: "power2.out", easeReverse: "power2.inOut" });
```

Why it matters here: a scrubber and a Prev button both move the playhead **backwards**.
Without `easeReverse` those reverse movements use the forward ease; with it, backwards
motion gets its own easing while forward motion keeps `ease`.

## Scroll-Driven Scrub (bonus)

The scroll-linked analogue of the range scrubber is ScrollTrigger: `"Links the progress of
the animation directly to the scrollbar so it acts like a scrubber."`

```javascript
const tl = gsap.timeline({
  defaults: { duration: 0.5, ease: "power2.inOut" },
  scrollTrigger: {
    trigger: "#figure",
    scrub: true,                    // true or a number: "seconds that the playhead should take to catch up"
    snap: { snapTo: "labels" },     // "snap to the closest label in the timeline"
  },
});
```

- `scrub` accepts `true` or a number; `snap: { snapTo: "labels" }` snaps the playhead to
  step labels, so scroll position always lands on a real step.
- **UNVERIFIED:** the ScrollTrigger import/registration path was not quoted in R3 (only the
  DrawSVG import `gsap/DrawSVGPlugin` was); registering plugins with `gsap.registerPlugin()`
  before use is standard GSAP practice.

## Caveats

- **SplitText cannot split SVG text:** `"SplitText does not support SVG <text>."` Keep
  animated text in HTML or animate whole `<text>`/`<tspan>` nodes instead.
- **GSDevTools is dev-only:** `"UI for scrubbing timelines... Use during development only;
  do not ship."` The Quick Start's buttons + slider are the shippable scrubber.
- **No shipped reference implementation:** R3 confirmed the official skills repo has no
  step-through/prev-next/scrubber example — the wiring in this skill is authored, so test it
  against your own step list.

## Common Patterns

- **Labels are step names.** `addLabel("stepN")` at every boundary; Prev/Next navigate
  labels, the slider seeks seconds. Never maintain a second, parallel step registry.
- **`tweenTo()` for buttons, `time()` for the slider.** Eased jumps feel right on discrete
  buttons; direct seeks keep a drag responsive.
- **Pause before any manual seek.** Buttons and slider handlers start with `tl.pause()` so
  playback never fights the user.
- **One sync direction via `onUpdate`.** Timeline → slider in `onUpdate`; slider → timeline
  on `input`.
- **`easeReverse` in `defaults`.** Set it once so every backwards movement eases properly,
  no matter how deeply nested.
- **Stroke everything DrawSVG touches**, prefer single-segment `<path>`s, and remember fill
  is out of scope for the plugin.
- **`.set()` for discrete steps, `attr` tweens for motion.** Zero-duration changes at label
  boundaries keep steps crisp.

## See Also

- `svg-fundamentals` - Inline SVG authoring, `viewBox`, scaling, groups, CSS, pointer coords.
- `svg-geometry` - Paths, Beziers, markers, connectors and dash arrays to draw on.
- `svg-interaction` - GSAP-free step state, renderStep(), Play/Pause/Prev/Next and sliders.
- `svg-d3-charts` - D3 7.9.0 joins, scales, axes and transitions for SVG figures.
- `svg-defs` - Reusable `<defs>` boilerplate: markers, gradients, masks, filters, text, plus the SVG.js imperative section.
