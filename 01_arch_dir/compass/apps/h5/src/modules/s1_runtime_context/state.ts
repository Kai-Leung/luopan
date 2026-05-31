import type { H5ProjectContext, H5ProjectContextMatch } from './types';

export const H5_PROJECT_CONTEXTS: H5ProjectContext[] = [];

export function findProjectContextMatches(
  text: string,
  projects: H5ProjectContext[] = H5_PROJECT_CONTEXTS,
): H5ProjectContextMatch[] {
  const normalizedText = normalizeProjectName(text);
  if (!normalizedText) return [];

  return projects.flatMap((project) => {
    const matchedAlias = project.aliases.find((alias) => {
      const normalizedAlias = normalizeProjectName(alias);
      return normalizedAlias && normalizedText.includes(normalizedAlias);
    });
    return matchedAlias ? [{ project, matchedAlias }] : [];
  });
}

export function createLocalProjectContext(displayName: string): H5ProjectContext {
  const normalizedName = displayName.trim();
  return {
    projectId: `local_project_${Date.now()}`,
    displayName: normalizedName,
    aliases: buildProjectAliases(normalizedName),
  };
}

export function normalizeProjectName(value: string): string {
  return value
    .trim()
    .replace(/项目|工地|现场/g, '')
    .replace(/\s+/g, '')
    .toLowerCase();
}

function buildProjectAliases(displayName: string): string[] {
  const normalizedName = displayName.trim();
  const shortName = normalizedName.replace(/项目|工地|现场/g, '').trim();
  return Array.from(new Set([normalizedName, shortName, `${shortName}项目`, `${shortName}工地`]))
    .filter((item) => item.trim().length > 0);
}
