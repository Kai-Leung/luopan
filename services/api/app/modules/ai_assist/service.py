"""Controlled AI assist intake service."""

from hashlib import sha256
from uuid import uuid4

from app.modules.ai_assist.schemas import (
    AiAssistCandidateIntakeRequest,
    AiAssistCandidateIntakeResponse,
)
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.enums.source_types import SourceType


def intake_ai_assist_candidate(
    payload: AiAssistCandidateIntakeRequest,
) -> AiAssistCandidateIntakeResponse:
    intake_id = f"ai_intake_{uuid4().hex}"
    trace_ref = new_trace_ref()
    raw_payload = {
        "text": payload.candidate_text,
        "ai_assist": {
            "intake_id": intake_id,
            "model_call_ref": payload.model_call_ref,
            "assist_type": payload.assist_type,
            "uncertainty_hints": payload.uncertainty_hints,
            "source_reference": payload.source_reference,
        },
        "_trace_ref": trace_ref,
    }
    raw = receive_raw_input(
        RawInputCreate(
            text=payload.candidate_text,
            idempotency_key=(
                "ai:"
                f"{sha256(payload.model_call_ref.encode('utf-8')).hexdigest()}"
            ),
            source_type=SourceType.AI_ASSISTED,
        )
    )
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            input_session_id=raw.input_session_id,
            raw_payload=raw_payload,
            source_type=SourceType.AI_ASSISTED,
        )
    )
    candidate_ids = [item.candidate_id for item in candidate.candidates]
    record_trace_event(
        trace_ref=trace_ref,
        raw_input_id=raw.raw_input_id,
        candidate_id=candidate.candidate_id,
        source_stage="ai_assist",
        target_stage="l0_l1_candidate",
        action_type="ai_assist_candidate_intake",
    )
    return AiAssistCandidateIntakeResponse(
        intake_id=intake_id,
        trace_ref=trace_ref,
        raw_input_id=raw.raw_input_id,
        input_session_id=raw.input_session_id,
        candidate_ids=candidate_ids,
        candidate_status=candidate.candidate_status,
        message="AI assist output entered L0/L1 and requires S2 governance",
    )
