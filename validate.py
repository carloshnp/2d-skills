#!/usr/bin/env python3
"""Validate skill/2d-skills before it is synced.

    python3 validate.py                 # every check
    python3 validate.py --against main  # also fail a file whose body shrank >10% since a ref

Run it with an interpreter that has PyYAML; Hermes's own venv does:
    ~/.hermes/hermes-agent/venv/bin/python validate.py

Router (SKILL.md)
  - frontmatter parses; name equals the folder; description starts "Use when" and is at
    most 60 chars; version is X.Y.Z; author present
  - every subskill in the Subskills table has references/<name>.md; every references/*.md
    is routed or listed; every file in scripts/ is listed
Subskills (the routed references/<name>.md files)
  - title on line 1, the "Subskill of `2d-skills`." line on line 3, no YAML frontmatter
  - illustration-spec: spine rows and fast-path questions match their prose counts
Every file
  - Markdown: code fences balanced; no banned adjective inside a "- REQ-" line
  - Markdown and Python: no em or en dash; every `references/...` and `scripts/...` path
    it names exists in the skill; Python compiles
  - line budget where one is declared (BUDGET)
With --against REF
  - no file lost more than 10 percent of its body lines (frontmatter and the subskill line
    excluded), following each file to its pre-2.0 path when REF predates the move

Exit 0 when every check passes.
"""

import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing: run with ~/.hermes/hermes-agent/venv/bin/python validate.py")

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "2d-skills"
SKILL = os.path.join(ROOT, "skill", NAME)
BUDGET = {"SKILL.md": (60, 160), "references/illustration-spec.md": (400, 600)}
BANNED = ("clear", "clean", "modern", "professional", "appealing", "balanced", "readable")
WORDS = {9: "Nine", 13: "thirteen"}
HEADER = "> Subskill of `%s`." % NAME


def read(rel):
    return open(os.path.join(SKILL, rel), encoding="utf-8").read()


def nlines(text):
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def body_lines(text):
    """Lines that carry content: frontmatter and the subskill line do not count."""
    lines = text.split("\n")
    if lines and lines[0] == "---" and "---" in lines[1:]:
        lines = lines[lines.index("---", 1) + 1:]
    return len([ln for ln in lines if not ln.startswith(HEADER)]) - (1 if text.endswith("\n") else 0)


def git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def at_ref(ref, rel):
    """The file's text at ref, at its 2.0 path or the pre-2.0 path it was moved from."""
    paths = ["skill/%s/%s" % (NAME, rel)]
    tree = (git("ls-tree", "-r", "--name-only", ref) or "").split()
    base = os.path.basename(rel)
    if rel.startswith("references/"):
        paths.append("skills/%s/SKILL.md" % base[:-3])
        paths += [p for p in tree if p.startswith("skills/") and p.endswith("/references/" + base)]
    elif rel.startswith("scripts/"):
        paths += [p for p in tree if p.startswith("skills/") and p.endswith("/scripts/" + base)]
    for p in paths:
        if p in tree:
            return git("show", "%s:%s" % (ref, p))
    return None


def frontmatter(text):
    parts = text.split("---", 2)
    if not (text.startswith("---") and len(parts) == 3):
        return None
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def check_router(text, out):
    fm = frontmatter(text)
    out.append(("frontmatter parses", fm is not None))
    if fm:
        desc = str(fm.get("description", ""))
        out.append(("name equals folder", fm.get("name") == NAME))
        out.append(("description starts Use when, <= 60 chars (%d)" % len(desc),
                    desc.startswith("Use when") and len(desc) <= 60))
        out.append(("version X.Y.Z", bool(re.fullmatch(r"\d+\.\d+\.\d+", str(fm.get("version", ""))))))
        out.append(("author present", bool(fm.get("author"))))
    table = text.split("## Subskills", 1)[1].split("\n## ", 1)[0] if "## Subskills" in text else ""
    routed = re.findall(r"^\| `([a-z0-9-]+)` \|", table, re.M)
    out.append(("%d subskills routed" % len(routed), len(routed) > 0))
    absent = [r for r in routed if not os.path.exists(os.path.join(SKILL, "references", r + ".md"))]
    out.append(("routed subskills have files %s" % absent, not absent))
    named = set(re.findall(r"`((?:references|scripts)/[\w./-]+)`", text))
    orphans = sorted(f for f in os.listdir(os.path.join(SKILL, "references"))
                     if f.endswith(".md") and f[:-3] not in routed and "references/" + f not in named)
    out.append(("every reference routed or listed %s" % orphans, not orphans))
    scripts_dir = os.path.join(SKILL, "scripts")
    unlisted = sorted(f for f in (os.listdir(scripts_dir) if os.path.isdir(scripts_dir) else [])
                      if f.endswith((".py", ".sh")) and "scripts/" + f not in named)
    out.append(("every script listed %s" % unlisted, not unlisted))
    return routed


