# WSL Build Solutions for "externally-managed-environment" Error

## Problem Description

The "externally-managed-environment" error occurs in WSL (Windows Subsystem for Linux) with newer Ubuntu versions (22.04+) that implement PEP 668. This prevents installing Python packages directly to the system Python environment.

## Root Cause

- **PEP 668 Implementation**: Ubuntu 22.04+ marks the system Python as "externally managed"
- **Package Protection**: Prevents accidental system Python corruption
- **WSL Specific**: More common in WSL environments with updated Ubuntu distributions

## Solution 1: Virtual Environment (Recommended)

**Best for**: Local development, full control over environment

### Steps:
1. **Setup Environment**:
   ```bash
   chmod +x fix_build_environment.sh
   ./fix_build_environment.sh
   ```

2. **Build APK**:
   ```bash
   chmod +x build_android_venv.sh
   ./build_android_venv.sh
   ```

### Benefits:
- ✅ Follows Python best practices
- ✅ Isolated from system Python
- ✅ Full control over dependencies
- ✅ Reusable environment

## Solution 2: Docker (Most Reliable)

**Best for**: WSL users, avoiding dependency conflicts

### Steps:
1. **Run Docker Build**:
   ```bash
   chmod +x build_with_docker.sh
   ./build_with_docker.sh
   ```

### Benefits:
- ✅ Pre-configured environment
- ✅ No local dependency installation
- ✅ Consistent builds
- ✅ Official Kivy support

## Solution 3: pipx (Alternative)

**Best for**: Users who prefer isolated tool installation

### Steps:
1. **Build with pipx**:
   ```bash
   chmod +x build_with_pipx.sh
   ./build_with_pipx.sh
   ```

### Benefits:
- ✅ Isolated tool installation
- ✅ No virtual environment management
- ✅ System-wide tool availability

## Quick Fix Commands

If you want to try the fastest solution first:

### Option A: Docker (Fastest)
```bash
# Install Docker if needed
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker $USER
# Log out and back in, then:
./build_with_docker.sh
```

### Option B: Virtual Environment
```bash
./fix_build_environment.sh
source buildenv/bin/activate
./build_android_venv.sh
```

## Legacy System Override (Not Recommended)

If you absolutely need to override the protection (not recommended):

```bash
# WARNING: This can break your system Python
sudo rm /usr/lib/python*/EXTERNALLY-MANAGED
pip install buildozer
```

**⚠️ WARNING**: This approach is dangerous and can corrupt your system Python installation.

## Troubleshooting

### Docker Issues
```bash
# If Docker permission denied:
sudo usermod -aG docker $USER
# Log out and log back in

# If Docker daemon not running:
sudo service docker start
```

### Virtual Environment Issues
```bash
# If venv creation fails:
sudo apt install python3-venv

# If buildozer not found after installation:
source buildenv/bin/activate
which buildozer
```

### WSL-Specific Issues
```bash
# If Java not found:
sudo apt install openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# If Android SDK download fails:
# Check internet connectivity in WSL
ping google.com
```

## Expected Build Time

- **First Build**: 20-60 minutes (downloads SDK, NDK, dependencies)
- **Subsequent Builds**: 2-5 minutes
- **Docker Build**: 10-30 minutes (downloads image first time)

## Success Indicators

After successful build, you should see:
```
=== APK Files Found ===
bin/synergyclient-0.1-arm64-v8a-debug.apk
```

## Installation

Install the APK on your Android device:
```bash
# Enable USB debugging on Android device
adb devices
adb install bin/synergyclient-0.1-arm64-v8a-debug.apk
```

## Recommended Approach

1. **Try Docker first** (most reliable for WSL)
2. **Fall back to Virtual Environment** if Docker issues
3. **Use pipx** as last resort
4. **Never use system override** unless absolutely necessary

## Getting Help

If all solutions fail:
1. Check WSL version: `wsl --version`
2. Check Ubuntu version: `lsb_release -a`
3. Check Python version: `python3 --version`
4. Share error logs from the failed build attempt