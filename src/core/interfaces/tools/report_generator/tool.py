from abc import ABC, abstractmethod

from core.models.excel_models import RawExcelModel
from core.models.reports import RawReportModel


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, raw_excel_model: RawExcelModel) -> RawReportModel:
        pass
