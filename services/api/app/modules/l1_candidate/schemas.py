"""L1 候选内容接口 Schema。

只承接 L0 原始输入到候选内容的最小包装，不承接 S2、确认或 L2 字段。
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel

from app.modules.standard_governance.enums.source_types import SourceType
from app.modules.standard_governance.enums.status_types import CandidateStatus


class L1CandidateCreate(BaseModel):
    raw_input_id: str
    input_session_id: Optional[str] = None
    supplement_candidate_id: Optional[str] = None
    raw_payload: Dict[str, Any]
    source_type: SourceType


class L1CandidateItem(BaseModel):
    candidate_id: str
    input_session_id: str
    raw_input_id: str
    candidate_status: CandidateStatus
    candidate_payload: Dict[str, Any]


class L1CandidateResponse(BaseModel):
    candidate_id: str
    input_session_id: str
    raw_input_id: str
    candidate_status: CandidateStatus
    candidate_payload: Dict[str, Any]
    candidates: list[L1CandidateItem]
    message: str
