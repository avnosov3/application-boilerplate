import pytest

from providers.azure_provider.provider import AzureCloudStorageProvider


@pytest.fixture
def azure_cloud_storage_provider() -> AzureCloudStorageProvider:
    return AzureCloudStorageProvider()
