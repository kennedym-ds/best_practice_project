.PHONY: help install install-dev test test-verbose coverage lint format type-check security docs clean build pre-commit-install

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package and dependencies
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev,docs,test]"

test:  ## Run tests
	pytest tests/

test-verbose:  ## Run tests with verbose output
	pytest -v tests/

coverage:  ## Run tests with coverage report
	pytest --cov=src/data_analysis --cov-report=term-missing --cov-report=html tests/

lint:  ## Run all linters (black check, isort check, flake8)
	black --check --diff src/ tests/
	isort --check-only --diff src/ tests/
	flake8 src/ tests/

format:  ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

type-check:  ## Run type checker (mypy)
	mypy src/data_analysis/

security:  ## Run security checks (bandit and safety)
	bandit -r src/
	safety check

docs:  ## Build documentation
	cd docs && make html

docs-serve:  ## Build and serve documentation locally
	cd docs && make html && python -m http.server --directory _build/html 8000

clean:  ## Clean up generated files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

pre-commit-install:  ## Install pre-commit hooks
	pre-commit install

pre-commit-run:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

venv:  ## Create virtual environment
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  Windows: .\\venv\\Scripts\\activate"
	@echo "  Unix/Mac: source venv/bin/activate"

all: format lint type-check test  ## Run format, lint, type-check, and test
