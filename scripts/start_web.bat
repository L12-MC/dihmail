@echo off
pushd "%~dp0\.." >nul
echo Starting dihmail web application...
echo.
if not exist .venv (
  echo Virtual env not found; creating...
  python -m venv .venv || goto fail
)
call .venv\Scripts\activate.bat || goto fail
python app.py
popd >nul
exit /b 0
:fail
echo Failed to start web app.
popd >nul
exit /b 1