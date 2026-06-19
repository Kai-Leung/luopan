"""人工确认层内存模型。

本文件只定义人工 review 记录结构；不使用 ORM，不写数据库。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ManualConfirmationRecord:
    review_id: str
    governance_id: str
    created_at: datetime
    governance_status: str
    review_action: str
    review_status: str
    policy_decision: str
    project_asset: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class PendingConfirmationRecord:
    pending_id: str
    input_session_id: str
    raw_input_id: str
    candidate_id: str
    governance_id: str
    governance_status: str
    fact_type: str
    fact_payload: Dict[str, Any]
    display_text: str
    required_permission: Optional[str]
    created_at: datetime
