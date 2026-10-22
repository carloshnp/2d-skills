---
name: 2d-skills
description: Use when planning or drawing 2D SVG figures and explainers.
version: 2.0.0
author: Carlos Pereira
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [illustration, svg, diagram, technical-drawing, explainer, animation, charts, spec]
    homepage: https://github.com/carloshnp/2d-skills
    related_skills: [spec-driven-development, threejs-viz-delivery, code-drawn-illustration]
---

# 2D Skills

One skill with nine subskills for planning and building 2D illustrations in SVG: technical
figures, mechanism explainers, charts, step-through pages, and sets of static sheets.

**This skill is a router.** The body says which subskill to load; the subskills hold the
rules. Load one with:

```
skill_view(name="2d-skills", file_path="references/<subskill>.md")
```

A name in backticks such as `svg-verify` means the subskill file `references/svg-verify.md`.
Inside a subskill, "this skill" means that subskill. Before 2.0.0 the nine subskills were
separate skills; `skill_view(name="illustration-spec")` no longer resolves, so use the path
above.

## Start here

- **A figure that carries an argument, will be reviewed, or will be built by agents:** load
  `illustration-spec` first and write the spec before the first mark. It decides what to draw;
  the `svg-*` subskills decide how.
- **A fix to an approved figure:** load only the subskill for the layer at fault and patch the
  offending geometry. Never regenerate an approved view: a drop of more than ten percent in its
  element count is lost work.
- **A set of figures for one chapter or deck:** `illustration-spec`, then
  `references/spec-set-orchestration.md` for the specs and `references/svg-raster-batch.md`
  for drawing static sheets.
- **Detail defaults to full.** Reduced detail is chosen only when asked for, and legibility
  floors hold either way.

## Subskills

| Subskill | Load when the work is |
|---|---|
| `illustration-spec` | deciding before drawing: message, view map with element floors, requirements with standing, mechanism and state model, acceptance tests, gates |
| `svg-fundamentals` | the canvas: viewBox, scaling, groups, CSS, pointer coordinates, stroke and text floors converted to CSS pixels |
| `svg-geometry` | shapes: paths, Beziers, markers, connectors, dashes, cylinders in section versus end view, geometry derived from the model |
| `svg-defs` | reusable resources: markers, gradients, patterns, masks, filters, one shared defs host with unique ids |
| `svg-explainer-layout` | the page around figures: cards, tabs per view, reading order, traces, accessibility |
| `svg-animation` | GSAP 3.15 paused timelines that tween one state variable for step-through explainers |
| `svg-interaction` | steps, scrubbers and sliders bound to the shared state, never a second source of truth |
| `svg-d3-charts` | D3 7.9.0 data binding for charts computed from the same model as the drawing |
| `svg-verify` | headless screenshots, DOM assertions, the full state sweep, the paint-server audit |

## Which subskill builds which spec section

| Spec section (`illustration-spec`) | Subskill |
|---|---|
| 4 canvas, 9 text split | `svg-fundamentals` |
| 5 line grammar, 8 composition geometry | `svg-geometry` |
| 5 palette, arrow semantics, filters | `svg-defs` |
| page and panel structure | `svg-explainer-layout` |
| 9 steps and timing | `svg-animation` |
| 9 interaction | `svg-interaction` |
| 6 encoding, shared scales, small multiples | `svg-d3-charts` |
| 9b state model, invariants | `svg-animation`, `svg-interaction`, `svg-verify` |
| 10 acceptance, DOM assertions | `svg-verify` |

Order of work: spec, canvas, geometry and defs, page, motion and charts, verification. Each
gate in `illustration-spec` passes before fidelity rises.

## Supporting references

Loaded from the subskill that names them, not on their own.

| File | Carries | Named by |
|---|---|---|
| `references/build-harness.md` | page audit, element floor, in-page state sweep, driver matrix, paint-server audit, fixtures that prove the harness can fail | `illustration-spec`, `svg-verify` |
| `references/delegated-illustration-build.md` | contract file, one module per view, test pages, the review round | `illustration-spec` |
| `references/spec-set-orchestration.md` | sets of specs by delegated writers: roster row, shared geometry, dual theme palette, wave audits, set verifier, `check_spec.py` traps | `illustration-spec` |
| `references/svg-raster-batch.md` | standalone SVG sheets: shell, data attributes, set level SVG audit, canary order, rasterising with the intended font | `illustration-spec` |
| `references/technical-sheet-conventions.md` | projection, line grammar, detail callouts, materials labels, accuracy ledger | `illustration-spec` |
| `references/evidence-and-folklore.md` | every rule with its standing and source, and the claims kept out of specs | `illustration-spec` |
| `references/research-method.md` | how a rule earns its standing; change control for plans and rules | `illustration-spec` |
| `references/cad-mechanical-sections.md` | dimensioned CAD style mechanical sections | `svg-geometry` |

## Scripts

| Script | Use |
|---|---|
| `scripts/check_spec.py` | mechanical audit of a spec before it is presented; exits non-zero on any finding |
| `scripts/svg_bounds_and_type_check.py` | elements outside their viewBox, and effective type size at the column width the figure lands in |

Run them from the installed skill:

```bash
python3 ~/.hermes/skills/2d-skills/scripts/check_spec.py specs/FIG-01.md
python3 ~/.hermes/skills/2d-skills/scripts/svg_bounds_and_type_check.py --column-px 350 --floor 11 svg/*.svg
```

## Where the rules come from

Every rule carries a standing (STANDARD, TAUGHT, PRACTICE, OPINION) and a source in
`references/evidence-and-folklore.md`. The research behind them lives outside this skill, in
the 2d-research workspace: `planning/P1..P7`, `planning/SYNTHESIS.md`, and
`planning/corpus-map.md` (rule to report line). The skill carries the distilled rules, not the
reports.

## Changing this skill

The installed copy is generated from the repository (https://github.com/carloshnp/2d-skills),
where `skill/2d-skills/` is this folder. A lesson learned mid-task may be patched in place with
`skill_manage` (`name="2d-skills"`, `file_path="references/<file>.md"`); `sync.sh --check`
reports the drift, `sync.sh --pull` copies it back into the repository, and `sync.sh` refuses
to install over drift that has not been pulled.
