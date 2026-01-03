from http import HTTPStatus

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_mock import MockerFixture

from core.base.exceptions import ObjectNotFoundError
from services import ReportService


@pytest.mark.asyncio
async def test_get_report_if_report_not_found(
    fastapi_app: FastAPI,
    async_client: AsyncClient,
    report_service: ReportService,
    mocker: MockerFixture,
) -> None:
    report_service._unit_of_work.report_repository.get_report = mocker.AsyncMock(side_effect=ObjectNotFoundError)
    with fastapi_app.container.report_service.override(report_service):
        response = await async_client.get("/api/v1/reports/22")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "message" in response.json()

    report_service._unit_of_work.report_repository.get_report.assert_awaited_once()
