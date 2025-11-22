@echo off
pushd "%~dp0\.." >nul
echo Creating Server Deployment Package...
echo.
set DEPLOY_FOLDER=dihmail_server_deploy
echo [1/4] Creating deployment folder...
if exist %DEPLOY_FOLDER% rmdir /s /q %DEPLOY_FOLDER%
mkdir %DEPLOY_FOLDER%
echo [2/4] Copying Python source files...
copy *.py %DEPLOY_FOLDER%\ >nul
copy requirements.txt %DEPLOY_FOLDER%\ >nul
copy start_web.bat %DEPLOY_FOLDER%\ >nul
copy DEPLOYMENT.md %DEPLOY_FOLDER%\ >nul
copy README.md %DEPLOY_FOLDER%\ >nul
echo [3/4] Copying templates and static files...
xcopy /E /I /Y templates %DEPLOY_FOLDER%\templates >nul
xcopy /E /I /Y static %DEPLOY_FOLDER%\static >nul
echo [4/4] Creating startup script...
(
echo @echo off
echo echo Starting DIH MAIL Web Server...
echo echo.
echo cd /d "%%~dp0"
echo if not exist ".venv" ^(
echo    echo Creating virtual environment...
echo    python -m venv .venv
echo    echo Installing dependencies...
echo    .venv\Scripts\pip install -r requirements.txt
echo ^)
echo echo ============================================
echo echo DIH MAIL Server Starting...
echo echo ============================================
echo echo Access from any browser:
echo echo   Local:   http://127.0.0.1:5000
echo echo.
echo .venv\Scripts\python.exe app.py
echo pause
) > %DEPLOY_FOLDER%\start_server.bat
echo.
echo ============================================
echo Server Package Complete!
echo Location: %DEPLOY_FOLDER%\
echo ============================================
popd >nul
exit /b 0