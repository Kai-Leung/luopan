"""人工确认层最小 review 路由。"""

from fastapi import APIRouter

from app.modules.s2_governance_gate.confirmation.schemas import (
    ManualConfirmationReviewRequest,
    ManualConfirmationReviewResponse,
    PendingConfirmationCreateRequest,
    PendingConfirmationItem,
    PendingConfirmationListResponse,
)
from app.modules.s2_governance_gate.confirmation.service import (
    create_pending_confirmation,
    list_pending_confirmations,
    review_confirmation,
)

router = APIRouter(prefix="/manual-confirmation", tags=["manual-confirmation"])


@router.post("/review", response_model=ManualConfirmationReviewResponse)
def review(
    payload: ManualConfirmationReviewRequest,
) -> ManualConfirmationReviewResponse:
    return review_confirmation(payload)


@router.post("/pending", response_model=PendingConfirmationItem)
def create_pending(
    payload: PendingConfirmationCreateRequest,
) -> PendingConfirmationItem:
    return create_pending_confirmation(payload)


@router.get("/pending", response_model=PendingConfirmationListResponse)
def list_pending() -> PendingConfirmationListResponse:
    return list_pending_confirmations()
