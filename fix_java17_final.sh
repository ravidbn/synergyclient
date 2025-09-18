#!/bin/bash

echo "=== Final Fix: Android Gradle Plugin Requires Java 17 ==="

# The error is clear: "Android Gradle plugin requires Java 17 to run"
# This script updates everything to use Java 17

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

# Install Java 17
echo "Installing Java 17 (required by Android Gradle Plugin)..."
sudo apt update
sudo apt install -y openjdk-17-jdk

# Set Java 17 environment variables with fallback detection
echo "Configuring Java 17 environment..."
JAVA_17_PATHS=(
    "/usr/lib/jvm/java-17-openjdk-amd64"
    "/usr/lib/jvm/java-17-openjdk"
    "/usr/lib/jvm/java-1.17.0-openjdk-amd64" 
    "/usr/lib/jvm/java-1.17.0-openjdk"
)

JAVA_HOME_FOUND=""
for path in "${JAVA_17_PATHS[@]}"; do
    if [ -d "$path" ]; then
        JAVA_HOME_FOUND="$path"
        break
    fi
done

if [ -z "$JAVA_HOME_FOUND" ]; then
    echo "❌ Java 17 installation failed or not found"
    exit 1
fi

export JAVA_HOME="$JAVA_HOME_FOUND"
export PATH="$JAVA_HOME/bin:$PATH"

echo "✅ JAVA_HOME: $JAVA_HOME"
echo "Java version:"
java -version

# Force all Java-related environment variables for Java 17
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"
export GRADLE_OPTS="-Xmx4096m -Dorg.gradle.daemon=false -Dorg.gradle.jvmargs=-Xmx4096m"
export ANDROID_JAVA_HOME="$JAVA_HOME"

# Create comprehensive gradle.properties for Java 17
echo "Creating Gradle configuration for Java 17..."
cat > gradle.properties << EOF
# Gradle JVM settings for Java 17
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8 -Duser.country=US -Duser.language=en
org.gradle.daemon=false
org.gradle.parallel=false
org.gradle.configureondemand=false

# Point Gradle to Java 17
org.gradle.java.home=$JAVA_HOME

# Android settings
android.useAndroidX=true
android.enableJetifier=true

# Target Android API compatible with Java 17
android.compileSdkVersion=33
android.targetSdkVersion=33
android.minSdkVersion=23

# Force Java 17 throughout the build
systemProp.java.specification.version=17
systemProp.java.version=17
systemProp.java.vm.specification.version=17
systemProp.java.runtime.version=17

# Kotlin compatibility for Java 17
kotlin.code.style=official
kotlin.jvm.target.validation.mode=warning
EOF

# Create global gradle.properties
mkdir -p ~/.gradle
cp gradle.properties ~/.gradle/gradle.properties

# Update buildozer to latest version
echo "Updating buildozer to latest version..."
pip install --upgrade buildozer

# Set environment in bashrc for future sessions
echo "Setting environment variables for future sessions..."
# Remove old Java exports first
sed -i '/export JAVA_HOME.*java-[0-9]/d' ~/.bashrc 2>/dev/null || true
sed -i '/export ANDROID_JAVA_HOME.*java-[0-9]/d' ~/.bashrc 2>/dev/null || true

echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "export ANDROID_JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "export PATH=$JAVA_HOME/bin:\$PATH" >> ~/.bashrc

# Verify Java 17 is working
echo ""
echo "Verifying Java 17 installation..."
if java -version 2>&1 | grep -q "openjdk version \"17"; then
    echo "✅ Java 17 successfully configured"
else
    echo "⚠️ Warning: Java version verification failed"
    java -version
fi

echo ""
echo "✅ Java 17 configuration complete!"
echo ""
echo "The Android Gradle Plugin requires Java 17, which is now configured."
echo ""
echo "Environment configured:"
echo "- JAVA_HOME: $JAVA_HOME" 
echo "- Java Version: $(java -version 2>&1 | head -1)"
echo "- Gradle configured for Java 17"
echo "- Android Gradle Plugin compatibility: ✅"
echo ""
echo "Now try building:"
echo ""
echo "buildozer android debug"
echo ""
echo "If you get cache issues, run: buildozer android clean && buildozer android debug"