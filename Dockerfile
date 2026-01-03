FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

WORKDIR app/

COPY pyproject.toml uv.lock ./

RUN uv sync -p 3.13 --frozen --no-dev

COPY src/ ./src/

CMD /app/.venv/bin/uvicorn \
    --factory main:create_app \
    --port ${INNER_PORT:-8000} \
    --host ${HOST:-0.0.0.0} \
    --app-dir src
