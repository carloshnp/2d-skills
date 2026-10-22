# Drawing a batch of static sheets

Use when the specs are approved and the deliverable is N standalone SVG files that a site
or print pipeline rasterises, rather than interactive panels. The spec side is
`spec-set-orchestration.md`; this file is the drawing side.

## 1. One shell, one class table

One self-contained SVG per figure. No external references, no filters, no gradients, no
`foreignObject`; a `<style>` block with role classes and the full-bleed card rect first, so
a light sheet on a dark page reads as a plate and not as a hole.

- **Write literal hexes in the CSS.** librsvg resolves `var(--x, fallback)` to the fallback
  and drops a custom property with no fallback, so a class palette built on CSS variables
  renders unstyled. Literal hexes also make palette containment auditable.
- **Root carries `viewBox`, `width`, `height`, `role="img"`, `<title>` and `<desc>`.** The
  desc is the message sentence; the caption lives in the page's alt text, never both here.
- **Markers per role** (`head-muted`, `head-accent`, `head-warning`, `head-success`), sized in
  canvas units, `orient="auto-start-reverse"` so one marker serves both directions.
- **`data-view` on every view group and `data-el` on every element that carries an inventory
  id.** This is the whole traceability mechanism: an audit can then prove each spec row
  reached the drawing, count elements per view against its floor, and catch an inventory row
  that never got drawn.

## 2. Prove the toolchain before the fan-out

- **Probe the rasteriser, then look at the PNG.** A twenty-line probe with a class-based
  style block, a marker, a dash pattern, a `text-anchor` and two font weights answers in one
  render whether the CSS you plan to write survives. Do not assume any of it; the same
toolchain can honour classes and ignore variables.
- **Confirm the intended family resolves:** `fc-match "<Family>"`. A substituted font
  invalidates every type size, label fit and measure the specs assert, and the render looks
  fine.
- **Install a webfont for fontconfig when the site ships only woff2.** `pip install fonttools
  brotli`, read the woff2 with `TTFont`, pin the weight instance with
  `fontTools.varLib.instancer.instantiateVariableFont(font, {"wght": 400})`, then fix the name
  table: with `updateFontNames=False` the file keeps the variable font's default instance
  name (`Family Thin`) and matches nothing. Rewrite name IDs 1, 2, 4, 6, 16 and 17, set OS/2
  `usWeightClass` and the `fsSelection` bold/italic bits, write the TTF into
  `~/.local/share/fonts/<family>/`, run `fc-cache -f`, and re-check with `fc-match`.

## 3. Canary, then fan out

- **One agent draws the smallest sheet first.** Rasterise it and look before dispatching the
  rest: a flaw in the shell or the class table then costs one file, not N.
- **Then one agent per figure, all in one batch.** Each reads the interface in full, writes
  only its own file, runs the audit to `ok`, rasterises once, and reports the audit line plus
  the raster path. A child reporting success from a file that exists has not rendered it.
- **Keep the swarm wide when the requester asked for one.** Serialising to save tokens is the
  wrong trade for a set: the wave boundary is the only serialisation.

## 4. The set-level SVG audit

One script, run on every file, exiting non-zero on the first failure. Checks that pay for
themselves:

- parses; `viewBox` width equals the locked canvas; view groups present in spec order
- every inventory id from the spec's section 6 appears as a `data-el`, and every `data-el`
  exists in the inventory (both directions, or a dropped row hides)
- per view: live element count at or above its floor and under the node budget
- every hex value inside the locked palette; reject three- and eight-digit forms
- every `<text>` carries an explicit `font-size` at or above the floor, label length at or
  under the cap, no em dash and no en dash
- forbidden tags and attributes absent: `script`, `foreignObject`, `filter`, gradients, any
  external `href` or `url()`
- print per file: views against floors, ids drawn over ids declared, file size in kB

A clean run proves transcription, not composition. Look at every rendered sheet anyway;
the audit cannot see a wrong projection, a label pointing at the wrong part, or a state
painted with the wrong role.

## 5. Delivery is part of the contract

- **A raster figure cannot follow a class-based theme.** One asset holds one palette. Either
  plan two rendered variants plus the manifest and component change they need, or decide one
  theme explicitly and say which, with what the other theme will look like.
- **Rasterising at a fixed width makes font, label size and measure part of the deliverable.**
  Record the output widths and the source-to-raster rule in the interface so the next
  revision does not silently change the type size.
- **Put the render command in the interface and make the child run it**, e.g.
  `rsvg-convert --width 1000 --format png --output <fig>.png <fig>.svg`.

## Pitfalls

- **A helper script named like a stdlib module shadows it.** Python puts the script's own
  directory first on `sys.path`, so `inspect.py` beside a fontTools helper breaks an import
  inside the dependency. Run helper scripts from a directory with no such names, or rename the
  file.
- **`updateFontNames=False` is not "leave the names alone".** It leaves the variable font's
  default instance name, which is usually the thinnest weight, so `fc-match` fails and the
  render falls back while reporting success.
- **A missing fallback makes `var()` invisible.** The class is present in the DOM, the cascade
  looks right, and the shape renders in the default black fill; nothing warns.
- **Do not promise both themes for one raster.** The delivery pipeline renders one image per
  figure, so a dual-palette promise is a component change, not a drawing change.
- **A green audit plus one screenshot is not a review of N sheets.** The defect that survives
  a set audit is cross-sheet: the same graph laid out differently, a role meaning changed, one
  sheet at a different type size.
