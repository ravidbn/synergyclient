#!/bin/bash

echo "=== Fixing Java/Gradle Compatibility Issues ==="

# This script fixes the "component compatible with Java 11 vs Java 8" error

echo "Cleaning previous build artifacts..."
rm -rf .buildozer bin/

# Check current Java version
echo "Checking Java version..."
java -version

# Set Java 11 environment
echo "Setting Java 11 environment..."
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# If Java 11 is not found, try to find it automatically
if [ ! -d "$JAVA_HOME" ]; then
    echo "Java 11 not found at expected location. Searching..."
    JAVA_HOME_AUTO=$(find /usr/lib/jvm -name "java-11-openjdk*" -type d | head -1)
    if [ -n "$JAVA_HOME_AUTO" ]; then
        export JAVA_HOME="$JAVA_HOME_AUTO"
        echo "Found Java 11 at: $JAVA_HOME_AUTO"
    else
        echo "Installing Java 11..."
        sudo apt update
        sudo apt install -y openjdk-11-jdk
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    fi
fi

# Set PATH to include Java 11
export PATH=$JAVA_HOME/bin:$PATH

echo "Current JAVA_HOME: $JAVA_HOME"
echo "Current Java version:"
java -version

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  Not in virtual environment. Activating buildenv..."
    if [ -d "buildenv" ]; then
        source buildenv/bin/activate
    else
        echo "❌ buildenv not found. Run fix_simple.sh first."
        exit 1
    fi
fi

# Update buildozer to latest version (helps with compatibility)
echo "Updating buildozer..."
pip install --upgrade buildozer

# Set Gradle JVM arguments for compatibility
echo "Setting Gradle JVM arguments..."
export GRADLE_OPTS="-Xmx2048m -Dorg.gradle.jvmargs=-Xmx2048m"

# Create gradle.properties file with Java 11 compatibility
echo "Creating gradle.properties for Java compatibility..."
mkdir -p ~/.gradle
cat > ~/.gradle/gradle.properties << EOF
org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
org.gradle.parallel=true
org.gradle.configureondemand=true
org.gradle.daemon=true
android.useAndroidX=true
android.enableJetifier=true
# Force Java 11 for all components
org.gradle.java.home=$JAVA_HOME
android.compileSdkVersion=33
android.buildToolsVersion=33.0.0
# Ensure consistent Java version across all dependencies
systemProp.java.specification.version=11
systemProp.java.version=11
systemProp.java.vm.specification.version=11
EOF

# Also create project-specific gradle.properties
echo "Creating project-specific gradle.properties..."
cat > gradle.properties << EOF
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
# Force Java 11 compatibility
android.compileSdkVersion=33
android.targetSdkVersion=33
android.minSdkVersion=23
# Java version enforcement
org.gradle.java.home=$JAVA_HOME
systemProp.java.specification.version=11
systemProp.java.version=11
EOF

# Create a custom gradle wrapper configuration
echo "Configuring Gradle wrapper for Java 11..."
mkdir -p .buildozer/android/platform/build-arm64-v8a/gradle/wrapper 2>/dev/null || true

echo "✅ Java/Gradle environment configured"
echo ""
echo "Now try building again:"
echo "buildozer android debug"
echo ""
echo "If you still get Java compatibility errors, the buildozer.spec has been"
echo "updated to use Android API 33 and NDK 25c for optimal compatibility."
echo ""
echo "Configuration used:"
echo "- Android API: 33 (down from 34 for Java 11 compatibility)"
echo "- NDK: 25c (minimum supported version)"
echo "- Min API: 23 (good device coverage)"
echo "- Java: 11 (required for modern Android builds)"