from collections.abc import Callable
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.interfaces.repositories import UnitOfWork
from repositories.sqlalchemy_repositories.raw_excel_repository.repository import SqlAlchemyRawExcelRepository
from repositories.sqlalchemy_repositories.report_repository.repository import SqlAlchemyReportRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        raw_excel_repo_factory: Callable[[AsyncSession], SqlAlchemyRawExcelRepository],
        report_repo_factory: Callable[[AsyncSession], SqlAlchemyReportRepository],
    ) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._raw_excel_repo_factory = raw_excel_repo_factory
        self._report_repo_factory = report_repo_factory

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.raw_excel_repository = self._raw_excel_repo_factory(self._session)
        self.report_repository = self._report_repo_factory(self._session)
        return self

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exception_type is not None:
                await self.rollback()
        finally:
            await self.close()
            self._session = None

    def _session_or_raise(self) -> AsyncSession:
        if self._session is None:
            message = "UnitOfWork is not started. Use: async with uow:"
            raise RuntimeError(message)

        return self._session

    async def rollback(self) -> None:
        await self._session_or_raise().rollback()

    async def close(self) -> None:
        await self._session_or_raise().close()

    async def commit(self) -> None:
        await self._session_or_raise().commit()
