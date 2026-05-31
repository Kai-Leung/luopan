"""L5 recommendation draft service.

Creates a non-final recommendation draft from L4/L3 references only.
It does not persist recommendations, does not write L2, and does not trigger L6.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import get_fact_record, load_json_field
from app.db.session import SessionLocal
from app.modules.l5_recommendation.schemas import (
    L5RecommendationDraftRequest,
    L5RecommendationDraftResponse,
)
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_DRAFT, build_trace_ref


def create_l5_recommendation_draft(
    payload: L5RecommendationDraftRequest,
) -> L5RecommendationDraftResponse:
    if not payload.analysis_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="analysis_id or source_fact_id is required")

    fact_summary = None
    if payload.source_fact_id:
        fact_summary = _load_source_fact_summary(payload.source_fact_id)

    if payload.analysis_id:
        _validate_analysis_reference(payload.analysis_id)

    return L5RecommendationDraftResponse(
        recommendation_id=f"recommendation_{uuid4().hex}",
        recommendation_status="draft",
        source_fact_id=payload.source_fact_id,
        analysis_id=payload.analysis_id,
        trace_ref=build_trace_ref(),
        processing_direction=PROCESSING_DIRECTION_DRAFT,
        recommendation_summary=_build_recommendation_summary(
            analysis_id=payload.analysis_id,
            source_fact_id=payload.source_fact_id,
            fact_summary=fact_summary,
            context_payload=payload.context_payload,
        ),
        auto_executable=False,
        created_at=datetime.now(timezone.utc),
    )


def _load_source_fact_summary(source_fact_id: str) -> str:
    db = SessionLocal()
    try:
        row = get_fact_record(db, source_fact_id)
        if row is None:
            raise HTTPException(status_code=404, detail="source fact not found")
        try:
            fact_payload = load_json_field(row.fact_payload)
        except ValueError:
            raise HTTPException(status_code=500, detail="source fact payload is invalid")
        summary = (
            fact_payload.get("candidate_summary")
            or fact_payload.get("fact_summary")
            or fact_payload.get("text")
            or "暂无可读摘要"
        )
        return str(summary)[:120]
    finally:
        db.close()


def _validate_analysis_reference(analysis_id: str) -> None:
    if not analysis_id.startswith("analysis_"):
        raise HTTPException(status_code=404, detail="analysis preview not found")


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
