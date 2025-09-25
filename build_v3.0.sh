#!/bin/bash

echo "🎯 SYNERGY CLIENT v3.0 BUILD - SINGLE-FILE SOLUTION"
echo "=================================================="

cd /mnt/c/repos/synergyclient

# Version tracking
VERSION="v3.0"
BUILD_DATE=$(date +"%Y-%m-%d")

echo "Building version: $VERSION - SINGLE-FILE APPROACH"
echo "Build date: $BUILD_DATE"
echo ""

# 1. Backup everything
echo "📁 Creating v3.0 backups..."
cp buildozer.spec buildozer.spec.backup_v3
cp main.py main.py.backup_v3

# 2. Use v3.0 single-file approach
echo "🔄 Setting up v3.0 single-file solution..."
cp main_v3.0.py main.py
cp buildozer_v3.0.spec buildozer.spec

echo "✅ Active files for v3.0:"
echo "   main.py <- main_v3.0.py (ALL SERVICES EMBEDDED)"
echo "   buildozer.spec <- buildozer_v3.0.spec (minimal config)"
echo ""

# 3. Show the approach
echo "🔧 v3.0 APPROACH EXPLANATION:"
echo "================================"
echo "❌ PROBLEM: Buildozer not including separate .py service files"
echo "✅ SOLUTION: Embed ALL service code directly in main.py"
echo ""
echo "📋 Embedded in main.py:"
echo "   - BluetoothServiceMock class"
echo "   - WiFiHotspotServiceMock class" 
echo "   - FileTransferServiceMock class"
echo "   - All service functionality"
echo ""
echo "🎯 EXPECTED RESULT:"
echo "   - App shows 'SYNERGY CLIENT v3.0 - SINGLE FILE SOLUTION' in MAGENTA"
echo "   - ALL services work because they're embedded in main.py"
echo "   - No import errors since no external files needed"
echo ""

# 4. Show minimal buildozer config
echo "📋 v3.0 Buildozer Configuration (Ultra-Simple):"
echo "=============================================="
echo "Title: $(grep '^title' buildozer.spec)"
echo "Version: $(grep '^version' buildozer.spec)"
echo "Include: $(grep '^source.include_exts' buildozer.spec)"
echo "NO complex inclusion patterns - just main.py!"
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

# 7. Build the single-file solution
echo "🚀 Starting v3.0 SINGLE-FILE build..."
echo ""
echo "This SHOULD work because:"
echo "- Only main.py is needed (always included by buildozer)"
echo "- All services are embedded classes in main.py"
echo "- No separate files to include/exclude"
echo "- Minimal buildozer configuration"
echo ""

buildozer android debug

BUILD_RESULT=$?

if [ $BUILD_RESULT -eq 0 ]; then
    echo ""
    echo "🎉 v3.0 SINGLE-FILE BUILD SUCCESSFUL!"
    echo ""
    echo "📱 INSTALLATION & VERIFICATION:"
    echo "1. Install: bin/synergyclient-3.0-arm64-v8a-debug.apk"
    echo ""
    echo "2. LOOK FOR MAGENTA HEADER:"
    echo "   'SYNERGY CLIENT v3.0 - SINGLE FILE SOLUTION'"
    echo "   Build: $BUILD_DATE"
    echo ""
    echo "3. TAP 'Show Available Files (v3.0 Single-File)'"
    echo "   Should show embedded services status"
    echo ""
    echo "4. TEST EMBEDDED SERVICES:"
    echo "   - Tap 'Test Embedded Bluetooth' ✅"
    echo "   - Tap 'Test Embedded WiFi' ✅"
    echo "   - Tap 'Test Embedded File Transfer' ✅"
    echo ""
    echo "🎯 ALL SERVICES SHOULD WORK - they're embedded in main.py!"
    echo ""
else
    echo ""
    echo "❌ v3.0 SINGLE-FILE BUILD FAILED!"
    echo ""
    echo "If this fails, the issue is deeper than source file inclusion."
    echo "This would indicate a fundamental buildozer/environment problem."
fi

echo ""
echo "📄 To restore original files:"
echo "   cp buildozer.spec.backup_v3 buildozer.spec"
echo "   cp main.py.backup_v3 main.py"
echo ""
echo "🔧 v3.0 single-file build process complete!"