"""L6 execution response schemas."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from app.modules.standard_governance.processing import StandardErrorResult


class L6ExecutionResponseRequest(BaseModel):
    recommendation_id: Optional[str] = None
    source_fact_id: Optional[str] = None
    execution_note: str
    execution_status: str


class L6ExecutionResponseResponse(BaseModel):
    execution_response_id: str
    execution_status: str
    recommendation_id: Optional[str] = None
    source_fact_id: Optional[str] = None
    trace_ref: Optional[str] = None
    processing_direction: Literal["response"]
    execution_note: str
    creates_fact: Literal[False]
    created_at: datetime
    standard_error: Optional[StandardErrorResult] = None
