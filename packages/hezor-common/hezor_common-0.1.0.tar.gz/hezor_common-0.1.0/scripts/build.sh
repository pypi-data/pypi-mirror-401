#!/bin/bash
# Build script for hezor-common package

set -e

echo "🔨 Building hezor-common package..."

# Clean previous builds
if [ -d "dist" ]; then
    echo "🧹 Cleaning previous builds..."
    rm -rf dist/
fi

if [ -d "build" ]; then
    rm -rf build/
fi

# Find and remove egg-info directories
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Build the package
echo "📦 Building package..."
uv build

echo "✅ Build completed successfully!"
echo ""
echo "📋 Built packages:"
ls -lh dist/

echo ""
echo "💡 To publish to PyPI:"
echo "   ./scripts/publish.sh"
echo ""
echo "💡 To publish to TestPyPI:"
echo "   ./scripts/publish.sh --test"
