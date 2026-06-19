export interface H5ProjectContext {
  projectId: string;
  displayName: string;
  aliases: string[];
}

export interface H5ProjectContextMatch {
  project: H5ProjectContext;
  matchedAlias: string;
}

export interface H5ExtractedProjectContext {
  project: H5ProjectContext;
  isNew: boolean;
}

export interface RuntimePermissionResult {
  action: string;
  allowed: boolean;
  denied_reason?: string;
}

export interface RuntimeContextResponse {
  context_id: string;
  user_id: string;
  user_display_name: string;
  organization_id: string;
  organization_name: string;
  role_ids: string[];
  role_names: string[];
  project_scope_mode: 'organization' | 'selected_projects';
  project_scope: Array<{
    project_id: string;
    display_name: string;
    aliases: string[];
  }>;
  selected_project_id?: string;
  allowed_actions: string[];
  permission_results: RuntimePermissionResult[];
  denied_reason?: string;
  context_source: 'controlled_claim' | 'development_baseline';
  is_authenticated: boolean;
}
