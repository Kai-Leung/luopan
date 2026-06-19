"""L1 候选内容内存模型。

本文件只定义候选内容的内存级数据结构；不使用 ORM，不写数据库。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from app.modules.standard_governance.enums.source_types import SourceType
from app.modules.standard_governance.enums.status_types import CandidateStatus


@dataclass(frozen=True)
class CandidateRecord:
    candidate_id: str
    input_session_id: str
    raw_input_id: str
    created_at: datetime
    source_type: SourceType
    candidate_status: CandidateStatus
    candidate_payload: Dict[str, Any]
