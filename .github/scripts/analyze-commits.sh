#!/usr/bin/env bash
set -euo pipefail

PREV_TAG="${PREV_TAG:-}"
NOTES_DIR="${NOTES_DIR:-/tmp/release-notes}"
BOT_AUTHORS_REGEX="github-actions\[bot\]|github-actions"

rm -rf "$NOTES_DIR"
mkdir -p "$NOTES_DIR"

for f in highlights features improvements fixes performance docs internal deps files contributors; do
  : > "$NOTES_DIR/$f.md"
done

if [ -n "$PREV_TAG" ]; then
  RANGE="${PREV_TAG}..HEAD"
else
  RANGE="HEAD"
fi

# Commit list: hash | subject  (body is not needed for classification level
# we use here; BREAKING CHANGE footers are still detected via git log %B below)
mapfile -t COMMIT_HASHES < <(git log "$RANGE" --no-merges --format="%H" \
                                --perl-regexp --author="^(?!.*(${BOT_AUTHORS_REGEX})).*$" 2>/dev/null || true)

COMMIT_COUNT=0
HAS_BREAKING=false
HAS_FEATURE=false

for HASH in "${COMMIT_HASHES[@]:-}"; do
  [ -z "$HASH" ] && continue
  SUBJECT=$(git log -1 --format="%s" "$HASH")
  BODY=$(git log -1 --format="%b" "$HASH")
  SHORT=$(git rev-parse --short "$HASH")
  COMMIT_COUNT=$((COMMIT_COUNT + 1))

  LOWER_SUBJECT=$(echo "$SUBJECT" | tr '[:upper:]' '[:lower:]')

  # --- Conventional Commit prefix, e.g. "feat(auth)!: add SSO" -------------
  # (regex kept in a variable, not inlined, because bash's [[ =~ ]] parser
  # gets confused by literal parentheses typed directly inside the test)
  TYPE=""
  BREAKING=false
  CC_REGEX='^([a-zA-Z]+)(\([^)]*\))?(!)?:[[:space:]]*(.*)$'
  if [[ "$SUBJECT" =~ $CC_REGEX ]]; then
    TYPE=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
    [ -n "${BASH_REMATCH[3]}" ] && BREAKING=true
    CLEAN_SUBJECT="${BASH_REMATCH[4]}"
  else
    CLEAN_SUBJECT="$SUBJECT"
  fi

  if echo "$BODY" | grep -qi "BREAKING CHANGE"; then
    BREAKING=true
  fi
  [ "$BREAKING" = true ] && HAS_BREAKING=true

  ENTRY="- ${CLEAN_SUBJECT^} (${SHORT})"

  # --- Dependency updates checked first (can appear under any type) --------
  if [[ "$TYPE" == "deps" ]] || \
     echo "$LOWER_SUBJECT" | grep -Eq "\b(bump|upgrade|dependenc(y|ies)|requirements\.txt)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/deps.md"

  elif [[ "$TYPE" == "feat" || "$TYPE" == "feature" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(add|new|introduce|implement)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/features.md"
    HAS_FEATURE=true

  elif [[ "$TYPE" == "fix" || "$TYPE" == "bugfix" || "$TYPE" == "hotfix" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(fix|bug|resolve|patch|crash|error)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/fixes.md"

  elif [[ "$TYPE" == "perf" || "$TYPE" == "performance" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(perf|performance|optimi[sz]e|speed up|faster)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/performance.md"

  elif [[ "$TYPE" == "docs" || "$TYPE" == "doc" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(readme|docs?|documentation)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/docs.md"

  elif [[ "$TYPE" == "refactor" || "$TYPE" == "improve" || "$TYPE" == "improvement" || "$TYPE" == "style" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(improve|enhance|refactor|clean ?up|rework|optimize)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/improvements.md"

  else
    # chore, ci, test, build (non-dependency), or anything unclassified
    echo "$ENTRY" >> "$NOTES_DIR/internal.md"
  fi

  if [ "$BREAKING" = true ]; then
    echo "- ${CLEAN_SUBJECT^} (${SHORT}) — breaking change" >> "$NOTES_DIR/highlights.md"
  fi
done

# --- Highlights: breaking changes first, then top 3 new features -----------
if [ -s "$NOTES_DIR/features.md" ]; then
  head -n 3 "$NOTES_DIR/features.md" >> "$NOTES_DIR/highlights.md"
fi

# --- Files touched (capped so the notes stay readable) ----------------------
if [ -n "$PREV_TAG" ]; then
  FILES_CHANGED=$(git diff --name-only "${PREV_TAG}..HEAD" -- . ':(exclude)CHANGELOG.md' ':(exclude)README.md' 2>/dev/null || true)
else
  FILES_CHANGED=$(git ls-files)
fi
FILE_COUNT=$(echo "$FILES_CHANGED" | grep -c . || true)
if [ "$FILE_COUNT" -gt 0 ]; then
  echo "$FILES_CHANGED" | head -n 20 | sed 's/^/- `/;s/$/`/' >> "$NOTES_DIR/files.md"
  if [ "$FILE_COUNT" -gt 20 ]; then
    echo "- …and $((FILE_COUNT - 20)) more file(s)" >> "$NOTES_DIR/files.md"
  fi
fi

# --- Contributors -------------------------------------------------------
if [ -n "$PREV_TAG" ]; then
  git log "${PREV_TAG}..HEAD" --no-merges --format="%aN" \
    | grep -Ev "^(github-actions(\[bot\])?)$" | sort -u > "$NOTES_DIR/contributors.md" || true
else
  git log --no-merges --format="%aN" \
    | grep -Ev "^(github-actions(\[bot\])?)$" | sort -u > "$NOTES_DIR/contributors.md" || true
fi
sed -i 's/^/- /' "$NOTES_DIR/contributors.md" 2>/dev/null || true

# --- Determine bump ----------------------------------------------------
if [ "$COMMIT_COUNT" -eq 0 ]; then
  BUMP="none"
elif [ "$HAS_BREAKING" = true ]; then
  BUMP="major"
elif [ "$HAS_FEATURE" = true ]; then
  BUMP="minor"
else
  BUMP="patch"
fi

echo "bump=$BUMP" >> "$GITHUB_OUTPUT"
echo "commit_count=$COMMIT_COUNT" >> "$GITHUB_OUTPUT"
echo "Analyzed $COMMIT_COUNT commit(s) since '${PREV_TAG:-<repo start>}' -> bump=$BUMP"
