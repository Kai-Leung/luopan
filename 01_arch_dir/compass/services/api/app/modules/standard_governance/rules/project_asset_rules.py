"""项目资产创建候选规则。

本文件只定义项目创建候选识别与候选字段，不创建正式项目资产。
"""

import re
from typing import Any, Mapping

PROJECT_ASSET_CANDIDATE_KIND = "project_asset_candidate"
PROJECT_ASSET_PERMISSION = "project_asset:create"
PROJECT_ASSET_TYPE = "project_asset"

PROJECT_CREATE_INTENT_KEYWORDS = (
    "新建项目",
    "新建一个项目",
    "创建项目",
    "创建一个项目",
    "新增项目",
    "新增一个项目",
    "新开一个项目",
    "立项",
    "建个项目",
    "开一个工地",
    "新项目叫",
)

PROJECT_ASSET_REQUIRED_FIELDS = (
    "project_name",
    "customer_name",
    "project_address",
)


def is_project_asset_create_intent(text: str) -> bool:
    return any(keyword in text for keyword in PROJECT_CREATE_INTENT_KEYWORDS)


def extract_project_asset_name(text: str) -> str:
    for pattern in (
        r"(?:新项目叫|项目叫|项目名称是|项目名是)([^，。；,\s]+)",
        r"(?:新建|创建|新增|立项)(?:一个)?项目(?:叫|为|是)?([^，。；,\s]+)",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return ""


def extract_project_customer_name(text: str) -> str:
    for pattern in (
        r"(?:客户|业主|甲方)(?:是|叫|为)?([^，。；,\s]+)",
        r"([^，。；,\s]+)(?:客户|业主|甲方)",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return ""


def extract_project_address(text: str) -> str:
    for pattern in (
        r"(?:地址|位置|地点)(?:是|在|为)?([^，。；,\s]+)",
        r"在([^，。；,\s]+)(?:新建|创建|新增|立项|开一个工地|建个项目)",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return ""


def build_project_asset_candidate_fields(text: str) -> dict[str, str]:
    fields = {
        "candidate_type": PROJECT_ASSET_CANDIDATE_KIND,
        "asset_type": PROJECT_ASSET_TYPE,
        "required_permission": PROJECT_ASSET_PERMISSION,
        "project_asset_action": "create_project",
        "raw_text": text,
        "fact_record_type": "other_fact_record",
    }
    project_name = extract_project_asset_name(text)
    customer_name = extract_project_customer_name(text)
    project_address = extract_project_address(text)
    if project_name:
        fields["project_name"] = project_name
    if customer_name:
        fields["customer_name"] = customer_name
    if project_address:
        fields["project_address"] = project_address
    fields["candidate_summary"] = _build_project_asset_summary(fields, text)
    return fields


def is_project_asset_candidate(candidate_payload: Mapping[str, Any]) -> bool:
    return candidate_payload.get("candidate_type") == PROJECT_ASSET_CANDIDATE_KIND


def find_missing_project_asset_fields(candidate_payload: Mapping[str, Any]) -> list[str]:
    return [
        field_name
        for field_name in PROJECT_ASSET_REQUIRED_FIELDS
        if not _has_non_empty_string(candidate_payload.get(field_name))
    ]


def _build_project_asset_summary(fields: Mapping[str, str], text: str) -> str:
    summary_parts = [
        fields.get("project_name", ""),
        fields.get("customer_name", ""),
        fields.get("project_address", ""),
    ]
    summary = "；".join(part for part in summary_parts if part)
    if summary:
        return f"项目创建候选：{summary}"
    return f"项目创建候选：{text[:40]}"


def _has_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
