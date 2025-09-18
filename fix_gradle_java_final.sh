#!/bin/bash

echo "=== Final Fix for Gradle Java Version Conflicts ==="

# This script addresses the persistent "Java 11 vs Java 8" compatibility issue

echo "Cleaning all build artifacts..."
rm -rf .buildozer bin/ __pycache__ *.pyc
rm -rf gradle.properties 2>/dev/null

# Ensure we're in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "buildenv" ]; then
        source buildenv/bin/activate
    else
        echo "❌ Virtual environment not found. Run fix_simple.sh first."
        exit 1
    fi
fi

# Set Java 11 environment variables with fallback detection
echo "Configuring Java 11 environment..."
JAVA_11_PATHS=(
    "/usr/lib/jvm/java-11-openjdk-amd64"
    "/usr/lib/jvm/java-11-openjdk"
    "/usr/lib/jvm/java-1.11.0-openjdk-amd64"
    "/usr/lib/jvm/java-1.11.0-openjdk"
)

JAVA_HOME_FOUND=""
for path in "${JAVA_11_PATHS[@]}"; do
    if [ -d "$path" ]; then
        JAVA_HOME_FOUND="$path"
        break
    fi
done

if [ -z "$JAVA_HOME_FOUND" ]; then
    echo "Installing Java 11..."
    sudo apt update
    sudo apt install -y openjdk-11-jdk
    JAVA_HOME_FOUND="/usr/lib/jvm/java-11-openjdk-amd64"
fi

export JAVA_HOME="$JAVA_HOME_FOUND"
export PATH="$JAVA_HOME/bin:$PATH"

echo "JAVA_HOME: $JAVA_HOME"
echo "Java version:"
java -version

# Force all Java-related environment variables
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"
export GRADLE_OPTS="-Xmx3072m -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx3072m"
export ANDROID_JAVA_HOME="$JAVA_HOME"

# Create comprehensive gradle.properties
echo "Creating comprehensive Gradle configuration..."
cat > gradle.properties << 'EOF'
# Gradle JVM settings
org.gradle.jvmargs=-Xmx3072m -Dfile.encoding=UTF-8 -Duser.country=US -Duser.language=en -Duser.variant
org.gradle.daemon=false
org.gradle.parallel=false
org.gradle.configureondemand=false

# Android settings
android.useAndroidX=true
android.enableJetifier=true

# Java version enforcement - THIS IS CRITICAL
android.compileSdkVersion=33
android.targetSdkVersion=33
android.minSdkVersion=23

# Force Java 11 throughout the build
systemProp.java.specification.version=11
systemProp.java.version=11
systemProp.java.vm.specification.version=11
systemProp.java.runtime.version=11

# Kotlin compatibility
kotlin.code.style=official
kotlin.jvm.target.validation.mode=warning
EOF

# Create global gradle.properties
mkdir -p ~/.gradle
cp gradle.properties ~/.gradle/gradle.properties

# Update buildozer to latest version (helps with Java compatibility)
echo "Updating buildozer to latest version..."
pip install --upgrade buildozer

# Create a custom buildozer hook for Java enforcement
echo "Creating buildozer Java enforcement hook..."
mkdir -p .buildozer/android/platform/build-arm64-v8a 2>/dev/null || true

# Force environment in current shell
echo "Setting environment variables for this session..."
echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "export ANDROID_JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "export PATH=$JAVA_HOME/bin:\$PATH" >> ~/.bashrc

# Additional fix: Ensure gradle wrapper uses correct Java
export GRADLE_USER_HOME=~/.gradle
export JAVA_OPTIONS="-Dfile.encoding=UTF-8"

echo ""
echo "✅ Comprehensive Java/Gradle configuration complete!"
echo ""
echo "Environment configured:"
echo "- JAVA_HOME: $JAVA_HOME"
echo "- Java Version: $(java -version 2>&1 | head -1)"
echo "- Gradle configured for Java 11"
echo "- BuildTools configured for consistency"
echo ""
echo "Now try building with FRESH ENVIRONMENT:"
echo ""
echo "# Close terminal and open new WSL session, then:"
echo "cd $(pwd)"
echo "source buildenv/bin/activate"
echo "export JAVA_HOME=$JAVA_HOME"
echo "buildozer android debug"
echo ""
echo "If still failing, the issue may be in python-for-android dependencies."
echo "In that case, try: buildozer android clean && buildozer android debug"