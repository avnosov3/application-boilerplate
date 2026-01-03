import pytest

from core.interfaces.providers import CloudStorageProvider
from core.interfaces.repositories import UnitOfWork
from services import ReportService


@pytest.fixture
def report_service(unit_of_work: UnitOfWork, azure_cloud_storage_provider: CloudStorageProvider) -> ReportService:
    return ReportService(
        unit_of_work=unit_of_work,
        cloud_storage_provider=azure_cloud_storage_provider,
    )
