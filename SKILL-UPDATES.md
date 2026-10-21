# Proposed skill updates (from transformer.html test build, 2026-10-17)

Status: DRAFT for review. Each item names the target skill file and the exact
addition. Proven in `test/transformer.html` unless marked otherwise.

## 1. LaTeX formulas via MathJax (`svg-explainer-layout`, `svg-fundamentals`)

- Formulas are real LaTeX rendered with MathJax 3 (CHTML output:
  `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js`), not
  hand-drawn SVG text and not Unicode approximations (`&radic;`, `<sub>`).
- Do NOT use the `tex-svg.js` output: its `<svg>` sizes itself in `ex`
  units, which some Chromium builds ignore, collapsing the graphic to full
  container width (a small inline root rendered 6-8x oversized in testing).
  CHTML sizes in CSS and is robust. If SVG output is ever required, verify
  inline-math height against surrounding text with a cropped screenshot.
- Recipe: `\(...\)` delimiters configured via
  `window.MathJax = { tex: { inlineMath: [['\\(','\\)']] } }`,
  script `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js`.
- Raw TeX stays readable if the CDN fails, so the page degrades gracefully.
- Inside SVG `<text>`, keep `tspan` subscripts instead: headless Chromium
  renders Unicode subscripts (U+2080+) as tofu. MathJax handles HTML text only.
- Cap inline math size (`mjx-container { font-size: 100%; }`) so notes don't blow up.

## 2. Controls live inside the figure card (`svg-explainer-layout`, `svg-interaction`)

- Prev/Play/Next + scrubber + readout + caption sit at the bottom of the
  pipeline card, not in a floating global bar. One card = one self-contained
  demo a reader can operate without scrolling.
- Same single-`renderStep()` wiring; only the markup position changes.

## 3. Trace shows real code with highlighting (`svg-explainer-layout`)

- The trace is the page's own logic (softmax, renderWeights), not pseudocode.
  Each `.ln` line keeps its `data-step` highlight behavior.
- Highlighting is a ~15-line regex highlighter run once on load (split `//`
  comments first, then escape, then strings, keywords, numbers). No external
  library, survives offline. Verified pattern in test file.

## 4. Programmatic overlap audit (`svg-verify`)

- New required check before any visual sign-off: run the page with `?audit=1`,
  dump the DOM headless, read the overlap verdict from `<title>`:
  `chromium --headless=new --dump-dom "page.html?still=1&step=N&audit=1" | grep -o "<title>[^<]*</title>"`
- Audit snippet (runs in-page): collect `getBoundingClientRect()` for
  `#pipe rect, #pipe text`, ignore zero-area boxes, flag pairwise
  intersections over 2px, exempt full containment (labels inside boxes are
  correct, not overlaps). Title becomes `OVERLAP-AUDIT CLEAN` or lists hits
  with pixel sizes.
- Run at the final step (all groups visible = worst case). Vision review
  stays for taste, never for geometry.
- Audit only what the reader can see: walk each candidate's ancestors and
  skip nodes under `opacity < 0.5` (dimmed future steps, swapped-out groups).
  Proven in `test/az92a.html` (`runAudit` + `vis()`).
- Companion pattern: zone swapping. When two groups share one zone across
  steps (composition bars steps 0-4, precipitate scheme step 5), toggle a
  `swap` class on the SVG at the cutoff step with a high-specificity rule
  (`#pipe.swap #compZone { opacity: 0; }`) instead of stacking them.

## 5. Schematic curves with measured markers (from AZ92A rebuild)

- When full numeric series are unavailable, draw schematic age-hardening
  curves on a log-time axis and mark ONLY the sourced peak points with dots
  plus value labels; y-axis carries no other numbers. State the convention in
  the figure caption (curves schematic, markers measured, with source).
- Smooth the schematic with a Catmull-Rom-to-Bezier pass through the
  anchor points; verify dot-on-curve coincidence numerically from
  `--dump-dom` (circle cx/cy vs path data), not by eye.
- Drawn microstructure follows the same honesty rule: dendrite trees,
  globular grains, DP fans and CP dots are generated schematically from
  literature descriptions (divorced eutectic network, dissolution at
  ~410 C, DP from grain boundaries + CP interiors), captioned as schematic.
## 6. Audit discipline learned on the AZ92A rebuild

- Run the audit AFTER render, never before: an init-time audit measures the
  pre-render state and reports a false CLEAN. Wire it at the end of the
  render path (and after tab switches), not at startup.
- Full-canvas steps need EXCLUSIVE reveal (`=== step`), not cumulative
  (`<= step`): stacked scenes garble each other. Inactive full-scene groups
  must be opacity 0, not dimmed: 0.15 ghosts show through in screenshots
  (dimming is only for progressive-build diagrams).
- Identical-position boxes defeat containment exemptions: two titles at the
  same coordinates count as "contained" and are skipped. Keep titles short
  enough to fit the viewBox (long titles overflow and read as garbling).
- Make hits self-locating: report each element's tag plus its SVG-unit
  x/y/w/h (not CSS pixels), so a hit maps straight back to the drawing.

## 7. Layout rule that fell out of the transformer fix (`svg-geometry`)

- Right-hand annotation columns (scores, weights, output) need vertical
  budget planned up front: mini-bars plus labels plus the output box did not
  fit in 340 units. Prefer stacking (scores / weights / output top to
  bottom) over squeezing beside the flow.

## 8. Headless rendering rules (from AZ92A smoke debugging)

- Headless captures freeze animation clocks at t=0. Design every animated
  element so its frozen state is a sensible still: pour streams read as
  streams, the rising cavity fill reads as "just started", dimmed-but-visible
  states must never carry information the step needs.
- Never gate static visibility on animation state. An opacity animation that
  starts at 0 hides the element in every screenshot; prefer a static base
  opacity and animate only transform (or nothing).
- `feGaussianBlur` filters suppressed rendering entirely in headless
  Chromium: filtered elements came out invisible while unfiltered twins
  rendered. Prefer layered translucent shapes over blur; if a filter is
  used, verify it in the actual capture pipeline, not just a live browser.
- When an element will not render, bisect with a solid-color static control:
  first remove animation, then remove the filter. The step that makes it
  appear names the culprit.


## 9. Planning gate in every builder skill (new `illustration-spec`, all eight)

- New ninth draft skill `illustration-spec` holds the pre-drawing discipline: the
  eight-decision spine, a twelve-question fast path, a fill-in spec template with
  twelve sections, gates G0-G5, acceptance tests in three tiers, a folklore blacklist,
  and the free parameters a spec must declare as local law. It is loaded BEFORE any
  builder skill.
- Each of the eight builder skills now opens with a `## Before you draw` block naming
  the three or four spec outputs that skill consumes. The block is a pointer, not a
  second copy of the theory: duplicating rules across eight files is how they drift.
- Placement rule: directly under the H1, above `## Quick Start`, under nine lines, so
  it is read before the first code sample.
- The join between planning and building is the ID contract: content-inventory IDs
  become DOM ids (VIZ-<ID>), which become the assertions `svg-verify` runs.
