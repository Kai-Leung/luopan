"""L2 正式事实入链最小服务。

只允许 confirmed_candidate 通过完整前置链路写入 fact_records；不反写 L0/L1/S2/人工确认。
"""

import logging
from datetime import datetime, timezone
from typing import Any, List
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import (
    create_fact_record,
    ensure_minimal_storage_tables,
    get_candidate,
    get_fact_record_by_review_id,
    get_governance_result,
    get_manual_review,
    get_raw_input,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l2_fact.models import FactRecordEntry
from app.modules.l2_fact.schemas import L2FactCreateRequest, L2FactResponse
from app.modules.standard_governance.rules.fact_record_types import is_known_fact_record_type
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    runtime_context_snapshot,
)
from app.modules.s3_audit_trace.service import new_trace_ref, record_fact_chain_events

FACT_RECORD_MEMORY_STORE: List[FactRecordEntry] = []
ACTIVE_FACT_STATUS = "active_fact"
CONFIRMED_REVIEW_STATUS = "confirmed_candidate"
logger = logging.getLogger(__name__)


def _require_non_empty(value: object, field_name: str) -> None:
    if value is None:
        raise HTTPException(status_code=400, detail=f"{field_name} is required")
    if isinstance(value, str) and not value.strip():
        raise HTTPException(status_code=400, detail=f"{field_name} is required")
    if isinstance(value, dict) and not value:
        raise HTTPException(status_code=400, detail=f"{field_name} is required")


def create_l2_fact(payload: L2FactCreateRequest) -> L2FactResponse:
    _validate_l2_payload(payload)

    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        _validate_l2_chain(db, payload)
        existing = get_fact_record_by_review_id(db, payload.review_id)
        if existing is not None:
            return _build_existing_l2_fact_response(existing)
        ensure_minimal_storage_tables(include_fact_records=True)
        record = _build_fact_record(payload, trace_ref=new_trace_ref())
        FACT_RECORD_MEMORY_STORE.append(record)
        _persist_fact_record(db, record)
    finally:
        db.close()

    trace_ref = str(record.fact_payload["_trace_ref"])
    record_fact_chain_events(
        trace_ref=trace_ref,
        source_fact_id=record.fact_id,
        raw_input_id=record.raw_input_id,
        candidate_id=record.candidate_id,
        governance_id=record.governance_id,
        review_id=record.review_id,
    )
    return _build_l2_fact_response(record)


def _build_existing_l2_fact_response(row: Any) -> L2FactResponse:
    try:
        fact_payload = load_json_field(row.fact_payload)
    except ValueError:
        raise HTTPException(status_code=500, detail="existing fact payload is invalid")
    ensure_payload_in_current_scope(fact_payload)
    return L2FactResponse(
        fact_id=row.fact_id,
        fact_status=row.fact_status,
        fact_payload=fact_payload,
        raw_input_id=row.raw_input_id,
        candidate_id=row.candidate_id,
        governance_id=row.governance_id,
        review_id=row.review_id,
        message="fact record already exists",
    )


def _validate_l2_payload(payload: L2FactCreateRequest) -> None:
    _require_non_empty(payload.raw_input_id, "raw_input_id")
    _require_non_empty(payload.candidate_id, "candidate_id")
    _require_non_empty(payload.governance_id, "governance_id")
    _require_non_empty(payload.review_id, "review_id")
    _require_non_empty(payload.fact_type, "fact_type")
    _require_non_empty(payload.fact_payload, "fact_payload")

    if not is_known_fact_record_type(payload.fact_type):
        logger.warning("L2 entry rejected because fact type is not known")
        raise HTTPException(status_code=400, detail="fact_type is not a known fact record type")

    if payload.review_status != CONFIRMED_REVIEW_STATUS:
        logger.warning("L2 entry rejected because review status is not confirmed")
        raise HTTPException(
            status_code=400,
            detail="only confirmed_candidate can enter L2",
        )


