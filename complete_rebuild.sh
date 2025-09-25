#!/bin/bash

echo "=== COMPLETE APK REBUILD TO FIX MISSING SERVICE FILES ==="

# This script addresses the "No module named 'bluetooth_service_mock'" error
# by doing a complete clean rebuild with updated buildozer configuration

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Run this script from the project root directory."
    exit 1
fi

# Check if virtual environment is available
if [ ! -d "buildenv" ]; then
    echo "❌ Error: buildenv directory not found. Run fix_simple.sh first."
    exit 1
fi

echo "Step 1: Activate virtual environment"
source buildenv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✅ Virtual environment activated"

echo ""
echo "Step 2: Verify service files exist"
missing_files=0

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 MISSING"
        missing_files=$((missing_files + 1))
    fi
}

check_file "bluetooth_service.py"
check_file "bluetooth_service_mock.py"
check_file "wifi_hotspot_service.py"
check_file "wifi_hotspot_service_mock.py"
check_file "file_transfer_service.py"
check_file "file_transfer_service_mock.py"
check_file "utils/protocol.py"

if [ $missing_files -gt 0 ]; then
    echo "❌ $missing_files service files are missing. Cannot proceed."
    exit 1
fi

echo ""
echo "Step 3: Choose main.py version"
echo "1. Debug version (shows what files are actually in APK)"
echo "2. Real services version (production)"
echo "3. Keep current main.py"
read -p "Choose option (1-3): " version_choice

case $version_choice in
    1)
        if [ -f "main_debug.py" ]; then
            cp main.py main_backup.py 2>/dev/null
            cp main_debug.py main.py
            echo "✅ Switched to Debug version"
        else
            echo "❌ main_debug.py not found"
            exit 1
        fi
        ;;
    2)
        if [ -f "main_real_services.py" ]; then
            cp main.py main_backup.py 2>/dev/null
            cp main_real_services.py main.py
            echo "✅ Switched to Real Services version"
        else
            echo "❌ main_real_services.py not found"
            exit 1
        fi
        ;;
    3)
        echo "✅ Keeping current main.py"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "Step 4: Verify buildozer.spec configuration"
if grep -q "bluetooth_service.*\.py" buildozer.spec; then
    echo "✅ buildozer.spec includes explicit service file patterns"
else
    echo "⚠️  buildozer.spec may not include service files explicitly"
fi

echo ""
echo "Step 5: Complete clean rebuild"
echo "Removing all build artifacts..."
rm -rf .buildozer
rm -rf bin/
rm -rf dist/
rm -rf __pycache__
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
echo "✅ Build artifacts cleaned"

echo ""
echo "Step 6: Build APK with service files"
echo "This may take 10-30 minutes for the first build..."
echo ""

# Build with verbose output to see what files are being included
buildozer android debug --verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 BUILD SUCCESSFUL!"
    echo ""
    if [ -d "bin" ]; then
        echo "=== APK FILES CREATED ==="
        ls -la bin/*.apk
        echo ""
        echo "Step 7: Install APK"
        echo "Run this command to install:"
        echo "adb install bin/*.apk"
        echo ""
        echo "Step 8: Test the app"
        echo "1. Open the app on your phone"
        echo "2. Look for service status indicators"
        echo "3. If using debug version, tap 'Show Available Files'"
        echo "4. Check logs: adb logcat | grep -i synergy"
        echo ""
        if [ "$version_choice" = "1" ]; then
            echo "DEBUG VERSION NOTES:"
            echo "- The debug version will show exactly which files are in the APK"
            echo "- Look for 'Files: X .py files' in the app"
            echo "- Tap 'Show Available Files' to see the complete list"
            echo "- This will tell us if service files are actually included"
        fi
    else
        echo "❌ Build succeeded but no bin/ directory found"
        echo "Check the build output above for errors"
    fi
else
    echo ""
    echo "❌ BUILD FAILED"
    echo ""
    echo "Common issues:"
    echo "1. Java version - make sure Java 17 is installed"
    echo "2. Android SDK - buildozer will download if needed"
    echo "3. NDK version - using 25c in buildozer.spec"
    echo ""
    echo "Check the error messages above and try:"
    echo "- Run fix_java17_final.sh if Java errors"
    echo "- Run buildozer android clean && buildozer android debug"
    exit 1
fi

echo ""
echo "=== REBUILD COMPLETE ==="
echo ""
echo "Next steps:"
echo "1. Install: adb install bin/*.apk"
echo "2. Test: Open app and check service status"
echo "3. Debug: adb logcat | grep -i synergy"
echo ""
echo "If you still see 'No module named' errors:"
echo "1. Use the debug version to see what files are actually in APK"
echo "2. Check the verbose build output above for file inclusion messages"
echo "3. The problem may be in buildozer's file packaging, not our configuration"