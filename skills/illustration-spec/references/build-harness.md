# Build harness for SVG figures

Use with section 9 (build contract), section 9b (mechanism), and section 10 (acceptance).
`delegated-illustration-build.md` covers the contract and the review round; this file
covers the machine that checks the build.

Everything here comes from a five-view build (a V8 engine figure) and its harness. Where
that build fell short, the shortfall is named, because the gaps taught more than the parts
that worked.

## Two halves

| Half | Runs | Checks | Why it lives there |
|---|---|---|---|
| page audit | inside the page, when `?audit=1` | element floor, labels, state sweep, invariants, paint servers | the page has the DOM and the model; one load can render every state |
| driver | outside, headless browser | matrix of view x viewport x sampled state, routing, screenshots, report | only the outside can change the viewport and see the pixels |

The page reports through `document.title`, which `--dump-dom` returns without any
automation library: `AUDIT CLEAN <view> <w>x<h>` or `AUDIT FAIL <reason>; <reason>`.
A JavaScript error must also land in the title (`JSERR <message>`), or a crash reads as a
missing title and the driver cannot tell a broken page from a slow one.

## Page audit

```js
// shell, after mount; FLOOR, INVARIANTS, STATE come from the spec (view map, 9b)
window.addEventListener("error", e => { document.title = "JSERR " + e.message; });

function audit(view) {
  const svg = document.querySelector(`#view-${view} svg`);
  const fails = [];
  const n = svg.querySelectorAll("*").length;            // descendants, not children
  if (n < FLOOR[view]) fails.push(`floor ${view} ${n}<${FLOOR[view]}`);
  const vb = svg.viewBox.baseVal, scale = svg.getBoundingClientRect().width / vb.width;
  for (const t of svg.querySelectorAll("text")) {
    const b = t.getBBox();
    if (b.x < 0 || b.y < 0 || b.x + b.width > vb.width || b.y + b.height > vb.height)
      fails.push(`off-canvas "${t.textContent}"@${b.x | 0},${b.y | 0}`);
    if (b.height * scale < MIN_LABEL_PX) fails.push(`small "${t.textContent}"`);
  }
  return fails.concat(sweep(svg), paintAudit());   // paintAudit: see svg-verify
}

function sweep(svg) {
  const fails = [], base = svg.querySelectorAll("*").length;
  for (let s = STATE.min; s <= STATE.max && fails.length < 8; s += STATE.step) {
    render(s);
    if (/NaN|Infinity/.test(svg.innerHTML)) fails.push(`NaN@${s}`);
    for (const [id, holds] of INVARIANTS) if (!holds(s, svg)) fails.push(`${id}@${s}`);
    if (svg.querySelectorAll("*").length !== base) fails.push(`nodes changed@${s}`);
  }
  render(STATE.initial);   // leave the page in the state the URL asked for
  return fails;
}
```

- **Sweep inside the page.** One load renders all 720 states in milliseconds; 720
  browser launches take minutes. The driver samples states for screenshots and layout,
  the page sweeps for invariants.
- **Report the first failing state by value** (`INV-02@437`), capped at a handful, so the
  title stays readable and the failure is reproducible with `?angle=437`.
- **`render` must update, never recreate.** The `nodes changed` check catches a render
  that appends on every call, which passes any single-frame check.
- **References must paint.** `paintAudit()` (code in `svg-verify`, Paint servers) fails on
  a duplicated id, a missing `url(#id)` target, or a target inside a `display:none` subtree
  used by a visible element. Chromium paints nothing in each case. The V8 shell injected
  one hatch pattern into all five tab SVGs, and tab B shipped with an unhatched section
  through a 116/116 harness run.
- **Invariants are functions of the state**, written from section 9b: two rods on one pin
  stay 90 degrees apart, exactly one dial numeral is lit and it names the firing
  cylinder, the pointer clears every numeral, no label overlaps another.

In the V8 build only the firing-order dial had a full sweep, on its standalone test page.
The crank, crankpin, and schedule views were checked at six sampled angles, and a rod
drawn along the pin axis in one of them was caught by eye. Put the sweep in the shell so
every view gets it.

## Driver

Matrix: every view, at every viewport the spec names, at the sampled states from 9b.
For the V8 build: 5 views x 3 viewports (1280x720, 1920x1080, 2560x1440) x 6 angles
(0, 90, 270, 450, 630, 719) = 90 page loads, each one read from its title.

```python
FLAGS = ["--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--virtual-time-budget=3000"]

def title(view, w, h, state):
    url = f"file://{PAGE}?tab={view}&audit=1&angle={state}"
    out = subprocess.run([CHROME, *FLAGS, f"--window-size={w},{h}", "--dump-dom", url],
                         capture_output=True, text=True, timeout=60).stdout
    m = re.search(r"<title>(.*?)</title>", out, re.S)
    return html.unescape(m.group(1)).strip() if m else None   # None is a failure
```

Then four checks a page audit cannot make on itself:

1. **Router distinctness.** Hash each view's DOM at one state; the number of distinct
   hashes must equal the number of views. A page that ignores `?tab=` passes every other
   row once per view. In the V8 build the first harness run found exactly this: five
   byte-identical dumps.
2. **Screenshot size.** Read width and height from the PNG IHDR chunk and compare with
   the window. A wrong size means the viewport row tested nothing.
3. **Screenshot not blank.** Count distinct colours; under 8 means nothing drew. A
   correctly sized white PNG passes the size check.
4. **Tokens from the contract.** Each view must contain the class names or data
   attributes its contract section promises (`data-cyl`, `counterweight`). Generate the
   list from `INTERFACE.md` rather than typing it into the driver: a hand-typed list drifts
   the first time a module renames a class, and then it either fails a correct page or
   checks nothing.

Write `shots/VERIFY.md`: one summary row per view (passed / total), then one table per
view with every check, expected value, actual value, and status. Exit 0 only when every
executed check passes.

## Test the harness before trusting it

A harness that has never failed has not been tested. Before the first real run, point it
at pages built to fail and confirm each one does:

| Fixture | Expected |
|---|---|
| page that throws on load | `JSERR`, row fails |
| page with no `<title>` | `None`, row fails, not crashes |
| page that ignores `?tab=` | router check fails |
| blank PNG of the right size | colour count fails |
| view one element under its floor | floor fails |
| render that appends a node per call | `nodes changed` fails |
| one invariant broken at a single state | `INV-nn@<state>` names that state |
| pattern id duplicated, first copy in a hidden view | `DUPID` and `HIDDENDEF` fail |

The V8 harness carried the first four; run against the earlier page it scored 110/116 and
exited 1, which is the evidence it could fail at all.

## Pitfalls

- **Green audit, wrong drawing.** The harness checks presence, position, and invariants;
  it does not know a crankpin is drawn in the wrong projection. Look at every view at the
  sampled states after the harness passes.
- **Token present, paint absent.** A class or token check proves an element carries the
  class, not that its fill renders. Pair every token check on a patterned or clipped
  feature with the paint-server check, or diff pixels with the defs moved to a visible host.
- **A floor typed from the finished drawing** tests nothing. Set it from the inventory
  before the build, and raise it only by a spec revision.
- **Virtual time is not real time.** `--virtual-time-budget` lets timers and fonts settle
  for headless capture; a figure that animates on load must expose its final state by
  parameter instead of relying on the budget.
- **`--window-size` is not the viewport** in every headless mode. Print
  `innerWidth x innerHeight` in the CLEAN title so each row records what it measured.
