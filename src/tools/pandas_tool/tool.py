import logging
from collections.abc import Mapping

from core.interfaces.tools import ExcelBytesParser


class PandasTool(ExcelBytesParser):
    def __init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def to_dict(self, content: bytes) -> Mapping:
        return {"ping": "pong"}
