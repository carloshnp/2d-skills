# Technical sheet conventions for explainer figures

Depth for figures that borrow engineering-drawing conventions but are not manufacturing
documents. The distinction matters: half the rules in a real drawing standard exist so a
part can be made, and importing them into an explainer adds constraint without adding
clarity.

## Adopt, versus exclude

| Adopt for an explainer | Exclude: manufacture or acceptance rules |
|---|---|
| Declared projection, one convention per sheet | Sheet sizes, margins, title-block layout |
| Outline thick, annotation thin, ratio >= 2:1 | Absolute millimetre minima taken from print |
| Dashed hidden, chain centreline, chain-with-thick-ends cutting plane | Patent sheet rules, reference-character sizes |
| Dimensions once, outside the outline, bottom-reading | Tolerance callouts, interface-only assembly dims |
| Hatch at 45 degrees, one angle per part | Standard hardware left unsectioned |
| Capitals, one lettering style | Ink and paper acceptance criteria |
| Axonometric when readers compare sizes or follow order | Full GD&T |

Every millimetre value in a standard is a print-sheet value at a stated scale. On screen
there is no scale until the spec declares one, so re-derive the number and label it
"declared local".

## Projection declaration

State it in section 4 and repeat it in section 5: orthographic first or third angle,
axonometric, flat schematic, or none. One convention per sheet. A section view, an end
view, and a chart can coexist because a chart is not a projection; two different
projections of the same subject cannot.

A section is a plane, so name it: "section A-A along the crank axis, viewed from the
left". Readers reconstruct the cut from that sentence alone, and a wrong cut is
unfixable later.

### What a section actually shows

A section answers one question: which features does this cutting plane pass through? That
answer fixes each feature's mark shape, and getting it wrong is the commonest way a
correct drawing still reads as broken.

- A cylinder whose axis lies in the cutting plane is a **rectangle** (journals, pins,
  shafts, bolts seen lengthwise). A cylinder whose axis is perpendicular to the plane is a
  **circle**. Drawing a crankpin as a circle inside a longitudinal section pastes an end
  view into a side view, and the result reads as unmechanical even to a reader who cannot
  name why.
- A part behind the plane is a **hidden** outline: long dash, narrower silhouette, and a
  small axial offset so it never coincides with the near part. A thinner solid line at the
  same position reads as a duplicate, not as depth.
- Webs, fillets and counterweights in profile carry most of the mechanical credibility. A
  shaft drawn as its journals and pins alone looks like beads on a string.
- Dimensions annotate a quantity, or they annotate a false claim. With no sourced number,
  draw the extension lines and label the quantity (`stroke`, `bore spacing`) and stop; a
  plausible millimetre value no source supports can be measured against the drawing and
  will not match.

## Line grammar on screen

Standards give print line widths and a floor ratio. For SVG, declare a three-weight
scale and keep the ratio:

- outline 2.0 px, annotation 1.0 px (ratio 2:1), centreline 0.75 px dash-dot
- hidden 1.0 px dashed, dash pattern 6 3
- detail boundary 0.75 px chain, thin

Nothing below 3 px in a 1180 px-wide figure is meaningful detail; that is a declared
local floor, not a standard.

## Detail callouts

A detail is not a second drawing. It is the parent view, magnified:

- chain-thin boundary drawn around the source feature in the parent
- the same boundary repeated as a circle or frame in the detail
- one leader from boundary to boundary, or a letter pair (D and D)
- the scale in the label: `D 3:1`

Derive the detail's geometry by transforming the parent's coordinates, not by redrawing.
Then a dimension check in the parent also validates the detail, and the two cannot drift.

## Materials labels

When a section exposes an interface between two materials, that interface is the
interesting content, not a footnote:

- one label, one leader, terminating on the interface line itself
- name both materials, three words maximum: `Al block, iron liner`
- the caption names the specific variant, because a family of parts rarely shares one
  material (an engine family with both aluminium and cast iron blocks is the normal case)

## Factual accuracy ledger

Sits after the revision history, opens at G0, and closes only at the accuracy gate
between G3 and G4.

| Claim in the figure | Status |
|---|---|
| four crankpins, two cylinders each, offset 90 degrees | confirmed, source, date, short quote |
| firing order 1-8-7-2-6-5-4-3 | confirmed, source, quote |
| rods sit side by side on the journal | Tier 3 only, confirm or annotate before G3 |
| five main journals | Tier 3 only, drop the label if unconfirmed |

Status vocabulary, used literally:

- **confirmed**: opened a source during this work, quote recorded, tier noted
- **Tier 3 only**: exists on low-tier pages, not yet safe to assert
- **not used**: deliberately excluded, with the reason
- **excluded**: outside the figure's non-goals

A ledger row that says "Tier 3 only" is doing its job. A claim that never got a row is
the failure this table exists to prevent, because a plausible drawing of a mechanism is
indistinguishable from a correct one once it is on the screen.
