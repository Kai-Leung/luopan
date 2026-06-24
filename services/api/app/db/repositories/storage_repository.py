from __future__ import annotations

from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import engine


def ensure_minimal_storage_tables(*, include_fact_records: bool = False) -> None:
    # Table creation never creates business records. Keep every mapped table in
    # metadata so test cleanup and later create_all calls remain deterministic.
    from app.db import models as _models

    _ = (_models, include_fact_records)
    Base.metadata.create_all(bind=engine)
    _upgrade_pending_confirmations_table()


def _upgrade_pending_confirmations_table() -> None:
    inspector = inspect(engine)
    if "pending_confirmations" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("pending_confirmations")
    }
    column_definitions = {
        "pending_status": "VARCHAR NOT NULL DEFAULT 'active'",
        "resolved_at": "DATETIME",
        "review_id": "VARCHAR",
        "resolved_action": "VARCHAR",
    }
    missing_columns = [
        (column_name, definition)
        for column_name, definition in column_definitions.items()
        if column_name not in existing_columns
    ]
    if missing_columns and engine.dialect.name != "sqlite":
        raise RuntimeError(
            "pending_confirmations schema upgrade requires an explicit migration "
            f"for database dialect {engine.dialect.name}"
        )
    if engine.dialect.name != "sqlite":
        return

    with engine.begin() as connection:
        for column_name, definition in missing_columns:
            connection.execute(
                text(
                    f'ALTER TABLE pending_confirmations '
                    f'ADD COLUMN "{column_name}" {definition}'
                )
            )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS "
                "ix_pending_confirmations_pending_status "
                "ON pending_confirmations (pending_status)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS "
                "ix_pending_confirmations_review_id "
                "ON pending_confirmations (review_id)"
            )
        )
