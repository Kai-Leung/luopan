"""标准治理字段规则中台。

只沉淀字段规则、显示规则、反问规则和候选文本抽取规则；不执行 S2，不写 L2。
"""
from typing import Any, Mapping, Optional

FIELD_REQUIRED_RULES = (
    "primary_project_id",
    "primary_subject_id",
    "occurred_at",
)

FIELD_OPTIONAL_RULES = (
    "linked_project_ids",
    "linked_subject_ids",
    "source_record_ids",
    "evidence_refs",
    "record_title",
    "record_summary",
)

FIELD_TEXT_REQUIRED_RULES = (
    "fact_summary",
)

FIELD_CONDITIONAL_RULES = (
    {
        "field_name": "object_asset_name",
        "fact_record_type": ("construction_record",),
        "issue_keyword": ("防水", "施工", "维修", "现场", "返工"),
    },
    {
        "field_name": "evidence_refs",
        "risk_level": ("high", "blocking"),
    },
    {
        "field_name": "confirmation_scope",
        "risk_level": ("high", "blocking"),
        "issue_keyword": ("付款", "尾款", "收款", "结算", "金额", "签证", "变更", "赔偿"),
    },
    {
        "field_name": "source_record_id",
        "source_type": (
            "uploaded_document",
            "chat_record",
            "external_feedback",
            "interface_callback",
            "external_collaboration",
        ),
    },
    {
        "field_name": "document_asset_type",
        "fact_record_type": ("document_record",),
    },
    {
        "field_name": "material_asset_id",
        "fact_record_type": ("material_flow_record", "purchase_record"),
    },
    {
        "field_name": "related_subject_ids",
        "fact_record_type": ("material_flow_record", "purchase_record"),
        "issue_keyword": ("水泥", "材料", "供应商", "采购", "买了", "到货"),
    },
)

FIELD_DISPLAY_RULES = {
    "primary_project_id": "项目",
    "primary_subject_id": "人员/主体",
    "occurred_at": "时间",
    "fact_summary": "事项内容",
    "object_asset_name": "位置/对象",
    "evidence_refs": "证据",
    "confirmation_scope": "确认范围",
    "source_record_id": "来源记录",
    "document_asset_type": "资料类型",
    "material_asset_id": "物资",
    "related_subject_ids": "相关主体",
    "project_name": "项目名称",
    "customer_name": "客户",
    "project_address": "项目地址",
}

FIELD_PROMPT_RULES = {
    "primary_project_id": "请补充项目",
    "primary_subject_id": "请补充人员或主体",
    "occurred_at": "请补充时间",
    "fact_summary": "请补充事项内容",
    "object_asset_name": "请补充位置或对象",
    "evidence_refs": "请补充证据",
    "confirmation_scope": "请补充确认范围",
    "source_record_id": "请补充来源记录",
    "document_asset_type": "请补充资料类型",
    "material_asset_id": "请补充物资",
    "related_subject_ids": "请补充供应商或相关主体",
    "project_name": "请补充项目名称",
    "customer_name": "请补充客户",
    "project_address": "请补充项目地址",
}

FIELD_TEXT_SIGNAL_RULES = {
    "primary_project_id": ("项目", "工地", "地块", "楼栋"),
    "primary_subject_id": (
        "张工",
        "李工",
        "王工",
        "赵工",
        "负责人",
        "责任人",
        "班组",
        "甲方",
        "客户",
        "供应商",
        "经理",
        "主管",
        "师傅",
    ),
    "occurred_at": ("今天", "昨日", "昨天", "明天", "上午", "下午", "晚上", "本周", "上周", "下周"),
    "material_asset_id": ("水泥", "材料"),
}

L1_FIELD_EXTRACTION_RULES = {
    "primary_project_id": (
        r"([\u4e00-\u9fa5A-Za-z0-9]{2,20}项目)",
        r"(万科\s*102|万科102)",
        r"([\u4e00-\u9fa5]{1,8}老师家)",
        r"([\u4e00-\u9fa5A-Za-z0-9]{2,20}(?:工地|地块|楼栋))",
    ),
    "primary_subject_id": (
        r"([\u4e00-\u9fa5]{1,4}师傅)",
        r"([\u4e00-\u9fa5]{1,4}工)",
        r"(客户|甲方|业主|供应商|班组)",
    ),
    "occurred_at": (
        r"(今天|昨天|昨日|明天)",
        r"(\d{1,2}月\d{1,2}日)",
        r"(\d{4}-\d{1,2}-\d{1,2})",
        r"(\d{1,2}/\d{1,2})",
    ),
    "amount_text": (
        r"(尾款\s*\d+(?:\.\d+)?\s*(?:元|万)?)",
        r"(金额\s*\d+(?:\.\d+)?\s*(?:元|万)?)",
        r"(\d+(?:\.\d+)?\s*万元?)",
        r"(\d+(?:\.\d+)?\s*元)",
    ),
}

