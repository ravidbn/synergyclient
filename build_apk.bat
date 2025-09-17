@echo off
echo === APK Build Script for Windows (WSL Required) ===
echo.

echo This script will help you build the APK using WSL.
echo.

REM Check if WSL is available
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL is not installed or not available.
    echo Please install WSL2 with Ubuntu:
    echo   wsl --install Ubuntu
    echo.
    echo After installation, restart and run this script again.
    pause
    exit /b 1
)

echo WSL detected. Checking WSL environment...
echo.

REM Check if we're in the right directory in WSL
wsl ls -la main.py >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: main.py not found in current directory within WSL.
    echo Please ensure you're in the correct project directory.
    echo.
    echo Current directory contents in WSL:
    wsl ls -la
    pause
    exit /b 1
)

echo Project files found in WSL environment.
echo.

echo Choose your build method:
echo 1. Simple Fix (Recommended - just fixes the error)
echo 2. Full Virtual Environment (includes all dependencies)
echo 3. pipx method
echo 4. Docker method
echo 5. Test environment first
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo === Simple Fix - Just fixes externally-managed-environment error ===
    echo This creates a virtual environment without installing system packages
    echo Running simple fix script in WSL...
    wsl chmod +x fix_simple.sh
    wsl ./fix_simple.sh
    if %errorlevel% neq 0 (
        echo Simple fix failed. Trying full setup instead...
        wsl chmod +x fix_build_environment.sh build_android_venv.sh
        wsl ./fix_build_environment.sh
        wsl ./build_android_venv.sh
    ) else (
        echo.
        echo Running buildozer in WSL...
        wsl bash -c "source buildenv/bin/activate && buildozer android debug"
    )
) else if "%choice%"=="2" (
    echo.
    echo === Building with Full Virtual Environment ===
    echo Running setup script in WSL...
    wsl chmod +x fix_build_environment.sh build_android_venv.sh
    wsl ./fix_build_environment.sh
    if %errorlevel% neq 0 (
        echo Setup failed. Check error messages above.
        pause
        exit /b 1
    )
    echo.
    echo Running build script in WSL...
    wsl ./build_android_venv.sh
) else if "%choice%"=="3" (
    echo.
    echo === Building with pipx ===
    wsl chmod +x build_with_pipx.sh
    wsl ./build_with_pipx.sh
) else if "%choice%"=="4" (
    echo.
    echo === Building with Docker ===
    wsl chmod +x build_with_docker.sh
    wsl ./build_with_docker.sh
) else if "%choice%"=="5" (
    echo.
    echo === Testing Environment ===
    wsl chmod +x test_environment.sh
    wsl ./test_environment.sh
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo === Build Process Complete ===
echo.

REM Check for APK files
wsl find . -name "*.apk" -type f 2>nul
if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! APK file(s) found:
    wsl find . -name "*.apk" -type f
    echo.
    echo To install on your Android device:
    echo   adb install bin/*.apk
) else (
    echo.
    echo No APK files found. Check the build output above for errors.
)

echo.
pause