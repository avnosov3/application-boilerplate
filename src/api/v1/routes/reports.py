from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.v1.schemas import ReportOutSchema
from bootstrap.container import Container
from services import ReportService

router = APIRouter()


@router.get("/{report_id}")
@inject
async def get_report(
    report_id: int,
    report_service: Annotated[ReportService, Depends(Provide[Container.report_service])],
) -> ReportOutSchema:
    result = await report_service.get_report(report_id=report_id)
    return ReportOutSchema.from_model(report_model=result.report_model, report_cloud_link=result.report_cloud_link)
