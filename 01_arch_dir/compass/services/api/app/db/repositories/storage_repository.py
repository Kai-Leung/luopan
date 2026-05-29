from __future__ import annotations

from app.db.base import Base
from app.db.session import engine


def ensure_minimal_storage_tables(*, include_fact_records: bool = False) -> None:
    if include_fact_records:
        _include_fact_record_table()
    else:
        _exclude_fact_record_table()

    Base.metadata.create_all(bind=engine)


def _include_fact_record_table() -> None:
    from app.db.models import FactRecord

    if "fact_records" not in Base.metadata.tables:
        FactRecord.__table__.to_metadata(Base.metadata)


def _exclude_fact_record_table() -> None:
    table = Base.metadata.tables.get("fact_records")
    if table is not None:
        Base.metadata.remove(table)
