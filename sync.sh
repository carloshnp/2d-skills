#!/usr/bin/env bash
# sync.sh: install skill/2d-skills into Hermes as one skill, and prove it.
#
#   bash sync.sh                  install (refuses to overwrite in-place edits), then verify
#   bash sync.sh --check          verify only; exit 0 when the install equals the repo
#   bash sync.sh --dry-run        show what install would do; no writes
#   bash sync.sh --pull           copy in-place edits from the install back into the repo
#   bash sync.sh --remove-legacy  delete the pre-2.0 copies under svg/, only if git holds them
#
# Target: ${SKILLS_DIR:-~/.hermes/skills}/2d-skills. The install keeps a hash list of what
# it wrote in .sync-baseline, so a later difference can be told apart:
#   STALE    the repo changed since the last install; install will update it
#   EDITED   the installed copy changed in place (a skill_manage patch); pull it first
#   CONFLICT both changed; merge by hand
#   MISSING  in the repo, absent from the install
# Exit codes: 0 ok, 1 differences, 2 usage, 3 refused (unpulled edits), 4 legacy not in git.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="2d-skills"
SRC="$REPO/skill/$NAME"
ROOT="${SKILLS_DIR:-$HOME/.hermes/skills}"
DST="$ROOT/$NAME"
BASE="$DST/.sync-baseline"
LEGACY=(illustration-spec svg-animation svg-d3-charts svg-defs svg-explainer-layout
        svg-fundamentals svg-geometry svg-interaction svg-verify)
MODE="${1:-install}"

case "$MODE" in
  install|--check|--dry-run|--pull|--remove-legacy) ;;
  -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
  *) echo "unknown option: $MODE" >&2; exit 2 ;;
esac
[ -f "$SRC/SKILL.md" ] || { echo "no skill at $SRC" >&2; exit 2; }

list_files() { (cd "$1" && find . -type f ! -name '.sync-baseline' ! -name '*.pyc' \
                 ! -path '*/__pycache__/*' | sed 's|^\./||' | sort); }
hash_of() { [ -f "$1" ] && sha256sum "$1" | cut -c1-64 || echo "-"; }
base_of() { { [ -f "$BASE" ] && awk -v f="$1" '$2 == f {print $1}' "$BASE" | head -1; } || true; }

# classify every path in repo or install; prints "STATE path"
classify() {
  { list_files "$SRC"; [ -d "$DST" ] && list_files "$DST"; } | sort -u | while IFS= read -r rel; do
    s="$(hash_of "$SRC/$rel")"; d="$(hash_of "$DST/$rel")"; b="$(base_of "$rel")"
    if [ "$s" = "$d" ]; then echo "OK $rel"
    elif [ "$d" = "-" ]; then echo "MISSING $rel"
    elif [ -n "$b" ] && [ "$d" = "$b" ]; then echo "STALE $rel"
    elif [ -n "$b" ] && [ "$s" = "$b" ]; then echo "EDITED $rel"
    elif [ "$s" = "-" ] && [ -z "$b" ]; then echo "EDITED $rel"
    else echo "CONFLICT $rel"; fi
  done
}

report() {  # prints non-OK rows and a summary; returns 1 when anything differs
  local rows ok total
  rows="$(classify)"
  ok="$(grep -c '^OK ' <<<"$rows" || true)"; total="$(list_files "$SRC" | wc -l)"
  grep -v '^OK ' <<<"$rows" | awk '{printf "%-9s %s\n", $1, $2}' || true
  if [ "$ok" -eq "$total" ] && ! grep -qv '^OK ' <<<"$rows"; then
    echo "OK: $ok/$total files match in $DST"; return 0
  fi
  echo "FAIL: $ok/$total files match in $DST" >&2; return 1
}

case "$MODE" in
--check)
  [ -d "$DST" ] || { echo "not installed: $DST" >&2; exit 1; }
  report; exit $? ;;

--dry-run)
  echo "would install $SRC -> $DST ($(list_files "$SRC" | wc -l) files)"
  [ -d "$DST" ] && { report || true; } || echo "target absent: fresh install"
  exit 0 ;;

--pull)
  [ -f "$BASE" ] || { echo "no $BASE: cannot tell edits from stale files; compare by hand" >&2; exit 3; }
  pulled=0; conflict=0
  while read -r state rel; do
    case "$state" in
      EDITED) mkdir -p "$(dirname "$SRC/$rel")"; cp -a "$DST/$rel" "$SRC/$rel"
              echo "pulled    $rel"; pulled=$((pulled + 1)) ;;
      CONFLICT) echo "CONFLICT  $rel (repo and install both changed)" >&2; conflict=1 ;;
    esac
  done < <(classify)
  echo "$pulled file(s) copied into $SRC; review and commit them"
  exit $((conflict ? 3 : 0)) ;;

--remove-legacy)
  report >/dev/null || { echo "install $NAME and pass --check before removing the old copies" >&2; exit 1; }
  missing=0; files=0
  for s in "${LEGACY[@]}"; do
    [ -d "$ROOT/svg/$s" ] || continue
    while IFS= read -r f; do
      files=$((files + 1))
      git -C "$REPO" cat-file -e "$(git -C "$REPO" hash-object "$f")" 2>/dev/null \
        || { echo "NOT IN GIT  $f" >&2; missing=1; }
    done < <(find "$ROOT/svg/$s" -type f ! -name '*.pyc' ! -path '*/__pycache__/*')
  done
  [ "$missing" -eq 0 ] || { echo "nothing removed: import those files first" >&2; exit 4; }
  for s in "${LEGACY[@]}"; do [ -d "$ROOT/svg/$s" ] && rm -rf "${ROOT:?}/svg/$s"; done
  rmdir "$ROOT/svg" 2>/dev/null || true
  echo "removed $files legacy file(s); every one is a blob in git"
  exit 0 ;;
esac

# install
if [ -d "$DST" ]; then
  refused="$(classify | grep -E '^(EDITED|CONFLICT) ' || true)"
  if [ -n "$refused" ]; then
    echo "$refused" | awk '{printf "%-9s %s\n", $1, $2}' >&2
    echo "refused: the install was edited in place; run 'bash sync.sh --pull' and commit first" >&2
    exit 3
  fi
fi
mkdir -p "$ROOT"
NEW="$ROOT/.$NAME.new.$$"; OLD="$ROOT/.$NAME.old.$$"
trap 'rm -rf "$NEW" "$OLD"' EXIT
cp -a "$SRC" "$NEW"
find "$NEW" \( -name '__pycache__' -o -name '*.pyc' \) -prune -exec rm -rf {} +
(cd "$NEW" && list_files . | while IFS= read -r rel; do
   printf '%s  %s\n' "$(hash_of "$rel")" "$rel"; done) > "$NEW/.sync-baseline"
[ -d "$DST" ] && mv "$DST" "$OLD"
mv "$NEW" "$DST"
echo "installed $(list_files "$SRC" | wc -l) files into $DST"
report
