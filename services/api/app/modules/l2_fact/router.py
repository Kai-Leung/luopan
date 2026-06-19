"""L2 正式事实入链最小路由。"""

from fastapi import APIRouter

from app.modules.l2_fact.schemas import L2FactCreateRequest, L2FactResponse
from app.modules.l2_fact.service import create_l2_fact

router = APIRouter(prefix="/l2/source-of-truth", tags=["l2-source-of-truth"])


@router.post("/facts", response_model=L2FactResponse)
def create_fact(payload: L2FactCreateRequest) -> L2FactResponse:
    return create_l2_fact(payload)
