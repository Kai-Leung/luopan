"""S2 横向治理内存模型。

本文件只定义最小治理结果结构；不使用 ORM，不写数据库。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class GovernanceRecord:
    governance_id: str
    candidate_id: str
    created_at: datetime
    governance_status: str
    missing_fields: List[str]
    risk_level: str
    question_prompts: List[str]
    validation_hints: List[str]
    risk_hints: List[str]
    required_permission: Optional[str]
    checked_payload: Dict[str, Any]
