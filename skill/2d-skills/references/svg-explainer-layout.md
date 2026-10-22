# SVG Explainer Layout

> Subskill of `2d-skills`. HTML+SVG explainer pages: cards, tabs, traces, a11y.

## Before you draw

A page is a composition before it is a layout. From `illustration-spec` bring the
figure inventory with one message per figure, the panel order and its justification,
the reading entry point for each figure, and the acceptance test each figure must
pass. A card grid organises figures that already have a job; it cannot supply the job.
The view map supplies the page structure: views in reading order, what each depends on,
and each view's element floor. At `detail: full` (the default), a view that needs height
for its detail gets its own full-page tab rather than a band in a grid.

## Quick Start

One minimal, self-contained explainer page: responsive figure cards around inline SVG, a
step control panel, and a code trace. Everything a reader may copy, search, or hear
stays real DOM text.

```html
<!doctype html>
<title>Cumulative sum, explained</title>
<style>
  /* Page shell (flex/grid) is UNVERIFIED against the source reports; any layout
     that yields "card + caption + controls" blocks works. What IS verified:
     the figure CSS below (Distill GP: svg{width:100%;height:auto}). */
  body  { max-width: 720px; margin: 2rem auto; line-height: 1.5; }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
  .card { border: 1px solid #ccc; border-radius: 8px; padding: 0.75rem; }
  .card svg { width: 100%; height: auto; display: block; } /* viewBox never changes */
  .controls button { min-width: 4rem; }
</style>

<h1>Cumulative sum, explained</h1>
<p>Prose lives in HTML. Only short labels go inside SVG <code><text></code>.</p>

<div class="cards">
  <section class="card">
    <svg viewBox="0 0 200 120" role="img" aria-label="running total after each step">
      <g id="scene"></g>
      <text x="10" y="14" font-size="10">running total</text>
    </svg>
  </section>
  <section class="card">
    <svg viewBox="0 0 200 120" role="img" aria-label="input items">…</svg>
  </section>
</div>

<div class="controls">
  <button id="prev" title="Previous step">Prev</button>
  <button id="play-pause" title="Run/Pause">Play</button>
  <button id="next" title="Step">Next</button>
  <button id="reset" title="Reset">Reset</button>
  <span id="iter-number">step 0</span>
</div>

<pre class="code-trace"><code id="trace">…highlighted source line(s)…</code></pre>

<script>
  // Step state: one integer is the source of truth; renderStep is the ONLY
  // DOM writer (TensorFlow Playground routes every control through oneStep()).
  const STEPS = 5;
  let step = 0, playing = false;
  function renderStep(s) {
    document.querySelector("#iter-number").textContent = `step ${s}`;
    // sequencing classes (authored convention, UNVERIFIED):
    document.querySelectorAll(".anim").forEach((el) =>
      el.classList.toggle("on", Number(el.dataset.step) <= s));
    // trace highlighting rides the same render path:
    highlightTrace(s);
    drawScene(s); // write SVG attributes (d, cx/cy, transform, opacity); never innerHTML
  }
  document.querySelector("#prev").onclick = () => renderStep(Math.max(0, --step));
  document.querySelector("#next").onclick = () => renderStep(Math.min(STEPS - 1, ++step));
  document.querySelector("#reset").onclick = () => renderStep(step = 0);
  document.querySelector("#play-pause").onclick = () => { /* raf loop calls next() */ };
  renderStep(0);
</script>
```

## Anatomy of verified reference explainers

| Explainer | Composition evidence (R5, opened 2026-10-17) |
|---|---|
| Distill, "Visual Exploration of Gaussian Processes" | 11 `<d-figure>` custom elements as figure mount points; figures scale by `svg.svelte-1gc1gg1{width:100%;height:auto}` while each SVG keeps its `viewBox` (set 25 times); sliders + drag handles. |
| TensorFlow Playground | One fixed-pixel inline SVG for the network (`<svg id="svg" width="510" height="450">`, no `viewBox`, a legacy exception) beside `<canvas>` data; button panel Play/Pause (`title="Run/Pause"`), Step (`title="Step"`), Reset, plus `#iter-number` readout. |
| Red Blob Games, A* | Page of many small figures: 17 `<svg>` tags, 16 carrying one reused `viewBox="-55,-55 110,110"`; per-figure toggle buttons (`id="diagram-early-exit-true"` / `-false`); `aria-label="start location blob"` on SVG icons; 21 `<canvas>` panels. |
| Setosa, Markov Chains | Ten `<input>` controls; heavy demo isolated in `<iframe src="…/markov/playground.html">`. |
| Distill t-SNE | Control-panel reference: `.play-pause`, `.restart`, `#tray-steps-display` step counter (figures are canvas). |
| Transformer Explainer | `type="range"` sliders (temperature, top-k, and a `min="0" max="17"` state selector); `role="img"`, `aria-hidden="true"` on SVGs. |

