# Changelog

One version for the whole skill from 2.0.0 on. Entries name the subskill each change
touches.

## 2.0.0 (2026-10-22)

The nine skills become one skill, `2d-skills`, with nine subskills.

- **Layout.** Each former `SKILL.md` is now `references/<name>.md` under one router
  `SKILL.md`; supporting references sit beside them, both scripts in `scripts/`. Installed
  at `~/.hermes/skills/2d-skills/`. `skill_view(name="illustration-spec")` and the other
  eight names no longer resolve; load
  `skill_view(name="2d-skills", file_path="references/<name>.md")`.
- **2d-skills.** Router: where to start, the subskill table, the spec section to subskill
  map, supporting references, scripts, where the research lives, how in-place edits return
  to the repo. Author: Carlos Pereira.
- **illustration-spec.** Spec sets, the raster batch reference and
  `svg_bounds_and_type_check.py`, written into the installed copy on 2026-10-22 by the DSA
  chapter figure session and imported verbatim. The Spec sets bullets and the delegated build
  rules that repeated their references became pointers; the two sentences found only in the
  skill moved into `delegated-illustration-build.md`. 597 lines, inside its 400 to 600
  budget.
- **All subskills.** YAML frontmatter replaced by one header line that keeps the trigger
  description. `svg-verify` points at `references/build-harness.md` directly.
- **repo.** `sync.sh` installs one folder atomically, keeps its baseline in the install,
  labels drift `STALE`, `EDITED` or `CONFLICT`, refuses to overwrite in-place edits, adds
  `--pull` and `--remove-legacy`. `validate.py` checks the router, subskill headers and
  routing coverage, and follows moved files in its shrink check.

## Before 2.0.0: one version per skill

### illustration-spec

- **1.3.2** (tag `illustration-spec-v1.3.2`). Sources named behind each standing: ISO and
  ASME rows marked scope only where the clause was never opened; line weights cite the
  opened ASME Y14.2-2008 ("approximately 2:1"); lettering split into STANDARD and TAUGHT.
- **1.3.1** (tag `illustration-spec-v1.3.1`). Paint-server audit added to the build harness.
- **1.3.0** (tag `illustration-spec-v1.3.0`). Nine-decision spine with "How it moves",
  thirteen-question fast path, section 9b mechanism and state model, view map with element
  floors, `detail: full | reduced`, MUST-STANDARD, MUST-LOCAL and SHOULD, assumptions and
  boundaries, the spec-driven development adaptation, build harness, research method,
  evidence and folklore references, `check_spec.py` support for all of it.

### svg-* (1.1.0, untagged)

- **svg-fundamentals.** View map, `detail: full` default, stroke and text floors converted
  to CSS pixels at the smallest specified viewport.
- **svg-geometry.** Cylinders in section versus end view, geometry derived from the
  mechanism model, hidden versus faint, patch instead of regenerate.
- **svg-defs.** One shared defs host with unique ids; a pattern defined only in a hidden
  tab does not paint.
- **svg-animation.** Timelines tween one state variable; the model places the parts.
- **svg-interaction.** Controls bind to the section 9b state, never a second source of truth.
- **svg-d3-charts.** Series computed from the same model; cyclic intervals split at the wrap.
- **svg-explainer-layout.** The view map sets reading order, dependencies and element
  floors; full-detail views get full-page tabs.
- **svg-verify.** In-page sweep over the whole state range with INV-nn assertions, and the
  paint-server audit.
