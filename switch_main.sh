#!/bin/bash

echo "=== Synergy Client Main File Switcher ==="

# Function to show current main file
show_current() {
    if [ -f "main.py" ]; then
        if grep -q "Real Android Services" main.py; then
            echo "Current: Real Services Version"
        elif grep -q "Minimal Version" main.py; then
            echo "Current: Minimal Version"
        else
            echo "Current: Standard Version"
        fi
    else
        echo "Current: No main.py found"
    fi
}

# Show menu
echo ""
show_current
echo ""
echo "Available versions:"
echo "1. Real Services (use real Android APIs when possible)"
echo "2. Debug Version (shows what files are in APK)"
echo "3. Standard Version (original main.py)"
echo "4. Minimal Version (basic testing)"
echo "5. Show current file details"
echo ""
read -p "Choose version (1-5): " choice

case $choice in
    1)
        if [ -f "main_real_services.py" ]; then
            echo "Switching to Real Services version..."
            cp main.py main_backup.py 2>/dev/null
            cp main_real_services.py main.py
            echo "✅ Switched to Real Services version"
            echo "📦 Rebuild APK: source buildenv/bin/activate && buildozer android debug"
        else
            echo "❌ main_real_services.py not found"
        fi
        ;;
    2)
        if [ -f "main_debug.py" ]; then
            echo "Switching to Debug version..."
            cp main.py main_backup.py 2>/dev/null
            cp main_debug.py main.py
            echo "✅ Switched to Debug version"
            echo "📦 This version will show what files are actually in the APK"
            echo "📦 Rebuild APK: source buildenv/bin/activate && buildozer android debug"
        else
            echo "❌ main_debug.py not found"
        fi
        ;;
    3)
        if [ -f "main_backup.py" ]; then
            echo "Restoring Standard version..."
            cp main_backup.py main.py
            echo "✅ Restored Standard version"
        else
            echo "ℹ️  main.py is already the standard version"
        fi
        ;;
    4)
        if [ -f "main_minimal.py" ]; then
            echo "Switching to Minimal version..."
            cp main.py main_backup.py 2>/dev/null
            cp main_minimal.py main.py
            echo "✅ Switched to Minimal version"
        else
            echo "❌ main_minimal.py not found"
        fi
        ;;
    5)
        echo ""
        echo "=== Current main.py Details ==="
        if [ -f "main.py" ]; then
            echo "File size: $(wc -l < main.py) lines"
            echo ""
            echo "Key features detected:"
            grep -q "Real Android Services" main.py && echo "✅ Real Services support"
            grep -q "mock" main.py && echo "✅ Mock service fallback"
            grep -q "ANDROID_AVAILABLE" main.py && echo "✅ Android API detection"
            grep -q "dp(" main.py && echo "✅ Fixed UI layout"
            grep -q "prevent_backgrounding" main.py && echo "✅ Background prevention"
            echo ""
            echo "First few lines:"
            head -10 main.py
        else
            echo "❌ main.py not found"
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
show_current
echo ""
echo "Note: After switching, rebuild the APK to see changes on device"