#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${CONFIG_FILE:-configs.py}"
NEW_VERSION="${NEW_VERSION:?NEW_VERSION env var required}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "::error::$CONFIG_FILE not found."
  exit 1
fi

if ! grep -qE '^VERSION[[:space:]]*=' "$CONFIG_FILE"; then
  echo "::error::No VERSION = \"X.Y.Z\" declaration found in $CONFIG_FILE — refusing to insert one."
  exit 1
fi

sed -E -i "s/^VERSION[[:space:]]*=[[:space:]]*['\"][0-9]+\.[0-9]+\.[0-9]+['\"]/VERSION = \"${NEW_VERSION}\"/" "$CONFIG_FILE"

WRITTEN=$(grep -E '^VERSION[[:space:]]*=' "$CONFIG_FILE" | head -n 1 \
  | sed -E "s/^VERSION[[:space:]]*=[[:space:]]*['\"]([0-9]+\.[0-9]+\.[0-9]+)['\"].*/\1/")

if [ "$WRITTEN" != "$NEW_VERSION" ]; then
  echo "::error::Verification failed — configs.py has '$WRITTEN', expected '$NEW_VERSION'."
  exit 1
fi

echo "Verified: configs.py VERSION = \"$NEW_VERSION\""
