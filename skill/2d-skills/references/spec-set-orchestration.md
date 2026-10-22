# Spec sets: writing many figure specs with delegated writers

Use when a chapter, paper, deck or product needs a set of figures (roughly 4 to 20) that
share one visual system, and the deliverable of the current phase is the specs, not the
drawings. The single figure rules live in SKILL.md; this file is the set level procedure.

## 1. Files the set needs

| File | Carries |
|---|---|
| `PLAN.md` | message, audience, view map, roster, anchors, non-goals, gates, open questions |
| `BRIEFING.md` | the contract every writer reads: verified facts, shared geometry, palette in both themes, canvas and type contract, required section structure, audit traps, report shape |
| `FIG-<set>-NN-<slug>.md` | one spec per figure |
| `verify_specs.py` | the set level audit (section 7) |

A worked set to copy the shape from: `~/study-site/docs/figures/dsa-09-graphs/` holds the
brief, the plan, the verifier and eleven specs for one guide chapter.

The brief is on trial with the writers. When three or more independent writers resolve one
ambiguity the same way and that way is wrong, the brief is contradictory, not the writers: one
line said panel frames were outlined at 3.2 while the palette said the border hue owns frames, so
half the set painted 3.2 and half painted 1.0, and several files contradicted their own inventory.
Fix the contract first, then the files, or the next wave reintroduces the same deviation.

Roster row schema, one row per figure. The child gets its row pasted verbatim, not the whole
plan:

`id | title | anchor (section id, and the sentence the figure follows) | views, each with its
element floor | dominant element | must show | forbidden`

Anchors must be ids the build actually produced, not re-slugified headings. Validate every
anchor against the built artifact (for a guide chapter, the `sections[].id` array in the
chapter JSON) before dispatch; a guessed id drifts on the next build and the figure lands on
the wrong page or nowhere.

## 2. Facts before writers

Recompute every number from the data structure, never copy it from prose. A wrong number in
the shared brief is replicated once per writer, and each writer cites the brief as its
source, so no per file audit can ever catch it.

- Put a fact table in the brief with a status per row: `chapter` (stated in the source, with
  the section), `verified` (recomputed), `derived` (follows from a named operation).
- When two framings of one quantity disagree, pick one, say why, and forbid the other in the
  roster row. A literal path sum and a shortest prefix distance can both be correct and still
  contradict each other in one figure; the figure then ships a claim the text denies.
- A figure that isolates a leaking simplification (a negative edge breaking finality, a cycle
  forbidding an order) needs its numbers in the fact table too, even when the source states
  them in a code comment.
- A mechanism figure's state transitions belong in the fact table. When the prose names an event
  and the listing's invariant asserts a state, the invariant wins: "its distance is final when
  dequeued" and "every vertex in the queue already holds its final dist" can both be true, and a
  figure that paints queued values as pending is false on the frame it draws. Write the
transition as a row whose source is the invariant, not the sentence.

## 3. Geometry shared across figures

Any object drawn in two or more figures gets one coordinate table in the brief, in canvas
units, with the node or part radius. State in each spec that the coordinates are inherited
and that an offset is a single translation, not a redraw.

Without this, five figures of the same graph read as five different graphs, and a reader who
learned the layout in the third cannot navigate the ninth. It also makes review cheap: a
misplaced node is visible across the whole set at once.

## 4. One palette, both themes

Declare a role table with a light and a dark hex per role, plus what each role is allowed to
carry. Then compute the contrast of every pair the figure will actually use and write the
numbers into the brief, so requirements can quote them instead of asserting them.

Turn the computed consequences into requirements, not advice:

- a role below 4.5:1 against its surface never carries text
- a surface tint under 3:1 only groups, it never encodes: a state shown by a wash alone
  disappears in the other theme and for a reader who cannot separate the hues
- a meaningful stroke uses the role that clears 3:1, never the panel border hue
- every hue role also carries a shape, dash or label difference

A figure dropping into a themed site that declares one theme is half drawn.

A role name is not a role meaning. Independently written sheets each invent a use for the same
role: one paints a count with `success`, one a verified tick, one a settled value, and all three
look consistent because the hex matches. Put a role to state table in the brief (`active`,
`frontier`, `settled`, `verified`, `rejected`, `broken`, `unreachable`) and audit that table
across files, not per file. The fault is a meaning that changed while the colour did not, which
no palette containment check can see.

## 5. Dispatch

- **One writer per figure, all in one delegate call.** They fan out concurrently; the wave
  boundary is the only serialization. Batches of three or four are for a pool that cannot
  hold the whole set.
- **Each child receives:** the absolute path of the brief (read in full first), its roster row
  verbatim, the path of the source excerpt, the exact file it must write, the audit command,
  and the report shape. Nothing about the other figures except what the roster row implies.
- **Boundaries in the prompt:** write only its own file; never edit the source corpus, the
  app, another spec, or the plan; escalate rather than drop a required element.
- **Demand the audit line in the report.** A child reporting success from a file that exists
  has not run the audit. Require: path, audit output line, per view element counts, every
  claim it could not source, open questions.
