from fastapi import APIRouter

from api.v1.routes.excel_processing import router as excel_processing_router
from api.v1.routes.reports import router as reports_router

router = APIRouter()

router.include_router(excel_processing_router, prefix="/excel-processing", tags=["excel_processing"])
router.include_router(reports_router, prefix="/reports", tags=["reports"])
