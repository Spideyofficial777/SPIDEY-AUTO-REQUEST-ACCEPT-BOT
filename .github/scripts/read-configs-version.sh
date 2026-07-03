#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${CONFIG_FILE:-configs.py}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "::error::$CONFIG_FILE not found."
  exit 1
fi

CURRENT_VERSION=$(grep -E '^VERSION[[:space:]]*=' "$CONFIG_FILE" | head -n 1 \
  | sed -E "s/^VERSION[[:space:]]*=[[:space:]]*['\"]([0-9]+\.[0-9]+\.[0-9]+)['\"].*/\1/")

if [ -z "$CURRENT_VERSION" ]; then
  echo "::error::No VERSION = \"X.Y.Z\" declaration found in $CONFIG_FILE."
  exit 1
fi

echo "current_version=$CURRENT_VERSION" >> "$GITHUB_OUTPUT"
echo "Current version (from $CONFIG_FILE): $CURRENT_VERSION"
