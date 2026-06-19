"""External collaboration controlled intake routes."""

from fastapi import APIRouter

from app.modules.external_collaboration.schemas import (
    ExternalFeedbackIntakeRequest,
    ExternalFeedbackIntakeResponse,
)
from app.modules.external_collaboration.service import intake_external_feedback

router = APIRouter(
    prefix="/external-collaboration",
    tags=["external-collaboration"],
)


@router.post(
    "/feedback/intake",
    response_model=ExternalFeedbackIntakeResponse,
)
def intake_feedback(
    payload: ExternalFeedbackIntakeRequest,
) -> ExternalFeedbackIntakeResponse:
    return intake_external_feedback(payload)
