import logging
import pickle
from typing import NamedTuple

from core.interfaces.providers import CloudStorageProvider
from core.interfaces.repositories import UnitOfWork
from core.models.reports import ReportModel


class ReportResult(NamedTuple):
    report_model: ReportModel
    report_cloud_link: str


class ReportService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        cloud_storage_provider: CloudStorageProvider,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._cloud_storage_provider = cloud_storage_provider
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def get_report(self, report_id: int) -> ReportResult:
        async with self._unit_of_work as uow:
            report_model = await uow.report_repository.get_report(report_id=report_id)

        cloud_storage_link = await self._cloud_storage_provider.upload(
            data=pickle.dumps(report_model.rows),
            filename=report_model.filename,
        )
        return ReportResult(report_model=report_model, report_cloud_link=cloud_storage_link)
