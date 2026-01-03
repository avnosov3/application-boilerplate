import logging
from collections.abc import Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from core.interfaces.repositories import RawExcelRepository
from core.models.excel_models import RawExcelModel
from repositories.sqlalchemy_repositories.orm_models import RawExcelOrmModel


class SqlAlchemyRawExcelRepository(RawExcelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def create_raw_excel(self, filename: str, data: Mapping) -> RawExcelModel:
        orm_model = RawExcelOrmModel(filename=filename, data=data)
        self._session.add(orm_model)
        await self._session.flush()
        return RawExcelModel.model_validate(orm_model)
