import pytest
from pytest_mock import MockerFixture

from core.interfaces.repositories import ReportRepository, UnitOfWork
from repositories import SqlAlchemyReportRepository


@pytest.fixture
def report_repository(mocker: MockerFixture) -> ReportRepository:
    return SqlAlchemyReportRepository(session=mocker.AsyncMock())


@pytest.fixture
def unit_of_work(mocker: MockerFixture, report_repository: ReportRepository) -> UnitOfWork:
    uow = mocker.MagicMock(spec=UnitOfWork)

    uow.__aenter__ = mocker.AsyncMock(return_value=uow)
    uow.__aexit__ = mocker.AsyncMock(return_value=None)

    uow.commit = mocker.AsyncMock()
    uow.rollback = mocker.AsyncMock()
    uow.close = mocker.AsyncMock()
    uow.report_repository = report_repository

    return uow
