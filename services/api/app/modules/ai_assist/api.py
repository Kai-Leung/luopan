"""AI assist controlled intake routes."""

from fastapi import APIRouter

from app.modules.ai_assist.schemas import (
    AiAssistCandidateIntakeRequest,
    AiAssistCandidateIntakeResponse,
)
from app.modules.ai_assist.service import intake_ai_assist_candidate

router = APIRouter(prefix="/ai-assist", tags=["ai-assist"])


@router.post(
    "/candidates/intake",
    response_model=AiAssistCandidateIntakeResponse,
)
def intake_candidate(
    payload: AiAssistCandidateIntakeRequest,
) -> AiAssistCandidateIntakeResponse:
    return intake_ai_assist_candidate(payload)
