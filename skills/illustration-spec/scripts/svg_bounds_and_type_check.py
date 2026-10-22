#!/usr/bin/env python3
"""Static checks an SVG audit usually misses: canvas bounds and effective type size.

Two failures that survive element-count and inventory-id audits:

1. An element drawn outside its viewBox. It clips at render time and looks like a
   layout bug in review. Coordinates in x/y/width/height/cx/cy/r are checkable without
   rasterising.
2. Type sized against the canvas instead of the column it lands in. A 14 px label on a
   1000 px sheet renders near 5 px in a 350 px phone column. Compute the effective size
   and compare against a legibility floor.

Usage:
    python3 svg_bounds_and_type_check.py svg/*.svg
    python3 svg_bounds_and_type_check.py --column-px 350 --floor 11 svg/*.svg

Exit code is 1 when any file has an out-of-bounds element or type below the floor.

Note: only literal numeric attributes are checked. Paths (d="...") and text whose
position is set by a transform are not measured; confirm those visually or with a
raster. This is a cheap gate, not a replacement for looking at the picture.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ATTR = re.compile(r'\b([a-zA-Z-]+)="(-?[\d.]+)"')
TAG = re.compile(r"<(rect|text|circle|image|use)\b[^>]*>")
FONT_ATTR = re.compile(r'font-size="(-?[\d.]+)"')
FONT_CLASS = re.compile(r'\.([a-zA-Z0-9_-]+)\s*\{[^}]*font-size:\s*(-?[\d.]+)')
CLASS_ATTR = re.compile(r'class="([^"]*)"')


def viewbox(text: str) -> tuple[float, float] | None:
    m = re.search(r'viewBox="([\d.\s-]+)"', text)
    if not m:
        return None
    parts = [float(v) for v in m.group(1).split()]
    if len(parts) != 4:
        return None
    return parts[2], parts[3]


def external_refs(text: str) -> list[str]:
    """Real external references only: the SVG and xlink namespace URIs are required."""
    hits = []
    for m in re.finditer(r'https?://[^"\s>]+', text):
        url = m.group(0)
        if url.rstrip("/") in (SVG_NS, XLINK_NS):
            continue
        hits.append(url)
    return hits


def min_font(text: str) -> tuple[float | None, str]:
    """Smallest font size, from literal attributes or from a class's CSS declaration."""
    sizes: list[tuple[float, str]] = []
    for m in FONT_ATTR.finditer(text):
        sizes.append((float(m.group(1)), "attr"))
    css = {name: float(size) for name, size in FONT_CLASS.findall(text)}
    for m in CLASS_ATTR.finditer(text):
        for cls in m.group(1).split():
            if cls in css:
                sizes.append((css[cls], f"class .{cls}"))
    if not sizes:
        return None, "none"
    size, source = min(sizes)
    return size, source


def bounds_hits(text: str, width: float, height: float, tol: float = 1.0) -> list[str]:
    hits: list[str] = []
    for tag_match in TAG.finditer(text):
        tag = tag_match.group(0)
        tag_name = tag_match.group(1)
        attrs: dict[str, float] = {}
        for name, value in ATTR.findall(tag):
            try:
                attrs[name] = float(value)
            except ValueError:
                continue
        x, y = attrs.get("x"), attrs.get("y")
        w, h = attrs.get("width"), attrs.get("height")
        cx, cy, r = attrs.get("cx"), attrs.get("cy"), attrs.get("r")
        if x is not None and (x < -tol or x > width + tol):
            hits.append(f"<{tag_name}> x={x:g} outside 0..{width:g}")
        if y is not None and (y < -tol or y > height + tol):
            hits.append(f"<{tag_name}> y={y:g} outside 0..{height:g}")
        if x is not None and w is not None and x + w > width + tol:
            hits.append(f"<{tag_name}> x+w={x + w:g} past {width:g}")
        if y is not None and h is not None and y + h > height + tol:
            hits.append(f"<{tag_name}> y+h={y + h:g} past {height:g}")
        if cx is not None and r is not None and (cx - r < -tol or cx + r > width + tol):
            hits.append(f"<{tag_name}> cx-r..cx+r={cx - r:g}..{cx + r:g} outside 0..{width:g}")
        if cy is not None and r is not None and (cy - r < -tol or cy + r > height + tol):
            hits.append(f"<{tag_name}> cy-r..cy+r={cy - r:g}..{cy + r:g} outside 0..{height:g}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--column-px", type=float, default=None,
                    help="width the figure renders at in its narrowest medium (e.g. 350)")
    ap.add_argument("--floor", type=float, default=11.0,
                    help="legibility floor in CSS px at that width (default 11)")
    ap.add_argument("--tol", type=float, default=1.0, help="bounds tolerance in user units")
    args = ap.parse_args()

    failures = 0
    for path in args.files:
        text = path.read_text()
        vb = viewbox(text)
        if vb is None:
            print(f"?    {path.name:34s} no viewBox")
            failures += 1
            continue
        width, height = vb
        hits = bounds_hits(text, width, height, args.tol)
        ext = external_refs(text)
        size, source = min_font(text)

        line = f"{'ok  ' if not hits and not ext else 'FAIL'} {path.name:34s} {width:g}x{height:g}"
        if size is not None:
            line += f"  min {size:g}px ({source})"
            if args.column_px:
                eff = size * (args.column_px / width)
                flag = "" if eff >= args.floor else f"  BELOW FLOOR {args.floor:g}"
                line += f" -> {eff:.1f}px at {args.column_px:g}px{flag}"
                if eff < args.floor:
                    failures += 1
        print(line)
        for h in hits:
            print(f"       bounds: {h}")
            failures += 1
        for u in ext:
            print(f"       external: {u}")
            failures += 1

    print(f"\n{len(args.files)} file(s), {failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
