"""L4 analysis preview service.

Only reads an existing L2/L3 fact record and returns a non-final preview.
It does not call AI, does not persist analysis output, and does not write L2.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import get_fact_record, load_json_field
from app.db.session import SessionLocal
from app.modules.l4_analysis.schemas import L4AnalysisPreviewResponse
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_READONLY, build_trace_ref


def get_l4_analysis_preview(fact_id: str) -> L4AnalysisPreviewResponse:
    db = SessionLocal()
    try:
        row = get_fact_record(db, fact_id)
        if row is None:
            raise HTTPException(status_code=404, detail="source fact not found")

        try:
            fact_payload = load_json_field(row.fact_payload)
        except ValueError:
            raise HTTPException(status_code=500, detail="source fact payload is invalid")

        return L4AnalysisPreviewResponse(
            analysis_id=f"analysis_{uuid4().hex}",
            source_fact_id=row.fact_id,
            trace_ref=build_trace_ref(),
            processing_direction=PROCESSING_DIRECTION_READONLY,
            analysis_status="preview",
            analysis_summary=_build_preview_summary(row.fact_type, fact_payload),
            readonly=True,
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()


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