L1_ISSUE_KEYWORD_RULES = (
    "防水",
    "购买水泥",
    "水泥",
    "结算",
    "付款",
    "尾款",
    "签证",
    "变更",
    "整改",
    "验收",
    "交付",
    "投诉",
    "风险",
    "沟通",
    "回访",
    "考勤",
    "采购",
    "购买",
    "买了",
    "到货",
    "合同",
    "资料",
    "回访",
    "履历",
)


def normalize_payload_for_field_rules(candidate_payload: Mapping[str, Any], text: str) -> dict[str, Any]:
    normalized_payload = {
        **candidate_payload,
        "fact_summary": candidate_payload.get("fact_summary") or text,
    }
    for field_name in FIELD_TEXT_SIGNAL_RULES:
        if _is_missing_value(normalized_payload.get(field_name)) and text_has_field_signal(field_name, text):
            normalized_payload[field_name] = "text_signal"
    return normalized_payload


def find_missing_text_required_fields(payload: Mapping[str, Any]) -> list[str]:
    return [field_name for field_name in FIELD_TEXT_REQUIRED_RULES if _is_missing_value(payload.get(field_name))]


def find_missing_by_field_rules(
    payload: Mapping[str, Any],
    *,
    text: str = "",
    fact_record_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    source_type: Optional[str] = None,
) -> list[str]:
    missing_fields = []
    for field_name in FIELD_REQUIRED_RULES:
        if _is_missing_value(payload.get(field_name)):
            missing_fields.append(field_name)
    for rule in FIELD_CONDITIONAL_RULES:
        field_name = str(rule["field_name"])
        if not conditional_rule_matches(
            rule,
            text=text,
            fact_record_type=fact_record_type,
            risk_level=risk_level,
            source_type=source_type,
        ):
            continue
        if _is_missing_value(payload.get(field_name)) and field_name not in missing_fields:
            missing_fields.append(field_name)
    return missing_fields


def build_field_question_prompts(missing_fields: list[str]) -> list[str]:
    return [FIELD_PROMPT_RULES[field_name] for field_name in missing_fields if field_name in FIELD_PROMPT_RULES]


def build_field_validation_hints(missing_fields: list[str]) -> list[str]:
    return [f"字段缺口：{FIELD_DISPLAY_RULES.get(field_name, field_name)}" for field_name in missing_fields]


def infer_fact_record_type(candidate_payload: Mapping[str, Any], text: str) -> Optional[str]:
    value = candidate_payload.get("fact_record_type") or candidate_payload.get("fact_type")
    if isinstance(value, str) and value:
        return value
    return None


def infer_source_type(candidate_payload: Mapping[str, Any]) -> Optional[str]:
    value = candidate_payload.get("source_type")
    if isinstance(value, str) and value:
        return value
    raw_payload = candidate_payload.get("raw_payload")
    if isinstance(raw_payload, Mapping):
        value = raw_payload.get("source_type")
        if isinstance(value, str) and value:
            return value
    return None


def text_has_field_signal(field_name: str, text: str) -> bool:
    tokens = FIELD_TEXT_SIGNAL_RULES.get(field_name, ())
    if field_name == "occurred_at" and any(char.isdigit() for char in text):
        return True
    return _text_has_any_issue_keyword(text, tokens)


def conditional_rule_matches(
    rule: Mapping[str, Any],
    *,
    text: str,
    fact_record_type: Optional[str],
    risk_level: Optional[str],
    source_type: Optional[str],
) -> bool:
    if "fact_record_type" in rule and fact_record_type not in rule["fact_record_type"]:
        return False
    if "risk_level" in rule and risk_level not in rule["risk_level"]:
        return False
    if "source_type" in rule and source_type not in rule["source_type"]:
        return False
    if "issue_keyword" in rule and not _text_has_any_issue_keyword(text, rule["issue_keyword"]):
        return False
    return True


def _text_has_any_issue_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _is_missing_value(value: Any) -> bool:
    return value is None or value == "" or value == []
