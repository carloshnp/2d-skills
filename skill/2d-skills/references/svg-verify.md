# SVG Explainer Verification

> Subskill of `2d-skills`. Headless screenshot verification for SVG explainers.

## Before you draw

Verification starts before the build, because the spec supplies the assertions. From
`illustration-spec` bring the acceptance criteria table and the inventory IDs: each DOM
id should equal its inventory ID (VIZ-<ID>) so the state dump asserts the right node,
and each Tier A gate (contrast, colour-only encoding, at-size legibility) should map to
one check here. A requirement with no test is not a requirement. Two more inputs: the
view map's element floor per view, and section 9b's state variable and INV-nn lines,
which become the state sweep.

Adapted from the `threejs-viz-delivery` loop (used for WebGL scenes) to inline-SVG
explainer pages: serve over HTTP, capture headless Chromium screenshots with
state-forcing query params, syntax-check inline scripts, review with binary vision
questions, and assert DOM state: the SVG analogue of pixel checks.

## Quick Start

```bash
# 0. Serve the work dir over HTTP (module imports/assets fail under file://).
python3 -m http.server 8000 &        # server choice UNVERIFIED; smallest standard option

# 1. Syntax-check every inline <script> BEFORE capturing.
awk '/<script/{f=1;next}/<\/script>/{f=0}f' explainer.html > inline.js  # extraction UNVERIFIED
node --check inline.js                # node --check step is verified (threejs-viz-delivery)

# 2. Capture a state-forced screenshot.
chromium --headless=new --no-sandbox --window-size=1600,1000 --hide-scrollbars \
  --virtual-time-budget=6000 --screenshot=step2.png \
  "http://127.0.0.1:8000/explainer.html?step=2&still=1"

# 3. Dump DOM state for assertions.
chromium --headless=new --dump-dom \
  "http://127.0.0.1:8000/explainer.html?step=2&still=1" > dom-step2.html
```

## Procedure

1. **Serve over HTTP.** Same rationale as `threejs-viz-delivery`: module imports and some
   assets fail under `file://`. The 3D loop's GPU software-render flags
   (`--enable-unsafe-swiftshader --use-angle=swiftshader`) are unnecessary for plain 2D SVG;
   keep `--headless=new --no-sandbox --window-size=1600,1000 --hide-scrollbars
   --virtual-time-budget=6000 --screenshot=…`.