def check_subskill(name, text, out):
    lines = text.split("\n")
    out.append(("no YAML frontmatter", not text.startswith("---")))
    out.append(("title on line 1", lines[0].startswith("# ")))
    out.append(("subskill line on line 3", len(lines) > 2 and lines[2].startswith(HEADER)))
    if name == "illustration-spec":
        spine = text[text.index("## The decision spine"):text.index("## View map")]
        rows = len(re.findall(r"^\| \d+ \|", spine, re.M))
        out.append(("spine rows (%d) match prose" % rows,
                    "%s decisions" % WORDS.get(rows, str(rows)) in spine))
        fast = text[text.index("## Fast path"):text.index("## Full path")]
        qs = len(re.findall(r"^\d+\. \*\*", fast, re.M))
        out.append(("fast path questions (%d) match prose" % qs,
                    WORDS.get(qs, str(qs)) in fast and "(%d questions" % qs in text))


def check_file(rel, text, out, against):
    if rel.endswith(".md"):
        out.append(("code fences balanced", text.count("```") % 2 == 0))
        bad = [w for ln in text.splitlines() if ln.strip().startswith("- REQ-")
               for w in BANNED if re.search(r"\b%s\b" % w, ln.lower())]
        out.append(("no banned adjectives in REQ lines %s" % bad, not bad))
    if rel.endswith(".py"):
        try:
            compile(text, rel, "exec")
            out.append(("compiles", True))
        except SyntaxError as e:
            out.append(("compiles (%s)" % e, False))
    dashes = [i for i, ln in enumerate(text.splitlines(), 1) if "\u2014" in ln or "\u2013" in ln]
    out.append(("no em/en dashes %s" % dashes[:3], not dashes))
    named = set(re.findall(r"`((?:references|scripts)/[\w./-]+)`", text))
    missing = sorted(p for p in named if not os.path.exists(os.path.join(SKILL, p)))
    out.append(("%d named paths exist %s" % (len(named), missing), not missing))
    if rel in BUDGET:
        lo, hi = BUDGET[rel]
        out.append(("line budget %d-%d (%d)" % (lo, hi, nlines(text)), lo <= nlines(text) <= hi))
    if against:
        old = at_ref(against, rel)
        if old:
            before, now = body_lines(old), body_lines(text)
            drop = (before - now) / before if before else 0
            out.append(("body vs %s: %d -> %d (%+.0f%%)" % (against, before, now, -drop * 100),
                        drop <= 0.10))


def main():
    against = sys.argv[sys.argv.index("--against") + 1] if "--against" in sys.argv else None
    if not os.path.isfile(os.path.join(SKILL, "SKILL.md")):
        sys.exit("no skill at %s" % SKILL)
    rels = sorted(os.path.relpath(os.path.join(r, f), SKILL)
                  for r, _d, fs in os.walk(SKILL) for f in fs
                  if f.endswith((".md", ".py")) and "__pycache__" not in r)
    routed = []
    failed = 0
    for rel in ["SKILL.md"] + [r for r in rels if r != "SKILL.md"]:
        text = read(rel)
        out = []
        if rel == "SKILL.md":
            routed = check_router(text, out)
        elif rel.startswith("references/") and os.path.basename(rel)[:-3] in routed:
            check_subskill(os.path.basename(rel)[:-3], text, out)
        check_file(rel, text, out, against)
        bad = [label for label, ok in out if not ok]
        failed += len(bad)
        print("%-45s %s  %d lines" % (rel, "FAIL" if bad else "ok  ", nlines(text)))
        for label in bad:
            print("    FAIL " + label)
    print("\n%d failing checks" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
