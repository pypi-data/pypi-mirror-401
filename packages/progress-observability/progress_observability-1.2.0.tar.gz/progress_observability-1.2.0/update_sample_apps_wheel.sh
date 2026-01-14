#!/bin/bash

set -e

# This script should be run from the Progress.Observability.Instrumentation root
SAMPLE_APPS_DIR="sample_apps"
PYPROJECT_FILE="$SAMPLE_APPS_DIR/pyproject.toml"

if [ ! -f "$PYPROJECT_FILE" ]; then
  echo "❌ $PYPROJECT_FILE not found. Run this script from Progress.Observability.Instrumentation root."
  exit 1
fi

# Find the latest built wheel in sample_apps (copied there by run-sample.sh)
shopt -s nullglob
wheel_candidates=("$SAMPLE_APPS_DIR"/progress_observability-*-py3-none-any.whl)
shopt -u nullglob
if [ ${#wheel_candidates[@]} -eq 0 ]; then
  echo "❌ No progress_observability wheel found in $SAMPLE_APPS_DIR."
  exit 1
fi
LATEST_WHEEL="${wheel_candidates[0]}"
for wheel in "${wheel_candidates[@]}"; do
  if [ "$wheel" -nt "$LATEST_WHEEL" ]; then
    LATEST_WHEEL="$wheel"
  fi
done

WHEEL_BASENAME=$(basename "$LATEST_WHEEL")

echo "🔧 Updating $PYPROJECT_FILE to use $WHEEL_BASENAME..."

# Replace the hardcoded placeholder progress_observability-0.0.0-py3-none-any.whl with the actual wheel name
sed -i.bak -E "s|progress-observability = \{ path = \"progress_observability-0.0.0-py3-none-any.whl\" \}|progress-observability = { path = \"$WHEEL_BASENAME\" }|" "$PYPROJECT_FILE"

rm -f "$PYPROJECT_FILE.bak"

echo "✅ Updated $PYPROJECT_FILE to use $WHEEL_BASENAME"
