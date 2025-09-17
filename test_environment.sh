#!/bin/bash

echo "=== Testing Build Environment for APK Creation ==="

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

# Test basic requirements
echo "Checking basic requirements..."

# Check Python
python3 --version >/dev/null 2>&1
print_status $? "Python 3 is installed"

# Check if we can create virtual environments
python3 -m venv --help >/dev/null 2>&1
print_status $? "Python venv module available"

# Check pip
pip --version >/dev/null 2>&1 || python3 -m pip --version >/dev/null 2>&1
print_status $? "pip is available"

# Check for externally managed environment
if [ -f "/usr/lib/python3.*/EXTERNALLY-MANAGED" ] || [ -f "/usr/lib/python*/EXTERNALLY-MANAGED" ]; then
    echo "⚠️  Externally managed Python environment detected (this is why you're getting the error)"
else
    echo "✅ No externally managed environment detected"
fi

# Check Java
java -version >/dev/null 2>&1
print_status $? "Java is installed"

if [ -n "$JAVA_HOME" ]; then
    echo "✅ JAVA_HOME is set: $JAVA_HOME"
else
    echo "⚠️  JAVA_HOME not set"
fi

# Check Docker
command_exists docker
print_status $? "Docker is available"

if command_exists docker; then
    docker info >/dev/null 2>&1
    print_status $? "Docker daemon is running"
fi

# Check pipx
command_exists pipx
print_status $? "pipx is available"

# Check system dependencies
echo ""
echo "Checking system dependencies..."

command_exists git
print_status $? "git"

command_exists zip
print_status $? "zip"

command_exists unzip
print_status $? "unzip"

command_exists autoconf
print_status $? "autoconf"

command_exists libtool
print_status $? "libtool"

command_exists cmake
print_status $? "cmake"

# Check if scripts are executable
echo ""
echo "Checking build scripts..."

[ -x "fix_build_environment.sh" ]
print_status $? "fix_build_environment.sh is executable"

[ -x "build_android_venv.sh" ]
print_status $? "build_android_venv.sh is executable"

[ -x "build_with_pipx.sh" ]
print_status $? "build_with_pipx.sh is executable"

[ -x "build_with_docker.sh" ]
print_status $? "build_with_docker.sh is executable"

# Check project files
echo ""
echo "Checking project structure..."

[ -f "main.py" ]
print_status $? "main.py exists"

[ -f "buildozer.spec" ]
print_status $? "buildozer.spec exists"

[ -f "requirements.txt" ]
print_status $? "requirements.txt exists"

echo ""
echo "=== Environment Test Complete ==="
echo ""

# Provide recommendations
echo "Recommendations:"
echo ""

if command_exists docker && docker info >/dev/null 2>&1; then
    echo "🐳 RECOMMENDED: Use Docker approach (most reliable for WSL)"
    echo "   Run: ./build_with_docker.sh"
elif python3 -m venv --help >/dev/null 2>&1; then
    echo "🐍 RECOMMENDED: Use Virtual Environment approach"
    echo "   Run: ./fix_build_environment.sh && ./build_android_venv.sh"
elif command_exists pipx; then
    echo "📦 RECOMMENDED: Use pipx approach"
    echo "   Run: ./build_with_pipx.sh"
else
    echo "⚠️  You may need to install additional dependencies first"
    echo "   For Docker: sudo apt install docker.io"
    echo "   For venv: sudo apt install python3-venv"
    echo "   For pipx: sudo apt install pipx"
fi

echo ""
echo "If you see the 'externally-managed-environment' error, use one of the provided scripts above."