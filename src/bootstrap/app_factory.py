from collections.abc import AsyncGenerator, Mapping
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.v1.exception_handlers import build_exception_responses, build_exceptions
from api.v1.router import router as v1_router
from bootstrap.container import Container
from core.config import Settings


def get_successful_response() -> Mapping:
    return {"response": "success"}


class FastApiAppMaker:
    def __init__(self, container: Container, settings: Settings) -> None:
        self._container: Container = container
        self._settings = settings

    def build(self) -> FastAPI:
        @asynccontextmanager
        async def lifespan(_app: FastAPI) -> AsyncGenerator[Any, Any]:
            init_resources = self._container.init_resources()
            if init_resources is None:
                message = "init resources failed"
                raise NotImplementedError(message)

            await init_resources

            yield

            shutdown_resources = self._container.shutdown_resources()
            if shutdown_resources is None:
                message = "shutdown resources failed"
                raise NotImplementedError(message)

            await shutdown_resources

        docs_url = "/api/v1/docs"
        app = FastAPI(
            title="xlsx-processor",
            description="xlsx-processor",
            redoc_url="/api/v1/redoc" if self._settings.IS_DEV_ENV else None,
            docs_url=docs_url if self._settings.IS_DEV_ENV else None,
            exception_handlers=build_exceptions(),
            responses=build_exception_responses(),
            lifespan=lifespan,
        )

        @app.get("/")
        async def index() -> Any:  # noqa: ANN401
            if self._settings.IS_DEV_ENV:
                return RedirectResponse(docs_url)
            return 200

        @app.get("/healthcheck")
        async def healthcheck() -> Mapping:
            return get_successful_response()

        app.include_router(v1_router, prefix="/api/v1")
        app.container = self._container  # type: ignore[attr-defined]

        return app
