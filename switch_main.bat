@echo off
echo === Synergy Client Main File Switcher ===

REM Function to show current main file
if exist main.py (
    findstr /C:"Real Android Services" main.py >nul
    if %errorlevel%==0 (
        echo Current: Real Services Version
    ) else (
        findstr /C:"Minimal Version" main.py >nul
        if %errorlevel%==0 (
            echo Current: Minimal Version
        ) else (
            echo Current: Standard Version
        )
    )
) else (
    echo Current: No main.py found
)

echo.
echo Available versions:
echo 1. Real Services (use real Android APIs when possible)
echo 2. Standard Version (current main.py)
echo 3. Minimal Version (basic testing)
echo 4. Show current file details
echo.
set /p choice="Choose version (1-4): "

if "%choice%"=="1" (
    if exist main_real_services.py (
        echo Switching to Real Services version...
        if exist main.py copy main.py main_backup.py >nul 2>&1
        copy main_real_services.py main.py >nul
        echo ✅ Switched to Real Services version
        echo 📦 Rebuild APK: 
        echo    wsl
        echo    source buildenv/bin/activate
        echo    buildozer android debug
    ) else (
        echo ❌ main_real_services.py not found
    )
    goto end
)

if "%choice%"=="2" (
    if exist main_backup.py (
        echo Restoring Standard version...
        copy main_backup.py main.py >nul
        echo ✅ Restored Standard version
    ) else (
        echo ℹ️  main.py is already the standard version
    )
    goto end
)

if "%choice%"=="3" (
    if exist main_minimal.py (
        echo Switching to Minimal version...
        if exist main.py copy main.py main_backup.py >nul 2>&1
        copy main_minimal.py main.py >nul
        echo ✅ Switched to Minimal version
    ) else (
        echo ❌ main_minimal.py not found
    )
    goto end
)

if "%choice%"=="4" (
    echo.
    echo === Current main.py Details ===
    if exist main.py (
        for /f %%A in ('find /c /v "" ^< main.py') do echo File size: %%A lines
        echo.
        echo Key features detected:
        findstr /C:"Real Android Services" main.py >nul && echo ✅ Real Services support
        findstr /C:"mock" main.py >nul && echo ✅ Mock service fallback
        findstr /C:"ANDROID_AVAILABLE" main.py >nul && echo ✅ Android API detection
        findstr /C:"dp(" main.py >nul && echo ✅ Fixed UI layout
        findstr /C:"prevent_backgrounding" main.py >nul && echo ✅ Background prevention
        echo.
        echo First few lines:
        more +1 main.py | head -10
    ) else (
        echo ❌ main.py not found
    )
    goto end
)

echo Invalid choice
goto end

:end
echo.
REM Show current again
if exist main.py (
    findstr /C:"Real Android Services" main.py >nul
    if %errorlevel%==0 (
        echo Current: Real Services Version
    ) else (
        findstr /C:"Minimal Version" main.py >nul
        if %errorlevel%==0 (
            echo Current: Minimal Version
        ) else (
            echo Current: Standard Version
        )
    )
) else (
    echo Current: No main.py found
)
echo.
echo Note: After switching, rebuild the APK in WSL to see changes on device
pause