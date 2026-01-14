#!/bin/bash

set -e  # Exit on any error

echo "🔨 Building Progress Observability Python SDK..."
uv build

echo "📦 Copying wheel to sample_apps..."
cp dist/progress_observability-*.whl sample_apps/

# 🔁 Update sample_apps/pyproject.toml to point to the latest wheel
bash ./update_sample_apps_wheel.sh

echo "📥 Installing dependencies in sample_apps..."
cd sample_apps
uv sync

echo "✅ Done!"
