"""标准治理只读约束层测试
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/03_枚举总表.md
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/04_状态口径总表.md
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/02_字段规范总表.md
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/08_校验规则口径.md
"""

import pytest
from pathlib import Path
import re


def _find_repo_root() -> Path:
    """向上查找仓库根目录（包含 apps/ 和 services/ 的 compass 目录或者包含 backend/ 和 frontend/ 的目录）。
    ARCH_DIR 结构: compass/ ├─ apps/h5/ └─ services/api/
    Compass 工作区结构: compass/ ├─ backend/ └─ frontend/
    """
    p = Path(__file__).resolve()
    while p.parent != p:
        if (p / "backend").is_dir() and (p / "frontend").is_dir():
            return p
        if (p / "apps").is_dir() and (p / "services").is_dir():
            return p
        p = p.parent
    raise RuntimeError(f"Cannot find repo root from {__file__}")


def _frontend_src() -> Path:
    """返回前端源码目录。兼容 ARCH_DIR 结构（apps/h5/）和 Compass 工作区结构（frontend/）。"""
    root = _find_repo_root()
    if (root / "frontend").is_dir():
        return root / "frontend" / "src"
    if (root / "apps" / "h5").is_dir():
        return root / "apps" / "h5" / "src"
    raise RuntimeError(f"Cannot find frontend src from {root}")


from app.modules.standard_governance.enums.fact_types import (
    ENUM_CATEGORY_MAP,
    KNOWN_ENUM_CATEGORIES,
    FactRecordType,
)
from app.modules.standard_governance.enums.source_types import (
    SourceType,
)
from app.modules.standard_governance.rules.field_rules import (
    FIELD_CONDITIONAL_RULES,
    FIELD_DISPLAY_RULES,
    FIELD_OPTIONAL_RULES,
    FIELD_PROMPT_RULES,
    FIELD_REQUIRED_RULES,
)
from app.modules.standard_governance.display.fields import (
    KNOWN_FIELD_NAMES,
)
from app.modules.standard_governance.rules.fact_record_types import (
    FACT_RECORD_TYPE_BOUNDARIES,
    FACT_RECORD_TYPE_DISPLAY,
    FACT_RECORD_TYPE_KEYWORDS,
    FACT_RECORD_TYPE_RULES,
    classify_fact_record_type,
)
from app.modules.standard_governance.display.questions import (
    FIELD_TO_QUESTION_FAMILY,
    QUESTION_FIELD_FAMILIES,
    QUESTION_PROMPTS_BY_FIELD,
    QUESTION_TEMPLATE_TODO,
    QUESTION_TEMPLATES_BY_FIELD_FAMILY,
)
from app.modules.standard_governance.rules.risk_rules import (
    BLOCKING_RISK_KEYWORDS,
    HIGH_RISK_KEYWORDS,
    RISK_KEYWORD_MAPPING,
    RISK_LEVEL_VALUES,
    RiskLevel,
    match_risk_keywords,
)
from app.modules.standard_governance.enums.status_types import KNOWN_STATUS_GROUPS, STATUS_GROUP_MAP
from app.modules.standard_governance.validators import (
    find_missing_required_fields,
    find_missing_field_rule_fields,
    is_known_enum_name,
    is_known_field,
    is_known_status_group,
    is_valid_enum,
    is_valid_fact_type,
    is_valid_risk_level,
    is_valid_source_type,
    is_valid_status,
    require_known_field,
    require_required_fields,
    require_valid_enum,
    require_valid_fact_type,
    require_valid_risk_level,
    require_valid_source_type,
    require_valid_status,
)

SOURCE_TYPE_DEV_BASIS_VALUES = {
    "manual_input",
    "uploaded_document",
    "image_input",
    "audio_input",
    "chat_record",
    "external_feedback",
    "system_generated",
    "ai_assisted",
    "interface_callback",
    "template_output",
    "view_output",
    "manual_confirmation",
    "system_validation",
    "feedback_return",
    "external_collaboration",
}

FACT_RECORD_TYPE_DEV_BASIS_VALUES = {
    "construction_record",
    "financial_record",
    "material_flow_record",
    "document_record",
    "communication_service_record",
    "issue_risk_record",
    "decision_change_record",
    "relationship_record",
    "attendance_record",
    "resume_record",
    "business_maintenance_record",
    "acceptance_delivery_record",
    "purchase_record",
    "other_fact_record",
}

RISK_LEVEL_DEV_BASIS_VALUES = {"none", "low", "medium", "high", "blocking"}

