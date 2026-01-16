.PHONY: help install build publish publish-test clean test bump-patch bump-minor bump-major

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
	@echo "Version Management:"
	@echo "  make bump-patch     - Bump patch version (0.1.0 -> 0.1.1)"
	@echo "  make bump-minor     - Bump minor version (0.1.0 -> 0.2.0)"
	@echo "  make bump-major     - Bump major version (0.1.0 -> 1.0.0)"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	uv sync

build:
	@echo "🔨 Building package..."
	@./scripts/build.sh

publish-test:
	@echo "🚀 Publishing to TestPyPI..."
	@make clean
	@make build
	@./scripts/publish.sh --test

publish:
	@echo "🚀 Publishing to PyPI..."
	@make clean
	@make build
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

bump-patch:
	@echo "⬆️  Bumping patch version..."
	@uv run bump-my-version bump patch

bump-minor:
	@echo "⬆️  Bumping minor version..."
	@uv run bump-my-version bump minor

bump-major:
	@echo "⬆️  Bumping major version..."
	@uv run bump-my-version bump major
