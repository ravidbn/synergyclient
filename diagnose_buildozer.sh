#!/bin/bash

echo "🔍 COMPREHENSIVE BUILDOZER DIAGNOSTICS"
echo "======================================"

cd /mnt/c/repos/synergyclient

echo "📁 STEP 1: Current Directory & Files"
echo "Current directory: $(pwd)"
echo "Python files in current directory:"
find . -maxdepth 1 -name "*.py" | head -10
echo ""

echo "📋 STEP 2: Buildozer Version & Environment"
source buildenv/bin/activate
buildozer --version
echo "Python version: $(python --version)"
echo "Kivy installed: $(python -c 'import kivy; print(kivy.__version__)' 2>/dev/null || echo 'NOT INSTALLED')"
echo ""

echo "🧪 STEP 3: Test Ultra-Minimal Config"
cp buildozer_ultra_minimal.spec buildozer.spec
echo "Using ultra-minimal buildozer.spec:"
cat buildozer.spec
echo ""

echo "🔍 STEP 4: Buildozer Source Analysis (Dry Run)"
echo "Let's see what buildozer thinks about our source files..."
buildozer android debug --verbose 2>&1 | grep -E "(source|include|exclude|\.py)" | head -20
echo ""

echo "📂 STEP 5: Check .buildozer Directory"
if [ -d ".buildozer" ]; then
    echo "Build directory exists. Checking for Python files in build:"
    find .buildozer/ -name "*.py" | wc -l
    echo "Python files found in .buildozer/"
else
    echo "No .buildozer directory found"
fi
echo ""

echo "🎯 STEP 6: Alternative Test - Single File App"
echo "Creating single-file test app..."
cat > test_single.py << 'EOF'
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='Test: Python files ARE included!', font_size=20)

TestApp().run()
EOF

echo "Created test_single.py"
echo ""

echo "📝 STEP 7: Create Single File Buildozer Config"
cat > buildozer_single.spec << 'EOF'
[app]
title = Test App
package.name = testapp
package.domain = org.test
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy

[buildozer]
log_level = 2
EOF

echo "Created buildozer_single.spec for single file test"
echo ""

echo "🚀 NEXT STEPS:"
echo "1. Try building with ultra-minimal config:"
echo "   buildozer android debug"
echo ""
echo "2. If that fails, try single file test:"
echo "   cp buildozer_single.spec buildozer.spec"
echo "   cp test_single.py main.py"
echo "   buildozer android debug"
echo ""
echo "3. Check build logs for 'source' related messages"