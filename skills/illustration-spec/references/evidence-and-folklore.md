# Evidence and folklore

The rules this skill relies on, each with its standing, and the claims it refuses to
write into a spec. Moved out of `SKILL.md` to keep the decision workflow within its
length budget; nothing here was shortened in the move.

How a rule earns or loses its standing: `research-method.md`. Which report and source
each rule came from: `planning/corpus-map.md` in the 2d-research workspace.

## Rules worth carrying, with their standing

STANDARD means a document says it. TAUGHT means a named teacher or textbook. PRACTICE
means working convention. OPINION means taste, and it must be labelled as such.

| Rule | Standing | Where it comes from |
|---|---|---|
| One dominant element; at least two focal mechanisms | TAUGHT | composition literature |
| Hierarchy capped at three levels | TAUGHT | composition literature |
| Value planned before hue: notan, then values, then colour | TAUGHT (notan step PRACTICE) | painting and concept-art teaching |
| Palette documented as role plus hex, never as swatches | PRACTICE | art bibles, design systems |
| Projection declared, one convention per sheet, never mixed | STANDARD | ISO 5456-2, ASME Y14.3 (scope only, clause not opened); rule text via RoyMech |
| Outline thick, annotation thin, ratio about 2:1 or more | STANDARD | ASME Y14.2-2008, opened: "approximately two-to-one", 0.3/0.6 mm minima; ISO 128-2 scope only |
| Dashed is hidden; chain-thin is centreline; chain with thick ends is a cutting plane | STANDARD | ISO 128-2 (scope only, clause not opened); rule text via RoyMech |
| Dimensions once only, outside the outline, readable from the bottom | STANDARD | ISO 129-1 (scope only, clause not opened); rule text via a university drafting lecture |
| Hatch at 45 degrees, one angle per part, broken around labels | STANDARD | USPTO 37 CFR 1.84 (open text); ISO 128-44 scope only |
| Capitals, one lettering style, at least 3.5 mm at final size | STANDARD (one style) / TAUGHT (capitals, 3.5 mm) | ASME Y14.2-2008, opened, for one style; RoyMech for capitals and 3.5 mm (print minima); ISO 3098-1 scope only |
| Isometric at 30/30/vertical; 0.816 only for registration against orthographic | TAUGHT | technical drawing canons |
| Axonometric rather than perspective when readers compare sizes or order | PRACTICE | technical illustration |
| Balloons tied to a parts list; leaders never cross, never point at voids | STANDARD | assembly drawing convention, via a practitioner guide; ASME text not opened |
| Position on a common scale is the most accurate encoding; avoid angle, area, hue for the take-home quantity | TAUGHT | Cleveland and McGill (1984), replicated |
| Delete every element with no teaching job | STANDARD | Sundararajan and Adesope (2020) meta-analysis, g = -0.33 overall, -0.43 static |
| Label on the part, not in a detached legend | STANDARD | Schroeder and Cenkci (2018) meta-analysis, g = 0.63 |
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
