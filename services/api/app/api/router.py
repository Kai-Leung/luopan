from fastapi import APIRouter, Depends

from app.modules.ai_assist.api import router as ai_assist_router
from app.modules.external_collaboration.api import router as external_collaboration_router
from app.modules.l0_input.router import router as l0_input_router
from app.modules.l1_candidate.router import router as l1_candidate_router
from app.modules.l2_fact.router import router as l2_fact_router
from app.modules.l3_query_view.router import router as l3_query_view_router
from app.modules.l4_analysis.api import router as l4_analysis_router
from app.modules.l5_recommendation.api import router as l5_recommendation_router
from app.modules.l6_execution.api import router as l6_execution_router
from app.modules.l7_feedback.api import router as l7_feedback_router
from app.modules.s3_audit_trace.api import router as s3_audit_trace_router
from app.modules.s1_runtime_context.api import router as s1_runtime_context_router
from app.modules.s1_runtime_context.service import require_runtime_context
from app.modules.s2_governance_gate.confirmation.router import router as confirmation_router
from app.modules.s2_governance_gate.router import router as s2_governance_gate_router
from app.modules.upload.api import router as upload_router
from app.modules.voice_transcription.router import router as voice_transcription_router

router = APIRouter()
router.include_router(s1_runtime_context_router)

business_router = APIRouter(dependencies=[Depends(require_runtime_context)])
business_router.include_router(l0_input_router)
business_router.include_router(l1_candidate_router)
business_router.include_router(s2_governance_gate_router)
business_router.include_router(confirmation_router)
business_router.include_router(l2_fact_router)
business_router.include_router(l3_query_view_router)
business_router.include_router(l4_analysis_router)
business_router.include_router(l5_recommendation_router)
business_router.include_router(l6_execution_router)
business_router.include_router(l7_feedback_router)
business_router.include_router(s3_audit_trace_router)
business_router.include_router(upload_router)
business_router.include_router(voice_transcription_router)
business_router.include_router(ai_assist_router)
business_router.include_router(external_collaboration_router)
router.include_router(business_router)
