"""L1 候选字段抽取工具。"""

import re

from app.modules.standard_governance.rules.field_rules import (
    L1_FIELD_EXTRACTION_RULES,
    L1_ISSUE_KEYWORD_RULES,
)
from app.modules.standard_governance.rules.fact_record_types import classify_fact_record_type
from app.modules.standard_governance.rules.project_asset_rules import (
    build_project_asset_candidate_fields,
    is_project_asset_create_intent,
)


def extract_candidate_fields(text: str) -> dict[str, str]:
    if not text:
        return {}
    if is_project_asset_create_intent(text):
        return build_project_asset_candidate_fields(text)

    extracted: dict[str, str] = {}
    project = _extract_project(text)
    subject = _extract_subject(text)
    occurred_at = _extract_time(text)
    amount = _extract_amount(text)
    material = _extract_material(text)
    quantity = _extract_quantity(text)
    issue_or_action = _extract_issue_or_action(text)
    fact_record_type = classify_fact_record_type(text)

    if project:
        extracted["primary_project_id"] = project
        extracted["project_name"] = project
    if subject:
        extracted["primary_subject_id"] = subject
        extracted["subject_name"] = subject
    if occurred_at:
        extracted["occurred_at"] = occurred_at
    if amount:
        extracted["amount_text"] = amount
    if material:
        extracted["material_asset_id"] = material
    if quantity:
        extracted["quantity_text"] = quantity
    if issue_or_action:
        extracted["fact_summary"] = issue_or_action
        extracted["issue_or_action"] = issue_or_action
    extracted["fact_record_type"] = fact_record_type

    return extracted


def build_candidate_summary(extracted_fields: dict[str, str], text: str) -> str:
    existing_summary = extracted_fields.get("candidate_summary")
    if existing_summary:
        return existing_summary

    summary_parts = []
    for key in ("project_name", "subject_name", "occurred_at", "issue_or_action", "amount_text"):
        value = extracted_fields.get(key)
        if value:
            summary_parts.append(str(value))
    if summary_parts:
        return "；".join(summary_parts)
    return text[:60]


def _extract_project(text: str) -> str:
    return _clean_project_value(_extract_by_rule("primary_project_id", text).replace(" ", ""))


def _extract_subject(text: str) -> str:
    return _clean_subject_value(_extract_by_rule("primary_subject_id", text))


def _extract_time(text: str) -> str:
    return _extract_by_rule("occurred_at", text)


def _extract_amount(text: str) -> str:
    return re.sub(r"\s+", "", _extract_by_rule("amount_text", text))


def _extract_material(text: str) -> str:
    return _extract_by_rule("material_asset_id", text)


def _extract_quantity(text: str) -> str:
    return re.sub(r"\s+", "", _extract_by_rule("quantity_text", text))


def _extract_by_rule(field_name: str, text: str) -> str:
    for pattern in L1_FIELD_EXTRACTION_RULES.get(field_name, ()):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ""


def _clean_project_value(value: str) -> str:
    separators = ("在", "到", "去", "给", "把", "从", "于", "：", ":")
    cleaned = value.strip()
    last_separator_index = max((cleaned.rfind(separator) for separator in separators), default=-1)
    if last_separator_index >= 0 and last_separator_index < len(cleaned) - 1:
        return cleaned[last_separator_index + 1 :].strip()
    return cleaned


def _clean_subject_value(value: str) -> str:
    return re.sub(r"^(今天|昨天|昨日|明天|上午|下午|晚上|本周|上周|下周)", "", value.strip()).strip()


def _extract_issue_or_action(text: str) -> str:
    matched = [keyword for keyword in L1_ISSUE_KEYWORD_RULES if keyword in text]
    if "尾款" in text and ("付" in text or "付款" in text) and "付款" not in matched:
        matched.insert(0, "付款")
    return "、".join(matched)
