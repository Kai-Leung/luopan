"""Controlled S1 runtime-context baseline.

This is intentionally not a complete account or multi-tenant system. It
validates a small, explicit identity registry and exposes backend-owned action
decisions for the current single-organization phase.
"""

from __future__ import annotations

from contextvars import ContextVar
from hashlib import sha256
from typing import AsyncIterator, Optional

from fastapi import Header, HTTPException, Request

from app.core.config import settings
from app.modules.s1_runtime_context.schemas import (
    PermissionResult,
    RuntimeContextResponse,
    RuntimeProjectScopeItem,
)


DEFAULT_USER_ID = "user_compass_owner"
DEFAULT_ORGANIZATION_ID = "org_compass_default"
DEFAULT_ROLE_ID = "owner"

ROLE_ALLOWED_ACTIONS = {
    "owner": {
        "s1:read",
        "l0:submit",
        "l1:create",
        "s2:check",
        "confirmation:manage",
        "l2:create",
        "l3:read",
        "l4:read",
        "l5:create_draft",
        "l6:respond",
        "l7:submit_feedback",
        "s3:read",
        "upload:create",
        "voice:transcribe",
        "project_asset:create",
        "ai_assist:intake",
        "external_collaboration:intake",
    }
}

CONTROLLED_IDENTITIES = {
    (DEFAULT_USER_ID, DEFAULT_ORGANIZATION_ID, DEFAULT_ROLE_ID): {
        "user_display_name": "罗盘负责人",
        "organization_name": "罗盘默认组织",
        "role_name": "负责人",
    }
}

REQUEST_ACTIONS = {
    ("POST", "/api/v1/l0/raw-input"): "l0:submit",
    ("POST", "/api/v1/l1/candidates"): "l1:create",
    ("POST", "/api/v1/s2/governance/check"): "s2:check",
    ("POST", "/api/v1/manual-confirmation/pending"): "confirmation:manage",
    ("GET", "/api/v1/manual-confirmation/pending"): "confirmation:manage",
    ("POST", "/api/v1/manual-confirmation/review"): "confirmation:manage",
    ("POST", "/api/v1/l2/source-of-truth/facts"): "l2:create",
    ("GET", "/api/v1/l3/facts"): "l3:read",
    ("GET", "/api/v1/l4/analysis/preview"): "l4:read",
    ("POST", "/api/v1/l5/recommendations/draft"): "l5:create_draft",
    ("POST", "/api/v1/l6/execution-responses"): "l6:respond",
    ("POST", "/api/v1/l7/feedback"): "l7:submit_feedback",
    ("GET", "/api/v1/s3/trace/summary"): "s3:read",
    ("POST", "/api/v1/upload/files"): "upload:create",
    ("POST", "/api/v1/voice-transcription/transcribe"): "voice:transcribe",
    ("POST", "/api/v1/ai-assist/candidates/intake"): "ai_assist:intake",
    (
        "POST",
        "/api/v1/external-collaboration/feedback/intake",
    ): "external_collaboration:intake",
}

_CURRENT_RUNTIME_CONTEXT: ContextVar[Optional[RuntimeContextResponse]] = ContextVar(
    "compass_runtime_context",
    default=None,
)


