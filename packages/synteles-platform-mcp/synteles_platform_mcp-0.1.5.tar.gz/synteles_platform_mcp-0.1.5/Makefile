.PHONY: install test lint typed security depcheck unusedcode format check clean all

install:
	uv sync 

test:
	uv run python -m unittest discover tests -v

lint:
	uv run python -m ruff check synteles_platform_mcp/ --exclude tests

typed:
	uv run python -m mypy synteles_platform_mcp/ --exclude tests

security:
	uv run python -m bandit -rq synteles_platform_mcp/ --exclude tests

depcheck:
	uv run python -m deptry synteles_platform_mcp/ --exclude tests

unusedcode:
	uv run python -m vulture synteles_platform_mcp/ --exclude tests || true

format:
	uv run ruff format synteles_platform_mcp/ tests/

check: lint typed security depcheck unusedcode

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

all: install test lint