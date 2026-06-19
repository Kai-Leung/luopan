"""L3 正式事实只读视图 Schema。"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel


class L3FactViewResponse(BaseModel):
    fact_id: str
    fact_type: str
    fact_payload: Dict[str, Any]
    fact_status: Literal["active_fact"]
    created_at: datetime


class L3FactListItem(BaseModel):
    fact_id: str
    fact_type: str
    fact_payload_summary: str
    source_type: str
    fact_status: Literal["active_fact"]
    created_at: datetime


class L3FactListQueryParams(BaseModel):
    fact_type: Optional[str] = None
    keyword: Optional[str] = None
    limit: int = 20
    offset: int = 0


class L3FactListResponse(BaseModel):
    items: List[L3FactListItem]
    total: int
