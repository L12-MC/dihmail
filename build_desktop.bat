@echo off
echo Building DihMail Desktop Application...
echo.

cd /d "%~dp0"

echo [1/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] Building executable with PyInstaller...
.venv\Scripts\pyinstaller.exe build_exe.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo [3/3] Copying required files to dist folder...
if not exist "dist\DihMail\static" mkdir "dist\DihMail\static"
copy "static\dihmail.png" "dist\DihMail\static\" >nul
copy "DEPLOYMENT.md" "dist\DihMail\" >nul

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Executable location: dist\DihMail\DihMail.exe
echo.
echo To test: cd dist\DihMail ^&^& DihMail.exe
echo.

pause
