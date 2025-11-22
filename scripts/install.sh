#!/usr/bin/env bash
set -euo pipefail
cd ..  # ensure project root

echo "=== dihmail install (Linux) ==="

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found in PATH" >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
else
  echo "Reusing existing .venv"
fi

source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip || echo "(pip upgrade failed, continuing)"

echo "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

echo "\n============================================"
echo "Installation Complete!"
echo "Activate later: source .venv/bin/activate"
echo "Run web app:   python app.py"
echo "============================================"