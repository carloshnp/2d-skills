# 2d-skills

Hermes skills for planning and building 2D illustrations as SVG: technical figures,
interactive explainers, mechanisms, and charts.

`illustration-spec` decides what to draw before the first mark. The eight `svg-*`
skills build it.

| Skill | Answers |
|---|---|
| `illustration-spec` | what to decide before drawing, in dependency order; the spec template, gates, acceptance tests |
| `svg-fundamentals` | viewBox, scaling, groups, CSS, pointer coordinates |
| `svg-geometry` | paths, curves, connectors, projection and sections |
| `svg-defs` | markers, gradients, masks, patterns, filters |
| `svg-explainer-layout` | page structure: cards, tabs, traces, accessibility |
| `svg-animation` | GSAP timelines for step-through explainers |
| `svg-interaction` | steps, scrubbers, sliders, direct manipulation |
| `svg-d3-charts` | data binding for charts and derived series |
| `svg-verify` | headless screenshot and DOM verification |

## Layout

    skills/<name>/SKILL.md
    skills/<name>/references/*.md   optional, loaded on demand
    skills/<name>/scripts/*         optional, run by path
    docs/                           change history for the suite
    sync.sh                         the only install path

## Installing

    bash sync.sh --dry-run    # what would be copied
    bash sync.sh              # copy into ~/.hermes/skills/svg, then verify by sha256
    bash sync.sh --check      # verify only

`sync.sh` exits non-zero on any `MISMATCH`, `MISSING`, or `EXTRA`. `EXTRA` means a
file exists in the installed copy but not here: an installed skill was edited in place.
Copy it back, commit it, then sync. Never edit `~/.hermes/skills/svg` directly; that is
how this repository's first commit came to need a fix.

## Commits and versions

Semantic commits, scoped by skill: `type(scope): subject`, with types `feat`, `fix`,
`docs`, `refactor`, `chore`. Use `repo` as the scope for changes that are not one
skill. Each skill carries its own `version:` in frontmatter; a version bump is tagged
`<skill>-v<major>.<minor>.<patch>`.

## Evidence

Every rule in `illustration-spec` carries a standing (STANDARD, TAUGHT, PRACTICE,
OPINION, or declared local). The research behind it lives outside this repository, in
the `2d-research` workspace under `planning/`: seven domain reports, their extracts, and
`planning/corpus-map.md`, which maps each rule to the report and source it came from.
The method that produced it is `skills/illustration-spec/references/research-method.md`.
