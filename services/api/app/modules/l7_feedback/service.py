"""Persistent L7 feedback service with controlled L0/L1 return."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_feedback_record,
    ensure_minimal_storage_tables,
    get_execution_response_record,
    get_fact_record,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.l7_feedback.schemas import L7FeedbackRequest, L7FeedbackResponse
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    get_current_runtime_context,
)
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.enums.source_types import SourceType
from app.modules.standard_governance.processing import PROCESSING_DIRECTION_CANDIDATE


def create_l7_feedback_candidate(payload: L7FeedbackRequest) -> L7FeedbackResponse:
    if not payload.execution_response_id and not payload.source_fact_id:
        raise HTTPException(status_code=400, detail="execution_response_id or source_fact_id is required")
    if not payload.feedback_note.strip():
        raise HTTPException(status_code=400, detail="feedback_note is required")

    context = get_current_runtime_context()
    ensure_minimal_storage_tables(include_fact_records=True)
    db = SessionLocal()
    try:
        execution = (
            get_execution_response_record(db, payload.execution_response_id)
            if payload.execution_response_id
            else None
        )
        if payload.execution_response_id and execution is None:
            raise HTTPException(status_code=404, detail="execution response not found")
        if execution and execution.organization_id != context.organization_id:
            raise HTTPException(status_code=403, detail="cross-organization execution access is blocked")

        source_fact_id = payload.source_fact_id or (
            execution.source_fact_id if execution else None
        )
        if execution and payload.source_fact_id and execution.source_fact_id != payload.source_fact_id:
            raise HTTPException(status_code=400, detail="execution response does not belong to source fact")
        fact_trace_ref = _validate_source_fact(db, source_fact_id)
        trace_ref = execution.trace_ref if execution else fact_trace_ref or new_trace_ref()
    finally:
        db.close()

    feedback_id = f"feedback_{uuid4().hex}"
    raw_input = receive_raw_input(
        RawInputCreate(
            text=payload.feedback_note.strip(),
            idempotency_key=f"feedback-return:{feedback_id}",
            source_type=SourceType.FEEDBACK_RETURN,
        )
    )
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw_input.raw_input_id,
            input_session_id=raw_input.input_session_id,
            raw_payload={
                "text": payload.feedback_note.strip(),
                "feedback_id": feedback_id,
                "source_fact_id": source_fact_id,
                "execution_response_id": payload.execution_response_id,
            },
            source_type=SourceType.FEEDBACK_RETURN,
        )
    )

    created_at = datetime.now(timezone.utc)
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_feedback_record(
            db,
            feedback_id=feedback_id,
            feedback_status="candidate",
            execution_response_id=payload.execution_response_id,
            source_fact_id=source_fact_id,
            trace_ref=trace_ref,
            feedback_note=payload.feedback_note.strip(),
            feedback_type=payload.feedback_type,
            return_raw_input_id=raw_input.raw_input_id,
            return_candidate_id=candidate.candidate_id,
            organization_id=context.organization_id,
            created_at=created_at,
        )
    finally:
        db.close()

    record_trace_event(
        trace_ref=trace_ref,
        source_fact_id=source_fact_id,
        raw_input_id=raw_input.raw_input_id,
        candidate_id=candidate.candidate_id,
        execution_response_id=payload.execution_response_id,
        feedback_id=feedback_id,
        source_stage="l7_feedback",
        target_stage="l1_candidate",
        action_type="feedback_returned_to_candidate_flow",
    )
    return L7FeedbackResponse(
        feedback_id=feedback_id,
        feedback_status="candidate",
        execution_response_id=payload.execution_response_id,
        source_fact_id=source_fact_id,
        trace_ref=trace_ref,
        processing_direction=PROCESSING_DIRECTION_CANDIDATE,
        feedback_note=payload.feedback_note.strip(),
        feedback_type=payload.feedback_type,
        return_raw_input_id=raw_input.raw_input_id,
        return_candidate_id=candidate.candidate_id,
        governance_required=True,
        returns_to_candidate_flow=True,
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
