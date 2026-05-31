export interface H5ProjectContext {
  projectId: string;
  displayName: string;
  aliases: string[];
}

export interface H5ProjectContextMatch {
  project: H5ProjectContext;
  matchedAlias: string;
}
