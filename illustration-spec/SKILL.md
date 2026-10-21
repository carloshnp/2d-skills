---
name: illustration-spec
description: Use when planning a 2D illustration before drawing.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [illustration, planning, spec, composition, technical-drawing, diagram, requirements]
    category: creative
    related_skills: [svg-explainer-layout, svg-geometry, svg-verify, svg-fundamentals]
---

# Illustration Spec

A drawing discipline borrowed from spec-driven development: write the picture down
before you draw it, then test the drawing against what you wrote.

The eight `svg-*` skills answer *how* to draw. This one answers *what to decide before
the first mark*, in the order the decisions depend on each other. Skip it and the
figure gets composed by accident, then decorated.

Two paths:

- **Fast path** (12 questions, minutes). One-off figures you will throw away.
- **Full path** (the spec below). Anything published, presented, revised, reused, or
  handed to an agent in a later session.

## When to use

- A figure that carries an argument, not just decoration.
- Anything that will be reviewed, revised, or rebuilt.
- Anything drawn by an agent from a brief, where the brief is the only memory between
  sessions.
- Multi-panel figures, where panel logic is itself a decision.

Skip for: thumbnails, studies, exploration sketches, and anything whose only purpose is
to find out whether an idea is worth drawing.

## The decision spine

Eight decisions, in this order. Each one narrows the next. Reversing the order is the
most common cause of an illustration that is beautiful and says nothing.

| # | Decision | Settles |
|---|---|---|
| 1 | Why it exists | one message, audience, intended change |
| 2 | Where it is seen | size, medium, context, print or projection |
| 3 | What it contains | one job per element, and the deletions |
| 4 | What convention governs | projection, line grammar, scale claims |
| 5 | How attention is ordered | dominant element, reading path, hierarchy |
| 6 | How meaning is encoded | value plan, palette roles, redundancy |
| 7 | What the build contract is | canvas, node budget, text split, steps |
| 8 | How it will be judged | acceptance tests, reviewer, severity |

## Fast path: twelve questions

Answer in writing. Each line names what it costs when skipped.

1. **What is the one sentence a reader should repeat afterwards?** Skipped: the figure
   becomes a diagram of everything, and of nothing.
2. **Who reads it, and what do they already know?** Skipped: labels explain what the
   audience already knows, and skip what it does not.
3. **At what size and in what medium?** Print column, projected slide, phone. Skipped:
   text sized for A4 becomes unreadable at 89 mm or on a projector.
4. **What must be present, and what must be absent?** Skipped: the missing element is
   found in review, after composition is frozen.
5. **Which convention applies: none, orthographic, axonometric, flat schematic?** Skipped:
   mixed conventions that look like errors.
6. **What is the one dominant element?** Skipped: two things compete and the eye bounces.
7. **What is the reading path, in order, with arrows?** Skipped: readers enter at the
   wrong place and stop there.
8. **What is the value plan, with the strongest contrast junction at the focus?**
   Skipped: colour is used to fix a value problem it cannot fix.
9. **What does each colour mean, as a role, not a swatch?** Skipped: colours chosen per
   session, so panel 2 does not match panel 1.
10. **How is each element labelled, and where does the label sit?** Skipped: detached
    legends that force eye travel.
11. **What is deliberately not stated, and what is the note that covers it?**
    Skipped: implied claims nobody verified.
12. **What test will this fail if it is wrong?** Skipped: review by taste, no falsifiable
    criterion.

## Full path: the spec

Copy this block into a file named for the figure (`FIG-03-eutectic.md`), fill it, and
keep it next to the drawing. Sections 2 to 6 are filled before any sketch exists.
Section 8 is filled at thumbnail time, section 9 before build, section 10 before review.

