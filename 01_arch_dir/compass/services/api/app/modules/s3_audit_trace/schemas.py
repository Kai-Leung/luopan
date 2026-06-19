"""S3 minimal source trace schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class S3TraceEvent(BaseModel):
    trace_ref: str
    source_fact_id: Optional[str] = None
    raw_input_id: Optional[str] = None
    candidate_id: Optional[str] = None
    governance_id: Optional[str] = None
    review_id: Optional[str] = None
    analysis_id: Optional[str] = None
    recommendation_id: Optional[str] = None
    execution_response_id: Optional[str] = None
    feedback_id: Optional[str] = None
    created_at: datetime
    source_stage: str
    target_stage: str
    action_type: str
    actor_id: str
    organization_id: str
    readonly: bool = True
    no_write_l2: bool = True


class S3TraceSummaryRequest(BaseModel):
    source_fact_id: Optional[str] = None
    trace_ref: Optional[str] = None


class S3TraceSummaryResponse(BaseModel):
    trace_ref: str
    source_fact_id: Optional[str] = None
    chain_summary: str
    events: List[S3TraceEvent]
    no_write_l2: bool = True
