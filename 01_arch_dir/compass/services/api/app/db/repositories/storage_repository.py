from __future__ import annotations

from app.db.base import Base
from app.db.session import engine


def ensure_minimal_storage_tables(*, include_fact_records: bool = False) -> None:
    # Table creation never creates business records. Keep every mapped table in
    # metadata so test cleanup and later create_all calls remain deterministic.
    from app.db import models as _models

    _ = (_models, include_fact_records)
    Base.metadata.create_all(bind=engine)
