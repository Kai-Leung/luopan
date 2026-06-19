"""Persistent L6 execution-response service.

The service records a response only. It does not execute external actions and
does not create or modify L2 facts.
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_execution_response_record,
    ensure_minimal_storage_tables,
    get_fact_record,
    get_recommendation_record,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l6_execution.schemas import (
    L6ExecutionResponseRequest,
    L6ExecutionResponseResponse,
)
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    get_current_runtime_context,
)
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_RESPONSE


def create_l6_execution_response(
    payload: L6ExecutionResponseRequest,
) -> L6ExecutionResponseResponse:
    if not payload.recommendation_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="recommendation_id or source_fact_id is required")
    if not payload.execution_note.strip():
        raise HTTPException(status_code=400, detail="execution_note is required")
    if not payload.execution_status.strip():
        raise HTTPException(status_code=400, detail="execution_status is required")

    context = get_current_runtime_context()
    ensure_minimal_storage_tables(include_fact_records=True)
    db = SessionLocal()
    try:
        recommendation = (
            get_recommendation_record(db, payload.recommendation_id)
            if payload.recommendation_id
            else None
        )
        if payload.recommendation_id and recommendation is None:
            raise HTTPException(status_code=404, detail="recommendation draft not found")
        if recommendation and recommendation.organization_id != context.organization_id:
            raise HTTPException(status_code=403, detail="cross-organization recommendation access is blocked")

        source_fact_id = payload.source_fact_id or (
            recommendation.source_fact_id if recommendation else None
        )
        if recommendation and payload.source_fact_id and recommendation.source_fact_id != payload.source_fact_id:
            raise HTTPException(status_code=400, detail="recommendation does not belong to source fact")
        fact_trace_ref = _validate_source_fact(db, source_fact_id)
        trace_ref = recommendation.trace_ref if recommendation else fact_trace_ref or new_trace_ref()

        execution_response_id = f"execution_response_{uuid4().hex}"
        created_at = datetime.now(timezone.utc)
        create_execution_response_record(
            db,
            execution_response_id=execution_response_id,
            execution_status=payload.execution_status.strip(),
            recommendation_id=payload.recommendation_id,
            source_fact_id=source_fact_id,
            trace_ref=trace_ref,
            execution_note=payload.execution_note.strip(),
            organization_id=context.organization_id,
            created_at=created_at,
        )
    finally:
        db.close()

    record_trace_event(
        trace_ref=trace_ref,
        source_fact_id=source_fact_id,
        recommendation_id=payload.recommendation_id,
        execution_response_id=execution_response_id,
        source_stage="l5_recommendation",
        target_stage="l6_execution",
        action_type="execution_response_recorded",
    )
    return L6ExecutionResponseResponse(
        execution_response_id=execution_response_id,
        execution_status=payload.execution_status.strip(),
        recommendation_id=payload.recommendation_id,
        source_fact_id=source_fact_id,
        trace_ref=trace_ref,
        processing_direction=PROCESSING_DIRECTION_RESPONSE,
        execution_note=payload.execution_note.strip(),
        creates_fact=False,
        created_at=created_at,
    )


def _validate_source_fact(db, source_fact_id: str | None) -> str | None:
    if not source_fact_id:
        return None
    row = get_fact_record(db, source_fact_id)
    if row is None:
        raise HTTPException(status_code=404, detail="source fact not found")
    try:
        fact_payload = load_json_field(row.fact_payload)
    except ValueError:
        raise HTTPException(status_code=500, detail="source fact payload is invalid")
    ensure_payload_in_current_scope(fact_payload)
    trace_ref = fact_payload.get("_trace_ref")
    return trace_ref if isinstance(trace_ref, str) else None
