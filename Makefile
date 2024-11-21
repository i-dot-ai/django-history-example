.PHONY: help
help:     ## Show this help.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run the tests
	poetry run pytest tests/

.PHONY: check-python-code
check-python-code: ## Check Python code - linting and mypy
	poetry run ruff check --select I .
	poetry run ruff check .
	poetry run mypy . --ignore-missing-imports

.PHONY: format-python-code
format-python-code: ## Format Python code including sorting imports
	poetry run ruff check --select I . --fix
	poetry run ruff check . --fix
	poetry run ruff format .