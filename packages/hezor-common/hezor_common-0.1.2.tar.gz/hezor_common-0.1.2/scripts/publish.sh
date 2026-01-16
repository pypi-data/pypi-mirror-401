#!/bin/bash
# Publish script for hezor-common package

set -e

TEST_PYPI=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_PYPI=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--test]"
            exit 1
            ;;
    esac
done

# Check if dist directory exists
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "❌ No build found. Please run ./scripts/build.sh first"
    exit 1
fi

# Install twine if not available
if ! uv pip list | grep -q twine; then
    echo "📦 Installing twine..."
    uv pip install twine
fi

# Publish
if [ "$TEST_PYPI" = true ]; then
    echo "🚀 Publishing to TestPyPI..."
    echo ""
    echo "📝 You will need TestPyPI credentials."
    echo "   Sign up at: https://test.pypi.org/account/register/"
    echo ""
    uv run twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Published to TestPyPI!"
    echo "🔗 View at: https://test.pypi.org/project/hezor-common/"
    echo ""
    echo "💡 To install from TestPyPI:"
    echo "   pip install --index-url https://test.pypi.org/simple/ hezor-common"
else
    echo "🚀 Publishing to PyPI..."
    echo ""
    echo "📝 You will need PyPI credentials."
    echo "   Sign up at: https://pypi.org/account/register/"
    echo ""
    echo "⚠️  This will publish to the REAL PyPI!"
    read -p "Are you sure you want to continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 1
    fi
    
    uv run twine upload dist/*
    echo ""
    echo "✅ Published to PyPI!"
    echo "🔗 View at: https://pypi.org/project/hezor-common/"
    echo ""
    echo "💡 To install:"
    echo "   pip install hezor-common"
fi
