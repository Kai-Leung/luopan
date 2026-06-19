"""External collaboration intake contracts."""

from typing import Literal

from pydantic import BaseModel, Field


ExternalFeedbackType = Literal[
    "customer_feedback",
    "partner_receipt",
    "external_document",
    "external_status",
]


class ExternalFeedbackIntakeRequest(BaseModel):
    external_source: str = Field(min_length=1, max_length=160)
    source_reference: str = Field(min_length=1, max_length=500)
    feedback_type: ExternalFeedbackType
    content: str = Field(min_length=1, max_length=20000)
    attachment_refs: list[str] = Field(default_factory=list, max_length=50)
    project_hint: str | None = Field(default=None, max_length=160)


class ExternalFeedbackIntakeResponse(BaseModel):
    intake_id: str
    trace_ref: str
    raw_input_id: str
    input_session_id: str
    candidate_ids: list[str]
    candidate_status: Literal["new_candidate"]
    governance_required: Literal[True] = True
    creates_fact: Literal[False] = False
    next_stage: Literal["s2_governance"] = "s2_governance"
    message: str
