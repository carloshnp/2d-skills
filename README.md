# 2d-skills

One Hermes skill for planning and building 2D illustrations as SVG: technical figures,
interactive explainers, mechanisms, charts, and sets of static sheets.

Hermes shows a single skill, `2d-skills`. Its `SKILL.md` is a router; the nine subskills
are files in `references/` that load on demand:

```
skill_view(name="2d-skills", file_path="references/illustration-spec.md")
```

`illustration-spec` decides what to draw before the first mark. The eight `svg-*`
subskills build it.

| Subskill | Answers |
|---|---|
| `illustration-spec` | what to decide before drawing, in dependency order; the spec template, gates, acceptance tests |
| `svg-fundamentals` | viewBox, scaling, groups, CSS, pointer coordinates, pixel floors |
| `svg-geometry` | paths, curves, connectors, projection and sections |
| `svg-defs` | markers, gradients, masks, patterns, filters, shared defs |
| `svg-explainer-layout` | page structure: cards, tabs, traces, accessibility |
| `svg-animation` | GSAP timelines for step-through explainers |
| `svg-interaction` | steps, scrubbers, sliders, direct manipulation |
| `svg-d3-charts` | data binding for charts and derived series |
| `svg-verify` | headless screenshot and DOM verification, state sweeps |

Author: Carlos Pereira.

## Layout

    skill/2d-skills/SKILL.md            the router Hermes registers
    skill/2d-skills/references/*.md     nine subskills plus their supporting references
    skill/2d-skills/scripts/*           check_spec.py, svg_bounds_and_type_check.py
    docs/                               CHANGELOG and change history
    sync.sh                             the only install path
    validate.py                         run before every commit

Subskills are flat files on purpose. Hermes registers a skill for every `SKILL.md` it
finds, but skips `references/` and `scripts/` under a skill root, and lists
`references/*.md` without recursing. A nested `subskills/<name>/SKILL.md` would show up as
nine extra skills.

## Installing

    bash sync.sh --dry-run        # what install would do
    bash sync.sh                  # install into ~/.hermes/skills/2d-skills, then verify
    bash sync.sh --check          # verify only
    bash sync.sh --pull           # copy in-place edits from the install into this repo
    bash sync.sh --remove-legacy  # delete the pre-2.0 copies under ~/.hermes/skills/svg

Install replaces the folder atomically and records a hash list in
`~/.hermes/skills/2d-skills/.sync-baseline`. That list lets `--check` tell three kinds of
difference apart:

| Label | Meaning | What to do |
|---|---|---|
| `STALE` | this repo changed since the last install | `bash sync.sh` |
| `EDITED` | the installed copy changed in place, usually a `skill_manage` patch | `bash sync.sh --pull`, review, commit |
| `CONFLICT` | both changed | merge by hand |

`sync.sh` refuses to install over `EDITED` or `CONFLICT` files (exit 3), so a lesson an
agent patched into the installed skill is never overwritten. `--remove-legacy` deletes the
old nine-skill copies only after the new install checks clean and every legacy file's
exact bytes exist in git (exit 4 otherwise, nothing removed). `SKILLS_DIR=/path` points
every mode at another skills folder.

## Validating

    ~/.hermes/hermes-agent/venv/bin/python validate.py
    ~/.hermes/hermes-agent/venv/bin/python validate.py --against main

It checks the router (frontmatter, description of at most 60 characters, every subskill
routed and present, no unlisted reference or script), each subskill's header, dashes,
named paths, banned adjectives in requirement lines, line budgets (`illustration-spec`
400 to 600), and with `--against` that no file's body shrank more than 10 percent,
following files to their pre-2.0 paths.

## Commits and versions

Semantic commits: `type(scope): subject`, with types `feat`, `fix`, `docs`, `refactor`,
`chore`. The scope is the subskill a change touches (`svg-verify`), `2d-skills` for the
router or the skill as a whole, and `repo` for tooling. One `main` branch.

The skill has one version, in the router's frontmatter. A release is tagged
`2d-skills-v<major>.<minor>.<patch>`; tags never move. The `illustration-spec-v1.3.x` tags
are history from before the merge. `docs/CHANGELOG.md` records what changed per subskill.

## Evidence

Every rule in `illustration-spec` carries a standing (STANDARD, TAUGHT, PRACTICE,
OPINION, or declared local). The research behind it lives outside this repository, in
the `2d-research` workspace under `planning/`: seven domain reports, their extracts, and
`planning/corpus-map.md`, which maps each rule to the report and source it came from.
The method that produced it is `skill/2d-skills/references/research-method.md`.
