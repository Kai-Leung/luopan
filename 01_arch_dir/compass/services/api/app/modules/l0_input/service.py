"""L0 原始输入接收服务。

接收原始输入并写入 raw_inputs；不生成候选，不治理，不写正式事实。
"""

from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.db.repositories import create_raw_input, ensure_minimal_storage_tables
from app.db.session import SessionLocal
from app.modules.l0_input.models import RawInputRecord
from app.modules.l0_input.schemas import RawInputCreate, RawInputReceived

RAW_INPUT_MEMORY_STORE: List[RawInputRecord] = []


def receive_raw_input(payload: RawInputCreate) -> RawInputReceived:
    raw_input_id = f"raw_{uuid4().hex}"
    input_session_id = payload.input_session_id or f"session_{raw_input_id.removeprefix('raw_')}"
    raw_payload = {
        "text": payload.text,
        "image_ref": payload.image_ref,
        "file_ref": payload.file_ref,
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
