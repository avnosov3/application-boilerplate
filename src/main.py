from fastapi import FastAPI

from bootstrap.app_factory import FastApiAppMaker
from bootstrap.container import Container
from bootstrap.logging import setup_logging
from core.config import settings

setup_logging(settings=settings)


def create_fastapi_app() -> FastAPI:
    return FastApiAppMaker(container=Container(), settings=settings).build()
