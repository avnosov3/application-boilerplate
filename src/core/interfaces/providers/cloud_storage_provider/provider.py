from abc import ABC, abstractmethod


class CloudStorageProvider(ABC):
    FAILED_TO_GENERATE_LINK = "Failed to generate link"

    @abstractmethod
    async def upload(self, data: bytes, filename: str) -> str:
        """Raises:
        CloudStorageProviderError
        """
