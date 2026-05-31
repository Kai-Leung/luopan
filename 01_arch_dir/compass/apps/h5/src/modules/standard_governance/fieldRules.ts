export const FIELD_REQUIRED_RULES = [
  "primary_project_id",
] as const;

export const FIELD_OPTIONAL_RULES = [
  "linked_project_ids",
  "linked_subject_ids",
  "source_record_ids",
  "evidence_refs",
  "record_title",
  "record_summary",
] as const;

export const FIELD_CONDITIONAL_RULES = [
  {
    fieldName: "object_asset_name",
    factRecordType: ["construction_record"],
    issueKeyword: ["防水", "施工", "维修", "现场", "返工"],
  },
  {
    fieldName: "evidence_refs",
    riskLevel: ["high", "blocking"],
  },
  {
    fieldName: "confirmation_scope",
    riskLevel: ["high", "blocking"],
    issueKeyword: ["付款", "尾款", "收款", "结算", "金额", "签证", "变更", "赔偿"],
  },
  {
    fieldName: "source_record_id",
    sourceType: ["uploaded_document", "chat_record", "external_feedback", "interface_callback", "external_collaboration"],
  },
  {
    fieldName: "document_asset_type",
    factRecordType: ["document_record"],
  },
  {
    fieldName: "material_asset_id",
    factRecordType: ["material_flow_record"],
  },
  {
    fieldName: "related_subject_ids",
    issueKeyword: ["水泥", "材料", "供应商", "采购", "买了", "到货"],
  },
] as const;

export const FIELD_DISPLAY_RULES: Record<string, string> = {
  primary_project_id: "项目",
  primary_subject_id: "人员/主体",
  occurred_at: "时间",
  fact_summary: "事项内容",
  object_asset_name: "位置/对象",
  evidence_refs: "证据",
  confirmation_scope: "确认范围",
  source_record_id: "来源记录",
  document_asset_type: "资料类型",
  material_asset_id: "物资",
  related_subject_ids: "相关主体",
};

export const FIELD_PROMPT_RULES: Record<string, string> = {
  primary_project_id: "请补充项目",
  primary_subject_id: "请补充人员或主体",
  occurred_at: "请补充时间",
  fact_summary: "请补充事项内容",
  object_asset_name: "请补充位置或对象",
  evidence_refs: "请补充证据",
  confirmation_scope: "请补充确认范围",
  source_record_id: "请补充来源记录",
  document_asset_type: "请补充资料类型",
  material_asset_id: "请补充物资",
  related_subject_ids: "请补充供应商或相关主体",
};
