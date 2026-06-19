"""S1 runtime identity, organization, role, and access-scope contracts."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


ProjectScopeMode = Literal["organization", "selected_projects"]
ContextSource = Literal["controlled_claim", "development_baseline"]


class RuntimeProjectScopeItem(BaseModel):
    project_id: str
    display_name: str
    aliases: list[str] = Field(default_factory=list)


class PermissionResult(BaseModel):
    action: str
    allowed: bool
    denied_reason: Optional[str] = None


class RuntimeContextResponse(BaseModel):
    context_id: str
    user_id: str
    user_display_name: str
    organization_id: str
    organization_name: str
    role_ids: list[str]
    role_names: list[str]
    project_scope_mode: ProjectScopeMode
    project_scope: list[RuntimeProjectScopeItem]
    selected_project_id: Optional[str] = None
    allowed_actions: list[str]
    permission_results: list[PermissionResult]
    denied_reason: Optional[str] = None
    context_source: ContextSource
    is_authenticated: bool = True
