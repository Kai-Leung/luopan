"""S3 minimal source trace summary service."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.modules.s3_audit_trace.schemas import S3TraceEvent, S3TraceSummaryResponse


def get_s3_trace_summary(
    *,
    source_fact_id: str | None = None,
    trace_ref: str | None = None,
) -> S3TraceSummaryResponse:
    if not source_fact_id and not trace_ref:
        raise HTTPException(status_code=400, detail="source_fact_id or trace_ref is required")

    resolved_trace_ref = trace_ref or f"trace_{uuid4().hex}"
    events = [
        S3TraceEvent(
            trace_ref=resolved_trace_ref,
            source_fact_id=source_fact_id,
            created_at=datetime.now(timezone.utc),
            source_stage="l2_l3_fact",
            target_stage="l4_l7_governance_summary",
            action_type="trace_summary",
            readonly=True,
            no_write_l2=True,
        )
    ]
    source_label = source_fact_id or resolved_trace_ref
    return S3TraceSummaryResponse(
        trace_ref=resolved_trace_ref,
        source_fact_id=source_fact_id,
        chain_summary=f"最小来源追溯摘要：{source_label} 仅读取来源引用，不写入 L2。",
        events=events,
        no_write_l2=True,
    )
