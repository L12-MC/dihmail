#!/usr/bin/env bash
set -euo pipefail
cd ..  # ensure project root

echo "Starting dihmail web application (Linux)..."

if [ ! -d .venv ]; then
  echo "Virtual env not found; creating..."
  python3 -m venv .venv
fi
source .venv/bin/activate

python app.py