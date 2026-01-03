import logging

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.base.exceptions import ObjectNotFoundError
from core.interfaces.repositories import ReportRepository
from core.models.reports import RawReportModel, ReportModel
from repositories.sqlalchemy_repositories.orm_models import ReportOrmModel


class SqlAlchemyReportRepository(ReportRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def create_report(self, raw_report_model: RawReportModel) -> ReportModel:
        report_orm_model = ReportOrmModel.from_model(raw_report_model=raw_report_model)
        self._session.add(report_orm_model)
        await self._session.flush()
        return report_orm_model.to_model()

    async def get_report(self, report_id: int) -> ReportModel:
        try:
            report_orm_model = await self._session.scalars(select(ReportOrmModel).where(ReportOrmModel.id == report_id))
            return report_orm_model.one().to_model()
        except NoResultFound as error:
            raise ObjectNotFoundError(self.REPORT_NOT_FOUND_MESSAGE) from error
