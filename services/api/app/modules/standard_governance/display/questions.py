"""标准治理只读约束层：关键字段反问模板配置
Source: docs/dev_basis/罗盘系统正式开发依据包_v1.0.0/罗盘系统正式开发依据包_v1.0.0/30_标准治理/10_关键字段反问口径.md
注意：本文件只落位字段族绑定结构，不接入 S2，不生成反问结果。
"""

from ..rules.field_rules import FIELD_PROMPT_RULES

QUESTION_FIELD_FAMILIES = {
    "subject": {
        "label": "主体字段",
        "typical_content": ["录入人", "经手人", "责任主体", "确认主体", "客户", "甲方", "供应商", "班组", "外部主体"],
    },
    "project": {
        "label": "项目字段",
        "typical_content": ["项目 ID", "项目名称", "项目阶段", "项目归属", "组织归属"],
    },
    "object": {
        "label": "对象字段",
        "typical_content": ["对象类型", "对象 ID", "对象名称", "资料对象", "物资对象", "主体对象"],
    },
    "fact_type": {
        "label": "事实类型字段",
        "typical_content": [
            "施工",
            "沟通",
            "财务",
            "物资",
            "资料",
            "问题风险",
            "决策变更",
            "关系",
            "出勤",
            "履历",
            "责任确认",
            "商务维护",
            "复盘反馈",
        ],
    },
    "time": {
        "label": "时间字段",
        "typical_content": ["发生时间", "记录时间", "确认时间", "上传时间", "外部提交时间"],
    },
    "source": {
        "label": "来源字段",
        "typical_content": ["来源类型", "来源主体", "来源渠道", "来源记录", "外部回执"],
    },
    "evidence": {
        "label": "证据字段",
        "typical_content": ["附件", "截图", "聊天记录", "照片", "文件", "签字", "回执", "资料引用"],
    },
    "amount": {
        "label": "金额字段",
        "typical_content": ["金额", "币种", "单价", "数量", "扣款", "赔付", "付款", "结算口径"],
    },
    "responsibility": {
        "label": "责任字段",
        "typical_content": ["责任主体", "责任范围", "责任原因", "责任金额", "责任确认状态"],
    },
    "confirmation": {
        "label": "确认字段",
        "typical_content": ["确认主体", "确认范围", "确认时间", "确认依据", "授权关系"],
    },
    "status": {
        "label": "状态字段",
        "typical_content": ["候选", "待补", "挂起", "待确认", "正式", "作废", "归档"],
    },
    "risk": {
        "label": "风险字段",
        "typical_content": ["风险等级", "风险来源", "风险事项", "阻断原因"],
    },
    "permission": {
        "label": "权限字段",
        "typical_content": ["可见范围", "操作范围", "确认范围", "外部可见范围"],
    },
    "traceability": {
        "label": "追溯字段",
        "typical_content": ["版本", "快照", "操作日志", "审计记录", "payload_hash", "双时间戳"],
    },
    "external_display": {
        "label": "外部展示字段",
        "typical_content": ["展示对象", "展示范围", "脱敏要求", "分享对象", "导出用途"],
    },
}

QUESTION_TEMPLATES_BY_FIELD_FAMILY = {
    field_family: [] for field_family in QUESTION_FIELD_FAMILIES
}

QUESTION_PROMPTS_BY_FIELD = FIELD_PROMPT_RULES

FIELD_TO_QUESTION_FAMILY = {
    "primary_subject_id": "subject",
    "linked_subject_ids": "subject",
    "created_by": "subject",
    "confirmed_by": "confirmation",
    "primary_project_id": "project",
    "linked_project_ids": "project",
    "object_asset_id": "object",
    "object_asset_type": "object",
    "object_asset_name": "object",
    "fact_record_type": "fact_type",
    "fact_type": "fact_type",
    "fact_summary": "fact_type",
    "occurred_at": "time",
    "recorded_at": "time",
    "confirmed_at": "time",
    "source_type": "source",
    "source_record_id": "source",
    "source_payload_id": "source",
    "evidence_refs": "evidence",
    "risk_level": "risk",
    "validation_status": "status",
    "visibility_scope": "permission",
    "audit_trace_id": "traceability",
    "payload_hash": "traceability",
    "external_display_allowed": "external_display",
    "desensitization_required": "external_display",
}

QUESTION_TEMPLATE_TODO = (
    "10_关键字段反问口径.md 定义关键字段族、触发条件和组织原则，"
    "未定义可直接落位的完整自然语言反问模板库。"
)
