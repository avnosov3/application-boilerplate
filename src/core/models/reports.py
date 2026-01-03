from pydantic import BaseModel


class RawReportModel(BaseModel):
    rows: dict
    filename: str
    table_name: str


class ReportModel(RawReportModel):
    id: int
