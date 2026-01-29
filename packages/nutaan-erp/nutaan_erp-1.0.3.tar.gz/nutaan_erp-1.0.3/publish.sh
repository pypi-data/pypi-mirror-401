#!/bin/bash
# Quick publish script for nutaan-erp to PyPI

set -e

cd "$(dirname "$0")"

echo "🧹 Cleaning old builds..."
rm -rf build/ dist/ *.egg-info/ nutaan_erp.egg-info/

echo "📦 Building package..."
python -m build

echo "🔍 Checking package..."
python -m twine check dist/*

echo ""
echo "✅ Package built successfully!"
echo ""
echo "📤 To upload to PyPI, run:"
echo "   python -m twine upload dist/*"
echo ""
echo "📤 To upload to Test PyPI first (recommended), run:"
echo "   python -m twine upload --repository testpypi dist/*"
echo ""
echo "Package details:"
ls -lh dist/
