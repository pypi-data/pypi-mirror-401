# CCFraud Detector - Build, Lint, and Test Commands
# Authors: Ekta Bhatia (Lead Developer), Aditya Patange
# License: MIT

.PHONY: all install install-dev build clean lint format typecheck test test-unit test-integration coverage publish help

# Default target
all: lint typecheck test

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Build
build: clean
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Linting and Formatting
lint:
	ruff check ccfraud_detector/ tests/

format:
	ruff format ccfraud_detector/ tests/
	ruff check --fix ccfraud_detector/ tests/

typecheck:
	mypy ccfraud_detector/

# Testing
test: test-unit

test-unit:
	pytest tests/ -v --ignore=tests/test_integration.py -m "not integration"

test-integration:
	pytest tests/ -v -m integration

test-all:
	pytest tests/ -v

coverage:
	pytest tests/ -v --cov=ccfraud_detector --cov-report=html --cov-report=term-missing

# Publishing
publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Help
help:
	@echo "CCFraud Detector - Available Commands"
	@echo "======================================"
	@echo "Authors: Ekta Bhatia (Lead Developer), Aditya Patange"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install package in editable mode"
	@echo "  make install-dev  - Install with development dependencies"
	@echo ""
	@echo "Build:"
	@echo "  make build        - Build distribution packages"
	@echo "  make clean        - Remove build artifacts"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run ruff linter"
	@echo "  make format       - Format code with ruff"
	@echo "  make typecheck    - Run mypy type checking"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run unit tests"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-integration - Run integration tests (requires ANTHROPIC_API_KEY)"
	@echo "  make test-all     - Run all tests"
	@echo "  make coverage     - Run tests with coverage report"
	@echo ""
	@echo "Publishing:"
	@echo "  make publish      - Publish to PyPI"
	@echo "  make publish-test - Publish to TestPyPI"
