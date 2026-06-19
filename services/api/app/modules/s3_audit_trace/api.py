"""S3 minimal trace summary API."""

from typing import Optional

from fastapi import APIRouter, Query

from app.modules.s3_audit_trace.schemas import S3TraceSummaryResponse
from app.modules.s3_audit_trace.service import get_s3_trace_summary

router = APIRouter(prefix="/s3/trace", tags=["s3-trace"])


@router.get("/summary", response_model=S3TraceSummaryResponse)
def read_trace_summary(
    source_fact_id: Optional[str] = Query(None),
    trace_ref: Optional[str] = Query(None),
) -> S3TraceSummaryResponse:
    return get_s3_trace_summary(source_fact_id=source_fact_id, trace_ref=trace_ref)
