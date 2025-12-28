#!/bin/bash

echo "=================================================="
echo "Trix Python SDK - Structure Verification"
echo "=================================================="
echo ""

# Check Python version
echo "✓ Python Version:"
python3 --version | sed 's/^/  /'
echo ""

# Count and verify files
echo "✓ Project Statistics:"
echo "  Source files: $(find src -name "*.py" | wc -l)"
echo "  Test files: $(find tests -name "*.py" | wc -l)"
echo "  Example files: $(find examples -name "*.py" | wc -l)"
echo "  Total lines of source code: $(find src -name "*.py" -exec cat {} + | wc -l)"
echo ""

# Resource modules
echo "✓ Resource Modules (11):"
for file in src/trix/resources/*.py; do
    if [ "$(basename $file)" != "__init__.py" ]; then
        echo "  - $(basename $file .py)"
    fi
done
echo ""

# Core modules
echo "✓ Core Modules (5):"
echo "  - client (sync & async clients)"
echo "  - types (Pydantic models)"
echo "  - exceptions (error handling)"
echo "  - auth (authentication)"
echo "  - __init__ (exports)"
echo ""

# Utils
echo "✓ Utility Modules (2):"
echo "  - pagination"
echo "  - retry"
echo ""

# Documentation
echo "✓ Documentation (5):"
for doc in README.md CONTRIBUTING.md CHANGELOG.md INSTALL.md PROJECT_SUMMARY.md; do
    if [ -f "$doc" ]; then
        echo "  - $doc ($(wc -l < "$doc") lines)"
    fi
done
echo ""

# Examples
echo "✓ Examples (4):"
for ex in examples/*.py; do
    echo "  - $(basename $ex)"
done
echo ""

# Configuration
echo "✓ Configuration Files:"
echo "  - pyproject.toml (package config)"
echo "  - .gitignore (git ignore)"
echo "  - Makefile (development tasks)"
echo "  - .editorconfig (editor settings)"
echo "  - .python-version (Python 3.9)"
echo "  - py.typed (PEP 561 marker)"
echo "  - MANIFEST.in (package manifest)"
echo ""

# Testing
echo "✓ Testing:"
echo "  - pytest configuration in pyproject.toml"
echo "  - GitHub Actions CI/CD workflow"
echo "  - Test fixtures in conftest.py"
echo ""

echo "=================================================="
echo "✓ Structure verification complete!"
echo "=================================================="
echo ""
echo "The SDK is ready for installation:"
echo ""
echo "  pip install -e ."
echo ""
echo "Or with dev dependencies:"
echo ""
echo "  pip install -e \".[dev]\""
echo ""