QUESTION_FIELD_FAMILY_DEV_BASIS_VALUES = {
    "subject",
    "project",
    "object",
    "fact_type",
    "time",
    "source",
    "evidence",
    "amount",
    "responsibility",
    "confirmation",
    "status",
    "risk",
    "permission",
    "traceability",
    "external_display",
}


def _extract_ts_enum_values(source: str, enum_name: str) -> set[str]:
    match = re.search(rf"export enum {enum_name} \{{(?P<body>.*?)\n\}}", source, re.S)
    if not match:
        return set()
    return set(re.findall(r'"([^"]+)"', match.group("body")))


def test_valid_enum_value():
    assert is_valid_enum("object_asset_type", "project_asset")
    assert is_valid_enum("fact_record_type", "construction_record")
    assert is_valid_enum("source_type", "manual_input")


def test_invalid_enum_value():
    assert not is_valid_enum("object_asset_type", "fake_type")
    with pytest.raises(ValueError, match="无效的枚举值"):
        require_valid_enum("object_asset_type", "fake_type")


def test_unknown_enum_name():
    assert not is_known_enum_name("unknown_enum_name")
    assert not is_valid_enum("unknown_enum_name", "anything")


def test_known_enum_names_are_mapped():
    assert set(ENUM_CATEGORY_MAP.keys()) == KNOWN_ENUM_CATEGORIES


def test_standard_governance_layered_imports_are_available():
    from app.modules.standard_governance.display.fields import KNOWN_FIELD_NAMES as layered_fields
    from app.modules.standard_governance.display.questions import QUESTION_PROMPTS_BY_FIELD as layered_prompts
    from app.modules.standard_governance.enums.fact_types import FactRecordType as layered_fact_type
    from app.modules.standard_governance.enums.source_types import SourceType as layered_source_type
    from app.modules.standard_governance.enums.status_types import CandidateStatus as layered_candidate_status
    from app.modules.standard_governance.enums.status_types import STATUS_GROUP_MAP as layered_status_map
    from app.modules.standard_governance.rules.fact_record_types import FACT_RECORD_TYPE_RULES as layered_fact_rules
    from app.modules.standard_governance.rules.field_rules import FIELD_REQUIRED_RULES as layered_required_rules
    from app.modules.standard_governance.rules.risk_rules import RiskLevel as layered_risk_level

    assert layered_source_type is SourceType
    assert layered_fact_type is FactRecordType
    assert layered_candidate_status.__name__ == "CandidateStatus"
    assert layered_risk_level is RiskLevel
    assert layered_status_map is STATUS_GROUP_MAP
    assert layered_fields is KNOWN_FIELD_NAMES
    assert layered_prompts is QUESTION_PROMPTS_BY_FIELD
    assert layered_fact_rules is FACT_RECORD_TYPE_RULES
    assert layered_required_rules is FIELD_REQUIRED_RULES


def test_source_type_contains_only_dev_basis_values():
    assert {item.value for item in SourceType} == SOURCE_TYPE_DEV_BASIS_VALUES
    assert len(SourceType) == 15


def test_fact_record_type_contains_only_dev_basis_values():
    assert {item.value for item in FactRecordType} == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    assert len(FactRecordType) == 14
    assert FactRecordType.ACCEPTANCE_DELIVERY_RECORD.value == "acceptance_delivery_record"


def test_fact_record_type_rules_cover_all_14_types():
    assert set(FACT_RECORD_TYPE_RULES.keys()) == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    assert set(FACT_RECORD_TYPE_DISPLAY.keys()) == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    assert set(FACT_RECORD_TYPE_KEYWORDS.keys()) == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    assert set(FACT_RECORD_TYPE_BOUNDARIES.keys()) == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    assert len(FACT_RECORD_TYPE_RULES) == 14


def test_each_fact_record_type_has_display_rule_and_boundary():
    for fact_type in FACT_RECORD_TYPE_DEV_BASIS_VALUES:
        assert FACT_RECORD_TYPE_DISPLAY[fact_type]
        assert FACT_RECORD_TYPE_RULES[fact_type]["description"]
        assert FACT_RECORD_TYPE_BOUNDARIES[fact_type]
    assert FACT_RECORD_TYPE_KEYWORDS["other_fact_record"] == ()


