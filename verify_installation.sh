#!/bin/bash

echo "=================================================="
echo "TrixDB Python SDK - Installation Verification"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Python 3 not found"
    exit 1
fi

# Check if we can import the module
echo ""
echo "Checking module structure..."
if python3 -c "import sys; sys.path.insert(0, 'src'); import trixdb" 2>/dev/null; then
    echo "✓ trixdb module can be imported"
else
    echo "✗ Cannot import trixdb module"
    exit 1
fi

# Count files
echo ""
echo "Counting project files..."
PY_FILES=$(find src -name "*.py" | wc -l)
TEST_FILES=$(find tests -name "*.py" | wc -l)
EXAMPLE_FILES=$(find examples -name "*.py" | wc -l)
echo "✓ Source files: $PY_FILES"
echo "✓ Test files: $TEST_FILES"
echo "✓ Example files: $EXAMPLE_FILES"

# Check documentation
echo ""
echo "Checking documentation..."
[ -f README.md ] && echo "✓ README.md exists" || echo "✗ README.md missing"
[ -f CONTRIBUTING.md ] && echo "✓ CONTRIBUTING.md exists" || echo "✗ CONTRIBUTING.md missing"
[ -f CHANGELOG.md ] && echo "✓ CHANGELOG.md exists" || echo "✗ CHANGELOG.md missing"
[ -f LICENSE ] && echo "✓ LICENSE exists" || echo "✗ LICENSE missing"

# Check configuration
echo ""
echo "Checking configuration files..."
[ -f pyproject.toml ] && echo "✓ pyproject.toml exists" || echo "✗ pyproject.toml missing"
[ -f .gitignore ] && echo "✓ .gitignore exists" || echo "✗ .gitignore missing"
[ -f Makefile ] && echo "✓ Makefile exists" || echo "✗ Makefile missing"

# Check directory structure
echo ""
echo "Checking directory structure..."
[ -d src/trixdb ] && echo "✓ src/trixdb/ exists" || echo "✗ src/trixdb/ missing"
[ -d src/trixdb/resources ] && echo "✓ src/trixdb/resources/ exists" || echo "✗ resources/ missing"
[ -d src/trixdb/utils ] && echo "✓ src/trixdb/utils/ exists" || echo "✗ utils/ missing"
[ -d tests ] && echo "✓ tests/ exists" || echo "✗ tests/ missing"
[ -d examples ] && echo "✓ examples/ exists" || echo "✗ examples/ missing"

echo ""
echo "=================================================="
echo "✓ Installation verification complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Install the package: pip install -e ."
echo "2. Run tests: pytest"
echo "3. Try quickstart: python examples/quickstart.py"
echo ""
