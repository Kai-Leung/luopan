export const RUNTIME_CONTEXT_CLAIM = {
  userId: 'user_compass_owner',
  organizationId: 'org_compass_default',
  roleId: 'owner',
} as const;

let selectedProjectId: string | null = null;

export function setRuntimeProjectId(projectId: string | null): void {
  selectedProjectId = projectId?.trim() || null;
}

export function buildRuntimeContextHeaders(): Record<string, string> {
  return {
    'X-Compass-User-Id': RUNTIME_CONTEXT_CLAIM.userId,
    'X-Compass-Organization-Id': RUNTIME_CONTEXT_CLAIM.organizationId,
    'X-Compass-Role': RUNTIME_CONTEXT_CLAIM.roleId,
    ...(selectedProjectId ? { 'X-Compass-Project-Id': selectedProjectId } : {}),
  };
}
