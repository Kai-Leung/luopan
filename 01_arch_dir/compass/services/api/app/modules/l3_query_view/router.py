"""L3 正式事实只读视图路由。"""

from fastapi import APIRouter

from app.modules.l3_query_view.schemas import L3FactViewResponse
from app.modules.l3_query_view.service import get_l3_fact_view

router = APIRouter(prefix="/l3/facts", tags=["l3-facts"])


@router.get("/{fact_id}", response_model=L3FactViewResponse)
def read_fact(fact_id: str) -> L3FactViewResponse:
    return get_l3_fact_view(fact_id)
