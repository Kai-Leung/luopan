"""L3 正式事实只读视图 Schema。"""

from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel


class L3FactViewResponse(BaseModel):
    fact_id: str
    fact_type: str
    fact_payload: Dict[str, Any]
    fact_status: Literal["active_fact"]
    created_at: datetime
