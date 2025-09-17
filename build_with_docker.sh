#!/bin/bash

echo "=== Android Build with Docker (Recommended for WSL) ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker..."
    
    # Install Docker on WSL/Ubuntu
    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release
    
    # Add Docker's official GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up the repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    
    echo "Docker installed. Please log out and log back in, then run this script again."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "Starting Docker daemon..."
    sudo service docker start
fi

# Clean any previous build artifacts
echo "Cleaning previous build artifacts..."
rm -rf .buildozer bin/

# Try multiple Docker image options
echo "=== Trying Docker build with multiple image options ==="

# Option 1: Try official image with specific tag
echo "Attempting with kivy/buildozer:1.5.0..."
if docker run --rm \
    -v "$PWD":/home/user/hostcwd \
    -e ANDROID_HOME=/opt/android-sdk \
    kivy/buildozer:1.5.0 \
    buildozer android debug 2>/dev/null; then
    echo "✅ Build successful with kivy/buildozer:1.5.0"
else
    echo "❌ Failed with kivy/buildozer:1.5.0, trying alternative..."
    
    # Option 2: Try with older Ubuntu-based image (non-interactive)
    echo "Attempting with custom Ubuntu buildozer setup..."
    if docker run --rm \
        -v "$PWD":/home/user/hostcwd \
        -w /home/user/hostcwd \
        -e DEBIAN_FRONTEND=noninteractive \
        -e TZ=UTC \
        ubuntu:20.04 \
        bash -c "
        ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone &&
        apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip git openjdk-8-jdk zip unzip autoconf libtool \
        pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
        cmake libffi-dev libssl-dev build-essential &&
        pip3 install --no-cache-dir buildozer cython==0.29.33 &&
        export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 &&
        buildozer android debug --verbose
        " 2>/dev/null; then
        echo "✅ Build successful with Ubuntu setup"
    else
        echo "❌ Docker builds failed. Please use virtual environment approach instead."
        echo "Run: ./fix_build_environment.sh && ./build_android_venv.sh"
        exit 1
    fi
fi

echo "=== Docker build completed ==="

# Check output
if [ -d "bin" ]; then
    echo "=== APK Files Found ==="
    ls -la bin/
    find bin/ -name "*.apk" -type f
    echo ""
    echo "Success! APK built using Docker."
    echo "Install with: adb install bin/*.apk"
else
    echo "=== No bin directory found ==="
    echo "Build may have failed. Check Docker logs above for errors."
    echo "Try running with verbose output:"
    echo "docker run --rm -v \"\$PWD\":/home/user/hostcwd kivy/buildozer:latest buildozer android debug -v"
fi

echo "=== Build process finished ==="