```markdown
# FIG-<id>: <title>
status: draft | review | frozen | superseded
rev: <n>   date: <YYYY-MM-DD>   author: <who>

## 1. Summary
One paragraph: what the figure shows and why it exists.
Then one line: MESSAGE = the sentence a reader should repeat.

## 2. Communicative intent
- AUDIENCE: who, what prior knowledge, what they currently believe
- INTENDED CHANGE: understand / believe / do
- READING CONTEXT: slide, paper column, dashboard, phone; neighbours on the page
- REPRODUCTION: width x height, aspect, final display size, print or screen
- LIFETIME: one talk, one paper, an illustration system

## 3. Goals and non-goals
- GOAL-1..n: one observable outcome each
- NON-GOAL-1..n: plausible things this figure deliberately does not do
  (never write a goal in negated form)

## 4. Constraints
- canvas: viewBox 0 0 <W> <H>; aspect; unit scale (1 unit = ...)
- node budget: <= <N> live elements; interactive ceiling is roughly 1000
- palette budget: <= <N> colours
- typography: family, sizes at final render, minimum cap height in px
- text split: what is HTML prose, what is an in-SVG label, max words per label
- convention: <none | orthographic first/third angle | axonometric isometric |
  flat schematic | map-like>
- time appetite: how much effort this deserves before it is over-engineered

## 5. Visual system lock
- projection: <declared, one per sheet, never mixed>
- line grammar: outline <px>, annotation <px>, ratio >= 2:1; hidden <dash>;
  centreline <dash-dot>; cutting plane <chain with thick ends>
- palette table (one row per colour, roles not swatches):

  | NAME | HEX | RGB | ROLE | USED FOR |
  |------|-----|-----|------|----------|

- value plan: <3 foundation values; where the highest light/dark junction sits>
- light: <one direction, one shadow type, or "flat, no light declared">
- detail floor: nothing meaningful below <px> at final size

## 6. Content inventory
| ID | element | job in the argument | must show | budget | label | convention |
|----|---------|---------------------|-----------|--------|-------|------------|

Every element carries a job. An element without a job is deleted, not shrunk.
IDs become DOM ids (VIZ-<ID>) so acceptance tests can assert them.

## 7. Requirements
- REQ-FIG-01 [MUST] <checkable statement>
- REQ-FIG-02 [SHOULD] <checkable statement, with the cost of complying>

Banned adjectives in requirements: clear, clean, modern, professional, appealing,
balanced, readable (say what makes it so, measurably).

## 8. Composition plan
- DOMINANT: the one element seen first
- FOCAL MECHANISM: >= 2 of isolation / value contrast / hue contrast / size /
  convergence / detail density
- HIERARCHY: <= 3 levels, named
- READING PATH: entry -> second -> third -> payoff, drawn as arrows or listed
- BALANCE: symmetrical / asymmetrical / radial, with the mass compensation
- FRAMING: crop, horizon placement, lead room
- NEGATIVE SPACE: what the empty regions do
- GROUPING: proximity tighter inside groups than between them

## 9. Build contract
- steps: <n> steps, one idea each. 0: <...> 1: <...> 2: <...>
- interaction: none / step controls / slider, justified by the reading task
- animation: none (default) or a timeline, with the enabling test: why the reader
  cannot infer the transition from statics
- ids and classes: DOM ids equal inventory IDs; one class per visual role
- verification hooks: which state can be forced by query param

## 10. Acceptance criteria
| REQ | test | pass condition | method |
|-----|------|----------------|--------|

One primary check per goal, plus guardrails. Name the reviewer and the method.
Copy thresholds from the section below, and mark invented ones as invented.

## 11. Open questions
- Q1: <undecided, owner, and what evidence would settle it>

## 12. Revision history
| rev | date | change | why |
|-----|------|--------|-----|
```

## Gate list

Gates run in order. Do not raise fidelity until the current gate passes. Each gate
approves a different class of error, which is why one review cannot replace them.

- **G0 Intake.** Sections 1 to 4 complete. No sketch exists yet.
- **G1 Thumbnails.** Three or more distinct concepts, at the final aspect ratio, in
  grayscale, too small to hold detail. Approves layout and type space.
