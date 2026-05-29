"""L3 正式事实只读视图服务。

只读取 L2 fact_records，不创建、修改、删除正式事实。
"""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.db.repositories import get_fact_record, load_json_field
from app.db.session import SessionLocal
from app.modules.l3_query_view.schemas import L3FactViewResponse

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

        return L3FactViewResponse(
            fact_id=row.fact_id,
            fact_type=row.fact_type,
            fact_payload=fact_payload,
            fact_status=row.fact_status,
            created_at=row.created_at,
        )
    finally:
        db.close()
