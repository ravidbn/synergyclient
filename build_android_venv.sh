#!/bin/bash

echo "=== Android Build with Virtual Environment ==="

# Check if virtual environment exists
if [ ! -d "buildenv" ]; then
    echo "Virtual environment not found. Run fix_build_environment.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source buildenv/bin/activate

# Verify buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "Installing buildozer in virtual environment..."
    pip install buildozer cython==0.29.33
fi

# Set environment variables to prevent interactive prompts
export BUILDOZER_WARN_ON_ROOT=1
export ANDROID_SDK_ROOT=$HOME/.buildozer/android/platform/android-sdk
export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Create android home directory
mkdir -p $ANDROID_HOME

# Accept all SDK licenses by creating the license files
mkdir -p "$ANDROID_HOME/licenses"
echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$ANDROID_HOME/licenses/android-sdk-license"
echo "d56f5187479451eabf01fb78af6dfcb131a6481e" > "$ANDROID_HOME/licenses/android-sdk-preview-license"
echo "84831b9409646a918e30573bab4c9c91346d8abd" > "$ANDROID_HOME/licenses/android-sdk-preview-license-old"

echo "=== SDK Licenses accepted ==="

# Run buildozer with verbose output
echo "=== Running buildozer build ==="
buildozer android debug --verbose

echo "=== Build completed ==="

# Check output
if [ -d "bin" ]; then
    echo "=== APK Files Found ==="
    ls -la bin/
    find bin/ -name "*.apk" -type f
else
    echo "=== No bin directory found ==="
    echo "=== Searching for APK files ==="
    find . -name "*.apk" -type f 2>/dev/null
fi

echo "=== Build process finished ==="
echo "To use this APK, install it with: adb install bin/*.apk"