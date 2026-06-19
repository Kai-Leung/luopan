"""L1 候选内容生成服务。

仅从 L0 原始输入生成候选包装并写入 candidates；不执行 S2，不进入确认，不写 L2。
"""

from datetime import datetime, timezone
from dataclasses import replace
from typing import List
from uuid import uuid4

from fastapi import HTTPException

from app.db.repositories import create_candidate as create_candidate_row
from app.db.repositories import ensure_minimal_storage_tables
from app.db.repositories import get_raw_input, load_json_field, update_candidate_payload
from app.db.session import SessionLocal
from app.modules.l1_candidate.extractor import build_candidate_summary, extract_candidate_fields
from app.modules.l1_candidate.models import CandidateRecord
from app.modules.l1_candidate.schemas import L1CandidateCreate, L1CandidateItem, L1CandidateResponse
from app.modules.l1_candidate.segmenter import extract_raw_text, split_candidate_texts
from app.modules.standard_governance.enums.source_types import SourceType
from app.modules.standard_governance.enums.status_types import CandidateStatus
from app.modules.s1_runtime_context.service import (
    ensure_payload_in_current_scope,
    runtime_context_snapshot,
)

CANDIDATE_MEMORY_STORE: List[CandidateRecord] = []


def create_candidate(payload: L1CandidateCreate) -> L1CandidateResponse:
    input_session_id = payload.input_session_id or f"session_{payload.raw_input_id.removeprefix('raw_')}"
    _require_existing_raw_input(payload.raw_input_id)
    if payload.supplement_candidate_id:
        return _merge_candidate_supplement(payload, input_session_id)

    raw_text = extract_raw_text(payload.raw_payload)
    candidate_texts = split_candidate_texts(raw_text)
    records = [
        _build_candidate_record(
            raw_input_id=payload.raw_input_id,
            input_session_id=input_session_id,
            source_type=payload.source_type,
            raw_payload=payload.raw_payload,
            candidate_text=candidate_text,
            candidate_index=index,
            candidate_count=len(candidate_texts),
        )
        for index, candidate_text in enumerate(candidate_texts, start=1)
    ]
    CANDIDATE_MEMORY_STORE.extend(records)

    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        for record in records:
            create_candidate_row(
                db,
                candidate_id=record.candidate_id,
                raw_input_id=record.raw_input_id,
                candidate_status=record.candidate_status.value,
                candidate_payload=record.candidate_payload,
                created_at=record.created_at,
            )
    finally:
        db.close()

    return _build_response(records)


def _build_candidate_record(
    *,
    raw_input_id: str,
    input_session_id: str,
    source_type: SourceType,
    raw_payload: dict,
    candidate_text: str,
    candidate_index: int,
    candidate_count: int,
) -> CandidateRecord:
    extracted_fields = extract_candidate_fields(candidate_text)
    candidate_payload = {
        "raw_payload": raw_payload,
        "text": candidate_text,
        "_runtime_context": runtime_context_snapshot(),
        "input_session_id": input_session_id,
        "candidate_index": candidate_index,
        "candidate_count": candidate_count,
        **extracted_fields,
        "candidate_summary": build_candidate_summary(extracted_fields, candidate_text),
        "candidate_note": "candidate only; waiting for later validation",
    }
    return CandidateRecord(
        candidate_id=f"cand_{uuid4().hex}",
        input_session_id=input_session_id,
        raw_input_id=raw_input_id,
        created_at=datetime.now(timezone.utc),
        source_type=source_type,
        candidate_status=CandidateStatus.NEW_CANDIDATE,
        candidate_payload=candidate_payload,
    )


def _build_response(records: list[CandidateRecord]) -> L1CandidateResponse:
    first = records[0]
    return L1CandidateResponse(
        candidate_id=first.candidate_id,
        input_session_id=first.input_session_id,
        raw_input_id=first.raw_input_id,
        candidate_status=first.candidate_status,
        candidate_payload=first.candidate_payload,
        candidates=[_to_candidate_item(record) for record in records],
        message="candidate created",
    )


def _to_candidate_item(record: CandidateRecord) -> L1CandidateItem:
    return L1CandidateItem(
        candidate_id=record.candidate_id,
        input_session_id=record.input_session_id,
        raw_input_id=record.raw_input_id,
        candidate_status=record.candidate_status,
        candidate_payload=record.candidate_payload,
    )


def _merge_candidate_supplement(
    payload: L1CandidateCreate,
    input_session_id: str,
) -> L1CandidateResponse:
    supplement_text = extract_raw_text(payload.raw_payload)
    for index, record in enumerate(CANDIDATE_MEMORY_STORE):
        if record.candidate_id != payload.supplement_candidate_id:
            continue
        previous_text = extract_raw_text(record.candidate_payload)
        merged_text = "\n".join(text for text in (previous_text, supplement_text) if text)
        merged_fields = extract_candidate_fields(merged_text)
        merged_payload = {
            **record.candidate_payload,
            "text": merged_text,
            "supplemental_texts": [
                *record.candidate_payload.get("supplemental_texts", []),
                supplement_text,
            ],
            "input_session_id": input_session_id,
            **merged_fields,
            "candidate_summary": build_candidate_summary(merged_fields, merged_text),
        }
        updated_record = replace(
            record,
            input_session_id=input_session_id,
            candidate_payload=merged_payload,
        )
        CANDIDATE_MEMORY_STORE[index] = updated_record
        _persist_candidate_payload(updated_record.candidate_id, updated_record.candidate_payload)
        return _build_response([updated_record])
    raise HTTPException(status_code=400, detail="supplement_candidate_id not found")


def _require_existing_raw_input(raw_input_id: str) -> None:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        raw_input = get_raw_input(db, raw_input_id)
        if raw_input is None:
            raise HTTPException(status_code=400, detail="raw_input_id not found")
        try:
            raw_payload = load_json_field(raw_input.raw_payload)
        except ValueError:
            raise HTTPException(status_code=400, detail="raw input payload is invalid")
        ensure_payload_in_current_scope(raw_payload)
    finally:
        db.close()


def _persist_candidate_payload(candidate_id: str, candidate_payload: dict) -> None:
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        if update_candidate_payload(
            db,
            candidate_id=candidate_id,
            candidate_payload=candidate_payload,
        ) is None:
            raise HTTPException(status_code=400, detail="candidate_id not found")
    finally:
        db.close()
