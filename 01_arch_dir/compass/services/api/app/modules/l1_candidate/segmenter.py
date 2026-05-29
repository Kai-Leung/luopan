"""L1 候选文本拆分工具。"""

import re

from app.modules.standard_governance.rules.project_asset_rules import is_project_asset_create_intent


def extract_raw_text(raw_payload: dict) -> str:
    for key in ("text", "raw_text", "content"):
        value = raw_payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def split_candidate_texts(text: str) -> list[str]:
    if not text:
        return [""]
    if is_project_asset_create_intent(text):
        return [text]
    split_parts = [part.strip() for part in re.split(r"[，,；;。]\s*", text) if part.strip()]
    parts: list[str] = []
    for part in split_parts:
        if parts and _is_amount_continuation(part):
            parts[-1] = f"{parts[-1]}，{part}"
            continue
        parts.append(part)
    return parts or [text]


def _is_amount_continuation(text: str) -> bool:
    return bool(re.fullmatch(r"(金额)?\s*\d+(?:\.\d+)?\s*(?:元|万元?|万)?", text))
