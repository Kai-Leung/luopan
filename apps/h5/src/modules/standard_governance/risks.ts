/** Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/07_风险分级口径.md */

export enum RiskLevel {
  NONE = "none",
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  BLOCKING = "blocking",
}

export const RISK_LEVEL_VALUES = [
  RiskLevel.NONE,
  RiskLevel.LOW,
  RiskLevel.MEDIUM,
  RiskLevel.HIGH,
  RiskLevel.BLOCKING,
] as const;

// 07_风险分级口径.md 定义了风险触发来源和高风险事项表，但未定义受控关键词表。
// 后续如需关键词识别，应由任务依据开发依据另行落位，不得在此处自行编造。
export const RISK_KEYWORD_MAPPING: Record<RiskLevel, readonly string[]> = {
  [RiskLevel.NONE]: [],
  [RiskLevel.LOW]: [],
  [RiskLevel.MEDIUM]: [],
  [RiskLevel.HIGH]: [],
  [RiskLevel.BLOCKING]: [],
};

export const RISK_KEYWORD_TODO =
  "07_风险分级口径.md 定义风险类型和处理口径，未定义可直接用于自动识别的受控关键词表。";
