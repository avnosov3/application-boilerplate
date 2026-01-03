python ?= 3.13
port ?= 8000

sync:
	uv sync -p $(python) --frozen
init-app:
	@make sync
	uv run pre-commit install
update-libs:
	uv sync -U
app:
	uv run uvicorn --factory main:create_fastapi_app --port $(port) --app-dir src --reload
lint:
	uv run ruff check --fix
format:
	uv run ruff format
pretty:
	@make lint
	@make format
type-check:
	uv run mypy src
unit:
	uv run pytest tests/unit -vv -s
integration:
	uv run pytest tests/integration -vv -s
e2e:
	uv run pytest tests/e2e -vv -s
test-all:
	@make unit
	@make integration
	@make e2e
pr:
	@make lint
	@make format
	@make type-check
	@make unit
	@make integration
migration:
	uv run alembic revision --autogenerate -m "$(text)" --rev-id $(rev)
apply-migration:
	uv run alembic upgrade head
rollback-migration:
	uv run alembic downgrade $(rev)
