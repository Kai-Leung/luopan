"""L1 候选内容生成路由。"""

from fastapi import APIRouter

from app.modules.l1_candidate.schemas import L1CandidateCreate, L1CandidateResponse
from app.modules.l1_candidate.service import create_candidate

router = APIRouter(prefix="/l1", tags=["l1-candidate"])


@router.post("/candidates", response_model=L1CandidateResponse)
def create_l1_candidate(payload: L1CandidateCreate) -> L1CandidateResponse:
    return create_candidate(payload)
