#!/usr/bin/env python3
"""Validate every skill in skills/ before it is synced.

    python3 validate.py                 # all skills
    python3 validate.py --against main  # also fail a SKILL.md that shrank >10% since a ref

Run it with an interpreter that has PyYAML; Hermes's own venv does:
    ~/.hermes/hermes-agent/venv/bin/python validate.py

Checks per skill
  - frontmatter parses as YAML; name equals the directory; description <= 60 chars;
    version present
  - code fences balanced
  - no em or en dashes in any .md or .py file of the skill
  - every `references/...` and `scripts/...` path named in SKILL.md exists
  - no banned adjective inside a "- REQ-" line
  - line budget where one is declared (BUDGET)
  - illustration-spec only: spine rows and fast-path questions match their prose counts
  - with --against: SKILL.md line count did not drop more than 10 percent

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
SKILLS = os.path.join(ROOT, "skills")
BUDGET = {"illustration-spec": (400, 600)}
BANNED = ("clear", "clean", "modern", "professional", "appealing", "balanced", "readable")
WORDS = {9: "Nine", 13: "thirteen"}


def files_of(skill_dir):
    for root, _dirs, names in os.walk(skill_dir):
        for n in names:
            if n.endswith((".md", ".py")):
                yield os.path.join(root, n)


def git_lines(ref, rel):
    try:
        out = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (ref, rel)],
                             capture_output=True, text=True, check=True).stdout
        return out.count("\n") + 1
    except subprocess.CalledProcessError:
        return None


def check_skill(name, against):
    d = os.path.join(SKILLS, name)
    path = os.path.join(d, "SKILL.md")
    out = []

    def check(label, ok):
        out.append(("PASS" if ok else "FAIL", label))

    if not os.path.exists(path):
        check("SKILL.md exists", False)
        return out
    text = open(path, encoding="utf-8").read()
    n = text.count("\n") + 1

    parts = text.split("---", 2)
    fm = None
    try:
        fm = yaml.safe_load(parts[1]) if text.startswith("---") and len(parts) == 3 else None
    except yaml.YAMLError:
        fm = None
    check("frontmatter parses", isinstance(fm, dict))
    if isinstance(fm, dict):
        check("name equals directory", fm.get("name") == name)
        desc = str(fm.get("description", ""))
        check("description <= 60 chars (%d)" % len(desc), 0 < len(desc) <= 60)
        check("version present", bool(fm.get("version")))

    check("code fences balanced", text.count("```") % 2 == 0)

    dashes = ["%s:%d" % (os.path.relpath(f, d), i)
              for f in files_of(d)
              for i, ln in enumerate(open(f, encoding="utf-8"), 1)
              if "\u2014" in ln or "\u2013" in ln]
    check("no em/en dashes %s" % dashes[:3], not dashes)

    named = set(re.findall(r"`((?:references|scripts)/[\w./-]+)`", text))
    missing = sorted(p for p in named if not os.path.exists(os.path.join(d, p)))
    check("%d named files exist %s" % (len(named), missing), not missing)

    bad = [w for ln in text.splitlines() if ln.strip().startswith("- REQ-")
           for w in BANNED if re.search(r"\b%s\b" % w, ln.lower())]
    check("no banned adjectives in REQ lines %s" % bad, not bad)

    if name in BUDGET:
        lo, hi = BUDGET[name]
        check("line budget %d-%d (%d)" % (lo, hi, n), lo <= n <= hi)

    if name == "illustration-spec":
        spine = text[text.index("## The decision spine"):text.index("## View map")]
        rows = len(re.findall(r"^\| \d+ \|", spine, re.M))
        check("spine rows (%d) match prose" % rows,
              "%s decisions" % WORDS.get(rows, str(rows)) in spine)
        fast = text[text.index("## Fast path"):text.index("## Full path")]
        qs = len(re.findall(r"^\d+\. \*\*", fast, re.M))
        check("fast path questions (%d) match prose" % qs,
              WORDS.get(qs, str(qs)) in fast and "(%d questions" % qs in text)

    if against:
        before = git_lines(against, "skills/%s/SKILL.md" % name)
        if before:
            drop = (before - n) / before
            check("lines vs %s: %d -> %d (%+.0f%%)" % (against, before, n, -drop * 100),
                  drop <= 0.10)
    out.append(("INFO", "%d lines" % n))
    return out


def main():
    against = None
    if "--against" in sys.argv:
        against = sys.argv[sys.argv.index("--against") + 1]
    failed = 0
    for name in sorted(os.listdir(SKILLS)):
        if not os.path.isdir(os.path.join(SKILLS, name)):
            continue
        results = check_skill(name, against)
        bad = [r for r in results if r[0] == "FAIL"]
        failed += len(bad)
        info = [r[1] for r in results if r[0] == "INFO"]
        print("%-22s %s  %s" % (name, "FAIL" if bad else "ok  ", ", ".join(info)))
        for _s, label in bad:
            print("    FAIL " + label)
    print("\n%d failing checks" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