def resolve_runtime_context(
    *,
    user_id: Optional[str],
    organization_id: Optional[str],
    role_id: Optional[str],
    selected_project_id: Optional[str],
) -> RuntimeContextResponse:
    supplied = [user_id, organization_id, role_id]
    if any(supplied) and not all(supplied):
        raise HTTPException(
            status_code=400,
            detail="user, organization, and role context headers must be supplied together",
        )

    context_source = "controlled_claim"
    if not any(supplied):
        if settings.APP_ENV.strip().lower() in {"production", "prod"}:
            raise HTTPException(status_code=401, detail="runtime context is required")
        user_id = DEFAULT_USER_ID
        organization_id = DEFAULT_ORGANIZATION_ID
        role_id = DEFAULT_ROLE_ID
        context_source = "development_baseline"

    identity = CONTROLLED_IDENTITIES.get((user_id, organization_id, role_id))
    if identity is None:
        raise HTTPException(status_code=403, detail="runtime context is outside the allowed scope")

    allowed_actions = sorted(ROLE_ALLOWED_ACTIONS.get(role_id, set()))
    context_id = _build_context_id(
        user_id=user_id,
        organization_id=organization_id,
        role_id=role_id,
        selected_project_id=selected_project_id,
    )
    return RuntimeContextResponse(
        context_id=context_id,
        user_id=user_id,
        user_display_name=identity["user_display_name"],
        organization_id=organization_id,
        organization_name=identity["organization_name"],
        role_ids=[role_id],
        role_names=[identity["role_name"]],
        project_scope_mode="organization",
        project_scope=[],
        selected_project_id=selected_project_id,
        allowed_actions=allowed_actions,
        permission_results=[
            PermissionResult(action=action, allowed=True)
            for action in allowed_actions
        ],
        context_source=context_source,
    )


async def require_runtime_context(
    request: Request,
    user_id: Optional[str] = Header(None, alias="X-Compass-User-Id"),
    organization_id: Optional[str] = Header(None, alias="X-Compass-Organization-Id"),
    role_id: Optional[str] = Header(None, alias="X-Compass-Role"),
    selected_project_id: Optional[str] = Header(None, alias="X-Compass-Project-Id"),
) -> AsyncIterator[RuntimeContextResponse]:
    context = resolve_runtime_context(
        user_id=user_id,
        organization_id=organization_id,
        role_id=role_id,
        selected_project_id=selected_project_id,
    )
    required_action = _required_action(request.method, request.url.path)
    if required_action and required_action not in context.allowed_actions:
        raise HTTPException(
            status_code=403,
            detail=f"permission denied: {required_action}",
        )

    request.state.runtime_context = context
    token = _CURRENT_RUNTIME_CONTEXT.set(context)
    try:
        yield context
    finally:
        _CURRENT_RUNTIME_CONTEXT.reset(token)


def get_current_runtime_context() -> RuntimeContextResponse:
    context = _CURRENT_RUNTIME_CONTEXT.get()
    if context is not None:
        return context
    return resolve_runtime_context(
        user_id=None,
        organization_id=None,
        role_id=None,
        selected_project_id=None,
    )


def runtime_context_snapshot() -> dict:
    context = get_current_runtime_context()
    return {
        "context_id": context.context_id,
        "user_id": context.user_id,
        "organization_id": context.organization_id,
        "role_ids": context.role_ids,
        "selected_project_id": context.selected_project_id,
        "context_source": context.context_source,
    }


def ensure_payload_in_current_scope(payload: dict, *, allow_legacy_baseline: bool = True) -> None:
    context = get_current_runtime_context()
    snapshot = payload.get("_runtime_context")
    if not isinstance(snapshot, dict):
        if allow_legacy_baseline and context.context_source == "development_baseline":
            return
        raise HTTPException(status_code=403, detail="record runtime context is missing")
    if snapshot.get("organization_id") != context.organization_id:
        raise HTTPException(status_code=403, detail="cross-organization access is blocked")
    selected_project_id = context.selected_project_id
    payload_project_id = snapshot.get("selected_project_id")
    if selected_project_id and payload_project_id and selected_project_id != payload_project_id:
        raise HTTPException(status_code=403, detail="cross-project access is blocked")


def _required_action(method: str, path: str) -> Optional[str]:
    direct = REQUEST_ACTIONS.get((method.upper(), path))
    if direct:
        return direct
    if method.upper() == "GET" and path.startswith("/api/v1/l3/facts/"):
        return "l3:read"
    return None


def _build_context_id(
    *,
    user_id: str,
    organization_id: str,
    role_id: str,
    selected_project_id: Optional[str],
) -> str:
    raw = "|".join((user_id, organization_id, role_id, selected_project_id or ""))
    return f"context_{sha256(raw.encode('utf-8')).hexdigest()[:24]}"