- **Do not hand a child the whole plan to interpret.** Long prompts make children re-derive
  conventions and drift; the row is the assignment, the brief is the contract.

## 6. Audit in waves, then patch

The lenses are read-only: run all four before anything is edited.

1. **Mechanical:** the per file script on every file, plus the set verifier below.
2. **Factual:** every occurrence of a quantity, not just the fact table. A writer can flag a
   brief error in an open question and still carry the wrong number into three places (prose, an
   inventory row, a data attribute), so grep each count and compare every hit. This is the
   accuracy ledger gate run once at set level instead of N times.
3. **Consistency:** palette containment, the role to state table, canvas agreement, inherited
   geometry, requirement prefixes, and whether two figures claim the same beat.
4. **Coverage:** every teaching beat has a figure or an explicit non-goal; no figure merely
   restates the prose. This lens reads the source and the specs, never the audit script, and it
   may overrule the mechanical pass: a spec can be green on traceability and still fail its own
   argument by naming three parts where the source defines four.
5. **Escalate findings that change scope.** A lens that proposes adding or cutting a figure has
   found a scope change, not a defect: route it, record a revision row, then dispatch a writer.
   Absorbing an eleventh figure silently leaves the plan's anchor table and the set verifier's
   roster wrong.
6. **One editor applies the findings.** Patch, never regenerate: a regenerated spec loses the
   decisions that were expensive to make and comes back thinner.

## 7. The set level verifier

A per file audit cannot see identity, drift, or agreement between files. Write a script that
prints one table and exits non-zero on any failure:

- the file exists, the per file audit exits 0, the file is under its line ceiling
- every requirement id carries that figure's own prefix (catches a copy-pasted file)
- every hex value is inside the locked palette (catches palette drift)
- section 4 declares the shared canvas width (catches a figure widened alone)
- the anchor section id appears in the file and exists in the built source
- section 6 yields at least one view with a numeric element floor
- print per figure: audit verdict, requirement count, view count, floor total, line count
- parse the view table by header name, never by column index: the `element floor` column lands
  second, third or fourth in independently written files, and a fixed index fails a correct file
- require each spec to cite its own anchor id in READING CONTEXT and require that id to exist in
  the built source; most writers describe the placement in words and omit the id, and the
  verifier then fails them all for a one line patch each

A green run means the set is consistent. It does not mean the figures are good: composition,
projection and meaning still need a reader, exactly as a green DOM audit does at build time.

## 8. check_spec.py traps

These cost a round trip each and none of them is visible in the spec template:

- **Requirement lines** must be `- REQ-<ID>-NN [MUST-STANDARD|MUST-LOCAL|SHOULD] <text>`;
  bare `[MUST]` is a warning, and ids must be unique and appear in section 10 and nowhere
  else in the acceptance table.
- **Banned adjectives** are scanned across the whole section 7 block, so ordinary verbs count:
  `clear` in "clear the queue" fails the file.
- **Do not total in prose.** A line reading `<number> colours` in section 5 or
  `<number> elements` in section 6 is compared against the table row count, so a stale
  sentence fails the file even when the table is right. Describe the tables, do not sum them.
- **Section 6 needs two tables in order:** the view table with a column literally named
  `element floor` and digits in every view row, then the element inventory whose header row
  starts with `ID`.
- **No em dash and no en dash anywhere** in the file, prose or table.
- **Section 9b has a trap for static figures.** The checker skips the field checks only when
  the section body starts with `none`. A line written `- STATE: none: ...` does not start with
  `none`, so it still needs a `- DATUM:` line with content and an `INV-nn`. For a static
  figure write the four fields with `not applicable` values plus a `- FUTURE STATE:` line
  naming what a later interactive revision would drive.
- **Sections 11 and 12 must exist**, even when nearly empty.

Run it before presenting, and run it again after every patch: a patch that adds a requirement
without an acceptance row is the most common way a clean file goes red.

## 9. The fix wave

The audit is worth nothing if the fix regenerates what the audit criticised.

- **Split by disjoint file group, one writer each.** One editor for ten files serialises the
  wave and applies patches to lines that moved; one writer per two or three files, each told
  exactly which files it owns and that everything else is off limits, runs concurrently without
  conflicts.
- **Copy each file to `<name>.old` before editing** and report the element count per view before
  and after. A drop is lost work, and a spec that lost an inventory row can still audit green.
- **No requirement may be deleted to make room.** If a finding cannot be applied without
  removing approved content, it escalates.
- **State the ruling, not the symptom.** The fix prompt carries the decision ("the chip turns
  final at enqueue; the ring stays at dequeue") and the reason, plus every derived line that has
  to move with it: inventory rows, invariants, requirements, acceptance rows.
- **Re-run both audits on every touched file**, and ask the writer to report the strings the file
  now prints (cycle order, final list, count) so the parent can compare them across files
  without re-reading each one.
- **Record the wave in the plan.** A revision row per correction, with why the plan was wrong,
  keeps the next session from reopening a decision that was already ruled on.
