"""Persistent, read-only L4 analysis preview service."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_analysis_record,
    ensure_minimal_storage_tables,
    get_fact_record,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l4_analysis.schemas import L4AnalysisPreviewResponse
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    get_current_runtime_context,
)
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_READONLY


def get_l4_analysis_preview(fact_id: str) -> L4AnalysisPreviewResponse:
    context = get_current_runtime_context()
    ensure_minimal_storage_tables(include_fact_records=True)
    db = SessionLocal()
    try:
        row = get_fact_record(db, fact_id)
        if row is None:
            raise HTTPException(status_code=404, detail="source fact not found")
        try:
            fact_payload = load_json_field(row.fact_payload)
        except ValueError:
            raise HTTPException(status_code=500, detail="source fact payload is invalid")
        ensure_payload_in_current_scope(fact_payload)

        analysis_id = f"analysis_{uuid4().hex}"
        trace_ref = _fact_trace_ref(fact_payload)
        created_at = datetime.now(timezone.utc)
        summary = _build_preview_summary(row.fact_type, fact_payload)
        create_analysis_record(
            db,
            analysis_id=analysis_id,
            source_fact_id=row.fact_id,
            trace_ref=trace_ref,
            analysis_status="preview",
            analysis_summary=summary,
            organization_id=context.organization_id,
            created_at=created_at,
        )
    finally:
        db.close()

    record_trace_event(
        trace_ref=trace_ref,
        source_fact_id=fact_id,
        analysis_id=analysis_id,
        source_stage="l3_query_view",
        target_stage="l4_analysis",
        action_type="analysis_preview_created",
    )
    return L4AnalysisPreviewResponse(
        analysis_id=analysis_id,
        source_fact_id=fact_id,
        trace_ref=trace_ref,
        processing_direction=PROCESSING_DIRECTION_READONLY,
        analysis_status="preview",
        analysis_summary=summary,
        readonly=True,
        created_at=created_at,
    )


def _fact_trace_ref(fact_payload: dict) -> str:
    trace_ref = fact_payload.get("_trace_ref")
    return trace_ref if isinstance(trace_ref, str) and trace_ref else new_trace_ref()


def _build_preview_summary(fact_type: str, fact_payload: dict) -> str:
    summary = (
        fact_payload.get("candidate_summary")
        or fact_payload.get("fact_summary")
        or fact_payload.get("text")
        or "暂无可读摘要"
    )
    return (
        f"基于已有正式事实生成的规则化分析预览：事实类型为 {fact_type}，"
        f"摘要为“{str(summary)[:120]}”。该内容不作为最终判断。"
    )
