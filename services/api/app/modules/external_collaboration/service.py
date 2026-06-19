"""Controlled external collaboration feedback intake."""

from hashlib import sha256
from uuid import uuid4

from app.modules.external_collaboration.schemas import (
    ExternalFeedbackIntakeRequest,
    ExternalFeedbackIntakeResponse,
)
from app.modules.l0_input.schemas import RawInputCreate
from app.modules.l0_input.service import receive_raw_input
from app.modules.l1_candidate.schemas import L1CandidateCreate
from app.modules.l1_candidate.service import create_candidate
from app.modules.s3_audit_trace.service import new_trace_ref, record_trace_event
from app.modules.standard_governance.enums.source_types import SourceType


def intake_external_feedback(
    payload: ExternalFeedbackIntakeRequest,
) -> ExternalFeedbackIntakeResponse:
    intake_id = f"external_intake_{uuid4().hex}"
    trace_ref = new_trace_ref()
    raw_payload = {
        "text": payload.content,
        "external_collaboration": {
            "intake_id": intake_id,
            "external_source": payload.external_source,
            "source_reference": payload.source_reference,
            "feedback_type": payload.feedback_type,
            "attachment_refs": payload.attachment_refs,
            "project_hint": payload.project_hint,
        },
        "_trace_ref": trace_ref,
    }
    raw = receive_raw_input(
        RawInputCreate(
            text=payload.content,
            idempotency_key="external:" + sha256(
                (
                    f"{payload.external_source}|{payload.source_reference}"
                ).encode("utf-8")
            ).hexdigest(),
            source_type=SourceType.EXTERNAL_COLLABORATION,
        )
    )
    candidate = create_candidate(
        L1CandidateCreate(
            raw_input_id=raw.raw_input_id,
            input_session_id=raw.input_session_id,
            raw_payload=raw_payload,
            source_type=SourceType.EXTERNAL_COLLABORATION,
        )
    )
    candidate_ids = [item.candidate_id for item in candidate.candidates]
    record_trace_event(
        trace_ref=trace_ref,
        raw_input_id=raw.raw_input_id,
        candidate_id=candidate.candidate_id,
        source_stage="external_collaboration",
        target_stage="l0_l1_candidate",
        action_type="external_feedback_intake",
    )
    return ExternalFeedbackIntakeResponse(
        intake_id=intake_id,
        trace_ref=trace_ref,
        raw_input_id=raw.raw_input_id,
        input_session_id=raw.input_session_id,
        candidate_ids=candidate_ids,
        candidate_status=candidate.candidate_status,
        message="external feedback entered L0/L1 and requires S2 governance",
    )