2. **Bake state-forcing query params into the page** (`?still=1`, `?step=N`, the DIY
   rewrite of the 3D loop's `still=1`, `view=`, `steady=`). Captures are only deterministic
   if the page honours them before rendering.
3. **Syntax-check before every capture:** extract each inline `<script>` (or
   `<script type="module">`) body to a temp `.js` (`.mjs`) file and run `node --check`.
   A blank capture is almost always a JS error, not a rendering problem.
4. **Capture every state** the page can show: default, `?still=1`, and each
   `step=0…N-1`. Because a verified page has a single `renderStep`, per-step captures
   exercise the entire state machine.
5. **Review with binary vision questions, one defect per question, per state.**
   Open-ended asks ("describe this") invite confabulation. Ask pointed follow-ups against
   prior claims: vision reviewers anchor on their own earlier descriptions and report
   imaginary details (labels, colors, arrows) as fact.
6. **Settle disputes with DOM assertions**: the SVG analogue of the 3D loop's pixel
   measurements (see below).
7. **Rewrites go to a NEW file,** verified by capture, then moved over the original;
   targeted edits use patch. Never delete the last-known-good file before its replacement
   is verified. Deliver the verified file to its durable destination path in the same
   session: scratch and cache dirs are pruned and must never hold the only copy.
8. **Ground explainer facts in sourced research notes** before drawing them. Tag every
   unpublished or inferred value as unverified and never bake guessed numbers into visible
   labels: SVG `<text>` is real text, so a wrong label reads as fact in every capture.

## State-forcing query params

```javascript
// The page reads params once; renderStep stays the only DOM writer.
const q = new URLSearchParams(location.search);
const forcedStep = q.get("step");
const still = q.get("still") === "1";

if (forcedStep !== null) renderStep(Number(forcedStep)); // deterministic capture
else if (still) renderStep(step);                        // paused, current state
else startPlayLoop();                                    // normal browsing: autoplay on
```

- `?still=1` suppresses the `requestAnimationFrame` play loop so captures are
  time-independent.
- `?step=N` forces state N before first paint; the capture verifies exactly one state.
- Add further params as needed (e.g. `?variant=…`) rather than special-casing URLs.

## DOM assertions: the SVG analogue of pixel checks

Inline SVG state *is* DOM state, so most correctness claims can be measured in markup
instead of pixels:

```bash
chromium --headless=new --dump-dom "…?step=2&still=1" > dom-step2.html
```

```javascript
// assert-state.mjs: compare selector counts and attribute values across states.
import { readFileSync } from "node:fs";
const dom = readFileSync(process.argv[2], "utf8");
const count = (re) => (dom.match(re) ?? []).length;
console.log("rect marks:", count(/<rect\b/g));           // e.g. bars should equal step+1
console.log("anim on:   ", count(/(class="[^"]*\bon\b")/g));
const t = dom.match(/transform="translate\(([^)]*)\)"/g); // read attribute values
```

- **Every renderStep claim is an attribute claim:** node counts
  (`document.querySelectorAll("rect").length`), attribute values (`transform`, `d`,
  `opacity`, `class`), and step-class state. Compare against the pre-change dump and
  across `step=N` captures.
- **Mirrors the 3D noise-floor rule:** if an attribute is unchanged after a real
  geometry edit, the render is fine and the vision reviewer is anchoring on its own
  earlier description; no measured signal means the render is fine and the reviewer wrong.
- `--dump-dom` and the regex-count style are **UNVERIFIED** in the source reports (a
  standard headless-Chromium capability of the same binary the verified screenshot
  command uses); the *measure-instead-of-argue* rule itself is verified practice.
- **When the claim is raster-only** (font metrics, gradient smoothness, antialiasing),
  use the 3D loop's pixel tool from the `threejs-viz-delivery` skill,
  `~/.hermes/skills/threejs-viz-delivery/scripts/verify-screenshot.py` (`python3 verify-screenshot.py shot.png --crop
  x0,y0,x1,y1 --bins …`): mean RGB for color-cast claims, FFT bin magnitudes for
  periodic-structure claims; bins are content-specific (e.g. dash-spacing frequency).

## Auditing a tabbed page

When one page carries several full-page views behind a tab bar, a single audit run only
measures the visible tab. Loop the matrix and force the tab through a query param.

1. **Activate each tab before measuring, then restore.** A `display:none` section has
   zero-size boxes, so `getBBox()` and every overlap test return meaningless values. The
   audit sets `?tab=X`, renders, measures, and returns to the starting tab before the run
   ends, so the screenshot that follows still shows what the reader sees.
2. **Assert the routing, not just the content.** A page that ignores `?tab=` returns the
   same DOM five times and passes the whole matrix. Compare a per-tab signature (element
   count plus the first `data-k` values) and fail when two tabs match.
3. **Audit every tab at every state and every viewport.** Five tabs x six angles x three
   sizes is 90 dumps and runs in under a minute with a script; hand-running it produces a
   matrix with holes. Write `verify.py` once, print a per-tab table, and exit non-zero on
   any failure.
4. **Per-tab content tokens must come from the panel, not from the shell.** A token that
   also appears in the shell CSS (`hatch`, `pin`) is satisfied by an empty panel. Grep the
   tab's own DOM for a token only that panel emits, and take the token list from the build
   contract (the interface file the panels were written against), not from memory of what
   a panel probably draws. Even then a token proves the class exists, not that its fill
   paints: run the paint-server check too.
5. **PNG size asserts the window, not the layout viewport.** A capture requested at
   1280x720 is a 1280x720 PNG even though the page laid out at a shorter `innerHeight`;
   a passing size check says nothing about the scale labels rendered at.

## Sweeping a mechanism

A figure with a 9b mechanism section is checked at every state, not at the few angles the
matrix captures. The sweep runs inside the page under `?audit=1`: it steps the state
variable through its full range at the 9b resolution, calls the same `render(state)` the
controls call, asserts every INV-nn at each step, and writes the first failing state into
the audit title. Two invariants hold for every mechanism and need no INV line: no written
attribute is `NaN` or `Infinity`, and no part leaves the canvas at any state. One load renders all 720 states of a four-stroke cycle in milliseconds;
720 headless loads take minutes and still miss what falls between the captured angles.

- The matrix (tabs x states x viewports) checks layout; the sweep checks the model. Run
  both: neither covers the other.
- A view whose parts move by a rule and has no sweep is unverified, whatever its captures
  look like. In the V8 build only one of five views had a full sweep.
- The page audit, element floor, sweep code, driver matrix, and the failure fixtures that
  prove the harness can fail are in `references/build-harness.md`.

## Paint servers: references that paint

A token or class check proves a reference exists, not that it paints. A `url(#id)` whose
first match is duplicated, missing, or inside a `display:none` subtree paints nothing in
Chromium (see `svg-defs`, Defs across several SVGs). Check it in the page:

```javascript
// paint-server audit: a visible element whose url(#id) target is duplicated, missing,
// or inside a display:none subtree paints nothing there (measured in Chromium 154)
function paintAudit() {
  const out = [], seen = new Map();
  document.querySelectorAll("[id]").forEach((e) => seen.set(e.id, (seen.get(e.id) || 0) + 1));
  for (const [id, n] of seen) if (n > 1) out.push(`DUPID ${id} x${n}`);
  const shown = (el) => el.closest("svg").getClientRects().length > 0;
  const props = ["fill", "stroke", "clip-path", "mask", "filter", "marker-start", "marker-mid", "marker-end"];
  const refs = new Set();
  document.querySelectorAll("svg *").forEach((e) => {
    if (!shown(e)) return;                               // hidden users paint nothing anyway
    const cs = getComputedStyle(e);
    for (const p of props) {
      const m = String(cs.getPropertyValue(p)).match(/url\("?#([^")]+)"?\)/);
      if (m) refs.add(m[1]);
    }
  });
  for (const id of refs) {
    const t = document.getElementById(id);              // first match: what the renderer uses
    if (!t) out.push(`NOREF ${id}`);
    else if (!shown(t)) out.push(`HIDDENDEF ${id}`);
  }
  return out;
}
```

- **Only visible users count.** Elements in a hidden tab that reference their own hidden
  defs paint nothing either way; flagging them buries the real fault under false alarms.
  The first version of this check did exactly that.
- **Proved against a real defect.** On a five-tab page that injected one hatch pattern into
  every tab, the check reported `DUPID h45 x5` on every tab and `HIDDENDEF h45` on the one
  tab that used it, the same tab where a pixel diff found 9,540 changed pixels in the
  hatched region. With the pattern moved to one visible host, all five tabs came back
  `PAINT CLEAN`. The harness that shipped that page checked for the `hatch` class and passed.
- **When in doubt, diff pixels.** Render the view as built and with the suspect defs moved
  to a visible host; any difference confined to filled regions is a paint fault.

## Common Patterns

- **Determinism checklist:** HTTP (not `file://`), `?still=1&step=N` honoured before
  paint, no autoplay under still, `--virtual-time-budget` set, `node --check` clean.
- **Per-state vision questions** (yes/no, one defect each): "Is only step 2's edge
  highlighted?" · "Do all 8 rows appear at step 7?" · "Does the label read 'n²'?"
- **Dump-diff loop:** capture DOM at step pairs (0/1, N-1/N) and diff attribute values;
  expected diffs confirm renderStep covers the transition.
- **Anchoring defence:** when vision repeats a defect across real edits, dump DOM /
  measure pixels before editing again. When vision quotes a specific string
  ("the label reads X", "the button is empty"), grep the dumped DOM for that
  string first: reviewers invent plausible labels and miss rendered text, and a
  present-in-DOM string needs no edit.
- **Never trust a blank capture:** run `node --check` first; blank SVG areas are script
  errors far more often than paint problems.

## Field notes (defaults, not laws)
Verification is non-negotiable; the tooling below is recommended, not mandated.
Anything that checks the same properties (Playwright, pixel diffs, DOM asserts)
is fine.
- Bbox overlap audit: run the page with `?audit=1`, dump headless DOM, read
  the verdict from `<title>`: `chromium --headless=new --dump-dom
  "page.html?still=1&step=N&audit=1" | grep -o "<title>[^<]*</title>"`. Audit
  collects `getBoundingClientRect()` for figure rects/texts, ignores
  zero-area boxes and fully-contained pairs (labels inside boxes are
  correct), flags pairwise intersections over 2px. Run at the final step
  (worst case) and after every tab switch. Thresholds (2px, opacity 0.5)
  are starting points, not tolerances; tune to the figure.
- Run the audit AFTER render, never before: an init-time audit measures the
  pre-render state and reports a false CLEAN. Identical-position boxes count
  as "contained" and are skipped, so keep titles short enough to fit the
  viewBox and zone-swap (or re-layout) shared regions instead of stacking them.
- Triage audit hits before editing: `getBoundingClientRect()` is axis-aligned,
  so rotated groups (e.g. `rotate(45)` pistons, bores) report overlaps their shapes
  never make, and stroke-adjacent elements legitimately touch past 2px. Fix hits
  where a shape escapes its container (flame out of the gas rect, text out of its
  box) and confirm the rest against the screenshot: a layered engine cross-section
  can report 20+ hits with nothing visually wrong.
- Headless captures freeze animation clocks at t=0 (observed): design every
  animated element so its frozen state reads sensibly, and never gate static
  visibility on animation state. In the tested build, `feGaussianBlur`
  filters suppressed rendering entirely; prefer layered translucent shapes,
  and verify any filter in the capture pipeline, not just a live browser.
- **`--window-size` is the window, not the viewport.** Headless Chromium reports an
  `innerHeight` smaller than the requested height, so a scale computed from the window
  size overestimates how large labels and strokes render. Compute the scale from
  `svg.getBoundingClientRect()` against its `viewBox`, and print `innerWidth x innerHeight`
  in the audit verdict so a floor failure can be read at the size it happened. A label
  measured at exactly the 11 px floor is usually a float just under it: raise the size at
  the smallest audited viewport instead of loosening the check.
- **Element counts: descendants, not children.** `childElementCount` reports 2 for a panel
  that mounts one `<g>` holding 300 elements. Use `querySelectorAll("*").length`, and
  prefer semantic selectors over class names invented by a different author.

## See Also

- `svg-explainer-layout` - Composing the HTML+SVG explainer pages this loop verifies.
- `svg-fundamentals` - Inline SVG authoring, `viewBox` discipline, pointer conversion.
- `svg-interaction` - Step state, sliders, scrubbers: the state machine being verified.
- `svg-geometry` - Paths, Beziers, markers and dash arrays for the figures under test.
- `svg-d3-charts` - D3 joins, scales and axes for data-driven cards.
- `svg-animation` - Timeline-driven SVG animation with a scrubbed playhead.
- `svg-defs` - Reusable `<defs>` boilerplate plus the SVG.js imperative section.
- `illustration-spec` - its build-harness reference (`references/build-harness.md`): page audit, sweep, driver, fixtures.
