"""S1 runtime-context API."""

from typing import Optional

from fastapi import APIRouter, Header

from app.modules.s1_runtime_context.schemas import RuntimeContextResponse
from app.modules.s1_runtime_context.service import resolve_runtime_context


router = APIRouter(prefix="/s1/runtime-context", tags=["s1-runtime-context"])


@router.get("/current", response_model=RuntimeContextResponse)
def current_runtime_context(
    user_id: Optional[str] = Header(None, alias="X-Compass-User-Id"),
    organization_id: Optional[str] = Header(None, alias="X-Compass-Organization-Id"),
    role_id: Optional[str] = Header(None, alias="X-Compass-Role"),
    selected_project_id: Optional[str] = Header(None, alias="X-Compass-Project-Id"),
) -> RuntimeContextResponse:
    return resolve_runtime_context(
        user_id=user_id,
        organization_id=organization_id,
        role_id=role_id,
        selected_project_id=selected_project_id,
    )
