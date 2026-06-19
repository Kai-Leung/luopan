"""L2 正式事实入链内存记录模型。

仅记录已进入 fact_records 的最小事实链路，不承接 L3 视图。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class FactRecordEntry:
    fact_id: str
    raw_input_id: str
    candidate_id: str
    governance_id: str
    review_id: str
    fact_type: str
    fact_payload: Dict[str, Any]
    fact_status: str
    created_at: datetime
