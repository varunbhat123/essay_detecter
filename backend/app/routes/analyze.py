from fastapi import APIRouter

from app.models.essay import EssayRequest, EssayResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api", tags=["analysis"])
service = AnalysisService()


@router.post("/analyze", response_model=EssayResponse)
async def analyze_essay(payload: EssayRequest) -> EssayResponse:
    result = await service.analyze(payload.essay)
    return EssayResponse(**result)
