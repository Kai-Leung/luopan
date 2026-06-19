from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.models import Candidate, GovernanceResult, ManualReview, RawInput


CODE_ROOT = Path(__file__).resolve().parents[4]
DEVELOPMENT_DATABASE_PATH = CODE_ROOT / "data" / "dev" / "compass_dev.sqlite3"
DEVELOPMENT_DATABASE_URL = f"sqlite:///{DEVELOPMENT_DATABASE_PATH}"
TEST_DATABASE_URL = "sqlite:///:memory:"
PRODUCTION_ENV_VALUES = {"production", "prod"}
TEST_ENV_VALUES = {"test", "testing"}


def _is_running_under_pytest() -> bool:
    return "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ


def _ensure_sqlite_parent_dir(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    database_path = database_url.removeprefix("sqlite:///")
    if database_path == ":memory:":
        return
    Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def resolve_database_url(
    *,
    app_env: Optional[str] = None,
    explicit_database_url: Optional[str] = None,
) -> str:
    resolved_env = (app_env if app_env is not None else settings.APP_ENV).strip().lower()
    resolved_url = (
        explicit_database_url
        if explicit_database_url is not None
        else os.getenv("COMPASS_DATABASE_URL") or settings.DATABASE_URL
    )

    if resolved_url and resolved_url.strip():
        return resolved_url.strip()

    if resolved_env in PRODUCTION_ENV_VALUES:
        raise RuntimeError("DATABASE_URL must be configured outside development")

    if resolved_env in TEST_ENV_VALUES:
        return TEST_DATABASE_URL

    if app_env is None and explicit_database_url is None and _is_running_under_pytest():
        return TEST_DATABASE_URL

    _ensure_sqlite_parent_dir(DEVELOPMENT_DATABASE_URL)
    return DEVELOPMENT_DATABASE_URL


DATABASE_URL = resolve_database_url()

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine_kwargs = {"connect_args": connect_args}

if DATABASE_URL == TEST_DATABASE_URL:
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
