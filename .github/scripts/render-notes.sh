#!/usr/bin/env bash
set -euo pipefail

NOTES_DIR="${NOTES_DIR:-/tmp/release-notes}"
OUTPUT_FILE="${OUTPUT_FILE:?OUTPUT_FILE env var required}"
INTRO="${INTRO:-}"

: > "$OUTPUT_FILE"

[ -n "$INTRO" ] && printf "%s\n\n" "$INTRO" >> "$OUTPUT_FILE"

write_section () {
  local file="$1" heading="$2"
  if [ -s "$NOTES_DIR/$file" ]; then
    printf "## %s\n\n" "$heading" >> "$OUTPUT_FILE"
    cat "$NOTES_DIR/$file" >> "$OUTPUT_FILE"
    printf "\n" >> "$OUTPUT_FILE"
  fi
}

write_section "highlights.md"    "Highlights"
write_section "features.md"      "New Features"
write_section "improvements.md"  "Improvements"
write_section "fixes.md"         "Bug Fixes"
write_section "performance.md"   "Performance"
write_section "docs.md"          "Documentation"
write_section "internal.md"      "Internal Changes"
write_section "deps.md"          "Dependency Updates"
write_section "files.md"         "Files Updated"
write_section "contributors.md"  "Contributors"

# Trim trailing blank lines
sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$OUTPUT_FILE" 2>/dev/null || true
