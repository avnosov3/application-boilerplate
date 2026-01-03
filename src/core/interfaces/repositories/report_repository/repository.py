from abc import ABC, abstractmethod

from core.models.reports import RawReportModel, ReportModel


class ReportRepository(ABC):
    REPORT_NOT_FOUND_MESSAGE = "Report not found"

    @abstractmethod
    async def create_report(self, raw_report_model: RawReportModel) -> ReportModel:
        pass

    @abstractmethod
    async def get_report(self, report_id: int) -> ReportModel:
        """Raises:
        ObjectNotFoundError
        """
