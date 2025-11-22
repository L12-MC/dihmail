#!/usr/bin/env bash
set -euo pipefail
cd ..  # ensure project root

echo "Creating Server Deployment Package (Linux)..."
DEPLOY_FOLDER="dihmail_server_deploy"

echo "[1/4] Creating deployment folder..."
rm -rf "$DEPLOY_FOLDER" || true
mkdir -p "$DEPLOY_FOLDER"

echo "[2/4] Copying Python source files..."
cp *.py requirements.txt DEPLOYMENT.md README.md start_web.bat "$DEPLOY_FOLDER" 2>/dev/null || true

echo "[3/4] Copying templates and static files..."
mkdir -p "$DEPLOY_FOLDER/templates" "$DEPLOY_FOLDER/static"
cp -R templates "$DEPLOY_FOLDER/" 2>/dev/null || true
cp -R static "$DEPLOY_FOLDER/" 2>/dev/null || true

echo "[4/4] Creating startup script (start_server.sh)..."
cat > "$DEPLOY_FOLDER/start_server.sh" <<'EOS'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
  source .venv/bin/activate
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi
cat <<INFO

============================================
DIH MAIL Server Starting...
============================================
Access locally:   http://127.0.0.1:5000
Press Ctrl+C to stop server.
INFO
python app.py
EOS
chmod +x "$DEPLOY_FOLDER/start_server.sh"

echo "\n============================================"
echo "Server Package Complete!"
echo "Location: $DEPLOY_FOLDER/"
echo "To deploy: copy folder to server and run ./start_server.sh"
echo "============================================"