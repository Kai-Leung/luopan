"""L0 原始输入接收服务。

接收原始输入并写入 raw_inputs；不生成候选，不治理，不写正式事实。
"""

from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.db.repositories import (
    create_raw_input,
    ensure_minimal_storage_tables,
    find_raw_input_by_idempotency_key,
    load_json_field,
)
from app.db.session import SessionLocal
from app.modules.l0_input.models import RawInputRecord
from app.modules.l0_input.schemas import RawInputCreate, RawInputReceived
from app.modules.s1_runtime_context.service import runtime_context_snapshot

RAW_INPUT_MEMORY_STORE: List[RawInputRecord] = []


def receive_raw_input(payload: RawInputCreate) -> RawInputReceived:
    existing_response = _find_idempotent_response(payload.idempotency_key)
    if existing_response is not None:
        return existing_response

    raw_input_id = f"raw_{uuid4().hex}"
    input_session_id = payload.input_session_id or f"session_{raw_input_id.removeprefix('raw_')}"
    raw_payload = {
        "text": payload.text,
        "image_ref": payload.image_ref,
        "file_ref": payload.file_ref,
        "input_session_id": input_session_id,
        "idempotency_key": payload.idempotency_key,
        "_runtime_context": runtime_context_snapshot(),
    }
    record = RawInputRecord(
        raw_input_id=raw_input_id,
        input_session_id=input_session_id,
        received_at=datetime.now(timezone.utc),
        source_type=payload.source_type,
        raw_payload=raw_payload,
    )
    RAW_INPUT_MEMORY_STORE.append(record)

    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        create_raw_input(
            db,
            raw_input_id=record.raw_input_id,
            source_type=record.source_type.value,
            raw_payload=record.raw_payload,
            status=record.status,
            received_at=record.received_at,
        )
    finally:
        db.close()

    return RawInputReceived(
        raw_input_id=record.raw_input_id,
        input_session_id=record.input_session_id,
        status=record.status,
        message="raw input received",
    )


def _find_idempotent_response(idempotency_key: str | None) -> RawInputReceived | None:
    if not idempotency_key:
        return None
    ensure_minimal_storage_tables()
    db = SessionLocal()
    try:
        row = find_raw_input_by_idempotency_key(db, idempotency_key)
        if row is None:
            return None
        try:
            raw_payload = load_json_field(row.raw_payload)
        except ValueError:
            return None
        from app.modules.s1_runtime_context.service import ensure_payload_in_current_scope

        ensure_payload_in_current_scope(raw_payload)
        input_session_id = raw_payload.get("input_session_id")
        if not isinstance(input_session_id, str) or not input_session_id:
            input_session_id = f"session_{row.raw_input_id.removeprefix('raw_')}"
        return RawInputReceived(
            raw_input_id=row.raw_input_id,
            input_session_id=input_session_id,
            status=row.status,
            message="raw input received",
        )
    finally:
        db.close()
