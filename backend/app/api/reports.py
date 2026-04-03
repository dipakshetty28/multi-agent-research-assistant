from fastapi import APIRouter

from app.models.schemas import ReportRequest, ReportResponse
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(request: ReportRequest) -> ReportResponse:
    return report_service.generate_report(request)
