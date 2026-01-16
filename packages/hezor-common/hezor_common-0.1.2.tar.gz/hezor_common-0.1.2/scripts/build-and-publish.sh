#!/bin/bash
# Complete build and publish script for hezor-common package

set -e

echo "🔄 Building and publishing hezor-common..."
echo ""

# Build
./scripts/build.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Publish to TestPyPI by default for safety
./scripts/publish.sh --test
