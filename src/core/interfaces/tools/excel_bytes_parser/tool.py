from abc import ABC, abstractmethod
from collections.abc import Mapping


class ExcelBytesParser(ABC):
    @abstractmethod
    def to_dict(self, content: bytes) -> Mapping:
        pass