def test_communication_and_issue_risk_are_separate_rules():
    assert classify_fact_record_type("今天客户沟通了售后服务安排") == "communication_service_record"
    assert classify_fact_record_type("今天客户投诉漏水并提示质量风险") == "issue_risk_record"
    assert FACT_RECORD_TYPE_DISPLAY["communication_service_record"] == "沟通与服务记录"
    assert FACT_RECORD_TYPE_DISPLAY["issue_risk_record"] == "问题与风险记录"


def test_other_fact_record_is_only_fallback():
    assert classify_fact_record_type("今天有一条无法识别的普通事项") == "other_fact_record"
    assert classify_fact_record_type("今天张师傅做了厨房防水") == "construction_record"


def test_frontend_and_backend_standard_enums_are_consistent():
    repo_root = _find_repo_root()
    frontend_enums = (
        _frontend_src() / "modules" / "standard_governance" / "enums.ts"
    ).read_text(encoding="utf-8")

    assert _extract_ts_enum_values(frontend_enums, "SourceType") == SOURCE_TYPE_DEV_BASIS_VALUES
    assert (
        _extract_ts_enum_values(frontend_enums, "FactRecordType")
        == FACT_RECORD_TYPE_DEV_BASIS_VALUES
    )


def test_frontend_fact_record_type_display_rules_exist():
    repo_root = _find_repo_root()
    frontend_fact_rules = (
        _frontend_src()
        / "modules"
        / "standard_governance"
        / "factRecordTypes.ts"
    ).read_text(encoding="utf-8")

    for fact_type in FACT_RECORD_TYPE_DEV_BASIS_VALUES:
        assert f"{fact_type}:" in frontend_fact_rules
    assert 'communication_service_record: "沟通与服务记录"' in frontend_fact_rules
    assert 'issue_risk_record: "问题与风险记录"' in frontend_fact_rules
    assert 'other_fact_record: "其他事实记录"' in frontend_fact_rules


def test_h5_uses_fact_record_type_display_mapping():
    repo_root = _find_repo_root()
    # 组件拆分后，FACT_RECORD_TYPE_DISPLAY 在 h5Interaction.ts 中消费
    h5_interaction = (_frontend_src() / "modules" / "input_flow" / "h5Interaction.ts").read_text(
        encoding="utf-8"
    )

    assert "FACT_RECORD_TYPE_DISPLAY" in h5_interaction
    assert "payload.fact_record_type" in h5_interaction
    assert "construction_record：" not in h5_interaction


def test_risk_level_contains_only_dev_basis_values():
    assert {item.value for item in RiskLevel} == RISK_LEVEL_DEV_BASIS_VALUES
    assert set(RISK_LEVEL_VALUES) == RISK_LEVEL_DEV_BASIS_VALUES


def test_risk_level_does_not_contain_blocked():
    assert "blocked" not in {item.value for item in RiskLevel}
    assert RiskLevel.BLOCKING.value == "blocking"


def test_governance_status_still_contains_blocked():
    assert is_valid_status("validation_status", "blocked")
    assert "blocked" in [item.value for item in STATUS_GROUP_MAP["validation_status"]]


def test_risk_keyword_mapping_is_controlled_by_standard_governance():
    assert set(RISK_KEYWORD_MAPPING.keys()) == RISK_LEVEL_DEV_BASIS_VALUES
    assert RISK_KEYWORD_MAPPING["high"] == list(HIGH_RISK_KEYWORDS)
    assert RISK_KEYWORD_MAPPING["blocking"] == list(BLOCKING_RISK_KEYWORDS)
    assert match_risk_keywords("今天涉及签证和金额确认").risk_level == RiskLevel.HIGH.value
    assert match_risk_keywords("今天提交阻断事项").risk_level == RiskLevel.BLOCKING.value


def test_frontend_and_backend_risk_level_are_consistent():
    repo_root = _find_repo_root()
    frontend_risks = (
        _frontend_src() / "modules" / "standard_governance" / "risks.ts"
    ).read_text(encoding="utf-8")

    assert _extract_ts_enum_values(frontend_risks, "RiskLevel") == RISK_LEVEL_DEV_BASIS_VALUES
    assert '"blocked"' not in frontend_risks


def test_frontend_and_backend_risk_keyword_mapping_are_consistent():
    repo_root = _find_repo_root()
    frontend_risks = (
        _frontend_src() / "modules" / "standard_governance" / "risks.ts"
    ).read_text(encoding="utf-8")

    for item in RiskLevel:
        assert f"RiskLevel.{item.name}" in frontend_risks
    assert '"blocked"' not in frontend_risks


