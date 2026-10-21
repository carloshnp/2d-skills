---
name: illustration-spec
description: Use when planning a 2D illustration before drawing.
version: 1.3.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [illustration, planning, spec, composition, technical-drawing, diagram, requirements]
    category: creative
    related_skills: [spec-driven-development, svg-explainer-layout, svg-geometry, svg-verify, svg-fundamentals, svg-animation, svg-interaction]
---

# Illustration Spec

A drawing discipline borrowed from spec-driven development: write the picture down
before you draw it, then test the drawing against what you wrote.

The eight `svg-*` skills answer *how* to draw. This one answers *what to decide before
the first mark*, in the order the decisions depend on each other. Skip it and the
figure gets composed by accident, then decorated.

Two paths:

- **Fast path** (13 questions, minutes). One-off figures you will throw away.
- **Full path** (the spec below). Anything published, presented, revised, reused, or
  handed to an agent in a later session.

## Contents

- **Plan:** decision spine, view map, fast path, full spec, mechanism and state model,
  detail policy (default `full`)
- **Audit the plan:** pre-approval checks, detail views, projection and numbers
- **Build:** delegated agents, gate list
- **Judge:** acceptance tests, rules with their standing, folklore, free parameters
- **Connect:** handoff to the builder skills, failure modes, the SDD mapping, references

## When to use

- A figure that carries an argument, not just decoration.
- Anything that will be reviewed, revised, or rebuilt.
- Anything drawn by an agent from a brief, where the brief is the only memory between
  sessions.
- Multi-panel figures, where panel logic is itself a decision.

Skip for: thumbnails, studies, exploration sketches, and anything whose only purpose is
to find out whether an idea is worth drawing.

## The decision spine

Nine decisions, in this order. Each one narrows the next. Reversing the order is the
most common cause of an illustration that is beautiful and says nothing.

| # | Decision | Settles |
|---|---|---|
| 1 | Why it exists | one message, audience, intended change |
| 2 | Where it is seen | size, medium, context, print or projection |
| 3 | What it contains | one job per element, and the deletions |
| 4 | What convention governs | projection, line grammar, scale claims |
| 5 | How attention is ordered | dominant element, reading path, hierarchy |
| 6 | How meaning is encoded | value plan, palette roles, redundancy |
| 7 | How it moves | state variables, datum, derived parts, invariants |
| 8 | What the build contract is | canvas, node budget, text split, steps |
| 9 | How it will be judged | acceptance tests, reviewer, severity, state sweep |

## View map

Name the views before inventorying their elements, the way a software spec names its
modules before specifying any of them. The view map is section 6's first table.

| view | job in the argument | depends on | element floor |
|---|---|---|---|
| A | <what this view proves that no other view can> | none | <n> |
| B | <...> | A | <n> |

- A view with no job is deleted, not shrunk into a corner of another view.
- A view that depends on another is drawn after it, shares its unit scale, and names its
  parent in the caption, because the reader never sees the two side by side.
- Views with no dependency between them can be built in parallel, one agent each. The
  view map is the work breakdown for a delegated build.
- The element floor is the minimum live element count the view must reach (see Detail
  policy). Set it from the inventory, not from a finished drawing.

## Fast path: thirteen questions

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
13. **What moves, what drives it, and what must stay true at every state?** Skipped: the
    frame you checked is right and the other states are not. Answer "nothing moves" in
    writing if that is the answer.

## Full path: the spec

Copy this block into a file named for the figure (`FIG-03-eutectic.md`), fill it, and
keep it next to the drawing. Sections 2 to 6 are filled before any sketch exists.
Section 8 is filled at thumbnail time, sections 9 and 9b before build, section 10 before
review.

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
- ASSUMPTIONS: numbered, each marked confirmed or corrected by the requester

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
- detail: full (default) | reduced. reduced names what is dropped and why; "the
  requester asked for a simple figure" is a reason, "it was faster" is not
- element floor: per view, in the view map; the harness fails any view below it
- boundaries: Always <...> / Ask first <...> / Never <...>

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
- style reference: <path to one rendered frame that is the style source>