## Page composition: cards around inline SVG

- **One page, many figures, one coordinate space.** Red Blob repeats the same
  `viewBox` across grid diagrams so one unit = one grid cell everywhere; give every
  figure its own fixed `viewBox` (see `svg-fundamentals`).
- **Responsive scaling:** `.card svg { width: 100%; height: auto; }`; width follows the
  column, the `viewBox` never changes (Distill GP CSS, accessed 2026-10-17).
- **Figure mount points:** wrap each figure in a section/card; Distill uses `<d-figure>`
  custom elements the same way.
- **Isolate heavy demos:** mount a dense interactive demo in an `<iframe>` like Setosa
  Markov, so its scripts/styles don't infect the article chrome.
- **Hybrid split:** inline SVG for diagrams/chrome/labels, `<canvas>` for dense marks
  (TensorFlow Playground, Red Blob); stay on SVG up to ~1,000 live elements
  (ApexCharts/Felt numbers; switch to canvas for tens of thousands).
- **UNVERIFIED:** the card/grid CSS itself (flex vs grid, gutters, breakpoints); no
  source report covers page-level layout; only the figure CSS above is sourced.

## Step state and control panel

- A single integer state + one `renderStep(state)` that touches the DOM; Prev/Play/Step/Reset
  and any scrubber only mutate the index (R5 agent rule, from `oneStep()` and scrollama
  `data-step`).
- Give each button a `title` ("Run/Pause", "Step") and a visible step readout span
  (`#iter-number`, `#tray-steps-display`, both verified in shipped explainers).
