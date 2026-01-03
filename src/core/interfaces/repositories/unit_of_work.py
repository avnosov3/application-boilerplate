from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from .raw_excel_repository.repository import RawExcelRepository
from .report_repository.repository import ReportRepository


class UnitOfWork(ABC):
    raw_excel_repository: RawExcelRepository
    report_repository: ReportRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
