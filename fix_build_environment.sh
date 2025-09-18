#!/bin/bash

echo "=== Fixing 'externally-managed-environment' Error ==="

# Create a virtual environment for the project
echo "Creating virtual environment..."
python3 -m venv buildenv

# Activate the virtual environment
echo "Activating virtual environment..."
source buildenv/bin/activate

# Upgrade pip in the virtual environment
echo "Upgrading pip..."
pip install --upgrade pip

# Install build dependencies
echo "Installing build dependencies..."
pip install setuptools wheel setuptools-scm distlib

echo "Installing buildozer and cython..."
pip install buildozer cython==0.29.33

# Install project requirements
echo "Installing project requirements..."
pip install -r requirements.txt

# Install additional system dependencies for WSL
echo "Installing system dependencies..."
sudo apt update

# Detect Ubuntu version and install compatible packages
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "20.04")
echo "Detected Ubuntu version: $UBUNTU_VERSION"

if [ "$(echo "$UBUNTU_VERSION >= 22.04" | bc -l 2>/dev/null || echo 0)" -eq 1 ]; then
    echo "Installing packages for Ubuntu 22.04+..."
    sudo apt install -y git zip unzip openjdk-11-jdk python3-pip python3-venv python3-dev python3-setuptools autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libncurses6 cmake libffi-dev libssl-dev build-essential
else
    echo "Installing packages for Ubuntu 20.04 and earlier..."
    sudo apt install -y git zip unzip openjdk-11-jdk python3-pip python3-venv python3-dev python3-setuptools python3-distutils autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential
fi

# If libtinfo5 failed, try alternatives
if ! dpkg -l | grep -q libtinfo5 && ! dpkg -l | grep -q libncurses6; then
    echo "Trying alternative ncurses packages..."
    sudo apt install -y libncurses6 || sudo apt install -y libtinfo6 || echo "Warning: Some ncurses packages may be missing"
fi

# Set Java 11 as default (required for Android API 31+)
echo "Setting Java 11 as default..."
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

# Clean any previous build attempts
echo "Cleaning previous build attempts..."
if [ -d ".buildozer" ]; then
    rm -rf .buildozer
fi

echo "=== Environment Setup Complete ==="
echo "Virtual environment created and activated."
echo "Now run: source buildenv/bin/activate && ./build_android.sh"