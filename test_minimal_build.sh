#!/bin/bash

echo "🔧 Testing Minimal Buildozer Configuration"
echo "=========================================="

# Make sure we're in the right directory
cd /mnt/c/repos/synergyclient

# 1. Backup current buildozer.spec
echo "📁 Backing up current buildozer.spec..."
cp buildozer.spec buildozer.spec.backup

# 2. Use minimal configuration
echo "🔄 Switching to minimal buildozer configuration..."
cp buildozer_minimal.spec buildozer.spec

# 3. Verify service files exist
echo "📋 Checking if service files exist..."
echo "✅ Checking bluetooth_service_mock.py: $([ -f bluetooth_service_mock.py ] && echo "EXISTS" || echo "MISSING")"
echo "✅ Checking wifi_hotspot_service_mock.py: $([ -f wifi_hotspot_service_mock.py ] && echo "EXISTS" || echo "MISSING")"
echo "✅ Checking file_transfer_service_mock.py: $([ -f file_transfer_service_mock.py ] && echo "EXISTS" || echo "MISSING")"
echo "✅ Checking main.py: $([ -f main.py ] && echo "EXISTS" || echo "MISSING")"

# 4. Switch to debug version
echo "🔄 Switching to debug main.py..."
cp main_debug.py main.py

# 5. Clean build completely
echo "🧹 Cleaning buildozer build artifacts..."
rm -rf .buildozer/
rm -rf bin/

# 6. Show what files will be included
echo "📂 Files that should be included (*.py files):"
find . -name "*.py" -not -path "./.buildozer/*" -not -path "./buildenv/*" -not -path "./.git/*" | head -20

echo ""
echo "🚀 Ready to build! Run:"
echo "   source buildenv/bin/activate"
echo "   buildozer android debug"
echo ""
echo "📱 After installing APK, check if 'Show Available Files' shows Python files"
echo ""
echo "To restore original buildozer.spec:"
echo "   cp buildozer.spec.backup buildozer.spec"