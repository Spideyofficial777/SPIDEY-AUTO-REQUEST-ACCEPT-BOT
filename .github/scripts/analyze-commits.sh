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

mapfile -t COMMIT_HASHES < <(git log "$RANGE" --no-merges --format="%H" \
                                --perl-regexp --author="^(?!.*(${BOT_AUTHORS_REGEX})).*$" 2>/dev/null || true)

COMMIT_COUNT=0
HAS_BREAKING=false
HAS_FEATURE=false
HAS_RELEASE_ELIGIBLE=false

for HASH in "${COMMIT_HASHES[@]:-}"; do
  [ -z "$HASH" ] && continue
  SUBJECT=$(git log -1 --format="%s" "$HASH")
  BODY=$(git log -1 --format="%b" "$HASH")
  SHORT=$(git rev-parse --short "$HASH")
  COMMIT_COUNT=$((COMMIT_COUNT + 1))

  LOWER_SUBJECT=$(echo "$SUBJECT" | tr '[:upper:]' '[:lower:]')

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
  ELIGIBLE=false

  LOCKED_NON_ELIGIBLE=false
  case "$TYPE" in
    chore|style|test|tests|ci|build) LOCKED_NON_ELIGIBLE=true ;;
  esac

  if [ "$LOCKED_NON_ELIGIBLE" = true ]; then
    echo "$ENTRY" >> "$NOTES_DIR/internal.md"

  elif [[ "$TYPE" == "deps" ]] || \
     echo "$LOWER_SUBJECT" | grep -Eq "\b(bump|upgrade|dependenc(y|ies)|requirements\.txt)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/deps.md"

  elif [[ "$TYPE" == "security" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(security|vulnerabilit(y|ies)|cve|exploit)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/fixes.md"
    ELIGIBLE=true

  elif [[ "$TYPE" == "feat" || "$TYPE" == "feature" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(add|new|introduce|implement)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/features.md"
    HAS_FEATURE=true
    ELIGIBLE=true

  elif [[ "$TYPE" == "fix" || "$TYPE" == "bugfix" || "$TYPE" == "hotfix" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(fix|bug|resolve|patch|crash|error)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/fixes.md"
    ELIGIBLE=true

  elif [[ "$TYPE" == "perf" || "$TYPE" == "performance" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(perf|performance|optimi[sz]e|speed up|faster)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/performance.md"
    ELIGIBLE=true

  elif [[ "$TYPE" == "docs" || "$TYPE" == "doc" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(readme|docs?|documentation)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/docs.md"

  elif [[ "$TYPE" == "refactor" || "$TYPE" == "improve" || "$TYPE" == "improvement" ]] || \
       echo "$LOWER_SUBJECT" | grep -Eq "\b(improve|enhance|refactor|clean ?up|rework|optimize)\b"; then
    echo "$ENTRY" >> "$NOTES_DIR/improvements.md"
    ELIGIBLE=true

  else
    echo "$ENTRY" >> "$NOTES_DIR/internal.md"
  fi

  [ "$ELIGIBLE" = true ] && HAS_RELEASE_ELIGIBLE=true

  if [ "$BREAKING" = true ]; then
    echo "- ${CLEAN_SUBJECT^} (${SHORT}) — breaking change" >> "$NOTES_DIR/highlights.md"
  fi
done

if [ -s "$NOTES_DIR/features.md" ]; then
  head -n 3 "$NOTES_DIR/features.md" >> "$NOTES_DIR/highlights.md"
fi

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

if [ -n "$PREV_TAG" ]; then
  git log "${PREV_TAG}..HEAD" --no-merges --format="%aN" \
    | grep -Ev "^(github-actions(\[bot\])?)$" | sort -u > "$NOTES_DIR/contributors.md" || true
else
  git log --no-merges --format="%aN" \
    | grep -Ev "^(github-actions(\[bot\])?)$" | sort -u > "$NOTES_DIR/contributors.md" || true
fi
sed -i 's/^/- /' "$NOTES_DIR/contributors.md" 2>/dev/null || true

if [ "$COMMIT_COUNT" -eq 0 ]; then
  BUMP="none"
elif [ "$HAS_BREAKING" = true ]; then
  BUMP="major"
elif [ "$HAS_FEATURE" = true ]; then
  BUMP="minor"
elif [ "$HAS_RELEASE_ELIGIBLE" = true ]; then
  BUMP="patch"
else
  BUMP="none"
fi

echo "bump=$BUMP" >> "$GITHUB_OUTPUT"
echo "commit_count=$COMMIT_COUNT" >> "$GITHUB_OUTPUT"
echo "release_eligible=$HAS_RELEASE_ELIGIBLE" >> "$GITHUB_OUTPUT"
echo "Analyzed $COMMIT_COUNT commit(s) since '${PREV_TAG:-<repo start>}' -> bump=$BUMP, release_eligible=$HAS_RELEASE_ELIGIBLE"
