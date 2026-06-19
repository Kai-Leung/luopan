"""L3 正式事实只读视图服务。

只读取 L2 fact_records，不创建、修改、删除正式事实。
"""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from typing import Optional

from app.db.repositories import get_fact_record, list_fact_records, load_json_field
from app.db.session import SessionLocal
from app.modules.l3_query_view.schemas import L3FactListResponse, L3FactListItem, L3FactViewResponse
from app.modules.s1_runtime_context.service import ensure_payload_in_current_scope

logger = logging.getLogger(__name__)


def get_l3_fact_view(fact_id: str) -> L3FactViewResponse:
    db = SessionLocal()
    try:
        try:
            row = get_fact_record(db, fact_id)
        except SQLAlchemyError:
            logger.exception("L3 fact read failed while querying fact record")
            row = None

        if row is None:
            raise HTTPException(status_code=404, detail="fact record not found")

        try:
            fact_payload = load_json_field(row.fact_payload)
        except ValueError:
            logger.exception("L3 fact read failed because fact payload is invalid JSON")
            raise HTTPException(status_code=500, detail="fact payload is invalid")
        ensure_payload_in_current_scope(fact_payload)

        return L3FactViewResponse(
            fact_id=row.fact_id,
            fact_type=row.fact_type,
            fact_payload=fact_payload,
            fact_status=row.fact_status,
            created_at=row.created_at,
        )
    finally:
        db.close()


def _extract_summary(fact_payload: dict) -> str:
    """Extract a human-readable summary from fact_payload."""
    candidates = (
        fact_payload.get("candidate_summary")
        or fact_payload.get("fact_summary")
        or fact_payload.get("text")
        or fact_payload.get("candidate_payload", {}).get("fact_summary", "")
    )
    if candidates:
        return str(candidates)[:120]
    return "(no summary)"


def _extract_source_type(fact_payload: dict) -> str:
    """Extract source_type from fact_payload, default to manual_confirmation."""
    return fact_payload.get("source_type") or fact_payload.get("raw_payload", {}).get("source_type") or "manual_confirmation"


def list_l3_facts(
    *,
    fact_type: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> L3FactListResponse:
    """List L3 fact records with optional filtering. Read-only."""
    db = SessionLocal()
    try:
        rows = list_fact_records(db, fact_type=fact_type, keyword=keyword, limit=limit, offset=offset)
        items = []
        for row in rows:
            try:
                fact_payload = load_json_field(row.fact_payload)
            except ValueError:
                continue
            try:
                ensure_payload_in_current_scope(fact_payload)
            except HTTPException:
                continue
            summary = _extract_summary(fact_payload)
            source = _extract_source_type(fact_payload)
            items.append(
                L3FactListItem(
                    fact_id=row.fact_id,
                    fact_type=row.fact_type,
                    fact_payload_summary=summary,
                    source_type=source,
                    fact_status=row.fact_status,
                    created_at=row.created_at,
                )
            )

        # total count (same filters, no pagination)
        all_rows = list_fact_records(db, fact_type=fact_type, keyword=keyword, limit=10000, offset=0)
        total = len(all_rows)

        return L3FactListResponse(items=items, total=total)
    finally:
        db.close()