def test_question_field_families_come_from_dev_basis():
    assert set(QUESTION_FIELD_FAMILIES.keys()) == QUESTION_FIELD_FAMILY_DEV_BASIS_VALUES
    assert QUESTION_FIELD_FAMILIES["subject"]["label"] == "主体字段"
    assert QUESTION_FIELD_FAMILIES["project"]["label"] == "项目字段"
    assert QUESTION_FIELD_FAMILIES["fact_type"]["label"] == "事实类型字段"
    assert QUESTION_FIELD_FAMILIES["external_display"]["label"] == "外部展示字段"


def test_question_templates_are_empty_until_dev_basis_provides_templates():
    assert set(QUESTION_TEMPLATES_BY_FIELD_FAMILY.keys()) == QUESTION_FIELD_FAMILY_DEV_BASIS_VALUES
    assert all(templates == [] for templates in QUESTION_TEMPLATES_BY_FIELD_FAMILY.values())
    assert QUESTION_TEMPLATE_TODO


def test_field_required_optional_conditional_rules_are_defined():
    assert set(FIELD_REQUIRED_RULES) == {"primary_project_id"}
    assert "evidence_refs" in FIELD_OPTIONAL_RULES
    assert all(rule["field_name"] in KNOWN_FIELD_NAMES for rule in FIELD_CONDITIONAL_RULES)
    assert any("fact_record_type" in rule for rule in FIELD_CONDITIONAL_RULES)
    assert any("risk_level" in rule for rule in FIELD_CONDITIONAL_RULES)
    assert any("source_type" in rule for rule in FIELD_CONDITIONAL_RULES)
    assert any("issue_keyword" in rule for rule in FIELD_CONDITIONAL_RULES)


def test_field_rule_missing_detection_ignores_optional_fields():
    payload = {
        "primary_project_id": "宝山项目",
        "primary_subject_id": "张工",
        "occurred_at": "今天",
    }

    assert find_missing_field_rule_fields(payload) == []


def test_field_rule_missing_detection_checks_required_fields():
    assert find_missing_field_rule_fields({"primary_subject_id": "张工"}) == ["primary_project_id"]


def test_low_risk_construction_detail_missing_does_not_block():
    payload = {
        "primary_project_id": "宝山项目",
        "primary_subject_id": "张工",
        "occurred_at": "今天",
    }

    assert find_missing_field_rule_fields(
        payload,
        text="今天张工在宝山项目做防水",
        fact_record_type="construction_record",
    ) == []


def test_field_rule_condition_not_matched_does_not_mark_missing():
    payload = {
        "primary_project_id": "宝山项目",
        "primary_subject_id": "张工",
        "occurred_at": "今天",
    }

    assert find_missing_field_rule_fields(payload, text="今天张工在宝山项目普通记录") == []


def test_question_prompts_are_user_readable_for_internal_fields():
    assert QUESTION_PROMPTS_BY_FIELD["primary_project_id"] == "请补充项目"
    assert "primary_project_id" not in QUESTION_PROMPTS_BY_FIELD["primary_project_id"]


def test_field_display_rules_are_user_readable():
    assert FIELD_DISPLAY_RULES["primary_project_id"] == "项目"
    assert FIELD_DISPLAY_RULES["primary_subject_id"] == "人员/主体"
    assert "primary_project_id" not in FIELD_DISPLAY_RULES.values()


def test_field_prompt_rules_are_rule_center_output():
    assert FIELD_PROMPT_RULES["primary_project_id"] == "请补充项目"
    assert FIELD_PROMPT_RULES["related_subject_ids"] == "请补充供应商或相关主体"
    assert QUESTION_PROMPTS_BY_FIELD is FIELD_PROMPT_RULES


def test_question_templates_bind_standard_fields_to_field_families():
    assert FIELD_TO_QUESTION_FAMILY["primary_project_id"] == "project"
    assert FIELD_TO_QUESTION_FAMILY["primary_subject_id"] == "subject"
    assert FIELD_TO_QUESTION_FAMILY["occurred_at"] == "time"
    assert FIELD_TO_QUESTION_FAMILY["fact_summary"] == "fact_type"


def test_frontend_and_backend_question_field_families_are_consistent():
    repo_root = _find_repo_root()
    frontend_questions = (
        _frontend_src() / "modules" / "standard_governance" / "questions.ts"
    ).read_text(encoding="utf-8")

    for field_family in QUESTION_FIELD_FAMILY_DEV_BASIS_VALUES:
        assert f"{field_family}:" in frontend_questions
    assert "QUESTION_TEMPLATES_BY_FIELD_FAMILY" in frontend_questions
    assert "FIELD_TO_QUESTION_FAMILY" in frontend_questions
    assert "QUESTION_TEMPLATE_TODO" in frontend_questions


