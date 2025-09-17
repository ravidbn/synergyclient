#!/bin/bash

echo "=== APK Build Script - Automatic Solution Selection ==="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
    else
        echo "❌ $2"
    fi
}

echo "Checking available build methods..."

# Check for externally managed environment
EXTERNALLY_MANAGED=false
if ls /usr/lib/python*/EXTERNALLY-MANAGED 2>/dev/null | head -1; then
    EXTERNALLY_MANAGED=true
    echo "⚠️  Externally managed Python environment detected"
fi

# Method 1: Try Virtual Environment (Most reliable)
if python3 -m venv --help >/dev/null 2>&1; then
    echo ""
    echo "🐍 Using Virtual Environment approach (RECOMMENDED)"
    echo "This method creates an isolated Python environment to avoid the externally-managed-environment error."
    echo ""
    
    # Check if virtual environment already exists
    if [ ! -d "buildenv" ]; then
        echo "Setting up virtual environment..."
        if ./fix_build_environment.sh; then
            echo "✅ Virtual environment setup complete"
        else
            echo "❌ Virtual environment setup failed, trying alternative methods..."
        fi
    else
        echo "✅ Virtual environment already exists"
    fi
    
    # Only try to build if setup succeeded or venv already exists
    if [ -d "buildenv" ]; then
        echo "Building APK with virtual environment..."
        if ./build_android_venv.sh; then
            echo ""
            echo "🎉 SUCCESS! APK built successfully using virtual environment"
            echo ""
            if [ -d "bin" ]; then
                echo "APK location:"
                find bin/ -name "*.apk" -type f
                echo ""
                echo "To install on your Android device:"
                echo "adb install bin/*.apk"
            fi
            exit 0
        else
            echo "❌ Virtual environment build failed, trying alternative methods..."
        fi
    fi
fi

# Method 2: Try pipx (More reliable than Docker)
if command_exists pipx; then
    echo ""
    echo "📦 Trying pipx approach..."
    if ./build_with_pipx.sh; then
        echo "🎉 SUCCESS! APK built successfully using pipx"
        if [ -d "bin" ]; then
            echo "APK location:"
            find bin/ -name "*.apk" -type f
        fi
        exit 0
    else
        echo "❌ pipx build failed"
    fi
fi

# Method 3: Try Docker (last resort - can have timezone issues)
if command_exists docker && docker info >/dev/null 2>&1; then
    echo ""
    echo "🐳 Trying Docker approach (last resort)..."
    echo "Note: This may take longer and might prompt for timezone configuration"
    if ./build_with_docker.sh; then
        echo "🎉 SUCCESS! APK built successfully using Docker"
        if [ -d "bin" ]; then
            echo "APK location:"
            find bin/ -name "*.apk" -type f
        fi
        exit 0
    else
        echo "❌ Docker build failed"
    fi
fi

# If all methods fail
echo ""
echo "❌ All automated build methods failed."
echo ""
echo "Manual steps to resolve:"
echo ""
echo "1. RECOMMENDED: Virtual Environment (if not tried yet)"
echo "   chmod +x fix_build_environment.sh build_android_venv.sh"
echo "   ./fix_build_environment.sh"
echo "   source buildenv/bin/activate"
echo "   ./build_android_venv.sh"
echo ""
echo "2. Install missing dependencies:"
echo "   sudo apt update"
echo "   sudo apt install python3-venv python3-pip openjdk-8-jdk"
echo ""
echo "3. Check your environment:"
echo "   ./test_environment.sh"
echo ""
echo "4. For help, see: WSL_BUILD_SOLUTIONS.md"

exit 1