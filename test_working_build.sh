#!/bin/bash

echo "🔧 TESTING WORKING BUILDOZER CONFIGURATION"
echo "=========================================="

cd /mnt/c/repos/synergyclient

# 1. Backup current buildozer.spec
echo "📁 Backing up current buildozer.spec..."
cp buildozer.spec buildozer.spec.backup2

# 2. Use working configuration with essential Android settings
echo "🔄 Switching to working buildozer configuration..."
cp buildozer_working.spec buildozer.spec

# 3. Clean build completely
echo "🧹 Cleaning buildozer build artifacts..."
rm -rf .buildozer/
rm -rf bin/

# 4. Switch to debug main.py
echo "🔄 Switching to debug main.py..."
cp main_debug.py main.py

# 5. Show configuration being used
echo "📋 Using this buildozer.spec:"
echo "=========================="
cat buildozer.spec
echo ""

# 6. Activate environment and build
echo "🚀 Starting build with essential Android settings..."
source buildenv/bin/activate

echo "📱 About to run: buildozer android debug"
echo ""
echo "This should now complete successfully and include Python files!"
echo ""
echo "After build completes, install APK and test 'Show Available Files' button"
echo ""
echo "Press Enter to start build or Ctrl+C to cancel..."
read

buildozer android debug

echo ""
echo "🎯 BUILD COMPLETED!"
echo ""
echo "If successful, install the APK and test the 'Show Available Files' button"
echo "It should now show multiple .py files instead of 0"
echo ""
echo "To restore original buildozer.spec:"
echo "   cp buildozer.spec.backup2 buildozer.spec"