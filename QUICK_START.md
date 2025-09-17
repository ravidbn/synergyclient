# Quick Start Guide - Fix "externally-managed-environment" Error

## Current Situation

You're seeing the "externally-managed-environment" error when trying to build your APK. This happens in WSL (Windows Subsystem for Linux) with newer Ubuntu versions that protect the system Python.

## From Windows (Current Terminal)

Since you're currently in Windows PowerShell/Command Prompt, you need to use WSL to build the APK:

### Option 1: Use the Windows Batch Script (Recommended)
```cmd
build_apk.bat
```
This script will guide you through the process and automatically use WSL.

### Option 2: Manual WSL Commands (Fastest)
```cmd
REM Enter WSL
wsl

REM In WSL terminal, run:
chmod +x fix_simple.sh
./fix_simple.sh
source buildenv/bin/activate
buildozer android debug
```

**Note**: If you get package errors, try the full setup script instead:
```bash
chmod +x fix_build_environment.sh build_android_venv.sh
./fix_build_environment.sh
./build_android_venv.sh
```

## From WSL/Linux Terminal

If you're already in WSL or a Linux terminal:

### Simple Solution (Fixes the core error only)
```bash
chmod +x fix_simple.sh
./fix_simple.sh
source buildenv/bin/activate
buildozer android debug
```

### Full Solution (Includes all system dependencies)
```bash
chmod +x fix_build_environment.sh build_android_venv.sh
./fix_build_environment.sh
./build_android_venv.sh
```

### Alternative Solutions (if virtual environment fails)
```bash
# Test your environment first
./test_environment.sh

# Or try pipx approach (more reliable than Docker)
./build_with_pipx.sh

# Docker (only if others fail - can have timezone issues)
./build_with_docker.sh
```

## What Each Script Does

- **`fix_build_environment.sh`** - Creates isolated Python environment (fixes the externally-managed error)
- **`build_android_venv.sh`** - Builds APK using the isolated environment
- **`build_with_pipx.sh`** - Alternative using pipx for tool isolation
- **`build_with_docker.sh`** - Uses Docker containers (fixed for compatibility issues)
- **`fix_distutils.sh`** - Fixes "No module named 'distutils'" error (Python 3.12+)
- **`test_environment.sh`** - Checks what's available on your system

## Expected Results

After successful build, you'll see:
```
=== APK Files Found ===
bin/synergyclient-0.1-arm64-v8a-debug.apk
```

Install with:
```bash
adb install bin/*.apk
```

## If You're Still Getting Errors

1. **Make sure you're in WSL**: The error only occurs in Linux environments
2. **Check WSL version**: `wsl --version` (WSL2 recommended)
3. **Try virtual environment first**: Most reliable solution
4. **Check the detailed guide**: See `WSL_BUILD_SOLUTIONS.md`

## Quick Fixes

### For the core error only (fastest):
```bash
chmod +x fix_simple.sh && ./fix_simple.sh && source buildenv/bin/activate && buildozer android debug
```

### For automatic detection and full setup:
```bash
chmod +x build_apk.sh && ./build_apk.sh
```

### If you get "No module named 'distutils'" error:
```bash
chmod +x fix_distutils.sh && ./fix_distutils.sh
```

### If you get libtinfo5 package errors:
Use the simple fix above, then install dependencies manually:
```bash
sudo apt install -y git zip unzip openjdk-8-jdk cmake build-essential python3-dev python3-setuptools
```