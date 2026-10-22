# Research method for illustration rules

Use when adding, changing, or challenging a rule in this skill suite, and when a figure's
accuracy ledger needs sources. The rules in `SKILL.md` are only as good as the method that
produced them; this file is that method, written down so the next extension is held to
the same bar.

## Five musts

1. **Web search for every claim. Model memory is not a source.** Search, open the page,
   and read the passage before writing the claim. A fact the model "knows" is a lead to
   search for, never a citation. If the search finds nothing, the claim goes under Not
   confirmed or becomes a declared local rule; it does not go in as fact.
2. **Open every source you cite.** Record the URL, the access date, and the document's
   own version or date when it shows one. A citation copied from another page's
   bibliography is second-hand and is labelled that way.
3. **Quote at most 25 words per claim, verbatim**, in quotation marks, on first use.
   One short exact quote per operative rule beats a chain of paraphrase.
4. **Every claim carries a status and a tier.** Status: confirmed (opened, quote found)
   or not confirmed (with what blocked it: paywall, 404, JavaScript-only, no date).
   Tier 1: standards, peer-reviewed papers, journal author guides, university course
   material, official design-system docs. Tier 2: practitioner books with a publisher
   page, studio or agency guidance, named educators. Tier 3: forums and undated lists,
   usable only to show a practice exists.
5. **Delegated findings are re-verified before use.** A child agent's report is a
   self-report. The parent reopens every load-bearing number and every quote a rule
   depends on, not a sample, before the rule enters a skill.

Canonical books (Itten, Arnheim, Tufte, Mayer, Bertin, Giesecke) may be cited at book
level. Any specific claim attributed to one needs a page that was actually opened: a
publisher preview, a course PDF that quotes it, an accessible chapter. Otherwise write
"book-level citation only".

## Standing of a rule

| Standing | Means | Example |
|---|---|---|
| STANDARD | a document says it | WCAG 1.4.3 contrast 4.5:1 |
| TAUGHT | a named teacher, textbook, or research line | value planned before hue |
| PRACTICE | working convention, observed in several places | palette as role plus hex |
| OPINION | taste, labelled as taste | shape language |
| declared local | no source resolves it; this skill decided | 3 detail callouts per 16:9 sheet |

Prescription is not description. "ISO 128 defines line types" is a standard; "thumbnails
are two inches tall" is one practitioner's habit. Labelling them differently is what
keeps habits from hardening into law.

Numbers need a source. Any threshold (line weight, font size at final size, contrast,
annotation count) names the document that states it, or is marked declared local.

## Wave structure

The suite came from two research waves; extend it the same way.

1. **Plan file first.** Write `planning/BRIEFING.md`: why the wave exists, the
   application context, the evidence rules, the source bar, the output contract per
   report, and working rules (which directories each agent may write). Every agent gets
   the briefing path and its own narrow question, not a long restated prompt.
2. **Domains as parents, sub-questions as children.** Wave 2 ran seven domains (P1 to
   P7), each with two children on one narrow sub-question each, each writing its own
   file. Children have no context from the parent, so the briefing carries it.
3. **Per-domain output contract.** Frontmatter with `sources_opened`, then Scope,
   Findings, Operative rules (imperative, tagged, sourced, checkable on a finished
   picture), What the sources disagree about, Gaps, Sources, Not confirmed.
4. **Extract, then re-verify.** Each parent writes an `EXTRACT.md` of its operative
   rules. The orchestrator reopens the load-bearing sources independently. In wave 2 this
   caught a spatial contiguity effect size attributed to the wrong meta-analysis; the
   rule survived, the attribution did not.
5. **Synthesis as a dependency spine.** `planning/SYNTHESIS.md` orders decisions by what
   each one needs settled first, and records conflicts and gaps. Gaps become the free
   parameters a spec must declare.
6. **Map rules back to sources.** `planning/corpus-map.md` lists every rule in the skills
   with the report and source it came from. A rule with no row is either given one or
   demoted to declared local. A report section no rule uses is listed as unused.

## Change control

The plan is followed as written, and when it changes, the plan file changes with it.

- A change to the wave plan (a domain added, a question narrowed, a source bar relaxed)
  edits `BRIEFING.md` in the same commit as the work that needed it, with one line saying
  what changed and why.
- A rule changed in a skill updates its corpus-map row in the same commit.
- A rule withdrawn is not deleted silently: it moves to the folklore list or to Not
  confirmed with the reason, so nobody re-adds it from memory.
- An execution that departs from its plan records the departure in the plan file's
  execution log before moving on, not in the final report.

## Pitfalls

- **A confident paraphrase with no quote** is the most common way memory enters as fact.
  If the quote cannot be found on the opened page, the claim is not confirmed.
- **The most-cited number is not always the right one.** Effect sizes travel between
  papers detached from their meta-analysis. Find the table that reports it.
- **A paywalled standard is not confirmed by its abstract.** ISO and ASME clause text was
  out of reach in wave 2; rules built on those standards cite the clause number and say
  the text was not opened.
- **Search results are leads, not sources.** A snippet is not the page.
