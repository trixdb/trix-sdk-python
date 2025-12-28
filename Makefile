.PHONY: help install install-dev test test-cov lint format type-check clean build publish

help:
	@echo "Trix Python SDK - Available Commands"
	@echo "======================================"
	@echo "install       - Install package"
	@echo "install-dev   - Install package with dev dependencies"
	@echo "test          - Run tests"
	@echo "test-cov      - Run tests with coverage report"
	@echo "lint          - Run linter (ruff)"
	@echo "format        - Format code with black"
	@echo "type-check    - Run type checker (mypy)"
	@echo "clean         - Remove build artifacts"
	@echo "build         - Build distribution packages"
	@echo "publish       - Publish to PyPI"
	@echo "quality       - Run all quality checks (format, lint, type-check, test)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=trix --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/

format:
	black src/ tests/ examples/

type-check:
	mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

quality: format lint type-check test
	@echo "✓ All quality checks passed!"
