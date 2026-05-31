from fastapi import APIRouter

from app.modules.l0_input.router import router as l0_input_router
from app.modules.l1_candidate.router import router as l1_candidate_router
from app.modules.l2_fact.router import router as l2_fact_router
from app.modules.l3_query_view.router import router as l3_query_view_router
from app.modules.l4_analysis.api import router as l4_analysis_router
from app.modules.l5_recommendation.api import router as l5_recommendation_router
from app.modules.l6_execution.api import router as l6_execution_router
from app.modules.l7_feedback.api import router as l7_feedback_router
from app.modules.s3_audit_trace.api import router as s3_audit_trace_router
from app.modules.s2_governance_gate.confirmation.router import router as confirmation_router
from app.modules.s2_governance_gate.router import router as s2_governance_gate_router
from app.modules.upload.api import router as upload_router
from app.modules.voice_transcription.router import router as voice_transcription_router

router = APIRouter()
router.include_router(l0_input_router)
router.include_router(l1_candidate_router)
router.include_router(s2_governance_gate_router)
router.include_router(confirmation_router)
router.include_router(l2_fact_router)
router.include_router(l3_query_view_router)
router.include_router(l4_analysis_router)
router.include_router(l5_recommendation_router)
router.include_router(l6_execution_router)
router.include_router(l7_feedback_router)
router.include_router(s3_audit_trace_router)
router.include_router(upload_router)
router.include_router(voice_transcription_router)
