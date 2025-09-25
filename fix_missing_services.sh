#!/bin/bash

echo "=== Fixing Missing Service Files in APK ==="

# The log showed: "No module named 'bluetooth_service_mock'"
# This means service files weren't included in the APK build

echo "Issue identified: Service files not included in APK build"
echo "Solution: Updated buildozer.spec to explicitly include service files"
echo ""

# Check if we have the service files in the project
echo "Checking service files in project..."
if [ -f "bluetooth_service.py" ]; then
    echo "✅ bluetooth_service.py found"
else
    echo "❌ bluetooth_service.py missing"
fi

if [ -f "bluetooth_service_mock.py" ]; then
    echo "✅ bluetooth_service_mock.py found"
else
    echo "❌ bluetooth_service_mock.py missing"
fi

if [ -f "wifi_hotspot_service.py" ]; then
    echo "✅ wifi_hotspot_service.py found"
else
    echo "❌ wifi_hotspot_service.py missing"
fi

if [ -f "wifi_hotspot_service_mock.py" ]; then
    echo "✅ wifi_hotspot_service_mock.py found"
else
    echo "❌ wifi_hotspot_service_mock.py missing"
fi

if [ -f "file_transfer_service.py" ]; then
    echo "✅ file_transfer_service.py found"
else
    echo "❌ file_transfer_service.py missing"
fi

if [ -f "file_transfer_service_mock.py" ]; then
    echo "✅ file_transfer_service_mock.py found"
else
    echo "❌ file_transfer_service_mock.py missing"
fi

echo ""
echo "=== buildozer.spec has been updated with: ==="
echo "- Explicit inclusion of *_service*.py files"
echo "- Explicit inclusion of *_mock.py files"
echo "- Explicit inclusion of utils/*.py files"
echo "- Exclusion of build/test files to avoid conflicts"
echo ""

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not active"
    echo "Please run: source buildenv/bin/activate"
    echo ""
fi

echo "Next steps to rebuild APK with service files:"
echo ""
echo "1. Activate virtual environment:"
echo "   source buildenv/bin/activate"
echo ""
echo "2. Clean previous build:"
echo "   rm -rf .buildozer bin/"
echo ""
echo "3. Rebuild APK with service files included:"
echo "   buildozer android debug"
echo ""
echo "4. Install new APK:"
echo "   adb install bin/*.apk"
echo ""
echo "5. Test the app - should now show real services instead of 'No module named' errors"
echo ""

# Optional: automatically run if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment is active. Do you want to rebuild now? (y/n)"
    read -p "Rebuild APK: " rebuild
    if [ "$rebuild" = "y" ] || [ "$rebuild" = "Y" ]; then
        echo "Cleaning previous build..."
        rm -rf .buildozer bin/
        
        echo "Rebuilding APK with service files..."
        buildozer android debug
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ APK rebuilt successfully!"
            echo "Install with: adb install bin/*.apk"
            echo ""
            echo "The app should now load real services instead of showing 'No module named' errors."
        else
            echo "❌ Build failed. Check error messages above."
        fi
    fi
fi

echo "=== Fix Complete ==="