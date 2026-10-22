# Building a multi-view figure with delegated agents

Use when a figure has three or more views, or when the detail budget per view is large
enough that one agent would serialise the build. The shell stays yours; the views go out
in parallel.

## Files

```
build/
  INTERFACE.md          the contract, written before any agent starts
  index.html            shell: grid, tabs, shared state, audit
  parts/panelA.js       one module per view
  parts/panelA.test.html  standalone harness, stubs the shared state
  verify.py             per-view headless audit
```

## The contract file

Six blocks, in this order. Agents read it first and nothing else.

1. **Shell and state.** The object the shell defines, the helpers it exposes, and the
   exact kinematics constants. Any helper an agent re-derives is a helper that drifts.
2. **Module shape.** `window.PANEL_X = {mount(svg), render(state)}`. `mount` runs once,
   `render` runs on every state change and must never recreate nodes.
3. **CSS class table.** The drawing grammar the shell already defines (outline,
   annotation, hidden, centreline, dimension, label, halo, fill roles) plus palette
   variables. Agents may use these and may not redefine them.
4. **One section per view.** Canvas and aspect, scale, the required features as a list,
   the labels with the feature each leader must terminate on, and the node budget.
5. **Content rules that apply to every view.** Real features only; hidden, centre and
   section lines never mixed; every label on its feature; no numeric dimension unless the
   spec allows one.
6. **Self-test the agent must run before reporting:** `node --check`, a standalone page
   that stubs the shared state and renders three states, a headless title check, a
   screenshot, and a look at that screenshot.

## Dispatch

- One agent per view, all in one batch, each told to read the contract and not to edit
  the shell or another view.
- Give the canvas size in the task text as well as in the contract. Agents that only skim
  the file default to the size they saw first.
- When the architecture changes mid-build, send each running agent a short steer with the
  new numbers and the sentence "re-read the contract". Do not kill and restart them:
  restarting loses their verified work and their test page.

## Review round

Run the shell audit across every view and every state first, to remove mechanical
failures (missing module, label under the legibility floor, label outside the canvas,
label over three words). Then look at one screenshot per view and ask for concrete
defects, not a description:

- does the subject read as the thing it claims to be, in the right projection;
- is the second part of a pair actually drawn, not implied;
- does every leader terminate on the feature it names;
- is any row, column or segment clipped by the canvas edge;
- does the dominant element still dominate in grayscale.

A passing audit is not a correct drawing. In one build the audit was green while the crank
sat in the wrong projection, one panel split its subject across two half-views, and one
chart clipped every row.

A view that passes the audit and fails this look is usually one or two wrong decisions,
not a wrong idea, so **patch it by default**. Name the defect and give the geometry: an
agent told "it looks wrong" will restyle, an agent told "journals and pins are rectangles
in this projection, at these coordinates" will redraw only that part.

Rewrite a view only when the projection itself is wrong, and port the old feature list
into the new contract line by line. Before any rewrite, copy the file to
`panelX.js.old`, and after it count `querySelectorAll("*").length` against the copy: a
drop over ten percent means the rewrite discarded work that was already approved.
Regeneration is the cheapest way to lose detail and the easiest loss to miss, because a
simpler drawing still passes every mechanical check.

## Pitfalls

- **`childElementCount` counts top-level children only.** A panel that mounts one group
  reads as empty. Count `querySelectorAll("*").length`.
- **A headless `--window-size` is not the viewport.** Measure the scale from the SVG's
  `getBoundingClientRect()` against its viewBox, and print `innerWidth x innerHeight` in
  the audit verdict so a floor failure can be read at the size it happened.
- **Agents report success from a file that exists.** Require the test page and the
  screenshot, and re-run the audit yourself.
- **Vertical space is what pays for detail.** Adding a second bank, a bearing shell or a
  counterweight needs canvas height; a view that shares its band with four others can
  only grow sideways, which is why tabbing the views is often the cheaper move than
  shrinking the detail.
- **A rewrite is not a fix.** Deleting a panel and writing it again from the brief is the
  fastest way to lose detail: element counts fall, labels thin out, and the result still
  passes the audit. Back up first, patch the offending geometry, and compare counts.
- **Carry the old feature list forward.** When a panel has to be rebuilt, read the old
  file's labels and feature groups before writing, and tick each one off in the new
  version; memory of the brief is weaker than the file that was already reviewed.
