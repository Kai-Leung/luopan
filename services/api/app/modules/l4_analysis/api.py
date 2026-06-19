"""L4 analysis preview API."""

from fastapi import APIRouter, Query

from app.modules.l4_analysis.schemas import L4AnalysisPreviewResponse
from app.modules.l4_analysis.service import get_l4_analysis_preview

router = APIRouter(prefix="/l4/analysis", tags=["l4-analysis"])


@router.get("/preview", response_model=L4AnalysisPreviewResponse)
def read_analysis_preview(
    fact_id: str = Query(..., min_length=1, description="Existing L2/L3 fact id"),
) -> L4AnalysisPreviewResponse:
    return get_l4_analysis_preview(fact_id)
