@echo off
pushd "%~dp0\.." >nul
echo === dihmail install (Windows) ===
where python >nul 2>&1
if errorlevel 1 goto noPython

if not exist .venv goto createVenv
echo Reusing existing .venv
goto activate

:createVenv
echo Creating virtual environment (.venv)...
python -m venv .venv
if errorlevel 1 goto fail

:activate
call .venv\Scripts\activate.bat
if errorlevel 1 goto fail

echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 goto fail
pip install pyinstaller
if errorlevel 1 goto fail

echo.
echo ============================================
echo Installation Complete!
echo Activate later: call .venv\Scripts\activate.bat
echo Run web app:   python app.py
echo ============================================
popd >nul
exit /b 0

:noPython
echo ERROR: Python not found in PATH
goto fail

:fail
echo.
echo Installation FAILED (errorlevel %errorlevel%).
popd >nul
exit /b 1