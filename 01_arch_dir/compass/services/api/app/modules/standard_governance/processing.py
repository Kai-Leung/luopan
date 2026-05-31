"""Shared processing standards for horizontal governance."""

from datetime import datetime
from typing import Literal, Optional
from uuid import uuid4

from pydantic import BaseModel

TRACE_REF_PREFIX = "trace_"

PROCESSING_DIRECTION_READONLY = "readonly"
PROCESSING_DIRECTION_DRAFT = "draft"
PROCESSING_DIRECTION_RESPONSE = "response"
PROCESSING_DIRECTION_CANDIDATE = "candidate"
PROCESSING_DIRECTION_BLOCKED = "blocked"
PROCESSING_DIRECTION_NEED_SUPPLEMENT = "need_supplement"
PROCESSING_DIRECTION_NEED_CONFIRMATION = "need_confirmation"
PROCESSING_DIRECTION_FAILED = "failed"

StandardProcessingDirection = Literal[
    "readonly",
    "draft",
    "response",
    "candidate",
    "blocked",
    "need_supplement",
    "need_confirmation",
    "failed",
]


class StandardErrorResult(BaseModel):
    error_code: str
    message: str
    processing_direction: StandardProcessingDirection = "failed"


class StandardSourceRef(BaseModel):
    source_stage: str
    source_id: str


class StandardTraceRef(BaseModel):
    trace_ref: str
    source_fact_id: Optional[str] = None
    created_at: datetime


class StandardBoundaryNotice(BaseModel):
    processing_direction: StandardProcessingDirection
    readonly: bool = True
    no_write_l2: bool = True
    message: str


def build_trace_ref() -> str:
    """Create a non-persistent trace reference for readonly governance outputs."""
    return f"{TRACE_REF_PREFIX}{uuid4().hex}"
