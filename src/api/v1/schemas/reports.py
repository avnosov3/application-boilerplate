from api.base import ForbidSchema
from core.models.reports import ReportModel


class ReportOutSchema(ForbidSchema):
    id: int
    report_cloud_link: str
    rows: dict
    filename: str
    table_name: str

    @classmethod
    def from_model(cls, report_model: ReportModel, report_cloud_link: str) -> "ReportOutSchema":
        return ReportOutSchema(
            rows=report_model.rows,
            filename=report_model.filename,
            table_name=report_model.table_name,
            id=report_model.id,
            report_cloud_link=report_cloud_link,
        )
