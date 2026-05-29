"""标准治理只读约束层：基础校验函数
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/08_校验规则口径.md
注意：本文件只提供只读基础校验函数，不执行 S2，不生成治理结果。
"""
from typing import Optional

from typing import Any, Mapping, Sequence

from .enums.fact_types import ENUM_CATEGORY_MAP, KNOWN_ENUM_CATEGORIES
from .rules.field_rules import (
    FIELD_CONDITIONAL_RULES,
    FIELD_REQUIRED_RULES,
    find_missing_by_field_rules,
)
from .display.fields import KNOWN_FIELD_NAMES
from .rules.risk_rules import RISK_LEVEL_VALUES
from .enums.status_types import KNOWN_STATUS_GROUPS, STATUS_GROUP_MAP


def is_valid_enum(enum_name: str, value: str) -> bool:
    enum_class = ENUM_CATEGORY_MAP.get(enum_name)
    if enum_class is None:
        return False
    return value in enum_class._value2member_map_


def require_valid_enum(enum_name: str, value: str) -> None:
    if not is_valid_enum(enum_name, value):
        enum_class = ENUM_CATEGORY_MAP.get(enum_name)
        valid_values = list(enum_class._value2member_map_.keys()) if enum_class else []
        raise ValueError(
            f"无效的枚举值 {value!r}，枚举分类 {enum_name!r} 的可选值：{valid_values}"
        )


def is_valid_status(status_group: str, value: str) -> bool:
    status_class = STATUS_GROUP_MAP.get(status_group)
    if status_class is None:
        return False
    return value in status_class._value2member_map_


def require_valid_status(status_group: str, value: str) -> None:
    if not is_valid_status(status_group, value):
        status_class = STATUS_GROUP_MAP.get(status_group)
        valid_values = list(status_class._value2member_map_.keys()) if status_class else []
        raise ValueError(
            f"无效的状态值 {value!r}，状态组 {status_group!r} 的可选值：{valid_values}"
        )


def is_known_enum_name(enum_name: str) -> bool:
    return enum_name in KNOWN_ENUM_CATEGORIES


def is_known_status_group(status_group: str) -> bool:
    return status_group in KNOWN_STATUS_GROUPS


def is_known_field(field_name: str) -> bool:
    return field_name in KNOWN_FIELD_NAMES


def require_known_field(field_name: str) -> None:
    if not is_known_field(field_name):
        raise ValueError(f"未知字段名：{field_name!r}")


def find_missing_required_fields(
    payload: Mapping[str, Any],
    required_fields: Sequence[str],
) -> list[str]:
    missing_fields = []
    for field_name in required_fields:
        require_known_field(field_name)
        value = payload.get(field_name)
        if value is None or value == "":
            missing_fields.append(field_name)
    return missing_fields


def find_missing_field_rule_fields(
    payload: Mapping[str, Any],
    *,
    text: str = "",
    fact_record_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    source_type: Optional[str] = None,
) -> list[str]:
    for field_name in FIELD_REQUIRED_RULES:
        require_known_field(field_name)
    for rule in FIELD_CONDITIONAL_RULES:
        require_known_field(str(rule["field_name"]))
    return find_missing_by_field_rules(
        payload,
        text=text,
        fact_record_type=fact_record_type,
        risk_level=risk_level,
        source_type=source_type,
    )


def require_required_fields(
    payload: Mapping[str, Any],
    required_fields: Sequence[str],
) -> None:
    missing_fields = find_missing_required_fields(payload, required_fields)
    if missing_fields:
        raise ValueError(f"缺少必填字段：{missing_fields}")


def is_valid_risk_level(value: str) -> bool:
    return value in RISK_LEVEL_VALUES


def require_valid_risk_level(value: str) -> None:
    if not is_valid_risk_level(value):
        raise ValueError(f"无效的风险等级：{value!r}")


def is_valid_source_type(value: str) -> bool:
    return is_valid_enum("source_type", value)


def require_valid_source_type(value: str) -> None:
    require_valid_enum("source_type", value)


def is_valid_fact_type(value: str) -> bool:
    return is_valid_enum("fact_record_type", value)


def require_valid_fact_type(value: str) -> None:
    require_valid_enum("fact_record_type", value)