- Play loops via `requestAnimationFrame`/timer calling the same `next()`; no second render path.
- **UNVERIFIED:** a dedicated timeline scrubber was searched and not found in the wild
  (R5 "Not confirmed"). Verified substitutes: bind `<input type="range" min="0" max="N-1" step="1">`
  straight to `step` (Transformer Explainer's state selector) or show a counter.

## Sliders writing SVG attributes

- `<input type="range">` with `min/max/step` clamping in HTML so JS needs no validation;
  knob/interval logic stays in the model (TF Playground noise slider `min="0" max="50" step="5"`).
- Listen on `input`, not `change`, so the SVG tracks continuously; recompute a pure model
  `f(params) -> geometry`, then write attributes only (`d`, `cx/cy`, `transform`,
  `opacity`, `stroke-width`); never rebuild markup strings.

## Code-trace blocks and `.anim` sequencing

- **Code traces:** show the executing code as a `<pre><code>` block and highlight the line
  for the current step inside `renderStep()`. The widget itself is an authored convention
  (**UNVERIFIED**: no source report shows one), but it must be DOM text, not painted pixels:
  SVG/DOM text is "searchable, selectable, and accessible by screen readers" (dev.to,
  2026-10-13), so captions and traces a reader may copy stay in text nodes.
- **`.anim` sequencing classes:** mark elements that appear/change at a step with
  `class="anim" data-step="N"`; `renderStep` toggles an `is-on` class. Authored convention,
  **UNVERIFIED**; the verified core underneath is step-index-driven rendering via one
  `renderStep` (TensorFlow Playground `oneStep()`, scrollama `data-step`).
- **UNVERIFIED:** tab toggles as a widget (tablist semantics). The verified primitive is
  per-figure state-toggling buttons (Red Blob `id="diagram-early-exit-true"` / `-false`);
  implement tabs as a plain button row toggling one visible pane unless another source is found.
  The full-page tab layout in the next section is verified by a built headless page, not by
  a published source.

## Full-page tabs

Use when several views must each reach the same detail: one view per tab, each owning the
whole viewport, instead of bands that cap how much any one view can hold.

- **Markup:** one `<section role="tabpanel">` per view, each `position:absolute; inset:0`,
  hidden with `display:none` and shown by a class. A `<div role="tablist">` of
  `<button role="tab" aria-selected>` in the header, never links.
- **One canvas per tab, same viewBox.** Every tab's SVG is `width:100%;height:100%` with the
  same `viewBox`, so one stroke weight and one label floor serve all views. Different
  viewBoxes per tab quietly change the unit scale and the legibility floor with it.
- **State lives in the shell, not the tab.** One angle/step variable, one `render(state)`
  called on every switch as well as on every state change, so a tab reopened at a new
  angle shows the new angle. Restore the previously active tab after any internal loop.
- **URL params for every state:** `?tab=C&angle=90&audit=1` makes any tab capturable
  headlessly; without a `tab` param a verify loop measures the same view five times.
- **Keys 1..5 and arrow keys.** A tab bar that only responds to the mouse cannot be
  driven in a demo or by a scripted check.
- **Caption per tab.** No two views are ever seen together, so each tab carries its own
  scale and its own reading; a header caption carries only the figure's message.
- **Shared defs outside the tabs.** A pattern, gradient, marker, or clip path defined inside
  a `display:none` tab paints nothing anywhere else, and a duplicated id resolves to the
  first copy even when it is hidden. Inject shared defs once into a zero-size visible SVG
  before the tabs mount (`svg-defs`, Defs across several SVGs). In one five-tab build the
  same hatch pattern was injected into every tab, and the one tab that used it rendered its
  section unhatched while every audit passed.
- **Element floor per tab, from the view map.** The audit counts descendants of each tab's
  SVG (`querySelectorAll("*").length`) against its floor, so a tab that comes back simpler
  after a rewrite fails a number instead of passing a glance.
- **Tab letters in reading order**, matching the view map, so "tab C" means the same view in
  the spec, the harness, and the review notes.

## Accessibility and text-first typography

- Everything narrative is real text: prose in HTML, short labels in SVG `<text>`. Canvas is
  not a fallback: "Canvas content is not exposed to accessibility tools as semantic HTML is."
  (MDN, accessed 2026-10-17).
- Each figure gets `role="img"` + `<title>`/`aria-label` (Red Blob `aria-label="start location blob"`)
  or `aria-hidden="true"` when adjacent prose already says it (Transformer Explainer); complex
  figures need a complete text equivalent (W3C WAI Images tutorial: "graphs and diagrams").
- Typography choices (families, sizes, measure, spacing) are **UNVERIFIED** beyond the
  references being text-heavy articles that keep figures subordinate to prose.
- Focus styling on buttons/sliders: keep default browser focus or an explicit CSS `:focus`
  ring: the reports cover ARIA attributes only; keyboard-focus conventions are **UNVERIFIED**.

## Common Patterns

- **ViewBox discipline:** fixed internal space, declared once, browser scales it; pointer
  events convert once via `getScreenCTM().inverse()` at the boundary.
- **Slider → attr:** `input` events → pure model → attribute writes; clamp in HTML.
- **Text-first:** anything copyable/searchable/hearable lives in DOM text, never canvas.
- **The distill of it:** card + caption + controls is the pattern shipped by every reference
  explainer; the specific CSS is yours (**UNVERIFIED**).

## Verifying the page

After building or changing the page, verify with headless screenshots + DOM assertions per
state; the loop lives in `svg-verify`.

## Field notes (defaults, not laws)
Provenance: two built explainers (transformer stepper, AZ92A tabbed process).
MUSTs are load-bearing; everything else is a starting point: a different control
scheme, trace design, or reveal style that serves the same purpose is a win,
not a violation.
- MUST: trace code must be REAL (the page's own logic or a real recipe), never
  illustrative pseudocode. Readers copy it; a wrong line reads as fact.
- DEFAULT: controls live with the figure they drive (in-card bottom, or one set
  per tab pane). The principle is proximity plus one shared state per figure:
  a global bar, scroll-driven progress, or keyboard-first scheme honoring that
  is equally good. Improve freely.
- DEFAULT: full-canvas scene steps use EXCLUSIVE reveal (`=== step`);
  progressive builds use cumulative reveal with dimmed context. Stacked full
  scenes garble; match the reveal to the composition, not to this text.
- EXAMPLE: ~15-line regex highlighter run once on load (split `//` comments
  first, then escape, strings, keywords, numbers). Any highlighter (library,
  pre-rendered, or hand-rolled) is fine as long as trace text stays DOM text.
- MathJax 3 CHTML for formulas in HTML text (see `svg-fundamentals` for the
  `tex-svg.js` ban and the `tspan` rule).

## See Also

- `svg-fundamentals` - Inline SVG authoring, `viewBox`, scaling, groups, CSS, pointer coords.
- `svg-interaction` - Step state, sliders, scrubbers: the control layer these panels host.
- `svg-verify` - Headless verification loop for the finished explainer page.
- `svg-geometry` - Paths, Beziers, markers, connectors and dash arrays for figures.
- `svg-d3-charts` - D3 joins, scales and axes for data-driven cards.
- `svg-animation` - Timeline-driven SVG animation with a scrubbed playhead.
- `svg-defs` - Reusable `<defs>` boilerplate plus the SVG.js imperative section.
