#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/sample_apps"

echo "🚀 Running test_gemini_genAI.py..."
uv run python test_gemini_genAI.py
