# Makefile for Agentic Labs - Developer (Contributor) Operations
# This Makefile contains targets for common developer operations.
# For user operations (running labs), see the lab README files.

.PHONY: help setup upgrade clean lint format check

help: ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Reset and setup development environment
	@echo "Setting up development environment..."
	rm -rf .venv
	uv sync --all-groups
	@echo "Development environment ready!"

upgrade: ## Upgrade dependencies to latest versions
	@echo "Upgrading dependencies..."
	uv sync --upgrade --all-groups
	@echo "Dependencies upgraded!"

clean: ## Remove temporary and build artifacts
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/
	@echo "Cleanup complete!"

lint: ## Run linting checks
	@echo "Running linting checks..."
	uv run ruff check .

format: ## Format code automatically
	@echo "Formatting code..."
	uv run ruff format .
	uv run ruff check --fix .

check: lint ## Run all checks (lint + format check)
	@echo "Running format check..."
	uv run ruff format --check .
	@echo "All checks passed!"
