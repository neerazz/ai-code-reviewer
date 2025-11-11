.PHONY: help install dev-install test lint format clean docker-build docker-up docker-down migrate

help:
	@echo "AI Code Reviewer - Available Commands"
	@echo "====================================="
	@echo "install          Install production dependencies"
	@echo "dev-install      Install development dependencies"
	@echo "test             Run tests"
	@echo "test-cov         Run tests with coverage"
	@echo "lint             Run linters"
	@echo "format           Format code with black and isort"
	@echo "clean            Remove cache and temporary files"
	@echo "docker-build     Build Docker images"
	@echo "docker-up        Start Docker containers"
	@echo "docker-down      Stop Docker containers"
	@echo "migrate          Run database migrations"
	@echo "run              Run development server"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=backend --cov-report=html --cov-report=term

lint:
	flake8 backend/
	mypy backend/
	bandit -r backend/

format:
	black backend/ config/ tests/
	isort backend/ config/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	alembic upgrade head

run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

setup: dev-install
	cp .env.example .env
	@echo "Please edit .env with your configuration"
