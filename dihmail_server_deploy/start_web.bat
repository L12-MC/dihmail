@echo off
echo Starting dihmail web application...
echo.
cd /d "%~dp0"
.venv\Scripts\python.exe app.py
pause
