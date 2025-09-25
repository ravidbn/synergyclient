#!/bin/bash

echo "🚀 SYNERGY CLIENT v2.0 BUILD - FORCED SOURCE INCLUSION"
echo "===================================================="

cd /mnt/c/repos/synergyclient

# Version tracking
VERSION="v2.0"
BUILD_DATE=$(date +"%Y-%m-%d")

echo "Building version: $VERSION"
echo "Build date: $BUILD_DATE"
echo ""

# 1. Backup everything
echo "📁 Creating backups..."
cp buildozer.spec buildozer.spec.backup_v2
cp main.py main.py.backup_v2

# 2. Use v2.0 files
echo "🔄 Setting up v2.0 files..."
cp main_v2.0.py main.py
cp buildozer_v2.0.spec buildozer.spec

echo "✅ Active files for v2.0:"
echo "   main.py <- main_v2.0.py (with version display)"
echo "   buildozer.spec <- buildozer_v2.0.spec (aggressive inclusion)"
echo ""

# 3. Verify service files exist
echo "📋 Verifying service files exist..."
for file in bluetooth_service_mock.py wifi_hotspot_service_mock.py file_transfer_service_mock.py; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING!"
        exit 1
    fi
done
echo ""

# 4. Show buildozer config being used
echo "📋 v2.0 Buildozer Configuration:"
echo "==============================="
echo "Title: $(grep '^title' buildozer.spec)"
echo "Version: $(grep '^version' buildozer.spec)"
echo "Include extensions: $(grep '^source.include_exts' buildozer.spec)"
echo "Include patterns: $(grep '^source.include_patterns' buildozer.spec)"
echo "Android add_src: $(grep '^android.add_src' buildozer.spec)"
echo ""

# 5. Complete clean
echo "🧹 Complete clean build..."
rm -rf .buildozer/
rm -rf bin/
echo "✅ Build directories cleaned"
echo ""

# 6. Activate environment
echo "🐍 Activating build environment..."
source buildenv/bin/activate

# 7. Build with multiple fallback strategies
echo "🚀 Starting v2.0 build process..."
echo ""

echo "Strategy 1: Building with aggressive source inclusion..."
buildozer android debug

BUILD_RESULT=$?

if [ $BUILD_RESULT -eq 0 ]; then
    echo ""
    echo "🎉 BUILD SUCCESSFUL!"
    echo ""
    echo "📱 INSTALLATION INSTRUCTIONS:"
    echo "1. Install the APK: bin/synergyclient-2.0-arm64-v8a-debug.apk"
    echo "2. Look for 'SYNERGY CLIENT v2.0 - SOURCE FIX ATTEMPT' at the top"
    echo "3. Tap 'Show Available Files (v2.0 Debug)'"
    echo "4. Should show multiple .py files instead of 0"
    echo ""
    echo "🔍 VERIFICATION:"
    echo "- Yellow version header should show: v2.0 - SOURCE FIX ATTEMPT"
    echo "- Build date should show: $BUILD_DATE"
    echo "- File listing should show .py files"
    echo ""
else
    echo ""
    echo "❌ v2.0 BUILD FAILED!"
    echo ""
    echo "📋 Trying alternative approach..."
    
    # Alternative: Copy files directly to build directory approach
    echo "Strategy 2: Manual file copying approach..."
    
    # This would need to be implemented if Strategy 1 fails
    echo "Please check build logs and try manual intervention"
fi

echo ""
echo "📄 To restore original files:"
echo "   cp buildozer.spec.backup_v2 buildozer.spec"
echo "   cp main.py.backup_v2 main.py"
echo ""
echo "🔧 v2.0 build process complete!"