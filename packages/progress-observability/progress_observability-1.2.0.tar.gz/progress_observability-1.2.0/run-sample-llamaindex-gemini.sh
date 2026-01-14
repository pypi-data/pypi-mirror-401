#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/sample_apps"
uv run python test_llamaindex_gemini.py
