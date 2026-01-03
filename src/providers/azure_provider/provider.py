import asyncio
import logging

from core.interfaces.providers import CloudStorageProvider


class AzureCloudStorageProvider(CloudStorageProvider):
    def __init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def upload(self, data: bytes, filename: str) -> str:
        await asyncio.sleep(0.2)
        return "unique_link"
