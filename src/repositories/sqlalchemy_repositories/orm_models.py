from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, func
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.models.excel_models import FILENAME_MAX_LEN
from core.models.reports import RawReportModel, ReportModel

CASCADE = "CASCADE"
ALL_DELETE = "all, delete"
SET_NULL = "SET NULL"


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


class RawExcelOrmModel(BaseModel):
    __tablename__ = "raw_excel"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(FILENAME_MAX_LEN),
        nullable=False,
    )
    data: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSON),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"RawExcelOrmModel(id={self.id} filename={self.filename:.20s})"


class ReportOrmModel(BaseModel):
    __tablename__ = "report"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(FILENAME_MAX_LEN),
        nullable=False,
    )
    data: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSON),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"ReportOrmModel(id={self.id}, filename={self.filename})"

    @classmethod
    def from_model(cls, raw_report_model: RawReportModel) -> "ReportOrmModel":
        return ReportOrmModel(filename=raw_report_model.filename, data=raw_report_model.rows)

    def to_model(self) -> ReportModel:
        return ReportModel(id=self.id, rows=self.data, filename=self.filename, table_name=self.filename)
