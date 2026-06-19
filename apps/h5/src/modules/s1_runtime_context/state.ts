import type { H5ExtractedProjectContext, H5ProjectContext, H5ProjectContextMatch } from './types';

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

export function extractProjectContextFromText(
  text: string,
  projects: H5ProjectContext[] = H5_PROJECT_CONTEXTS,
): H5ExtractedProjectContext | null {
  const matches = findProjectContextMatches(text, projects);
  if (matches.length === 1) {
    return { project: matches[0].project, isNew: false };
  }
  if (matches.length > 1) return null;

  const projectName = extractProjectName(text);
  if (!projectName) return null;

  const exactMatch = projects.find((project) => normalizeProjectName(project.displayName) === normalizeProjectName(projectName));
  if (exactMatch) return { project: exactMatch, isNew: false };

  return { project: createLocalProjectContext(projectName), isNew: true };
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

function extractProjectName(text: string): string | null {
  const normalizedText = text.trim();
  const patterns = [
    /([\u4e00-\u9fa5A-Za-z0-9]{2,24}(?:项目|工地|现场|地块|楼栋))/,
    /([\u4e00-\u9fa5]{1,8}老师家)/,
  ];
  for (const pattern of patterns) {
    const match = normalizedText.match(pattern);
    if (match?.[1]) return cleanExtractedProjectName(match[1]);
  }
  return null;
}

function cleanExtractedProjectName(value: string): string {
  const cleanedValue = value.trim();
  const separators = ["在", "到", "去", "给", "把", "从", "于", "：", ":"];
  const lastSeparatorIndex = Math.max(...separators.map((separator) => cleanedValue.lastIndexOf(separator)));
  if (lastSeparatorIndex >= 0 && lastSeparatorIndex < cleanedValue.length - 1) {
    return cleanedValue.slice(lastSeparatorIndex + 1).trim();
  }
  return cleanedValue;
}
