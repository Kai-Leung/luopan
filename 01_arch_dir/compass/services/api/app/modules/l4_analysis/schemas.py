"""L4 analysis preview schemas."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from app.modules.standard_governance.processing import StandardErrorResult


class L4AnalysisPreviewRequest(BaseModel):
    fact_id: str


class L4AnalysisPreviewResponse(BaseModel):
    analysis_id: str
    source_fact_id: str
    trace_ref: Optional[str] = None
    processing_direction: Literal["readonly"]
    analysis_status: Literal["preview"]
    analysis_summary: str
    readonly: Literal[True]
    created_at: datetime
    standard_error: Optional[StandardErrorResult] = None
