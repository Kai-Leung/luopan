"""S2 横向治理最小校验路由。"""

from fastapi import APIRouter

from app.modules.s2_governance_gate.schemas import (
    S2GovernanceCheckRequest,
    S2GovernanceCheckResponse,
)
from app.modules.s2_governance_gate.service import check_candidate_governance

router = APIRouter(prefix="/s2/governance", tags=["s2-governance"])


@router.post("/check", response_model=S2GovernanceCheckResponse)
def check_governance(
    payload: S2GovernanceCheckRequest,
) -> S2GovernanceCheckResponse:
    return check_candidate_governance(payload)
