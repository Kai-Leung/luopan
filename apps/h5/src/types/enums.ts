/**
 * 前端全局类型边界。
 *
 * 本目录不承载业务治理规则、字段规则、枚举标准或 S2 决策口径。
 * 全局标准治理规则统一归口到 apps/h5/src/modules/standard_governance。
 */

export type LegacyUnderstandingRecordType =
  | "construction"
  | "communication"
  | "finance"
  | "material"
  | "document"
  | "risk"
  | "change"
  | "confirmation"
  | "unknown";

export const RECORD_TYPES_LABELS: Record<LegacyUnderstandingRecordType, string> = {
  construction: "施工现场",
  communication: "沟通记录",
  finance: "财务记录",
  material: "材料记录",
  document: "文档记录",
  risk: "风险问题",
  change: "变更记录",
  confirmation: "确认记录",
  unknown: "未分类",
};
