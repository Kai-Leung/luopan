"""AI assist intake contracts.

The API accepts an already-produced assist result and places it into L0/L1.
It does not call a model, perform governance, or create an L2 fact.
"""

from typing import Literal

from pydantic import BaseModel, Field


AssistType = Literal[
    "transcription_cleanup",
    "candidate_organization",
    "gap_hint",
    "analysis_suggestion",
]


class AiAssistCandidateIntakeRequest(BaseModel):
    model_call_ref: str = Field(min_length=1, max_length=160)
    assist_type: AssistType
    candidate_text: str = Field(min_length=1, max_length=20000)
    uncertainty_hints: list[str] = Field(default_factory=list, max_length=50)
    source_reference: str | None = Field(default=None, max_length=500)


class AiAssistCandidateIntakeResponse(BaseModel):
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
