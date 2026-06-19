/** Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/08_校验规则口径.md */

import { ENUM_CATEGORY_VALUES } from "./enums";
import { FIELD_DESCRIPTIONS } from "./fields";
import { RISK_LEVEL_VALUES } from "./risks";
import { STATUS_GROUP_VALUES } from "./statuses";

export function isKnownField(fieldName: string): boolean {
  return Object.prototype.hasOwnProperty.call(FIELD_DESCRIPTIONS, fieldName);
}

export function requireKnownField(fieldName: string): void {
  if (!isKnownField(fieldName)) {
    throw new Error(`未知字段名：${fieldName}`);
  }
}

export function isValidEnum(enumName: string, value: string): boolean {
  return Boolean(ENUM_CATEGORY_VALUES[enumName]?.includes(value));
}

export function requireValidEnum(enumName: string, value: string): void {
  if (!isValidEnum(enumName, value)) {
    throw new Error(`无效的枚举值：${value}`);
  }
}

export function isValidStatus(statusGroup: string, value: string): boolean {
  return Boolean(STATUS_GROUP_VALUES[statusGroup]?.includes(value));
}

export function requireValidStatus(statusGroup: string, value: string): void {
  if (!isValidStatus(statusGroup, value)) {
    throw new Error(`无效的状态值：${value}`);
  }
}

export function findMissingRequiredFields(
  payload: Record<string, unknown>,
  requiredFields: readonly string[],
): string[] {
  return requiredFields.filter((fieldName) => {
    requireKnownField(fieldName);
    const value = payload[fieldName];
    return value === undefined || value === null || value === "";
  });
}

export function requireRequiredFields(
  payload: Record<string, unknown>,
  requiredFields: readonly string[],
): void {
  const missingFields = findMissingRequiredFields(payload, requiredFields);
  if (missingFields.length > 0) {
    throw new Error(`缺少必填字段：${missingFields.join(",")}`);
  }
}

export function isValidRiskLevel(value: string): boolean {
  return RISK_LEVEL_VALUES.includes(value as typeof RISK_LEVEL_VALUES[number]);
}

export function requireValidRiskLevel(value: string): void {
  if (!isValidRiskLevel(value)) {
    throw new Error(`无效的风险等级：${value}`);
  }
}

export function isValidSourceType(value: string): boolean {
  return isValidEnum("source_type", value);
}

export function requireValidSourceType(value: string): void {
  requireValidEnum("source_type", value);
}

export function isValidFactType(value: string): boolean {
  return isValidEnum("fact_record_type", value);
}

export function requireValidFactType(value: string): void {
  requireValidEnum("fact_record_type", value);
}
