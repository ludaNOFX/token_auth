.PHONY: format lint test check

format:
	poetry run black .
	poetry run ruff --fix .

lint:
	poetry run ruff .

test:
	poetry run pytest

check: lint test
