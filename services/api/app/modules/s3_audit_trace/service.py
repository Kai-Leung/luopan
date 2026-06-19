"""Persistent S3 source trace and audit service."""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_audit_event,
    ensure_minimal_storage_tables,
    get_fact_record,
    list_audit_events,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    get_current_runtime_context,
)
from app.modules.s3_audit_trace.schemas import S3TraceEvent, S3TraceSummaryResponse


def new_trace_ref() -> str:
    return f"trace_{uuid4().hex}"


def record_fact_chain_events(
    *,
    trace_ref: str,
    source_fact_id: str,
    raw_input_id: str,
    candidate_id: str,
    governance_id: str,
    review_id: str,
) -> None:
    stages = [
        ("l0_input", "l1_candidate", "raw_input_received"),
        ("l1_candidate", "s2_governance", "candidate_created"),
        ("s2_governance", "manual_confirmation", "governance_checked"),
        ("manual_confirmation", "l2_fact", "candidate_confirmed"),
        ("l2_fact", "l3_query_view", "fact_created"),
    ]
    for source_stage, target_stage, action_type in stages:
        record_trace_event(
            trace_ref=trace_ref,
            source_fact_id=source_fact_id,
            raw_input_id=raw_input_id,
            candidate_id=candidate_id,
            governance_id=governance_id,
            review_id=review_id,
            source_stage=source_stage,
            target_stage=target_stage,
            action_type=action_type,
        )


def record_trace_event(
    *,
    trace_ref: str,
    source_stage: str,
    target_stage: str,
    action_type: str,
    source_fact_id: Optional[str] = None,
    raw_input_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
    governance_id: Optional[str] = None,
    review_id: Optional[str] = None,
    analysis_id: Optional[str] = None,
    recommendation_id: Optional[str] = None,
    execution_response_id: Optional[str] = None,
    feedback_id: Optional[str] = None,
) -> None:
    context = get_current_runtime_context()
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_audit_event(
            db,
            trace_ref=trace_ref,
            source_fact_id=source_fact_id,
            raw_input_id=raw_input_id,
            candidate_id=candidate_id,
            governance_id=governance_id,
            review_id=review_id,
            analysis_id=analysis_id,
            recommendation_id=recommendation_id,
            execution_response_id=execution_response_id,
            feedback_id=feedback_id,
            source_stage=source_stage,
            target_stage=target_stage,
            action_type=action_type,
            actor_id=context.user_id,
            organization_id=context.organization_id,
            readonly=True,
            no_write_l2=True,
            created_at=datetime.now(timezone.utc),
        )
    finally:
        db.close()


def get_s3_trace_summary(
    *,
    source_fact_id: str | None = None,
    trace_ref: str | None = None,
) -> S3TraceSummaryResponse:
    if not source_fact_id and not trace_ref:
        raise HTTPException(status_code=400, detail="source_fact_id or trace_ref is required")

    context = get_current_runtime_context()
    ensure_minimal_storage_tables(include_fact_records=True)
    db = SessionLocal()
    try:
        if source_fact_id:
            fact = get_fact_record(db, source_fact_id)
            if fact is None:
                raise HTTPException(status_code=404, detail="source fact not found")
            try:
                fact_payload = load_json_field(fact.fact_payload)
            except ValueError:
                raise HTTPException(status_code=500, detail="source fact payload is invalid")
            ensure_payload_in_current_scope(fact_payload)

        rows = list_audit_events(
            db,
            organization_id=context.organization_id,
            source_fact_id=source_fact_id,
            trace_ref=trace_ref,
        )
    finally:
        db.close()

    if not rows:
        resolved_trace_ref = trace_ref or new_trace_ref()
        record_trace_event(
            trace_ref=resolved_trace_ref,
            source_fact_id=source_fact_id,
            source_stage="l2_l3_fact",
            target_stage="s3_audit_trace",
            action_type="legacy_trace_initialized",
        )
        ensure_minimal_storage_tables()
        db = SessionLocal()
        try:
            rows = list_audit_events(
                db,
                organization_id=context.organization_id,
                source_fact_id=source_fact_id,
                trace_ref=resolved_trace_ref,
            )
        finally:
            db.close()

    resolved_trace_ref = rows[0].trace_ref
    events = [_to_trace_event(row) for row in rows]
    source_label = source_fact_id or resolved_trace_ref
    return S3TraceSummaryResponse(
        trace_ref=resolved_trace_ref,
        source_fact_id=source_fact_id or rows[0].source_fact_id,
        chain_summary=f"来源追溯链：{source_label}，共 {len(events)} 个受控事件，不写入 L2。",
        events=events,
        no_write_l2=True,
    )


def _to_trace_event(row) -> S3TraceEvent:
    return S3TraceEvent(
        trace_ref=row.trace_ref,
        source_fact_id=row.source_fact_id,
        raw_input_id=row.raw_input_id,
        candidate_id=row.candidate_id,
        governance_id=row.governance_id,
        review_id=row.review_id,
        analysis_id=row.analysis_id,
        recommendation_id=row.recommendation_id,
        execution_response_id=row.execution_response_id,
        feedback_id=row.feedback_id,
        created_at=row.created_at,
        source_stage=row.source_stage,
        target_stage=row.target_stage,
        action_type=row.action_type,
        actor_id=row.actor_id,
        organization_id=row.organization_id,
        readonly=row.readonly,
        no_write_l2=row.no_write_l2,
    )