def _validate_l2_chain(db: Any, payload: L2FactCreateRequest) -> None:
    raw_input = get_raw_input(db, payload.raw_input_id)
    if raw_input is None:
        logger.warning("L2 entry rejected because raw input is missing")
        raise HTTPException(status_code=400, detail="raw_input_id not found")
    try:
        raw_payload = load_json_field(raw_input.raw_payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="raw input payload is invalid")
    ensure_payload_in_current_scope(raw_payload)

    candidate = get_candidate(db, payload.candidate_id)
    if candidate is None:
        logger.warning("L2 entry rejected because candidate is missing")
        raise HTTPException(status_code=400, detail="candidate_id not found")
    if candidate.raw_input_id != payload.raw_input_id:
        logger.warning("L2 entry rejected because candidate does not belong to raw input")
        raise HTTPException(status_code=400, detail="candidate does not belong to raw_input")
    try:
        candidate_payload = load_json_field(candidate.candidate_payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="candidate payload is invalid")
    ensure_payload_in_current_scope(candidate_payload)
    _validate_candidate_fact_type(candidate.candidate_payload, payload.fact_type)

    governance = get_governance_result(db, payload.governance_id)
    if governance is None:
        logger.warning("L2 entry rejected because governance result is missing")
        raise HTTPException(status_code=400, detail="governance_id not found")
    if governance.candidate_id != payload.candidate_id:
        logger.warning("L2 entry rejected because governance does not belong to candidate")
        raise HTTPException(status_code=400, detail="governance does not belong to candidate")
    if governance.governance_status == "blocked":
        logger.warning("L2 entry rejected because governance result is blocked")
        raise HTTPException(status_code=400, detail="blocked governance result cannot enter L2")

    manual_review = get_manual_review(db, payload.review_id)
    if manual_review is None:
        logger.warning("L2 entry rejected because manual review is missing")
        raise HTTPException(status_code=400, detail="review_id not found")
    if manual_review.governance_id != payload.governance_id:
        logger.warning("L2 entry rejected because review does not belong to governance")
        raise HTTPException(status_code=400, detail="review does not belong to governance")
    if manual_review.review_status != CONFIRMED_REVIEW_STATUS:
        logger.warning("L2 entry rejected because manual review is not confirmed")
        raise HTTPException(
            status_code=400,
            detail="manual review is not confirmed_candidate",
        )


def _validate_candidate_fact_type(candidate_payload_raw: str, requested_fact_type: str) -> None:
    try:
        candidate_payload = load_json_field(candidate_payload_raw)
    except ValueError:
        logger.warning("L2 entry rejected because candidate payload is invalid")
        raise HTTPException(status_code=400, detail="candidate payload is invalid")

    candidate_fact_type = candidate_payload.get("fact_record_type")
    if not isinstance(candidate_fact_type, str) or not candidate_fact_type.strip():
        logger.warning("L2 entry rejected because candidate fact type is missing")
        raise HTTPException(status_code=400, detail="candidate fact_record_type is required")

    if not is_known_fact_record_type(candidate_fact_type):
        logger.warning("L2 entry rejected because candidate fact type is not known")
        raise HTTPException(status_code=400, detail="candidate fact_record_type is not known")

    if requested_fact_type != candidate_fact_type:
        logger.warning("L2 entry rejected because requested fact type does not match candidate")
        raise HTTPException(status_code=400, detail="fact_type does not match candidate fact_record_type")


def _build_fact_record(payload: L2FactCreateRequest, *, trace_ref: str) -> FactRecordEntry:
    fact_payload = {
        **payload.fact_payload,
        "_trace_ref": trace_ref,
        "_runtime_context": runtime_context_snapshot(),
    }
    return FactRecordEntry(
        fact_id=f"fact_{uuid4().hex}",
        raw_input_id=payload.raw_input_id,
        candidate_id=payload.candidate_id,
        governance_id=payload.governance_id,
        review_id=payload.review_id,
        fact_type=payload.fact_type,
        fact_payload=fact_payload,
        fact_status=ACTIVE_FACT_STATUS,
        created_at=datetime.now(timezone.utc),
    )


def _persist_fact_record(db: Any, record: FactRecordEntry) -> None:
    create_fact_record(
        db,
        fact_id=record.fact_id,
        raw_input_id=record.raw_input_id,
        candidate_id=record.candidate_id,
        governance_id=record.governance_id,
        review_id=record.review_id,
        fact_type=record.fact_type,
        fact_payload=record.fact_payload,
        fact_status=record.fact_status,
        created_at=record.created_at,
    )


def _build_l2_fact_response(record: FactRecordEntry) -> L2FactResponse:
    return L2FactResponse(
        fact_id=record.fact_id,
        fact_status=record.fact_status,
        fact_payload=record.fact_payload,
        raw_input_id=record.raw_input_id,
        candidate_id=record.candidate_id,
        governance_id=record.governance_id,
        review_id=record.review_id,
        message="fact record created",
    )
