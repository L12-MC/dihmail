#!/usr/bin/env bash
set -euo pipefail
cd ..  # ensure project root

echo "Building DihMail Desktop Application (Linux)..."

if [ ! -d .venv ]; then
  echo "Virtual env not found; creating..."
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "[1/3] Cleaning old build files..."
rm -rf build dist || true

echo "[2/3] Building executable with PyInstaller..."
pyinstaller build_exe.spec

echo "[3/3] Copying required files to dist folder..."
mkdir -p dist/DihMail/static
cp static/dihmail.png dist/DihMail/static/ 2>/dev/null || true
cp DEPLOYMENT.md dist/DihMail/ 2>/dev/null || true
cp README.md dist/DihMail/ 2>/dev/null || true

cat <<EOF

============================================
Build Complete!
Executable location: dist/DihMail/DihMail
To test: cd dist/DihMail && ./DihMail
============================================
EOF