.PHONY: help install build publish publish-test clean test

help:
	@echo "Hezor Common - Build & Publish Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install        - Install dependencies using uv"
	@echo "  make build          - Build the package"
	@echo "  make publish-test   - Publish to TestPyPI"
	@echo "  make publish        - Publish to PyPI (production)"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make test           - Run tests (if any)"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	uv sync

build:
	@echo "🔨 Building package..."
	@./scripts/build.sh

publish-test:
	@echo "🚀 Publishing to TestPyPI..."
	@./scripts/publish.sh --test

publish:
	@echo "🚀 Publishing to PyPI..."
	@./scripts/publish.sh

clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf dist/ build/ *.egg-info
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete"

test:
	@echo "🧪 Running tests..."
	@uv run pytest
