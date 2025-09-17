#!/bin/bash

echo "=== Quick Fix for 'No module named distutils' Error ==="

# This specifically fixes the distutils error that occurs with Python 3.12+

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

echo "Installing packages to fix distutils error..."

# Install setuptools and related packages
pip install --upgrade setuptools wheel setuptools-scm

# Install distutils alternatives
pip install distlib

# Try to install distutils if available
pip install distutils-extra 2>/dev/null || echo "distutils-extra not available (this is normal)"

echo "✅ Distutils compatibility packages installed"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" == "3.12" ]] || [[ "$PYTHON_VERSION" > "3.12" ]]; then
    echo "⚠️  Python 3.12+ detected. Installing additional compatibility packages..."
    
    # For Python 3.12+, we need to ensure setuptools provides distutils
    pip install --upgrade pip setuptools
    
    # Install specific packages that help with distutils compatibility
    pip install packaging
fi

echo ""
echo "✅ Distutils fix complete!"
echo ""
echo "Now try building again:"
echo "buildozer android debug"
echo ""
echo "If you still get distutils errors, you may need to install system packages:"
echo "sudo apt update"
echo "sudo apt install -y python3-dev python3-setuptools"