"""Persistent L5 recommendation draft service."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_recommendation_record,
    ensure_minimal_storage_tables,
    get_analysis_record,
    get_fact_record,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l5_recommendation.schemas import (
    L5RecommendationDraftRequest,
    L5RecommendationDraftResponse,
)
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    get_current_runtime_context,
)
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_DRAFT


def create_l5_recommendation_draft(
    payload: L5RecommendationDraftRequest,
) -> L5RecommendationDraftResponse:
    if not payload.analysis_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="analysis_id or source_fact_id is required")

    context = get_current_runtime_context()
    ensure_minimal_storage_tables(include_fact_records=True)
    db = SessionLocal()
    try:
        analysis = get_analysis_record(db, payload.analysis_id) if payload.analysis_id else None
        if payload.analysis_id and analysis is None:
            raise HTTPException(status_code=404, detail="analysis preview not found")
        if analysis and analysis.organization_id != context.organization_id:
            raise HTTPException(status_code=403, detail="cross-organization analysis access is blocked")

        source_fact_id = payload.source_fact_id or (analysis.source_fact_id if analysis else None)
        if analysis and payload.source_fact_id and analysis.source_fact_id != payload.source_fact_id:
            raise HTTPException(status_code=400, detail="analysis does not belong to source fact")

        fact_summary, fact_trace_ref = _load_source_fact(db, source_fact_id)
        trace_ref = analysis.trace_ref if analysis else fact_trace_ref or new_trace_ref()
        recommendation_id = f"recommendation_{uuid4().hex}"
        created_at = datetime.now(timezone.utc)
        summary = _build_recommendation_summary(
            analysis_id=payload.analysis_id,
            source_fact_id=source_fact_id,
            fact_summary=fact_summary,
            context_payload=payload.context_payload,
        )
        create_recommendation_record(
            db,
            recommendation_id=recommendation_id,
            recommendation_status="draft",
            source_fact_id=source_fact_id,
            analysis_id=payload.analysis_id,
            trace_ref=trace_ref,
            recommendation_summary=summary,
            organization_id=context.organization_id,
            created_at=created_at,
        )
    finally:
        db.close()

    record_trace_event(
        trace_ref=trace_ref,
        source_fact_id=source_fact_id,
        analysis_id=payload.analysis_id,
        recommendation_id=recommendation_id,
        source_stage="l4_analysis",
        target_stage="l5_recommendation",
        action_type="recommendation_draft_created",
    )
    return L5RecommendationDraftResponse(
        recommendation_id=recommendation_id,
        recommendation_status="draft",
        source_fact_id=source_fact_id,
        analysis_id=payload.analysis_id,
        trace_ref=trace_ref,
        processing_direction=PROCESSING_DIRECTION_DRAFT,
        recommendation_summary=summary,
        auto_executable=False,
        created_at=created_at,
    )


def _load_source_fact(db, source_fact_id: str | None) -> tuple[str | None, str | None]:
    if not source_fact_id:
        return None, None
    row = get_fact_record(db, source_fact_id)
    if row is None:
        raise HTTPException(status_code=404, detail="source fact not found")
    try:
        fact_payload = load_json_field(row.fact_payload)
    except ValueError:
        raise HTTPException(status_code=500, detail="source fact payload is invalid")
    ensure_payload_in_current_scope(fact_payload)
    summary = (
        fact_payload.get("candidate_summary")
        or fact_payload.get("fact_summary")
        or fact_payload.get("text")
        or "暂无可读摘要"
    )
    trace_ref = fact_payload.get("_trace_ref")
    return str(summary)[:120], trace_ref if isinstance(trace_ref, str) else None


def _build_recommendation_summary(
    *,
    analysis_id: str | None,
    source_fact_id: str | None,
    fact_summary: str | None,
    context_payload: dict | None,
) -> str:
    context_note = ""
    if context_payload:
        context_note = f"；已接收上下文键：{', '.join(sorted(context_payload.keys()))}"
    source_note = source_fact_id or analysis_id or "未指定来源"
    base = fact_summary or "基于已提供的分析预览引用生成"
    return (
        f"建议草稿：请人工复核来源 {source_note} 后，再决定是否形成正式处理方案。"
        f"参考摘要：{base}{context_note}。该草稿不代表正式决策。"
    )
