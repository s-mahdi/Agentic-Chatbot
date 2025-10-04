.PHONY: help dev start lint format typecheck test clean install

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Start the chatbot in development mode
	@echo "Starting agentic chatbot..."
	uv run python main.py

start: ## Start the chatbot
	@echo "Starting agentic chatbot..."
	uv run python main.py

lint: ## Run linting
	uv run ruff check src/

format: ## Format code
	uv run ruff format src/

typecheck: ## Run type checking
	uv run mypy src/ --ignore-missing-imports

test: ## Run tests
	uv run pytest

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
