# Dimensioned CAD-style mechanical sections

When a cross-section must read as an engineering drawing rather than a cartoon:
use real-unit coordinates, dimension lines, centerlines, and material fills,
and verify every mechanical joint visually.

## Real-unit viewBox

- Set 1 user unit = 1 mm (or 0.1 mm) and take proportions from published practice
  (bore, stroke, rod centers, deck height). Compute shared anchors once in a script
  (axis points, seat/pivot positions, port corners) and mirror about the centerline.
- State the basis in the figure (`SECTION A-A · 1 unit = 1 mm · bore …`) and flag
  simplifications in the caption (splayed valves, one pushrod of a pair shown,
  trapezoidal lift); never silently stylize measured-looking numbers.

## Dimension layer

- Thin teal lines with arrow markers on both ends, monospace values with a white
  halo (`paint-order: stroke`), extension lines from the measured features.
- Typical set: bore diameter, stroke, rod centers, deck height, bank-angle arc,
  journal diameter callouts. Five to six dims; more belongs in a table.

## Centerlines and section fills

- Red chain-dash (`18 4 3 4`) along every axis of motion and symmetry, plus shaft
  center crosses. 45-degree hatch for cut casting; distinct flat fills per material
  (steel, aluminum, bronze guides); coolant dots inside jackets.

## Slider-crank kinematics (screen frame, y down, clockwise positive)

- Pin `P = C + R·(cos a, sin a)`; piston distance along bore axis
  `t = b + sqrt(b² − c)` with `b = (P−C)·u`, `c = |P−C|² − L²`.
- Piston group is `translate(Q) rotate(bankAngle)` with crown art in local units;
  crank group is `translate(C) rotate(a)` with the counterweight wedge opposite
  the pin in crank-local coordinates.

## Flame front instead of starbursts

- Two to three nested irregular closed contours (dark orange outer, amber middle,
  yellow inner) plus a pale kernel circle at the plug gap.
- Clip gas and flame to the bore with a `clipPath` in piston-local coordinates;
  scale the flame about the crown by available height so it collapses to a kernel
  flash at top dead center and grows as the piston descends.

## Joint closure

- Every connected part must touch its neighbor: runner meets port face, manifold
  meets head, cam sits below the lifters inside the valley, plug gap inside the
  chamber. Gaps under ~3 units read as detached parts in a capture, so check
  joints in a zoomed screenshot, not by coordinate inspection.
- Rocker/pushrod linearization for small lifts: valve origin = seat − outward·off;
  tip = tip0 − outward·off; cup = pivot + (pivot − tip)·0.9; arm path
  `M cup L pivot L tip`; pushrod top = midpoint of cups; lifter rise =
  off / rocker-ratio.
