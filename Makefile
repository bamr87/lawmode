.PHONY: install test lint format clean docker-build docker-run help

help:
	@echo "LawMode.ai - Development Commands"
	@echo ""
	@echo "  make install      - Install LawMode and dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run LawMode in Docker"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check lawmode/ tests/
	mypy lawmode/

format:
	ruff format lawmode/ tests/
	black lawmode/ tests/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t lawmode:latest .

docker-run:
	docker-compose up

