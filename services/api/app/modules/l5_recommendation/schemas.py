"""L5 recommendation draft schemas."""

from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel

from app.modules.standard_governance.processing import StandardErrorResult


class L5RecommendationDraftRequest(BaseModel):
    analysis_id: Optional[str] = None
    source_fact_id: Optional[str] = None
    context_payload: Optional[Dict[str, Any]] = None


class L5RecommendationDraftResponse(BaseModel):
    recommendation_id: str
    recommendation_status: Literal["draft"]
    source_fact_id: Optional[str] = None
    analysis_id: Optional[str] = None
    trace_ref: Optional[str] = None
    processing_direction: Literal["draft"]
    recommendation_summary: str
    auto_executable: Literal[False]
    created_at: datetime
    standard_error: Optional[StandardErrorResult] = None
