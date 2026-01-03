from core.interfaces.tools import ReportGenerator
from core.models.excel_models import RawExcelModel
from core.models.reports import RawReportModel


class CustomReportGenerator(ReportGenerator):
    def generate_report(self, raw_excel_model: RawExcelModel) -> RawReportModel:
        return RawReportModel(
            filename=raw_excel_model.filename,
            rows={"ping": "pong"},
            table_name=raw_excel_model.filename,
        )
