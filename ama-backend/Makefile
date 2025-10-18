.PHONY: help install test lint format clean docker-build docker-run docker-stop

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e .

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=csn_server --cov-report=html

lint: ## Run linting
	flake8 csn_server/
	mypy csn_server/

format: ## Format code
	black csn_server/
	isort csn_server/

clean: ## Clean up
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

docker-build: ## Build Docker image
	docker build -t csn_server .

docker-run: ## Run with Docker Compose
	docker-compose up --build

docker-stop: ## Stop Docker Compose
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f csn_server

run: ## Run the server locally
	python -m csn_server.main

run-dev: ## Run the server in development mode
	uvicorn csn_server.main:app --reload --host 0.0.0.0 --port 8000

setup: ## Initial setup
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "source venv/bin/activate  # On Unix/macOS"
	@echo "venv\\Scripts\\activate     # On Windows"
	@echo "Then run: make install" 