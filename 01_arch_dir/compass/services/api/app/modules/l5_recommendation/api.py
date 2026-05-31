"""L5 recommendation draft API."""

from fastapi import APIRouter

from app.modules.l5_recommendation.schemas import (
    L5RecommendationDraftRequest,
    L5RecommendationDraftResponse,
)
from app.modules.l5_recommendation.service import create_l5_recommendation_draft

router = APIRouter(prefix="/l5/recommendations", tags=["l5-recommendations"])


@router.post("/draft", response_model=L5RecommendationDraftResponse)
def create_recommendation_draft(
    payload: L5RecommendationDraftRequest,
) -> L5RecommendationDraftResponse:
    return create_l5_recommendation_draft(payload)
