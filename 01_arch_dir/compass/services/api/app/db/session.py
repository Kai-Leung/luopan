import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.models import Candidate, GovernanceResult, ManualReview, RawInput

DEVELOPMENT_DATABASE_URL = "sqlite:///:memory:"
PRODUCTION_ENV_VALUES = {"production", "prod"}


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
    return DEVELOPMENT_DATABASE_URL


DATABASE_URL = resolve_database_url()

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine_kwargs = {"connect_args": connect_args}

if DATABASE_URL == "sqlite:///:memory:":
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
