"""L2 正式事实入链最小接口 Schema。

L2 是第一处允许形成正式事实的层级；请求必须携带完整前置链路引用。
"""

from typing import Any, Dict, Literal

from pydantic import BaseModel, field_validator

from app.modules.standard_governance.rules.fact_record_types import is_known_fact_record_type

ReviewStatus = Literal["confirmed_candidate"]
FactStatus = Literal["active_fact"]


class L2FactCreateRequest(BaseModel):
    raw_input_id: str
    candidate_id: str
    governance_id: str
    review_id: str
    review_status: str
    fact_type: str
    fact_payload: Dict[str, Any]

    @field_validator("fact_type")
    @classmethod
    def validate_fact_type(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("fact_type is required")
        normalized_value = value.strip()
        if not is_known_fact_record_type(normalized_value):
            raise ValueError("fact_type is not a known fact record type")
        return normalized_value


class L2FactResponse(BaseModel):
    fact_id: str
    fact_status: FactStatus
    fact_payload: Dict[str, Any]
    raw_input_id: str
    candidate_id: str
    governance_id: str
    review_id: str
    message: str
