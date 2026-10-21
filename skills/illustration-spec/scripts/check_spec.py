#!/usr/bin/env python3
"""Mechanical audit for an illustration spec, run before presenting it for approval.

Checks
  1. every REQ-* has exactly one acceptance row in section 10, and every acceptance
     row names a REQ-* that exists in section 7
  2. no banned adjectives inside requirement text
  3. counts stated in prose match the tables they describe (elements, colours)
  4. no em or en dashes
  5. section 9b, when present, states STATE, DATUM, and at least one INV-nn
     invariant, or says "none"

Usage
  python3 check_spec.py path/to/FIG-XX-NN.md

Exit code 0 when clean, 1 when there are findings. Warnings never change the exit code.
"""

import re
import sys

BANNED = (
    "clear",
    "clean",
    "modern",
    "professional",
    "appealing",
    "balanced",
    "readable",
)

ONES = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine".split())}
TEENS = {w: 10 + i for i, w in enumerate(
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split())}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}


def parse_count(token):
    t = token.strip().lower()
    if t.isdigit():
        return int(t)
    if t in TEENS:
        return TEENS[t]
    if t in TENS:
        return TENS[t]
    if "-" in t:
        head, _, tail = t.partition("-")
        if head in TENS and tail in ONES:
            return TENS[head] + ONES[tail]
    return None


def find_sections(lines):
    """Map leading section number to (start, end) line indices.

    Plain sections are keyed by int (7); lettered ones by string ("9b").
    """
    marks = []
    for i, ln in enumerate(lines):
        m = re.match(r"^##\s+(\d+)([a-z]?)[.\s]", ln)
        if m:
            key = int(m.group(1)) if not m.group(2) else m.group(1) + m.group(2)
            marks.append((key, i))
    marks.sort(key=lambda pair: pair[1])
    out = {}
    for idx, (num, start) in enumerate(marks):
        end = marks[idx + 1][1] if idx + 1 < len(marks) else len(lines)
        out[num] = (start, end)
    return out


def table_cells(lines, start, end):
    """Yield (line_number, cells) for real table rows, skipping rules and headers."""
    for offset, ln in enumerate(lines[start:end]):
        s = ln.strip()
        if not s.startswith("|"):
            continue
        if set(s) <= set("|-: "):
            continue
        yield start + offset + 1, [c.strip() for c in s.strip("|").split("|")]


def main(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print("cannot read %s: %s" % (path, exc))
        return 1

    lines = text.splitlines()
    sections = find_sections(lines)
    fails = []
    warns = []

    # 1. traceability
    reqs = []  # (line_number, id, tagged)
    block = sections.get(7)
    if block is None:
        fails.append("no '## 7. Requirements' section found")
    else:
        for offset, ln in enumerate(lines[block[0]:block[1]]):
            m = re.match(r"^-\s+(REQ-[A-Za-z0-9]+-\d+)\s+\[(MUST|SHOULD)\]", ln)
            if m:
                reqs.append((block[0] + offset + 1, m.group(1), m.group(2)))
        if not reqs:
            fails.append("section 7 has no lines matching '- REQ-<id> [MUST|SHOULD]'")

    accepted = []
    block = sections.get(10)
    if block is None:
        fails.append("no '## 10. Acceptance criteria' section found")
    else:
        for line_no, cells in table_cells(lines, block[0], block[1]):
            if cells and cells[0].startswith("REQ-"):
                accepted.append((line_no, cells[0]))
        if not accepted:
            fails.append("section 10 has no rows whose first cell is a REQ id")

    req_ids = [r[1] for r in reqs]
    dupes = sorted({i for i in req_ids if req_ids.count(i) > 1})
    for d in dupes:
        fails.append("duplicate requirement id %s" % d)

    for line_no, rid, _tag in reqs:
        if rid not in [a[1] for a in accepted]:
            fails.append("line %d: %s has no acceptance row" % (line_no, rid))
    for line_no, aid in accepted:
        if aid not in req_ids:
            fails.append("line %d: acceptance row %s has no requirement" % (line_no, aid))

    # 2. banned adjectives inside requirement blocks
    if block is not None or sections.get(7):
        start, end = sections.get(7, (0, 0))
        current = None
        current_line = 0
        for offset, ln in enumerate(lines[start:end]):
            if ln.startswith("- REQ-") or ln.startswith("## "):
                current = ln
                current_line = start + offset + 1
            elif current is not None and ln.strip():
                current = current + " " + ln.strip()
            if current is not None:
                lowered = current.lower()
                for word in BANNED:
                    if re.search(r"\b%s\b" % word, lowered):
                        fails.append(
                            "line %d: banned adjective '%s' in requirement text"
                            % (current_line, word))
                        current = current.replace(word, "")

    # 3. counts in prose against the tables
    block = sections.get(6)
    if block:
        rows = [c for _n, c in table_cells(lines, block[0], block[1])
                if c and re.match(r"^[A-Za-z][A-Za-z0-9]*-\d+$", c[0])]
        stated = None
        for ln in lines[block[0]:block[1]]:
            m = re.search(r"\b([A-Za-z]+(?:-[A-Za-z]+)?|\d+)\s+elements\b", ln, re.I)
            if m:
                stated = parse_count(m.group(1))
                break
        if stated is not None and stated != len(rows):
            fails.append(
                "section 6 states %d elements but the inventory table has %d rows"
                % (stated, len(rows)))

    block = sections.get(5)
    if block:
        rows = [c for _n, c in table_cells(lines, block[0], block[1])
                if "#" in "|".join(c)]
        stated = None
        for ln in lines[block[0]:block[1]]:
            m = re.search(r"\b([A-Za-z]+(?:-[A-Za-z]+)?|\d+)\s+colou?rs\b", ln, re.I)
            if m:
                stated = parse_count(m.group(1))
                break
        if stated is not None and stated != len(rows):
            fails.append(
                "section 5 states %d colours but the palette table has %d rows"
                % (stated, len(rows)))

    # 4. dashes
    for i, ln in enumerate(lines, start=1):
        if "\u2014" in ln or "\u2013" in ln:
            fails.append("line %d: em or en dash" % i)

    # 5. mechanism section
    block = sections.get("9b")
    if block is None:
        warns.append("no '## 9b. Mechanism and state model': confirm nothing is derived")
    else:
        body = "\n".join(lines[block[0] + 1:block[1]])
        if not re.search(r"^\s*none\b", body, re.I | re.M):
            for field in ("STATE", "DATUM"):
                if not re.search(r"^-\s+%s:\s*\S" % field, body, re.M):
                    fails.append("section 9b has no '- %s:' line with content" % field)
            if not re.search(r"\bINV-\d+", body):
                fails.append("section 9b states no INV-nn invariant")

    if sections.get(11) is None:
        warns.append("no '## 11. Open questions' section")
    if sections.get(12) is None:
        warns.append("no '## 12. Revision history' section")

    for msg in fails:
        print("FAIL  " + msg)
    for msg in warns:
        print("WARN  " + msg)
    print("\n%d requirements, %d acceptance rows, %d findings"
          % (len(reqs), len(accepted), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
