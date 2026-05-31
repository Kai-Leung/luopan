"""L7 feedback candidate API."""

from fastapi import APIRouter

from app.modules.l7_feedback.schemas import L7FeedbackRequest, L7FeedbackResponse
from app.modules.l7_feedback.service import create_l7_feedback_candidate

router = APIRouter(prefix="/l7", tags=["l7-feedback"])


@router.post("/feedback", response_model=L7FeedbackResponse)
def create_feedback_candidate(payload: L7FeedbackRequest) -> L7FeedbackResponse:
    return create_l7_feedback_candidate(payload)