## 6. Content inventory
Views first (one row per view, see View map), then elements.

| view | job in the argument | depends on | element floor |
|------|---------------------|------------|---------------|

| ID | element | job in the argument | must show | budget | label | convention |
|----|---------|---------------------|-----------|--------|-------|------------|

Every element carries a job. An element without a job is deleted, not shrunk.
IDs become DOM ids (VIZ-<ID>) so acceptance tests can assert them.

## 7. Requirements
- REQ-FIG-01 [MUST-STANDARD] <checkable statement> (source: <document, clause>)
- REQ-FIG-02 [MUST-LOCAL] <checkable statement> (why: <the decision it records>)
- REQ-FIG-03 [SHOULD] <checkable statement, with the cost of complying>

Banned adjectives in requirements: clear, clean, modern, professional, appealing,
balanced, readable (say what makes it so, measurably).

Standing decides what can be traded. MUST-STANDARD comes from a document (ISO, WCAG,
a venue's figure guide) and is never traded; it is met by patching the offending
feature, never by deleting approved detail around it. MUST-LOCAL is a decision made
for this figure and is tradeable. When applying any requirement would delete content
already approved, stop and ask: show the rule, what it removes, and an option that
keeps both.

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
- commands: render, verify, and sweep, with flags, so a later session can reproduce
  every state a reviewer saw

## 9b. Mechanism and state model
Required when any position, visibility, or label is derived from a state.
Write "none: nothing is derived" when that is true.
- STATE: <name, unit, range, step, default>, one line per variable
- DATUM: <what zero means, and for which part>
- DERIVED: <element ID>: <formula>, one line each; every element not listed is placed
- CHAIN: <driver> -> <derived> -> <derived>
- INVARIANTS: INV-01 <statement true at every state>, INV-02 ...
- SAMPLED STATES: <states reviewed by eye, and why each one>
- SWEEP: <every value | declared sample of n>, run by <harness path>

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

## Mechanism and state model

Almost every interactive figure is a mechanism, and every figure with motion is one: some
part's position is computed from a state rather than placed. A crank angle drives eight
pistons, a slider drives a curve, a step index decides which labels exist. One correct
frame proves nothing about the other states, so the mechanism is planned, defined, and
reviewed like the composition is.

It is required whenever any position, visibility, or label is derived from a state. That
includes a static figure frozen at one state: it is one sample of a mechanism, and the
next revision will ask for a different one. Write it as section 9b, before the build
contract freezes.

- **State variables.** Name, unit, range, step, default: `crank angle, degrees, 0 to 719,
  step 1, default 90`. A four-stroke cycle spans 720 degrees, not 360; a range wrong by a
  factor is the cheapest mechanism bug to make and the most expensive to find late.
- **Phase datum.** What zero means and for which part: "0 = cylinder 1 at top dead centre
  of compression". Every other phase is stated once, relative to the datum.
- **Derived versus placed.** List every element whose geometry comes from a formula, with
  the formula: piston pin height `r cos(t) + sqrt(L^2 - r^2 sin^2(t))`. Everything not on
  the list is placed and must not move when the state changes.
- **Kinematic chain.** Which derived part depends on which: crank, pin, rod, piston. Build
  order follows the chain, and so does debugging.
- **Invariants.** Statements true at every state, written so a harness can assert them:
  "the two rods on one crankpin stay 90 degrees apart", "no piston crown rises above the
  deck line", "no derived coordinate is NaN", "no label leaves the canvas".
- **Sampled states.** The few states a reviewer inspects by eye: the datum, one state at
  each phase boundary, and the worst case for clearance or label collision.

Review is a sweep, not a frame. The harness steps through every value in the range (or a
declared sample when the range is continuous), asserts every invariant at every step, and
reports the first failing state. A mechanism checked at one frame is unreviewed.

Static, animated, and interactive versions share one model. Draw the static figure by
calling the function the slider calls, so the frozen frame and the live one cannot
disagree. `references/build-harness.md` carries the sweep.

## Detail policy

`detail: full` is the default. A figure is drawn at the detail its subject has, not the
detail that was quick to produce, unless the requester asked for a simple figure.
`reduced` is legitimate when it is stated in section 4 with what is dropped.

Three rules hold the default in place, because each failure below happened in one build:

- **Element floor per view (MUST).** Written in the view map, asserted by the harness.
  A node budget is a ceiling and cannot see a view getting simpler; a floor turns a
  thinner redraw into a failing number instead of a passing glance.
- **Patch, never regenerate, to answer a requirement.** A projection requirement was
  answered by regenerating two detailed views from the brief. Both came back at about a
  third of their source length, and the requester restored the originals.
- **No requirement silently deletes approved content.** Escalate instead (section 7).

## Before you present a spec for approval

The document is the deliverable at this stage, so audit it the way you will audit the
drawing. Four checks, all mechanical, all before anyone reads it:

1. **Traceability.** Every requirement has exactly one acceptance row, and every
   acceptance row names a requirement. A requirement with no test is not a requirement,
   and a test with no requirement is scope creep.
2. **Banned adjectives.** Scan the requirement lines for clear, clean, modern,
   professional, appealing, balanced, readable. Each one hides a decision nobody made.
   Replace it with the property that makes it true and the way to check it.
3. **Derived counts.** Totals written in prose ("twenty-six elements", "five colours",
   "eight detents") drift the moment a table grows. Count from the table, write the
   number, and recount after every revision. A stale total is the first thing a reviewer
   notices and the last thing you remember to fix.
4. **Claim status.** Every factual claim the figure will assert sits in the accuracy
   ledger with a status, a source, and, where the source is weak, what would replace it.
   A claim with no ledger row is a claim that will be drawn from memory.

`scripts/check_spec.py <spec.md>` runs checks 1 to 3 mechanically and exits non-zero on
any hit. Run it before presenting, not after a reviewer finds the problem.

## Detail views and medium changes

When a revision adds views, the medium changes before the layout does.

- A detail is a magnified portion of a parent view, never a standalone redrawing:
  chain-thin boundary around the source, a leader that terminates on the feature, and
  the scale declared in the label (3:1, 2:1).
- Derive detail geometry from the parent by the scale factor. Redrawing by hand is how a
  detail and its parent come to disagree about proportions, and it makes dimension
  checks impossible to run in both.
- Adding views forces a medium decision: magnified callouts inside the existing panels,
  or standalone panels on a taller sheet. Decide it explicitly, then update section 2
  and section 4 together and record what the aspect change costs on a projector. A
  figure that quietly stops being 16:9 is a figure that stops fitting the slide it was
  specified for.
- Three details in one 16:9 sheet is about the practical ceiling before the callouts
  start competing with the parent view. Past that, move to a taller sheet or split the
  figure; the number is a declared local judgement, not a standard.
- **When every view must reach the same detail, give each view its own full-page tab on
  one shared canvas.** A grid of bands caps what a view can hold: a band grows sideways
  while detail needs height, so five views on one screen means five reduced drawings.
  Five tabs on one viewBox means five drawings at the same unit scale, switched by a tab
  bar that preserves the shared state (crank angle, step, selection) across switches.
  Keep the tab letters in reading order and put the scale in each tab caption, since no
  two views are ever seen together and each must stand alone.

## Projection discipline and numbers

Two rules no gate catches, because every element can be present and the drawing still
wrong.

- **A cylindrical feature is a rectangle when its axis lies in the section plane, and a
  circle only in an end view.** A journal or crankpin drawn as a circle inside a side
  section is an end view pasted into a section: it reads as unmechanical even to a reader
  who cannot name why. Decide per view which features are seen along their axis (circles)
  and draw every other cylinder as a rectangle with webs and fillets. Write this into the
  spec as a requirement, because a builder given radii will draw circles.
- **A dimension label must agree with the drawn geometry at one scale.** Annotate a number
  only when the distance on the sheet matches the same unit scale as every other dimension
  on that sheet. A builder asked for detail invents plausible figures: a 300-unit bore
  spacing labelled 112 mm is a false claim the reader can measure. When the spec forbids
  real numbers, draw the extension lines and label the quantity ("stroke", "bore
  spacing") with no value at all. An unsourceable number is worse than no number.
- **Hidden means hidden, not faint.** A second part at a different depth takes a long dash
  pattern, a narrower silhouette, and a small axial offset so it never coincides with the
  near part; drawing it at the same position in a thinner line reads as a duplicate, not
  as depth.

## Building from the spec with delegated agents

A multi-view figure parallelises by view, not by element. Write the contract first, then
one agent per view.

1. **Contract file in the build directory** (`INTERFACE.md`): module shape
   (`window.PANEL_X = {mount(svg), render(state)}`), the shared state the shell owns and
   every helper it exposes, the CSS class table with palette variables, and one section
   per view carrying its canvas, its required features, and its label list.
2. **One module per view plus a standalone test page** that stubs the shared state and
   renders three states. An agent that can only test inside the integrated page cannot
   tell whether its own panel works, and will report success from a file that exists.
3. **Re-steer, do not restart, when the architecture changes mid-build.** Agents already
   drawing carried the old canvas; send each the new dimensions and the contract path.
   Restarting loses their verified work and their test page.
4. **Count descendants, not children,** in any audit: `querySelectorAll("*").length`, not
   `childElementCount`, or a panel that mounts a single group reads as empty.
5. **A passing DOM audit is not a correct drawing.** Assert what is checkable, then look
   at every state. In one build the audit was green while the crank sat in the wrong
   projection, one panel split its subject across two half-views, and one chart clipped
   every row.
6. **A review note is a reason to patch, not to regenerate.** Regenerating a panel from
   the brief discards the detail that was expensive to draw, and detail is the first
   thing to vanish. Copy the working file to `panelX.js.old` before touching it, compare
   `querySelectorAll("*").length` before and after, and treat a drop over ten percent as
   lost work. Rewrite only when the projection itself is wrong, and then port the old
   feature list into the new contract line by line rather than writing from memory.

`references/delegated-illustration-build.md` carries the contract template and the fix
round pattern.

## Gate list

Gates run in order. Do not raise fidelity until the current gate passes. Each gate
approves a different class of error, which is why one review cannot replace them.

- **G0 Intake.** Sections 1 to 4 complete. No sketch exists yet.
- **G1 Thumbnails.** Three or more distinct concepts, at the final aspect ratio, in
  grayscale, too small to hold detail. Approves layout and type space.
- **G2 Silhouette and value.** Two-value reduction, then a 3 to 5 value study. Approves
  readability and focal contrast. Failures are rejected here, not fixed in colour.
- **G3 Rough.** Drawing accuracy, content coverage, labels roughed in. Content freezes
  at approval; later redesigns are new scope. The state model freezes with it: a new
  state variable after G3 is new scope.
- **G4 Build.** Line grammar, palette, text placement, steps. Approves craft.
- **G5 Acceptance.** Section 10 run in full, the state sweep green for every invariant,
  plus one non-author reviewer.

For technical figures insert a gate between G3 and G4: **factual accuracy**. No
professional illustration workflow has this gate, and an explainer without it is
unverified by construction. Check every number, unit, phase label, and micrograph
attribution against a primary source before styling begins.

## Adapted from spec-driven development

This skill is the 2D instance of `spec-driven-development`. Its phases map onto the gates
so the two never read as competing workflows:

| SDD phase | Here | Human reviews |
|---|---|---|
| 0 Scope check, capability map | view map | views, dependencies, build order |
| 1 Specify | spine 1 to 7; spec sections 1 to 8 and 9b; G0 | the spec, in a later turn |
| 2 Plan | G1 thumbnails, G2 value, section 9 build contract | the chosen concept |
| 3 Tasks | one module per view, the contract file | the contract |
| 4 Implement | G3 rough, factual accuracy, G4 build | each gate |
| Verification | G5 acceptance and state sweep | non-author reviewer |

Carried over, rewritten for figures:

- **Surface assumptions before the spec.** List them and ask for corrections:
  `1. third-angle projection 2. seen on a 1920x1080 projector 3. audience knows the
  four-stroke cycle 4. detail: full`. An unstated assumption becomes a composition
  decision nobody approved.
- **Reframe vague asks as checks.** "Make it more detailed" becomes an element floor per
  view, a shell and oil hole on every bearing, and every leader ending on a named part.
  "Make it pop" becomes a value junction at the dominant element, read in grayscale.
- **Boundaries in three tiers**, in section 4. Always: run the harness before reporting,
  patch rather than regenerate. Ask first: dropping approved detail, changing projection,
  adding or removing a view, changing the aspect ratio. Never: an unsourced number, colour
  as the only carrier of meaning, editing a frozen view without a revision row.
- **Commands belong in the spec.** Section 9 names render, verify, and sweep commands with
  their flags (`verify.py`, `index.html?tab=C&angle=90&audit=1`).
- **One reference frame beats three paragraphs of style**, the way a code spec points at
  one real snippet instead of describing conventions.
- **Stop after the spec.** Present it with its open questions and end the turn.
  Thumbnails start after approval.
- **Keep it alive.** A decision that changes mid-build edits the spec first, with a
  revision row, then the drawing. A requirement added during build with no acceptance
  row is the usual way this breaks, and `check_spec.py` catches it.

| Rationalization | Reality |
|---|---|
| "It's just a diagram" | A diagram makes claims and needs a dominant element. A twenty-line spec is enough. |
| "I'll compose it after drawing the parts" | That is layout. The reading path decides which parts are drawn large. |
| "The requester knows what they want" | A precise brief still leaves projection, audience, and size open. |
| "Detail can come later" | Detail added after composition fights it. Plan the floor first. |
| "A review note means start over" | It means patch the feature it names. Regenerating discards the costliest work. |
| "One frame looks right" | One frame is one sample of the mechanism. Sweep the states. |
| "The audit is green" | A DOM audit checks presence, not projection or meaning. Look at every state. |

Red flags: drawing before section 1 has a MESSAGE line; a view with no row in the view
map; a requirement with no acceptance row; moving parts with no section 9b; a redraw
whose element count fell; a number with no ledger row; thumbnails started in the turn the
spec was presented.

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
- State sweep (declared local, gate for mechanisms): every invariant in section 9b holds
  at every swept state, and the first failing state is reported by value.

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

## Rules, standing, and folklore

Every rule carries a standing: STANDARD (a document says it), TAUGHT (a named teacher or
research line), PRACTICE (working convention), OPINION (taste, labelled), or declared
local. The full table, with sources, and the folklore blacklist (golden ratio, rule of
thirds as law, shape-language certainty, "animation is always better", data-ink as a
number, pixel thresholds sold as standards) are in `references/evidence-and-folklore.md`.
Do not write a blacklisted claim into a spec as a requirement, and say so when asked.

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
| 9b state model, invariants | `svg-animation`, `svg-interaction`, `svg-verify` |
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
- **Regeneration loss.** A view is rebuilt to answer a review note and comes back
  simpler: fewer features, fewer labels, less of the detail that made it worth having.
  The reviewer's complaint was local, the rebuild was global. Fixed by patching the
  offending geometry in place, keeping a `.old` copy, and counting elements before and
  after every rewrite.

## See Also

- `references/technical-sheet-conventions.md` for projection, line grammar, detail
  callouts, materials labels, and the accuracy ledger format
- `references/delegated-illustration-build.md` for the contract file, per-view modules
  and the fix round that follows a visual review
- `references/build-harness.md` for the page audit, state sweep, driver matrix, and the
  fixtures that prove the harness can fail
- `references/evidence-and-folklore.md` for every rule with its standing and source, and
  the claims kept out of specs
- `references/research-method.md` for how a rule earns its standing, and the change
  control that keeps plans and rules current
- `scripts/check_spec.py` for the mechanical pre-presentation audit
- `svg-explainer-layout` for page structure around figures
- `svg-verify` for the headless loop that runs Tier A checks mechanically
- The research corpus behind each rule lives in the 2d-research workspace, `planning/P1..P7`,
  `planning/SYNTHESIS.md`, and `planning/corpus-map.md` (rule to source). The installed
  skill carries the distilled rules, not the reports.
