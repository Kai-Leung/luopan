"""L7 feedback candidate service.

Creates a feedback candidate only. It does not write L2, does not publish
rules, and does not bypass L0/L1/S2/manual confirmation.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import get_fact_record
from app.db.session import SessionLocal
from app.modules.l7_feedback.schemas import L7FeedbackRequest, L7FeedbackResponse
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_CANDIDATE, build_trace_ref


def create_l7_feedback_candidate(payload: L7FeedbackRequest) -> L7FeedbackResponse:
    if not payload.execution_response_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="execution_response_id or source_fact_id is required")
    if not payload.feedback_note.strip():
        raise HTTPException(status_code=400, detail="feedback_note is required")

    if payload.execution_response_id:
        _validate_execution_response_reference(payload.execution_response_id)
    if payload.source_fact_id:
        _validate_source_fact(payload.source_fact_id)

    return L7FeedbackResponse(
        feedback_id=f"feedback_{uuid4().hex}",
        feedback_status="candidate",
        execution_response_id=payload.execution_response_id,
        source_fact_id=payload.source_fact_id,
        trace_ref=build_trace_ref(),
        processing_direction=PROCESSING_DIRECTION_CANDIDATE,
        feedback_note=payload.feedback_note,
        feedback_type=payload.feedback_type,
        returns_to_candidate_flow=True,
        created_at=datetime.now(timezone.utc),
    )


def _validate_execution_response_reference(execution_response_id: str) -> None:
    if not execution_response_id.startswith("execution_response_"):
        raise HTTPException(status_code=404, detail="execution response not found")


def _validate_source_fact(source_fact_id: str) -> None:
    db = SessionLocal()
    try:
        if get_fact_record(db, source_fact_id) is None:
            raise HTTPException(status_code=404, detail="source fact not found")
    finally:
        db.close()
