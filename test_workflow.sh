#!/bin/bash

echo "=== GitHub Workflow Test Script ==="
echo "This script simulates the GitHub Actions workflow locally"
echo ""

# Check if running on Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "❌ This script requires Ubuntu/Debian (apt-get)"
    echo "For other systems, manually install the dependencies listed in WORKFLOW_FIXES.md"
    exit 1
fi

echo "🔍 Checking system dependencies..."

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
sudo apt-get install -y build-essential m4 gettext

# Try to install libtinfo5, fallback to libtinfo6 if not available
sudo apt-get install -y libtinfo5 || sudo apt-get install -y libtinfo6

# Enable 32-bit architecture and install 32-bit packages (optional for modern builds)
echo "🔧 Enabling 32-bit architecture support..."
sudo dpkg --add-architecture i386 || true
sudo apt-get update || true
sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386 || echo "⚠️  Warning: Some 32-bit packages not available, continuing without them"

echo "☕ Setting up Java environment..."
# Install both Java 8 and 17
sudo apt-get install -y openjdk-17-jdk

echo "Using Java 17 for Android SDK setup..."
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
echo "Java 17 version:"
java -version

echo "🐍 Setting up Python environment..."
python3 -m pip install --upgrade pip
pip install buildozer cython==0.29.33

echo "📋 Installing Python requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Requirements installed successfully"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

echo "🧹 Cleaning previous builds..."
rm -rf .buildozer
rm -rf bin
if [ -f ".gitmodules" ]; then
    echo "🗑️ Removing problematic .gitmodules"
    rm -f .gitmodules
fi

echo "🔧 Creating Android SDK licenses..."
if [ -z "$ANDROID_HOME" ]; then
    export ANDROID_HOME=$HOME/.buildozer/android/platform/android-sdk
fi

mkdir -p "$ANDROID_HOME/licenses"
echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > "$ANDROID_HOME/licenses/android-sdk-license"
echo "d56f5187479451eabf01fb78af6dfcb131a6481e" > "$ANDROID_HOME/licenses/android-sdk-preview-license"
echo "84831b9409646a918e30573bab4c9c91346d8abd" > "$ANDROID_HOME/licenses/android-sdk-preview-license-old"

echo "🔄 Switching to Java 8 for buildozer..."
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
echo "Java 8 version for buildozer:"
java -version

echo "� Starting Android build..."
echo "This may take 20-40 minutes for the first build..."

export ANDROID_SDK_ROOT=$ANDROID_HOME
buildozer android debug --verbose

# Check build result
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 BUILD SUCCESSFUL!"
    echo ""
    if [ -d "bin" ]; then
        echo "📱 APK Files:"
        ls -la bin/*.apk 2>/dev/null || echo "No APK files found in bin/"
    fi
    echo ""
    echo "✅ The GitHub workflow should now work correctly"
else
    echo ""
    echo "❌ BUILD FAILED"
    echo ""
    echo "Check the error messages above for troubleshooting"
    echo "Refer to BUILD_TROUBLESHOOTING.md for additional help"
    exit 1
fi

echo ""
echo "=== Test Complete ==="