def test_frontend_field_rules_file_exports_rule_center_structures():
    repo_root = _find_repo_root()
    frontend_field_rules = (
        _frontend_src()
        / "modules"
        / "standard_governance"
        / "fieldRules.ts"
    ).read_text(encoding="utf-8")

    for export_name in [
        "FIELD_REQUIRED_RULES",
        "FIELD_OPTIONAL_RULES",
        "FIELD_CONDITIONAL_RULES",
        "FIELD_DISPLAY_RULES",
        "FIELD_PROMPT_RULES",
    ]:
        assert f"export const {export_name}" in frontend_field_rules
    assert "primary_project_id: \"项目\"" in frontend_field_rules
    assert "primary_project_id: \"请补充项目\"" in frontend_field_rules


def test_valid_status_value():
    assert is_valid_status("fact_record_status", "candidate")
    assert is_valid_status("validation_status", "passed")
    assert is_valid_status("confirmation_status", "confirmed")


def test_invalid_status_value():
    assert not is_valid_status("fact_record_status", "fake_status")
    with pytest.raises(ValueError, match="无效的状态值"):
        require_valid_status("fact_record_status", "fake_status")


def test_unknown_status_group():
    assert not is_known_status_group("unknown_status_group")
    assert not is_valid_status("unknown_status_group", "candidate")


def test_known_status_groups_are_mapped():
    assert set(STATUS_GROUP_MAP.keys()) == KNOWN_STATUS_GROUPS


def test_field_existence():
    assert is_known_field("fact_record_type")
    assert is_known_field("source_type")
    assert is_known_field("validation_status")
    assert "fact_record_type" in KNOWN_FIELD_NAMES


def test_unknown_field():
    assert not is_known_field("fake_field_name")
    with pytest.raises(ValueError, match="未知字段名"):
        require_known_field("fake_field_name")


def test_required_field_missing_detection():
    payload = {
        "source_type": "manual_input",
        "fact_type": "",
    }

    assert find_missing_required_fields(
        payload,
        ["source_type", "fact_type", "risk_level"],
    ) == ["fact_type", "risk_level"]
    with pytest.raises(ValueError, match="缺少必填字段"):
        require_required_fields(payload, ["source_type", "fact_type", "risk_level"])


def test_required_field_unknown_name_is_rejected():
    with pytest.raises(ValueError, match="未知字段名"):
        find_missing_required_fields({}, ["fake_field_name"])


def test_risk_level_validation_helpers():
    assert is_valid_risk_level("low")
    assert is_valid_risk_level("medium")
    assert is_valid_risk_level("high")
    assert is_valid_risk_level("blocking")
    assert not is_valid_risk_level("blocked")
    with pytest.raises(ValueError, match="无效的风险等级"):
        require_valid_risk_level("blocked")


def test_source_type_validation_helpers():
    assert is_valid_source_type("manual_input")
    assert is_valid_source_type("external_collaboration")
    assert not is_valid_source_type("manual_text")
    with pytest.raises(ValueError, match="无效的枚举值"):
        require_valid_source_type("manual_text")


def test_fact_type_validation_helpers():
    assert is_valid_fact_type("construction_record")
    assert is_valid_fact_type("financial_record")
    assert is_valid_fact_type("other_fact_record")
    assert not is_valid_fact_type("finance_record")
    assert not is_valid_fact_type("fake_fact_type")
    with pytest.raises(ValueError, match="无效的枚举值"):
        require_valid_fact_type("fake_fact_type")


def test_frontend_standard_validation_helpers_exist():
    repo_root = _find_repo_root()
    frontend_validators = (
        _frontend_src()
        / "modules"
        / "standard_governance"
        / "validators.ts"
    ).read_text(encoding="utf-8")

    for function_name in [
        "isKnownField",
        "requireKnownField",
        "isValidEnum",
        "requireValidEnum",
        "isValidStatus",
        "requireValidStatus",
        "findMissingRequiredFields",
        "requireRequiredFields",
        "isValidRiskLevel",
        "requireValidRiskLevel",
        "isValidSourceType",
        "requireValidSourceType",
        "isValidFactType",
        "requireValidFactType",
    ]:
        assert f"function {function_name}" in frontend_validators
