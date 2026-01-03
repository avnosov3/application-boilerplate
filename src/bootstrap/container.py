import logging
from collections.abc import AsyncGenerator
from typing import Any

from dependency_injector import containers, providers
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings
from providers import AzureCloudStorageProvider
from repositories import SqlAlchemyRawExcelRepository, SqlAlchemyReportRepository, SqlAlchemyUnitOfWork
from services import ExcelProcessingService, ReportService
from tools import CustomReportGenerator, PandasTool

logger = logging.getLogger(f"{__name__}")


async def init_generic_httpx_client() -> AsyncGenerator[Any, AsyncClient]:
    client = AsyncClient()
    logger.info("Created HttpX client")
    yield client
    await client.aclose()
    logger.info("Closed HttpX client")


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.routes.excel_processing",
            "api.v1.routes.reports",
        ]
    )

    config = providers.Configuration()

    open_ai_client = providers.Resource(
        init_generic_httpx_client,
    )

    # db
    sqlalchemy_engine = providers.Singleton(
        create_async_engine,
        url=str(settings.DATABASE_URL),
        echo=settings.DEBUG_QUERIES,
    )

    sqlalchemy_session_factory = providers.Singleton(
        async_sessionmaker,
        bind=sqlalchemy_engine,
        expire_on_commit=False,
    )

    sqlalchemy_unit_of_work = providers.Factory(
        SqlAlchemyUnitOfWork,
        session_factory=sqlalchemy_session_factory,
        raw_excel_repo_factory=SqlAlchemyRawExcelRepository,
        report_repo_factory=SqlAlchemyReportRepository,
    )

    # providers
    azure_cloud_storage_provider = providers.Singleton(
        AzureCloudStorageProvider,
    )

    # tools
    pandas_tool = providers.Singleton(
        PandasTool,
    )
    custom_report_generator = providers.Factory(
        CustomReportGenerator,
    )

    # services
    excel_processing_service = providers.Factory(
        ExcelProcessingService,
        unit_of_work=sqlalchemy_unit_of_work,
        excel_bytes_parser=pandas_tool,
        report_generator=custom_report_generator,
        cloud_storage_provider=azure_cloud_storage_provider,
    )
    report_service = providers.Factory(
        ReportService,
        unit_of_work=sqlalchemy_unit_of_work,
        cloud_storage_provider=azure_cloud_storage_provider,
    )
