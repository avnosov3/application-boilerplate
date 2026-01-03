from abc import ABC, abstractmethod
from collections.abc import Mapping

from core.models.excel_models import RawExcelModel


class RawExcelRepository(ABC):
    @abstractmethod
    async def create_raw_excel(self, filename: str, data: Mapping) -> RawExcelModel:
        pass
