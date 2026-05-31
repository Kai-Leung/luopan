"""L7 feedback candidate schemas."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from app.modules.standard_governance.processing import StandardErrorResult


class L7FeedbackRequest(BaseModel):
    execution_response_id: Optional[str] = None
    source_fact_id: Optional[str] = None
    feedback_note: str
    feedback_type: Optional[str] = None


class L7FeedbackResponse(BaseModel):
    feedback_id: str
    feedback_status: Literal["candidate"]
    execution_response_id: Optional[str] = None
    source_fact_id: Optional[str] = None
    trace_ref: Optional[str] = None
    processing_direction: Literal["candidate"]
    feedback_note: str
    feedback_type: Optional[str] = None
    returns_to_candidate_flow: Literal[True]
    created_at: datetime
    standard_error: Optional[StandardErrorResult] = None
