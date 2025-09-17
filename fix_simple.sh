#!/bin/bash

echo "=== Simple Fix for 'externally-managed-environment' Error ==="

# This is a minimal script that only fixes the core issue
# without installing all system dependencies

echo "Creating virtual environment (this fixes the externally-managed-environment error)..."
python3 -m venv buildenv

# Check if virtual environment was created successfully
if [ ! -d "buildenv" ]; then
    echo "❌ Failed to create virtual environment"
    echo "Trying to install python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
    
    # Try again
    python3 -m venv buildenv
    if [ ! -d "buildenv" ]; then
        echo "❌ Still failed to create virtual environment"
        exit 1
    fi
fi

echo "✅ Virtual environment created successfully"

# Activate the virtual environment
echo "Activating virtual environment..."
source buildenv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install minimal requirements for buildozer
echo "Installing setuptools (fixes distutils error)..."
pip install setuptools wheel

echo "Installing buildozer and cython..."
pip install buildozer cython==0.29.33

# Install project requirements
if [ -f "requirements.txt" ]; then
    echo "Installing project requirements..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found, installing basic requirements..."
    pip install kivy==2.3.0 requests pyjnius
fi

# Install distutils for Python 3.12+ compatibility
echo "Installing additional Python packages for compatibility..."
pip install setuptools-scm distlib

echo ""
echo "✅ Simple setup complete!"
echo ""
echo "The 'externally-managed-environment' error is now fixed."
echo "To build your APK:"
echo "1. source buildenv/bin/activate"
echo "2. buildozer android debug"
echo ""
echo "Note: You may need to install system dependencies manually if the build fails:"
echo "sudo apt install -y git zip unzip openjdk-8-jdk cmake build-essential python3-distutils"
echo ""
echo "If you still get distutils errors, also install:"
echo "sudo apt install -y python3-dev python3-setuptools"