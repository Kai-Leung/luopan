"""L0 原始输入内存模型。

本文件只定义内存级数据结构；不使用 ORM，不写数据库。
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from app.modules.standard_governance.enums.source_types import SourceType


@dataclass(frozen=True)
class RawInputRecord:
    raw_input_id: str
    input_session_id: str
    received_at: datetime
    source_type: SourceType
    raw_payload: Dict[str, object]
    status: str = "received_only"
