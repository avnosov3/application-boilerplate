from http import HTTPStatus
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from api.v1.schemas import ReportOutSchema
from bootstrap.container import Container
from services import ExcelProcessingService

router = APIRouter()


@router.post("/upload")
@inject
async def upload_excel(
    file: UploadFile,
    excel_processing_service: Annotated[ExcelProcessingService, Depends(Provide[Container.excel_processing_service])],
) -> ReportOutSchema:
    if file.filename is None:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_CONTENT, detail="File must have filename")

    result = await excel_processing_service.process_excel(filename=file.filename, content=await file.read())
    return ReportOutSchema.from_model(report_model=result.report_model, report_cloud_link=result.report_cloud_link)
