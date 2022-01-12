POETRY=poetry run

# Starts the development server
.PHONY: run
run:
	${POETRY} uvicorn demo_api.app:app

# Lint using black
.PHONY: format
format:
	${POETRY} autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place demo_api tests
	${POETRY} black --line-length=80 demo_api tests
	${POETRY} isort demo_api tests