@echo off
echo Starting DIH MAIL Web Server...
echo.
cd /d "%~dp0"

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Installing dependencies...
    .venv\Scripts\pip install -r requirements.txt
)

echo.
echo ============================================
echo DIH MAIL Server Starting...
echo ============================================
echo.
echo Access from any browser:
echo   Local:   http://127.0.0.1:5000
echo   Network: http://YOUR-IP:5000
echo.
echo Press Ctrl+C to stop server
echo.

.venv\Scripts\python.exe app.py
pause
