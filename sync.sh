#!/usr/bin/env bash
# sync.sh: install the skills in this repo into Hermes, and prove it.
#
#   bash sync.sh            copy skills/* into the target, then verify
#   bash sync.sh --check    verify only, no writes
#   bash sync.sh --dry-run  list what would be copied, no writes
#
# Target defaults to ~/.hermes/skills/svg; override with SKILLS_DIR=/path.
# Exit 0 only when every file in the repo matches the target by sha256 and the
# target holds no skill file the repo does not have.
#
# EXTRA means a file exists in the target but not in the repo: somebody edited
# an installed skill in place. Copy it back into the repo and commit it before
# syncing, or it will keep drifting.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO/skills"
DST="${SKILLS_DIR:-$HOME/.hermes/skills/svg}"
MODE="${1:-install}"

case "$MODE" in
  install|--check|--dry-run) ;;
  -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
  *) echo "unknown option: $MODE" >&2; exit 2 ;;
esac

[ -d "$SRC" ] || { echo "no skills/ directory at $SRC" >&2; exit 2; }

list_files() { (cd "$1" && find . -type f ! -name '*.pyc' ! -path '*/__pycache__/*' | sed 's|^\./||' | sort); }

if [ "$MODE" = "--dry-run" ]; then
  echo "would copy $SRC -> $DST"
  list_files "$SRC" | sed 's/^/  /'
  exit 0
fi

if [ "$MODE" = "install" ]; then
  mkdir -p "$DST"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    mkdir -p "$DST/$name"
    cp -a "$skill". "$DST/$name/"
  done
  echo "copied $(list_files "$SRC" | wc -l) files into $DST"
fi

fail=0
match=0
while IFS= read -r rel; do
  if [ ! -f "$DST/$rel" ]; then
    printf 'MISSING   %s\n' "$rel"; fail=1; continue
  fi
  a="$(sha256sum "$SRC/$rel" | cut -c1-64)"
  b="$(sha256sum "$DST/$rel" | cut -c1-64)"
  if [ "$a" = "$b" ]; then
    match=$((match + 1))
  else
    printf 'MISMATCH  %s\n' "$rel"; fail=1
  fi
done < <(list_files "$SRC")

# only inspect skills this repo owns, so unrelated skills in the target are ignored
while IFS= read -r rel; do
  skill="${rel%%/*}"
  [ -d "$SRC/$skill" ] || continue
  [ -f "$SRC/$rel" ] || { printf 'EXTRA     %s\n' "$rel"; fail=1; }
done < <(list_files "$DST")

total="$(list_files "$SRC" | wc -l)"
if [ "$fail" -eq 0 ]; then
  echo "OK: $match/$total files match in $DST"
else
  echo "FAIL: $match/$total files match in $DST" >&2
fi
exit "$fail"
