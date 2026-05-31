"""L6 execution response service.

Records an execution response object only. It does not execute real actions,
does not persist facts, and does not trigger L7 feedback.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import get_fact_record
from app.db.session import SessionLocal
from app.modules.l6_execution.schemas import (
    L6ExecutionResponseRequest,
    L6ExecutionResponseResponse,
)
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_RESPONSE, build_trace_ref


def create_l6_execution_response(
    payload: L6ExecutionResponseRequest,
) -> L6ExecutionResponseResponse:
    if not payload.recommendation_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="recommendation_id or source_fact_id is required")
    if not payload.execution_note.strip():
        raise HTTPException(status_code=400, detail="execution_note is required")
    if not payload.execution_status.strip():
        raise HTTPException(status_code=400, detail="execution_status is required")

    if payload.recommendation_id:
        _validate_recommendation_reference(payload.recommendation_id)
    if payload.source_fact_id:
        _validate_source_fact(payload.source_fact_id)

    return L6ExecutionResponseResponse(
        execution_response_id=f"execution_response_{uuid4().hex}",
        execution_status=payload.execution_status,
        recommendation_id=payload.recommendation_id,
        source_fact_id=payload.source_fact_id,
        trace_ref=build_trace_ref(),
        processing_direction=PROCESSING_DIRECTION_RESPONSE,
        execution_note=payload.execution_note,
        creates_fact=False,
        created_at=datetime.now(timezone.utc),
    )


def _validate_recommendation_reference(recommendation_id: str) -> None:
    if not recommendation_id.startswith("recommendation_"):
        raise HTTPException(status_code=404, detail="recommendation draft not found")


def _validate_source_fact(source_fact_id: str) -> None:
    db = SessionLocal()
    try:
        if get_fact_record(db, source_fact_id) is None:
            raise HTTPException(status_code=404, detail="source fact not found")
    finally:
        db.close()