- **G2 Silhouette and value.** Two-value reduction, then a 3 to 5 value study. Approves
  readability and focal contrast. Failures are rejected here, not fixed in colour.
- **G3 Rough.** Drawing accuracy, content coverage, labels roughed in. Content freezes
  at approval; later redesigns are new scope.
- **G4 Build.** Line grammar, palette, text placement, steps. Approves craft.
- **G5 Acceptance.** Section 10 run in full, plus one non-author reviewer.

For technical figures insert a gate between G3 and G4: **factual accuracy**. No
professional illustration workflow has this gate, and an explainer without it is
unverified by construction. Check every number, unit, phase label, and micrograph
attribution against a primary source before styling begins.

## Acceptance tests

Tier A gates have documented numeric passes. Tier B are named methods with judgment
passes, so the spec has to declare its own threshold. Tier C is hygiene.

**Tier A (gate):**

- Contrast: text at least 4.5:1, large text at least 3:1, meaningful graphics at least
  3:1 against adjacent colours (WCAG 1.4.3, 1.4.11).
- No colour-only encoding: every hue-encoded meaning also carried by shape, dash,
  label, or position (WCAG 1.4.1).
- At-size legibility: render at final display size and read every label. For print
  venues, 7 pt maximum and 5 pt minimum body text, 8 pt bold upright panel labels
  (Nature guide; Science and Elsevier are close but not identical).
- Alt text: an equivalent purpose, not a description of marks; one or two sentences plus
  a linked data table when the figure carries numbers.
- Rubric form: each acceptance descriptor lets the maker picture the next action.

**Tier B (require, judge):**

- Squint test: blurred, the intended dominant element is still seen first.
- Thumbnail test: at thumbnail size, no clear discrepancy against intent.
- Grayscale check: value structure survives desaturation; the strongest junction is at
  the focus.
- Mirror flip: horizontal flip for asymmetry and alignment errors, then flip back.
- Five-second test: a fresh viewer recalls the message, not the decoration.
- Notan check: reduced to two or three flat values, every key object is still
  recognisable as its shape class.
- Non-author reviewer: at least one person who did not draw it, and who is not
  emotionally invested.
- Brief anchoring: every comment tied to a numbered requirement; unanchored comments
  are opinions and get logged as such.

**Tier C (recommend):** colour-vision simulation, severity rating per finding,
expert inspection before reader testing, two-pass heuristic review.

Where a threshold does not exist, write the number you chose and the phrase "declared
local". That is honest. Quoting an authority that never said it is not.

## Rules worth carrying, with their standing

STANDARD means a document says it. TAUGHT means a named teacher or textbook. PRACTICE
means working convention. OPINION means taste, and it must be labelled as such.

| Rule | Standing | Where it comes from |
|---|---|---|
| One dominant element; at least two focal mechanisms | TAUGHT | composition literature |
| Hierarchy capped at three levels | TAUGHT | composition literature |
| Value planned before hue: notan, then values, then colour | TAUGHT | painting and concept-art teaching |
| Palette documented as role plus hex, never as swatches | PRACTICE | art bibles, design systems |
| Projection declared, one convention per sheet, never mixed | STANDARD | ISO 5456-2, ASME Y14.3 |
| Outline thick, annotation thin, ratio at least 2:1 | STANDARD | ISO 128-2, ASME Y14.2 |
| Dashed is hidden; chain-thin is centreline; chain with thick ends is a cutting plane | STANDARD | ISO 128-2 |
| Dimensions once only, outside the outline, readable from the bottom | STANDARD | ISO 129-1 |
| Hatch at 45 degrees, one angle per part, broken around labels | STANDARD | ISO 128-44 |
| Capitals, one lettering style, at least 3.5 mm at final size | STANDARD | ISO 3098 |
| Isometric at 30/30/vertical; 0.816 only for registration against orthographic | TAUGHT | technical drawing canons |
| Axonometric rather than perspective when readers compare sizes or order | PRACTICE | technical illustration |
| Balloons tied to a parts list; leaders never cross, never point at voids | STANDARD | assembly drawing convention |
| Position on a common scale is the most accurate encoding; avoid angle, area, hue for the take-home quantity | TAUGHT + EMPIRICAL | Cleveland and McGill, replicated |
| Delete every element with no teaching job | STANDARD | seductive-details meta-analysis, g = -0.33 overall, -0.43 static |
| Label on the part, not in a detached legend | STANDARD | spatial contiguity meta-analysis, g = 0.63 |
| Arrows assert movement, transformation, causation, or sequence only | TAUGHT | diagram comprehension research |
| Stepped statics are the default for causal processes | TAUGHT | animation research |
| One expertise level per figure; novice scaffolding in a disclosure layer | TAUGHT | expertise-reversal effect |
| Six categorical colours at most, twelve as a hard ceiling | TAUGHT | category discrimination research |

