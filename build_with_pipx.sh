#!/bin/bash

echo "=== Android Build with pipx (Alternative Solution) ==="

# Install pipx if not already installed
if ! command -v pipx &> /dev/null; then
    echo "Installing pipx..."
    sudo apt update
    sudo apt install -y pipx
    pipx ensurepath
    # Reload shell environment
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install buildozer using pipx (isolated environment)
echo "Installing buildozer with pipx..."
pipx install buildozer

# Install cython with pipx
echo "Installing cython with pipx..."
pipx install cython==0.29.33

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update

# Detect Ubuntu version and install compatible packages
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "20.04")
echo "Detected Ubuntu version: $UBUNTU_VERSION"

if [ "$(echo "$UBUNTU_VERSION >= 22.04" | bc -l 2>/dev/null || echo 0)" -eq 1 ]; then
    echo "Installing packages for Ubuntu 22.04+..."
    sudo apt install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libncurses6 cmake libffi-dev libssl-dev build-essential
else
    echo "Installing packages for Ubuntu 20.04 and earlier..."
    sudo apt install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential
fi

# If libtinfo5 failed, try alternatives
if ! dpkg -l | grep -q libtinfo5 && ! dpkg -l | grep -q libncurses6; then
    echo "Trying alternative ncurses packages..."
    sudo apt install -y libncurses6 || sudo apt install -y libtinfo6 || echo "Warning: Some ncurses packages may be missing"
fi

# Set Java 11 as default (required for Android API 31+)
echo "Setting up Java environment..."
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# Verify Java installation
java -version
if [ $? -ne 0 ]; then
    echo "⚠️ Java installation issue detected. Trying to set JAVA_HOME automatically..."
    JAVA_HOME_AUTO=$(find /usr/lib/jvm -name "java-11-openjdk*" -type d | head -1)
    if [ -n "$JAVA_HOME_AUTO" ]; then
        export JAVA_HOME="$JAVA_HOME_AUTO"
        echo "export JAVA_HOME=\"$JAVA_HOME_AUTO\"" >> ~/.bashrc
        echo "✅ JAVA_HOME set to: $JAVA_HOME_AUTO"
    fi
fi

# Set environment variables
export BUILDOZER_WARN_ON_ROOT=1
export ANDROID_SDK_ROOT=$HOME/.buildozer/android/platform/android-sdk
export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk

# Create android home directory
mkdir -p $ANDROID_HOME

# Accept all SDK licenses
mkdir -p "$ANDROID_HOME/licenses"
echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$ANDROID_HOME/licenses/android-sdk-license"
echo "d56f5187479451eabf01fb78af6dfcb131a6481e" > "$ANDROID_HOME/licenses/android-sdk-preview-license"
echo "84831b9409646a918e30573bab4c9c91346d8abd" > "$ANDROID_HOME/licenses/android-sdk-preview-license-old"

echo "=== SDK Licenses accepted ==="

# Clean previous builds
if [ -d ".buildozer" ]; then
    echo "Cleaning previous build..."
    rm -rf .buildozer
fi

# Run buildozer
echo "=== Running buildozer build with pipx ==="
~/.local/bin/buildozer android debug --verbose

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