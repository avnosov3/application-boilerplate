import logging
import pickle
from typing import NamedTuple

from core.interfaces.providers import CloudStorageProvider
from core.interfaces.repositories import UnitOfWork
from core.interfaces.tools import ExcelBytesParser, ReportGenerator
from core.models.reports import ReportModel


class ProcessedExcelResult(NamedTuple):
    report_model: ReportModel
    report_cloud_link: str


class ExcelProcessingService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        excel_bytes_parser: ExcelBytesParser,
        cloud_storage_provider: CloudStorageProvider,
        report_generator: ReportGenerator,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._excel_bytes_parser = excel_bytes_parser
        self._cloud_storage_provider = cloud_storage_provider
        self._report_generator = report_generator
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def process_excel(self, filename: str, content: bytes) -> ProcessedExcelResult:
        excel_dict_representation = self._excel_bytes_parser.to_dict(content=content)
        async with self._unit_of_work as uow:
            raw_excel_model = await uow.raw_excel_repository.create_raw_excel(
                filename=filename,
                data=excel_dict_representation,
            )
            raw_report_model = self._report_generator.generate_report(raw_excel_model=raw_excel_model)
            report_model = await uow.report_repository.create_report(raw_report_model=raw_report_model)
            await uow.commit()

        cloud_storage_link = await self._cloud_storage_provider.upload(
            data=pickle.dumps(report_model.rows),
            filename=report_model.filename,
        )
        return ProcessedExcelResult(report_model=report_model, report_cloud_link=cloud_storage_link)