## Folklore blacklist

Do not write these into a spec as requirements, and say so when a stakeholder asks for
them:

- **Golden ratio placement, sizing, or spirals.** Three independent lines of evidence
  agree the beauty claims are unsupported, and the Parthenon does not exhibit the ratio.
  Usable as declared scaffolding, never as a rule.
- **Rule of thirds as law.** Keep it as a named heuristic; its own best source calls it
  the most consistently misapplied rule in photography.
- **Shape language certainty.** Circle friendly, square stable, triangle dangerous is
  lore level. Declare it when used, and log every inversion.
- **"Animation is always better."** Effects concentrate in procedural and motor tasks;
  learners who can self-animate show no advantage.
- **Data-ink ratio as a number.** The principle is usable, the ratio is not a target.
- **Any pixel threshold presented as a standard.** 2 px strokes and 4 px detail floors
  are design-system conventions, not standards.

## Free parameters: declare local law

No source resolves these, so the spec decides and records the decision:

- stroke weight scale in px for screen SVG (standards give print millimetres and a 2:1
  floor)
- minimum cap height in px at the final render size
- maximum annotation or leader count per view
- minimum gap between leader and its target
- ghost and trail opacity for exploded views
- exploded-view gap sizes
- arrowhead proportions, and whether leader arrows differ from flow arrows
- colour versus hatching for cut material in explainers
- behaviour at nine or more categorical series

## Handoff to the builder skills

| Spec section | Builder skill |
|---|---|
| 4 canvas, 9 text split | `svg-fundamentals` |
| 5 line grammar, 8 composition geometry | `svg-geometry` |
| 5 palette, arrow semantics, filters | `svg-defs` |
| 9 steps and timing | `svg-animation` |
| 6 encoding, shared scales, small multiples | `svg-d3-charts` |
| 9 interaction | `svg-interaction` |
| page and panel structure | `svg-explainer-layout` |
| 10 acceptance, DOM assertions | `svg-verify` |

## Failure modes

- **Fidelity before composition.** Detail on an uncomposed thumbnail. Fixed by G1: final
  aspect ratio, grayscale, too small for detail.
- **Encoding by taste.** Colour chosen before values, or before the encoding channel is
  decided. Fixed by the fixed order: notan, values, gamut, roles.
- **Unfalsifiable review.** "It feels cluttered" with no criterion. Fixed by anchoring
  every comment to a numbered requirement.
- **Spec as novel.** Sections filled after the drawing to document it. The spec is
  written before, and its value is in what it forces you to decide early.
- **Borrowed thresholds.** A pixel value quoted as a standard when it came from one
  company's design system. Name the source and its scope, or mark it local.

## See Also

- `svg-explainer-layout` for page structure around figures
- `svg-verify` for the headless loop that runs Tier A checks mechanically
- `planning/SYNTHESIS.md` and `planning/P1..P7/` for the evidence behind each rule
