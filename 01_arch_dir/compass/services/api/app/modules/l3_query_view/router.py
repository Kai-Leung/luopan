"""L3 正式事实只读视图路由。"""

from typing import Optional

from fastapi import APIRouter, Query

from app.modules.l3_query_view.schemas import L3FactListResponse, L3FactViewResponse
from app.modules.l3_query_view.service import get_l3_fact_view, list_l3_facts

router = APIRouter(prefix="/l3/facts", tags=["l3-facts"])


@router.get("", response_model=L3FactListResponse)
def list_facts(
    fact_type: Optional[str] = Query(None, description="Filter by fact type"),
    keyword: Optional[str] = Query(None, description="Search keyword in fact_payload"),
    limit: int = Query(20, ge=1, le=200, description="Max items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
) -> L3FactListResponse:
    """List L3 facts with optional filtering and pagination. Read-only."""
    return list_l3_facts(fact_type=fact_type, keyword=keyword, limit=limit, offset=offset)


@router.get("/{fact_id}", response_model=L3FactViewResponse)
def read_fact(fact_id: str) -> L3FactViewResponse:
    return get_l3_fact_view(fact_id)
