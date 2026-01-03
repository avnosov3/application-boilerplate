from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture

from bootstrap.app_factory import get_successful_response


@pytest.mark.asyncio
async def test_app_success(async_client: AsyncClient) -> None:
    response = await async_client.get("/healthcheck")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == get_successful_response()


@pytest.mark.asyncio
async def test_app_if_exception_raised(fastapi_app: FastAPI, mocker: MockerFixture) -> None:
    mocker.patch("bootstrap.app_factory.get_successful_response", side_effect=Exception("error"))
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app, raise_app_exceptions=False),
        base_url="http://test",
    ) as client:
        response = await client.get("/healthcheck")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {"message": "Something went wrong"}
