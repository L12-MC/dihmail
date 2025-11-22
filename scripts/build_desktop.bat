@echo off
pushd "%~dp0\.." >nul
echo Building DihMail Desktop Application...
echo.
if not exist .venv (
  echo Virtual env not found; creating...
  python -m venv .venv || goto fail
)
call .venv\Scripts\activate.bat || goto fail
echo [1/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo [2/3] Building executable with PyInstaller...
pyinstaller build_exe.spec || goto fail
echo [3/3] Copying required files to dist folder...
if not exist "dist\DihMail\static" mkdir "dist\DihMail\static"
copy "static\dihmail.png" "dist\DihMail\static\" >nul
copy "DEPLOYMENT.md" "dist\DihMail\" >nul
copy "README.md" "dist\DihMail\" >nul
echo.
echo ============================================
echo Build Complete!
echo Executable location: dist\DihMail\DihMail.exe
echo To test: cd dist\DihMail ^&^& DihMail.exe
echo ============================================
popd >nul
exit /b 0
:fail
echo Build failed (errorlevel %errorlevel%).
popd >nul
exit /b 1