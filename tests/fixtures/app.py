from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from main import create_fastapi_app


@pytest.fixture
def fastapi_app() -> FastAPI:
    return create_fastapi_app()


@pytest_asyncio.fixture
async def async_client(fastapi_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test",
    ) as client:
        yield client
